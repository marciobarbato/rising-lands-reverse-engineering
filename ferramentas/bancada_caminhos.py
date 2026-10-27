"""Experimentos sintéticos no solucionador original; requer Unicorn com JIT.

Não é uma reimplementação do algoritmo: executa seus bytes originais sob os
limites da bancada, com grades fornecidas pelo experimento, sem APIs Windows.
"""
import struct
from emulador import BancadaX86

GRADE = 0x1100000
ATRIBUTOS = 0x1120000
OBJETOS = 0x1130000
JOGADORES = 0x1140000
ROTA = 0x1141000

# Trechos identificados, incluindo epílogos compartilhados pelo compilador.
INTERVALOS = [(0x42d4f8, 0x42d64c), (0x42d674, 0x42e890),
              (0x42e890, 0x42eb42), (0x42eba4, 0x42ee1c),
              (0x42f1da, 0x42f1e1), (0x42f214, 0x43b30b),
              (0x43b30b, 0x43e128), (0x43eb64, 0x43ec48),
              (0x4423d2, 0x442416), (0x46d838, 0x46d877),
              (0x4704dc, 0x470520), (0x48c3b0, 0x48c3c8), (0x48d890, 0x48d933)]


class BancadaCaminhos(BancadaX86):
    def __init__(self):
        super().__init__()
        self.cpu.mem_map(GRADE, 0x50000)
        for endereco, valor in [(0x4e0f38, GRADE), (0x507da8, ATRIBUTOS),
                                (0x507d74, OBJETOS), (0x5080a8, JOGADORES)]:
            self.cpu.mem_write(endereco, struct.pack('<I', valor))

    def buscar(self, inicio, destino, largura=16, altura=16, bloqueios=(), semente=1,
               tipo=0, mascara=1, regioes=None):
        if not (1 <= largura <= 256 and 1 <= altura <= 256 and 0 <= tipo < 26):
            raise ValueError('Dimensões ou tipo inválidos')
        def celula(xy):
            x, y = xy
            if not 0 <= x < largura or not 0 <= y < altura:
                raise ValueError('Coordenada fora do mapa')
            return x + y * 256
        a, b = celula(inicio), celula(destino)
        self.cpu.mem_write(GRADE, bytes(0x20000))
        atributos = bytearray(65536)
        for posicao in bloqueios:
            atributos[celula(posicao)] = mascara
        self.cpu.mem_write(ATRIBUTOS, bytes(atributos))
        self.cpu.mem_write(OBJETOS, bytes(65536))
        for posicao, regiao in (regioes or {}).items():
            self.cpu.mem_write(GRADE + celula(posicao) * 2, struct.pack('<H', regiao))
        self.cpu.mem_write(ROTA, bytes(1024))
        self.cpu.mem_write(JOGADORES, bytes(100))
        self.cpu.mem_write(0x497168, struct.pack('<HH', largura, altura))
        self.cpu.mem_write(0x497164, struct.pack('<I', semente))
        self.cpu.mem_write(0x4e1771, b'\0')
        unidade = bytearray(276)
        unidade[1], unidade[2] = tipo, 7
        struct.pack_into('<H', unidade, 8, a)
        struct.pack_into('<H', unidade, 0x7e, b)
        struct.pack_into('<H', unidade, 0xfa, (regioes or {}).get(inicio, 0))
        self.escrever_unidade(unidade)
        r = self.executar(0x43b30b, INTERVALOS, dict(EAX=a, EDX=b, EBX=0, ECX=mascara),
                          pilha={4: struct.pack('<III', ROTA, 0, 0)})
        preparacao = bool(r['EAX'] & 255)
        destino_registrado = not self.cpu.mem_read(0x496302, 1)[0]
        self.executar(0x42f214, INTERVALOS)
        tamanho = struct.unpack('<H', self.cpu.mem_read(ROTA, 2))[0]
        if tamanho > 255:
            raise RuntimeError('Tamanho de rota inesperado')
        invertidas = struct.unpack('<' + 'H' * tamanho, self.cpu.mem_read(ROTA + 2, tamanho * 2)) if tamanho else ()
        return dict(preparacao=preparacao, concluido=self.cpu.mem_read(0x496302, 1)[0],
                    sucesso=self.cpu.mem_read(0x4e0f37, 1)[0], status=self.cpu.mem_read(0x4e0f4c, 1)[0],
                    destino_ajustado=(struct.unpack('<H', self.cpu.mem_read(0x4e0f46, 2))[0] if destino_registrado else None),
                    rota=[[c & 255, c >> 8] for c in reversed(invertidas)],
                    semente_final=struct.unpack('<I', self.cpu.mem_read(0x497164, 4))[0])


if __name__ == '__main__':
    import json
    from pathlib import Path
    from emulador import HASH_ORIGINAL
    casos = [
        dict(nome='aberto_diagonal', inicio=(2, 2), destino=(8, 8)),
        dict(nome='aberto_horizontal', inicio=(2, 2), destino=(8, 2)),
        dict(nome='mesma_celula', inicio=(2, 2), destino=(2, 2)),
        dict(nome='parede_proxima', inicio=(2, 2), destino=(8, 2), bloqueios=[(3, y) for y in range(6)]),
        dict(nome='parede_distante', inicio=(2, 2), destino=(8, 2), bloqueios=[(5, y) for y in range(6)]),
        dict(nome='destino_bloqueado', inicio=(2, 2), destino=(8, 2), bloqueios=[(8, 2)]),
        dict(nome='regioes_distintas', inicio=(2, 2), destino=(8, 2), regioes={(8, 2): 23}),
        dict(nome='classe_2', inicio=(2, 2), destino=(8, 8), tipo=11),
        dict(nome='classe_3', inicio=(2, 2), destino=(8, 8), tipo=3),
    ]
    resultados = []
    for caso in casos:
        argumentos = {k: v for k, v in caso.items() if k != 'nome'}
        resultado = BancadaCaminhos().buscar(**argumentos)
        entrada = dict(argumentos)
        if 'regioes' in entrada:
            entrada['regioes'] = [dict(posicao=k, rotulo=v) for k, v in entrada['regioes'].items()]
        resultados.append(dict(nome=caso['nome'], entrada=entrada, resultado=resultado))
    relatorio = dict(sha256_original=HASH_ORIGINAL, limite_instrucoes_por_chamada=20000,
                     observacao='Grades sintéticas; rotas podem ser parciais. Não valida o movimento integrado.',
                     casos=resultados)
    arquivo = Path(__file__).resolve().parents[1] / 'relatorios/caminhos-experimentos.json'
    arquivo.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(str(arquivo))
