//! Pilot ABI. Foreign pointers must reference valid caller-owned memory.
//! Supported hosts are64-bit; u32 lengths/indices widen to usize without loss.
#![deny(unsafe_op_in_unsafe_fn)]
use rl_core::{EngineError, MemoriaJogo, Registers, Routine, World};
use std::{
    cell::RefCell,
    collections::BTreeMap,
    panic::{catch_unwind, AssertUnwindSafe},
    ptr, slice,
    sync::{Mutex, OnceLock},
};

pub const ABI_VERSION: u32 = 0x00010000;
const MAX_BLOCKS: u32 = 65536;
const MAX_BYTES: usize = 64 * 1024 * 1024;
#[repr(C)]
pub struct RlBloco {
    pub address: u32,
    pub length: u32,
    pub data: *const u8,
}
struct Registry {
    next: u64,
    worlds: BTreeMap<u64, World>,
}
static REGISTRY: OnceLock<Mutex<Registry>> = OnceLock::new();
thread_local! { static LAST_ERROR: RefCell<String> = const { RefCell::new(String::new()) }; }
#[derive(Debug)]
enum AbiError {
    InvalidArgument,
    InvalidHandle,
    Memory(EngineError),
    UnknownRoutine,
    UnsupportedPath(EngineError),
    BufferTooSmall,
    Panic,
    Poisoned,
    ResourceLimit,
    VersionMismatch,
}
impl AbiError {
    fn code(&self) -> i32 {
        match self {
            Self::InvalidArgument => 1,
            Self::InvalidHandle => 2,
            Self::Memory(_) => 3,
            Self::UnknownRoutine => 4,
            Self::UnsupportedPath(_) => 5,
            Self::BufferTooSmall => 6,
            Self::Panic => 7,
            Self::Poisoned => 8,
            Self::ResourceLimit => 9,
            Self::VersionMismatch => 10,
        }
    }
    fn message(&self) -> String {
        match self {
            Self::Memory(e) | Self::UnsupportedPath(e) => e.to_string(),
            _ => format!("{self:?}"),
        }
    }
}
impl From<EngineError> for AbiError {
    fn from(e: EngineError) -> Self {
        match e {
            EngineError::UnknownRoutine(_) => Self::UnknownRoutine,
            EngineError::UnsupportedThreadGetter { .. } => Self::UnsupportedPath(e),
            EngineError::InvalidTickRate => Self::InvalidArgument,
            _ => Self::Memory(e),
        }
    }
}
type Result<T> = std::result::Result<T, AbiError>;
fn status(f: impl FnOnce() -> Result<()>) -> i32 {
    let outcome = catch_unwind(AssertUnwindSafe(f)).unwrap_or(Err(AbiError::Panic));
    match outcome {
        Ok(()) => {
            LAST_ERROR.with(|e| e.borrow_mut().clear());
            0
        }
        Err(error) => {
            LAST_ERROR.with(|e| *e.borrow_mut() = error.message());
            error.code()
        }
    }
}
fn with_registry<T>(f: impl FnOnce(&mut Registry) -> Result<T>) -> Result<T> {
    let mut registry = REGISTRY
        .get_or_init(|| {
            Mutex::new(Registry {
                next: 1,
                worlds: BTreeMap::new(),
            })
        })
        .lock()
        .map_err(|_| AbiError::Poisoned)?;
    f(&mut registry)
}
fn with_world<T>(handle: u64, f: impl FnOnce(&mut World) -> Result<T>) -> Result<T> {
    with_registry(|r| f(r.worlds.get_mut(&handle).ok_or(AbiError::InvalidHandle)?))
}
#[no_mangle]
pub extern "C" fn rl_versao() -> u32 {
    ABI_VERSION
}

