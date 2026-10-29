"""Original-only captures of the economy routines the MONDE01 M2 frame reaches.

Input: the frozen accepted M1 post-load state (Missions'
``captura-carga-missao-original-v2.json``, ``oracle.final_state``), mapped
whole into the bounded x86 bench. It is the snapshot at MissionLoad's return
to 0x42d22d, NOT a frame-1 input: the frame counter and every override below
are declared inputs. Original code runs unpatched over the whole code
section; unreached callees are explicit stops at their entries, never stubs.
No reconstructed routine is imported. See M2_FRAME_INVENTORY.md.
"""
import argparse
import base64
import datetime
import hashlib
import json
import struct
import subprocess
import sys
import zlib
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ENTRADA_M1 = RAIZ / 'pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original-v2.json'
SHA_ESTADO_M1 = '58a5020e79f812e741991410bde0ebc847c927ce141176975a82c0a51a7a1114'
HASH_EXE = '6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb'
CONTROLE_X87 = 0x127f  # Watcom startup control word used by the existing economy benches

ROTINAS = dict(RechercheCalcul=0x47125c, PlayerInitAllianceCompteur=0x46da3b, SetUpdateChamp=0x475328,
               UpdateChamp=0x478806, CalculMatiere=0x467718, CalculCompteurMarche=0x466dd1,
               CalculCompteurProposition=0x466e9b, PlayerAttaqueCalculSympa=0x46d629)
ORDEM_QUADRO = ('RechercheCalcul', 'PlayerInitAllianceCompteur', 'SetUpdateChamp', 'UpdateChamp',
                'CalculMatiere', 'CalculCompteurMarche', 'CalculCompteurProposition', 'PlayerAttaqueCalculSympa')
# Unreached callees and pre-branch checkpoints: execution stops here, never continues.
PARADAS = {0x470f98: 'InventionSetEffet', 0x471830: 'InitGameZone', 0x475118: 'MAJSympathie',
           0x46994b: 'MessageBoxSet', 0x447b2f: 'AnimBallonStatic', 0x466533: 'CalculValeur',
           0x4610a4: 'ForgetMarche', 0x466e01: 'CalculCompteurMarche state-3 branch',
           0x466ed1: 'CalculCompteurProposition state-4 branch',
           0x466fe1: 'CalculCompteurProposition state-5 branch'}
ESTADO7, SAIDA_ESTADO7 = 0x456966, 0x454ccd
TIPO2, SAIDA_TIPO2 = 0x426918, 0x4281c0
UNIDADES_ESTADO7 = (0, 1, 2, 11, 12, 13, 14, 15)
CONTADOR, LOCAL, MISSAO = 0x508f7c, 0x508041, 0x496fe4


def blocos_m1():
    dados = json.loads(ENTRADA_M1.read_bytes())
    final = dados['oracle']['final_state']
    if final['summary']['sha256'] != SHA_ESTADO_M1:
        raise ValueError('Not the accepted M1 post-load state')
    blocos = []
    for nome, b in final['blocks'].items():
        raw = zlib.decompress(base64.b64decode(b['zlib_base64']))
        if len(raw) != b['bytes'] or hashlib.sha256(raw).hexdigest() != b['sha256']:
            raise ValueError(f'M1 block {nome} does not match its SHA-256')
        blocos.append((nome, int(b['base'], 16), raw))
    return blocos


