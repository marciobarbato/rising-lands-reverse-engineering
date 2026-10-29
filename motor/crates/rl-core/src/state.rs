use crate::{EngineError, MemoriaJogo, Result, TickClock};

pub const WORLD_SEED: u32 = 0x497164;
pub const CRT_GETTER: u32 = 0x4990cc;
pub const THREAD_DATA: u32 = 0x522244;
pub const SINGLE_THREAD_GETTER: u32 = 0x48e7c7;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct WorldRng {
    pub seed: u32,
}
impl WorldRng {
    pub fn draw(&mut self) -> u32 {
        let quotient = self.seed / 127773;
        let remainder = self.seed % 127773;
        let mut next = remainder
            .wrapping_mul(16807)
            .wrapping_sub(quotient.wrapping_mul(2836));
        if next == 0 || next & 0x80000000 != 0 {
            next = next.wrapping_add(0x7fffffff);
        }
        self.seed = next;
        next
    }
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CrtRng {
    pub seed: u32,
}
impl CrtRng {
    pub fn draw(&mut self) -> u32 {
        self.seed = self.seed.wrapping_mul(0x41c64e6d).wrapping_add(0x3039);
        self.seed.wrapping_shr(16) & 0x7fff
    }
}
/// Four unpacked bytes, units first. The thousands byte may exceed9.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct BcdDigits(pub [u8; 4]);
impl BcdDigits {
    pub fn encode(value: u16) -> Self {
        let mut remaining = u32::from(value);
        let mut digits = [0; 4];
        for (index, divisor) in [(3, 1000), (2, 100), (1, 10), (0, 1)] {
            // Each quotient is <=65; intentional original-byte width.
            digits[index] = (remaining / divisor) as u8;
            remaining %= divisor;
        }
        Self(digits)
    }
    pub fn load(memory: &MemoriaJogo, address: u32) -> Result<Self> {
        let mut digits = [0; 4];
        for (offset, digit) in digits.iter_mut().enumerate() {
            *digit = memory.u8(address.wrapping_add(u32::try_from(offset).expect("four digits")))?;
        }
        Ok(Self(digits))
    }
    pub fn project(&self, memory: &mut MemoriaJogo, address: u32) -> Result<()> {
        // Original store order: thousands, hundreds, tens, units.
        for index in (0..4).rev() {
            memory.set_u8(
                address.wrapping_add(u32::try_from(index).expect("four digits")),
                self.0[index],
            )?;
        }
        Ok(())
    }
    pub fn decode_aliasing(&self, source: u32, destination: u32) -> u16 {
        let mut value = 0u16; // Original zeros destination before reading digits.
        let mut multiplier = 1u16;
        for (offset, original_digit) in self.0.iter().enumerate() {
            let address = source.wrapping_add(u32::try_from(offset).expect("four digits"));
            let digit = if address == destination {
                value.to_le_bytes()[0]
            } else if address == destination.wrapping_add(1) {
                value.to_le_bytes()[1]
            } else {
                *original_digit
            };
            value = value.wrapping_add(u16::from(digit).wrapping_mul(multiplier));
            multiplier = multiplier.wrapping_mul(10);
        }
        value
    }
}

#[repr(C)]
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub struct Registers {
    pub eax: u32,
    pub ebx: u32,
    pub ecx: u32,
    pub edx: u32,
    pub esi: u32,
    pub edi: u32,
    pub ebp: u32,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Routine {
    Random,
    LongRand,
    CrtRand,
    IntToBcd,
    BcdToInt,
}
impl TryFrom<u32> for Routine {
    type Error = EngineError;
    fn try_from(id: u32) -> Result<Self> {
        match id {
            1 => Ok(Self::Random),
            2 => Ok(Self::LongRand),
            3 => Ok(Self::CrtRand),
            4 => Ok(Self::IntToBcd),
            5 => Ok(Self::BcdToInt),
            _ => Err(EngineError::UnknownRoutine(id)),
        }
    }
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GameState {
    pub world_rng: Option<WorldRng>,
    pub crt_rng: Option<CrtRng>,
}
/// Address bindings and opaque, declared bytes belong to projection, not logic.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Projection {
    template: MemoriaJogo,
    crt_seed_address: Option<u32>,
}
impl GameState {
    pub fn load(memory: MemoriaJogo) -> Result<(Self, Projection)> {
        let world_rng = memory
            .optional_u32(WORLD_SEED)?
            .map(|seed| WorldRng { seed });
        let getter = memory.optional_u32(CRT_GETTER)?;
        let thread = memory.optional_u32(THREAD_DATA)?;
        let crt_seed_address = if getter == Some(SINGLE_THREAD_GETTER) {
            thread
                .map(|address| address.wrapping_add(12))
                .filter(|address| *address != 0)
        } else {
            None
        };
        let crt_rng = match crt_seed_address {
            Some(address) => memory.optional_u32(address)?.map(|seed| CrtRng { seed }),
            None => None,
        };
        Ok((
            Self { world_rng, crt_rng },
            Projection {
                template: memory,
                crt_seed_address,
            },
        ))
    }
    pub fn project(&self, layout: &Projection) -> Result<MemoriaJogo> {
        let mut memory = layout.template.clone();
        if let Some(rng) = self.world_rng {
            memory.set_u32(WORLD_SEED, rng.seed)?;
        }
        if let Some(rng) = self.crt_rng {
            let address = layout
                .crt_seed_address
                .ok_or(EngineError::IncompleteField {
                    address: THREAD_DATA,
                })?;
            memory.set_u32(address, rng.seed)?;
        }
        Ok(memory)
    }
}
#[derive(Debug, Clone)]
pub struct World {
    pub state: GameState,
    projection: Projection,
    pub clock: TickClock,
}
impl World {
    pub fn new(rate: u32, epoch: u32) -> Result<Self> {
        Self::load(MemoriaJogo::default(), TickClock::new(rate, epoch)?)
    }
    pub fn load(memory: MemoriaJogo, clock: TickClock) -> Result<Self> {
        let (state, projection) = GameState::load(memory)?;
        Ok(Self {
            state,
            projection,
            clock,
        })
    }
    pub fn project(&self) -> Result<MemoriaJogo> {
        self.state.project(&self.projection)
    }
    pub fn replace_memory(&mut self, memory: MemoriaJogo) -> Result<()> {
        *self = Self::load(memory, self.clock.clone())?;
        Ok(())
    }
    /// An isolated routine call, NOT a game frame. Errors publish no state/register change.
    pub fn step(&mut self, routine: Routine, input: Registers) -> Result<Registers> {
        let mut next = self.clone();
        let mut memory = next.project()?;
        let mut output = input;
        match routine {
            Routine::Random => {
                let rng = next
                    .state
                    .world_rng
                    .as_mut()
                    .ok_or(EngineError::UndeclaredAccess {
                        address: WORLD_SEED,
                        size: 4,
                    })?;
                output.eax = rng.draw();
                memory = next.project()?;
            }
            Routine::LongRand | Routine::CrtRand => {
                let getter = memory.u32(CRT_GETTER)?;
                if getter != SINGLE_THREAD_GETTER {
                    return Err(EngineError::UnsupportedThreadGetter {
                        address: 0x48c513,
                        value: getter,
                    });
                }
                let address = memory.u32(THREAD_DATA)?.wrapping_add(12);
                output.eax = if address == 0 {
                    0
                } else {
                    next.state
                        .crt_rng
                        .as_mut()
                        .ok_or(EngineError::UndeclaredAccess { address, size: 4 })?
                        .draw()
                };
                memory = next.project()?;
            }
            Routine::IntToBcd => {
                // Intentional low16 of original DX; semantic value then projection.
                let digits = BcdDigits::encode(input.edx as u16);
                digits.project(&mut memory, input.eax)?;
                output.eax = 0;
                output.edx = 1; // Original final div bx: AX=0, DX=1.
            }
            Routine::BcdToInt => {
                memory.read(input.eax, 2)?; // Validate destination before original zero/store.
                let digits = BcdDigits::load(&memory, input.edx)?;
                let value = digits.decode_aliasing(input.edx, input.eax);
                memory.set_u16(input.eax, value)?;
                output.edx = 10000; // Original final multiplier, not the converted value.
            }
        }
        // Refresh bindings after writes: BCD buffers may alias an RNG/global.
        next.replace_memory(memory)?;
        *self = next;
        Ok(output)
    }
}
