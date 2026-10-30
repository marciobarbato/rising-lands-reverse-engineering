//! No-key InputGame/MenuInit and published display logic effects, translated
//! from entrada_quadro_ia.py and efeitos_logicos_exibicao.py. Pixels omitted.
use crate::{
    frame::{binding, boundary, stop, EventLog, FrameInput},
    frame_core, MemoriaJogo, Result,
};
fn guard(m: &MemoriaJogo, a: u32, site: u32, name: &'static str) -> Result<()> {
    if m.u8(a)? != 0 {
        stop(name, site)
    } else {
        Ok(())
    }
}
pub fn icons(m: &mut MemoriaJogo) -> Result<u32> {
    let local = u32::from(m.u8(0x508041)?);
    if m.u16(0x508728 + (local << 9))? == 1 {
        return stop("CalculIconeAction selected unit", 0x45e962);
    }
    if m.u16(0x495be0 + 2 * local)? != 0xffff {
        return stop("CalculIconeAction selected structure", 0x45e9bf);
    }
    for i in 0..10 {
        let r = 0x4e2410 + 6 * i;
        if m.u16(r)? != 0x29b1 || m.u16(r + 2)? != 1 || m.u16(r + 4)? != 0 {
            return stop("CalculIconeAction icon slot", 0x45ea64);
        }
        m.set_u16(r, 0x29b1)?;
        m.set_u16(r + 2, 1)?;
        m.set_u16(r + 4, 0)?;
    }
    m.set_u8(0x496d48, 255)?;
    Ok(10)
}
fn zone(m: &MemoriaJogo) -> Result<u16> {
    let x = i64::from(m.u16(0x5099a8)?);
    let y = i64::from(m.u16(0x5099aa)?);
    let mut z = m.u16(0x50a9b4)?;
    while z <= m.u16(0x50a9b6)? {
        let r = 0x5099b4 + 16 * u32::from(z);
        if i64::from(m.u32(r)? as i32) <= x
            && i64::from(m.u32(r + 4)? as i32) <= y
            && x <= i64::from(m.u32(r + 8)? as i32)
            && y <= i64::from(m.u32(r + 12)? as i32)
        {
            return Ok(z);
        }
        z = z.wrapping_add(1);
        if z == 0 {
            return stop("MouseZone wrapping zone range", 0x479cac);
        }
    }
    Ok(0)
}
pub(crate) fn rain(m: &mut MemoriaJogo) -> Result<()> {
    let wind = m.u16(0x496d2e)? as i16;
    if wind >= 0 {
        return stop("NextGouttes non-negative wind", 0x45ac56);
    }
    let strength = m.u8(0x496d2e)?.wrapping_neg();
    let mode = m.u8(0x496d2c)?;
    if mode == 2 {
        return stop("NextGouttes mode 2", 0x45ac6b);
    }
    if mode != 1 {
        return Ok(());
    }
    let denominator = 5 - i32::from(strength);
    if denominator == 0 {
        return stop("NextGouttes division zero", 0x45ad5e);
    }
    for i in 0..120 {
        let r = 0x4e1da0 + 6 * i;
        let y = (i32::from(m.u16(r + 2)? as i16) + 20) % 446;
        m.set_u16(r + 2, y as u16)?;
        let x = (i32::from(m.u16(r)? as i16) - 20 / denominator + 510) % 510;
        m.set_u16(r, x as u16)?;
        m.set_u8(r + 4, m.u8(r + 4)?.wrapping_add(1) % 4)?;
    }
    Ok(())
}
fn hover(m: &mut MemoriaJogo, player: u8) -> Result<()> {
    let y = u32::from(m.u16(0x5099aa)?);
    let x = u32::from(m.u16(0x5099a8)?);
    let c =
        (((y >> 5) + u32::from(m.u16(0x508722)?)) << 8) + (x >> 5) + u32::from(m.u16(0x508720)?);
    let margin = i64::from(m.u8(0x508f90)? as i8) * 32;
    if i64::from(x) >= i64::from(m.u16(0x508724)?) * 32 - margin
        || i64::from(y) >= i64::from(m.u16(0x508726)?) * 32 - margin
        || i64::from(x) < margin
        || i64::from(y) < margin
    {
        return Ok(());
    }
    let c = c & 65535;
    let local = u32::from(m.u8(0x508041)?);
    if frame_core::call(m, "CaseEstDecouverte", &[c, local])? as u8 == 0 {
        return stop("InputGame undiscovered hover", 0x4298e2);
    }
    let obj = m.u8(m.u32(0x507d74)?.wrapping_add(c))?;
    if obj >= 0x42 {
        return stop("TerrainEstSac bag", 0x4766c9);
    }
    if obj >= 0x1d {
        return stop("TerrainEstGc", 0x4762d1);
    }
    let tile = m.u16(m.u32(0x507d70)?.wrapping_add(2 * c))?;
    if (0x251..=0x252).contains(&tile) || (0x255..=0x256).contains(&tile) {
        return stop("TerrainEstMine", 0x4762af);
    }
    if obj == 0x46 {
        return stop("TerrainEstPiege", 0x4762fa);
    }
    if frame_core::call(m, "CaseEstIlluminee", &[c, u32::from(player)])? as u8 != 0 {
        if m.u8(m.u32(0x4e0f38)?.wrapping_add(2 * c + 1))? & 128 != 0 {
            return stop("InputGame structure hover", 0x429a8c);
        }
        m.set_u16(0x496ac4, 65535)?;
        let pool = m.u32(0x4e19a0)?;
        for i in 0..800 {
            let r = pool.wrapping_add(276 * i);
            if [0, 4].contains(&m.u8(r + 2)?) || m.u8(r + 0x72)? == 0 {
                continue;
            }
            let filter = 1 + u32::from(m.u8(r + 0xab)? != 0);
            if crate::frame_units::call(m, "EnginOccupeCase", &[i, c, filter])? as u8 != 0 {
                return stop("ChercheIndiceEngin unit found", 0x44671c);
            }
        }
        m.set_u16(0x496ac2, 65535)?;
    }
    if [9, 12, 11, 3, 13, 5, 10, 1, 2, 7].contains(&m.u16(0x4e05ae)?) {
        return stop("InputGame hover help page", 0x429b8c);
    }
    let selected = 0x508728 + (u32::from(player) << 9);
    if m.u16(selected)? == 0
        && m.u16(0x495be0 + 2 * u32::from(player))? == 65535
        && m.u8(0x4e19b0)? == 0
        && m.u8(0x5099ae)? != 0
    {
        return stop("InputGame hover held button", 0x42a6fd);
    }
    guard(m, 0x4e19b0, 0x42b85d, "InputGame hover flag")?;
    if m.u16(selected)? != 0 {
        return stop("InputGame selected troops hover", 0x42a762);
    }
    if m.u16(0x496ac2)? != 65535 {
        return stop("InputGame unit info", 0x42a793);
    }
    if m.u16(0x496ac4)? != 65535 {
        return stop("InputGame structure info", 0x42ac1b);
    }
    Ok(())
}
pub fn input(m: &mut MemoriaJogo, player: u8, events: &mut EventLog) -> Result<()> {
    m.set_u16(0x49a010, 0x1dd8)?;
    m.set_u16(0x4e0612, 0)?;
    m.set_u16(0x4e0614, 0)?;
    m.set_u32(0x49a014, 0)?;
    m.set_u16(0x4e0616, 0)?;
    m.set_u8(0x508f8f, 0)?;
    m.set_u8(0x4e17ac, 0)?;
    m.set_u16(0x4e0618, 0)?;
    for a in [0x496d4a, 0x496ac2, 0x496ac4] {
        m.set_u16(a, 65535)?;
    }
    binding(events, 2, 0x429300, &[0x1b], 0);
    for (a, site) in [
        (0x5099ae, 0x42934d),
        (0x5099ae, 0x42935e),
        (0x4e05a8, 0x42937b),
        (0x5099b1, 0x4293a1),
    ] {
        guard(m, a, site, "InputGame mouse/button guard")?;
    }
    m.set_u8(0x4e19b0, 0)?;
    let z = zone(m)?;
    m.set_u16(0x5099ac, z)?;
    guard(m, 0x49a05a, 0x4293dc, "InputGame focus flag")?;
    binding(events, 2, 0x429556, &[0x10], 0);
    if m.u16(0x4e05ae)? == 12 {
        return stop("InputGame help page12", 0x429573);
    }
    guard(m, 0x5099b1, 0x429585, "InputGame mouse button")?;
    guard(m, 0x5099b1, 0x4295aa, "InputGame mouse button")?;
    binding(events, 2, 0x4295fc, &[0x11], 0);
    if [8, 9].contains(&m.u16(0x4e05ae)?) {
        return stop("InputGame help page8/9", 0x42966c);
    }
    binding(events, 2, 0x42967e, &[0x2e], 0);
    if m.u16(0x4e05ae)? == 7 {
        return stop("InputGame help page7", 0x42969b);
    }
    binding(events, 2, 0x4296ad, &[0x12], 0);
    if m.u16(0x4e05ae)? == 2 {
        return stop("InputGame help page2", 0x4296ca);
    }
    for (vk, site) in [
        (0x20, 0x4296dc),
        (0x26, 0x4296f1),
        (0x28, 0x42970b),
        (0x27, 0x429732),
        (0x25, 0x42974c),
        (0x0d, 0x429773),
        (0x58, 0x429781),
    ] {
        binding(events, 2, site, &[vk], 0);
    }
    if m.u16(0x4e05ae)? == 13 {
        return stop("InputGame help page13", 0x4297a2);
    }
    if z >= 10 {
        return stop("InputGame zone>=10", 0x4297cd);
    }
    if z == 0 {
        hover(m, player)?;
    } else if z > 8 {
        return stop("InputGame zone9", 0x42c29f);
    } else {
        guard(m, 0x5099ae, 0x42ba8c, "InputGame scroll button")?;
        m.set_u32(0x49a014, 0)?;
        m.set_u16(0x49a010, z.wrapping_add(0x1dd7))?;
        if z != 1 {
            return stop("ScrollTerrain direction", 0x472048 + 4 * u32::from(z - 1));
        }
        for a in [0x508720, 0x508722] {
            let v = m.u16(a)?;
            if v > 0 {
                m.set_u16(a, v - 1)?;
            }
        }
    }
    if m.u32(0x4e060c)? != 0 {
        return stop("InputGame help info", 0x42c2bd);
    }
    let h = m.u16(0x4e0610)?;
    if h < m.u16(0x49620a)? {
        m.set_u16(0x4e0610, h.wrapping_add(1))?;
    }
    m.set_u32(0x4e060c, 0)?;
    m.set_u16(0x49620c, 65535)?;
    if m.u8(0x496d2c)? != 0 {
        rain(m)?;
    }
    Ok(())
}
fn cstring(m: &MemoriaJogo, a: u32) -> Result<Vec<u8>> {
    let mut v = Vec::new();
    let mut p = a;
    loop {
        let b = m.u8(p)?;
        if b == 0 {
            return Ok(v);
        }
        v.push(b);
        p = p.wrapping_add(1);
        if p == a {
            return stop("MenuInit unterminated path", a);
        }
    }
}
pub fn menu(
    m: &mut MemoriaJogo,
    input: &FrameInput,
    events: &mut EventLog,
    mut delete: impl FnMut(&mut MemoriaJogo, &mut EventLog, u32) -> Result<()>,
) -> Result<()> {
    let current = m.u8(0x4e2f78)?;
    if current == 0x12 {
        return Ok(());
    }
    if [6, 7, 10, 1, 19, 24].contains(&current) {
        return stop("MenuInit source mode", 0x4682f5);
    }
    binding(events, 1, 0x46837a, &[0], 0);
    m.set_u32(0x508f70, input.offscreen)?;
    let bank = m.u32(0x508f64)?;
    if bank != 0 {
        delete(m, events, bank)?;
        m.set_u32(0x508f64, 0)?;
    }
    if m.u32(0x508f68)? != 0 {
        return stop("MenuInit bank2", 0x4683c3);
    }
    guard(m, 0x49a054, 0x4683db, "MenuInit palette mode")?;
    // FilledBox writes pixels only. DDLock/Unlock bookkeeping restores itself.
    guard(m, 0x4e2f79, 0x46840e, "MenuInit asset mode")?;
    let path = cstring(m, 0x509494)?;
    let mut text = path.clone();
    text.extend(cstring(m, 0x494a4d)?);
    text.push(0);
    let mut stack = [0u32; 4];
    let mut mask = 0;
    for (k, word) in stack.iter_mut().enumerate() {
        if 4 * k < text.len() {
            let mut b = [0; 4];
            let n = (text.len() - 4 * k).min(4);
            b[..n].copy_from_slice(&text[4 * k..4 * k + n]);
            *word = u32::from_le_bytes(b);
            mask |= 1 << k;
        }
    }
    let ecx = 0u32
        .wrapping_sub(2)
        .wrapping_sub(u32::try_from(path.len()).map_err(|_| crate::EngineError::AddressOverflow)?);
    boundary(
        m,
        events,
        101,
        0x46847b,
        [
            input.registers.esp.wrapping_sub(4 + 0x14 + 0x138),
            m.u32(0x508f70)?,
            0,
            ecx,
        ],
        stack,
        mask,
    )?;
    let ebx = frame_core::call(m, "InitGameZone", &[1, 0])?;
    let i = m.u8(0x4e1d18)?;
    let track = 2 + u32::from(m.u8(0x4e1c18 + u32::from(i))? % 2);
    m.set_u8(0x4e1d18, i.wrapping_add(1))?;
    boundary(
        m,
        events,
        102,
        0x4684bd,
        [track, 0, (ebx & !255) | u32::from(i.wrapping_add(1)), 2],
        stack,
        mask,
    )?;
    m.set_u8(0x4e2f78, 0x12)?;
    guard(m, 0x508f90, 0x468c76, "MenuInit viewport margin")?;
    m.set_u32(0x4e2f70, 0)?;
    m.set_u16(0x4e2f40, 0)?;
    m.set_u8(0x508f90, m.u8(0x4e2f7a)?)?;
    Ok(())
}
// Exact sampled-origin domain of the accepted Graphics effect provider.
const ORIGINS: &[(u16, u16)] = &[
    (0, 0),
    (0, 1),
    (0, 2),
    (0, 6),
    (0, 7),
    (0, 12),
    (0, 14),
    (0, 18),
    (0, 21),
    (0, 24),
    (0, 28),
    (0, 30),
    (0, 35),
    (0, 36),
    (0, 42),
    (0, 47),
    (4, 6),
    (4, 30),
    (1, 3),
    (2, 4),
    (3, 5),
    (4, 44),
    (6, 0),
    (6, 7),
    (6, 14),
    (6, 21),
    (6, 28),
    (6, 35),
    (6, 42),
    (8, 0),
    (8, 6),
    (8, 12),
    (8, 18),
    (8, 24),
    (8, 30),
    (8, 36),
    (8, 42),
    (8, 47),
    (12, 0),
    (12, 7),
    (12, 14),
    (12, 21),
    (12, 28),
    (12, 35),
    (12, 40),
    (12, 42),
    (16, 0),
    (16, 6),
    (16, 12),
    (16, 18),
    (16, 24),
    (16, 30),
    (16, 36),
    (16, 42),
    (16, 47),
    (18, 0),
    (18, 7),
    (18, 14),
    (18, 21),
    (18, 28),
    (18, 35),
    (18, 42),
    (24, 0),
    (24, 6),
    (24, 7),
    (24, 12),
    (24, 14),
    (24, 18),
    (24, 21),
    (24, 24),
    (24, 28),
    (24, 30),
    (24, 35),
    (24, 36),
    (24, 42),
    (24, 47),
    (30, 0),
    (30, 7),
    (30, 14),
    (30, 21),
    (30, 28),
    (30, 35),
    (30, 42),
    (32, 0),
    (32, 6),
    (32, 12),
    (32, 18),
    (32, 24),
    (32, 30),
    (32, 36),
    (32, 42),
    (32, 47),
    (36, 0),
    (36, 7),
    (36, 14),
    (36, 21),
    (36, 28),
    (36, 35),
    (36, 42),
    (39, 0),
    (39, 6),
    (39, 12),
    (39, 18),
    (39, 24),
    (39, 30),
    (39, 36),
    (39, 42),
    (39, 47),
];
pub fn display_effects(m: &mut MemoriaJogo, flips: u32) -> Result<()> {
    if (m.u16(0x508724)?, m.u16(0x508726)?) != (25, 17) {
        return stop("Display effect viewport", 0x4178f7);
    }
    if !ORIGINS.contains(&(m.u16(0x508720)?, m.u16(0x508722)?)) {
        return stop(
            if m.player.is_some() {
                "AffGame"
            } else {
                "Display effect sampled origin"
            },
            0x415b77,
        );
    }
    let mut occupied = 0;
    for i in 0..1000 {
        let r = 0x49a0c8 + 276 * i;
        let state = m.u8(r + 5)?;
        if state > 7 {
            return stop(
                if m.player.is_some() {
                    "AffGame"
                } else {
                    "Display structure state"
                },
                0x407dd3,
            );
        }
        if state != 0 {
            occupied += 1;
            if occupied > 1 || m.u8(r + 8)? != 2 {
                return stop(
                    if m.player.is_some() {
                        "AffGame"
                    } else {
                        "Display structure domain"
                    },
                    0x407dd3,
                );
            }
            if state == 3 {
                return stop("BatimentEstHabiter display mode3", 0x40863e);
            }
        }
    }
    if m.u8(0x50b178)? > 1 {
        return stop("Display monster count", 0x41591f);
    }
    let pool = m.u32(0x5080f0)?;
    let mut active = 0;
    for i in 0..100 {
        let p = pool.wrapping_add(56 * i);
        if m.u8(p + 2)? != 0 {
            active += 1;
            if active > 1 || ![31, 32].contains(&m.u8(p)?) {
                return stop("Display projectile domain", 0x46ff70);
            }
        }
    }
    for _ in 0..flips {
        let n = m.u8(0x4dfb44)?;
        if n != 0 {
            m.set_u8(0x4e1d18, m.u8(0x4e1d18)?.wrapping_add(1))?;
            if m.u8(0x508f7c)? & 1 == 0 {
                m.set_u8(0x4dfb44, n - 1)?;
            }
        }
    }
    Ok(())
}
pub fn affgame(m: &mut MemoriaJogo) -> Result<u32> {
    if m.u8(0x4e2f78)? != 0x12 {
        return stop("AffGame mode", 0x4176a8);
    }
    guard(m, 0x4e1b0e, 0x417905, "AffGame event")?;
    let flag = m.u8(0x4e05a2)?;
    let counter = m.u32(0x508f7c)?;
    if flag == 0 {
        let divisor = u32::from(m.u8(0x497284)?);
        if divisor == 0 {
            return stop("AffGame divisor zero", 0x417921);
        }
        if counter % divisor != 0 {
            return Ok(counter / divisor);
        }
    }
    guard(m, 0x508f92, 0x417938, "AffGame video surface clear")?;
    if m.u16(0x496204)? != 65535 {
        return stop("AffGame marker animation", 0x417ba2);
    }
    display_effects(m, u32::from(m.u8(0x49a05b)?) + 1)?;
    if m.player.is_some() {
        // AffGame's post-flip cursor handoff, 0x417db2..0x417e78.
        // The software cursor uses this flag on the *following* draw. ShowCursor
        // itself belongs to host presentation; no OS callback runs in the engine.
        let margin = i32::from(m.u8(0x508f90)? as i8) * 32;
        let x = i32::from(m.u16(0x5099a8)?);
        let y = i32::from(m.u16(0x5099aa)?);
        let right = i32::from(m.u16(0x508724)?) * 32 - margin;
        let bottom = i32::from(m.u16(0x508726)?) * 32 - margin;
        match m.u8(0x49a054)? {
            0 if x < margin || x > right || y < margin || y > bottom => {
                m.set_u8(0x49a054, 1)?;
            }
            1 if x > margin && x < right && y > margin && y < bottom => {
                m.set_u8(0x49a054, 0)?;
            }
            _ => {}
        }
    }
    m.set_u8(0x4e05a2, 0)?;
    let eax = if counter % 5 == 0 {
        if m.u32(0x4e179c)? == 0 {
            return stop("DDSetPalette CreatePalette", 0x43ee95);
        }
        m.set_u8(0x4e05a2, 1)?;
        0
    } else {
        counter / 5
    };
    Ok((eax & !255) | u32::from(m.u8(0x4e1b0e)?))
}
