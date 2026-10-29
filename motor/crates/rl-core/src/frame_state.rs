//! Incremental semantic frame state and explicit original-layout bindings.
//!
//! Providers execute against a private projected transaction and reload these
//! semantic values after success. Unmodeled record bytes stay in Projection's
//! template; they never become zero-filled or invented Rust state.
use crate::{EngineError, MemoriaJogo, Result};

pub const UNIT_COUNT: usize = 800;
pub const STRUCTURE_COUNT: usize = 1000;
const STRIDE: u32 = 276;
const UNIT_POOL_POINTER: u32 = 0x4e19a0;
const STRUCTURE_POOL: u32 = 0x49a0c8;

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct UnitState {
    pub owner: u8,
    pub kind: u8,
    pub state: u8,
    pub provisions: u16,
    pub cell: u16,
    pub on_map: u8,
    pub fatigue_ticks: u16,
    pub previous_cell: u16,
    pub destination_cell: u16,
    pub moving: u8,
    pub turning: u8,
    pub order: u8,
    pub attack_phase: u8,
    pub facing: u8,
    pub target_facing: u8,
    pub airborne: u8,
    pub attack_range: u8,
    pub vision_radius: u8,
    pub special_direction: u8,
    pub status_flags: u8,
    pub fatigue_bonus: u8,
    pub frame_flag: u8,
    pub collision_cell_0: u16,
    pub collision_cell_1: u16,
    pub collision_cell_2: u16,
    pub collision_cell_3: u16,
    pub reload_ticks: u16,
    pub sound_handle: u32,
    pub next_group_unit: u16,
    pub observed_state: u8,
    pub observed_order: u8,
    pub group: u32,
}
impl UnitState {
    fn load(m: &MemoriaJogo, base: u32) -> Result<Self> {
        Ok(Self {
            owner: m.u8(base.wrapping_add(0x0))?,
            kind: m.u8(base.wrapping_add(0x1))?,
            state: m.u8(base.wrapping_add(0x2))?,
            provisions: m.u16(base.wrapping_add(0x4))?,
            cell: m.u16(base.wrapping_add(0x8))?,
            on_map: m.u8(base.wrapping_add(0x72))?,
            fatigue_ticks: m.u16(base.wrapping_add(0x74))?,
            previous_cell: m.u16(base.wrapping_add(0x7c))?,
            destination_cell: m.u16(base.wrapping_add(0x7e))?,
            moving: m.u8(base.wrapping_add(0x86))?,
            turning: m.u8(base.wrapping_add(0x87))?,
            order: m.u8(base.wrapping_add(0x89))?,
            attack_phase: m.u8(base.wrapping_add(0x8a))?,
            facing: m.u8(base.wrapping_add(0x90))?,
            target_facing: m.u8(base.wrapping_add(0x91))?,
            airborne: m.u8(base.wrapping_add(0xab))?,
            attack_range: m.u8(base.wrapping_add(0xb0))?,
            vision_radius: m.u8(base.wrapping_add(0xbb))?,
            special_direction: m.u8(base.wrapping_add(0xda))?,
            status_flags: m.u8(base.wrapping_add(0xdc))?,
            fatigue_bonus: m.u8(base.wrapping_add(0xf8))?,
            frame_flag: m.u8(base.wrapping_add(0xf9))?,
            collision_cell_0: m.u16(base.wrapping_add(0xfa))?,
            collision_cell_1: m.u16(base.wrapping_add(0xfc))?,
            collision_cell_2: m.u16(base.wrapping_add(0xfe))?,
            collision_cell_3: m.u16(base.wrapping_add(0x100))?,
            reload_ticks: m.u16(base.wrapping_add(0x102))?,
            sound_handle: m.u32(base.wrapping_add(0x104))?,
            next_group_unit: m.u16(base.wrapping_add(0x108))?,
            observed_state: m.u8(base.wrapping_add(0x10a))?,
            observed_order: m.u8(base.wrapping_add(0x10b))?,
            group: m.u32(base.wrapping_add(0x10c))?,
        })
    }
    fn project(&self, m: &mut MemoriaJogo, base: u32) -> Result<()> {
        m.set_u8(base.wrapping_add(0x0), self.owner)?;
        m.set_u8(base.wrapping_add(0x1), self.kind)?;
        m.set_u8(base.wrapping_add(0x2), self.state)?;
        m.set_u16(base.wrapping_add(0x4), self.provisions)?;
        m.set_u16(base.wrapping_add(0x8), self.cell)?;
        m.set_u8(base.wrapping_add(0x72), self.on_map)?;
        m.set_u16(base.wrapping_add(0x74), self.fatigue_ticks)?;
        m.set_u16(base.wrapping_add(0x7c), self.previous_cell)?;
        m.set_u16(base.wrapping_add(0x7e), self.destination_cell)?;
        m.set_u8(base.wrapping_add(0x86), self.moving)?;
        m.set_u8(base.wrapping_add(0x87), self.turning)?;
        m.set_u8(base.wrapping_add(0x89), self.order)?;
        m.set_u8(base.wrapping_add(0x8a), self.attack_phase)?;
        m.set_u8(base.wrapping_add(0x90), self.facing)?;
        m.set_u8(base.wrapping_add(0x91), self.target_facing)?;
        m.set_u8(base.wrapping_add(0xab), self.airborne)?;
        m.set_u8(base.wrapping_add(0xb0), self.attack_range)?;
        m.set_u8(base.wrapping_add(0xbb), self.vision_radius)?;
        m.set_u8(base.wrapping_add(0xda), self.special_direction)?;
        m.set_u8(base.wrapping_add(0xdc), self.status_flags)?;
        m.set_u8(base.wrapping_add(0xf8), self.fatigue_bonus)?;
        m.set_u8(base.wrapping_add(0xf9), self.frame_flag)?;
        m.set_u16(base.wrapping_add(0xfa), self.collision_cell_0)?;
        m.set_u16(base.wrapping_add(0xfc), self.collision_cell_1)?;
        m.set_u16(base.wrapping_add(0xfe), self.collision_cell_2)?;
        m.set_u16(base.wrapping_add(0x100), self.collision_cell_3)?;
        m.set_u16(base.wrapping_add(0x102), self.reload_ticks)?;
        m.set_u32(base.wrapping_add(0x104), self.sound_handle)?;
        m.set_u16(base.wrapping_add(0x108), self.next_group_unit)?;
        m.set_u8(base.wrapping_add(0x10a), self.observed_state)?;
        m.set_u8(base.wrapping_add(0x10b), self.observed_order)?;
        m.set_u32(base.wrapping_add(0x10c), self.group)?;
        Ok(())
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct StructureState {
    pub origin_cell: u16,
    pub owner: u8,
    pub state: u8,
    pub kind: u8,
    pub production_enabled: u8,
    pub requested_kind: u8,
    pub production_progress: u32,
    pub illuminated_player_0: u8,
    pub illuminated_player_1: u8,
    pub illuminated_player_2: u8,
    pub illuminated_player_3: u8,
}
impl StructureState {
    fn load(m: &MemoriaJogo, base: u32) -> Result<Self> {
        Ok(Self {
            origin_cell: m.u16(base.wrapping_add(0x2))?,
            owner: m.u8(base.wrapping_add(0x4))?,
            state: m.u8(base.wrapping_add(0x5))?,
            kind: m.u8(base.wrapping_add(0x8))?,
            production_enabled: m.u8(base.wrapping_add(0x74))?,
            requested_kind: m.u8(base.wrapping_add(0x7b))?,
            production_progress: m.u32(base.wrapping_add(0x8c))?,
            illuminated_player_0: m.u8(base.wrapping_add(0x110))?,
            illuminated_player_1: m.u8(base.wrapping_add(0x111))?,
            illuminated_player_2: m.u8(base.wrapping_add(0x112))?,
            illuminated_player_3: m.u8(base.wrapping_add(0x113))?,
        })
    }
    fn project(&self, m: &mut MemoriaJogo, base: u32) -> Result<()> {
        m.set_u16(base.wrapping_add(0x2), self.origin_cell)?;
        m.set_u8(base.wrapping_add(0x4), self.owner)?;
        m.set_u8(base.wrapping_add(0x5), self.state)?;
        m.set_u8(base.wrapping_add(0x8), self.kind)?;
        m.set_u8(base.wrapping_add(0x74), self.production_enabled)?;
        m.set_u8(base.wrapping_add(0x7b), self.requested_kind)?;
        m.set_u32(base.wrapping_add(0x8c), self.production_progress)?;
        m.set_u8(base.wrapping_add(0x110), self.illuminated_player_0)?;
        m.set_u8(base.wrapping_add(0x111), self.illuminated_player_1)?;
        m.set_u8(base.wrapping_add(0x112), self.illuminated_player_2)?;
        m.set_u8(base.wrapping_add(0x113), self.illuminated_player_3)?;
        Ok(())
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct FrameGlobals {
    pub game_frame: u32,
    pub mission: u8,
    pub ai_rng_seed: u32,
    pub end_condition: u8,
    pub hud_refresh: u8,
    pub end_condition_ticks: u32,
    pub network: u8,
    pub permutation_cursor: u8,
    pub input_player: u8,
    pub music_disabled: u8,
    pub game_state: u8,
    pub local_player: u8,
    pub view_x: u16,
    pub view_y: u16,
    pub view_width: u16,
    pub view_height: u16,
    pub iteration: u32,
    pub iteration_secondary: u32,
    pub iteration_tertiary: u32,
    pub cursor_x: u16,
    pub cursor_y: u16,
    pub frame_exit: u8,
    pub unit_counts: [u16; 5],
    pub structure_counts: [u32; 4],
    pub local_unit_count: u16,
    pub other_unit_count: u16,
    pub unit_kind_counts: [[u16; 26]; 4],
}
impl FrameGlobals {
    fn load(m: &MemoriaJogo) -> Result<Self> {
        let mut unit_counts = [0u16; 5];
        for (i, value) in unit_counts.iter_mut().enumerate() {
            *value = m.u16(0x4e1928 + 2 * i as u32)?;
        }
        let mut structure_counts = [0u32; 4];
        for (i, value) in structure_counts.iter_mut().enumerate() {
            *value = m.u32(0x4dfaa8 + 4 * i as u32)?;
        }
        let mut unit_kind_counts = [[0u16; 26]; 4];
        for (owner, kinds) in unit_kind_counts.iter_mut().enumerate() {
            for (kind, value) in kinds.iter_mut().enumerate() {
                *value = m.u16(0x4e1a3c + owner as u32 * 0x34 + kind as u32 * 2)?;
            }
        }
        Ok(Self {
            game_frame: m.u32(0x496d40)?,
            mission: m.u8(0x496fe4)?,
            ai_rng_seed: m.u32(0x498db4)?,
            end_condition: m.u8(0x4e05a0)?,
            hud_refresh: m.u8(0x4e05a2)?,
            end_condition_ticks: m.u32(0x4e061c)?,
            network: m.u8(0x4e0730)?,
            permutation_cursor: m.u8(0x4e1d18)?,
            input_player: m.u8(0x4e2480)?,
            music_disabled: m.u8(0x4e2f28)?,
            game_state: m.u8(0x4e2f78)?,
            local_player: m.u8(0x508041)?,
            view_x: m.u16(0x508720)?,
            view_y: m.u16(0x508722)?,
            view_width: m.u16(0x508724)?,
            view_height: m.u16(0x508726)?,
            iteration: m.u32(0x508f7c)?,
            iteration_secondary: m.u32(0x508f80)?,
            iteration_tertiary: m.u32(0x508f84)?,
            cursor_x: m.u16(0x5099a8)?,
            cursor_y: m.u16(0x5099aa)?,
            frame_exit: m.u8(0x5099b0)?,
            unit_counts,
            structure_counts,
            unit_kind_counts,
            local_unit_count: m.u16(0x4e1a3a)?,
            other_unit_count: m.u16(0x4e1a38)?,
        })
    }
    fn project(&self, m: &mut MemoriaJogo) -> Result<()> {
        m.set_u32(0x496d40, self.game_frame)?;
        m.set_u8(0x496fe4, self.mission)?;
        m.set_u32(0x498db4, self.ai_rng_seed)?;
        m.set_u8(0x4e05a0, self.end_condition)?;
        m.set_u8(0x4e05a2, self.hud_refresh)?;
        m.set_u32(0x4e061c, self.end_condition_ticks)?;
        m.set_u8(0x4e0730, self.network)?;
        m.set_u8(0x4e1d18, self.permutation_cursor)?;
        m.set_u8(0x4e2480, self.input_player)?;
        m.set_u8(0x4e2f28, self.music_disabled)?;
        m.set_u8(0x4e2f78, self.game_state)?;
        m.set_u8(0x508041, self.local_player)?;
        m.set_u16(0x508720, self.view_x)?;
        m.set_u16(0x508722, self.view_y)?;
        m.set_u16(0x508724, self.view_width)?;
        m.set_u16(0x508726, self.view_height)?;
        m.set_u32(0x508f7c, self.iteration)?;
        m.set_u32(0x508f80, self.iteration_secondary)?;
        m.set_u32(0x508f84, self.iteration_tertiary)?;
        m.set_u16(0x5099a8, self.cursor_x)?;
        m.set_u16(0x5099aa, self.cursor_y)?;
        m.set_u8(0x5099b0, self.frame_exit)?;
        for (i, value) in self.unit_counts.iter().enumerate() {
            m.set_u16(0x4e1928 + 2 * i as u32, *value)?;
        }
        for (i, value) in self.structure_counts.iter().enumerate() {
            m.set_u32(0x4dfaa8 + 4 * i as u32, *value)?;
        }
        for (owner, kinds) in self.unit_kind_counts.iter().enumerate() {
            for (kind, value) in kinds.iter().enumerate() {
                m.set_u16(0x4e1a3c + owner as u32 * 0x34 + kind as u32 * 2, *value)?;
            }
        }
        m.set_u16(0x4e1a3a, self.local_unit_count)?;
        m.set_u16(0x4e1a38, self.other_unit_count)?;
        Ok(())
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct FrameState {
    pub units: Vec<UnitState>,
    pub structures: Vec<StructureState>,
    pub globals: FrameGlobals,
    unit_pool_base: u32,
}

// Scope detection is deliberately structural: a sparse routine fixture is
// not a complete mission. Missing regions leave FrameState absent; no field
// value or missing part of a pool is synthesized.
fn declared(m: &MemoriaJogo, address: u32, size: usize) -> Result<bool> {
    match m.read(address, size) {
        Ok(_) => Ok(true),
        Err(EngineError::UndeclaredAccess { .. }) => Ok(false),
        Err(error) => Err(error),
    }
}

impl FrameState {
    pub fn unit_pool_base(&self) -> u32 {
        self.unit_pool_base
    }

    fn layout(m: &MemoriaJogo) -> Result<Option<u32>> {
        let Some(base) = m.optional_u32(UNIT_POOL_POINTER)? else {
            return Ok(None);
        };
        if !declared(m, base, UNIT_COUNT * STRIDE as usize)?
            || !declared(m, STRUCTURE_POOL, STRUCTURE_COUNT * STRIDE as usize)?
        {
            return Ok(None);
        }
        for (address, size) in [
            (0x496d40, 4),
            (0x496fe4, 1),
            (0x498db4, 4),
            (0x4e05a0, 1),
            (0x4e05a2, 1),
            (0x4e061c, 4),
            (0x4e0730, 1),
            (0x4e1d18, 1),
            (0x4e2480, 1),
            (0x4e2f28, 1),
            (0x4e2f78, 1),
            (0x508041, 1),
            (0x508720, 2),
            (0x508722, 2),
            (0x508724, 2),
            (0x508726, 2),
            (0x508f7c, 4),
            (0x508f80, 4),
            (0x508f84, 4),
            (0x5099a8, 2),
            (0x5099aa, 2),
            (0x5099b0, 1),
            (0x4e1928, 10),
            (0x4dfaa8, 16),
            (0x4e1a38, 4),
            (0x4e1a3c, 208),
        ] {
            if !declared(m, address, size)? {
                return Ok(None);
            }
        }
        Ok(Some(base))
    }

    pub fn load(m: &MemoriaJogo) -> Result<Option<Self>> {
        let Some(base) = Self::layout(m)? else {
            return Ok(None);
        };
        let units = (0..UNIT_COUNT)
            .map(|i| UnitState::load(m, base.wrapping_add(i as u32 * STRIDE)))
            .collect::<Result<Vec<_>>>()?;
        let structures = (0..STRUCTURE_COUNT)
            .map(|i| StructureState::load(m, STRUCTURE_POOL + i as u32 * STRIDE))
            .collect::<Result<Vec<_>>>()?;
        Ok(Some(Self {
            units,
            structures,
            globals: FrameGlobals::load(m)?,
            unit_pool_base: base,
        }))
    }

    pub fn project(&self, m: &mut MemoriaJogo) -> Result<()> {
        if self.units.len() != UNIT_COUNT
            || self.structures.len() != STRUCTURE_COUNT
            || Self::layout(m)? != Some(self.unit_pool_base)
        {
            return Err(EngineError::ProjectionFieldMismatch {
                address: UNIT_POOL_POINTER,
            });
        }
        for (i, unit) in self.units.iter().enumerate() {
            unit.project(m, self.unit_pool_base.wrapping_add(i as u32 * STRIDE))?;
        }
        for (i, structure) in self.structures.iter().enumerate() {
            structure.project(m, STRUCTURE_POOL + i as u32 * STRIDE)?;
        }
        self.globals.project(m)
    }
}
