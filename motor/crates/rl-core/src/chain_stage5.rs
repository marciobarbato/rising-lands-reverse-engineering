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
        "BagContient" | "BagContientTroupe" | "BagPrend" | "BagRetire" |
        "BagGetNbContenu" | "BagGetCode" | "BagGetType" | "BagAccepte" | "EnginGetBag" => {
            let mut out = crate::chain_bags::body(m,name,r)?;
            out.esp=out.esp.wrapping_add(4);Ok(out)
        }
        "BatimentHabitable" | "BatimentSetTechnologie" | "InitBatimentPlayer" |
        "InitBatimentNeutre" | "EnginGetTimeRecrute" | "EnginGetRessource" |
        "TypeEnginEstRealisable" | "BatimentGetCapacite" => crate::chain_habitation::own(m,name,r),
        "PlaceLibre" => {let mut out=crate::chain_entry::place_free(m,r)?;out.esp=out.esp.wrapping_add(4);Ok(out)}
        "BatimentAdjacent:AL" | "BatimentLogeEngin:AL" => {
            let value=if name=="BatimentAdjacent:AL" {
                crate::chain_entry::adjacent(m,r.eax as u16,r.edx as u16)?
            }else{crate::chain_entry::lodge(m,r.eax as u16,r.edx as u16)?};
            Ok(FrameRegisters{eax:u32::from(value),esp:r.esp.wrapping_add(4),..r})
        }
        "SetEnginRentreBatiment:effects" | "SetEnginSelectRentreBatiment:effects" |
        "CalculEntreBatiment:effects" | "RetireEngin:effects" | "EnginResetType:effects" => {
            match name {
                "SetEnginRentreBatiment:effects"=>crate::chain_entry::set_enter(m,r.eax as u16,r.edx as u16)?,
                "SetEnginSelectRentreBatiment:effects"=>crate::chain_entry::select_enter(m,r.eax as u8,r.edx as u16)?,
                "CalculEntreBatiment:effects"=>crate::chain_entry::calculate(m,r.eax as u16)?,
                "RetireEngin:effects"=>crate::chain_entry::retire(m,r.eax as u16)?,
                _=>crate::chain_entry::reset_type(m,r.eax as u16)?,
            }
            Ok(FrameRegisters{esp:r.esp.wrapping_add(4),..r})
        }
        "EnginNextEtape:state13:effects"=>{
            crate::chain_entry::state13(m,r.edi as u16,r.esi)?;Ok(r)
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
