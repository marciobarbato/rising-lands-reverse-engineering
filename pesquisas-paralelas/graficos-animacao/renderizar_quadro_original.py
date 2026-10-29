"""Python composition of one AffGame frame over a native reference fixture (M3 preparation).

Reads the fixture written by ``capturar_quadro_original_pixels`` (entry state of AffGame in the display
scenario, offscreen surface before and at the HUD checkpoint 0x417B1C), runs ``quadro_jogo.compor_quadro`` and
compares the surface with the original's.  Pure Python.  ``comparar`` reports the first stop (original address)
and the mismatching pixels, so unreconstructed passes stay visible.
"""
import base64, hashlib, json, struct, zlib
from pathlib import Path
from graficos import RAIZ, Catalogo
from ciclo_cache_terreno import CicloCacheTerreno, MemoriaMotor
from vinculos_graficos import ArenaGlobalFixa, RegistroVinculos
from quadro_jogo import compor_quadro, EstadoTela, MundoQuadro, DependenciaQuadro, GLOBAIS_QUADRO
from test_quadro_jogo import DD, tabelas

DGROUP = 0x494000
sha = lambda d: hashlib.sha256(bytes(d)).hexdigest()


class Fixture:
    def __init__(self, caminho):
        d = json.loads(Path(caminho).read_text())
        self.bruto = d
        dec = lambda e: self._ler(e)
        self.blocos = {n: dec(b) for n, b in d['blocks'].items()}
        self.estruturas = dec(d['structure_pool'])
        self.antes = dec(d['surface_before'])
        self.referencia = dec(d['surface_at_checkpoint'])
        self.dgroup = self.blocos['dgroup']

    @staticmethod
    def _ler(entrada):
        dados = zlib.decompress(base64.b64decode(entrada['zlib_base64']))
        if sha(dados) != entrada['sha256']: raise ValueError('Fixture block hash mismatch')
        return dados

    def u(self, endereco, n): return int.from_bytes(self.dgroup[endereco-DGROUP:endereco-DGROUP+n], 'little')

    def globais(self):
        return {n: self.dgroup[a-DGROUP:a-DGROUP+w] for n, a, w in GLOBAIS_QUADRO}

    def mundo(self):
        b = self.blocos
        return MundoQuadro(terreno=b['terreno'], objetos=b['objetos'], auxiliares=b['auxiliares'], regioes=b['regioes'],
            unidades=b['unidades'], projeteis=b['projeteis'], descoberta=[b[f'descoberta{i}'] for i in range(4)],
            iluminacao=[b[f'iluminacao{i}'] for i in range(4)], estruturas=self.estruturas)


def renderizar(fx, **extra):
    """(surface, stop dict or None, calls).  ``extra`` is forwarded to compor_quadro (provider hooks)."""
    tela = EstadoTela(fx.globais())
    catalogo = Catalogo(); sombra, ecl = tabelas()
    f = json.loads((RAIZ/'validacao/x86-quadro-jogo.json').read_text())['cache_alloc_fixture']
    mem = MemoriaMotor(contador_u32=f['counter_u32'], vinculos=ArenaGlobalFixa(inicio_u32=f['arena_next'],
        tamanho_u32=f['arena_end']-f['arena_next'], registro=RegistroVinculos()))
    ciclo = CicloCacheTerreno.apos_carregar_banco(catalogo); ciclo.alocar(mem); ciclo.iniciar()
    try:
        q = compor_quadro(fx.mundo(), tela, ciclo_cache=ciclo, catalogo=catalogo, tabela_sombra=sombra, tabela_eclairage=ecl,
            superficie=fx.antes, relogio=lambda: fx.u(0x4e17b4, 4) or 1500, directdraw=DD(),
            habitado=lambda i: bool(fx.bruto['habitation'][str(i)]),
            relogios_extra=(fx.u(0x508f80, 4), fx.u(0x508f84, 4)),
            selecao_estruturas=struct.unpack_from('<5H', fx.dgroup, 0x495be0-DGROUP), **extra)
        return q['superficie'], None, q['chamadas']
    except DependenciaQuadro as e:
        return e.superficie, dict(endereco=f'0x{e.endereco:08x}', detalhe=e.detalhe), e.chamadas


def comparar(fx, superficie):
    ref = fx.referencia
    dif = [i for i in range(len(ref)) if ref[i] != superficie[i]]
    caixa = None
    if dif:
        xs, ys = [i % 800 for i in dif], [i//800 for i in dif]
        caixa = (min(xs), min(ys), max(xs), max(ys))
    return dict(pixels=len(ref), diferentes=len(dif), caixa=caixa, iguais=not dif)


if __name__ == '__main__':
    import sys
    fx = Fixture(sys.argv[1])
    sup, parada, chamadas = renderizar(fx)
    print(json.dumps(dict(parada=parada, comparacao=comparar(fx, sup), chamadas=len(chamadas)), indent=1))
