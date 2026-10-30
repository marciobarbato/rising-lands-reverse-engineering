//! Semantic pilot state and an explicit original-address projection.
mod clock;
pub mod frame;
pub mod frame_combat;
pub mod frame_runtime_state;
pub mod frame_tasks;
pub mod render;
pub mod render_assets;
mod render_hud;
mod render_scene;
mod render_scripted;
mod render_units;
pub use frame_runtime_state::RuntimeState;
pub mod frame_ai;
pub mod frame_core;
pub mod frame_economy;
pub mod frame_input;
pub mod frame_missions;
pub mod frame_movement;
pub mod frame_path;
pub mod frame_raid;
pub mod frame_spawn;
pub mod frame_state;
pub use frame_state::{FrameGlobals, FrameState, StructureState, UnitState};
pub mod frame_units;
mod memory;
mod state;
pub use clock::*;
pub use frame::{FrameEvent, FrameInput, FrameRegisters};
pub use memory::*;
pub use state::*;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum EngineError {
    EmptyRegion,
    AddressOverflow,
    OverlappingRegions,
    UndeclaredAccess { address: u32, size: usize },
    IncompleteField { address: u32 },
    ProjectionFieldMismatch { address: u32 },
    UnsupportedThreadGetter { address: u32, value: u32 },
    UnknownRoutine(u32),
    InvalidTickRate,
    UnportedCallee { name: &'static str, address: u32 },
    InvalidFramePhase(u32),
    InvalidExecutionMode(u32),
    ExecutionReplayMismatch,
    ExecutionProjectionMismatch,
}
pub type Result<T> = std::result::Result<T, EngineError>;
impl std::fmt::Display for EngineError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::UnportedCallee { name, address } => write!(f, "{name} at 0x{address:08x}"),
            _ => write!(f, "{self:?}"),
        }
    }
}
impl std::error::Error for EngineError {}

pub mod player;
mod player_audio;
mod player_build;
mod player_input;
mod player_loop;
mod player_orders;
mod player_sight;

mod play;

mod chain_bags;
mod chain_display_origins;
mod chain_fatigue;
mod chain_queries;
mod chain_recruit;
mod chain_restore;
mod chain_s1;
mod chain_search;
mod chain_turret;
mod chain_work;

mod chain_entry;
mod chain_habitation;
pub mod chain_stage5;
mod chain_vision;
mod player_cave;

mod chain_groups;

mod render_chain;
