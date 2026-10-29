"""Original-only isolated captures of Economy's periodic branches (M2.3 prep), counters forced.

Two inputs, each NOT a frame input (the counter and every override below are declared):
- ``exibicao_s0``: the display post-load state (``capturar_campos_exibicao_original.blocos_exibicao``);
- ``quadro128``: the full-state checkpoint after frame 128 of the Mac mini's M2.2 capture
  (Missions ``ad50ab2:pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.json.xz``,
  raw JSON sha256 pinned), checked against that phase's state summary.

Routines, run whole over the intact code section from their entries:
- CalculCompteurMarche 0x466dd1 / CalculCompteurProposition 0x466e9b (AL = local player, as CalculGame):
  counter mod u16 0x496f90 / 0x496f92 (100) and 800. The market state-3/4/5 branches now run natively.
- PlayerAttaqueCalculSympa 0x46d629 (mod 2000) and MAJSympathie 0x475118 directly, AI context bytes cleared
  so the event-counter branch 0x47515d runs.
- PlayerInitAllianceCompteur 0x46da3b over declared counters 0x5080b0.
- BatimentNextEtape 0x4268d4 (AX = structure) for every live structure (state byte +5 != 0), counters around
  the 50-frame gate [0x495bfc] and the per-structure (counter + index) & 0x1f gates.
- GetMeteo 0x4290cf: counter mod 900 (weather 0x496d2c) and the 100-frame Random(5) roll (0x496d2e).
Execution stops only at UI/graphics callees owned elsewhere (``PARADAS``); stops record the registers.

    python3 -B pesquisas-paralelas/economia/capturar_temporizadores_original.py \
        --quadros128 .local/m2-3/captura-quadros128-monde01-exibicao-v2.json.xz \
        --output pesquisas-paralelas/economia/evidencias/captura-temporizadores-original.json
"""
import argparse
import base64
import datetime
import hashlib
import json
import lzma
from pathlib import Path
import struct
import subprocess
import sys
import zlib

import capturar_campos_exibicao_original as campos
import capturar_quadro_m2_original as base

RAIZ = base.RAIZ
SHA_QUADROS128 = '1ad031b96300e5c632fd5b6b7857ae30792f78e86531e4f17d1bf7124c6dd930'
ORIGEM_QUADROS128 = ('ad50ab2', 'pesquisas-paralelas/missoes/evidencias/captura-quadros128-monde01-exibicao-v2.json.xz')
MARCHE, PROPOSITION, SYMPA, MAJ = 0x466dd1, 0x466e9b, 0x46d629, 0x475118
ALLIANCE, BATIMENT, METEO = 0x46da3b, 0x4268d4, 0x4290cf
CONTADOR, LOCAL, ALEATORIO = 0x508f7c, 0x508041, 0x497164
ESTRUTURAS, IA_CONTEXTO = 0x49a0c8, 0x51a990
PARADAS = {0x46994b: 'MessageBoxSet', 0x471830: 'InitGameZone', 0x447b2f: 'AnimBallonStatic'}
CONTADORES_MERCADO = (0, 99, 100, 101, 200, 700, 799, 800, 801, 1600, 8999, 9000)
CONTADORES_ESTRUTURA = (0, 1, 31, 32, 33, 49, 50, 51, 99, 100, 101, 999, 1000, 1001, 2000)
CONTADORES_METEO = (0, 1, 99, 100, 101, 899, 900, 901, 1800, 2700)
SEMENTES = (0x00000001, 0x2b5e0c3a, 0x6a09e667)


def u8(v):
    return bytes([v & 0xff])


def u32(v):
    return struct.pack('<I', v & 0xffffffff)


def _dados(campo):
    return zlib.decompress(base64.b64decode(campo['zlib_base64'])) if 'zlib_base64' in campo \
        else bytes.fromhex(campo['hex'])


def resumo(blocos):
    """Missions' ``resumo_imagem`` over (name, base, bytes): name-sorted ``<II base, size>`` + bytes."""
    h = hashlib.sha256()
    for nome, b, dados in sorted(blocos):
        h.update(struct.pack('<II', b, len(dados)) + dados)
    return dict(blocks=len(blocos), bytes=sum(len(d) for _, _, d in blocos), sha256=h.hexdigest())


def blocos_quadro128(caminho):
    """(name, base, bytes) of the frame-128 full-state checkpoint, its summary checked."""
    bruto = lzma.decompress(Path(caminho).read_bytes())
    if hashlib.sha256(bruto).hexdigest() != SHA_QUADROS128:
        raise ValueError('Not the pinned M2.2 frame capture')
    fase = next(f for f in json.loads(bruto)['phases'] if f['phase'] == 'frame128')
    apos = fase['state_after']
    blocos = [(n, int(b['base'], 16), _dados(b)) for n, b in apos['full_state'].items() if n != 'native_stack']
    if resumo(blocos) != apos['summary']:
        raise ValueError('frame128 full state does not match its summary')
    return blocos, apos['summary']


