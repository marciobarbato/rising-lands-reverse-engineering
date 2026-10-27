"""Visão e minimapa usados por AvanceEngin, em grades com passo 256."""


class VisaoMovimento:
    def _visivel(self, celula, iluminada=False):
        grade = self.luz_bordas if iluminada else self.descoberto
        return (grade[self.jogador_local][celula] & 31) == 0

    def _cor_terreno(self, celula):
        if 0x1d <= self.objetos[celula] < 0x35:
            return 30
        tile = self.tiles[celula]
        return self.cores_tiles[tile] if tile < 702 else 30

    def minimapa(self, dono, celula, modo):
        mw, mh = self.tamanho_minimapa
        sx, sy = max(1, mw // self.largura), max(1, mh // self.altura)
        x, y = celula & 255, celula >> 8
        inicio = ((y * mh // self.altura) * mh + x * mw // self.largura) & 65535
        for yy in range(sy):
            for xx in range(sx):
                p = (inicio + yy * 128 + xx) & 65535
                cor = self._cor_terreno(celula)
                if modo == 1 and dono == self.jogador_local:
                    self.mini_final[p] = self.sombra[cor]
                elif modo == 2 and dono == self.jogador_local:
                    self.mini_final[p] = self.mini_unidades[p] or self.mini_estruturas[p] or cor
                elif modo == 3 and dono == self.jogador_local:
                    self.mini_final[p] = self.sombra[cor]
                elif modo == 4:
                    self.mini_unidades[p] = 30 if dono == 200 else self.cores_jogadores[dono]
                    if self._visivel(celula, True):
                        self.mini_final[p] = self.mini_unidades[p]
                elif modo == 5:
                    self.mini_unidades[p] = 0
                    if self._visivel(celula):
                        self.mini_final[p] = (self.mini_estruturas[p] or cor) if self._visivel(celula, True) else self.sombra[cor]

    def _bordas(self, grade, celula, apagar):
        x, y = celula & 255, celula >> 8
        lados = [(celula if x == 0 else celula - 1, 8 if x == 0 else 2),
                 (celula if y == 0 else celula - 256, 4 if y == 0 else 1),
                 (celula if x == self.largura - 1 else celula + 1, 2 if x == self.largura - 1 else 8),
                 (celula if y == self.altura - 1 else celula + 256, 1 if y == self.altura - 1 else 4)]
        for p, bit in lados:
            grade[p] = grade[p] & (255 ^ bit) if apagar else grade[p] | bit

    def descobrir_celula(self, celula, dono):
        grade = self.descoberto[dono]
        self._bordas(grade, celula, True)
        if grade[celula]:
            self.minimapa(dono, celula, 1)
        grade[celula] &= 0xef

    def iluminar_celula(self, celula, dono):
        contagens = self.contagem_luz[dono]
        if contagens[celula] == 0:
            self._bordas(self.luz_bordas[dono], celula, True)
            self.luz_bordas[dono][celula] &= 0xef
            self.minimapa(dono, celula, 2)
        if contagens[celula] != 255:
            contagens[celula] += 1

    def apagar_celula(self, celula, dono):
        contagens = self.contagem_luz[dono]
        if contagens[celula] == 1:
            self._bordas(self.luz_bordas[dono], celula, False)
            self.luz_bordas[dono][celula] |= 16
            self.minimapa(dono, celula, 3)
        if contagens[celula]:
            contagens[celula] -= 1

    def circulo(self, centro, raio):
        x, y = centro & 255, centro >> 8
        limite = (raio * raio + int(raio > 1)) & 65535
        for dy in range(-raio, raio + 1):
            for dx in range(-raio, raio + 1):
                if 0 <= x + dx < self.largura and 0 <= y + dy < self.altura and ((dx * dx + dy * dy) & 65535) <= limite:
                    yield (y + dy) * 256 + x + dx

    def iluminar_area(self, centro, raio, dono):
        for celula in self.circulo(centro, raio):
            self.iluminar_celula(celula, dono)

    def apagar_area(self, centro, raio, dono):
        for celula in self.circulo(centro, raio):
            self.apagar_celula(celula, dono)

    def descobrir_area(self, centro, raio, dono):
        for celula in self.circulo(centro, (raio + 1) & 65535):
            self.descobrir_celula(celula, dono)
