"""MaquinaTarefasViva: the unchanged task VM bound to the live task memory 0x512320..0x514908."""
import base64
import hashlib
import json
from pathlib import Path
import struct
import sys
import unittest
import zlib

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'ferramentas'))
from tarefas_ia import (MaquinaTarefas, MaquinaTarefasViva, POOL_TAREFAS, LISTA_LIVRE, CONTEXTOS_TAREFAS,
                        TAREFAS_ATIVAS, FIM_TAREFAS, i32)
from memoria_quadro_core import MemoriaQuadro

RUL = RAIZ.parent / 'source/cd/INSTALHD/RISING.RUL'
QUADRO1 = RAIZ / 'pesquisas-paralelas/missoes/evidencias/captura-quadro1-monde01-original.json'
DGROUP0 = 0x494000


def estados_quadro():
    """DGROUP at S0 (frozen M1 = frame-0 input) and after each Missions phase (exact frame states)."""
    from estado_m1_quadro import carregar_m1
    dados = QUADRO1.read_bytes()
    if hashlib.sha256(dados).hexdigest() != 'c06f78ea2f611d668b4a2fc7bde712b07c21ed8eb0a929668d4d70e56d47fed8':
        raise AssertionError('Missions frame-1 capture changed')
    estados = {'s0': bytes(carregar_m1()[0])}
    anterior = estados['s0']
    for p in json.loads(dados)['phases']:
        blocos = p['state_after']['blocks_changed_since_previous']
        if 'dgroup' in blocos:
            anterior = zlib.decompress(base64.b64decode(blocos['dgroup']['zlib_base64']))
        estados[p['phase']] = anterior
    return estados


def pela_ponte(programa, dgroup, acao):
    """Reference: the base MaquinaTarefas loaded from and stored back to a copy (ai-runtime's bridge)."""
    m = bytearray(dgroup)
    o = lambda a: a - DGROUP0
    u32 = lambda a: struct.unpack_from('<I', m, o(a))[0]
    mq = MaquinaTarefas(programa)
    mq.memoria[:] = m[o(POOL_TAREFAS):o(LISTA_LIVRE)]
    mq.livres = [i32(u32(LISTA_LIVRE)), u32(LISTA_LIVRE + 4)]
    mq.contextos = [[i32(u32(CONTEXTOS_TAREFAS + 16 * k)), u32(CONTEXTOS_TAREFAS + 16 * k + 4)] for k in range(5)]
    mq.ativas = u32(TAREFAS_ATIVAS)
    try:
        resultado = ('ok', acao(mq))
    except Exception as e:
        resultado = (type(e).__name__, str(e))
    m[o(POOL_TAREFAS):o(LISTA_LIVRE)] = mq.memoria
    for endereco, valor in [(LISTA_LIVRE, mq.livres[0]), (LISTA_LIVRE + 4, mq.livres[1]), (TAREFAS_ATIVAS, mq.ativas)] + [
            (CONTEXTOS_TAREFAS + 16 * k + 4 * j, mq.contextos[k][j]) for k in range(5) for j in (0, 1)]:
        struct.pack_into('<I', m, o(endereco), valor & 0xffffffff)
    return resultado, bytes(m)


def ao_vivo(programa, dgroup, acao):
    m = bytearray(dgroup)
    mq = MaquinaTarefasViva(programa, memoryview(m)[POOL_TAREFAS - DGROUP0:FIM_TAREFAS - DGROUP0])
    try:
        resultado = ('ok', acao(mq))
    except Exception as e:
        resultado = (type(e).__name__, str(e))
    return resultado, bytes(m), m


