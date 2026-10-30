//! Economy ciclo_trabalho: original 0x44bc74, immutable owner reference.
use crate::{
    frame::stop,
    player::{unit, Memory},
    FrameRegisters as R, MemoriaJogo, Result,
};
fn room(m: &MemoriaJogo, r: u32) -> Result<bool> {
    Ok(m.w(r + 0x70)? < m.w(r + 12)?)
}
fn dest(m: &mut MemoriaJogo, u: u32, r: u32, c: u32) -> Result<bool> {
    m.sw(r + 0x7e, c)?;
    let freed = m.w(0x496304)? == u;
    crate::frame_spawn::release(m, u)?;
    Ok(freed)
}
fn idle(m: &mut MemoriaJogo, u: u32, r: u32) -> Result<(bool, bool)> {
    if matches!(m.b(r + 2)?, 0 | 4) {
        return Ok((false, false));
    }
    m.sb(r + 2, 7)?;
    let f = m.w(0x496304)? == u;
    crate::frame_spawn::release(m, u)?;
    Ok((true, f))
}
fn bag(m: &mut MemoriaJogo, n: &str, a: u32, d: u32, b: u32) -> Result<u32> {
    Ok(crate::chain_bags::body(
        m,
        n,
        R {
            eax: a,
            edx: d,
            ebx: b,
            ..Default::default()
        },
    )?
    .eax)
}
fn append(m: &mut MemoriaJogo, a: u32, v: u32) -> Result<u32> {
    let n = m.w(a)?;
    m.sw(a + 0x66, m.w(a + 0x66)?.wrapping_add(1))?;
    m.sb(a + n + 0x42, 2)?;
    m.sw(a + 6 + 2 * n, v)?;
    m.sw(a, n.wrapping_add(1))?;
    Ok(n)
}
fn timer(m: &mut MemoriaJogo, r: u32) -> Result<u32> {
    let t = m.b(r + 1)?;
    let b = crate::frame_economy::bonus(m, m.b(r)?, t, 3, 0)?;
    let v = (b & !255) | m.b(0x4965de + 50 * t)?.wrapping_sub(b) & 255;
    m.sb(r + 0x8b, v)?;
    Ok(v)
}
fn dec(m: &mut MemoriaJogo, r: u32) -> Result<u32> {
    let t = m.b(r + 0x8b)?.wrapping_sub(1) & 255;
    m.sb(r + 0x8b, t)?;
    Ok(t)
}
fn near(m: &mut MemoriaJogo, r: u32) -> Result<bool> {
    Ok(m.b(r + 0x86)? == 0
        && m.b(r + 0x87)? == 0
        && crate::chain_entry::adjacent(m, m.w(r + 0xc0)? as u16, m.w(r + 8)? as u16)?)
}
fn centre(m: &MemoriaJogo, s: u32) -> Result<u32> {
    crate::frame_core::building_cell(m, s)
}
fn geometric_centre(m: &MemoriaJogo, s: u32) -> Result<u32> {
    Ok(crate::chain_entry::central_offset(m, s)? & 65535)
}
fn walk(m: &mut MemoriaJogo, u: u32) -> Result<u32> {
    crate::frame_movement::displace(m, u)
}
pub fn mine_index(m: &MemoriaJogo, c: u32) -> Result<u32> {
    for i in 0..20 {
        let o = m.w(0x509954 + 4 * i)?;
        if o != 0 && [o, o + 1, o + 256, o + 257].contains(&(c & 65535)) {
            return Ok(i);
        }
    }
    Ok(65535)
}
pub fn leaf(m: &mut MemoriaJogo, n: &str, mut r: R) -> Result<R> {
    let c = r.eax & 65535;
    r.eax = match n {
        "MineGetIndice" => mine_index(m, c)?,
        "MineEstSurTerrain" => {
            let t = m.w(m.d(0x507d70)? + 2 * c)?;
            (t & 0xff00) | u32::from(matches!(t, 0x253 | 0x254))
        }
        "MineSetWork" | "MineEndWork" => {
            let i = mine_index(m, c)?;
            if i == 65535 {
                65535
            } else {
                let o = m.w(0x509954 + 4 * i)?;
                let a = m.d(0x507dac)?;
                for d in [0, 1] {
                    let b = m.b(a + o + d)?;
                    m.sb(
                        a + o + d,
                        if n == "MineSetWork" {
                            b.wrapping_add(1)
                        } else {
                            b.wrapping_sub(1)
                        },
                    )?;
                }
                a
            }
        }
        "MineRecolte" => {
            let i = mine_index(m, c)?;
            if i == 65535 {
                0
            } else {
                let a = 0x509954 + 4 * i;
                let q = m.w(a + 2)?;
                if q > 1 {
                    m.sw(a + 2, q - 1)?;
                    1
                } else {
                    m.sw(a + 2, 0)?;
                    let o = m.w(a)?;
                    let g = m.d(0x507d70)?;
                    m.sw(g + 2 * o, 0x1db)?;
                    m.sw(g + 2 * o + 2, 0x1dc)?;
                    (r.ebx & 0xffff0000) | q
                }
            }
        }
        "TerrainRecolte" => {
            let g = m.d(0x507d74)?;
            let v = m.b(g + c)?;
            if !(0x1d..0x35).contains(&v) {
                v
            } else if v >= 0x33 {
                m.sb(g + c, v - 10)?;
                g + c
            } else {
                m.sb(g + c, 0)?;
                g
            }
        }
        "AjouteMatiere" => {
            let b = (r.ebx & 65535) << 2;
            let o = ((r.eax & 255) + b) << 3;
            r.ebx = ((b & 0xffff0000) | m.w(0x4e2eaa + o)?).wrapping_add(r.edx);
            r.edx = r.ebx & 65535;
            m.sw(0x4e2eaa + o, r.edx)?;
            if r.edx > 9999 {
                m.sw(0x4e2eaa + o, 9999)?;
            }
            o
        }
        _ => return stop("work leaf", 0x44bc74),
    };
    Ok(r)
}
fn mine_call(m: &mut MemoriaJogo, n: &str, c: u32) -> Result<u32> {
    Ok(leaf(
        m,
        n,
        R {
            eax: c,
            ..Default::default()
        },
    )?
    .eax)
}
pub fn anim(m: &mut MemoriaJogo, u: u32) -> Result<u32> {
    let a = unit(m, u)?;
    let t = m.b(a + 1)?;
    let mut eax = (u & !255) | t;
    if !matches!(t, 5 | 7 | 13) {
        return Ok(eax);
    }
    let p = m.b(a + 0x89)?;
    eax = (eax & !255) | p;
    if (t == 5 && p != 1) || (t == 7 && p != 12) || (t == 13 && !matches!(p, 1 | 4)) {
        return Ok(eax);
    }
    let v = m.b(a + 0xa9)?.wrapping_add(1) & 255;
    m.sb(a + 0xa9, v)?;
    if t == 7 {
        eax = (eax & 0xffff00ff) | (m.b(a + 0xa7)? << 8)
    } else if t == 13 && p == 4 {
        eax = (eax & 0xffff00ff) | (v << 8)
    }
    if v != m.b(a + 0xa7)? {
        return Ok(eax);
    }
    let n = m.b(a + 0xa4)? + 1;
    let d = if t == 7 { m.b(a + 0xa5)? } else { 4 };
    if d == 0 {
        return stop("AnimWorkEngin division", 0x447fc7);
    }
    m.sb(a + 0xa9, 0)?;
    m.sb(a + 0xa4, n % d)?;
    Ok(n / d)
}
fn voice(m: &mut MemoriaJogo, u: u32, r: u32) -> Result<()> {
    let p = m.b(0x508041)?;
    if m.b(r)? != p
        || crate::frame_core::call(m, "TerrainEstDecouvert", &[m.w(r + 8)?, p])? & 255 == 0
    {
        return Ok(());
    }
    crate::player_orders::volume(m, m.w(r + 8)?)?;
    m.sb(r + 0xf9, 0)?;
    if m.d(r + 0x104)? == u32::MAX {
        crate::player::sound(
            m,
            0x44d9e5,
            true,
            [0x50, (m.b(r + 1)? << 16) | 0x1000, r + 0x104, 0],
            Some(0x100),
        )?;
    }
    let _ = u;
    Ok(())
}
fn back(m: &mut MemoriaJogo, u: u32, r: u32) -> Result<u32> {
    let b = m.w(r + 0xb2)?;
    if b != 65535 {
        m.sb(r + 0x89, 0)?;
        let f = dest(m, u, r, b)?;
        m.sb(r + 0x88, 0)?;
        return Ok(if f { b & 0xff00 } else { b });
    }
    let pool = m.d(0x4e19a0)?;
    let (a, f) = idle(m, u, r)?;
    Ok(if !a || f { 0 } else { pool })
}
fn food_depot(m: &mut MemoriaJogo, u: u32, r: u32) -> Result<u32> {
    let mode = m.b(r + 0x82)?;
    if mode == 2 {
        let s = m.w(r + 0x80)?;
        m.sw(r + 0xc0, s)?;
        if s == 65535 {
            let pool = m.d(0x4e19a0)?;
            let (a, f) = idle(m, u, r)?;
            return Ok(if !a {
                0
            } else if f {
                pool & 0xffff00ff
            } else {
                pool
            });
        }
        let c = centre(m, s)?;
        m.sb(r + 0x89, 2)?;
        dest(m, u, r, c)?;
        m.sb(r + 0x88, 0)?;
        return Ok(u);
    }
    if mode == 1 {
        return stop("CalculWorkEngin depot mode 1", 0x44dd3b);
    }
    let pool = m.d(0x4e19a0)?;
    let (a, f) = idle(m, u, r)?;
    Ok(if !a || f { 0 } else { pool })
}
pub fn work(m: &mut MemoriaJogo, u: u32) -> Result<u32> {
    let r = unit(m, u)?;
    let t = m.b(r + 1)?;
    let p = m.b(r + 0x89)?;
    let b = r + 10;
    if !matches!(t, 5 | 6 | 7 | 13) {
        return Ok(u & 0xffff00ff);
    }
    if matches!(t, 6 | 13) {
        return stop(
            "CalculWorkEngin type",
            if t == 6 { 0x44cde4 } else { 0x44d85b },
        );
    }
    if (t == 5 && p > 3) || (t == 7 && p > 5) {
        return Ok((u & 0xffff0000) | p);
    }
    if t == 5 {
        match p {
            0 => {
                if !room(m, r)? {
                    m.sb(r + 0x89, 1)?;
                    m.sb(r + 0xa4, 0)?;
                    return timer(m, r);
                }
                let c = m.w(r + 8)?;
                if m.w(r + 0x7e)? != c {
                    return walk(m, u);
                }
                if crate::chain_search::gc(m, c)? {
                    m.sb(r + 0x89, 1)?;
                    m.sb(r + 0xa4, 0)?;
                    return timer(m, r);
                }
                let g = crate::chain_search::free_gc(m, c, 5, u)?;
                if g != 65535 {
                    dest(m, u, r, g)?;
                    m.sb(r + 0x88, 0)?;
                    m.sw(r + 0xb2, g)?;
                    return Ok(g);
                }
                voice(m, u, r)?;
                let mode = m.b(r + 0x82)?;
                if mode == 2 {
                    let c = geometric_centre(m, m.w(r + 0x80)?)?;
                    crate::frame_spawn::order(m, u, c as u16)
                } else if mode == 1 {
                    crate::frame_spawn::order(m, u, m.w(r + 0x80)? as u16)
                } else {
                    Ok(mode)
                }
            }
            1 => {
                if room(m, r)? {
                    anim(m, u)?;
                    let v = dec(m, r)?;
                    if v != 0 {
                        return Ok(v);
                    }
                    let c = m.w(r + 8)?;
                    mine_call(m, "TerrainRecolte", c)?;
                    append(m, b, 1)?;
                    if room(m, r)?
                        && crate::frame_economy::bonus(m, m.b(r)?, m.b(r + 1)?, 7, 0)? & 65535 != 0
                    {
                        append(m, b, 1)?;
                    }
                    let x = c.wrapping_add(crate::frame_core::random(m)? % 5);
                    let y = crate::frame_core::random(m)? % 5;
                    let a = ((y << 8).wrapping_sub(0x200).wrapping_add(x).wrapping_sub(2)) & 65535;
                    let g = crate::chain_search::veget(m, a, 5, 0x1e, 0x35)?;
                    if g != 65535 && room(m, r)? {
                        m.sb(r + 0xa4, 0)?;
                        let f = dest(m, u, r, g)?;
                        m.sb(r + 0x88, 0)?;
                        m.sb(r + 0x89, 0)?;
                        m.sw(r + 0xb2, g)?;
                        return Ok(if f { 65535 } else { 1 });
                    }
                }
                food_depot(m, u, r)
            }
            2 => {
                let mode = m.b(r + 0x82)?;
                if mode == 1 {
                    return stop("CalculWorkEngin depot mode 1", 0x44dfed);
                }
                if mode != 2 {
                    return Ok(mode);
                }
                if near(m, r)? {
                    m.sb(r + 0x89, 3)?;
                    let v = m.w(0x4965de + 50 * m.b(r + 1)?)? / 5;
                    m.sb(r + 0x8b, v)?;
                    return Ok(v);
                }
                if m.w(r + 8)? != m.w(r + 0x7e)? {
                    return walk(m, u);
                }
                let c = centre(m, m.w(r + 0x80)?)?;
                let f = dest(m, u, r, c)?;
                m.sb(r + 0x88, 0)?;
                Ok(if f { u & 0xff00 } else { u })
            }
            _ => {
                let v = dec(m, r)?;
                if v != 0 {
                    return Ok(v);
                }
                if bag(m, "BagContient", b, 2, 1)? & 65535 != 0 {
                    let mode = m.b(r + 0x82)?;
                    if mode == 1 {
                        return stop("CalculWorkEngin depot mode 1", 0x44e207);
                    }
                    if mode != 2 {
                        return Ok(mode);
                    }
                    crate::chain_entry::credit(m, 1, 1, m.b(r)? as u8, m.w(r + 0x80)? as u16)?;
                    let v = bag(m, "BagRetire", b, 2, 1)?;
                    m.sb(r + 0x8b, 50)?;
                    return Ok(v);
                }
                back(m, u, r)
            }
        }
    } else {
        match p {
            0 => {
                if !room(m, r)? {
                    let mode = m.b(r + 0x82)?;
                    if mode == 0 {
                        return Ok(0);
                    }
                    if mode != 2 {
                        return stop(
                            "CalculWorkEngin depot mode",
                            if mode == 1 { 0x44bf78 } else { 0x44bfef },
                        );
                    }
                    m.sw(r + 0xc0, m.w(r + 0x80)?)?;
                    let c = geometric_centre(m, m.w(r + 0x80)?)?;
                    if c & 65535 != 65535 {
                        m.sb(r + 0x89, 3)?;
                        let f = dest(m, u, r, c)?;
                        m.sb(r + 0x88, 0)?;
                        return Ok(if f { c & 0xffff00ff } else { c });
                    }
                    let pool = m.d(0x4e19a0)?;
                    return Ok(if idle(m, u, r)?.0 { pool } else { 0 });
                }
                let c = m.w(r + 8)?;
                if m.w(r + 0x7e)? != c {
                    return walk(m, u);
                }
                let target = m.w(r + 0xb2)?;
                if target != c {
                    dest(m, u, r, target)?;
                    m.sb(r + 0x88, 0)?;
                    return Ok(((r + 10) & 0xffff0000) | target);
                }
                if mine_call(m, "MineEstSurTerrain", c)? & 255 == 0 {
                    return stop("CalculWorkEngin", 0x44bd8a);
                }
                mine_call(m, "MineSetWork", c)?;
                crate::chain_entry::retire(m, u as u16)?;
                m.sb(r + 0x89, 1)?;
                timer(m, r)
            }
            1 => {
                anim(m, u)?;
                let v = dec(m, r)?;
                if v != 0 {
                    return Ok(v);
                }
                if !room(m, r)? {
                    m.sb(r + 0x89, 2)?;
                    return Ok(m.w(b + 2)? & 0xff00);
                }
                if mine_call(m, "MineRecolte", m.w(r + 8)?)? & 65535 == 0 {
                    return stop("CalculWorkEngin depleted mine", 0x44c181);
                }
                let n = append(m, b, 2)?;
                m.sb(r + 0x8b, 50)?;
                Ok(n)
            }
            2 => {
                let c = m.w(r + 8)?;
                if !crate::chain_search::passable(m, u, c)? {
                    return Ok(0);
                }
                mine_call(m, "MineEndWork", c)?;
                crate::frame_core::call(m, "SetEnginCollision", &[u, c])?;
                m.sb(r + 0x72, 1)?;
                let owner = m.b(r)?;
                if !matches!(owner, 4 | 200) {
                    let radius = m.b(r + 0xbb)? + m.b(r + 0xf5)?;
                    crate::player_sight::area(m, c as u16, radius + 2, owner as u8, 0)?;
                    crate::player_sight::area(m, c as u16, radius, owner as u8, 1)?;
                }
                crate::player_sight::minimap(m, owner as u8, c as u16, 4)?;
                let mode = m.b(r + 0x82)?;
                if mode == 0 {
                    let pool = m.d(0x4e19a0)?;
                    let (a, f) = idle(m, u, r)?;
                    return Ok(if !a {
                        0
                    } else if f {
                        pool & !255
                    } else {
                        pool
                    });
                }
                if mode != 2 {
                    return stop(
                        "CalculWorkEngin depot mode",
                        if mode == 1 { 0x44c4ac } else { 0x44c523 },
                    );
                }
                m.sw(r + 0xc0, m.w(r + 0x80)?)?;
                let c = geometric_centre(m, m.w(r + 0x80)?)?;
                if c & 65535 != 65535 {
                    m.sb(r + 0x89, 3)?;
                    let f = dest(m, u, r, c)?;
                    m.sb(r + 0x88, 0)?;
                    return Ok(if f { 0 } else { c & 65535 });
                }
                let pool = m.d(0x4e19a0)?;
                Ok(if idle(m, u, r)?.0 { pool } else { 0 })
            }
            3 => {
                let mode = m.b(r + 0x82)?;
                if mode == 1 {
                    return stop("CalculWorkEngin depot mode 1", 0x44c729);
                }
                if mode != 2 {
                    return Ok(mode);
                }
                if near(m, r)? {
                    m.sb(r + 0x89, 4)?;
                    m.sb(r + 0x8b, 50)?;
                    return Ok(1);
                }
                if m.w(r + 8)? != m.w(r + 0x7e)? {
                    return walk(m, u);
                }
                let c = centre(m, m.w(r + 0x80)?)?;
                dest(m, u, r, c)?;
                m.sb(r + 0x88, 0)?;
                Ok(u)
            }
            4 => {
                let mode = m.b(r + 0x82)?;
                if mode == 1 {
                    return stop("CalculWorkEngin depot mode 1", 0x44c970);
                }
                if mode != 2 {
                    return Ok(mode);
                }
                let v = dec(m, r)?;
                if v != 0 {
                    return Ok(v);
                }
                let v = bag(m, "BagContient", b, 2, 2)?;
                if v & 65535 == 0 {
                    m.sb(r + 0x89, 5)?;
                    return Ok(v);
                }
                bag(m, "BagRetire", b, 2, 2)?;
                crate::chain_entry::credit(m, 2, 1, m.b(r)? as u8, m.w(r + 0x80)? as u16)?;
                let v = m.w(0x4965de + 50 * m.b(r + 1)?)? / 2;
                m.sb(r + 0x8b, v)?;
                Ok(v)
            }
            _ => {
                let mode = m.b(r + 0x82)?;
                let c = m.w(r + 0xb2)?;
                if mode == 2 {
                    if !crate::chain_search::passable(m, u, m.w(r + 8)?)? {
                        return Ok(0);
                    }
                    m.sw(r + 0xc0, 65535)?;
                    if c != 65535 {
                        let i = mine_index(m, c)?;
                        let cap = m.w(0x509956 + 4 * i)?;
                        if cap != 0 {
                            m.sb(r + 0x89, 0)?;
                            let f = dest(m, u, r, c)?;
                            m.sb(r + 0x88, 0)?;
                            return Ok(if f { c & 255 } else { c });
                        }
                    }
                    let pool = m.d(0x4e19a0)?;
                    let (a, f) = idle(m, u, r)?;
                    m.sb(r + 0x82, 0)?;
                    return Ok(if !a {
                        0
                    } else if f {
                        65535
                    } else {
                        pool
                    });
                }
                if c != 65535 {
                    m.sb(r + 0x89, 0)?;
                    dest(m, u, r, c)?;
                    m.sb(r + 0x88, 0)?;
                    return unit(m, u);
                }
                let pool = m.d(0x4e19a0)?;
                let a = idle(m, u, r)?.0;
                m.sb(r + 0x82, 0)?;
                Ok(if a { pool } else { 0 })
            }
        }
    }
}
