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
        "iaSolver" => {
            let context = args[0];
            if !(0x5148b0..=0x5148f0).contains(&context) || !(context - 0x5148b0).is_multiple_of(16)
            {
                return Err(stop("iaSolver invalid context", 0x47d314));
            }
            // The exact empty linked-list path. No task instruction is silently skipped.
            if m.u32(context)? != u32::MAX {
                return Err(stop("iaSolver active task", 0x47d314));
            }
            Ok(if m.u32(0x514904)? != 0 { 0 } else { 0x1a1a000e })
        }
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
    if m.u8(0x50a9cc)? == 0 {
        m.set_u8(0x50a9cc, 1)?;
        for i in 0..u32::from(m.u16(0x50a9ce)?) {
            m.set_u32(0x50a9d0 + 12 * i + 8, m.u32(0x508f7c)?)?;
        }
    }
    if m.u8(0x496fe4)? == 0x17 {
        if m.u8(0x50b134)? != 0 {
            return Err(stop(
                "AvanceMonstre mission-0x17 pending group post",
                0x47b2d3,
            ));
        }
        return Ok(0);
    }
    let now = m.u32(0x508f7c)?;
    for i in 0..u32::from(m.u16(0x50a9ce)?) {
        let record = 0x50a9d0 + 12 * i;
        let period = m.u16(record + 4)?;
        if period == 0 || (now.wrapping_sub(m.u32(record + 8)?) as i32) < i32::from(period) {
            continue;
        }
        let mask = m.u16(record + 2)?;
        let mut bit = m.u8(record + 6)?;
        let mut found = false;
        for _ in 0..16 {
            bit = bit.wrapping_add(1) & 15;
            if mask & (1u16 << bit) != 0 {
                found = true;
                break;
            }
        }
        if !found {
            bit = 0xff;
        }
        m.set_u8(record + 6, bit)?;
        m.set_u32(record + 8, now)?;
        // ConstruitGroupeMonstre's three original early-return guards are complete.
        let group = m.u8(record + 6)?;
        if group == 0xff || (m.u32(0x50b178)? as i32) >= 0x32 || m.u8(0x50b134)? >= 0x10 {
            continue;
        }
        return Err(stop("ConstruitGroupeMonstre", 0x47a81d));
    }
    let mut i = 0u32;
    while (i as i32) < (m.u32(0x50ae80)? as i32) {
        let entry = 0x50ae84u32.wrapping_add(16u32.wrapping_mul(i));
        if m.u16(entry + 0xe)? == 0x31 {
            let timer = m.u32(entry + 8)?.wrapping_sub(1);
            m.set_u32(entry + 8, timer)?;
            if (timer as i32) <= 0 {
                return Err(stop("AvanceMonstre expired ambush action", 0x47b3d1));
            }
        }
        i = i.wrapping_add(1);
    }
    if m.u8(0x50b134)? != 0 {
        return Err(stop("AvanceMonstre pending attack", 0x47b44c));
    }
    Ok(0)
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
        _ => None,
    }
}