class Captura:
    def __init__(self):
        sys.path.insert(0, str(RAIZ / 'ferramentas'))
        from emulador import BancadaX86, RETORNO, PILHA, unicorn, x86
        self.RETORNO, self.PILHA, self.x86, self.unicorn = RETORNO, PILHA, x86, unicorn
        self.b = BancadaX86()
        self.blocos = blocos_m1()
        paginas = set()
        for nome, base, raw in self.blocos:
            if nome == 'dgroup':
                continue
            for p in range(base & ~0xfff, (base + len(raw) + 0xfff) & ~0xfff, 0x1000):
                paginas.add(p)
        for p in sorted(paginas):
            self.b.cpu.mem_map(p, 0x1000)
        self.codigo = list(self.b.vinculos_declarados.codigo_protegido)
        self.escritas = []
        self.b.cpu.hook_add(unicorn.UC_HOOK_MEM_WRITE, self._observar)

    def _observar(self, cpu, acesso, endereco, tamanho, valor, dados):
        if not self.PILHA <= endereco < self.PILHA + 0x10000:
            self.escritas.append([hex(endereco), tamanho, valor & ((1 << 8 * tamanho) - 1)])

    def recarregar(self):
        for _, base, raw in self.blocos:
            self.b.cpu.mem_write(base, raw)

    def ler(self, a, n):
        return bytes(self.b.cpu.mem_read(a, n))

    def escrever(self, a, dados):
        self.b.cpu.mem_write(a, bytes(dados))

    def sha_estado(self):
        h = hashlib.sha256()
        for nome, base, raw in self.blocos:
            h.update(nome.encode() + self.ler(base, len(raw)))
        return h.hexdigest()

    def chamar(self, rotulo, entrada, regs=None, saida=None):
        self.escritas.clear()
        self.b.cpu.reg_write(self.x86.UC_X86_REG_FPCW, CONTROLE_X87)
        paradas = {saida or self.RETORNO, *PARADAS}
        r = self.b.executar(entrada, self.codigo, dict(regs or {}), parada=paradas, limite_instrucoes=400000)
        eip = r['EIP']
        resultado = 'return' if eip == (saida or self.RETORNO) else 'stop'
        return dict(call=rotulo, entry=hex(entrada), regs_in={k: hex(v) for k, v in (regs or {}).items()},
                    outcome=resultado, stop=None if resultado == 'return' else dict(address=hex(eip), name=PARADAS[eip]),
                    regs_out={k: hex(v) for k, v in r.items()}, writes=list(self.escritas))


def cenario(c, nome, descricao, overrides, passos):
    c.recarregar()
    for a, dados in overrides:
        c.escrever(a, dados)
    inicial = c.sha_estado()
    chamadas = []
    for passo in passos:
        if passo[0] == 'contador':
            c.escrever(CONTADOR, struct.pack('<I', passo[1]))
            continue
        if passo[0] == 'escrever':
            c.escrever(passo[1], passo[2])
            continue
        chamadas.append(c.chamar(*passo[1:]))
    return dict(name=nome, description=descricao,
                overrides=[dict(address=hex(a), bytes=bytes(d).hex()) for a, d in overrides],
                initial_state_sha256=inicial, calls=chamadas, final_state_sha256=c.sha_estado())


def quadro(c, k):
    local = c.ler(LOCAL, 1)[0]
    passos = [('contador', k)]
    for nome in ORDEM_QUADRO:
        regs = {}
        if nome == 'CalculCompteurMarche':
            regs = dict(EAX=local)
        elif nome == 'CalculCompteurProposition':
            regs = dict(EAX=local, EDX=0)
        passos.append(('chamar', f'frame{k}:{nome}', ROTINAS[nome], regs))
    return passos


def u16(v):
    return struct.pack('<H', v)


def u32(v):
    return struct.pack('<I', v)


def recurso(jogador, r, total, apresentacao, bits):
    return 0x4e2ea8 + 32 * jogador + 8 * r + 2, struct.pack('<HHB', total, apresentacao, bits)


