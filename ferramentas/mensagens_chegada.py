"""Mensagens por mudança de estado, usando os perfis originais de 0x498b38."""
import json
import struct
from pathlib import Path

PERFIS = json.loads((Path(__file__).resolve().parents[1] / 'relatorios/perfis-mensagens.json').read_text())['perfis']


def notificar_estado(mundo, indice, maquina):
    p = mundo._indice(indice) * 276
    u = mundo.unidades
    if u[p + 2] == u[p + 0x10a] and u[p + 0x89] == u[p + 0x10b]:
        return None
    u[p + 0x10a], u[p + 0x10b] = u[p + 2], u[p + 0x89]
    dono = u[p]
    if dono >= 4 or mundo.controle_jogadores[dono] != 2:
        return None
    grupo = struct.unpack_from('<I', u, p + 0x10c)[0]
    if grupo == 0xffffffff:
        return None
    if grupo >= 100:
        raise ValueError('Grupo da unidade fora da tabela')
    g = grupo * 32
    mascara = struct.unpack_from('<I', mundo.grupos, g + 0x1c)[0]
    perfil = struct.unpack_from('<H', mundo.grupos, g + 0x16)[0]
    if not mascara or perfil == 0xffff or perfil == 0:
        return None
    if perfil >= len(PERFIS):
        raise ValueError('Perfil de mensagens fora do catálogo extraído')
    bits, resultado = 0, 1
    for regra in PERFIS[perfil]:
        if regra['tipo'] != u[p + 1] or regra['estado'] != u[p + 2] or regra['subestado'] not in (255, u[p + 0x89]):
            continue
        if regra['despacho_unidade'] not in (0, 255) or regra['despacho_estrutura'] not in (0, 255):
            raise NotImplementedError('Despacho administrativo adicional deste perfil ainda não traduzido')
        bits |= 1 << (regra['bit'] & 31)
        n, offset = regra['tamanho_resultado'], regra['offset_resultado']
        if n > 0 and offset:
            if offset + n > 276:
                raise ValueError('Payload fora da unidade')
            resultado = int.from_bytes(u[p + offset:p + offset + n], 'little') if n in (1, 2, 4) else 0
    if not bits:
        return None
    struct.pack_into('<I', mundo.grupos, g + 0x1c, 0)
    tarefa = struct.unpack_from('<I', mundo.grupos, g + 8)[0]
    valor = resultado if bits & mascara else 0xffffffff
    if tarefa != 0xffffffff:
        if maquina is None or tarefa >= 100:
            raise ValueError('Máquina/tarefa necessária para receber a mensagem')
        maquina.receber_resultado(tarefa, valor)
    return dict(unidade=indice, grupo=grupo, tarefa=tarefa, bits=bits, resultado=valor)
