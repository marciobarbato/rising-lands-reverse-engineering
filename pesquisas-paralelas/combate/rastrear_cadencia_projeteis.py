"""Referências diretas de cadência/impacto no EXE; escreve só nesta pesquisa.

Reinicia a decodificação por símbolo e confere CALL rel32 por byte. Não prova
ausência de chamadas indiretas, aliases ou caminhos não alcançáveis.
"""
import bisect
import hashlib
import json
import struct

from extrair_evidencias import HASH, PASTA, REPO, ler_imagem
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_AC_WRITE
from capstone.x86 import X86_OP_IMM, X86_OP_MEM

INICIO, FIM = 0x401000, 0x493c00  # BEGTEXT, tamanho bruto original
ALVOS = {0x46fc0f: 'ProjectileCalcul', 0x43f14f: 'DDFlipPage',
         0x47500e: 'ProgIteration', 0x42c868: 'CalculGame'}


def auditar():
    imagem = ler_imagem()
    bruto = (REPO / 'evidencias/simbolos-importados.tsv').read_bytes()
    simbolos = sorted((int(l.split('\t')[0], 16), l.split('\t')[1])
        for l in bruto.decode().splitlines()[1:]
        if INICIO <= int(l.split('\t')[0], 16) < FIM)
    enderecos = [a for a, _ in simbolos]
    def simbolo(a):
        posicao = bisect.bisect_right(enderecos, a) - 1
        return simbolos[posicao][1] if posicao >= 0 else '(antes do primeiro símbolo)'
    def registro(i):
        return dict(endereco=f'0x{i.address:08x}', simbolo=simbolo(i.address),
                    bytes=i.bytes.hex(), instrucao=f'{i.mnemonic} {i.op_str}')
    cs = Cs(CS_ARCH_X86, CS_MODE_32)
    cs.detail, cs.skipdata = True, True
    chamadas, campo_impacto, ciclo, fronteiras = [], [], [], set()
    limites = sorted({INICIO, FIM, *enderecos})
    for a, z in zip(limites, limites[1:]):
        for i in cs.disasm(bytes(imagem[a - 0x400000:z - 0x400000]), a):
            if not i.id:
                continue
            fronteiras.add(i.address)
            if i.mnemonic == 'call' and i.operands[0].type == X86_OP_IMM:
                destino = i.operands[0].imm
                if destino in ALVOS:
                    chamadas.append(dict(**registro(i), destino=f'0x{destino:08x}', nome=ALVOS[destino]))
            for op in i.operands:
                if op.type != X86_OP_MEM or op.mem.base or op.mem.index:
                    continue
                if op.mem.disp == 0x4dfb44:
                    campo_impacto.append(registro(i))
                if op.mem.disp == 0x508f7c and (op.access & CS_AC_WRITE or 0x46e52c <= i.address < 0x46e5fe):
                    ciclo.append(dict(**registro(i), tamanho=op.size,
                                      escrita=bool(op.access & CS_AC_WRITE)))
    # Não depende do alinhamento da primeira passagem para achar E8 rel32.
    por_byte = []
    for a in range(INICIO, FIM - 4):
        k = a - 0x400000
        if imagem[k] == 0xe8 and (a + 5 + struct.unpack_from('<i', imagem, k + 1)[0]) & 0xffffffff == 0x46fc0f:
            por_byte.append(dict(endereco=f'0x{a:08x}', simbolo=simbolo(a),
                bytes=bytes(imagem[k:k + 5]).hex(), fronteira_por_simbolo=a in fronteiras))
    return dict(sha256_original=HASH, sha256_simbolos=hashlib.sha256(bruto).hexdigest(),
        intervalo=['0x00401000', '0x00493c00'],
        metodo='Decodificação linear reiniciada por símbolo e busca de CALL rel32 por byte; sem prova geral de alcançabilidade ou aliases.',
        chamadas=chamadas, candidatos_call_projectilecalcul_por_byte=por_byte,
        referencias_4dfb44=campo_impacto, escritas_ciclo_e_leituras_anim=ciclo,
        limites='Chamadas indiretas e acessos por ponteiros calculados não são resolvidos; nomes vêm da tabela SBL já extraída.')


if __name__ == '__main__':
    relatorio = auditar()
    saida = PASTA / 'evidencias/rastreio-cadencia-projeteis.json'
    saida.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(relatorio["candidatos_call_projectilecalcul_por_byte"])} CALL rel32 para ProjectileCalcul; '
          f'{len(relatorio["referencias_4dfb44"])} referências absolutas ao impacto; {saida}')
