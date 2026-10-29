"""ProjectileAvance/ProjectileCalcul, com efeitos do mundo em callbacks.

Completa o despacho dos 256 bytes de tipo. Não calcula dano, desenha, move
unidades nem implementa um relógio em segundos. Random e consultas de magia
continuam externos; o byte global escrito pelo tipo 30 fica no contexto local.
"""
from dataclasses import dataclass

from projeteis import u16, por16
from avanco_projeteis import (TIPOS_LINEARES, animar_projetil, infligir_dano_projetil,
    _aleatorio, _efeito_chegada, _chegada, _passo_linear)


@dataclass
class MaquinaProjeteis:
    pool: object
    aleatorio: object = None
    tempo_magia: object = None
    campo_4dfb44: int = 0

    def _chegada(self, pool, indice, aleatorio):
        if pool.registro(indice)[0] == 30:
            self._area_tipo30(indice)
        else:
            _chegada(pool, indice, aleatorio)

    def _area_tipo30(self, indice):
        """0x46f088: raio 7, ordem por linha; nenhum dano central separado."""
        p = self.pool.registro(indice)
        self.campo_4dfb44 = 15
        alvo = u16(p, 0x16)
        cx, cy = alvo & 255, alvo >> 8
        for y in range(max(0, cy - 7), min(256, cy + 8)):
            for x in range(max(0, cx - 7), min(256, cx + 8)):
                if (x - cx) ** 2 + (y - cy) ** 2 > 49:
                    continue
                celula = x + y * 256
                self.pool._efeito('InfligeDegat', celula, 4, u16(p, 0x20), p[0], 0)
                filho = 6 + _aleatorio(self.aleatorio, 0x2f) % 3
                _efeito_chegada(self.pool, p, celula, filho)
        p[2] = 0

    def _tipo33(self, indice):
        p = self.pool.registro(indice)
        if p[0x18] != 20:
            return
        alvo = u16(p, 0x16)  # DI é salvo antes da primeira consulta Random
        if not (_aleatorio(self.aleatorio, 0x29) & 1):
            x, y = alvo & 255, alvo >> 8
            largura = 3 - int(x in (0, 255))
            altura = 3 - int(y in (0, 255))
            yy = max(0, y - 1) + _aleatorio(self.aleatorio, 0x2a) % altura
            xx = max(0, x - 1) + _aleatorio(self.aleatorio, 0x2b) % largura
            alvo = xx + yy * 256
        filho = 6 + _aleatorio(self.aleatorio, 0x2c) % 3
        # O filho recebe o destino antigo; só depois o pai ganha o alvo sorteado.
        _efeito_chegada(self.pool, p, alvo, filho)
        por16(p, 0x16, alvo)
        infligir_dano_projetil(self.pool, indice)
        p[2] = 0

    def avancar(self, indice):
        """ProjectileAvance 0x46eaf8, inclusive no-ops 0 e 35..255.

Não testa +02. Os callbacks observam as escritas anteriores, sem rollback
se faltarem. A máquina principal filtra atividade antes de chamar esta rotina.
"""
        p = self.pool.registro(indice)
        tipo, quadro = p[0], p[0x18]
        if tipo in TIPOS_LINEARES or tipo == 30:
            _passo_linear(self.pool, indice, self.aleatorio, self._chegada)
        elif tipo in (6, 7, 8, 18, 19, 34):
            if quadro == 32:
                p[2] = 0  # diferente do tipo 25: libera antes do RNG/efeito
                efeito = 56 + _aleatorio(self.aleatorio, 0x2e) % 6
                self.pool._efeito('CreerExplosion', u16(p, 0x16), efeito)
        elif tipo in (14, 15, 16, 26, 27, 31, 32):
            limite = 16 if tipo in (14, 15, 16) else 8 if tipo in (26, 27) else 32
            if quadro == limite:
                p[2] = 0
        elif tipo in (24, 25):
            if quadro == 32:
                infligir_dano_projetil(self.pool, indice)
                if tipo == 25:
                    efeito = 56 + _aleatorio(self.aleatorio, 0x2d) % 6
                    self.pool._efeito('CreerExplosion', u16(p, 0x16), efeito)
                p[2] = 0
        elif tipo == 28:
            if self.tempo_magia is None:
                raise NotImplementedError('Consulta necessária: SortilegeGetTempsFin')
            if quadro == (self.tempo_magia(0) & 65535):
                dono_bruto = p[0x20]  # antes da consulta do raio, como BL no x86
                if self.pool.raio_magia is None:
                    raise NotImplementedError('Consulta necessária: SortilegeGetRayonEffet')
                raio = self.pool.raio_magia(0) & 65535
                self.pool._efeito('EteintTerrain', u16(p, 0x16), raio, dono_bruto)
                p[2] = 0
        elif tipo == 33:
            self._tipo33(indice)

    def calcular(self, incremento_animacao):
        """ProjectileCalcul 0x46fc0f: uma animação geral e 30 passagens.

O argumento é o byte baixo do contador acumulado 0x508f7c, não um delta.
O pool é consultado ao vivo: filhos em IDs posteriores podem ser processados
na mesma passagem se Set deixar +01=0. +01 é limpo após cada varredura,
inclusive em slots inativos, mas só é escrito quando não nulo (0x46fc7f).
Isso não fixa uma duração de frame/tick.
"""
        for i in range(100):
            animar_projetil(self.pool.registro(i), incremento_animacao)
        for _ in range(30):
            for i in range(100):
                p = self.pool.registro(i)
                if p[2] and not p[1]:
                    self.avancar(i)
            for i in range(100):
                p = self.pool.registro(i)
                if p[1]:
                    p[1] = 0
