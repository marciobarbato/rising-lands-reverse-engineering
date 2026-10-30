//! DeplaceEngin/CalculNextCase/AvanceEngin with shared original grid projections.
use crate::{frame_path, frame_spawn, EngineError, MemoriaJogo, Result};
fn stop(name: &'static str, address: u32) -> EngineError {
    EngineError::UnportedCallee { name, address }
}
fn unit(m: &MemoriaJogo, i: u32) -> Result<u32> {
    frame_spawn::unit(m, i)
}
fn quad(t: u8) -> bool {
    matches!(t, 3 | 11 | 12 | 13 | 14 | 15 | 16 | 25)
}
fn occupy(m: &mut MemoriaJogo, i: u32, cell: u16, insert: bool) -> Result<()> {
    let u = unit(m, i)?;
    let t = m.u8(u + 1)?;
    if t >= 26 {
        return Ok(());
    }
    let mask = if matches!(t, 16 | 17) { 2 } else { 1 };
    let deltas = if quad(t) {
        &[0u16, 1, 257, 256][..]
    } else {
        &[0u16][..]
    };
    for (sub, d) in deltas.iter().enumerate() {
        let c = cell.wrapping_sub(*d);
        let a = m.u32(0x507da8)?.wrapping_add(u32::from(c));
        let old = m.u8(a)?;
        m.set_u8(a, if insert { old | mask } else { old & !mask })?;
        if matches!(t, 16 | 17) {
            continue;
        }
        let tag = 0x4000
            | ((i as u16) << 3)
            | sub as u16
            | if frame_path::CLASSES[t as usize] != 1 {
                4
            } else {
                0
            };
        let a = m.u32(0x4e0f38)?.wrapping_add(2 * u32::from(c));
        let old = m.u16(a)?;
        if insert && old < 0x4000 {
            m.set_u16(u + 0xfa + 2 * sub as u32, old)?;
            m.set_u16(a, tag)?;
        } else if !insert && old == tag {
            m.set_u16(a, m.u16(u + 0xfa + 2 * sub as u32)?)?;
        }
    }
    Ok(())
}
fn occupies(m: &MemoriaJogo, i: u32, cell: u16, mask: u8) -> Result<bool> {
    let u = unit(m, i)?;
    let ab = m.u8(u + 0xab)?;
    if (ab != 0 && mask == 1) || (ab == 0 && mask == 2) || m.u8(u + 2)? == 14 {
        return Ok(false);
    }
    for base in [m.u16(u + 8)?, m.u16(u + 0x7c)?] {
        for d in if quad(m.u8(u + 1)?) {
            &[0i32, 1, 257, 256][..]
        } else {
            &[0i32][..]
        } {
            if i32::from(base) - d == i32::from(cell) {
                return Ok(true);
            }
        }
    }
    Ok(false)
}
fn passage(m: &MemoriaJogo, i: u32, cell: u16) -> Result<(bool, bool)> {
    let u = unit(m, i)?;
    let t = m.u8(u + 1)?;
    if t >= 26 {
        return Err(stop("EnginPeutPasser type", 0x448b9f));
    }
    let mask = 1 + u8::from(m.u8(u + 0xab)? != 0);
    if quad(t) && (cell & 255 == 0 || cell >> 8 == 0) {
        return Ok((false, false));
    }
    let mut allowed = true;
    let mut blockers = false;
    for d in if quad(t) {
        &[0u16, 1, 257, 256][..]
    } else {
        &[0u16][..]
    } {
        let c = cell.wrapping_sub(*d);
        if occupies(m, i, c, mask)?
            || m.u8(m.u32(0x507da8)?.wrapping_add(u32::from(c)))? & mask == 0
        {
            continue;
        }
        let mut candidate = 65535;
        for other in 0..800 {
            let q = unit(m, other)?;
            if matches!(m.u8(q + 2)?, 0 | 4) || m.u8(q + 0x72)? == 0 {
                continue;
            }
            if !occupies(m, other, c, 1 + u8::from(m.u8(q + 0xab)? != 0))? {
                continue;
            }
            if m.u8(q + 1)? == 16 && m.u8(q + 0xab)? != 50 {
                continue;
            }
            candidate = other;
            if m.u8(q + 0xab)? != 0 {
                break;
            }
        }
        blockers |= candidate != 65535;
        let crush = if matches!(t, 12 | 15) && candidate != 65535 {
            let q = unit(m, candidate)?;
            m.u8(q)? != m.u8(u)?
                && matches!(
                    m.u8(q + 1)?,
                    0 | 1 | 2 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 18 | 19 | 22
                )
        } else {
            false
        };
        if !crush {
            allowed = false;
        }
    }
    Ok((allowed, blockers))
}
fn register_step(m: &mut MemoriaJogo, i: u32, cell: u16, d: u8, blockers: bool) -> Result<()> {
    let u = unit(m, i)?;
    if matches!(m.u8(u + 1)?, 12 | 15) && blockers {
        return Err(stop("EnginNextCase crush effects", 0x448d08));
    }
    occupy(m, i, m.u16(u + 0x7c)?, false)?;
    occupy(m, i, m.u16(u + 8)?, true)?;
    occupy(m, i, cell, true)?;
    m.set_u16(u + 0x7c, cell)?;
    m.set_u8(u + 0x90, d)?;
    Ok(())
}
pub fn choose_direct(m: &mut MemoriaJogo, i: u32) -> Result<u32> {
    let u = unit(m, i)?;
    let origin = m.u16(u + 8)?;
    let dest = m.u16(u + 0x7e)?;
    let mut d = frame_path::direction(origin, dest, false);
    for attempt in 0..3 {
        let c = frame_path::neighbor(m, origin, d)?;
        if c != 65535 {
            let (ok, blockers) = passage(m, i, c)?;
            if ok {
                register_step(m, i, c, d, blockers)?;
                m.set_u8(u + 0x8b, 0)?;
                return Ok(1);
            }
            if c == dest {
                m.set_u16(u + 0x7e, m.u16(u + 0x7c)?)?;
                frame_spawn::release(m, i)?;
                m.set_u8(u + 0x88, 0)?;
                return Ok(0);
            }
        }
        d = if attempt == 0 {
            ((i32::from(d) - 3).rem_euclid(16) + 1) as u8
        } else {
            ((u32::from(d) + 1) % 16 + 1) as u8
        };
    }
    m.set_u8(u + 0x88, 3)?;
    m.set_u8(u + 0x8b, 0)?;
    Ok(0)
}
pub fn choose_route(m: &mut MemoriaJogo, i: u32) -> Result<u32> {
    let u = unit(m, i)?;
    let route = frame_path::route(m, i)?;
    let n = m.u16(route)?;
    if n == 0 {
        m.set_u8(u + 0x88, 0)?;
        m.set_u8(u + 0x8b, 0)?;
        return Ok(0);
    }
    let cell = m.u16(route.wrapping_add(2 * u32::from(n)))?;
    let (ok, blockers) = passage(m, i, cell)?;
    if !ok {
        m.set_u8(u + 0x88, 0)?;
        m.set_u8(u + 0x8b, 0)?;
        return Ok(0);
    }
    let d = frame_path::direction(m.u16(u + 8)?, cell, false);
    register_step(m, i, cell, d, blockers)?;
    Ok(1)
}
fn rotate(m: &mut MemoriaJogo, i: u32) -> Result<u32> {
    let u = unit(m, i)?;
    let desired = m.u8(u + 0x90)?;
    let current = m.u8(u + 0x91)?;
    if !(1..=16).contains(&desired) || !(1..=16).contains(&current) {
        return Err(stop("RotateEngin orientation", 0x448599));
    }
    if matches!(m.u8(u + 1)?, 12 | 15) {
        m.set_u8(
            u + 0xda,
            desired.wrapping_sub(1).wrapping_mul(2).wrapping_add(1),
        )?;
    }
    if desired != current {
        let counter = m.u8(u + 0x92)?.wrapping_add(1);
        m.set_u8(u + 0x92, counter)?;
        if counter == m.u8(u + 0x93)? {
            let next = if (i32::from(desired) - i32::from(current)).rem_euclid(16) < 8 {
                current % 16 + 1
            } else if current == 1 {
                16
            } else {
                current - 1
            };
            m.set_u8(u + 0x91, next)?;
            m.set_u8(u + 0x92, 0)?;
        }
    }
    Ok(0)
}
fn can_advance(m: &MemoriaJogo, u: u32) -> Result<bool> {
    let desired = m.u8(u + 0x90)?;
    let current = m.u8(u + 0x91)?;
    if !(1..=16).contains(&desired) || !(1..=16).contains(&current) {
        return Err(stop("CalculNextCase orientation", 0x4490fd));
    }
    Ok(matches!(
        (i32::from(current) - i32::from(desired)).rem_euclid(16),
        0 | 1 | 2 | 14 | 15
    ))
}
fn animation(m: &mut MemoriaJogo, i: u32) -> Result<()> {
    let u = unit(m, i)?;
    let t = m.u8(u + 1)?;
    if t == 17 {
        return Err(stop("AnimBallonStatic", 0x447b2f));
    }
    if t == 16 || t > 25 {
        return Ok(());
    }
    let n = m.u8(u + 0xa9)?.wrapping_add(1);
    m.set_u8(u + 0xa9, n)?;
    if n == m.u8(u + 0xa7)? {
        let frames = m.u8(u + 0xa5)?;
        if frames == 0 {
            return Err(stop("CalculNextCase animation division", 0x449039));
        }
        m.set_u8(
            u + 0xa4,
            ((u16::from(m.u8(u + 0xa4)?) + 1) % u16::from(frames)) as u8,
        )?;
        m.set_u8(u + 0xa9, 0)?;
    }
    Ok(())
}
pub fn advance(m: &mut MemoriaJogo, i: u32, discount: u8) -> Result<u32> {
    let u = unit(m, i)?;
    let t = m.u8(u + 1)?;
    let owner = m.u8(u)?;
    let dest = m.u16(u + 0x7c)?;
    let fatigue = !matches!(m.u8(u + 2)?, 0 | 4) && m.u8(u + 0x72)? != 0 && (t <= 10 || t == 25);
    let limit = m
        .u16(0x4965dc + 50 * u32::from(t))?
        .wrapping_add(u16::from(m.u8(u + 0xf8)?));
    let bonus = if owner < 4 {
        crate::frame_economy::bonus(m, u32::from(owner), u32::from(t), 0, 0)? as u16
    } else {
        0
    };
    let limit = limit.wrapping_add(bonus);
    let count = m.u16(u + 0x74)?.wrapping_add(1);
    if fatigue && count >= limit && m.u16(u + 4)? == 0 {
        return Err(stop("AvanceEngin hunger without provisions", 0x448704));
    }
    if m.u8(m.u32(0x507d74)?.wrapping_add(u32::from(dest)))? == 0x46
        && m.u8(m.u32(0x507dac)?.wrapping_add(u32::from(dest)))? != owner
        && !matches!(t, 16 | 17)
    {
        return Err(stop("AvanceEngin hostile trap", 0x448704));
    }
    let step = m.u8(u + 0x98)?.wrapping_sub(discount);
    let (dx, dy) = frame_path::vector(m.u8(u + 0x90)?);
    m.set_u8(
        u + 0x86,
        (i32::from(m.u8(u + 0x86)?) + dx * i32::from(step)) as u8,
    )?;
    m.set_u8(
        u + 0x87,
        (i32::from(m.u8(u + 0x87)?) + dy * i32::from(step)) as u8,
    )?;
    let progress = m.u8(u + 0x97)?.wrapping_add(step);
    m.set_u8(u + 0x97, progress)?;
    let arrived = progress > 31;
    if arrived {
        m.set_u8(u + 0x86, 0)?;
        m.set_u8(u + 0x87, 0)?;
        m.set_u8(u + 0x97, 0)?;
        let current = m.u16(u + 8)?;
        occupy(m, i, current, false)?;
        occupy(m, i, dest, true)?;
        frame_spawn::minimap(m, owner, current, 5)?;
        if !matches!(owner, 4 | 200) {
            return Err(stop("AvanceEngin EteintTerrain", 0x476e82));
        }
        m.set_u16(u + 8, dest)?;
        frame_spawn::minimap(m, owner, dest, 4)?;
        let route = frame_path::route(m, i)?;
        let n = m.u16(route)?;
        if n != 0 {
            m.set_u16(route, n - 1)?;
        }
    }
    if fatigue {
        m.set_u16(u + 0x74, count)?;
        if count >= limit {
            m.set_u16(u + 0x74, 0)?;
            m.set_u16(u + 4, m.u16(u + 4)?.wrapping_sub(1))?;
        }
    }
    Ok(u32::from(arrived))
}
pub fn next_case(m: &mut MemoriaJogo, i: u32) -> Result<u32> {
    let u = unit(m, i)?;
    if m.u8(u + 0x86)? == 0 && m.u8(u + 0x87)? == 0 {
        match m.u8(u + 0x88)? {
            0 => {
                choose_direct(m, i)?;
            }
            5 => {
                choose_route(m, i)?;
            }
            _ => {}
        }
    }
    if m.u16(u + 0x7c)? == m.u16(u + 8)? {
        return Ok(0);
    }
    animation(m, i)?;
    if m.u8(u + 0x91)? != m.u8(u + 0x90)? {
        rotate(m, i)?;
    }
    let local = m.u8(0x508041)?;
    if m.u8(u)? == local
        && (11..=16).contains(&m.u8(u + 1)?)
        && m.u8(m
            .u32(0x507d78 + 4 * u32::from(local))?
            .wrapping_add(u32::from(m.u16(u + 8)?)))?
            & 31
            == 0
    {
        return Err(stop("CalculNextCase local volume", 0x4490c3));
    }
    if can_advance(m, u)? {
        advance(m, i, 0)?;
    }
    Ok(0)
}
pub fn displace(m: &mut MemoriaJogo, i: u32) -> Result<u32> {
    let u = unit(m, i)?;
    let state = m.u8(u + 0x88)?;
    if matches!(state, 0 | 5) || (state == 3 && (m.u8(u + 0x86)? != 0 || m.u8(u + 0x87)? != 0)) {
        return next_case(m, i);
    }
    match state {
        1 => m.set_u8(u + 0x88, 0)?,
        3 => {
            if m.u8(0x4e0f36)? == 0 {
                frame_path::begin(m, i)?;
                m.set_u8(u + 0x88, 4)?;
            }
        }
        4 => {
            if m.u8(0x496302)? == 0 {
                return Err(stop("DeplaceEngin unfinished continuation", 0x4493c8));
            }
            let status = m.u8(0x4e0f4c)?;
            if m.u8(0x4e0f37)? != 0 {
                if m.u8(u + 2)? == 2 && status == 2 {
                    m.set_u16(u + 0x7e, m.u16(0x4e0f4a)?)?;
                }
                m.set_u8(u + 0x88, 5)?;
            } else if status == 8 {
                m.set_u8(u + 0x88, 6)?;
                m.set_u8(u + 0x8b, 0)?;
            } else {
                return Err(stop("EnginDebloqueNextCase", 0x4493f9));
            }
            frame_spawn::release(m, i)?;
        }
        6 => {
            let n = m.u8(u + 0x8b)?.wrapping_add(1);
            if n == 20 {
                m.set_u8(u + 0x88, 3)?;
                m.set_u8(u + 0x8b, 0)?;
            } else {
                m.set_u8(u + 0x88, 6)?;
                m.set_u8(u + 0x8b, n)?;
            }
        }
        _ => {}
    }
    Ok(0)
}
pub fn isolated(id: u32) -> Option<(&'static str, usize)> {
    Some(match id {
        450 => ("GetFreeCell", 2),
        451 => ("CreerEngin", 4),
        452 => ("EnginSetPlayer", 2),
        453 => ("PlaceEngin", 1),
        454 => ("EnginGetCase", 1),
        455 => ("GetRandCaseChamps", 0),
        456 => ("GetRandCaseTypeBatPlayer", 2),
        457 => ("Chemin_Accessible", 2),
        458 => ("SetDeplaceEngin", 2),
        459 => ("EnginEnArret", 1),
        460 => ("DeplaceEngin", 1),
        461 => ("CalculNextCase", 1),
        462 => ("AvanceEngin", 2),
        463 => ("EnginNextCase", 1),
        464 => ("EnginNextCaseChemin", 1),
        465 => ("CheminCalcul", 0),
        466 => ("OptimiseChemin", 2),
        467 => ("Chemin_Verouille", 7),
        468 => ("RotateEngin", 1),
        469 => ("SetMiniMap", 3),
        470 => ("EnginSetType", 4),
        471 => ("EnginSetTypeCaract", 1),
        472 => ("TestLigneOptimise", 4),
        473 => ("ResetEnginCollision", 2),
        474 => ("EnginPeutPasser", 2),
        475 => ("ChercheIndiceEngin", 1),
        476 => ("CalculDirection", 2),
        477 => ("CalculDirCase", 2),
        478 => ("Distance2d", 4),
        479 => ("ResetOrdre", 1),
        480 => ("EnginEstVivant", 1),
        481 => ("TerrainEnCollision", 2),
        482 => ("ResetCollision", 2),
        483 => ("memset", 3),
        484 => ("GetNumIndiceTypeBatiment", 3),
        485 => ("GetCaseIndiceBatiment", 1),
        486 => ("PlayerGetColor", 1),
        487 => ("EnginTypeGetCapacite", 1),
        _ => return None,
    })
}
pub fn call(m: &mut MemoriaJogo, name: &str, a: &[u32]) -> Result<u32> {
    match name {
        "TestLigneOptimise" => frame_path::test_line(m, a[0], a[1] as u16, a[2] as u16, a[3]),
        "ResetEnginCollision" => {
            occupy(m, a[0], a[1] as u16, false)?;
            Ok(0)
        }
        "EnginPeutPasser" => Ok(u32::from(passage(m, a[0], a[1] as u16)?.0)),
        "ChercheIndiceEngin" => {
            let cell = a[0] as u16;
            let mut out = 65535;
            for i in 0..800 {
                let u = unit(m, i)?;
                if matches!(m.u8(u + 2)?, 0 | 4) || m.u8(u + 0x72)? == 0 {
                    continue;
                }
                let ab = m.u8(u + 0xab)?;
                if !occupies(m, i, cell, 1 + u8::from(ab != 0))? {
                    continue;
                }
                if m.u8(u + 1)? == 16 && ab != 50 {
                    continue;
                }
                out = i;
                if ab != 0 {
                    break;
                }
            }
            Ok(out)
        }
        "CalculDirection" => Ok(u32::from(frame_path::direction(
            a[0] as u16,
            a[1] as u16,
            false,
        ))),
        "CalculDirCase" => Ok(u32::from(frame_path::neighbor(m, a[0] as u16, a[1] as u8)?)),
        "Distance2d" => {
            let dx = (a[0] & 65535).wrapping_sub(a[2] & 65535);
            let dy = (a[1] & 65535).wrapping_sub(a[3] & 65535);
            Ok(dx.wrapping_mul(dx).wrapping_add(dy.wrapping_mul(dy)))
        }
        "DeplaceEngin" => displace(m, a[0]),
        "CalculNextCase" => next_case(m, a[0]),
        "AvanceEngin" => advance(m, a[0], a[1] as u8),
        "EnginNextCase" => choose_direct(m, a[0]),
        "EnginNextCaseChemin" => choose_route(m, a[0]),
        "CheminCalcul" | "OptimiseChemin" | "Chemin_Verouille" => frame_path::call(m, name, a),
        "RotateEngin" => rotate(m, a[0]),
        _ => frame_spawn::call(m, name, a),
    }
}