@unittest.skipUnless(RUL.exists(), 'Original RISING.RUL not available locally')
class TarefasVivas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from simbolos_ia import ler_rul
        cls.programa = ler_rul(RUL.read_bytes())
        cls.estados = estados_quadro()
        cls.tipo = next(t for t in range(1, 64) if cls.programa.entradas[t])

    def test_solver_on_live_memory_equals_the_bridge_at_the_frame_states(self):
        for fase, dgroup in self.estados.items():
            for jogador in range(5):
                with self.subTest(fase=fase, jogador=jogador):
                    ref, ref_bytes = pela_ponte(self.programa, dgroup, lambda mq: mq.atualizar(jogador))
                    viva, viva_bytes, _ = ao_vivo(self.programa, dgroup, lambda mq: mq.atualizar(jogador))
                    self.assertEqual(viva, ref)
                    self.assertEqual(viva_bytes, ref_bytes)

    def test_every_task_type_posted_and_solved_equals_the_bridge(self):
        """postar + atualizar(4) for all 42 rule entries: completion, sleep, subtasks and
        named world-operation stops (partial effects retained) all land identically."""
        dgroup = self.estados['between_frames']
        for tipo in (t for t in range(1, 64) if self.programa.entradas[t]):
            with self.subTest(tipo=tipo):
                acao = lambda mq: (mq.postar(4, tipo, (7, 8)), mq.atualizar(4))
                ref, ref_bytes = pela_ponte(self.programa, dgroup, acao)
                viva, viva_bytes, _ = ao_vivo(self.programa, dgroup, acao)
                self.assertEqual(viva, ref)
                self.assertEqual(viva_bytes, ref_bytes)

    def test_writes_land_in_the_callers_buffer(self):
        dgroup = self.estados['between_frames']
        resultado, _, buffer = ao_vivo(self.programa, dgroup, lambda mq: (mq.postar(4, 9, (7, 8)), mq.atualizar(4)))
        indice, retorno = resultado[1]
        self.assertEqual(retorno, 0)                          # the posted task stays active
        mudados = {DGROUP0 + i for i in range(len(dgroup)) if buffer[i] != dgroup[i]}
        self.assertTrue(mudados)
        self.assertTrue(all(POOL_TAREFAS <= a < FIM_TAREFAS for a in mudados))
        registro = POOL_TAREFAS + 0x60 * indice
        self.assertEqual(struct.unpack_from('<I', buffer, registro + 0x18 - DGROUP0)[0], 7)
        self.assertEqual(buffer[registro + 0x5c - DGROUP0], 4)
        self.assertEqual(struct.unpack_from('<i', buffer, CONTEXTOS_TAREFAS + 64 - DGROUP0)[0], indice)
        # The task and the subtask it spawned are both counted in the live u32 0x514904.
        self.assertEqual(struct.unpack_from('<I', buffer, TAREFAS_ATIVAS - DGROUP0)[0],
                         struct.unpack_from('<I', dgroup, TAREFAS_ATIVAS - DGROUP0)[0] + 2)

    def test_flat_memory_binding_aliases_the_segment(self):
        dgroup = bytearray(self.estados['s0'])
        memoria = MemoriaQuadro([(DGROUP0, dgroup)])
        mq = MaquinaTarefasViva.sobre_memoria(self.programa, memoria)
        antes = memoria.u32(TAREFAS_ATIVAS)
        mq.ativas += 1
        self.assertEqual(memoria.u32(TAREFAS_ATIVAS), (antes + 1) & 0xffffffff)
        self.assertEqual(struct.unpack_from('<I', dgroup, TAREFAS_ATIVAS - DGROUP0)[0], (antes + 1) & 0xffffffff)
        mq.contextos[4][1] = mq.contextos[4][1] + 1
        self.assertEqual(memoria.u32(CONTEXTOS_TAREFAS + 64 + 4), mq.contextos[4][1])

    def test_rejects_a_copy_of_the_wrong_size_or_read_only(self):
        with self.assertRaises(ValueError):
            MaquinaTarefasViva(self.programa, bytearray(100))
        with self.assertRaises(ValueError):
            MaquinaTarefasViva(self.programa, bytes(FIM_TAREFAS - POOL_TAREFAS))
        with self.assertRaises(ValueError):
            MaquinaTarefasViva.sobre_memoria(self.programa, MemoriaQuadro([(0x1000, bytearray(16))]))


if __name__ == '__main__':
    unittest.main()
