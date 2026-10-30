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
        "SauveSelectionGroupe" | "RestaureSelectionGroupe" => {
            let mut r = crate::chain_groups::entry(m, name, r)?;
            r.esp = r.esp.wrapping_add(4);
            Ok(r)
        }
        "MiniMapSetPos" | "MiniMapRecentre" | "CalculPosition" | "RechercheDecalageSortie" => {
            let mut r = crate::chain_vision::extra(m, name, r)?;
            r.esp = r.esp.wrapping_add(4);
            Ok(r)
        }
        "EnginGetCentreGroupe" => {
            let mut r = crate::chain_groups::centre(m, r)?;
            r.esp = r.esp.wrapping_add(4);
            Ok(r)
        }
        "BatimentModifyMap:effects" => {
            // The owner's contract leaves EAX/EDX scratch unspecified. This
            // test adapter compares effects and the preserved register file.
            crate::chain_vision::structure_minimap(m, r.eax as u16, r.edx as u8)?;
            Ok(FrameRegisters {
                esp: r.esp.wrapping_add(4),
                ..r
            })
        }
        "RechercheDecalageSortie:AX" => {
            // Explicit u16 semantic return: this adapter makes no claim for
            // the original's uninitialized EAX upper stack word.
            let value = crate::chain_vision::exit_cell(m, r.eax & 65535)?;
            Ok(FrameRegisters {
                eax: u32::from(value),
                esp: r.esp.wrapping_add(4),
                ..r
            })
        }
        _ => Err(EngineError::UnknownRoutine(0)),
    }
}
