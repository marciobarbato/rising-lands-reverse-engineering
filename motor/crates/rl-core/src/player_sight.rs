//! Core VisaoMovimento: light reference counts, borders and minimap layers.
use crate::{frame::stop, player::Memory, MemoriaJogo, Result};
fn borders(m: &mut MemoriaJogo, grid: u32, c: u32, erase: bool) -> Result<()> {
    let (x, y) = (c & 255, c >> 8);
    let (w, h) = (m.w(0x497168)?, m.w(0x49716a)?);
    for (p, bit) in [
        (if x == 0 { c } else { c - 1 }, if x == 0 { 8 } else { 2 }),
        (if y == 0 { c } else { c - 256 }, if y == 0 { 4 } else { 1 }),
        (
            if x == w - 1 { c } else { c + 1 },
            if x == w - 1 { 2 } else { 8 },
        ),
        (
            if y == h - 1 { c } else { c + 256 },
            if y == h - 1 { 1 } else { 4 },
        ),
    ] {
        let b = m.b(grid + p)?;
        m.sb(grid + p, if erase { b & !bit } else { b | bit })?
    }
    Ok(())
}
pub fn minimap(m: &mut MemoriaJogo, owner: u8, cell: u16, mode: u8) -> Result<u32> {
    let (w, h, mw, mh) = (
        m.w(0x497168)?,
        m.w(0x49716a)?,
        m.w(0x496fe0)?,
        m.w(0x496fe2)?,
    );
    if w == 0 || h == 0 {
        return stop("SetMiniMap map division", 0x46a3dc);
    }
    let (sx, sy) = ((mw / w).max(1), (mh / h).max(1));
    let c = u32::from(cell);
    let start = (((c >> 8) * mh / h) * mh + (c & 255) * mw / w) & 65535;
    let local = m.b(0x508041)?;
    let lit = m.b(m.d(0x507d88 + 4 * local)? + c)? & 31 == 0;
    let seen = m.b(m.d(0x507d78 + 4 * local)? + c)? & 31 == 0;
    let o = m.b(m.d(0x507d74)? + c)?;
    let t = m.w(m.d(0x507d70)? + 2 * c)?;
    let terrain = if (0x1d..0x35).contains(&o) || t >= 702 {
        30
    } else {
        m.b(0x509694 + t)?
    };
    for y in 0..sy {
        for x in 0..sx {
            let p = (start + y * 128 + x) & 65535;
            let f = m.d(0x507d5c)? + p;
            let u = m.d(0x507d60)? + p;
            let s = m.d(0x507d64)? + p;
            match mode {
                1 | 3 if u32::from(owner) == local => {
                    let color = m.b(m.d(0x4e24b4)? + terrain)?;
                    m.sb(f, color)?
                }
                2 if u32::from(owner) == local => {
                    let a = m.b(u)?;
                    let b = m.b(s)?;
                    m.sb(
                        f,
                        if a != 0 {
                            a
                        } else if b != 0 {
                            b
                        } else {
                            terrain
                        },
                    )?
                }
                1..=3 => {}
                4 => {
                    let color = if owner == 200 {
                        30
                    } else {
                        m.b(0x4e24dc + u32::from(owner))?
                    };
                    m.sb(u, color)?;
                    if lit {
                        m.sb(f, color)?
                    }
                }
                5 => {
                    m.sb(u, 0)?;
                    if seen {
                        let b = m.b(s)?;
                        m.sb(
                            f,
                            if lit {
                                if b != 0 {
                                    b
                                } else {
                                    terrain
                                }
                            } else {
                                m.b(m.d(0x4e24b4)? + terrain)?
                            },
                        )?
                    }
                }
                6 => {
                    let color = (if owner == 200 {
                        30
                    } else {
                        m.b(0x4e24dc + u32::from(owner))?
                    } + 2)
                        & 255;
                    m.sb(s, color)?;
                    if lit {
                        let a = m.b(u)?;
                        m.sb(f, if a != 0 { a } else { color })?
                    }
                }
                7 => {
                    m.sb(s, 0)?;
                    if seen {
                        let a = m.b(u)?;
                        m.sb(
                            f,
                            if lit {
                                if a != 0 {
                                    a
                                } else {
                                    terrain
                                }
                            } else {
                                m.b(m.d(0x4e24b4)? + terrain)?
                            },
                        )?
                    }
                }
                _ => return stop("SetMiniMap mode", 0x46a388),
            }
        }
    }
    Ok(sy)
}
/// Mode0 discovery (the body adds one to DX), mode1 illumination, mode2 extinction.
pub fn area(m: &mut MemoriaJogo, center: u16, radius: u32, owner: u8, mode: u32) -> Result<()> {
    if owner >= 4 {
        return stop("Terrain sight owner", 0x476851);
    }
    let radius = if mode == 0 {
        radius.wrapping_add(1) & 65535
    } else {
        radius
    };
    if radius > if mode == 0 { 24 } else { 20 } {
        return stop(
            "Terrain sight radius outside validated domain",
            if mode == 0 {
                0x476851
            } else if mode == 1 {
                0x476cb3
            } else {
                0x476e82
            },
        );
    }
    let (x, y) = (i32::from(center & 255), i32::from(center >> 8));
    let (w, h) = (m.w(0x497168)? as i32, m.w(0x49716a)? as i32);
    let rr = radius as i32;
    let limit = (radius * radius + u32::from(radius > 1)) & 65535;
    for dy in -rr..=rr {
        for dx in -rr..=rr {
            if x + dx < 0
                || x + dx >= w
                || y + dy < 0
                || y + dy >= h
                || ((dx * dx + dy * dy) as u32 & 65535) > limit
            {
                continue;
            }
            let c = ((y + dy) * 256 + x + dx) as u32;
            let p = u32::from(owner);
            if mode == 0 {
                let grid = m.d(0x507d78 + 4 * p)?;
                borders(m, grid, c, true)?;
                if m.b(grid + c)? != 0 {
                    minimap(m, owner, c as u16, 1)?;
                }
                m.sb(grid + c, m.b(grid + c)? & 0xef)?
            } else {
                let counts = m.d(0x507d98 + 4 * p)?;
                let grid = m.d(0x507d88 + 4 * p)?;
                let n = m.b(counts + c)?;
                if mode == 1 {
                    if n == 0 {
                        borders(m, grid, c, true)?;
                        m.sb(grid + c, m.b(grid + c)? & 0xef)?;
                        minimap(m, owner, c as u16, 2)?;
                    }
                    if n != 255 {
                        m.sb(counts + c, n + 1)?
                    }
                } else {
                    if n == 1 {
                        borders(m, grid, c, false)?;
                        m.sb(grid + c, m.b(grid + c)? | 16)?;
                        minimap(m, owner, c as u16, 3)?;
                    }
                    if n != 0 {
                        m.sb(counts + c, n - 1)?
                    }
                }
            }
        }
    }
    Ok(())
}
