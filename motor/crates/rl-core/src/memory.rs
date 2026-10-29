use crate::{EngineError, Result};
use std::collections::BTreeMap;

/// Sparse, owned blocks, ordered by original 32-bit base. No implicit regions.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct MemoriaJogo {
    blocks: BTreeMap<u32, Vec<u8>>,
}
impl MemoriaJogo {
    pub fn from_blocks(blocks: impl IntoIterator<Item = (u32, Vec<u8>)>) -> Result<Self> {
        let mut result = Self::default();
        for (base, bytes) in blocks {
            result.declare(base, bytes)?;
        }
        Ok(result)
    }
    pub fn blocks(&self) -> impl Iterator<Item = (u32, &[u8])> {
        self.blocks
            .iter()
            .map(|(&base, bytes)| (base, bytes.as_slice()))
    }
    pub fn declare(&mut self, base: u32, bytes: Vec<u8>) -> Result<()> {
        if bytes.is_empty() {
            return Err(EngineError::EmptyRegion);
        }
        let end = u64::from(base)
            .checked_add(u64::try_from(bytes.len()).map_err(|_| EngineError::AddressOverflow)?)
            .ok_or(EngineError::AddressOverflow)?;
        if end > 1u64 << 32 {
            return Err(EngineError::AddressOverflow);
        }
        if let Some((&previous, data)) = self.blocks.range(..=base).next_back() {
            let previous_end = u64::from(previous)
                + u64::try_from(data.len()).map_err(|_| EngineError::AddressOverflow)?;
            if u64::from(base) < previous_end {
                return Err(EngineError::OverlappingRegions);
            }
        }
        if let Some((&next, _)) = self.blocks.range(base..).next() {
            if u64::from(next) < end {
                return Err(EngineError::OverlappingRegions);
            }
        }
        self.blocks.insert(base, bytes);
        Ok(())
    }
    pub fn remove(&mut self, base: u32) -> Result<Vec<u8>> {
        self.blocks
            .remove(&base)
            .ok_or(EngineError::UndeclaredAccess {
                address: base,
                size: 1,
            })
    }
    fn location(&self, address: u32, size: usize) -> Result<(u32, usize)> {
        if let Some((&base, data)) = self.blocks.range(..=address).next_back() {
            let offset =
                usize::try_from(address - base).map_err(|_| EngineError::AddressOverflow)?;
            if offset
                .checked_add(size)
                .is_some_and(|end| end <= data.len())
            {
                return Ok((base, offset));
            }
        }
        Err(EngineError::UndeclaredAccess { address, size })
    }
    pub fn read(&self, address: u32, size: usize) -> Result<&[u8]> {
        let (base, offset) = self.location(address, size)?;
        Ok(&self.blocks[&base][offset..offset + size])
    }
    pub fn write(&mut self, address: u32, bytes: &[u8]) -> Result<()> {
        let (base, offset) = self.location(address, bytes.len())?;
        self.blocks.get_mut(&base).expect("validated region")[offset..offset + bytes.len()]
            .copy_from_slice(bytes);
        Ok(())
    }
    pub fn u8(&self, address: u32) -> Result<u8> {
        Ok(self.read(address, 1)?[0])
    }
    pub fn u16(&self, address: u32) -> Result<u16> {
        Ok(u16::from_le_bytes(
            self.read(address, 2)?.try_into().expect("width"),
        ))
    }
    pub fn u32(&self, address: u32) -> Result<u32> {
        Ok(u32::from_le_bytes(
            self.read(address, 4)?.try_into().expect("width"),
        ))
    }
    pub fn set_u8(&mut self, address: u32, value: u8) -> Result<()> {
        self.write(address, &[value])
    }
    pub fn set_u16(&mut self, address: u32, value: u16) -> Result<()> {
        self.write(address, &value.to_le_bytes())
    }
    pub fn set_u32(&mut self, address: u32, value: u32) -> Result<()> {
        self.write(address, &value.to_le_bytes())
    }
    /// A missing whole field is absent; a partially captured field is an error.
    pub fn optional_u32(&self, address: u32) -> Result<Option<u32>> {
        if let Ok(value) = self.u32(address) {
            return Ok(Some(value));
        }
        if (0..4).any(|offset| self.u8(address.wrapping_add(offset)).is_ok()) {
            return Err(EngineError::IncompleteField { address });
        }
        Ok(None)
    }
}
