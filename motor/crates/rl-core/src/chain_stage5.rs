//! Register-preserving owner entries for the live chain past construction.
use crate::{EngineError, FrameRegisters, MemoriaJogo, Result};
pub fn entry(m: &mut MemoriaJogo, name: &str, r: FrameRegisters) -> Result<FrameRegisters> {
    match name {
        "SacGetCapacite" | "TuyauEstSortie" | "MineGetCapacite" | "iagVilleSendMessage" => {
            crate::chain_queries::entry(m, name, r)
        }
        "GetCaseCentrale" => Ok(FrameRegisters {
            eax: (r.edi & 0xffff0000).wrapping_add(crate::chain_entry::central_offset(m, r.eax)?),
            esp: r.esp.wrapping_add(4),
            ..r
        }),
        "EnginSetType"
        | "EnginAddVie"
        | "EnginResetFatigue"
        | "EnginSetExperimente"
        | "SetSortEngin" => crate::chain_recruit::entry(m, name, r),
        "EnginSelectPeutEntrer:AL" => {
            let ok = crate::chain_entry::can_enter(m, r.eax & 255, r.edx & 255, r.ebx & 65535)?;
            Ok(FrameRegisters {
                eax: u32::from(ok),
                esp: r.esp.wrapping_add(4),
                ..r
            })
        }
        "BatimentAjouteMatiere:effects" => {
            crate::chain_entry::credit(m, r.eax as u8, r.edx as u16, r.ebx as u8, r.ecx as u16)?;
            Ok(FrameRegisters {
                esp: r.esp.wrapping_add(4),
                ..r
            })
        }
        "SetMiniMap:effects" => {
            crate::player_sight::minimap(m, r.eax as u8, r.ebx as u16, r.edx as u8)?;
            Ok(FrameRegisters {
                esp: r.esp.wrapping_add(4),
                ..r
            })
        }
        "CalculTroupe:effects" => {
            crate::frame_economy::production(m, r.eax & 65535, false, true)?;
            Ok(FrameRegisters {
                esp: r.esp.wrapping_add(4),
                ..r
            })
        }
        "TerrainEstGc"
        | "ChercheVeget"
        | "ChercheGc"
        | "ChercheGcLibre"
        | "TypeEnginPeutEcraser"
        | "IsDirectlyBlocking"
        | "IsIndirectlyBlocking" => {
            let mut q = crate::chain_search::entry(m, name, r)?;
            q.esp = q.esp.wrapping_add(4);
            Ok(q)
        }
        "BatimentPeutAttaquer" | "BatimentInitAttaqueSelect" => {
            let mut q = crate::chain_turret::entry(m, name, r)?;
            q.esp = q.esp.wrapping_add(4);
            Ok(q)
        }
        "ChercheBatimentProximiteCaveOuSanctuaire"
        | "TerrainEstMontagne"
        | "EnginEstVivant"
        | "BatimentGetDecalageConstruction"
        | "GetCaseIndiceBatiment"
        | "ChercheCaseBatiment"
        | "BatimentGetCaseAdjacent"
        | "listDeleteElem"
        | "listUnlinkElem"
        | "iaProbReturnTo"
        | "VoixOffAsk" => {
            let mut q = crate::chain_s1::entry(m, name, r)?;
            q.esp = q.esp.wrapping_add(4);
            Ok(q)
        }
        "MineGetIndice" | "MineEstSurTerrain" | "MineSetWork" | "MineEndWork" | "MineRecolte"
        | "TerrainRecolte" | "AjouteMatiere" => {
            let mut q = crate::chain_work::leaf(m, name, r)?;
            q.esp = q.esp.wrapping_add(4);
            Ok(q)
        }
        "CalculWorkEngin:effects"
        | "EnginRestaureEtat:effects"
        | "BatimentEnleveMatiere:effects"
        | "SetDechargeCaveEngin:effects"
        | "SetDechargeCaveEnginSelect:effects"
        | "EnginSetFatigue:effects"
        | "InitRecruteTroupe:effects"
        | "SortieTroupe:effects"
        | "BatimentRetireColon:effects" => {
            match name {
                "CalculWorkEngin:effects" => {
                    crate::chain_work::work(m, r.eax & 65535)?;
                }
                "EnginRestaureEtat:effects" => crate::chain_restore::restore(m, r.eax & 65535)?,
                "BatimentEnleveMatiere:effects" => {
                    crate::chain_restore::debit(m, r.eax as u8, r.edx as u16, r.ebx as u8)?
                }
                "SetDechargeCaveEngin:effects" => {
                    crate::chain_restore::unload(m, r.eax & 65535, r.edx & 65535)?
                }
                "SetDechargeCaveEnginSelect:effects" => {
                    crate::chain_restore::select_unload(m, r.eax & 255, r.edx & 65535)?
                }
                "EnginSetFatigue:effects" => crate::chain_fatigue::set(m, r.eax & 65535)?,
                "InitRecruteTroupe:effects" => {
                    crate::chain_recruit::init(m, r.eax & 255, r.edx & 255)?;
                }
                "SortieTroupe:effects" => {
                    crate::chain_recruit::sortie(m, r.eax & 65535, r.edx & 255)?
                }
                _ => {
                    crate::chain_recruit::retire_colonist(m, r.eax & 65535)?;
                }
            }
            Ok(FrameRegisters {
                esp: r.esp.wrapping_add(4),
                ..r
            })
        }
        "TerrainRetireMatiere" => {
            let eax = crate::chain_restore::retire_food(m, r.eax & 65535)?;
            Ok(FrameRegisters {
                eax,
                esp: r.esp.wrapping_add(4),
                ..r
            })
        }
        "EnginNextEtape:19:effects" => {
            crate::chain_restore::hunger(m, r.edi & 65535)?;
            Ok(r)
        }
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
        "BagContient" | "BagContientTroupe" | "BagPrend" | "BagRetire" | "BagGetNbContenu"
        | "BagGetCode" | "BagGetType" | "BagAccepte" | "EnginGetBag" => {
            let mut out = crate::chain_bags::body(m, name, r)?;
            out.esp = out.esp.wrapping_add(4);
            Ok(out)
        }
        "BatimentHabitable"
        | "BatimentSetTechnologie"
        | "InitBatimentPlayer"
        | "InitBatimentNeutre"
        | "EnginGetTimeRecrute"
        | "EnginGetRessource"
        | "TypeEnginEstRealisable"
        | "BatimentGetCapacite" => crate::chain_habitation::own(m, name, r),
        "PlaceLibre" => {
            let mut out = crate::chain_entry::place_free(m, r)?;
            out.esp = out.esp.wrapping_add(4);
            Ok(out)
        }
        "BatimentAdjacent:AL" | "BatimentLogeEngin:AL" => {
            let value = if name == "BatimentAdjacent:AL" {
                crate::chain_entry::adjacent(m, r.eax as u16, r.edx as u16)?
            } else {
                crate::chain_entry::lodge(m, r.eax as u16, r.edx as u16)?
            };
            Ok(FrameRegisters {
                eax: u32::from(value),
                esp: r.esp.wrapping_add(4),
                ..r
            })
        }
        "SetEnginRentreBatiment:effects"
        | "SetEnginSelectRentreBatiment:effects"
        | "CalculEntreBatiment:effects"
        | "RetireEngin:effects"
        | "EnginResetType:effects" => {
            match name {
                "SetEnginRentreBatiment:effects" => {
                    crate::chain_entry::set_enter(m, r.eax as u16, r.edx as u16)?
                }
                "SetEnginSelectRentreBatiment:effects" => {
                    crate::chain_entry::select_enter(m, r.eax as u8, r.edx as u16)?
                }
                "CalculEntreBatiment:effects" => crate::chain_entry::calculate(m, r.eax as u16)?,
                "RetireEngin:effects" => crate::chain_entry::retire(m, r.eax as u16)?,
                _ => crate::chain_entry::reset_type(m, r.eax as u16)?,
            }
            Ok(FrameRegisters {
                esp: r.esp.wrapping_add(4),
                ..r
            })
        }
        "EnginNextEtape:state13:effects" => {
            crate::chain_entry::state13(m, r.edi as u16, r.esi)?;
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
