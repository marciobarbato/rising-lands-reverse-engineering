//! Register-preserving owner entries for the live chain past construction.
use crate::{EngineError, FrameRegisters, MemoriaJogo, Result};
pub fn entry(m: &mut MemoriaJogo, name: &str, r: FrameRegisters) -> Result<FrameRegisters> {
    match name {
        "BatimentNextEtape:cave" | "BatimentNextEtape" => crate::player_cave::entry(m, r),
        "BatimentIllumine" | "BatimentDecouvre" | "IllumineCase" | "EteintCase"
        | "DecouvreCase" => {
            let mut r = crate::chain_vision::entry(m, name, r)?;
            r.esp = r.esp.wrapping_add(4);
            Ok(r)
        }
        _ => Err(EngineError::UnknownRoutine(0)),
    }
}
