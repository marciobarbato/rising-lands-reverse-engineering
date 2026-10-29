"""Static AffGame render of the accepted MONDE01 M1 post-load state (non-blocking, no new graphics systems).

Input: missions' frozen captura-carga-missao-original-v2.json (final_state blocks). The existing bounded
AffGame composition (cache lifecycle, terrain/sprite/projectile passes) runs over it; every unreconstructed
pass stops visibly at its named original address and is listed in the output manifest. Pure Python.
Usage: python3 renderizar_m1_estatico.py [saida_dir]
"""
import base64, hashlib, json, struct, sys, zlib
from pathlib import Path
from graficos import RAIZ, Catalogo, png
from cenas_quadro import globais_base, fundo
from ciclo_cache_terreno import CicloCacheTerreno, MemoriaMotor
from vinculos_graficos import ArenaGlobalFixa, RegistroVinculos
from quadro_jogo import compor_quadro, EstadoTela, MundoQuadro, DependenciaQuadro
from test_quadro_jogo import DD, tabelas

CAPTURA = RAIZ.parent/'missoes/evidencias/captura-carga-missao-original-v2.json'
DGROUP = 0x494000
CELULA_SANTUARIO = 2828  # (x=12, y=11)
sha = lambda d: hashlib.sha256(bytes(d)).hexdigest()


class EstadoM1:
    def __init__(self, caminho):
        bruto = Path(caminho).read_bytes(); self.sha256 = sha(bruto)
        blocos = json.loads(bruto)['oracle']['final_state']['blocks']
        self.dados = {}
        for nome, b in blocos.items():
            d = zlib.decompress(base64.b64decode(b['zlib_base64'])); assert sha(d) == b['sha256']
            self.dados[int(b['base'], 16)] = d
        self.dgroup = self.dados[DGROUP]

    def u(self, endereco, n):
        return int.from_bytes(self.dgroup[endereco-DGROUP:endereco-DGROUP+n], 'little')

    def bloco(self, endereco_ponteiro, tamanho):
        base = self.u(endereco_ponteiro, 4); return self.dados[base][:tamanho]

    def estatico(self, endereco, n): return self.dgroup[endereco-DGROUP:endereco-DGROUP+n]


def montar(m1, camera):
    pts = lambda base: [m1.bloco(base+4*i, 65536) for i in range(4)]
    mundo = MundoQuadro(terreno=m1.bloco(0x507d70, 131072), objetos=m1.bloco(0x507d74, 65536),
        auxiliares=m1.bloco(0x507dac, 65536), regioes=m1.bloco(0x4e0f38, 131072), unidades=m1.bloco(0x4e19a0, 220800),
        projeteis=m1.bloco(0x5080f0, 5600), descoberta=pts(0x507d78), iluminacao=pts(0x507d88))
    return mundo


def main(saida):
    saida = Path(saida); saida.mkdir(parents=True, exist_ok=True)
    m1 = EstadoM1(CAPTURA); camera = m1.u(0x508041, 1)
    mundo = montar(m1, camera)
    # Window of 25x17 cells with the Sanctuary (cell 2828) centred horizontally, declared origin.
    origem = (0, 3)
    g = globais_base(camera_u8=camera, origem=struct.pack('<HH', *origem))
    tela = EstadoTela(g)
    catalogo = Catalogo(); sombra, ecl = tabelas()
    f = json.loads((RAIZ/'validacao/x86-quadro-jogo.json').read_text())['cache_alloc_fixture']
    reg = RegistroVinculos()
    mem = MemoriaMotor(contador_u32=f['counter_u32'], vinculos=ArenaGlobalFixa(inicio_u32=f['arena_next'],
        tamanho_u32=f['arena_end']-f['arena_next'], registro=reg))
    ciclo = CicloCacheTerreno.apos_carregar_banco(catalogo); ciclo.alocar(mem); ciclo.iniciar()
    parada = None; superficie = None
    try:
        q = compor_quadro(mundo, tela, ciclo_cache=ciclo, catalogo=catalogo, tabela_sombra=sombra, tabela_eclairage=ecl,
            superficie=fundo(), relogio=lambda: 1500, directdraw=DD())
        superficie, chamadas = q['superficie'], q['chamadas']
    except DependenciaQuadro as e:
        parada = dict(endereco=f'0x{e.endereco:08x}', detalhe=e.detalhe); superficie, chamadas = e.superficie, e.chamadas
    cont = {}
    for c in chamadas: cont[c[0]] = cont.get(c[0], 0)+1
    pal = catalogo.paleta()
    rgba = b''.join(pal[p*3:p*3+3]+b'\xff' for p in superficie)
    img = saida/'monde01_m1_estatico.png'; img.write_bytes(png(800, 600, rgba))
    manifesto = dict(input=str(CAPTURA.name), input_sha256=m1.sha256, camera=camera, origem_celulas=origem,
        santuario_celula=CELULA_SANTUARIO, terreno_na_celula=struct.unpack_from('<H', mundo.terreno, CELULA_SANTUARIO*2)[0],
        regiao_na_celula=hex(mundo.palavra('regioes', CELULA_SANTUARIO)), chamadas=cont, parada=parada,
        surface_sha256=sha(superficie), png_sha256=sha(img.read_bytes()))
    (saida/'monde01_m1_estatico.json').write_text(json.dumps(manifesto, indent=1)+'\n')
    print(json.dumps(manifesto, indent=1))


if __name__ == '__main__': main(sys.argv[1] if len(sys.argv) > 1 else RAIZ.parents[1]/'.local/graficos-m1')
