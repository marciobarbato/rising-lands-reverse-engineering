//! Semantic pilot state and an explicit original-address projection.
mod clock;
mod memory;
mod state;
pub use clock::*;
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
}
pub type Result<T> = std::result::Result<T, EngineError>;
impl std::fmt::Display for EngineError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{self:?}")
    }
}
impl std::error::Error for EngineError {}
