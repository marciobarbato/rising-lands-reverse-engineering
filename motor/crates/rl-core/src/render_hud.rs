//! AffGame HUD tail through the last offscreen pixel write (0x417d30).
use crate::render::{i16, Context, Result};
impl Context<'_> {
    pub fn hud(&mut self, event: bool) -> Result<()> {
        for (k, x) in [492, 540, 588].into_iter().enumerate() {
            let a = 0x4e2eac + 8 * (4 * self.camera + k as u32);
            self.counter(self.u16(a)?, self.u8(a + 2)?, x, 557)?;
        }
        self.action_icons()?;
        let mx = self.u16(0x5099a8)?;
        let my = self.u16(0x5099aa)?;
        if mx <= self.u16(0x508724)? * 32
            && my <= self.u16(0x508726)? * 32
            && self.u16(0x4e05ae)? == 3
        {
            self.placement()?;
        }
        let cell = self.u16(0x496204)?;
        if cell != 65535 {
            let mut id = self.u16(0x4e05ac)?;
            if !(0x1e03..=0x1e09).contains(&id) {
                return self.stop(
                    0x417ba2,
                    "target marker outside captured animation IDs 0x1e03..0x1e09",
                );
            }
            if self.u8(0x508f7c)? & 1 == 0 {
                id += 1;
                self.put16("alvo_animacao_u16", 0x4e05ac, id)?;
            }
            let x = (cell as i32 % 256 - self.u16(0x508720)? as i32) * 32 + 12;
            let y = (cell as i32 / 256 - self.u16(0x508722)? as i32) * 32 + 12;
            self.bob(i16(x), i16(y), id, true, Some(self.camera))?;
            if id == 0x1e0a {
                self.put16("alvo_animacao_u16", 0x4e05ac, 0x1e03)?;
                self.put16("alvo_celula_u16", 0x496204, 65535)?;
            }
        }
        if (1..=4).contains(&self.u8(0x4e2e7c + self.camera)?) {
            return self.stop(0x4667a7, "AffMarche market state 1..4");
        }
        if self.u8(0x497285)? != 0 {
            self.minimap()?;
        }
        let mut selected = self.u16(0x496ac4)?;
        if selected == 65535 {
            selected = self.u16(0x495be0 + 2 * self.camera)?;
        }
        if selected != 65535 {
            let a = 0x49a0c8 + 276 * selected;
            if selected >= 1000
                || self.u8(a + 4)? != 0
                || self.camera != 0
                || !matches!(self.u8(a + 8)?, 2 | 3)
                || self.u8(a + 5)? != 5
                || self.u16(a + 0x74)? != 0
            {
                return self.stop(
                    0x401d18,
                    "AffChrono selected structure outside no-recruitment sanctuary domain",
                );
            }
        }
        self.info_zone()?;
        if self.u32(0x4e060c)? != 0 {
            self.tooltip()?;
        }
        if self.u8(0x4e17ac)? != 0 {
            return self.stop(0x417c7f, "AffDebug enabled");
        }
        if event {
            return self.stop(0x417c8a, "EvenementAffiche event in progress");
        }
        if self.u16(0x507d56)? != self.u16(0x507d54)? {
            return self.stop(0x469c5f, "MessageBoxAffiche queue not empty");
        }
        let players = self.u32(0x5080a8)?;
        for p in 0..4 {
            if p == self.camera {
                continue;
            }
            if self.camera <= 4 && self.u8(players + 20 * self.camera + 6)? & (1 << p) != 0 {
                return self.stop(0x417604, "AffDrapeauAlliance allied player flag");
            }
            if self.u32(0x5080b0 + 16 * self.camera + 4 * p)? != 0 {
                return self.stop(0x4175f2, "AffDrapeauAlliance contacting player");
            }
        }
        self.put16("mouse_x_copia_u16", 0x49a042, mx)?;
        self.put16("mouse_y_copia_u16", 0x49a044, my)?;
        if self.u8(0x49a054)? == 0 {
            let base = self.u16(0x49a010)?;
            self.bob(
                i16(mx as i32),
                i16(my as i32),
                (base + self.u16(0x49a014)?) & 65535,
                true,
                None,
            )?;
            let second = self.u16(0x4e062c)?;
            if second != 0 {
                if second > 16 {
                    return self.stop(0x417cfc, "second cursor count outside 0..16");
                }
                self.bob(
                    i16(mx as i32),
                    i16(my as i32),
                    (base + 16 - second) & 65535,
                    true,
                    None,
                )?;
            }
        }
        Ok(())
    }
    fn counter(&mut self, value: u32, highlight: u32, mut x: i32, y: i32) -> Result<()> {
        if value > 9999 {
            return self.stop(0x417f6e, "AffCompteurMatiere counter value above 9999");
        }
        let digits = [value / 1000, value / 100 % 10, value / 10 % 10, value % 10];
        let mut leading = true;
        for (i, digit) in digits.into_iter().enumerate() {
            let bit = (highlight >> (3 - i)) & 1;
            if digit == 0 && leading && i != 3 && bit == 0 {
                if i != 0 {
                    self.bob(x, y, 0x2a21, false, None)?;
                }
                x += 12;
                continue;
            }
            if i == 0 {
                for j in 0..digit.min(4) {
                    self.bob(x + 12 + 8 * j as i32, y - 9, 0x2a3c, false, None)?;
                }
            } else {
                self.bob(x, y, 0x2a22 + 2 * digit + bit, false, None)?;
            }
            leading = false;
            x += 12;
        }
        Ok(())
    }
    fn action_icons(&mut self) -> Result<()> {
        if self.u8(0x4e05a2)? == 0 {
            return Ok(());
        }
        let selected = self.u16(0x496d4a)?;
        let left = self.u16(0x4e2440)?;
        self.bob(
            8,
            547,
            if left == 0x29b1 {
                0x29b5
            } else if selected == 8 {
                0x2a39
            } else {
                0x2a37
            },
            false,
            None,
        )?;
        for i in 0..4 {
            let a = 0x4e2410 + 6 * i;
            let x = 31 + 60 * i as i32;
            let id = self.u16(a)?;
            if id == 0x29b1 {
                self.bob(x, 547, 0x29b1 + i, false, None)?;
                continue;
            }
            self.bob(x, 547, 0x29b7, false, None)?;
            self.bob(x + 2, 549, id, false, None)?;
            match self.u16(a + 2)? {
                0 => {
                    let value = self.u16(a + 4)?;
                    if value > 100 {
                        return self.stop(0x417086, "AffZoneIconeAction percent outside 0..100");
                    }
                    let mask = 0x2a1d - value * 42 / 100;
                    self.observe("PasteNoirBlancCmp", 0x45bf3d, &[x + 2, 549, mask as i32, 0]);
                    let q = self.assets.sprite(mask)?;
                    let table = self.m.read(self.u32(0x4e24bc)?, 256)?;
                    for sy in 0..q.height.min(600 - 549) {
                        for sx in 0..q.width.min(800 - (x as usize + 2)) {
                            let src = sy * q.width + sx;
                            if q.mask[src] != 0 {
                                let p = (549 + sy) * 800 + x as usize + 2 + sx;
                                self.surface[p] = table[self.surface[p] as usize];
                            }
                        }
                    }
                }
                1 => {}
                2 => {
                    let value = self.u16(a + 4)?;
                    if value > 999 {
                        return self.stop(0x417086, "AffZoneIconeAction counter outside 0..999");
                    }
                    let mut leading = true;
                    for (j, d) in [value / 100, value / 10 % 10, value % 10]
                        .into_iter()
                        .enumerate()
                    {
                        if leading && d == 0 && j < 2 {
                            continue;
                        }
                        self.bob(x + 22 + 12 * j as i32, 582, 0x2a22 + 2 * d, false, None)?;
                        leading = false;
                    }
                }
                _ => return self.stop(0x417086, "AffZoneIconeAction slot kind outside 1.5"),
            }
            if selected == i {
                self.bob(x + 2, 549, 0x2a36, false, None)?;
            }
        }
        let right = self.u16(0x4e2446)?;
        self.bob(
            272,
            547,
            if right == 0x29b1 {
                0x29b6
            } else if selected == 9 {
                0x2a3a
            } else {
                0x2a38
            },
            false,
            None,
        )
    }
    fn minimap(&mut self) -> Result<()> {
        let mx = self.u16(0x507d68)?;
        let my = self.u16(0x507d6a)?;
        let w = self.u16(0x496fe0)?;
        let h = self.u16(0x496fe2)?;
        let cw = self.u16(0x497168)?;
        let ch = self.u16(0x49716a)?;
        if w == 0 || h == 0 || mx + 1 + w > 800 || my + 1 + h > 600 || cw == 0 || ch == 0 {
            return self.stop(0x46a70c, "AffMiniMap outside captured geometry");
        }
        self.outline(
            mx as i32,
            my as i32,
            (mx + w + 1) as i32,
            (my + h + 1) as i32,
            20,
            true,
        )?;
        let data = self.m.read(self.u32(0x507d5c)?, (w * h) as usize)?;
        for y in 0..h as usize {
            let p = (my as usize + 1 + y) * 800 + mx as usize + 1;
            self.surface[p..p + w as usize]
                .copy_from_slice(&data[y * w as usize..(y + 1) * w as usize]);
        }
        let ox = self.u16(0x508720)?;
        let oy = self.u16(0x508722)?;
        self.outline(
            (ox * w / cw + mx + 1) as i32,
            (oy * h / ch + my + 1) as i32,
            ((ox + self.u16(0x508724)?) * w / cw + mx + 1) as i32,
            ((oy + self.u16(0x508726)?) * h / ch + my + 1) as i32,
            1,
            true,
        )
    }
    fn info_zone(&mut self) -> Result<()> {
        self.bob(298, 547, 0x29b8, false, None)?;
        let value = self.u16(0x4e0618)?;
        if value != 0 {
            return self.info_row(value, 0x2a46, 548);
        }
        let value = self.u16(0x4e0612)?;
        if value != 0 {
            self.info_row(value, 0x2a43, 548)?;
        }
        let value = self.u16(0x4e0614)?;
        if value != 0 {
            self.info_row(value, 0x2a44, 574)?;
        } else {
            let value = self.u16(0x4e0616)?;
            if value != 0 {
                self.info_row(value, 0x2a42, 574)?;
            }
        }
        Ok(())
    }
    fn info_row(&mut self, value: u32, id: u32, top: i32) -> Result<()> {
        self.bob(299, top, id, false, None)?;
        self.bob(327, top + 4, 0x2a45, false, None)?;
        if value > 9999 {
            return self.stop(0x40f77b, "AffZoneInfo cost counter exceeds 9999");
        }
        let mut x = 328;
        let mut leading = true;
        for (i, d) in [value / 1000, value / 100 % 10, value / 10 % 10, value % 10]
            .into_iter()
            .enumerate()
        {
            if leading && d == 0 && i < 3 {
                if i == 2 {
                    self.bob(x, top + 5, 0x2a21, false, None)?;
                    x += 12;
                }
                continue;
            }
            self.bob(x, top + 5, 0x2a22 + 2 * d, false, None)?;
            x += 12;
            leading = false;
        }
        Ok(())
    }
}
