//! Live S1 queries: Economy/AI original-first contracts at profile chain11.
use crate::{frame::stop, player::Memory, FrameRegisters as R, MemoriaJogo, Result};

pub fn sack(m: &MemoriaJogo, cell: u32) -> Result<u32> {
    let c = cell & 65535;
    let kind = m.b(m.d(0x507d74)?.wrapping_add(c))?;
    if (0x42..=0x44).contains(&kind) {
        let quantities = m.d(0x507dac)?;
        Ok((quantities & 0xffff0000) | m.b(quantities.wrapping_add(c))?)
    } else {
        Ok(0)
    }
}
pub fn mine(m: &MemoriaJogo, index: u32) -> Result<u32> {
    let index = index & 65535;
    if index >= 20 {
        return stop("MineGetCapacite invalid index", 0x475541);
    }
    m.w(0x509956 + 4 * index)
}
pub fn city(m: &mut MemoriaJogo, structure: u32) -> Result<u32> {
    let structure = structure & 65535;
    if structure >= 1000 {
        return stop("iagVilleSendMessage invalid structure", 0x484808);
    }
    let owner = m.b(0x49a0c8 + 276 * structure + 4)?;
    if owner >= 4 {
        return Ok(owner);
    }
    let kind = crate::frame_economy::call(m, "PlayerGetType", &[owner])? & 255;
    if kind == 2 {
        return stop("iagVilleSendMessage AI city handler", 0x48484c);
    }
    Ok(kind)
}
pub fn entry(m: &mut MemoriaJogo, name: &str, mut r: R) -> Result<R> {
    match name {
        "SacGetCapacite" => r.eax = sack(m, r.eax)?,
        "MineGetCapacite" => r.eax = mine(m, r.eax)?,
        "TuyauEstSortie" => {
            let i = r.eax & 65535;
            if i >= 1000 {
                return stop("TuyauEstSortie invalid structure", 0x420c7c);
            }
            let p = 0x49a0c8 + 276 * i;
            r.eax = (p & 0xffffff00) | u32::from(m.b(p + 0x76)? == 15 && m.b(p + 0x75)? != 0);
        }
        "iagVilleSendMessage" => {
            let structure = r.eax & 65535;
            r.eax = city(m, structure)?;
            r.edx = r.ebx;
            r.ebx = structure;
        }
        _ => return stop("unknown S1 query", 0),
    }
    r.esp = r.esp.wrapping_add(4);
    Ok(r)
}
