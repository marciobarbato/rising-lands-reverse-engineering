//! Live iaSolver control flow, lists, waits and primitive rules.
//! Resolved instructions are read from the original loaded RULE table, never
//! replaced with an artificial Rust task program.
use crate::{EngineError, MemoriaJogo, Result};
const TASKS: u32 = 0x512320;
const FREE: u32 = 0x5148a0;
const CONTEXTS: u32 = 0x5148b0;
const ACTIVE: u32 = 0x514904;
fn error(name: &'static str, address: u32) -> EngineError {
    EngineError::UnportedCallee { name, address }
}
fn task(index: u32) -> u32 {
    TASKS.wrapping_add(index.wrapping_mul(96))
}
fn put(m: &mut MemoriaJogo, index: u32, offset: u32, value: u32) -> Result<()> {
    m.set_u32(task(index).wrapping_add(offset), value)
}
fn get(m: &MemoriaJogo, index: u32, offset: u32) -> Result<u32> {
    m.u32(task(index).wrapping_add(offset))
}

pub fn new_task(m: &mut MemoriaJogo, kind: u32) -> Result<u32> {
    if kind == 0 || (kind as i32) >= 64 {
        return Ok(u32::MAX);
    }
    let entry = m.u16(0x51a720u32.wrapping_add(kind.wrapping_mul(2)))?;
    if entry == 0 {
        return Ok(u32::MAX);
    }
    let index = m.u32(FREE)?;
    if index == u32::MAX {
        return Ok(index);
    }
    let element = m
        .u32(FREE + 8)?
        .wrapping_mul(index)
        .wrapping_add(m.u32(FREE + 12)?);
    m.set_u32(FREE, m.u32(element)?)?;
    m.set_u32(element, u32::MAX)?;
    m.set_u32(FREE + 4, m.u32(FREE + 4)?.wrapping_sub(1))?;
    m.set_u32(ACTIVE, m.u32(ACTIVE)?.wrapping_add(1))?;
    put(m, index, 4, u32::MAX)?;
    put(m, index, 8, u32::MAX)?;
    let t = task(index);
    m.set_u16(t.wrapping_add(0x5a), kind as u16)?;
    m.set_u16(t.wrapping_add(0x58), 0)?;
    m.set_u8(t.wrapping_add(0x5e), 0)?;
    m.set_u8(t.wrapping_add(0x5f), 0)?;
    put(m, index, 0x10, 0)?;
    m.set_u8(t.wrapping_add(0x5d), 255)?;
    put(m, index, 0x14, 0)?;
    put(m, index, 0xc, u32::from(entry))?;
    Ok(index)
}
pub fn post(m: &mut MemoriaJogo, a: &[u32]) -> Result<u32> {
    let index = new_task(m, a[1])?;
    if index == u32::MAX {
        return Ok(index);
    }
    for (i, value) in a[2..8].iter().enumerate() {
        put(m, index, 0x18 + 4 * i as u32, *value)?;
    }
    m.set_u8(task(index).wrapping_add(0x5c), a[0] as u8)?;
    let header = CONTEXTS.wrapping_add(a[0].wrapping_shl(4));
    let stride = m.u32(header.wrapping_add(8))?;
    let base = m.u32(header.wrapping_add(12))?;
    let mut previous = m.u32(header)?;
    if previous == u32::MAX {
        m.set_u32(header, index)?;
    } else {
        let mut iterations = 0;
        loop {
            let address = base.wrapping_add(stride.wrapping_mul(previous));
            let next = m.u32(address)?;
            if next == u32::MAX {
                m.set_u32(address, index)?;
                break;
            }
            previous = next;
            iterations += 1;
            if iterations > 10000 {
                return Err(error("listLinkElemToTail cyclic list", 0x47d07a));
            }
        }
    }
    m.set_u32(base.wrapping_add(stride.wrapping_mul(index)), u32::MAX)?;
    m.set_u32(
        header.wrapping_add(4),
        m.u32(header.wrapping_add(4))?.wrapping_add(1),
    )?;
    Ok(index)
}
fn remove(m: &mut MemoriaJogo, context: u32, index: u32) -> Result<()> {
    let parent = get(m, index, 4)?;
    if parent != u32::MAX {
        m.set_u8(task(parent).wrapping_add(0x5e), 0)?;
        m.set_u8(task(parent).wrapping_add(0x5f), 1)?;
    }
    let mut previous = u32::MAX;
    let mut current = m.u32(context)?;
    let mut iterations = 0;
    while current != index {
        if current == u32::MAX {
            return Err(error("iaSolver task outside context", 0x47d471));
        }
        previous = current;
        current = get(m, current, 0)?;
        iterations += 1;
        if iterations > 10000 {
            return Err(error("iaSolver cyclic context", 0x47d471));
        }
    }
    let next = get(m, index, 0)?;
    if previous == u32::MAX {
        m.set_u32(context, next)?;
    } else {
        put(m, previous, 0, next)?;
    }
    m.set_u32(
        context.wrapping_add(4),
        m.u32(context.wrapping_add(4))?.wrapping_sub(1),
    )?;
    put(m, index, 0, m.u32(FREE)?)?;
    m.set_u32(FREE, index)?;
    m.set_u32(FREE + 4, m.u32(FREE + 4)?.wrapping_add(1))?;
    m.set_u32(ACTIVE, m.u32(ACTIVE)?.wrapping_sub(1))
}
pub fn sleep(m: &mut MemoriaJogo, index: u32, time: u32) -> Result<()> {
    m.set_u8(task(index).wrapping_add(0x5e), 1)?;
    put(m, index, 0x14, time)
}
fn arguments(m: &MemoriaJogo, index: u32, format: u32, constant: u32) -> Result<Vec<u32>> {
    let count = (format >> 4) & 15;
    let mut result = Vec::with_capacity(count as usize);
    for i in 0..count {
        let source = format.wrapping_shr(8 + 4 * i) & 15;
        result.push(if source == 0 {
            constant
        } else {
            get(m, index, 0x14 + 4 * source)?
        });
    }
    Ok(result)
}
fn div(a: u32, b: u32, address: u32) -> Result<u32> {
    (a as i32)
        .checked_div(b as i32)
        .map(|q| q as u32)
        .ok_or_else(|| error("iaSolver x86 signed division fault", address))
}
pub fn operation(
    m: &mut MemoriaJogo,
    address: u32,
    a: &[u32],
    player: u32,
    index: u32,
) -> Result<u32> {
    let required = match address {
        0x47da7a | 0x4812f4 => 1,
        0x481280 | 0x481296 | 0x4812ac | 0x4812b9 | 0x4812d0 | 0x481302 => 2,
        _ => 0,
    };
    if a.len() < required {
        return Err(error("iaSolver incomplete rule arguments", address));
    }
    match address {
        0x47da7a => {
            sleep(m, index, a[0])?;
            Ok(1)
        }
        0x47f31c => Ok(1),
        0x47f322 => Ok(u32::MAX),
        0x481280 => Ok(if a[0] == a[1] { 1 } else { u32::MAX }),
        0x481296 => Ok(if (a[0] as i32) > (a[1] as i32) {
            1
        } else {
            u32::MAX
        }),
        0x4812ac => Ok(a[0].wrapping_add(a[1])),
        0x4812b9 => Ok(if (a[0] as i32) >= (a[1] as i32) {
            a[0].wrapping_sub(a[1])
        } else {
            0
        }),
        0x4812d0 => Ok(div(a[0], a[1], address)?.wrapping_mul(100)),
        0x4812f4 => Ok(a[0]),
        0x4812f7 => Ok(u32::from(m.u8(0x496fe4)?)),
        0x481302 => {
            if a[1] == 0 {
                Ok(u32::MAX)
            } else {
                div(a[0], a[1], address)
            }
        }
        _ => crate::frame_raid::rule(m, address, a, player, index),
    }
}
pub fn solve(m: &mut MemoriaJogo, context: u32) -> Result<u32> {
    if !(CONTEXTS..=CONTEXTS + 64).contains(&context) || !(context - CONTEXTS).is_multiple_of(16) {
        return Err(error("iaSolver invalid context", 0x47d314));
    }
    let mut index = m.u32(context)?;
    let mut steps = 0;
    while index != u32::MAX {
        let next = get(m, index, 0)?;
        let t = task(index);
        if m.u8(t.wrapping_add(0x5e))? != 0 {
            let time = get(m, index, 0x14)? as i32;
            if time <= 0 {
                index = next;
                continue;
            }
            put(m, index, 0x14, (time - 1) as u32)?;
            if time > 1 {
                index = next;
                continue;
            }
            m.set_u8(t.wrapping_add(0x5e), 0)?;
            m.set_u8(t.wrapping_add(0x5f), 1)?;
            put(m, index, 0x54, 1)?;
        }
        loop {
            steps += 1;
            if steps > 10000 {
                return Err(error("iaSolver instruction budget", 0x47d314));
            }
            let pc = get(m, index, 12)?;
            let instruction = 0x514910u32.wrapping_add(pc.wrapping_mul(20));
            let address = m.u32(instruction)?;
            let format = m.u32(instruction.wrapping_add(4))?;
            let result_slot = format & 15;
            let result;
            if m.u8(t.wrapping_add(0x5f))? != 0 {
                if m.u16(t.wrapping_add(0x58))? != 0 {
                    m.set_u16(t.wrapping_add(0x58), 0)?;
                } else if result_slot != 0 {
                    put(m, index, 0x14 + result_slot * 4, get(m, index, 0x54)?)?;
                }
                m.set_u8(t.wrapping_add(0x5f), 0)?;
                result = get(m, index, 0x54)?;
            } else {
                let a = arguments(m, index, format, m.u32(instruction.wrapping_add(16))?)?;
                if address < 64 {
                    let child = new_task(m, address)?;
                    if child == u32::MAX {
                        remove(m, context, index)?;
                        break;
                    }
                    for (i, value) in a.iter().enumerate() {
                        put(m, child, 0x18 + 4 * i as u32, *value)?;
                    }
                    m.set_u8(task(child).wrapping_add(0x5c), m.u8(t.wrapping_add(0x5c))?)?;
                    put(m, child, 0, get(m, index, 0)?)?;
                    put(m, index, 0, child)?;
                    put(m, child, 4, index)?;
                    put(m, child, 0x14, 0)?;
                    m.set_u8(t.wrapping_add(0x5e), 1)?;
                    m.set_u16(t.wrapping_add(0x58), address as u16)?;
                    break;
                }
                result = operation(
                    m,
                    address,
                    &a,
                    u32::from(m.u8(t.wrapping_add(0x5c))?),
                    index,
                )?;
                if m.u8(t.wrapping_add(0x5e))? != 0 {
                    break;
                }
                if result_slot != 0 {
                    put(m, index, 0x14 + 4 * result_slot, result)?;
                }
            }
            let destination =
                m.u32(instruction.wrapping_add(if result == u32::MAX { 12 } else { 8 }))?;
            if destination <= 3 {
                let parent = get(m, index, 4)?;
                if [1, 2].contains(&destination) && parent != u32::MAX {
                    put(m, parent, 0x54, if destination == 1 { 1 } else { u32::MAX })?;
                }
                remove(m, context, index)?;
                break;
            }
            put(m, index, 12, destination)?;
        }
        index = next;
    }
    Ok(if m.u32(ACTIVE)? != 0 { 0 } else { 0x1a1a000e })
}
pub fn call(m: &mut MemoriaJogo, name: &str, a: &[u32]) -> Result<u32> {
    match name {
        "iaSolver" => solve(m, a[0]),
        "iaProbNew" => new_task(m, a[0]),
        "iaProbPost" => post(m, a),
        "iaProbSleep" => {
            sleep(m, a[0], a[1])?;
            Ok(0)
        }
        "RaidRule" => operation(m, a[0], &a[3..], a[1], a[2]),
        _ => Err(error("unknown task provider", 0x47d314)),
    }
}
