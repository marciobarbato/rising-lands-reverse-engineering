//! AI/runtime leaves translated from rotinas_quadro_ia.py, incursao_ia.py and ia.py.
//! Unsupported instruction and monster-spawn paths name their intact-image address.
use crate::{EngineError, MemoriaJogo, Result};

fn stop(name: &'static str, address: u32) -> EngineError {
    EngineError::UnportedCallee { name, address }
}

pub fn call(m: &mut MemoriaJogo, name: &str, args: &[u32]) -> Result<u32> {
    match name {
        "MessageBoxCalcul" => {
            let tail = m.u16(0x507d56)?;
            let head = m.u16(0x507d54)?;
            if tail != head {
                let address = 0x4e7858u32.wrapping_add(518 * u32::from(head));
                let remaining = m.u16(address)?.wrapping_sub(1);
                m.set_u16(address, remaining)?;
                if remaining == 0 {
                    m.set_u16(0x507d54, head.wrapping_add(1) % 256)?;
                    m.set_u8(0x507d58, 0)?;
                }
            }
            Ok(0)
        }
        "ProcessInputGame" => {
            let pointer = 0x4e2458 + 4 * u32::from(args[0] as u8);
            let command = m.u16(m.u32(pointer)?)?;
            let target = if command > 0x27 {
                0x45f2de
            } else {
                m.u32(0x45ed20 + 4 * u32::from(command))?
            };
            if target != 0x45f2de {
                return Err(stop("ProcessInputGame command", target));
            }
            for offset in [0, 2, 4, 6, 8] {
                let address = m.u32(pointer)?.wrapping_add(offset);
                m.set_u16(address, 0)?;
            }
            m.u32(pointer)
        }
        "AvanceMonstre" => advance_monsters(m),
        "iaSolver" => crate::frame_tasks::solve(m, args[0]),
        "CalculNextReflect" => {
            update_player(m, args[0] as u8, args[1] as u8)?;
            Ok(1)
        }
        "iagUnitSendMessage" => send_message(m, args[0] as u16, args[1] as u8),
        "iagUnitNoyau" => Err(stop("iagUnitNoyau", 0x482936)),
        "iagVilleNoyau" => Err(stop("iagVilleNoyau", 0x48453c)),
        "iagRessNoyau" => Err(stop("iagRessNoyau", 0x485183)),
        "iagWarNoyau" => Err(stop("iagWarNoyau", 0x4866d7)),
        "iagUnitDeleteAllGroups" => Err(stop("iagUnitDeleteAllGroups", 0x483d95)),
        "iaProbNew" | "iaProbPost" | "iaProbSleep" | "RaidRule" => {
            crate::frame_tasks::call(m, name, args)
        }
        "iaGroupNew"
        | "iagUnitAddToGroup"
        | "iagUnitGetFirstUnitInGroup"
        | "iagUnitGetNextUnitInGroup"
        | "StockeAction"
        | "ConstruitGroupeMonstre" => crate::frame_raid::call(m, name, args),
        _ => Err(stop("unknown AI frame provider", 0x42c868)),
    }
}

fn update_player(m: &mut MemoriaJogo, player: u8, mission: u8) -> Result<u32> {
    if player > 4 {
        return Err(stop("iaCalculPlayer invalid player", 0x47f927));
    }
    let context = 0x5148b0 + 16 * u32::from(player);
    if player == 4 {
        advance_monsters(m)?;
        return call(m, "iaSolver", &[context]);
    }
    let state = 0x51a98c + 16 * u32::from(player);
    if m.u8(state + 4)? != 0 {
        return Ok(0);
    }
    if m.u32(0x4dfaa8 + 4 * u32::from(player))? == 0
        && m.u16(0x4e1928 + 2 * u32::from(player))? == 0
    {
        let count = m.u8(state + 9)?.wrapping_add(1);
        m.set_u8(state + 9, count)?;
        if count == 10 {
            call(m, "iagUnitDeleteAllGroups", &[u32::from(player)])?;
            m.set_u8(state + 4, 1)?;
            return Ok(0);
        }
    } else {
        m.set_u8(state + 9, 0)?;
    }
    for routine in [
        "iagUnitNoyau",
        "iagVilleNoyau",
        "iagRessNoyau",
        "iagWarNoyau",
        "iaSolver",
    ] {
        let result = if routine == "iaSolver" {
            call(m, routine, &[context])?
        } else {
            call(m, routine, &[u32::from(player), u32::from(mission)])?
        };
        if result != 0 {
            return Ok(result);
        }
    }
    Ok(0)
}

fn advance_monsters(m: &mut MemoriaJogo) -> Result<u32> {
    crate::frame_raid::advance(m)
}

fn send_message(m: &mut MemoriaJogo, unit: u16, message: u8) -> Result<u32> {
    let record = m.u32(0x4e19a0)?.wrapping_add(276 * u32::from(unit));
    let owner = m.u8(record)?;
    if crate::frame_economy::call(m, "PlayerGetType", &[u32::from(owner)])? as u8 != 2 {
        return Ok(0);
    }
    let group = m.u32(record + 0x10c)?;
    let g = if group == u32::MAX {
        0
    } else {
        0x51a9e0u32.wrapping_add(group.wrapping_shl(5))
    };
    if message.wrapping_sub(0x41) > 11 {
        return Ok(0);
    }
    if message != 0x49 {
        return Err(stop("iagUnitSendMessage message handler", 0x482a49));
    }
    if g == 0 {
        return Ok(0);
    }
    let behaviour = m.u8(g + 0x1b)?;
    if behaviour == 0xff {
        return Ok(0);
    }
    let handler = m.u32(m.u32(0x498e94 + 4 * u32::from(behaviour))?.wrapping_add(8))?;
    if handler == 0 {
        return Ok(0);
    }
    Err(stop("iagUnitSendMessage 0x49 behaviour handler", handler))
}

/// Additive isolated validation entry identifiers; argument counts are part of ABI 1.1.
pub fn isolated(id: u32) -> Option<(&'static str, usize)> {
    match id {
        100 => Some(("MessageBoxCalcul", 0)),
        101 => Some(("ProcessInputGame", 1)),
        102 => Some(("AvanceMonstre", 0)),
        103 => Some(("iaSolver", 1)),
        104 => Some(("CalculNextReflect", 2)),
        105 => Some(("iagUnitSendMessage", 3)),
        400 => Some(("iaGroupNew", 2)),
        401 => Some(("iagUnitAddToGroup", 2)),
        402 => Some(("iagUnitGetFirstUnitInGroup", 1)),
        403 => Some(("iagUnitGetNextUnitInGroup", 0)),
        404 => Some(("StockeAction", 4)),
        405 => Some(("ConstruitGroupeMonstre", 2)),
        406 => Some(("iaProbNew", 1)),
        407 => Some(("iaProbPost", 8)),
        408 => Some(("iaProbSleep", 2)),
        409 => Some(("RaidRule", 10)),
        _ => None,
    }
}
