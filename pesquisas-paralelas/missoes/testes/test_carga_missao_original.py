"""Stage12 whole-MissionLoad oracle: CPU-free fixture guards plus one gated native replay.

The light tests exercise the declared external handlers with fake binding
calls and a byte-backed fake CPU. They do not validate x86 behavior. The
optional native test (RISING_EMULAR=1) re-runs the intact original from the
program start and compares the committed original-only capture.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import unittest
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ambiente_missoes
from fronteiras_carga_missao import (ArenaAlocacoes, ArquivosCRT, ArquivosWin32, EntradasNomeadas,
                                     MidiaOriginal, PerfilWindows, WindowsDeclarado, _analisar_ini,
                                     rotulo_volume_iso)
from vinculos_declarados import ParadaVinculoDeclarado

CAPTURA = ambiente_missoes.OWNED/'evidencias/captura-carga-missao-original.json'
BIN = ambiente_missoes.ROOT.parent/'source/RISING_LANDS_BR_.BIN'


class CPUFalsa:
    def __init__(self):
        self.regioes = []

    def mem_map(self, base, tamanho):
        self.regioes.append([base, bytearray(tamanho)])

    def _r(self, a, n):
        for base, dados in self.regioes:
            if base <= a and a+n <= base+len(dados):
                return dados, a-base
        raise ValueError('unmapped')

    def mem_write(self, a, dados):
        mem, o = self._r(a, len(dados))
        mem[o:o+len(dados)] = dados

    def mem_read(self, a, n):
        mem, o = self._r(a, n)
        return bytes(mem[o:o+n])


class ChamadaFalsa:
    def __init__(self, cpu, *argumentos, esp=0x1000, retorno=0x401234):
        self.cpu, self.argumentos, self.retorno = cpu, argumentos, retorno
        self.registradores = {'ESP': esp}

    def ler(self, a, n):
        return self.cpu.mem_read(a, n)

    def escrever(self, a, dados):
        self.cpu.mem_write(a, bytes(dados))


def entradas(**mudar):
    base = dict(diretorio_instalacao=b'C:\\RISING', unidade_cd=b'D', rotulo_cd=b'RISING_LANDS_BR_',
                relogio_ms=(5,), preenchimento_alocacao=0xa7, estado_memoria=bytes(32),
                teclas=((0x0d, 0x8000),), id_thread=1)
    base.update(mudar)
    return EntradasNomeadas(**base)


def cpu_com_textos(*textos):
    cpu = CPUFalsa()
    cpu.mem_map(0, 0x4000)
    enderecos, a = [], 0x2000
    for t in textos:
        cpu.mem_write(a, t+b'\0')
        enderecos.append(a)
        a += len(t)+16
    return cpu, enderecos


class FronteirasTest(unittest.TestCase):
    def test_named_inputs_reject_missing_or_malformed_values(self):
        for mudar in (dict(unidade_cd=b'DD'), dict(diretorio_instalacao=b''),
                      dict(preenchimento_alocacao=256), dict(estado_memoria=bytes(31)), dict(rotulo_cd=b'')):
            with self.assertRaises(ValueError):
                entradas(**mudar)

    def test_media_resolution_is_case_insensitive_read_only_and_bounded(self):
        m = MidiaOriginal(entradas())
        self.assertEqual(m.resolver(b'c:\\rising\\RISING.ini').name, 'RISING.INI')
        self.assertEqual(m.resolver(b'./monstre.ini').name, 'MONSTRE.INI')
        self.assertEqual(m.resolver(b'D:\\World\\Monde01.ETA').name, 'MONDE01.ETA')
        self.assertIsNone(m.resolver(b'D:\\World\\NOPE.ETA'))
        self.assertIsNone(m.resolver(b'C:\\RISING\\..\\RISING.INI'))
        with self.assertRaises(ParadaVinculoDeclarado):
            m.resolver(b'E:\\WORLD\\MONDE01.ETA')

    def test_profile_subset_matches_comment_trim_and_default_semantics(self):
        secoes = _analisar_ini(b'; c\r\n[Sec] \r\n Key = 12 \r\nS=" a "\r\n[Dup]\r\nk=1\r\nk=2\r\n')
        self.assertEqual(secoes[b'sec'][b'key'], [b'12'])
        self.assertEqual(secoes[b'sec'][b's'], [b'" a "'])
        self.assertEqual(secoes[b'dup'][b'k'], [b'1', b'2'])
        perfil = PerfilWindows(MidiaOriginal(entradas()))
        cpu, (sec, key, arq, padrao) = cpu_com_textos(b'Soldat', b'nope', b'C:\\RISING\\RISING.INI', b'dflt')
        self.assertEqual(perfil.inteiro(ChamadaFalsa(cpu, sec, key, 77, arq)), 77)
        self.assertEqual(perfil.texto(ChamadaFalsa(cpu, sec, key, padrao, 0x100, 3, arq)), 2)
        self.assertEqual(cpu.mem_read(0x100, 3), b'df\0')
        cpu2, (a2, k2, f2) = cpu_com_textos(b'x', b'y', b'C:\\RISING\\NOFILE.INI')
        with self.assertRaises(ParadaVinculoDeclarado):
            perfil.inteiro(ChamadaFalsa(cpu2, a2, k2, 0, f2))

    def test_crt_streams_return_item_counts_and_stop_on_unknown_streams(self):
        arquivos = ArquivosCRT(MidiaOriginal(entradas()))
        cpu, (caminho, modo, texto) = cpu_com_textos(b'C:\\RISING\\TABLEAU.COL', b'rb', b'rt')
        fluxo = arquivos.fopen(ChamadaFalsa(cpu, caminho, modo))
        self.assertTrue(fluxo)
        dados = (ambiente_missoes.CD/'INSTALHD/TABLEAU.COL').read_bytes()
        self.assertEqual(arquivos.fread(ChamadaFalsa(cpu, 0x100, 100, 7, fluxo)), 7)
        self.assertEqual(cpu.mem_read(0x100, 700), dados[:700])
        self.assertEqual(arquivos.fread(ChamadaFalsa(cpu, 0x100, 10, 1, fluxo)), 0)   # 2 bytes remain
        self.assertEqual(cpu.mem_read(0x100, 2), dados[700:702])
        with self.assertRaises(ParadaVinculoDeclarado):
            arquivos.fopen(ChamadaFalsa(cpu, caminho, texto))
        self.assertEqual(arquivos.fclose(ChamadaFalsa(cpu, fluxo)), 0)
        with self.assertRaises(ParadaVinculoDeclarado):
            arquivos.fread(ChamadaFalsa(cpu, 0x100, 1, 1, fluxo))
        cpu3, (ausente, rb) = cpu_com_textos(b'D:\\WORLD\\ABSENT.ETA', b'rb')
        self.assertEqual(arquivos.fopen(ChamadaFalsa(cpu3, ausente, rb)), 0)

    def test_win32_files_are_read_only_and_report_declared_failures(self):
        w = ArquivosWin32(MidiaOriginal(entradas()))
        cpu, (nome, ausente) = cpu_com_textos(b'RISING.SBL', b'NOPE.SBL')
        h = w.criar(ChamadaFalsa(cpu, nome, 0x80000000, 1, 0, 3, 0x80, 0))
        self.assertEqual(w.posicionar(ChamadaFalsa(cpu, h, 0, 0, 2)), 51451)
        self.assertEqual(w.criar(ChamadaFalsa(cpu, ausente, 0x80000000, 1, 0, 3, 0x80, 0)), 0xffffffff)
        self.assertEqual(w.erro(ChamadaFalsa(cpu)), 2)
        with self.assertRaises(ParadaVinculoDeclarado):
            w.erro(ChamadaFalsa(cpu))
        with self.assertRaises(ParadaVinculoDeclarado):
            w.criar(ChamadaFalsa(cpu, nome, 0x40000000, 0, 0, 2, 0x80, 0))

    def test_arena_has_fixed_identity_declared_fill_and_finite_budget(self):
        cpu = CPUFalsa()
        arena = ArenaAlocacoes(cpu, 0x40000000, 0x40004000, 3, 0xa7)
        p = arena.alocar(ChamadaFalsa(cpu, 0, 10, esp=0x40000000))
        self.assertEqual(cpu.mem_read(p, 10), b'\xa7'*10)
        z = arena.alocar(ChamadaFalsa(cpu, 0x40, 5000, esp=0x40000000))
        self.assertEqual(cpu.mem_read(z, 5000), bytes(5000))
        self.assertEqual(arena.fixar(ChamadaFalsa(cpu, p)), p)
        self.assertEqual(arena.handle(ChamadaFalsa(cpu, p)), p)
        with self.assertRaises(ParadaVinculoDeclarado):
            arena.liberar(ChamadaFalsa(cpu, p))          # still locked
        self.assertEqual(arena.desfixar(ChamadaFalsa(cpu, p)), 0)
        with self.assertRaises(ParadaVinculoDeclarado):
            arena.desfixar(ChamadaFalsa(cpu, p))
        self.assertEqual(arena.liberar(ChamadaFalsa(cpu, p)), 0)
        with self.assertRaises(ParadaVinculoDeclarado):
            arena.handle(ChamadaFalsa(cpu, p))           # stale
        with self.assertRaises(ParadaVinculoDeclarado):
            arena.alocar(ChamadaFalsa(cpu, 2, 10, esp=0x40000000))   # GMEM_MOVEABLE unsupported
        with self.assertRaises(ParadaVinculoDeclarado):
            arena.alocar(ChamadaFalsa(cpu, 0, 0x2000, esp=0x40000000))  # address budget

    def test_declared_windows_answers_are_ordered_and_exhaustible(self):
        w = WindowsDeclarado(entradas())
        cpu, (raiz, outra) = cpu_com_textos(b'd:\\', b'e:\\')
        self.assertEqual(w.tempo(ChamadaFalsa(cpu)), 5)
        with self.assertRaises(ParadaVinculoDeclarado):
            w.tempo(ChamadaFalsa(cpu))
        with self.assertRaises(ParadaVinculoDeclarado):
            w.tecla(ChamadaFalsa(cpu, 0x1b))
        self.assertEqual(w.tecla(ChamadaFalsa(cpu, 0x0d)), 0x8000)
        self.assertEqual(w.tipo_unidade(ChamadaFalsa(cpu, raiz)), 5)
        with self.assertRaises(ParadaVinculoDeclarado):
            w.tipo_unidade(ChamadaFalsa(cpu, outra))
        self.assertEqual(w.volume(ChamadaFalsa(cpu, raiz, 0x100, 0x1f, 0, 0, 0, 0, 0)), 1)
        self.assertEqual(cpu.mem_read(0x100, 17), b'RISING_LANDS_BR_\0')

    @unittest.skipUnless(BIN.exists(), 'Original CD image not present')
    def test_volume_label_comes_from_the_media_pvd(self):
        self.assertEqual(rotulo_volume_iso(BIN)[0], b'RISING_LANDS_BR_')

    def test_startup_skip_cleanup_matches_original_ret_immediates(self):
        import capstone
        import oraculo_carga_missao as o
        exe = (ambiente_missoes.CD/'INSTALHD/RISING.EXE').read_bytes()
        sym = o.simbolos()
        md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        texto_base = 0x401000 - 0x400   # BEGTEXT raw offset 0x400 -> RVA 0x1000
        for nome, (_, limpeza) in o.PULOS_INICIO.items():
            a, rets, visitados, pilha = sym[nome], set(), set(), [sym[nome]]
            while pilha:   # follow jumps inside shared epilogues until a RET
                x = pilha.pop()
                if x in visitados or len(visitados) > 400:
                    continue
                visitados.add(x)
                for ins in md.disasm(exe[x-texto_base:x-texto_base+0x800], x):
                    if ins.mnemonic == 'ret':
                        rets.add(int(ins.op_str, 16) if ins.op_str else 0)
                        break
                    if ins.mnemonic.startswith('j'):
                        try:
                            pilha.append(int(ins.op_str, 16))
                        except ValueError:
                            pass
                        if ins.mnemonic == 'jmp':
                            break
            self.assertEqual(rets, {limpeza}, nome)


@unittest.skipUnless(os.environ.get('RISING_EMULAR') == '1', 'Optional intact-x86: RISING_EMULAR=1')
class ReplayOriginalTest(unittest.TestCase):
    def test_program_start_missionload_reproduces_committed_original_capture(self):
        import capturar_carga_missao_original as c
        from oraculo_carga_missao import BancadaCargaMissaoOriginal, RETORNO_MISSION_LOAD
        captura = json.loads(CAPTURA.read_text())
        ni = captura['named_inputs']
        b = BancadaCargaMissaoOriginal(c.entradas(ni['allocation_fill'], ni['clock_ms'][0]), segundos=120)
        b.iniciar_relogio()
        b.executar_inicio()
        pre = b.imagem()
        self.assertEqual(b.resumo_imagem(pre), captura['inherited_state']['summary'])
        regs = b.executar_mission_load(300)
        self.assertEqual(regs['EIP'], RETORNO_MISSION_LOAD)
        self.assertEqual(regs['EAX'] & 0xff, captura['oracle']['al'])
        self.assertEqual(b.resumo_imagem(b.imagem()), captura['oracle']['final_state']['summary'])
        self.assertEqual(c.eventos_json(b.vinculos_declarados.eventos[b.evento_inicio_oraculo:]),
                         captura['oracle']['binding_events'])
        for nome, bloco in captura['oracle']['final_state']['blocks'].items():
            dados = zlib.decompress(base64.b64decode(bloco['zlib_base64']))
            self.assertEqual(hashlib.sha256(dados).hexdigest(), bloco['sha256'], nome)


if __name__ == '__main__':
    unittest.main()