def cenarios(c):
    s = []
    # 1. Economy-only frame calls over the M1 state, counters 1..8 (other fronts' calls not run).
    passos = []
    for k in range(1, 9):
        passos += quadro(c, k)
    s.append(('m1_frames_1_8', 'M1 post-load state; economy frame calls only, in CalculGame order, '
              'counter u32 0x508f7c = k declared before each frame (ProgIteration increment).', [], passos))
    s.append(('m1_counter_128', 'M1 post-load state; counter 128 (field update gate).', [],
              [('contador', 128)] + [('chamar', f'counter128:{n}', ROTINAS[n], {})
                                     for n in ('SetUpdateChamp', 'UpdateChamp')]))
    s.append(('m1_counter_2000', 'M1 post-load state; counter 2000 (sympathy gate).', [],
              [('contador', 2000), ('chamar', 'counter2000:PlayerAttaqueCalculSympa',
                                    ROTINAS['PlayerAttaqueCalculSympa'], {})]))
    s.append(('m1_structure0_type2_branch', 'M1 post-load state; BatimentNextEtape type-2 fragment '
              '0x426918 entered with EDI = structure 0, stopped at the shared exit 0x4281c0.', [],
              [('contador', 1), ('chamar', 'type2:structure0', TIPO2, dict(EDI=0), SAIDA_TIPO2)]))
    passos = []
    for k in range(1, 401):
        passos.append(('contador', k))
        passos += [('chamar', f'frame{k}:state7:unit{u}', ESTADO7, dict(EDI=u), SAIDA_ESTADO7)
                   for u in UNIDADES_ESTADO7]
    s.append(('m1_state7_400_frames', 'M1 post-load state; unit state-7 fragment 0x456966 entered with '
              'EDI = unit for the eight MONDE01 state-7 units in dispatcher order, 400 frames, '
              'stopped at the EnginNextEtape exit 0x454ccd. Shared prelude draws are not run.', [], passos))
    # 2. M1-derived declared overrides for the reached routines' data-dependent branches.
    unidades = struct.unpack('<I', c.ler(0x4e19a0, 4))[0]
    facings = (0, 15, 16, 127, 128, 200, 255, 13)
    ov = [(unidades + 276 * u + 0x91, bytes([f])) for u, f in zip(UNIDADES_ESTADO7, facings)]
    passos = []
    for k in range(1, 401):
        passos += [('chamar', f'frame{k}:state7:unit{u}', ESTADO7, dict(EDI=u), SAIDA_ESTADO7)
                   for u in UNIDADES_ESTADO7]
    s.append(('m1_override_state7_facings', 'M1-derived: facing byte +0x91 of the eight units overridden.',
              ov, passos))
    tipos = (9, 10, 11, 16, 17, 18, 25, 26)
    ov = [(unidades + 276 * u + 1, bytes([t])) for u, t in zip(UNIDADES_ESTADO7, tipos)]
    s.append(('m1_override_state7_types', 'M1-derived: unit type byte +1 overridden (9,10,11,16,17,18,25,26).',
              ov, [('chamar', f'state7:unit{u}', ESTADO7, dict(EDI=u), SAIDA_ESTADO7) for u in UNIDADES_ESTADO7]))
    materias = [
        ('m1_override_matiere_down', [recurso(0, 1, 5, 4321, 0), recurso(0, 2, 0, 9999, 0x0f)]),
        ('m1_override_matiere_mixed', [recurso(0, 0, 1909, 1090, 0x05), recurso(0, 1, 30, 30, 0x02),
                                       recurso(0, 3, 65535, 0, 0)]),
        ('m1_override_matiere_wide', [recurso(0, 0, 0, 65535, 0xff), recurso(0, 1, 12000, 9000, 0x30)]),
    ]
    for nome, ov in materias:
        s.append((nome, 'M1-derived: local player resource totals/presentation/bits overridden; '
                  'CalculMatiere called 24 times.', ov,
                  [('chamar', f'call{i}:CalculMatiere', ROTINAS['CalculMatiere'], {}) for i in range(24)]))
    s.append(('m1_override_matiere_local2', 'M1-derived: local player byte 0x508041 = 2 with player-2 records.',
              [(LOCAL, b'\x02'), recurso(2, 0, 77, 0, 0), recurso(2, 2, 3, 8, 0)],
              [('chamar', f'call{i}:CalculMatiere', ROTINAS['CalculMatiere'], {}) for i in range(20)]))
    # RechercheCalcul: scientists, invention threshold, end marker, mission gate, count gate.
    pesquisas = [
        ('m1_override_research_scientists', [(0x508174, u16(3) + u16(1) + u16(1000) + u16(0xffff))], 40),
        ('m1_override_research_threshold', [(0x5080f4 + 32 + 8, struct.pack('<d', 199.5)),
                                            (0x508174 + 4, u16(2))], 3),
        ('m1_override_research_end_marker', [(0x5080f4 + 0, bytes([19])), (0x5080f4 + 16 + 4, b'\x03'),
                                             (0x5080f4 + 16 + 3, bytes([18]))], 3),
        ('m1_override_research_mission_gate', [(MISSAO, b'\x00')], 3),
        ('m1_override_research_count_gate', [(0x50871c, bytes([2, 1, 3, 0xff])),
                                             (0x508174, u16(5) * 4)], 2),
    ]
    for nome, ov, n in pesquisas:
        s.append((nome, 'M1-derived research overrides; RechercheCalcul repeated.', ov,
                  [('chamar', f'call{i}:RechercheCalcul', ROTINAS['RechercheCalcul'], {}) for i in range(n)]))
    aliancas = [
        ('m1_override_alliance_nonlocal', [(0x5080b0 + 16 * 1 + 4 * 2, u32(3)), (0x5080b0 + 16 * 3, u32(1)),
                                           (0x5080b0 + 16 * 2 + 12, u32(0xffffffff))], 4),
        ('m1_override_alliance_local', [(0x5080b0 + 16 * 2 + 4, u32(1)), (0x5080b0 + 4, u32(2)),
                                        (0x5080b0 + 8, u32(5))], 3),
    ]
    for nome, ov, n in aliancas:
        s.append((nome, 'M1-derived alliance-counter overrides; PlayerInitAllianceCompteur repeated.', ov,
                  [('chamar', f'call{i}:PlayerInitAllianceCompteur', ROTINAS['PlayerInitAllianceCompteur'], {})
                   for i in range(n)]))
    for estado in (0, 1, 2, 3, 4, 5, 6, 0xff):
        for contato, parceiro in ((0, 0xff), (1, 0xff), (0, 2), (1, 3)):
            ov = [(0x4e2928, bytes([contato])), (0x496f8c, bytes([parceiro])),
                  (0x4e2e7c + (0 if contato == 1 else parceiro), bytes([estado]))]
            passos = [('contador', 300)]
            passos += [('chamar', 'CalculCompteurMarche', ROTINAS['CalculCompteurMarche'], dict(EAX=0)),
                       ('chamar', 'CalculCompteurProposition', ROTINAS['CalculCompteurProposition'],
                        dict(EAX=0, EDX=0))]
            s.append((f'm1_override_market_state{estado}_contact{contato}_partner{parceiro}',
                      'M1-derived market gate overrides; counter 300.', ov, passos))
    for nome, flags in (('m1_override_sympathy_all_attacked', [1] * 16),
                        ('m1_override_sympathy_one_pair', [1] * 6 + [0] + [1] * 9)):
        ov = [(0x508044 + 20 * (i // 4) + 4 * (i % 4), u32(f)) for i, f in enumerate(flags)]
        s.append((nome, 'M1-derived attack-flag overrides; counter 2000.', ov,
                  [('contador', 2000), ('chamar', 'PlayerAttaqueCalculSympa',
                                        ROTINAS['PlayerAttaqueCalculSympa'], {})]))
    return s


def capturar(destino):
    destino = Path(destino)
    if destino.exists():
        raise FileExistsError('Preserve existing capture; choose a new output')
    original = (RAIZ.parent / 'source/cd/INSTALHD/RISING.EXE').read_bytes()
    if hashlib.sha256(original).hexdigest() != HASH_EXE:
        raise ValueError('Not the intact executable')
    c = Captura()
    resultados = [cenario(c, *x) for x in cenarios(c)]
    chamadas = [k for r in resultados for k in r['calls']]
    arquivos = [Path(__file__), RAIZ / 'ferramentas/emulador.py', ENTRADA_M1]
    saida = dict(
        schema='rising-lands/economy-m2-frame-original-capture/1', sha256_exe=HASH_EXE,
        input=dict(path=str(ENTRADA_M1.relative_to(RAIZ)), state_sha256=SHA_ESTADO_M1,
                   label='M1 post-load state (MissionLoad return to 0x42d22d); NOT a frame-1 input'),
        source_commit=subprocess.check_output(['git', '-C', str(RAIZ), 'rev-parse', 'HEAD'], text=True).strip(),
        source_files=[dict(path=str(p.relative_to(RAIZ)), sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                      for p in arquivos],
        captured_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        x87_control_word=hex(CONTROLE_X87), translation_executed=False,
        allowed_original_intervals=[[hex(a), hex(b)] for a, b in c.codigo],
        stops={hex(a): n for a, n in PARADAS.items()},
        scenarios=len(resultados), original_entries=len(chamadas),
        returns=sum(k['outcome'] == 'return' for k in chamadas),
        dependency_stops=sum(k['outcome'] == 'stop' for k in chamadas),
        captures=resultados)
    destino.write_text(json.dumps(saida, separators=(',', ':')) + '\n')
    print(f"Captured original-only: {saida['scenarios']} scenarios, {saida['original_entries']} entries, "
          f"{saida['returns']} returns, {saida['dependency_stops']} dependency stops; translation_executed=False.")


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', required=True)
    capturar(p.parse_args().output)
