//! Graphics render API 1.7: read-only live state, persistent indexed surface/cache.
use crate::render_assets::{Assets, Sprite};
use crate::{EngineError, MemoriaJogo};
use std::{collections::BTreeMap, sync::Arc};
#[derive(Debug)]
pub enum Error {
    Memory(EngineError),
    Invalid(&'static str),
    Stop(u32, String),
}
impl From<EngineError> for Error {
    fn from(e: EngineError) -> Self {
        Self::Memory(e)
    }
}
pub type Result<T> = std::result::Result<T, Error>;
#[derive(Clone)]
pub struct Cache {
    pub keys: Vec<u8>,
    pub raw: Vec<u8>,
    pub cursor: u16,
}
impl Cache {
    pub fn validate(&self) -> Result<()> {
        if self.keys.len() != 1024 || self.raw.len() != 270336 || self.cursor > 255 {
            Err(Error::Invalid("terrain cache dimensions/cursor"))
        } else {
            Ok(())
        }
    }
}
#[repr(C)]
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Observation {
    pub kind: u32,
    pub address: u32,
    pub name: [u8; 48],
    pub count: u32,
    pub args: [i32; 8],
    pub before: [u8; 8],
    pub after: [u8; 8],
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct SavedBackground {
    pub address: u32,
    pub pixels: Vec<u8>,
}
/// Fixture-only attestation of the original probe's non-executed AffText boundary.
/// The C ABI never installs these; production rendering always reports glyph stops.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct RecordedTextBoundary {
    pub text: Vec<u8>,
    pub rectangle: [i32; 4],
    pub font: u32,
    pub flags: [u32; 2],
    pub surface_sha256: [u8; 32],
}
#[derive(Clone, Debug)]
pub struct Outcome {
    pub text_boundaries_checked: u32,
    pub disposition: u32,
    pub stop: Option<(u32, String)>,
    pub observations: Vec<Observation>,
}
#[derive(Clone)]
pub struct Renderer {
    pub audit: bool,
    pub saved_background: Option<SavedBackground>,
    pub recorded_text_boundaries: Option<std::collections::VecDeque<RecordedTextBoundary>>,
    pub tick: Option<u32>,
    pub assets: Arc<Assets>,
    pub surface: Vec<u8>,
    pub cache: Cache,
    pub cache_generation: u64,
    pub last: Option<(u64, u32, Outcome)>,
}
impl Renderer {
    pub fn new(assets: Arc<Assets>, surface: &[u8], cache: Cache) -> Result<Self> {
        cache.validate()?;
        if surface.len() != 480000 {
            return Err(Error::Invalid("initial surface must have 480000 indices"));
        }
        Ok(Self {
            audit: true,
            saved_background: None,
            recorded_text_boundaries: None,
            tick: None,
            assets,
            surface: surface.to_vec(),
            cache,
            cache_generation: 0,
            last: None,
        })
    }
    /// Reuse the atomic render transaction's buffers. Previous pixels/cache are
    /// copied because skipped drawing and unexpected errors must preserve them.
    pub fn prepare_from(&mut self, previous: &Self) {
        self.audit = previous.audit;
        self.surface.clone_from(&previous.surface);
        self.cache.keys.clone_from(&previous.cache.keys);
        self.cache.raw.clone_from(&previous.cache.raw);
        self.cache.cursor = previous.cache.cursor;
        self.assets = Arc::clone(&previous.assets);
        self.tick = previous.tick;
        self.cache_generation = previous.cache_generation;
        self.last.clone_from(&previous.last);
        self.recorded_text_boundaries
            .clone_from(&previous.recorded_text_boundaries);
        match (&mut self.saved_background, &previous.saved_background) {
            (Some(next), Some(old)) => {
                next.address = old.address;
                next.pixels.clone_from(&old.pixels);
            }
            _ => self.saved_background.clone_from(&previous.saved_background),
        }
    }
    pub fn reset(&mut self, surface: &[u8], cache: Cache) -> Result<()> {
        cache.validate()?;
        if surface.len() != 480000 {
            return Err(Error::Invalid("surface size"));
        }
        self.surface.copy_from_slice(surface);
        self.cache = cache;
        self.cache_generation = self.cache_generation.wrapping_add(1);
        self.last = None;
        self.saved_background = None;
        self.recorded_text_boundaries = None;
        Ok(())
    }
    #[doc(hidden)]
    pub fn render_building_fixture(
        &mut self,
        m: &MemoriaJogo,
        x: i32,
        y: i32,
        cell: u32,
    ) -> Result<Outcome> {
        let assets = Arc::clone(&self.assets);
        let mut c = Context {
            background: &mut self.saved_background,
            text_boundaries: &mut self.recorded_text_boundaries,
            text_checked: 0,
            tick: self.tick,
            m,
            overrides: BTreeMap::new(),
            surface: &mut self.surface,
            cache: &mut self.cache,
            assets: &assets,
            observations: Vec::new(),
            audit: self.audit,
            clip: [
                m.u16(0x49a020)? as i32,
                m.u16(0x49a01c)? as i32,
                m.u16(0x49a022)? as i32,
                m.u16(0x49a01e)? as i32,
            ],
            camera: m.u8(0x508041)? as u32,
        };
        let tile = m.u16(m.u32(0x507d70)? + cell * 2)? as u32;
        let code = m.u8(m.u32(0x507d74)? + cell)?;
        let discovery = m.u8(m.u32(0x507d78 + 4 * c.camera)? + cell)?;
        let result = c.building(x, y, cell, tile, code, discovery);
        let stop = match result {
            Ok(()) => None,
            Err(Error::Stop(a, s)) => Some((a, s)),
            Err(e) => return Err(e),
        };
        Ok(Outcome {
            disposition: if stop.is_some() { 2 } else { 0 },
            stop,
            observations: c.observations,
            text_boundaries_checked: 0,
        })
    }
    pub fn render(&mut self, m: &MemoriaJogo, hud: bool) -> Result<Outcome> {
        let assets = Arc::clone(&self.assets);
        let mut c = Context {
            background: &mut self.saved_background,
            text_boundaries: &mut self.recorded_text_boundaries,
            text_checked: 0,
            tick: self.tick,
            m,
            overrides: BTreeMap::new(),
            surface: &mut self.surface,
            cache: &mut self.cache,
            assets: &assets,
            observations: Vec::new(),
            audit: self.audit,
            clip: [0, 0, 799, 599],
            camera: 0,
        };
        let result = c.compose(hud);
        if result.as_ref().is_ok_and(|d| *d == 0)
            && c.text_boundaries.as_ref().is_some_and(|b| !b.is_empty())
        {
            return Err(Error::Invalid("Unconsumed AffText probe boundary"));
        }
        let (disposition, stop) = match result {
            Ok(d) => (d, None),
            Err(Error::Stop(a, s)) => (2, Some((a, s))),
            Err(e) => return Err(e),
        };
        if disposition != 1 {
            self.cache_generation = self.cache_generation.wrapping_add(1);
        }
        Ok(Outcome {
            text_boundaries_checked: c.text_checked,
            disposition,
            stop,
            observations: c.observations,
        })
    }
}
pub(crate) struct Context<'a> {
    pub background: &'a mut Option<SavedBackground>,
    pub text_boundaries: &'a mut Option<std::collections::VecDeque<RecordedTextBoundary>>,
    pub text_checked: u32,
    pub tick: Option<u32>,
    pub m: &'a MemoriaJogo,
    pub overrides: BTreeMap<u32, u8>,
    pub surface: &'a mut Vec<u8>,
    pub cache: &'a mut Cache,
    pub assets: &'a Assets,
    pub observations: Vec<Observation>,
    pub audit: bool,
    pub clip: [i32; 4],
    pub camera: u32,
}
pub(crate) fn w(r: &[u8], o: usize) -> u32 {
    u16::from_le_bytes(r[o..o + 2].try_into().unwrap()) as u32
}
pub(crate) fn dw(r: &[u8], o: usize) -> u32 {
    u32::from_le_bytes(r[o..o + 4].try_into().unwrap())
}
pub(crate) fn i16(v: i32) -> i32 {
    v as i16 as i32
}
impl Context<'_> {
    pub fn u8(&self, a: u32) -> Result<u32> {
        Ok(if let Some(v) = self.overrides.get(&a) {
            *v
        } else if let Some(background) = self
            .background
            .as_ref()
            .filter(|b| a >= b.address && (a - b.address) < b.pixels.len() as u32)
        {
            background.pixels[(a - background.address) as usize]
        } else {
            self.m.u8(a)?
        } as u32)
    }
    pub fn u16(&self, a: u32) -> Result<u32> {
        Ok(self.u8(a)? | self.u8(a + 1)? << 8)
    }
    pub fn u32(&self, a: u32) -> Result<u32> {
        Ok(self.u16(a)? | self.u16(a + 2)? << 16)
    }
    pub fn read(&self, a: u32, n: usize) -> Result<Vec<u8>> {
        (0..n)
            .map(|i| self.u8(a + i as u32).map(|v| v as u8))
            .collect()
    }
    pub fn stop<T>(&self, a: u32, s: impl Into<String>) -> Result<T> {
        Err(Error::Stop(a, s.into()))
    }
    pub fn observe(&mut self, name: &str, a: u32, args: &[i32]) {
        if !self.audit {
            return;
        }
        let mut n = [0; 48];
        let len = name.len().min(47);
        n[..len].copy_from_slice(&name.as_bytes()[..len]);
        let mut values = [0; 8];
        values[..args.len()].copy_from_slice(args);
        self.observations.push(Observation {
            kind: 2,
            address: a,
            name: n,
            count: args.len() as u32,
            args: values,
            before: [0; 8],
            after: [0; 8],
        });
    }
    pub fn put(&mut self, name: &str, a: u32, b: &[u8]) -> Result<()> {
        let old = self.read(a, b.len())?;
        if old != b && self.audit {
            self.observe(name, a, &[]);
            let e = self.observations.last_mut().unwrap();
            e.kind = 1;
            e.count = b.len() as u32;
            e.before[..b.len()].copy_from_slice(&old);
            e.after[..b.len()].copy_from_slice(b);
        }
        for (i, v) in b.iter().enumerate() {
            self.overrides.insert(a + i as u32, *v);
        }
        Ok(())
    }
    pub fn put16(&mut self, n: &str, a: u32, v: u32) -> Result<()> {
        self.put(n, a, &(v as u16).to_le_bytes())
    }
    pub fn put32(&mut self, n: &str, a: u32, v: u32) -> Result<()> {
        self.put(n, a, &v.to_le_bytes())
    }
    pub fn screen_clip(&self) -> [i32; 4] {
        [0, 0, 799, 599]
    }
    pub fn raster(
        &mut self,
        id: u32,
        x: i32,
        y: i32,
        op: u32,
        owner: u32,
        clip: [i32; 4],
    ) -> Result<()> {
        if op == 3 && owner > 4 {
            return Err(Error::Invalid("player table owner outside 0..4"));
        }
        let q = self.assets.sprite(id)?;
        self.raster_sprite(q, x, y, op, owner, clip);
        Ok(())
    }
    fn raster_sprite(&mut self, q: &Sprite, x: i32, y: i32, op: u32, owner: u32, clip: [i32; 4]) {
        let [l, t, r, b] = clip;
        let l = l.max(0);
        let t = t.max(0);
        let r = r.min(799);
        let b = b.min(599);
        for sy in 0.max(t - y)..(q.height as i32).min(b - y + 1) {
            for sx in 0.max(l - x)..(q.width as i32).min(r - x + 1) {
                let src = sy as usize * q.width + sx as usize;
                if q.mask[src] == 0 {
                    continue;
                }
                let dest = (y + sy) as usize * 800 + (x + sx) as usize;
                let v = self.surface[dest];
                self.surface[dest] = match op {
                    1 => self.assets.shadow[v as usize],
                    2 => self.assets.light[v as usize],
                    3 => player(q.pixels[src], owner),
                    _ => q.pixels[src],
                };
            }
        }
    }
    pub fn bob(
        &mut self,
        x: i32,
        y: i32,
        id: u32,
        clipped: bool,
        owner: Option<u32>,
    ) -> Result<()> {
        let name = if owner.is_some() {
            "PastePlayerCmp"
        } else {
            "PasteBobCmp"
        };
        let mut args = vec![x, y, id as i32, clipped as i32];
        if let Some(o) = owner {
            args.push(o as i32);
        }
        self.observe(
            name,
            if owner.is_some() { 0x45c455 } else { 0x45b247 },
            &args,
        );
        self.raster(
            id,
            x,
            y,
            if owner.is_some() { 3 } else { 0 },
            owner.unwrap_or(0),
            if clipped {
                self.clip
            } else {
                self.screen_clip()
            },
        )
    }
    pub fn shadow(&mut self, x: i32, y: i32, id: u32, light: bool) -> Result<()> {
        self.observe(
            if light {
                "PasteEclairCmp"
            } else {
                "PasteOmbreCmp"
            },
            if light { 0x45ba23 } else { 0x45b796 },
            &[x, y, id as i32, 1],
        );
        self.raster(id, x, y, if light { 2 } else { 1 }, 0, self.clip)
    }
    pub fn filled(&mut self, x0: i32, y0: i32, x1: i32, y1: i32, color: u8) -> Result<()> {
        let (x0, y0, x1, y1) = (i16(x0), i16(y0), i16(x1), i16(y1));
        self.observe("FilledBox", 0x45cacd, &[x0, y0, x1, y1, color as i32, 1]);
        let [l, t, r, b] = self.clip;
        let (x0, y0, x1, y1) = (
            x0.max(l).max(0),
            y0.max(t).max(0),
            x1.min(r).min(799),
            y1.min(b).min(599),
        );
        if x1 < x0 || y1 < y0 {
            return Ok(());
        }
        for y in y0..=y1 {
            self.surface[y as usize * 800 + x0 as usize..y as usize * 800 + x1 as usize + 1]
                .fill(color);
        }
        Ok(())
    }
    pub fn outline(
        &mut self,
        x0: i32,
        y0: i32,
        x1: i32,
        y1: i32,
        color: u8,
        clipped: bool,
    ) -> Result<()> {
        self.observe(
            "Box",
            0x45c912,
            &[x0, y0, x1, y1, color as i32, clipped as i32],
        );
        let [l, t, r, b] = if clipped {
            self.clip
        } else {
            [
                0,
                0,
                self.u16(0x49a018)? as i32 - 1,
                self.u16(0x49a01a)? as i32 - 1,
            ]
        };
        if x0 > r || y0 > b || x1 < l || y1 < t {
            return Ok(());
        }
        let (mut x0, mut y0, mut x1, mut y1) = (x0.max(l), y0.max(t), x1.min(r), y1.min(b));
        if x1 < x0 {
            std::mem::swap(&mut x0, &mut x1);
        }
        if y1 < y0 {
            std::mem::swap(&mut y0, &mut y1);
        }
        if x0 < 0 || y0 < 0 || x1 > 799 || y1 > 599 {
            return Err(Error::Invalid("Box outside physical surface"));
        }
        for y in [y0, y1] {
            self.surface[y as usize * 800 + x0 as usize..y as usize * 800 + x1 as usize + 1]
                .fill(color);
        }
        for y in y0..=y1 {
            self.surface[y as usize * 800 + x0 as usize] = color;
            self.surface[y as usize * 800 + x1 as usize] = color;
        }
        Ok(())
    }
}
fn player(v: u8, owner: u32) -> u8 {
    if !(160..168).contains(&v) {
        return v;
    }
    let i = (v - 160) as usize;
    match owner {
        1 => [144, 145, 146, 148, 149, 150, 253, 254][i],
        2 => [136, 137, 138, 139, 140, 141, 142, 143][i],
        3 => [48, 50, 52, 54, 56, 58, 59, 61][i],
        4 => 47,
        0 => v,
        _ => unreachable!("validated player table owner"),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn opaque_zero_skips_signed_clipping_and_destination_shadow() {
        // Synthetic fixture: literal zero is opaque, the upper-right pixel is a skip.
        let assets = Assets {
            sprites: vec![Sprite {
                width: 2,
                height: 2,
                pixels: vec![0, 8, 3, 4],
                mask: vec![255, 0, 255, 255],
                raw: vec![],
            }],
            palette: [0; 768],
            shadow: std::array::from_fn(|i| 255 - i as u8),
            light: std::array::from_fn(|i| i as u8),
        };
        let m = MemoriaJogo::default();
        let mut pixels = vec![7; 480000];
        let mut cache = Cache {
            keys: vec![0; 1024],
            raw: vec![0; 270336],
            cursor: 0,
        };
        let mut background = None;
        let mut text_boundaries = None;
        let mut c = Context {
            background: &mut background,
            text_boundaries: &mut text_boundaries,
            text_checked: 0,
            tick: None,
            m: &m,
            overrides: BTreeMap::new(),
            surface: &mut pixels,
            cache: &mut cache,
            assets: &assets,
            observations: vec![],
            audit: true,
            clip: [0, 0, 799, 599],
            camera: 0,
        };
        c.raster(1, 0, 0, 0, 0, c.clip).unwrap();
        assert_eq!(&c.surface[..2], &[0, 7]);
        assert_eq!(&c.surface[800..802], &[3, 4]);
        c.raster(1, -1, 0, 1, 0, c.clip).unwrap();
        assert_eq!(c.surface[0], 0);
        assert_eq!(c.surface[800], 252);
        c.raster(1, 0, -1, 0, 0, [1, 0, 799, 599]).unwrap();
        assert_eq!(&c.surface[..2], &[0, 4]);
    }
}
