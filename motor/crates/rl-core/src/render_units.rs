//! Normal bodies and Graphics 1.7 input overlays; unsupported branches stop.
use crate::render::{i16, w, Context, Result};
impl Context<'_> {
    pub fn unit(&mut self, x: i32, y: i32, index: u32, r: &[u8]) -> Result<()> {
        let kind = r[1];
        let state = r[2];
        let base_type = matches!(kind, 0 | 5 | 6 | 7 | 9);
        if kind == 9 && state == 13 && (r[0x99] != 0 || r[0xdc] != 0 || r[0xa5] != 8) {
            return self.stop(
                0x41591f,
                "normal state extension outside captured count/effects",
            );
        }
        let route = match state {
            1 | 22 | 24 => {
                if r[0x8a] == 0 {
                    1
                } else if r[0x8a] <= if state == 22 { 1 } else { 3 } {
                    2
                } else {
                    0
                }
            }
            2 | 3 | 6 | 7 | 8 | 9 | 13 | 16 | 17 | 18 | 19 | 20 | 21 | 23 | 30 => 1,
            4 | 5 | 11 | 15 => 2,
            _ => 0,
        };
        if base_type && route == 0 {
            return Ok(());
        }
        if kind == 7 && state == 5 && matches!(r[0x89], 1 | 2) {
            return self.work_body(r, x, y, index, false);
        }
        let overlay =
            r[0xba] != 0 || r[0xbd] != 0 || self.u16(0x496ac2)? == index || self.u8(0x508f8f)? != 0;
        let dx = r[0x86] as i8 as i32;
        let dy = r[0x87] as i8 as i32;
        let (px, py) = (x + dx, y + dy);
        if overlay {
            if !matches!(kind, 0 | 1 | 5 | 7 | 8 | 9)
                || r[0] != 0
                || self.camera != 0
                || !(matches!(state, 2 | 7)
                    || kind == 7 && matches!(state, 5 | 11 | 15)
                    || kind == 5 && state == 5
                    || kind == 9 && state == 13)
                || r[0x99] != 0
                || r[0xdc] != 0
            {
                return self.stop(
                    0x41591f,
                    "input overlay outside captured owner-0 normal field-unit domain",
                );
            }
            if r[0xa5] != if kind == 8 { 10 } else { 8 } {
                return self.stop(
                    0x41591f,
                    "input-overlay body count differs from initialized count",
                );
            }
            if (w(r, 4) != 4 || w(r, 0x76) != 4)
                && !(matches!(kind, 5 | 7) && w(r, 4) == 3 && w(r, 0x76) == 4)
            {
                return self.stop(0x410be4, "fatigue words outside captured +4 = +0x76 = 4");
            }
            if r[0xbd] != 0 && r[0x82] > 1 && !(kind == 5 && r[0x82] == 2) {
                return self.stop(
                    0x412923,
                    "selected unit order marker outside captured cell-target mode 1",
                );
            }
            if r[0xaf] >> 5 != 0 && kind != 7 {
                return self.stop(
                    0x413696,
                    "experience icon for a non-builder is not captured",
                );
            }
            if r[0xbd] != 0 && r[0] as u32 == self.camera {
                self.bob(i16(px), i16(py), 0x2a1e, true, None)?;
            }
            if matches!(state, 2 | 7) {
                self.order_markers(r)?;
            }
        }
        if matches!(kind, 5 | 7) && state == 5 {
            return self.work_body(r, x, y, index, overlay);
        }
        if kind == 7 && matches!(state, 11 | 15) {
            return self.construction_builder(r, x, y, index);
        }
        if matches!(kind, 1 | 8) {
            let count = if kind == 1 { 8 } else { 10 };
            if r[0] != 0
                || self.camera != 0
                || !matches!(state, 2 | 7)
                || r[0x99] != 0
                || r[0xdc] != 0
                || r[0xa5] != count
                || !(1..=16).contains(&r[0x91])
                || r[0xa4] >= count
            {
                return self.stop(
                    0x41591f,
                    format!(
                        "AffEngin unit {index} type {kind} outside captured type-1/8 body domain"
                    ),
                );
            }
            let (base, ax, ay) = if kind == 1 {
                (2290, 23, 9)
            } else {
                (2450, 32, 30)
            };
            let id = base + ((r[0x91] as u32).div_ceil(2) - 1) * count as u32 + r[0xa4] as u32;
            self.shadow(i16(px + 2), i16(py + 26), 10784, false)?;
            self.bob(i16(px - ax), i16(py - ay), id, true, None)?;
        } else {
            if !base_type {
                return self.stop(
                    0x41591f,
                    format!("AffEngin unit {index} type {kind} has no committed body"),
                );
            }
            if route != 1
                || !(matches!(state, 2 | 7) || kind == 9 && state == 13)
                || r[0] != 0
                || self.camera != 0
                || !(1..=16).contains(&r[0x91])
                || r[0xa4] > 7
            {
                return self.stop(0x41591f,format!("AffEngin unit {index} type {kind} state {state} outside validated body domain"));
            }
            let bag = w(r, 10) != 0;
            let (base, ax, ay) = match kind {
                0 => (2082, 40, 22),
                5 => (if bag { 1698 } else { 1602 }, 11, 11),
                6 => (if bag { 3042 } else { 2978 }, 16, 20),
                7 => (if bag { 1474 } else { 1346 }, 26, 26),
                9 => (1826, 19, 14),
                _ => unreachable!(),
            };
            self.shadow(px + 2, py + 26, 10784, false)?;
            self.bob(
                px - ax,
                py - ay,
                base + ((r[0x91] as u32 - 1) / 2) * 8 + r[0xa4] as u32,
                true,
                None,
            )?;
        }
        self.unit_tail(r, x, y, index, overlay)
    }
    pub(crate) fn unit_tail(
        &mut self,
        r: &[u8],
        x: i32,
        y: i32,
        index: u32,
        overlay: bool,
    ) -> Result<()> {
        let dx = r[0x86] as i8 as i32;
        let dy = r[0x87] as i8 as i32;
        let (px, py) = (x + dx, y + dy);
        let kind = r[1];
        let info = overlay
            && ((r[0] as u32 == self.camera && r[0xbd] != 0)
                || self.u16(0x496ac2)? == index
                || self.u8(0x508f8f)? != 0);
        if info {
            self.unit_info(r, px, py - 9)?;
        } else {
            let life = w(r, 0x74);
            let tired = w(r, 4) == w(r, 0x76) && life < 100;
            if tired && (life / 5).is_multiple_of(2) && (kind <= 10 || kind == 25) {
                if (dx != 0 || dy != 0) && !(kind == 9 && matches!(r[2], 2 | 7 | 13)) {
                    return self.stop(
                        0x4135fa,
                        "tired icon with nonzero body shift: origin not verified",
                    );
                }
                let owner = if r[0] == 200 {
                    None
                } else if r[0] < 5 {
                    Some(r[0] as u32)
                } else {
                    return self.stop(0x413650, "owner has no player table");
                };
                self.bob(px - 8, py - 11, w(r, 4) + 0x1e2b, true, owner)?;
            }
            if overlay {
                self.experience(r, px, py - 9, false)?;
            }
        }
        Ok(())
    }
    fn experience(&mut self, r: &[u8], x: i32, y: i32, info: bool) -> Result<()> {
        let level = r[0xaf] >> 5;
        if level != 0 && (info || r[0xba] != 0) && (r[0xba] == 0 || self.u32(0x508f7c)? % 5 == 0) {
            self.bob(i16(x - 8), i16(y - 2), 0x1e46 + level as u32, true, None)?;
        }
        Ok(())
    }
    fn unit_info(&mut self, r: &[u8], x: i32, y: i32) -> Result<()> {
        if r[0] as u32 != self.camera {
            return Ok(());
        }
        let maximum = self.u16(0x4965b6 + 50 * r[1] as u32)?;
        let hp = w(r, 0x9a);
        if maximum != 100 || hp > maximum {
            return self.stop(0x410be4, "unit health outside captured 0..100 / max 100");
        }
        if w(r, 12) > 1 {
            return self.stop(
                0x410a2c,
                "AffContenanceEngin bag capacity outside captured 0/1",
            );
        }
        let percent = hp;
        let height = (15 * percent / 100) as i32;
        self.filled(x - 11, y, x - 8, y + 15, 2)?;
        self.filled(
            x - 11,
            y + 15 - height,
            x - 9,
            y + 14,
            if percent > 75 {
                48
            } else if percent > 35 {
                180
            } else {
                145
            },
        )?;
        let life = w(r, 0x74);
        if !(w(r, 4) == w(r, 0x76) && life < 100) || (life / 5).is_multiple_of(2) {
            self.bob(
                i16(x - 8),
                i16(y - 2),
                0x1e2b + w(r, 4),
                true,
                Some(r[0] as u32),
            )?;
        }
        self.experience(r, x, y, true)
    }
    pub fn structure_overlay(
        &mut self,
        r: &[u8],
        cell: u32,
        frame: bool,
        gauge: bool,
    ) -> Result<()> {
        if r[8] == 3 || r[8] == 2 && w(r, 12) == 7 {
            return self.structure_overlay18(r, cell, frame, gauge);
        }
        if r[8] != 2 || r[5] != 5 || r[4] != 0 || self.camera != 0 {
            return self.stop(
                if frame { 0x4022c8 } else { 0x4020ec },
                "selection overlay outside captured inhabited owner-0 mode-5 sanctuary",
            );
        }
        let ox = self.u16(0x508720)?;
        let oy = self.u16(0x508722)?;
        let x = (cell as i32 % 256 - ox as i32) * 32 - 150;
        let y = (cell as i32 / 256 - oy as i32) * 32 - 93;
        if frame {
            let phase = (self.u32(0x508f80)? & 7) as i32;
            for (id, px, py) in [
                (0x2a79, x + phase - 20, y + phase),
                (0x2a78, x + phase - 20, y + 153 - phase),
                (0x2a7a, x + 175 - phase, y + phase),
                (0x2a77, x + 175 - phase, y + 153 - phase),
            ] {
                self.bob(i16(px), i16(py), id, true, Some(r[4] as u32))?;
            }
        }
        if !gauge {
            return Ok(());
        }
        let denominator = self.u16(0x495d90 + 104)?;
        let hp = w(r, 10);
        let damage = w(r, 6);
        if denominator != 600 || damage > hp || hp > 600 {
            return self.stop(0x4020ec, "sanctuary health/malus outside captured 0..600");
        }
        if w(r, 14) != 16 || w(r, 12) != 8 || r[0x4e..0x56] != [1; 8] || r[0x56..0x5e] != [0; 8] {
            return self.stop(
                0x401a70,
                "sanctuary contents outside captured 16-slot / 8-unit bag",
            );
        }
        let mut gx = i16(x - 23);
        let gy = i16(y + 90);
        if ox == 0 && gx < 0 {
            gx = 0;
        }
        self.bob(i16(gx + 9), gy, 0x2a7b, true, None)?;
        let height = ((hp * 200 / denominator - damage * 200 / denominator) * 60 / 200) as i32;
        self.filled(
            gx + 10,
            gy + 61 - height,
            gx + 14,
            gy + 60,
            if height <= 20 {
                145
            } else if height <= 40 {
                180
            } else {
                48
            },
        )?;
        for i in 0..16 {
            let code = r[0x4e + i];
            self.bob(
                i16(gx - if i >= 8 { 9 } else { 0 }),
                i16(gy + 8 * (i as i32 % 8)),
                if code == 1 { 0x2a3c } else { 0x2a3b },
                true,
                if code == 1 { Some(r[4] as u32) } else { None },
            )?;
        }
        Ok(())
    }
}
