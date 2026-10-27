"""Orquestração de 0x47f927. O conteúdo das etapas ainda é externo ao modelo."""
from dataclasses import dataclass
from typing import Callable

ETAPAS = (0x482936, 0x48453c, 0x485183, 0x4866d7, 0x47d314)


@dataclass
class EstadoIA:
    inativo: int = 0          # 0x51a990 + jogador * 16
    ciclos_sem_efetivo: int = 0  # 0x51a995 + jogador * 16


def atualizar_ia(jogador: int, missao: int, estado: EstadoIA,
                 contador_4dfaa8: int, unidades: int, chamar: Callable):
    """Executa ordem e retornos originais; callback recebe endereço e argumentos.

    O contador 0x4dfaa8 ainda não recebe o nome 'construções' sem evidência.
    Callback é obrigatório: não se inventa implementação das decisões internas.
    """
    if not 0 <= jogador <= 4:
        raise ValueError('Jogador deve estar entre 0 e 4')
    contexto = 0x5148b0 + jogador * 16
    if jogador == 4:
        chamar(0x47b283, jogador)
        return chamar(0x47d314, contexto) & 0xffffffff
    if estado.inativo:
        return 0
    if contador_4dfaa8 == 0 and (unidades & 65535) == 0:
        estado.ciclos_sem_efetivo = (estado.ciclos_sem_efetivo + 1) & 255
        if estado.ciclos_sem_efetivo == 10:
            chamar(0x483d95, jogador)
            estado.inativo = 1
            return 0
    else:
        estado.ciclos_sem_efetivo = 0
    for etapa in ETAPAS:
        argumentos = (jogador, missao) if etapa == 0x4866d7 else ((contexto,) if etapa == 0x47d314 else (jogador,))
        resultado = chamar(etapa, *argumentos) & 0xffffffff
        if resultado:
            return resultado
    return 0