/// # Safety
/// `output` is writable and properly aligned; outputs do not alias inputs.
#[no_mangle]
pub unsafe extern "C" fn rl_criar_mundo(
    version: u32,
    rate: u32,
    epoch_ms: u32,
    output: *mut u64,
) -> i32 {
    status(|| {
        if version != ABI_VERSION {
            return Err(AbiError::VersionMismatch);
        }
        if output.is_null() {
            return Err(AbiError::InvalidArgument);
        }
        let world = World::new(rate, epoch_ms)?;
        let handle = with_registry(|r| {
            let handle = r.next;
            r.next = r.next.checked_add(1).ok_or(AbiError::ResourceLimit)?;
            r.worlds.insert(handle, world);
            Ok(handle)
        })?;
        unsafe {
            output.write(handle);
        }
        Ok(())
    })
}
#[no_mangle]
pub extern "C" fn rl_liberar_mundo(handle: u64) -> i32 {
    status(|| {
        with_registry(|r| {
            r.worlds
                .remove(&handle)
                .map(|_| ())
                .ok_or(AbiError::InvalidHandle)
        })
    })
}
/// # Safety
/// `blocks` references `count` aligned descriptors. Each data points to length
/// readable bytes for this call; no pointer is retained, and no overlap with outputs.
#[no_mangle]
pub unsafe extern "C" fn rl_carregar_blocos(
    handle: u64,
    blocks: *const RlBloco,
    count: u32,
) -> i32 {
    status(|| {
        if count > MAX_BLOCKS {
            return Err(AbiError::ResourceLimit);
        }
        if count != 0 && blocks.is_null() {
            return Err(AbiError::InvalidArgument);
        }
        let descriptors = if count == 0 {
            &[]
        } else {
            unsafe { slice::from_raw_parts(blocks, count as usize) }
        }; // u32 count fits supported64-bit usize.
        let mut total = 0usize;
        for block in descriptors {
            if block.length == 0 || block.data.is_null() {
                return Err(AbiError::InvalidArgument);
            }
            total = total
                .checked_add(block.length as usize)
                .ok_or(AbiError::ResourceLimit)?; // u32 length fits64-bit usize.
            if total > MAX_BYTES {
                return Err(AbiError::ResourceLimit);
            }
        }
        let mut memory = MemoriaJogo::default();
        for block in descriptors {
            let bytes =
                unsafe { slice::from_raw_parts(block.data, block.length as usize) }.to_vec();
            memory.declare(block.address, bytes)?;
        }
        with_world(handle, |world| {
            world.replace_memory(memory)?;
            Ok(())
        })
    })
}
/// # Safety
/// `registers` is a writable aligned Registers; unchanged on failure.
#[no_mangle]
pub unsafe extern "C" fn rl_executar_rotina(
    handle: u64,
    routine: u32,
    registers: *mut Registers,
) -> i32 {
    status(|| {
        if registers.is_null() {
            return Err(AbiError::InvalidArgument);
        }
        let routine = Routine::try_from(routine)?;
        let input = unsafe { registers.read() };
        let output = with_world(handle, |world| Ok(world.step(routine, input)?))?;
        unsafe {
            registers.write(output);
        }
        Ok(())
    })
}
/// # Safety
/// `output` is writable and aligned.
#[no_mangle]
pub unsafe extern "C" fn rl_quantidade_blocos(handle: u64, output: *mut u32) -> i32 {
    status(|| {
        if output.is_null() {
            return Err(AbiError::InvalidArgument);
        }
        let count = with_world(handle, |world| {
            u32::try_from(world.project()?.blocks().count()).map_err(|_| AbiError::ResourceLimit)
        })?;
        unsafe {
            output.write(count);
        }
        Ok(())
    })
}
/// # Safety
/// address/required are distinct aligned writable u32 pointers. Buffer is
/// writable for capacity bytes when nonnull; no pointers alias. Metadata is
/// written on BufferTooSmall; byte buffer is untouched. Query with null/zero.
#[no_mangle]
pub unsafe extern "C" fn rl_projetar_bloco(
    handle: u64,
    index: u32,
    address: *mut u32,
    buffer: *mut u8,
    capacity: u32,
    required: *mut u32,
) -> i32 {
    status(|| {
        if address.is_null() || required.is_null() {
            return Err(AbiError::InvalidArgument);
        }
        let memory = with_world(handle, |world| Ok(world.project()?))?;
        let (base, bytes) = memory
            .blocks()
            .nth(index as usize)
            .ok_or(AbiError::InvalidArgument)?;
        let length = u32::try_from(bytes.len()).map_err(|_| AbiError::ResourceLimit)?;
        unsafe {
            address.write(base);
            required.write(length);
        }
        if capacity < length {
            return Err(AbiError::BufferTooSmall);
        }
        if buffer.is_null() {
            return Err(AbiError::InvalidArgument);
        }
        unsafe {
            ptr::copy_nonoverlapping(bytes.as_ptr(), buffer, bytes.len());
        }
        Ok(())
    })
}
#[no_mangle]
pub extern "C" fn rl_avancar_ticks(handle: u64, ticks: u64) -> i32 {
    status(|| {
        with_world(handle, |world| {
            world.clock.advance(ticks);
            Ok(())
        })
    })
}
/// # Safety
/// Outputs are distinct writable aligned u64/u32 pointers.
#[no_mangle]
pub unsafe extern "C" fn rl_relogio(handle: u64, tick: *mut u64, milliseconds: *mut u32) -> i32 {
    status(|| {
        if tick.is_null() || milliseconds.is_null() {
            return Err(AbiError::InvalidArgument);
        }
        let (t, ms) = with_world(handle, |world| {
            Ok((world.clock.tick(), world.clock.milliseconds()))
        })?;
        unsafe {
            tick.write(t);
            milliseconds.write(ms);
        }
        Ok(())
    })
}
/// # Safety
/// Required is writable/aligned. Buffer is writable for capacity bytes, disjoint
/// from required. Copies UTF8 plus NUL; query does not clear the previous error.
#[no_mangle]
pub unsafe extern "C" fn rl_erro_mensagem(
    buffer: *mut u8,
    capacity: u32,
    required: *mut u32,
) -> i32 {
    if required.is_null() {
        return 1;
    }
    LAST_ERROR.with(|error| {
        let text = error.borrow();
        let length = text.len() + 1;
        unsafe {
            required.write(u32::try_from(length).unwrap_or(u32::MAX));
        }
        if (capacity as usize) < length {
            return 6;
        }
        if buffer.is_null() {
            return 1;
        }
        unsafe {
            ptr::copy_nonoverlapping(text.as_ptr(), buffer, text.len());
            buffer.add(text.len()).write(0);
        }
        0
    })
}
