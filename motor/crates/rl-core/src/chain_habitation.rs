//! Economy cave ownership and technology, pinned54d148d.
use crate::{
    frame::stop,
    player::{structure, Memory},
    FrameRegisters as R, MemoriaJogo, Result,
};
const RADII: [u32; 22] = [
    20, 8, 10, 8, 5, 8, 8, 8, 8, 0, 7, 7, 0, 8, 8, 8, 8, 4, 8, 4, 8, 4,
];
fn low(v: u32, b: u32) -> u32 {
    (v & !255) | (b & 255)
}
pub(crate) fn level(m: &mut MemoriaJogo, p: u32, site: u32) -> Result<(u32, u32, u32)> {
    let a = 0x4e2ea8 + 32 * p;
    let n = m.w(0x4dfb2c + 6 * p)?;
    let d = m.w(0x4dfb2e + 6 * p)?;
    if n == 0 || d == 0 {
        return stop("cave stock indicator division", site);
    }
    let food = m.w(a + 10)?.wrapping_sub(m.w(a + 8)?) & 65535;
    let stone = m.w(a + 18)?.wrapping_sub(m.w(a + 16)?) & 65535;
    let q = (((food + stone) & 65535) / n) * 7;
    let v = q / d;
    let rem = q % d;
    m.sb(0x4dfb30 + 6 * p, v)?;
    Ok((v, rem, d))
}
fn bag_init(m: &mut MemoriaJogo, a: u32, cap: u32) -> Result<()> {
    for off in [0, 0x66, 4, 2] {
        m.sw(a + off, 0)?
    }
    for i in 0..30 {
        m.sw(a + 6 + 2 * i, 0)?;
        m.sb(a + 0x42 + i, 0)?
    }
    m.sw(a + 2, cap)
}
fn bag_take(m: &mut MemoriaJogo, a: u32, tag: u32, v: u32) -> Result<u32> {
    m.sw(a + 0x66, m.w(a + 0x66)?.wrapping_add(1))?;
    let n = m.w(a)?;
    m.sb(a + 0x42 + n, tag)?;
    m.sw(a + 6 + 2 * n, v)?;
    m.sw(a, n.wrapping_add(1))?;
    Ok(n)
}
pub fn technology(m: &mut MemoriaJogo, p: u32, t: u32) -> Result<Option<(u32, u32)>> {
    if p >= 4 || matches!(t,0|4|7..=12|14|17|19|21..=255) {
        return Ok(None);
    }
    if !matches!(t, 2 | 3) {
        return stop("BatimentSetTechnologie", 0x41c7af);
    }
    let bag = 0x4dd6e8 + 0x8f0 * p + 104 * t;
    let mut eax = if t == 3 { 3 } else { 4 };
    let mut edx = 30;
    bag_init(m, bag, eax)?;
    if t == 2 {
        for u in [5, 6, 7] {
            eax = m.b(0x4e1934 + 26 * p + u)?;
            edx = 26 * p;
            if eax & 255 != 0 {
                edx = bag_take(m, bag, 6, u)?;
                eax = bag
            }
        }
    }
    Ok(Some((eax, edx)))
}
pub fn habitable(m: &mut MemoriaJogo, s: u32) -> Result<u32> {
    let e = structure(s);
    let t = m.b(e + 8)?;
    let p = m.b(e + 4)?;
    technology(m, p, t)?;
    let mut eax = t;
    if !matches!(t, 17 | 9 | 12) {
        if t == 4 {
            m.sw(e + 0x78, 0)?
        } else if t == 3 && p < 4 && m.w(0x4dfb2c + 6 * p)? != 0 {
            level(m, p, 0x41cd55)?;
        }
        if t > 21 {
            return stop("BatimentHabitable", 0x41cd62);
        }
        let cell = crate::frame_core::building_cell(m, s)?;
        let radius = RADII[t as usize];
        crate::player_sight::area(m, cell as u16, radius + 3, p as u8, 0)?;
        crate::player_sight::area(m, cell as u16, radius, p as u8, 1)?;
        // entrada_estruturas.illumine_terrain: sign-extended row bound DX + 1.
        eax = (radius.wrapping_add(1) as u16 as i16 as i32) as u32;
    }
    m.sw(e + 0x84, 200)?;
    Ok(eax)
}
pub fn own(m: &mut MemoriaJogo, name: &str, mut r: R) -> Result<R> {
    match name {
        "BatimentHabitable" => r.eax = habitable(m, r.eax & 65535)?,
        "BatimentSetTechnologie" => {
            if let Some((a, d)) = technology(m, r.eax & 255, r.edx & 255)? {
                r.eax = a;
                r.edx = d
            }
        }
        "TypeEnginEstRealisable" => {
            let p = r.eax & 255;
            let t = r.edx & 255;
            r.eax = m.b(0x4e1934 + 26 * p + t)?;
            r.edx = 26 * p
        }
        "EnginGetTimeRecrute" => r.eax = m.w(0x4965ae + 50 * (r.eax & 255))?,
        "EnginGetRessource" => {
            let t = r.eax & 255;
            let a = 0x4965ae + 50 * t;
            let (food, parts, stone) = (m.w(a + 2)?, m.w(a + 4)?, m.w(a + 6)?);
            m.sw(r.edx, food)?;
            m.sw(r.ebx, stone)?;
            m.sw(r.ecx, parts)?;
            r.eax = parts;
            r.ebx = t;
            r.edx = (r.edx & 0xffff0000) | stone
        }
        "BatimentGetCapacite" => {
            let t = m.b(structure(r.eax) + 8)?;
            let mut c = m.b(0x495d8c + 52 * t + 18)?;
            if t == 14 {
                c = c.wrapping_sub(1)
            } else if t == 19 {
                c = c.wrapping_sub(m.b(0x495be8)?)
            }
            r.eax = low(13 * t, c)
        }
        "InitBatimentPlayer" => {
            let e = structure(r.eax);
            let p = r.edx & 255;
            let t = m.b(e + 8)?;
            if t == 18 {
                return stop("InitBatimentPlayer", 0x41bec6);
            }
            r.eax = (r.eax & 0xffff0000) | (p << 8) | t;
            r.edx = e;
            if t == 6 {
                m.sb(0x4dfb48 + p, m.b(0x4dfb48 + p)?.wrapping_add(1))?;
                r.eax = p
            } else if t == 3 {
                let a = 0x4dfb2c + 6 * p;
                let n = m.w(a)?.wrapping_add(1) & 65535;
                m.sw(a, n)?;
                r.eax = p;
                if p < 4 {
                    if n == 0 {
                        r.edx = 0
                    } else {
                        (r.eax, r.edx, _) = level(m, p, 0x41bfbe)?
                    }
                }
            }
        }
        "InitBatimentNeutre" => {
            let s = r.eax & 65535;
            let e = structure(s);
            let t = m.b(e + 8)?;
            let p = r.edx & 255;
            r.eax = low(r.eax, t);
            if t == 18 {
                return stop("InitBatimentNeutre", 0x41c05d);
            }
            if t == 20 {
                m.sb(e + 0x7a, 0)?;
                m.sb(e + 0x104, 0)?;
                m.sd(e + 0x108, 1)?
            } else if t == 6 {
                let n = m.b(0x4dfb48 + p)?.wrapping_sub(1) & 255;
                m.sb(0x4dfb48 + p, n)?;
                if n == 0 {
                    return stop("SortilegeResetRealisable", 0x41c152);
                }
                r.eax = n;
                r.edx = low(r.edx, n)
            } else if t == 3 {
                let a = 0x4dfb2c + 6 * p;
                m.sw(a, m.w(a)?.wrapping_sub(1))?;
                if m.b(e + 5)? == 3 {
                    r.eax = 3
                } else {
                    // The original executes two TerrainDeposeMatiere calls. Only their zero-stock
                    // loops are supported here; a positive stock remains an addressed dependency.
                    let depositor = m.b(0x4dfab8)?;
                    let stock = 0x4e2ea8 + 32 * depositor;
                    let food = m.w(stock + 10)?.wrapping_sub(m.w(stock + 8)?) & 65535;
                    let stone = m.w(stock + 18)?.wrapping_sub(m.w(stock + 16)?) & 65535;
                    if food != 0 {
                        return stop("TerrainDeposeMatiere", 0x41c10a);
                    }
                    if stone != 0 {
                        return stop("TerrainDeposeMatiere", 0x41c12d);
                    }
                    r.eax = (m.w(e + 2)? + 0x202) & 65535;
                    r.edx = 2;
                }
            }
        }
        _ => return stop("unported cave owner entry", 0x41cc70),
    }
    r.esp = r.esp.wrapping_add(4);
    Ok(r)
}
