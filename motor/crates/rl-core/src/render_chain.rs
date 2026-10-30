//! Graphics 1.8/1.9 layer plans, ported from committed original-first tables.
use crate::render::{i16, w, Context, Result};
impl Context<'_> {
    pub fn inhabited_cave(&mut self, r: &[u8], x: i32, y: i32, cell: u32) -> Result<()> {
        if r[4] != 0 || self.camera != 0 || r[5] != 5 || w(r, 6) != 0 {
            return self.stop(
                0x40958e,
                "inhabited CAVE outside owner0 mode5 no-fire domain",
            );
        }
        let level = self.u8(0x4dfb30 + 6 * r[4] as u32)?;
        if level != 0 || r[0x74] > 1 || r[0x75] > 1 || r[0x76] > 15 {
            return self.stop(0x40958e, "CAVE flags/player level outside native matrix");
        }
        let (x, y) = (i16(x - 57), i16(y - 47));
        let clock = self.u32(0x508f80)?;
        let phase = (clock.wrapping_add(cell)) & 7;
        self.bob(x, y, 7094, true, Some(r[4] as u32))?;
        for (id, dx, dy) in [
            (7095 + phase, 3, 10),
            (7103 + phase, 43, 0),
            (7111 + phase, 60, 23),
            (7127 + if r[0x74] != 0 { phase } else { 0 }, 12, 46),
            (7135 + level, 21, 16),
            (
                if r[0x76] < 8 { 7119 } else { 7137 } + r[0x76] as u32,
                64,
                if r[0x76] < 8 { 41 } else { 38 },
            ),
        ] {
            self.bob(i16(x + dx), i16(y + dy), id, true, None)?;
        }
        if r[0x76] == 15 && r[0x75] != 0 {
            self.bob(i16(x + 64), i16(y + 38), 7151 + phase, true, None)?;
        }
        Ok(())
    }
    pub fn work_body(&mut self, r: &[u8], x: i32, y: i32, index: u32, overlay: bool) -> Result<()> {
        let (kind, task) = (r[1], r[0x89]);
        if r[0] != 0
            || self.camera != 0
            || r[0xdc] != 0
            || r[0x99] != 0
            || r[0xa5] != 8
            || r[0xa4] >= 8
            || !(1..=16).contains(&r[0x91])
        {
            return self.stop(
                0x414a8a,
                "worker outside captured owner/count/effect bounds",
            );
        }
        if kind == 7 && matches!(task, 1 | 2) {
            return Ok(());
        }
        let (base, stride, anchor) = if kind == 5 {
            match task {
                0 | 2 | 3 => (if w(r, 10) == 0 { 1594 } else { 1690 }, 8, 11),
                1 => (1662, 4, 11),
                _ => return self.stop(0x414a8a, "uncaptured farmer work task"),
            }
        } else if kind == 7 && task == 0 {
            (if w(r, 10) == 0 { 1338 } else { 1466 }, 8, 26)
        } else {
            return self.stop(0x414a8a, "uncaptured builder work task");
        };
        self.order_markers(r)?;
        let (px, py) = (x + r[0x86] as i8 as i32, y + r[0x87] as i8 as i32);
        self.shadow(i16(px + 2), i16(py + 26), 10784, false)?;
        self.bob(
            i16(px - anchor),
            i16(py - anchor),
            base + (r[0x91] as u32).div_ceil(2) * stride + r[0xa4] as u32,
            true,
            None,
        )?;
        self.unit_tail(r, x, y, index, overlay)
    }
}
impl Context<'_> {
    pub fn structure_overlay18(
        &mut self,
        r: &[u8],
        cell: u32,
        frame: bool,
        gauge: bool,
    ) -> Result<()> {
        if !matches!(r[8], 2 | 3) || r[5] != 5 || r[4] != 0 || self.camera != 0 {
            return self.stop(
                if frame { 0x4022c8 } else { 0x4020ec },
                "structure selection outside API1.8 domain",
            );
        }
        let cave = r[8] == 3;
        let (ax, ay, right, height, gy, max, cap) = if cave {
            (57, 47, 83, 97, 34, 100, 2)
        } else {
            (150, 93, 175, 153, 90, 600, 16)
        };
        let ox = self.u16(0x508720)?;
        let oy = self.u16(0x508722)?;
        let (x, y) = (
            (cell as i32 % 256 - ox as i32) * 32 - ax,
            (cell as i32 / 256 - oy as i32) * 32 - ay,
        );
        if frame {
            let phase = (self.u32(0x508f80)? & 7) as i32;
            for (id, px, py) in [
                (0x2a79, x + phase - 20, y + phase),
                (0x2a78, x + phase - 20, y + height - phase),
                (0x2a7a, x + right - phase, y + phase),
                (0x2a77, x + right - phase, y + height - phase),
            ] {
                self.bob(i16(px), i16(py), id, true, Some(r[4] as u32))?;
            }
        }
        if !gauge {
            return Ok(());
        }
        let count = w(r, 12) as usize;
        if self.u16(0x495d90 + 52 * r[8] as u32)? != max
            || w(r, 10) != max
            || w(r, 6) != 0
            || w(r, 14) != cap
            || !(if cave {
                count == 1
            } else {
                count == 7 || count == 8
            })
        {
            return self.stop(0x4020ec, "structure gauge outside API1.8 matrix");
        }
        if r[0x4e..0x4e + count].iter().any(|b| *b != 1)
            || r[0x4e + count..0x4e + cap as usize].iter().any(|b| *b != 0)
        {
            return self.stop(0x401a70, "structure bag outside compact troop slots");
        }
        let mut gx = i16(x - 23);
        let gy = i16(y + gy);
        if ox == 0 && gx < 0 {
            gx = 0;
        }
        self.bob(i16(gx + 9), gy, 0x2a7b, true, None)?;
        self.filled(gx + 10, gy + 1, gx + 14, gy + 60, 48)?;
        for i in 0..cap as usize {
            let code = r[0x4e + i];
            self.bob(
                i16(gx - if i >= 8 { 9 } else { 0 }),
                i16(gy + 8 * (i as i32 % 8)),
                if code == 1 { 0x2a3c } else { 0x2a3b },
                true,
                if code == 1 { Some(r[4] as u32) } else { None },
            )?;
        }
        if cave {
            if self.u8(0x4dfb30 + 6 * r[4] as u32)? != 0 {
                return self.stop(0x401a70, "CAVE markers above level zero");
            }
            for i in 0..7 {
                self.bob(i16(gx + 63 + 8 * i), i16(gy + 48), 0x2a3b, true, None)?;
            }
        }
        Ok(())
    }
}
