//! Core structure vision, visao_grupos at pinned main 54d148d.
use crate::{
    frame::stop,
    player::{structure, Memory},
    FrameRegisters as R, MemoriaJogo, Result,
};

fn cell(m: &mut MemoriaJogo, c: u32, p: u32, mode: u32) -> Result<(u32, u32)> {
    if p > 3 {
        return stop("Structure vision player", 0x419233);
    }
    if mode == 0 {
        let base = m.d(0x507d78 + 4 * p)?;
        crate::player_sight::borders(m, base, c, true)?;
        if m.b(base + c)? != 0 && p == m.b(0x508041)? {
            crate::player_sight::minimap(m, p as u8, c as u16, 1)?;
        }
        m.sb(base + c, m.b(base + c)? & 0xef)?;
        return Ok((p, c));
    }
    let count = m.d(0x507d98 + 4 * p)?.wrapping_add(c);
    let n = m.b(count)?;
    if (mode == 1 && n == 0) || (mode == 2 && n == 1) {
        let base = m.d(0x507d88 + 4 * p)?;
        crate::player_sight::borders(m, base, c, mode == 1)?;
        let b = m.b(base + c)?;
        m.sb(base + c, if mode == 1 { b & 0xef } else { b | 0x10 })?;
        if p == m.b(0x508041)? {
            crate::player_sight::minimap(m, p as u8, c as u16, if mode == 1 { 2 } else { 3 })?;
        }
    }
    if mode == 1 {
        if n != 255 {
            m.sb(count, n + 1)?;
        }
        Ok((p, if n == 255 { n } else { n | ((n + 1) << 8) }))
    } else {
        if n != 0 {
            m.sb(count, n - 1)?;
        }
        Ok((count, (c & 255) | (n << 8)))
    }
}

pub fn entry(m: &mut MemoriaJogo, name: &str, mut r: R) -> Result<R> {
    let p = r.edx & 255;
    match name {
        "DecouvreCase" | "IllumineCase" | "EteintCase" => {
            (r.eax, r.edx) = cell(
                m,
                r.eax & 65535,
                p,
                match name {
                    "DecouvreCase" => 0,
                    "IllumineCase" => 1,
                    _ => 2,
                },
            )?;
        }
        "BatimentDecouvre" | "BatimentIllumine" => {
            let s = r.eax & 65535;
            if name == "BatimentDecouvre" && p == 200 {
                r.eax = 200;
                r.edx = s;
                return Ok(r);
            }
            if p > 3 {
                return stop("Structure vision player", 0x419233);
            }
            let e = structure(s);
            let t = m.b(e + 8)?;
            let (w, h) = (m.w(0x495d8c + 52 * t)?, m.w(0x495d8e + 52 * t)?);
            let origin = m.w(e + 2)?;
            let (x, y) = ((origin & 255) as i32, (origin >> 8) as i32);
            if name == "BatimentDecouvre" {
                let (w, h) = (w + u32::from(w < 256), h + u32::from(h < 256));
                for dy in -1..h as i32 {
                    if !(0..256).contains(&(y + dy)) {
                        continue;
                    }
                    for dx in -1..w as i32 {
                        if (0..256).contains(&(x + dx)) {
                            cell(m, (origin as i32 + dx + (dy << 8)) as u32 & 65535, p, 0)?;
                        }
                    }
                }
                r.eax = h;
                r.edx = h;
            } else {
                let mode = if r.ebx & 255 != 0 { 1 } else { 2 };
                r.ebx = origin;
                r.edx = 0;
                for dy in 0..h {
                    r.edx = dy;
                    if y + dy as i32 >= 256 {
                        continue;
                    }
                    r.ebx = 0;
                    for dx in 0..w {
                        r.edx = x as u32;
                        if x + (dx as i32) < 256 {
                            (_, r.edx) =
                                cell(m, (m.w(e + 2)? + dx + ((dy & 255) << 8)) & 65535, p, mode)?;
                        }
                        r.ebx += 1;
                    }
                }
                r.eax = h;
            }
        }
        _ => return stop("Unknown structure vision entry", 0x419233),
    }
    Ok(r)
}
