"""Strict seven-register routing for all 16 S1 Core coverage gaps plus AI/runtime's two queries.

Use the caller's owned ambiente_* bootstrap, then pass live u8/u16/u32 memory to provedor_lacunas_s1.
No world is initialized or copied. Every known call requires all seven registers. ChercheGcLibre,
BatimentGetCaseAdjacent and EnginRestaureEtat additionally require readable entry ESP; unknown stack
bits never become successful zero registers. The returned protocol is EAX/EBX/ECX/EDX/ESI/EDI/EBP.

restauracao and refugio are explicit owner providers (nome, chamada, regs) -> all seven registers:
Economy's provedor_restauracao(Restauracao(...)), and a thin adapter to Combat's LutaFatalViva.chamar
or refugio_registradores. Their game bodies are not copied here. Missing owner providers, unknown bits
or incomplete provider returns raise explicitly, retaining every effect that already occurred.
"""
from buscas_bloqueios import BuscasBloqueios, ROTINAS as BUSCAS
from consultas_luta import ConsultasLuta, ROTINAS as LUTAS
from consultas_estado_core import ConsultasEstadoCore, ROTINAS as ESTADO, REG7, M32, exigir_registradores

DONOS = {'EnginRestaureEtat': 0x45315f, 'ChercheBatimentProximiteCaveOuSanctuaire': 0x4539f3}
ROTINAS = {**BUSCAS, **LUTAS, **ESTADO, **DONOS}
EXIGE_ESP = frozenset(('ChercheGcLibre', 'BatimentGetCaseAdjacent', 'EnginRestaureEtat'))


class DependenciaLacunaS1(NotImplementedError):
    def __init__(self, nome, chamada, motivo):
        self.rotina, self.chamada = nome, chamada
        super().__init__(f'{nome} at 0x{chamada:x}: {motivo}; earlier effects retained')


def provedor_lacunas_s1(memoria, *, som=None, restauracao=None, refugio=None, outros=None):
    """Return externo(nome, chamada, regs); same live buffers, original stores/callback order.

Read-only searches/blocking/queries store nothing. The list/task stores and StopSound-before-PostSound
sequence remain ConsultasLuta's. Owner callbacks execute once, in place; exceptions propagate without
retry or rollback. Unknown names go unchanged to outros, or raise a named dependency.
"""
    buscas = BuscasBloqueios(memoria)
    luta = ConsultasLuta(memoria, som=som)
    estado = ConsultasEstadoCore(memoria)

    def externo(nome, chamada, regs):
        if nome not in ROTINAS:
            if outros is None:
                raise DependenciaLacunaS1(nome, chamada, 'no provider')
            return outros(nome, chamada, regs)
        entrada = exigir_registradores(nome, chamada, regs, esp=nome in EXIGE_ESP)
        if regs.get('_pilha'):
            raise ValueError(f'{nome} takes no pushed words')
        if nome in BUSCAS:
            saida = buscas.chamar(nome, entrada)
        elif nome in LUTAS:
            saida = luta.chamar(nome, entrada)
        elif nome in ESTADO:
            saida = estado.chamar(nome, entrada)
        else:
            provedor = restauracao if nome == 'EnginRestaureEtat' else refugio
            if provedor is None:
                raise DependenciaLacunaS1(nome, chamada, 'committed owner provider required')
            saida = provedor(nome, chamada, entrada)
        faltando = [k for k in REG7 if k not in saida]
        if faltando:
            raise DependenciaLacunaS1(nome, chamada, 'provider omitted ' + ', '.join(faltando))
        if any((saida.get('_incertos') or {}).values()):
            raise DependenciaLacunaS1(nome, chamada, 'exact stack/register values unavailable')
        return {k: saida[k] & M32 for k in REG7}
    return externo
