//! Graphics 1.7 scripted CAVE, builder/order, placement and tooltip branches.
use crate::render::{i16, w, Context, Error, Result, SavedBackground};
impl Context<'_> {
    fn set_clip(&mut self, left: i32, top: i32, right: i32, bottom: i32) -> Result<()> {
        let mut bytes = Vec::new();
        for v in [top, bottom, left, right] {
            bytes.extend((v as u16).to_le_bytes());
        }
        self.put("recorte", 0x49a01c, &bytes)?;
        self.clip = [
            left as u16 as i32,
            top as u16 as i32,
            right as u16 as i32,
            bottom as u16 as i32,
        ];
        Ok(())
    }
    fn remap_sprite(&mut self, x: i32, y: i32, id: u32, slot: u32) -> Result<()> {
        let q = self.assets.sprite(id)?;
        let table = self.m.read(self.u32(slot)?, 256)?;
        let [l, t, r, b] = self.clip;
        for sy in 0.max(t - y)..(q.height as i32).min(b.min(599) - y + 1) {
            for sx in 0.max(l - x)..(q.width as i32).min(r.min(799) - x + 1) {
                if q.mask[sy as usize * q.width + sx as usize] != 0 {
                    let p = (y + sy) as usize * 800 + (x + sx) as usize;
                    self.surface[p] = table[self.surface[p] as usize];
                }
            }
        }
        Ok(())
    }
    pub fn construction_facade(
        &mut self,
        x: i32,
        y: i32,
        cell: u32,
        index: u32,
        r: &[u8],
    ) -> Result<()> {
        let kind = r[8];
        let mode = r[5];
        if !matches!(kind, 2 | 3) || mode > 7 {
            return self.stop(0x40f23b, "facade outside types 2/3 modes 0..7");
        }
        let tile = self.u16(self.u32(0x507d70)? + cell * 2)?;
        if tile != if kind == 2 { 0x2ed } else { 0x30d } {
            return self.stop(0x40f23b, "facade trigger/type mismatch");
        }
        if w(r, 6) != 0 {
            return self.stop(0x4085cb, "structure damage/fire (+0x06 nonzero)");
        }
        if self.inhabited(index)? {
            if kind == 3 {
                return self.inhabited_cave(r, x, y, cell);
            }
            return self.stop(
                if kind == 3 { 0x40958e } else { 0x408ac8 },
                "facade outside captured uninhabited domain",
            );
        }
        let maximum = self.u16(0x495d90 + 52 * kind as u32)?;
        if maximum != if kind == 2 { 600 } else { 100 } || w(r, 10) > maximum {
            return self.stop(0x408ac8, "construction health outside captured maximum");
        }
        let (height, scaffold, dx, dy) = if kind == 2 {
            (153, 7031, 150, 93)
        } else {
            (97, 7093, 57, 47)
        };
        let mut x = i16(x - dx);
        let mut y = i16(y - dy);
        let width = self.u16(0x508724)? as i32 * 32;
        let height_window = self.u16(0x508726)? as i32 * 32;
        let state = (200 * w(r, 10) / maximum) as i32;
        if kind == 3 && matches!(mode, 0 | 1 | 2 | 6 | 7) && state >= 100 && r[0x76] != 0 {
            return self.stop(
                0x4099a6,
                "CAVE construction variant +0x76 outside captured zero-value domain",
            );
        }
        if matches!(mode, 0 | 1 | 2 | 6 | 7) {
            if state < 100 {
                self.set_clip(
                    0.max(x),
                    0.max(i16(y + (100 - state) * height / 100)),
                    width - 1,
                    height_window - 1,
                )?;
                self.bob(x, y, scaffold, true, None)?;
                return Ok(());
            }
            let offset = (200 - state) * height / 100;
            self.set_clip(0, 0, width - 1, i16(y + offset).min(height_window - 1))?;
            self.bob(x, y, scaffold, true, None)?;
            self.set_clip(
                0.max(x),
                0.max(i16(y + offset)),
                width - 1,
                height_window - 1,
            )?;
        } else if mode == 3 {
            let bottom = i16(y + height + self.jitter()?).min(height_window - 1);
            y = 0.max(i16(y + 200 + self.jitter()? - w(r, 0x84) as i32));
            self.set_clip(0, y, width, bottom)?;
            x = i16(x + self.jitter()?);
        }
        let parts: &[(u32, i32, i32)] = if kind == 2 {
            &[
                (7032, 0, 0),
                (7049, 74, 5),
                (7033, 89, 95),
                (7041, 151, 131),
                (7057, 18, 63),
            ]
        } else {
            &[
                (7094, 0, 0),
                (7095, 3, 10),
                (7103, 43, 0),
                (7111, 60, 23),
                (7119, 64, 41),
                (7127, 12, 46),
                (7135, 21, 16),
            ]
        };
        for &(id, ox, oy) in parts {
            self.bob(i16(x + ox), i16(y + oy), id, true, None)?;
        }
        for &(id, ox, oy) in parts {
            let (xx, yy) = (
                i16(x + ox),
                i16(y + if kind == 3 && id == 7119 { 38 } else { oy }),
            );
            self.observe("PasteGrisCmp", 0x45bcb0, &[xx, yy, id as i32, 1]);
            self.remap_sprite(xx, yy, id, 0x4e24c4)?;
        }
        Ok(())
    }
    fn jitter(&mut self) -> Result<i32> {
        let cursor = self.u8(0x4e1d18)?;
        let value = self.u8(0x4e1c18 + cursor)? % 3;
        self.put("rng_u8", 0x4e1d18, &[(cursor as u8).wrapping_add(1)])?;
        Ok(value as i32)
    }
    pub fn order_markers(&mut self, r: &[u8]) -> Result<()> {
        if r[0xbd] == 0 || r[0x82] == 0 || r[2] == 17 {
            return Ok(());
        }
        if r[0x82] != 1 && !(r[0x82] == 2 && r[1] == 5) {
            return self.stop(
                0x412923,
                "selected order marker outside captured cell-target mode 1",
            );
        }
        let ox = self.u16(0x508720)?;
        let oy = self.u16(0x508722)?;
        let width = self.u16(0x508724)?;
        let height = self.u16(0x508726)?;
        let phase = (self.u32(0x508f7c)? / 5) & 1;
        let mut second = w(r, 0x80);
        if r[0x82] == 2 {
            let depot = self.read(0x49a0c8 + 276 * second, 276)?;
            if depot[8] != 3 {
                return self.stop(0x412637, "depot marker structure type is not captured");
            }
            second = (w(&depot, 2) + 1) & 65535;
        }
        for (cell, base) in [(w(r, 0xb2), 0x1e43), (second, 0x1e45)] {
            let (cx, cy) = (cell % 256, cell / 256);
            if cx >= ox && cx < ox + width && cy >= oy && cy < oy + height {
                self.bob(
                    (cx - ox) as i32 * 32,
                    (cy - oy) as i32 * 32,
                    base + phase,
                    true,
                    None,
                )?;
            }
        }
        Ok(())
    }
    pub fn construction_builder(&mut self, r: &[u8], x: i32, y: i32, index: u32) -> Result<()> {
        if r[0] != 0
            || self.camera != 0
            || r[1] != 7
            || !matches!(r[2], 11 | 15)
            || r[0x89] > 1
            || r[0xbe] == 9
            || r[0xdc] != 0
            || r[0x99] != 0
            || r[0xa5] != 8
            || r[0xa4] >= 8
            || !(1..=16).contains(&r[0x91])
        {
            return self.stop(
                0x414495,
                "builder construction body outside captured owner-0 task 0/1 domain",
            );
        }
        let (px, py) = (x + r[0x86] as i8 as i32, y + r[0x87] as i8 as i32);
        let base = if r[0x89] != 0 {
            0x57a
        } else if w(r, 10) == 0 {
            0x53a
        } else {
            0x5ba
        };
        let id = base + (r[0x91] as u32).div_ceil(2) * 8 + r[0xa4] as u32;
        self.shadow(i16(px + 2), i16(py + 26), 10784, false)?;
        self.bob(i16(px - 26), i16(py - 26), id, true, None)?;
        self.unit_tail(r, x, y, index, true)
    }
    pub fn restore_background(&mut self) -> Result<()> {
        let x = i16(self.u16(0x49a046)? as i32);
        let y = i16(self.u16(0x49a048)? as i32);
        let width = self.u16(0x49a04a)? as usize;
        let height = self.u16(0x49a04c)? as usize;
        let ptr = self.u32(0x49a03c)?;
        if width * height > 480000 {
            return self.stop(
                0x4179e1,
                "saved-background geometry outside captured screen domain",
            );
        }
        let data = self.read(ptr, width * height)?;
        self.observe(
            "PasteBob",
            0x45adf3,
            &[x, y, width as i32, height as i32, ptr as i32],
        );
        for row in 0..height {
            let yy = y + row as i32;
            if !(0..600).contains(&yy) {
                continue;
            }
            let left = 0.max(x);
            let right = 800.min(x + width as i32);
            if right > left {
                let source = row * width + (left - x) as usize;
                let dest = yy as usize * 800 + left as usize;
                self.surface[dest..dest + (right - left) as usize]
                    .copy_from_slice(&data[source..source + (right - left) as usize]);
            }
        }
        self.put("restaurar_fundo_u8", 0x49a041, &[0])?;
        self.put("forcar_desenho_u8", 0x4e05a2, &[1])?;
        let old = self.u8(0x49a040)?;
        if old != 0 {
            self.put("fond_u8", 0x49a040, &[0])?;
        }
        Ok(())
    }
    pub fn placement(&mut self) -> Result<()> {
        let kind = self.u8(0x496207)?;
        if kind != 3 {
            return self.stop(0x41729b, "placement outside captured type-3 CAVE");
        }
        let width = self.u16(0x495d8c + 52 * kind)? as i32;
        let height = self.u16(0x495d8e + 52 * kind)? as i32;
        if (width, height) != (5, 5) {
            return self.stop(0x41729b, "placement outside captured type-3 5 x 5 CAVE");
        }
        let x = (self.u16(0x5099a8)? as i32 / 32 - width / 2) * 32;
        let y = (self.u16(0x5099aa)? as i32 / 32 - height / 2) * 32;
        self.outline(x, y, x + width * 32, y + height * 32, 31, true)?;
        self.shaded_box(x, y, x + width * 32, y + height * 32, false, true)?;
        for row in 0..height {
            for col in 0..width {
                if self.u8(0x4e05b9 + (row * width + col) as u32)? == 0 {
                    self.outline(
                        x + col * 32,
                        y + row * 32,
                        x + (col + 1) * 32,
                        y + (row + 1) * 32,
                        148,
                        true,
                    )?;
                }
            }
        }
        Ok(())
    }
    fn shaded_box(
        &mut self,
        x0: i32,
        y0: i32,
        x1: i32,
        y1: i32,
        shadow: bool,
        clipped: bool,
    ) -> Result<()> {
        self.observe(
            if shadow {
                "FilledBoxOmbre"
            } else {
                "FilledBoxGris"
            },
            if shadow { 0x45cc35 } else { 0x45cd91 },
            &[x0, y0, x1, y1, clipped as i32],
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
        let (x0, y0, x1, y1) = (
            x0.max(l).max(0),
            y0.max(t).max(0),
            x1.min(r).min(799),
            y1.min(b).min(599),
        );
        let table = self
            .m
            .read(self.u32(if shadow { 0x4e24b4 } else { 0x4e24c4 })?, 256)?;
        if x1 < x0 || y1 < y0 {
            return Ok(());
        }
        for y in y0..=y1 {
            for x in x0..=x1 {
                let p = y as usize * 800 + x as usize;
                self.surface[p] = table[self.surface[p] as usize];
            }
        }
        Ok(())
    }
    pub fn tooltip(&mut self) -> Result<()> {
        let ptr = self.u32(0x4e060c)?;
        if ptr == 0 {
            return Ok(());
        }
        if !(0x494000..0x523000).contains(&ptr) {
            return self.stop(0x40f8c0, "tooltip pointer outside captured DGROUP strings");
        }
        if self.u16(0x4e0610)? < self.u16(0x49620a)? {
            return Ok(());
        }
        let mx = self.u16(0x5099a8)?;
        let my = self.u16(0x5099aa)?;
        if mx > 800 || my > 600 {
            return self.stop(
                0x40f8c0,
                "tooltip mouse outside captured screen coordinates",
            );
        }
        let mut text = Vec::new();
        for i in 0..128 {
            let b = self.u8(ptr + i)? as u8;
            if b == 0 {
                break;
            }
            text.push(b);
        }
        if text.len() == 128 {
            return self.stop(0x40f8c0, "tooltip string exceeds captured bounded length");
        }
        if (text != b"CONSTRUTOR"
            && text != b"ARMAZ\xc9M"
            && text != b"SANTU\xc1RIO"
            && text != b"FAZENDEIRO")
            || self.u16(0x49620c)? != 65535
            || self.u32(0x4e1d94)? != 0
            || self.u32(0x4e1d98)? != 0
        {
            return self.stop(
                0x40f8c0,
                "tooltip outside captured builder/CAVE strings and single-byte font mode",
            );
        }
        self.put("restaurar_fundo_u8", 0x49a041, &[1])?;
        let mut width = 2;
        for b in &text {
            width += self.assets.sprite(0x23d5 + *b as u32 - 32)?.width as i32;
        }
        let mut height = self.assets.sprite(0x23d5 + 0x6a - 32)?.height as i32;
        let mut x = 0.max(mx as i32 + 24);
        let mut y = 0.max(
            my as i32
                + if my >= self.u16(0x508726)? * 32 {
                    120
                } else {
                    0
                }
                + 16,
        );
        if y + height + 6 > 592 {
            y = 591 - height - 6;
        }
        if x + width + 6 > 800 {
            x = 800 - width - 6;
        }
        width += 6 - i32::from(width % 2 == 0);
        height += 6;
        let old_width = self.u16(0x49a018)?;
        let old_height = self.u16(0x49a01a)?;
        self.put16("largura_tela_u16", 0x49a018, 800)?;
        self.put16("altura_tela_u16", 0x49a01a, 600)?;
        for (name, a, value) in [
            ("tooltip_x", 0x49a046, x),
            ("tooltip_y", 0x49a048, y),
            ("tooltip_w", 0x49a04a, width),
            ("tooltip_h", 0x49a04c, height),
        ] {
            self.put16(name, a, value as u32)?;
        }
        if x < 0 || y < 0 || width < 0 || height < 0 || x + width > 800 || y + height > 600 {
            return self.stop(0x40f8c0, "tooltip save outside captured screen domain");
        }
        let mut saved = Vec::with_capacity((width * height) as usize);
        for row in 0..height {
            let p = (y + row) as usize * 800 + x as usize;
            saved.extend_from_slice(&self.surface[p..p + width as usize]);
        }
        let address = self.u32(0x49a03c)?;
        self.observe("GetBob", 0x45aec2, &[x, y, width, height, address as i32]);
        self.observe("saved_background_pixels", address, &[]);
        if self.audit {
            let event = self.observations.last_mut().unwrap();
            event.kind = 3;
            event.count = saved.len() as u32;
        }
        *self.background = Some(SavedBackground {
            address,
            pixels: saved,
        });
        self.outline(x, y, x + width - 1, y + height - 1, 1, false)?;
        self.shaded_box(x + 1, y + 1, x + width - 2, y + height - 2, true, false)?;
        let rectangle = [x + 3, y + 1, x + width - 2, y + height - 2];
        self.observe(
            "AffText",
            0x459454,
            &[
                rectangle[0],
                rectangle[1],
                rectangle[2],
                rectangle[3],
                1,
                0,
                0,
                text.len() as i32,
            ],
        );
        if self.audit {
            let event = self.observations.last_mut().unwrap();
            event.kind = 4;
            let n = text.len().min(8);
            event.before[..n].copy_from_slice(&text[..n]);
            if text.len() > 8 {
                event.after[..text.len() - 8].copy_from_slice(&text[8..]);
            }
        }
        if let Some(boundaries) = self.text_boundaries.as_mut() {
            let expected = boundaries
                .pop_front()
                .ok_or(Error::Invalid("Unrecorded AffText probe boundary"))?;
            if expected.text != text
                || expected.rectangle != rectangle
                || expected.font != 1
                || expected.flags != [0, 0]
                || expected.surface_sha256 != crate::render_assets::sha256(self.surface)
            {
                return Err(Error::Invalid(
                    "AffText probe request/pre-text surface mismatch",
                ));
            }
            self.text_checked += 1;
        } else {
            return self.stop(
                0x459454,
                "AffText glyph renderer is not supplied; published probes declare non-execution",
            );
        }
        self.put16("largura_tela_u16", 0x49a018, old_width)?;
        self.put16("altura_tela_u16", 0x49a01a, old_height)?;
        Ok(())
    }
}
