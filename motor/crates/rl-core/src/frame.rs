//! Original-width M2 phase orchestration. Host calls are explicit, recorded inputs.
use crate::{frame_ai, frame_core, frame_economy, frame_input, frame_missions, frame_units};
use crate::{EngineError, MemoriaJogo, Result};

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct FrameRegisters {
    pub eax: u32,
    pub ebx: u32,
    pub ecx: u32,
    pub edx: u32,
    pub esi: u32,
    pub edi: u32,
    pub ebp: u32,
    pub esp: u32,
}
#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct FrameInput {
    pub cursor_x: i32,
    pub cursor_y: i32,
    pub offscreen: u32,
    pub registers: FrameRegisters,
    pub saved: [u32; 3],
    pub msg: [u32; 4],
}
/// ids and fixed layout are published in rising_engine.h. Zero unused slots
/// are structural padding, never default answers for an unknown game call.
#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct FrameEvent {
    pub kind: u32,
    pub id: u32,
    pub site: u32,
    pub args: [u32; 5],
    pub result: u32,
    pub registers: [u32; 4],
    pub stack: [u32; 4],
    pub stack_mask: u32,
}
pub fn stop<T>(name: &'static str, address: u32) -> Result<T> {
    Err(EngineError::UnportedCallee { name, address })
}
pub fn binding(events: &mut Vec<FrameEvent>, id: u32, site: u32, args: &[u32], result: u32) {
    let mut e = FrameEvent {
        kind: 1,
        id,
        site,
        result,
        ..FrameEvent::default()
    };
    e.args[..args.len()].copy_from_slice(args);
    events.push(e);
}
pub fn boundary(
    m: &MemoriaJogo,
    events: &mut Vec<FrameEvent>,
    id: u32,
    site: u32,
    registers: [u32; 4],
    stack: [u32; 4],
    mask: u32,
) -> Result<()> {
    let mut e = FrameEvent {
        kind: 2,
        id,
        site,
        registers,
        stack,
        stack_mask: mask,
        ..FrameEvent::default()
    };
    if id == 102 || id == 104 {
        e.args[0] = u32::from(m.u8(0x4e2f28)?);
        e.args[1] = u32::from(m.u8(0x4e2f29)?);
    }
    events.push(e);
    Ok(())
}
fn free(
    m: &mut MemoriaJogo,
    events: &mut Vec<FrameEvent>,
    freed: &mut MemoriaJogo,
    p: u32,
) -> Result<()> {
    // Adopted GMEM_FIXED buffers. The harness supplies/checks their allocation
    // and lock records; no host pointer or allocator participates in game logic.
    let bytes = m.remove(p)?;
    let size = u32::try_from(bytes.len()).map_err(|_| EngineError::AddressOverflow)?;
    binding(events, 3, 0x467ed8, &[p], p);
    binding(events, 4, 0x467ee0, &[p], 0);
    binding(events, 3, 0x467ee8, &[p], p);
    binding(events, 5, 0x467ef0, &[p], 0);
    events.push(FrameEvent {
        kind: 3,
        args: [p, 0, 0, 0, 0],
        result: size,
        ..FrameEvent::default()
    });
    freed.declare(p, bytes)
}
fn delete_bank(
    m: &mut MemoriaJogo,
    events: &mut Vec<FrameEvent>,
    freed: &mut MemoriaJogo,
    p: u32,
) -> Result<()> {
    if p == 0 {
        return Ok(());
    }
    let count = m.u16(p)?;
    for i in 0..u32::from(count) {
        let table = m.u32(p.wrapping_add(4))?;
        let entry = m.u32(table.wrapping_add(4 * i))?;
        if entry != 0 {
            let data = m.u32(entry.wrapping_add(8))?;
            if data != 0 {
                free(m, events, freed, data)?;
            }
            free(m, events, freed, entry)?;
        }
    }
    m.set_u16(p, 0)?;
    let table = m.u32(p.wrapping_add(4))?;
    if table != 0 {
        free(m, events, freed, table)?;
    }
    free(m, events, freed, p)
}
pub fn call(m: &mut MemoriaJogo, name: &str, a: &[u32]) -> Result<u32> {
    match name {
        "EvenementEnCours" => Ok(u32::from(m.u8(0x4e1b0e)?)),
        "ProjectileInit" | "ProjectileSet" | "ProjectileLineaire" => {
            crate::frame_combat::call(m, name, a)
        }
        "MissionGetNum" => Ok(u32::from(m.u8(0x496fe4)?)),
        "InputGame" => {
            frame_input::input(m, a[0] as u8, &mut Vec::new())?;
            Ok(0)
        }
        "AffGame" => frame_input::affgame(m),
        "InputSend" => {
            if m.u8(0x4e0730)? != 0 {
                stop("InputSend network", 0x45ecac)
            } else {
                Ok(0)
            }
        }
        "CalculIconeAction" => frame_input::icons(m),
        "TestFinDeMission" => frame_missions::test(m, a[0] as u8),
        "ProjectileCalcul" => {
            let pool = m.u32(0x5080f0)?;
            let increment = m.u8(0x508f7c)?;
            for i in 0..100 {
                let p = pool.wrapping_add(56 * i);
                let kind = m.u8(p)?;
                let frame = m.u8(p + 0x18)?;
                let next = match kind {
                    1..=5 | 17 => Some(frame.wrapping_add(increment) & 3),
                    20..=23 => Some(frame.wrapping_add(increment) & 7),
                    29 | 30 => Some(if frame < 12 {
                        frame + 1
                    } else {
                        let n = (u16::from(frame) + 1) % 20;
                        if n == 0 {
                            12
                        } else {
                            n as u8
                        }
                    }),
                    6..=8 | 14..=16 | 18 | 19 | 24..=28 | 31..=34 => Some(frame.wrapping_add(1)),
                    _ => None,
                };
                if let Some(next) = next {
                    m.set_u8(p + 0x18, next)?;
                }
            }
            for _ in 0..30 {
                for i in 0..100 {
                    let p = pool.wrapping_add(56 * i);
                    if m.u8(p + 2)? == 0 || m.u8(p + 1)? != 0 {
                        continue;
                    }
                    let kind = m.u8(p)?;
                    let frame = m.u8(p + 0x18)?;
                    match kind {
                        0 | 35..=255 => {}
                        14..=16 | 26 | 27 | 31 | 32 => {
                            let limit = if kind <= 16 {
                                16
                            } else if kind <= 27 {
                                8
                            } else {
                                32
                            };
                            if frame == limit {
                                m.set_u8(p + 2, 0)?;
                            }
                        }
                        _ => return stop("ProjectileAvance active type", 0x46eaf8),
                    }
                }
                for i in 0..100 {
                    let p = pool.wrapping_add(56 * i);
                    if m.u8(p + 1)? != 0 {
                        m.set_u8(p + 1, 0)?;
                    }
                }
            }
            Ok(0)
        }
        "CalculNextReflect" | "AvanceMonstre" | "iaSolver" | "MessageBoxCalcul"
        | "ProcessInputGame" => frame_ai::call(m, name, a),
        "CalculEnginNextEtape"
        | "EnginNextEtape"
        | "CalculBatimentNextEtape"
        | "BatimentNextEtape" => frame_units::call(m, name, a),
        "PlayerGetType"
        | "RechercheCalcul"
        | "PlayerInitAllianceCompteur"
        | "SetUpdateChamp"
        | "UpdateChamp"
        | "CalculMatiere"
        | "CalculCompteurMarche"
        | "CalculCompteurProposition"
        | "PlayerAttaqueCalculSympa" => frame_economy::call(m, name, a),
        _ => frame_core::call(m, name, a),
    }
}
fn body(
    m: &mut MemoriaJogo,
    input: &FrameInput,
    events: &mut Vec<FrameEvent>,
    ebx: u32,
) -> Result<()> {
    // PlayerAttaqueReset 0x46d628 is an original RET.
    if call(m, "EvenementEnCours", &[])? as u8 != 0 {
        return Ok(());
    }
    if m.u8(0x4e2f28)? == 0 {
        let cursor = m.u8(0x4e1d18)?;
        let track = 2 + u32::from(m.u8(0x4e1c18 + u32::from(cursor))? % 2);
        m.set_u8(0x4e1d18, cursor.wrapping_add(1))?;
        boundary(
            m,
            events,
            102,
            0x42d32d,
            [
                track,
                0,
                (ebx & !255) | u32::from(cursor.wrapping_add(1)),
                2,
            ],
            [0; 4],
            0,
        )?;
    }
    let network = m.u8(0x4e0730)?;
    let local = m.u8(0x508041)?;
    for player in 0..if network != 0 { 4 } else { 5 } {
        match call(m, "PlayerGetType", &[player])? as u8 {
            1 => {
                if player == u32::from(local) {
                    frame_input::input(m, local, events)?;
                    call(m, "InputSend", &[player])?;
                } else {
                    return stop("InputReceive", 0x45ed03);
                }
            }
            2 => {
                let mission = call(m, "MissionGetNum", &[])?;
                call(m, "CalculNextReflect", &[player, mission])?;
                if player == u32::from(local) {
                    frame_input::input(m, local, events)?;
                }
            }
            _ => {}
        }
    }
    m.set_u8(0x4e2480, local)?;
    for player in 0..4 {
        call(m, "ProcessInputGame", &[player])?;
    }
    let state = m.u8(0x4e2f78)?;
    if state == 0x12 || (state == 0x10 && m.u8(0x4e0730)? != 0) {
        call(m, "MessageBoxCalcul", &[])?;
        m.set_u32(0x496d40, m.u32(0x496d40)?.wrapping_add(1))?;
        for name in [
            "CalculIconeAction",
            "ProjectileCalcul",
            "CalculEnginNextEtape",
            "CalculBatimentNextEtape",
            "RechercheCalcul",
            "PlayerInitAllianceCompteur",
            "SetUpdateChamp",
            "UpdateChamp",
            "CalculMatiere",
        ] {
            call(m, name, &[])?;
        }
        let p = u32::from(m.u8(0x508041)?);
        call(m, "CalculCompteurMarche", &[p])?;
        let p = u32::from(m.u8(0x508041)?);
        call(m, "CalculCompteurProposition", &[p, 0])?;
        let x = u32::from(m.u16(0x508720)?);
        let y = u32::from(m.u16(0x508722)?);
        call(m, "NextAnimTerrain", &[x, y])?;
        if m.u8(0x4e0730)? != 0 {
            return stop("NextAnimVegetFullMap", 0x472c55);
        }
        let x = u32::from(m.u16(0x508720)?);
        let y = u32::from(m.u16(0x508722)?);
        call(m, "NextAnimVeget", &[x, y])?;
        call(m, "PlayerAttaqueCalculSympa", &[])?;
        let p = u32::from(m.u8(0x508041)?);
        let result = call(m, "TestFinDeMission", &[p])? as u8;
        m.set_u8(0x4e05a0, result)?;
        if result != 0 {
            if m.u8(0x496fe4)? == 6 && m.u32(0x4e061c)? == 0 {
                return stop("MessageBoxSet", 0x479049);
            }
            let c = m.u32(0x4e061c)?.wrapping_add(1);
            m.set_u32(0x4e061c, c)?;
            if c as i32 >= 100 {
                return stop("MenuInit mission end", 0x42c931);
            }
        }
    }
    m.set_u8(0x5099b0, 0)?;
    let _ = input;
    Ok(())
}
pub fn phase(
    m: &mut MemoriaJogo,
    phase: u32,
    mut input: FrameInput,
) -> Result<(FrameInput, Vec<FrameEvent>, MemoriaJogo)> {
    let mut events = Vec::new();
    let mut freed = MemoriaJogo::default();
    match phase {
        1 => {
            frame_input::display_effects(m, 2)?;
            let x = u32::from(m.u16(0x508724)?.wrapping_shl(5).wrapping_sub(1));
            let y = u32::from(m.u16(0x508726)?.wrapping_shl(5).wrapping_sub(1));
            call(m, "SetClipping", &[0, 0, x, y])?;
            for a in [0x508f7c, 0x508f80, 0x508f84] {
                m.set_u32(a, 0)?;
            }
            frame_input::menu(m, &input, &mut events, |m, e, p| {
                delete_bank(m, e, &mut freed, p)
            })?;
            let ebx = call(m, "InitGameZone", &[1, 0])?;
            body(m, &input, &mut events, ebx)?;
        }
        2 => {
            let eax = frame_input::affgame(m)?;
            if m.u8(0x5099af)? != 0 {
                m.set_u8(0x5099af, 0)?;
                m.set_u8(0x5099ae, 0)?;
            }
            if m.u8(0x5099b2)? != 0 {
                m.set_u8(0x5099b1, 0)?;
                m.set_u8(0x5099b2, 0)?;
            }
            let mut r = input.registers;
            r.eax = eax;
            r.edx = input.saved[0];
            r.ecx = input.saved[1];
            r.ebx = input.saved[2];
            r.esp = r.esp.wrapping_add(24);
            boundary(
                m,
                &mut events,
                103,
                0x460220,
                [r.eax, r.edx, r.ebx, r.ecx],
                input.msg,
                15,
            )?;
            boundary(
                m,
                &mut events,
                104,
                0x460225,
                [r.eax, r.edx, r.ebx, r.ecx],
                input.msg,
                15,
            )?;
            if r.ebx as u8 != m.u8(0x49a059)? {
                return stop("WinMain quit path", 0x460227);
            }
            binding(
                &mut events,
                6,
                0x4601d8,
                &[r.esp, r.ebx, r.ebx, r.ebx, r.ebx],
                0,
            );
            if r.ebx as u8 == m.u8(0x49a058)? {
                return stop("WinMain WaitMessage", 0x460214);
            }
            r.esp = r.esp.wrapping_sub(24);
            let c = m.u32(0x508f7c)?.wrapping_add(1);
            m.set_u32(0x508f7c, c)?;
            if c % 2 == 0 {
                m.set_u32(0x508f80, m.u32(0x508f80)?.wrapping_add(1))?;
            }
            if c % 3 == 0 {
                m.set_u32(0x508f84, m.u32(0x508f84)?.wrapping_add(1))?;
            }
            r.ebx = 3;
            r.edx = r.esp;
            binding(&mut events, 7, 0x47504b, &[r.esp], 1);
            m.set_u16(0x5099a8, input.cursor_x as u16)?;
            m.set_u16(0x5099aa, input.cursor_y as u16)?;
            r.eax = input.cursor_y as u32;
            r.esp = r.esp.wrapping_sub(4);
            input.registers = r;
        }
        3 => {
            m.set_u16(0x49a010, 0x1dd8)?;
            binding(
                &mut events,
                8,
                0x42c8a5,
                &[u32::from(m.u16(0x5099a8)?), u32::from(m.u16(0x5099aa)?)],
                1,
            );
            if m.u8(0x4e2f78)? != 0x12 {
                return stop("CalculGame game state", 0x42c868);
            }
            body(m, &input, &mut events, input.registers.ebx)?;
            input.registers.esp = input.registers.esp.wrapping_add(4);
        }
        _ => return Err(EngineError::InvalidFramePhase(phase)),
    }
    Ok((input, events, freed))
}

/// Parent phase leaves exposed for bounded isolated comparisons.
pub fn isolated(id: u32) -> Option<(&'static str, usize)> {
    Some(match id {
        300 => ("InputGame", 1),
        301 => ("InputSend", 1),
        302 => ("CalculIconeAction", 0),
        303 => ("EvenementEnCours", 0),
        304 => ("TestFinDeMission", 1),
        305 => ("ProjectileCalcul", 0),
        306 => ("AffGame", 0),
        _ => return None,
    })
}