class CapturaTemporizadores(campos.CapturaExibicao):
    """The display bench with pages mapped as contiguous runs and its own stop set."""
    def __init__(self, blocos):
        sys.path.insert(0, str(RAIZ / 'ferramentas'))
        from emulador import BancadaX86, RETORNO, PILHA, mapear_paginas, unicorn, x86
        self.RETORNO, self.PILHA, self.x86, self.unicorn = RETORNO, PILHA, x86, unicorn
        self.b = BancadaX86()
        self.blocos = blocos
        paginas = set()
        for nome, inicio, raw in blocos:
            if nome != 'dgroup':
                paginas.update(range(inicio & ~0xfff, (inicio + len(raw) + 0xfff) & ~0xfff, 0x1000))
        self.execucoes = mapear_paginas(self.b.cpu, paginas)
        self.codigo = list(self.b.vinculos_declarados.codigo_protegido)
        self.escritas = []
        self.b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._observar)
        self.b.cpu.ctl_flush_tb()

    def chamar(self, rotulo, entrada, regs=None, saida=None):
        self.escritas.clear()
        self.b.cpu.reg_write(self.x86.UC_X86_REG_FPCW, base.CONTROLE_X87)
        r = self.b.executar(entrada, self.codigo, dict(regs or {}), parada={self.RETORNO, *PARADAS},
                            limite_instrucoes=1000000)
        eip = r['EIP']
        return dict(call=rotulo, entry=hex(entrada), regs_in={k: hex(v) for k, v in (regs or {}).items()},
                    outcome='return' if eip == self.RETORNO else 'stop', stop=PARADAS.get(eip),
                    regs_out={k: hex(v) for k, v in r.items()}, writes=list(self.escritas))


def chamada(rotulo, entrada, regs=None):
    return ('chamar', rotulo, entrada, regs or {})


def cenarios(c, prefixo):
    c.recarregar()
    ler8 = lambda a: c.ler(a, 1)[0]
    local = ler8(LOCAL)
    s = []
    mercado = []
    for k in CONTADORES_MERCADO:
        mercado += [('contador', k), chamada(f'c{k}:CalculCompteurMarche', MARCHE, dict(EAX=local)),
                    chamada(f'c{k}:CalculCompteurProposition', PROPOSITION, dict(EAX=local, EDX=0))]
    s.append((f'{prefixo}_market_counters', 'Market and proposition gates as loaded, CalculGame order', [], mercado))
    for estado in (3, 4, 5):
        for contato, parceiro in ((0, 2), (1, 3), (1, 0xff)):
            ov = [(0x4e2928 + local, u8(contato)), (0x496f8c + local, u8(parceiro)),
                  (0x4e2e7c + (local if contato == 1 else parceiro), u8(estado))]
            passos = []
            for k in (99, 100, 101, 800):
                passos += [('contador', k), chamada(f'c{k}:CalculCompteurMarche', MARCHE, dict(EAX=local)),
                           chamada(f'c{k}:CalculCompteurProposition', PROPOSITION, dict(EAX=local, EDX=0))]
            s.append((f'{prefixo}_market_state{estado}_contact{contato}_partner{parceiro:#x}',
                      f'Declared market state {estado}, contact {contato}, partner {parceiro:#x}', ov, passos))
    s.append((f'{prefixo}_sympathy_counters', 'PlayerAttaqueCalculSympa as loaded around the 2000 gate', [],
              [p for k in (1999, 2000, 2001, 4000)
               for p in (('contador', k), chamada(f'c{k}:PlayerAttaqueCalculSympa', SYMPA))]))
    sans_ia = [(IA_CONTEXTO + 16 * j, u8(0)) for j in range(4)]
    s.append((f'{prefixo}_sympathy_no_ai', 'PlayerAttaqueCalculSympa at 2000 with AI context bytes cleared',
              sans_ia, [('contador', 2000), chamada('c2000:PlayerAttaqueCalculSympa', SYMPA)]))
    maj = [chamada(f'MAJSympathie:{a}:{b}:{e:#x}', MAJ, dict(EAX=a, EDX=b, EBX=e))
           for e in (0, 1, 9, 0x13, 0x14, 0x1f) for a, b in ((0, 1), (1, 0), (2, 3), (3, 3), (4, 1))]
    s.append((f'{prefixo}_majsympathie_no_ai', 'MAJSympathie events with AI context bytes cleared', sans_ia, maj))
    s.append((f'{prefixo}_majsympathie_as_loaded', 'MAJSympathie events as loaded', [], maj))
    for nome, ov, n in (('alliance_nonlocal', [(0x5080b0 + 16 * 1 + 8, u32(3)), (0x5080b0 + 16 * 3, u32(1)),
                                               (0x5080b0 + 16 * 2 + 12, u32(0xffffffff))], 4),
                        ('alliance_local', [(0x5080b0 + 16 * local + 4 * ((local + 1) % 4), u32(1)),
                                            (0x5080b0 + 16 * ((local + 2) % 4) + 4 * local, u32(2))], 3)):
        s.append((f'{prefixo}_{nome}', 'Declared alliance counters; PlayerInitAllianceCompteur repeated', ov,
                  [chamada(f'call{i}:PlayerInitAllianceCompteur', ALLIANCE) for i in range(n)]))
    vivas = [i for i in range(1000) if ler8(ESTRUTURAS + 0x114 * i + 5)]
    for i in vivas:
        passos = [p for k in CONTADORES_ESTRUTURA
                  for p in (('contador', k), chamada(f'c{k}:BatimentNextEtape:{i}', BATIMENT, dict(EAX=i)))]
        s.append((f'{prefixo}_structure{i}_counters',
                  f'BatimentNextEtape on live structure {i} (type {ler8(ESTRUTURAS + 0x114 * i + 8)}), '
                  'counters around its gates', [], passos))
    for semente in SEMENTES:
        passos = [p for k in CONTADORES_METEO
                  for p in (('contador', k), chamada(f'c{k}:GetMeteo', METEO))]
        s.append((f'{prefixo}_weather_seed{semente:#x}', f'GetMeteo over its gates, RNG {semente:#x}',
                  [(ALEATORIO, u32(semente))], passos))
    for clima in (0, 1, 2, 0xff):
        s.append((f'{prefixo}_weather_byte{clima:#x}', f'GetMeteo at counter 900 with weather byte {clima:#x}',
                  [(0x496d2c, u8(clima))], [('contador', 900), chamada('c900:GetMeteo', METEO)]))
    return s


