//! Original-width unit and structure frame dispatch, from the accepted Python chain.
use crate::{EngineError, MemoriaJogo, Result};

fn stop(name: &'static str, address: u32) -> EngineError {
    EngineError::UnportedCallee { name, address }
}
fn record(m: &MemoriaJogo, unit: u32) -> Result<u32> {
    Ok(m.u32(0x4e19a0)?.wrapping_add(276 * u32::from(unit as u16)))
}
fn economy(m: &mut MemoriaJogo, name: &str, args: &[u32]) -> Result<u32> {
    crate::frame_economy::call(m, name, args)
}
fn core(m: &mut MemoriaJogo, name: &str, args: &[u32]) -> Result<u32> {
    crate::frame_core::call(m, name, args)
}

pub fn call(m: &mut MemoriaJogo, name: &str, args: &[u32]) -> Result<u32> {
    match name {
        "CalculEnginNextEtape" => next_units(m),
        "CalculBatimentNextEtape" => next_structures(m),
        "EnginNextEtape" => next_unit(m, args[0] as u16),
        "BatimentNextEtape" => next_structure(m, args[0] as u16),
        "EnginTrouveCible" => find_target(m, args[0] as u16),
        "IATestUtilite" => {
            if args[0] as u8 == 1 {
                test_message(m, args[1] as u16)?;
            }
            Ok(0)
        }
        "iagMessTestSendMessageEngin" => {
            test_message(m, args[0] as u16)?;
            Ok(0)
        }
        "EnginOccupeCase" => occupies(m, args[0] as u16, args[1] as u16, args[2] as u8),
        _ => Err(stop("unknown unit frame provider", 0x45442c)),
    }
}
fn test_message(m: &mut MemoriaJogo, unit: u16) -> Result<()> {
    let r = record(m, u32::from(unit))?;
    if m.u8(r + 2)? == m.u8(r + 0x10a)? && m.u8(r + 0x89)? == m.u8(r + 0x10b)? {
        return Ok(());
    }
    m.set_u8(r + 0x10a, m.u8(r + 2)?)?;
    m.set_u8(r + 0x10b, m.u8(r + 0x89)?)?;
    let owner = m.u8(r)?;
    if owner >= 4
        || economy(m, "PlayerGetType", &[u32::from(owner)])? as u8 != 2
        || m.u32(r + 0x10c)? == u32::MAX
    {
        return Ok(());
    }
    Err(stop(
        "iagMessTestSendMessageEngin group-descriptor path",
        0x483f5d,
    ))
}
fn next_units(m: &mut MemoriaJogo) -> Result<u32> {
    m.set_u16(0x4e1a38, 0)?;
    m.set_u16(0x4e1a3a, 0)?;
    for owner in 0..4 {
        for kind in 0..26 {
            m.set_u16(0x4e1a3c + owner * 0x34 + kind * 2, 0)?;
        }
        m.set_u16(0x4e1928 + owner * 2, 0)?;
    }
    m.set_u16(0x4e1930, 0)?;
    for i in 0..800 {
        let r = record(m, i)?;
        let state = m.u8(r + 2)?;
        if state == 0 {
            continue;
        }
        if state != 4 {
            let owner = m.u8(r)?;
            let kind = m.u8(r + 1)?;
            if owner != 200 && owner != 4 {
                let a = 0x4e1a3c + u32::from(owner) * 0x34 + u32::from(kind) * 2;
                m.set_u16(a, m.u16(a)?.wrapping_add(1))?;
            }
            test_message(m, i as u16)?;
            if kind != 17 {
                let a = if owner == m.u8(0x508041)? {
                    0x4e1a3a
                } else {
                    0x4e1a38
                };
                m.set_u16(a, m.u16(a)?.wrapping_add(1))?;
            }
            if owner != 200 && kind != 5 {
                let a = 0x4e1928 + u32::from(owner) * 2;
                m.set_u16(a, m.u16(a)?.wrapping_add(1))?;
            }
        }
        next_unit(m, i as u16)?;
    }
    Ok(0)
}
fn next_structures(m: &mut MemoriaJogo) -> Result<u32> {
    economy(m, "ResetTableauHangar", &[])?;
    let period = m.u16(0x495c02)?;
    if period == 0 {
        return Err(stop("CalculBatimentNextEtape divide by zero", 0x4281e5));
    }
    if m.u32(0x508f7c)? % u32::from(period) == 0 {
        m.set_u8(0x4dfb9b, 0)?;
    }
    for owner in 0..4 {
        m.set_u32(0x4dfaa8 + 4 * owner, 0)?;
    }
    for i in 0..1000 {
        let r = 0x49a0c8 + 276 * i;
        if m.u8(r + 5)? == 0 {
            continue;
        }
        let owner = m.u8(r + 4)?;
        let kind = m.u8(r + 8)?;
        if owner < 4 && ![9, 12, 17].contains(&kind) {
            let a = 0x4dfaa8 + 4 * u32::from(owner);
            m.set_u32(a, m.u32(a)?.wrapping_add(1))?;
        }
        if m.u8(r + 5)? == 3 {
            return Err(stop("DemonteBatiment", 0x4282bb));
        }
        next_structure(m, i as u16)?;
        let cell = core(m, "BatimentGetCase", &[i])?;
        for player in 0..4 {
            if u32::from(m.u8(r + 4)?) == player {
                continue;
            }
            if core(m, "CaseEstDecouverte", &[cell & 0xffff, player])? as u8 != 0 {
                continue;
            }
            if core(m, "BatimentEstDecouvert", &[i, player])? as u8 == 0 {
                continue;
            }
            core(m, "BatimentDecouvre", &[i, player])?;
        }
        for player in 0..4 {
            if u32::from(m.u8(r + 4)?) == player {
                continue;
            }
            let flag = r + 0x110 + player;
            if core(m, "BatimentContourEstIllumine", &[i, player])? as u8 != 0 {
                if m.u8(flag)? == 0 {
                    core(m, "BatimentIllumine", &[i, player, 1])?;
                    m.set_u8(flag, 1)?;
                }
            } else if m.u8(flag)? != 0 {
                core(m, "BatimentIllumine", &[i, player, 0])?;
                m.set_u8(flag, 0)?;
            }
        }
    }
    m.set_u8(0x4dfb50, 0)?;
    Ok(0)
}
fn next_unit(m: &mut MemoriaJogo, unit: u16) -> Result<u32> {
    let n = u32::from(unit);
    let r = record(m, n)?;
    let mut owner = 0;
    let mut kind = 0;
    if m.u8(r + 2)? != 0 {
        owner = m.u8(r)?;
        kind = m.u8(r + 1)?;
        if m.u32(r + 0x104)? != u32::MAX {
            return Err(stop("EnginNextEtape sound handle", 0x454479));
        }
        m.set_u8(r + 0xf9, 0)?;
    }
    let state = m.u8(record(m, n)? + 2)?;
    if state == 0 || state == 4 {
        return switch_state(m, unit, r);
    }
    if m.u8(r + 1)? == 0x10 {
        return Err(stop("EnginNextEtape type-16 animation", 0x4544d7));
    }
    let rr = record(m, n)?;
    let current = m.u8(rr + 1)?;
    let limit = m.u16(0x4965de + 50 * u32::from(current))?;
    let current_owner = m.u8(rr)?;
    let bonus = economy(
        m,
        "BonusGetValEngin",
        &[u32::from(current_owner), u32::from(current), 3, rr],
    )? as u16;
    if i32::from(m.u16(rr + 0x102)?) < i32::from(limit) - i32::from(bonus) {
        return Err(stop("EnginNextEtape reload advance", 0x454587));
    }
    if kind >= 0x10 {
        return Err(stop("EnginNextEtape type >= 16", 0x45459a));
    }
    if kind.wrapping_sub(0xb) <= 5 {
        return Err(stop("EnginNextEtape types 11..16", 0x4545b9));
    }
    if m.u8(r + 2)? != 14 && m.u32(0x508f7c)?.wrapping_add(n) & 31 == 0 {
        let rr = record(m, n)?;
        let current = m.u8(rr + 1)?;
        if owner != 200
            && [
                0, 1, 2, 3, 8, 11, 12, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25,
            ]
            .contains(&current)
        {
            let player_type = economy(m, "PlayerGetType", &[u32::from(owner)])? as u8;
            if ![1, 19].contains(&m.u8(r + 2)?)
                && (![14, 16].contains(&kind) || m.u8(record(m, n)? + 0xda)? != 0)
            {
                let target = find_target(m, unit)? as u16;
                if target != 0xffff {
                    if player_type == 2 {
                        crate::frame_ai::call(
                            m,
                            "iagUnitSendMessage",
                            &[n, 0x49, u32::from(target)],
                        )?;
                    } else if m.u8(r + 2)? == 7 {
                        return Err(stop("SetAttaqueEngin", 0x4547db));
                    }
                }
            }
        }
    }
    if m.u8(record(m, n)? + 0xdc)? & 4 != 0 {
        return Err(stop("EnginNextEtape spell timer", 0x454811));
    }
    let t = m.u8(r + 1)?;
    if t > 25 {
        return Err(stop("EnginNextEtape fatigue type > 25", 0x454869));
    }
    let target = m.u32(0x454344 + 4 * u32::from(t))?;
    if target != 0x454851 {
        return Err(stop("EnginNextEtape fatigue table", target));
    }
    if m.u8(record(m, n)? + 0xdc)? & 4 == 0 {
        core(m, "CalculFatigue", &[n])?;
        if [0, 4].contains(&m.u8(record(m, n)? + 2)?) {
            return Ok(0x454ccd);
        }
        if m.u16(r + 4)? != 4 {
            let rr = record(m, n)?;
            if ![0, 4].contains(&m.u8(rr + 2)?)
                && m.u8(rr + 0x72)? != 0
                && m.u16(rr + 4)? == 0
                && m.u8(r + 0x86)? == 0
                && m.u8(r + 0x87)? == 0
            {
                let owner = m.u8(rr)?;
                if economy(m, "PlayerGetType", &[u32::from(owner)])? as u8 == 2 {
                    crate::frame_ai::call(m, "iagUnitSendMessage", &[n, 0x4b, 0])?;
                } else {
                    return Err(stop("EnginSetFatigue", 0x45498f));
                }
            }
        }
    }
    if m.u8(record(m, n)? + 1)? == 17 {
        return Err(stop("EnginNextEtape type 17", 0x4549c2));
    }
    if m.u8(record(m, n)? + 0x72)? != 0 && m.u8(r + 2)? != 4 {
        let cell = m.u16(r + 8)?;
        core(m, "SetEnginCollision", &[n, u32::from(cell)])?;
    }
    if m.u8(record(m, n)? + 0xdc)? & 2 != 0 {
        return Err(stop("EnginNextEtape bit 1", 0x454ba5));
    }
    if m.u8(record(m, n)? + 0xdc)? & 8 != 0 {
        return Err(stop("EnginNextEtape bit 3", 0x454c0e));
    }
    if m.u8(record(m, n)? + 1)? >= 12 {
        return Err(stop("EnginNextEtape type >= 12 tail", 0x454c70));
    }
    switch_state(m, unit, r)
}
fn switch_state(m: &mut MemoriaJogo, unit: u16, r: u32) -> Result<u32> {
    let state = m.u8(r + 2)?;
    if state > 24 {
        return Ok(0x454ccd);
    }
    let target = m.u32(0x4543c8 + 4 * u32::from(state))?;
    match target {
        0x454ccd => Ok(0x454ccd),
        0x456966 => {
            economy(m, "EnginNextEtape:state7", &[u32::from(unit)])?;
            Ok(0x454ccd)
        }
        0x4563da => {
            if m.u16(r + 0x7e)? != m.u16(r + 8)? {
                core(m, "DeplaceEngin", &[u32::from(unit)])?;
                return Ok(0x454ccd);
            }
            if m.u8(r + 0x91)? != m.u8(r + 0x90)? {
                return Err(stop("EnginNextEtape facing at arrival", 0x455a6f));
            }
            if core(m, "EnginEnArret", &[u32::from(unit)])? as u8 == 0 {
                return Err(stop("EnginNextEtape arrival animation", 0x456408));
            }
            if ![0, 4].contains(&m.u8(r + 2)?) {
                m.set_u8(r + 2, 7)?;
                if unit == m.u16(0x496304)? {
                    return Err(stop("EnginNextEtape path-search arrival", 0x4564c8));
                }
            }
            Ok(0x454ccd)
        }
        _ => Err(stop("EnginNextEtape state switch", target)),
    }
}
fn next_structure(m: &mut MemoriaJogo, structure: u16) -> Result<u32> {
    let kind = m.u8(0x49a0c8 + 276 * u32::from(structure) + 8)?;
    let index = kind.wrapping_sub(1);
    if index > 20 {
        return Ok(0);
    }
    let target = m.u32(0x426880 + 4 * u32::from(index))?;
    if target != 0x426918 {
        return Err(stop("BatimentNextEtape type switch", target));
    }
    economy(m, "BatimentNextEtape:production", &[u32::from(structure)])?;
    Ok(0)
}
fn allied(m: &MemoriaJogo, a: u8, b: u8) -> Result<bool> {
    if a == b {
        return Ok(true);
    }
    if a > 4 || b > 4 {
        return Ok(false);
    }
    Ok(m.u8(m.u32(0x5080a8)?.wrapping_add(20 * u32::from(a) + 6))? & (1u8 << b) != 0)
}
fn attack_types(a: u8, b: u8) -> bool {
    ![10, 17].contains(&b) && (b != 16 || [2, 8].contains(&a))
}
fn distance(a: u16, b: u16) -> u32 {
    let dx = i32::from(a & 255) - i32::from(b & 255);
    let dy = i32::from(a >> 8) - i32::from(b >> 8);
    (dx * dx + dy * dy) as u32
}
fn find_target(m: &MemoriaJogo, unit: u16) -> Result<u32> {
    let r = record(m, u32::from(unit))?;
    let kind = m.u8(r + 1)?;
    let owner = m.u8(r)?;
    let cell = m.u16(r + 8)?;
    let radius = u32::from(m.u8(r + 0xbb)?);
    if [2, 8].contains(&kind) {
        for i in 0..800 {
            let t = record(m, i)?;
            if [0, 4].contains(&m.u8(t + 2)?) || m.u8(t + 0x72)? == 0 {
                continue;
            }
            let other = m.u8(t)?;
            let enemy = if owner != other && (owner == 4 || other == 4) {
                true
            } else {
                owner != 200 && other != 200 && owner != other && !allied(m, owner, other)?
            };
            if !enemy || other == 200 {
                continue;
            }
            if attack_types(kind, m.u8(t + 1)?) && distance(cell, m.u16(t + 8)?) <= radius * radius
            {
                return Ok(i);
            }
        }
    }
    let x = u32::from(cell & 255);
    let y = u32::from(cell >> 8);
    let mut best = 0xffff;
    let mut least = 0xffff;
    let grid = m.u32(0x4e0f38)?;
    for cy in y.saturating_sub(radius)..256.min(y + radius + 1) {
        for cx in x.saturating_sub(radius)..256.min(x + radius + 1) {
            let c = cx + cy * 256;
            let occupation = m.u16(grid.wrapping_add(2 * c))?;
            if occupation & 0xc000 != 0x4000 {
                continue;
            }
            let i = u32::from((occupation & 0x3ff8) >> 3);
            if i >= 800 {
                return Err(stop(
                    "EnginTrouveCible occupant outside unit table",
                    0x453f74,
                ));
            }
            let t = record(m, i)?;
            let other = m.u8(t)?;
            if other == 200 || allied(m, other, owner)? || !attack_types(kind, m.u8(t + 1)?) {
                continue;
            }
            let d = distance(cell, c as u16) & 0xffff;
            if d <= radius * radius && d < least {
                best = i;
                least = d;
            }
        }
    }
    Ok(best)
}
fn occupies(m: &MemoriaJogo, unit: u16, cell: u16, filter: u8) -> Result<u32> {
    let r = record(m, u32::from(unit))?;
    let layer = m.u8(r + 0xab)?;
    if (layer != 0 && filter == 1) || (layer == 0 && filter == 2) || m.u8(r + 2)? == 14 {
        return Ok(0);
    }
    let kind = m.u8(r + 1)?;
    if kind > 25 {
        return Err(stop("EnginOccupeCase type outside domain", 0x44246e));
    }
    let offsets: &[u32] = if [3, 11, 12, 13, 14, 15, 16, 25].contains(&kind) {
        &[0, 1, 0x101, 0x100]
    } else {
        &[0]
    };
    for offset in [8, 0x7c] {
        for &d in offsets {
            if i64::from(m.u16(r + offset)?) - i64::from(d) == i64::from(cell) {
                return Ok(1);
            }
        }
    }
    Ok(0)
}

/// Isolated unit/structure validation entries; no clock tick is advanced.
pub fn isolated(id: u32) -> Option<(&'static str, usize)> {
    match id {
        150 => Some(("CalculEnginNextEtape", 0)),
        151 => Some(("CalculBatimentNextEtape", 0)),
        152 => Some(("EnginNextEtape", 1)),
        153 => Some(("BatimentNextEtape", 1)),
        154 => Some(("EnginTrouveCible", 1)),
        155 => Some(("IATestUtilite", 2)),
        156 => Some(("iagMessTestSendMessageEngin", 1)),
        157 => Some(("EnginOccupeCase", 3)),
        _ => None,
    }
}
