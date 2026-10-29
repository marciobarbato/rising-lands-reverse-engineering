"""Named oracle scenarios shared by the Missions capture and validation scripts.

``v1``: the accepted M1/frame-1 bench (display, text, audio and video skipped;
frames 0/1 with a declared ProgIteration caller frame).

``exibicao`` (display executed, the M2 reference): the real _WinMain@16 loop
from AppInit on, with AffInit/DDInit, the bank loaders, RestoreAll, menu and
game AffGame run natively over Graphics' declared DirectDraw backend; text,
LoadPie pictures, video, credits and audio stay declared boundaries.  Its
artifacts never replace v1 files.  ``exibicao_interino`` names the Stage17
artifacts made with the retired interim backend.  ``exibicao_v3`` (prepared,
no reference artifacts until M2.1 is accepted) additionally binds Core's CRT
fseek/fgets and executes LoadPie; text still waits for CRT ftell.  Importing this module executes nothing.
"""
import ambiente_missoes

OWNED = ambiente_missoes.OWNED
# Declared display clock after the M1 clock value: one answer per call, 40 ms apart (25 Hz).
TICKS_EXIBICAO = tuple(0x123456 + 40*k for k in range(1, 4097))
PROVENIENCIA_EXIBICAO = dict(
    display_ticks='declared GetTickCount/timeGetTime answers for every call other than iaRandom(0) in IaAlloc: '
                  '0x123456+40*k, k=1.. in call order (a 25 Hz display clock after the M1 clock value); every '
                  'value is an original execution, the real one is nondeterministic',
    ia_random_clock='the IaAlloc iaRandom(0) call keeps the accepted M1 clock value, so the game RNG seed '
                    'equals the v1 scenario',
    surface_fill='declared initial byte 0 of DirectDraw surfaces (contents undefined by DirectDraw)',
    directdraw='Graphics declared backend fronteiras_exibicao.ExibicaoDeclarada (objects at 0x3600000, surfaces at '
               '0x60000000), installed after the bench imports',
    window='no window was created (AppWindowInit is not executed): hwnd arguments are the values the '
           'program holds (0)')

ARTEFATOS = {
    'v1': dict(entrada='evidencias/entrada-carga-missao-original.json',
               captura_m1='evidencias/captura-carga-missao-original-v2.json',
               captura_quadro='evidencias/captura-quadro1-monde01-original.json',
               rastro_quadro='evidencias/rastro-quadro1-monde01.json'),
    # Stage17 display artifacts, made with the retired interim backend (historical, not rerunnable here).
    'exibicao_interino': dict(entrada='evidencias/entrada-carga-missao-exibicao.json',
                              captura_m1='evidencias/captura-carga-missao-exibicao.json',
                              captura_quadro='evidencias/captura-quadro1-monde01-exibicao.json',
                              rastro_quadro='evidencias/rastro-quadro1-monde01-exibicao.json'),
    # M2 reference: display scenario over Graphics' declared backend.
    'exibicao': dict(entrada='evidencias/entrada-carga-missao-exibicao-v2.json',
                     captura_m1='evidencias/captura-carga-missao-exibicao-v2.json',
                     captura_quadro='evidencias/captura-quadro1-monde01-exibicao-v2.json',
                     rastro_quadro='evidencias/rastro-quadro1-monde01-exibicao-v2.json'),
}


def caminho(cenario, chave):
    return OWNED/ARTEFATOS[cenario][chave]


def entradas_exibicao(preenchimento=0xa7, relogio=0x00123456, cursor=(0, 0), registradores=None,
                      ticks=TICKS_EXIBICAO, superficie=0, **base):
    import capturar_quadro_missao_original as cq
    from oraculo_exibicao_missao import EntradasExibicao
    return EntradasExibicao(quadro=cq.entradas_quadro(preenchimento, relogio, cursor, registradores, **base),
                            ticks=tuple(ticks), preenchimento_superficie=superficie,
                            proveniencia=PROVENIENCIA_EXIBICAO)


def bancada(cenario, preenchimento=0xa7, relogio=0x00123456, *, pulos=None, fronteiras=None, segundos=300,
            entradas_kw=None):
    """(bench, base EntradasNomeadas, named-input manifest) for a scenario."""
    entradas_kw = entradas_kw or {}
    if cenario == 'v1':
        import capturar_quadro_missao_original as cq
        from oraculo_quadro_missao import BancadaQuadroMissaoOriginal, FRONTEIRAS_QUADRO
        from oraculo_carga_missao import PULOS_INICIO
        q = cq.entradas_quadro(preenchimento, relogio, **entradas_kw)
        b = BancadaQuadroMissaoOriginal(q, segundos=segundos, pulos=pulos or PULOS_INICIO,
                                        fronteiras=fronteiras or FRONTEIRAS_QUADRO)
        return b, q.base, dict(m1=q.base.manifesto(), frame=q.manifesto())
    if cenario in ('exibicao', 'exibicao_v3'):
        from oraculo_exibicao_missao import BancadaExibicaoOriginal
        e = entradas_exibicao(preenchimento, relogio, **entradas_kw)
        v3 = cenario == 'exibicao_v3'
        # v3 executes LoadPie: MenuInit's menu pictures alone exceed 200,000 FileRead
        # resumptions (attempt 1 stopped there); budgets stay explicit and finite.
        limites = dict(segmentos=3000000, vinculos=3000000) if v3 else {}
        b = BancadaExibicaoOriginal(e, segundos=segundos, pulos=pulos, fronteiras=fronteiras, v3=v3, **limites)
        return b, e.quadro.base, dict(m1=e.quadro.base.manifesto(), frame=e.quadro.manifesto(), display=e.manifesto())
    raise ValueError(f'Unknown oracle scenario {cenario!r}')