def capturar(destino, quadros128):
    destino = Path(destino)
    if destino.exists():
        raise FileExistsError('Preserve existing capture; choose a new output')
    if hashlib.sha256((RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()).hexdigest() != base.HASH_EXE:
        raise ValueError('Not the intact executable')
    blocos_s0, resumo_s0, entradas = campos.blocos_exibicao()
    blocos_128, resumo_128 = blocos_quadro128(quadros128)
    resultados = []
    for prefixo, blocos in (('exibicao_s0', blocos_s0), ('quadro128', blocos_128)):
        c = CapturaTemporizadores(blocos)
        resultados += [base.cenario(c, *x) for x in cenarios(c, prefixo)]
        del c
    chamadas = [k for r in resultados for k in r['calls']]
    arquivos = [Path(__file__), Path(campos.__file__), Path(base.__file__), RAIZ / 'ferramentas/emulador.py']
    saida = dict(
        schema='rising-lands/economy-timers-original-capture/1', sha256_exe=base.HASH_EXE,
        inputs=dict(exibicao_s0=dict(paths=[str(p.relative_to(RAIZ)) for p in entradas],
                                     sha256=[hashlib.sha256(p.read_bytes()).hexdigest() for p in entradas],
                                     state_summary=resumo_s0),
                    quadro128=dict(git_object=':'.join(ORIGEM_QUADROS128), raw_json_sha256=SHA_QUADROS128,
                                   phase='frame128', state_summary=resumo_128),
                    label='post-load and frame-128 states with declared counters and overrides; NOT frame inputs'),
        source_commit=subprocess.check_output(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], text=True).strip(),
        source_files=[dict(path=str(p.relative_to(RAIZ)), sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                      for p in arquivos],
        captured_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        x87_control_word=hex(base.CONTROLE_X87), translation_executed=False, stops={hex(a): n for a, n in PARADAS.items()},
        scenarios=len(resultados), original_entries=len(chamadas),
        returns=sum(k['outcome'] == 'return' for k in chamadas),
        dependency_stops=sum(k['outcome'] == 'stop' for k in chamadas), captures=resultados)
    destino.write_text(json.dumps(saida, separators=(',', ':')) + '\n')
    print(f"Captured original-only: {saida['scenarios']} scenarios, {saida['original_entries']} entries, "
          f"{saida['returns']} returns, {saida['dependency_stops']} dependency stops; translation_executed=False.",
          flush=True)
    return destino


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--quadros128', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    sys.path.insert(0, str(RAIZ / 'ferramentas'))
    from encerramento_captura import encerrar_captura
    encerrar_captura(0, capturar(a.output, a.quadros128))
