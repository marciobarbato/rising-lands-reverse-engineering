//! Projectile creation and linear preparation from Combat's proved pool model.
//! Unknown world callbacks stop at their original address before publication.
use crate::{frame::stop, MemoriaJogo, Result};
fn record(m: &MemoriaJogo, index: u32) -> Result<u32> {
    if index >= 100 {
        return stop("ProjectileSet slot outside pool", 0x46e208);
    }
    Ok(m.u32(0x5080f0)?.wrapping_add(index.wrapping_mul(56)))
}
fn line(m: &mut MemoriaJogo, p: u32) -> Result<()> {
    let x = m.u16(p + 12)?;
    let y = m.u16(p + 14)?;
    let target = m.u16(p + 0x16)?;
    let dx = (target & 255)
        .wrapping_mul(32)
        .wrapping_add(16)
        .wrapping_sub(x) as i16;
    let dy = (target >> 8)
        .wrapping_mul(32)
        .wrapping_add(16)
        .wrapping_sub(y) as i16;
    let sx = if dx < 0 { -1i16 } else { 1 };
    let sy = if dy < 0 { -8192i16 } else { 8192 };
    let ax = dx.wrapping_abs() as u16;
    let ay = dy.wrapping_abs() as u16;
    let (major, minor, axial) = if (ax as i16) > (ay as i16) {
        (ax, ay, sx)
    } else {
        (ay, ax, sy)
    };
    m.set_u16(p + 0x34, major)?;
    m.set_u16(p + 0x2c, axial as u16)?;
    m.set_u16(p + 0x32, minor.wrapping_mul(2))?;
    m.set_u16(p + 0x2a, sx.wrapping_add(sy) as u16)?;
    m.set_u16(
        p + 0x30,
        minor.wrapping_mul(2).wrapping_sub(major.wrapping_mul(2)),
    )?;
    m.set_u32(
        p + 8,
        (i32::from(y as i16).wrapping_shl(13)).wrapping_add(i32::from(x as i16)) as u32,
    )?;
    m.set_u16(p + 0x2e, minor.wrapping_mul(2).wrapping_sub(major))?;
    if m.u8(p + 0x23)? != 0 {
        let divisor = i32::from(major as i16);
        let step = if divisor == 0 { 12800 } else { 12800 / divisor };
        m.set_u16(p + 0x28, step as u16)?;
        m.set_u32(p + 0x24, 0)?;
    }
    Ok(())
}
fn set(m: &mut MemoriaJogo, a: &[u32]) -> Result<u32> {
    let p = record(m, a[0])?;
    let kind = a[1] as u8;
    let from = a[2] as u16;
    let to = a[3] as u16;
    let mode = a[4] as u8;
    let attacker = a[5] as u16;
    let direction = a[6] as u8;
    let dx = a[7] as u16;
    let dy = a[8] as u16;
    let flag = a[9] as u8;
    m.set_u8(p, kind)?;
    m.set_u8(p + 1, 1)?;
    m.set_u8(p + 2, 1)?;
    m.set_u8(p + 3, 0)?;
    m.set_u16(p + 0x14, from)?;
    m.set_u16(p + 0x16, to)?;
    m.set_u8(p + 0x23, flag)?;
    m.set_u16(p + 12, (from & 255).wrapping_mul(32).wrapping_add(dx))?;
    m.set_u16(p + 14, (from >> 8).wrapping_mul(32).wrapping_add(dy))?;
    m.set_u16(p + 0x10, dx)?;
    m.set_u16(p + 0x12, dy)?;
    m.set_u32(p + 0x24, 0)?;
    m.set_u16(p + 0x28, 0)?;
    m.set_u8(p + 0x18, 0)?;
    m.set_u8(p + 0x19, 0)?;
    m.set_u16(p + 0x1a, 12)?;
    m.set_u16(p + 0x1c, 0)?;
    m.set_u8(p + 0x1f, mode)?;
    m.set_u8(p + 0x22, direction)?;
    m.set_u16(p + 0x20, attacker)?;
    match kind {
        1..=5 | 9..=13 | 17 | 20..=23 | 29 | 30 => {
            if matches!(kind, 1 | 9 | 17 | 20..=23) {
                m.set_u8(p + 1, 0)?;
            }
            let count = match kind {
                1 | 17 | 20..=23 => Some(15),
                2 => Some(10),
                3 => Some(8),
                4 => Some(4),
                9..=13 => Some(2),
                _ => None,
            };
            if let Some(count) = count {
                m.set_u8(p + 4, count)?;
            }
            if (9..=13).contains(&kind) {
                m.set_u16(p + 0x1a, 5)?;
            }
            m.set_u8(p + 0x19, u8::from(matches!(kind,1..=4|9..=12)))?;
            line(m, p)?;
            if kind == 9 {
                m.set_u16(p + 0x1c, 5)?;
            } else if matches!(kind, 1 | 17 | 20..=23) {
                m.set_u16(p + 0x1c, 10)?;
            }
            if matches!(kind, 20..=23 | 29 | 30) {
                m.set_u16(p + 0x1a, 20)?;
            }
        }
        15 | 16 if flag != 0 => m.set_u32(p + 0x24, 12800)?,
        26 => return stop("ProjectileSet InfligeDegat", 0x450874),
        28 => return stop("ProjectileSet SortilegeGetRayonEffet", 0x474734),
        _ => {} // The original leaves every other byte untouched for these types.
    }
    Ok(a[0]) // Semantic slot, not a claim about ProjectileSet's full EAX.
}
pub fn call(m: &mut MemoriaJogo, name: &str, a: &[u32]) -> Result<u32> {
    match name {
        "ProjectileInit" => {
            let pool = m.u32(0x5080f0)?;
            let mut slot = 0;
            while slot < 100 && m.u8(pool.wrapping_add(slot * 56 + 2))? != 0 {
                slot += 1;
            }
            if slot == 100 {
                return Ok(slot);
            }
            let mut args = [0u32; 10];
            args[0] = slot;
            args[1..].copy_from_slice(a);
            set(m, &args)
        }
        "ProjectileSet" => set(m, a),
        "ProjectileLineaire" => {
            let p = record(m, a[0])?;
            line(m, p)?;
            Ok(0)
        }
        "ProjectileCalcul" => crate::frame::call(m, "ProjectileCalcul", a),
        _ => stop("Unknown Combat frame provider", 0x46e44c),
    }
}
pub fn isolated(id: u32) -> Option<(&'static str, usize)> {
    Some(match id {
        550 => ("ProjectileInit", 9),
        551 => ("ProjectileSet", 10),
        552 => ("ProjectileLineaire", 1),
        _ => return None,
    })
}
