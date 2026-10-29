"""CalculGame 0x42c868 in-game frame body 0x42d2de..0x42d4f5, in original order.

``calcular_quadro(memoria, provedores)`` runs one frame body over an explicit
``MemoriaDeclarada``. Every global it touches is read or written at its original
width (``REGIOES_QUADRO``). Each callee is taken from ``provedores``, keyed by its
original SBL name, and called with keyword arguments at the original register
widths plus ``sitio`` (the original CALL address). A callee the caller did not
provide raises ``DependenciaIA(name, call site)``, and every store made before it
is retained. Nothing is defaulted.

The following bodies are reproduced here from their intact bytes:
- PlayerAttaqueReset 0x46d628, a one-byte ``ret`` with no effect;
- GameNextFrame 0x45d015, ``inc dword [0x496d40]``;
- CalculNextReflect 0x47fbea, which masks the player and mission bytes, runs
  iaCalculPlayer 0x47f927 through Core's ``ia.atualizar_ia`` and returns AL = 1.
  The AI context bytes 0x51a990/0x51a995 + 16p are written back even when a
  kernel provider is missing; the original stores the counter before its
  iagUnitDeleteAllGroups call and the inactive byte after it.

The returned dict holds the exit address (0x42d4e2, 0x42d4ea, or 0x42c92c for
the end-of-mission MenuInit tail) and the ordered calls with their arguments.
"""
from ia import EstadoIA, atualizar_ia
from memoria_ia_runtime import s32
from reinicio_ia import DependenciaIA

SAIDA_LIMPA, SAIDA_EPILOGO, SAIDA_MENU_FIM = 0x42d4e2, 0x42d4ea, 0x42c92c
REGIOES_QUADRO = (
    (0x496d40, 0x496d44, 'GameNextFrame counter'),
    (0x4e05a0, 0x4e05a1, 'TestFinDeMission result'),
    (0x4e061c, 0x4e0620, 'end-of-mission frame counter'),
    (0x4e0730, 0x4e0731, 'network flag'),
    (0x4e1928, 0x4e1930, 'unit counters per owner (read by iaCalculPlayer)'),
    (0x4e1c18, 0x4e1d19, 'CD track table and its index'),
    (0x4e2480, 0x4e2481, 'ProcessInputGame local player copy'),
    (0x4e2f28, 0x4e2f29, 'CD music off flag'),
    (0x4e2f78, 0x4e2f79, 'game state'),
    (0x4dfaa8, 0x4dfab8, 'structure counters per owner (read by iaCalculPlayer)'),
    (0x508041, 0x508042, 'local player'),
    (0x508720, 0x508724, 'view origin'),
    (0x5099b0, 0x5099b1, 'frame-exit flag'),
    (0x51a98c, 0x51a9dc, 'AI player contexts 0..4'),
)
# iaCalculPlayer call sites per callee; iaSolver differs for the monster player.
SITIOS_IA = {0x47b283: ('AvanceMonstre', 0x47f939), 0x483d95: ('iagUnitDeleteAllGroups', 0x47f9ad),
             0x482936: ('iagUnitNoyau', 0x47f9df), 0x48453c: ('iagVilleNoyau', 0x47f9ea),
             0x485183: ('iagRessNoyau', 0x47f9f5), 0x4866d7: ('iagWarNoyau', 0x47fa02)}
ARGUMENTOS_IA = {0x4866d7: ('jogador', 'missao'), 0x47d314: ('contexto',)}


class Quadro:
    def __init__(self, memoria, provedores):
        self.memoria, self.provedores, self.chamadas = memoria, provedores, []

    def chamar(self, rotina, sitio, **argumentos):
        self.chamadas.append(dict(sitio=sitio, rotina=rotina, **argumentos))
        provedor = self.provedores.get(rotina)
        if provedor is None:
            raise DependenciaIA(rotina, sitio)
        return provedor(sitio=sitio, **argumentos)

    def calcul_next_reflect(self, jogador, missao):
        """CalculNextReflect 0x47fbea: AL = 1 regardless of iaCalculPlayer's EAX."""
        m = self.memoria
        jogador, missao = jogador & 0xff, missao & 0xff
        self.chamadas.append(dict(sitio=0x42d35d, rotina='CalculNextReflect', jogador=jogador, missao=missao))
        contexto = 0x51a98c + 16 * jogador
        # Reads in the original order, and only where the original reads: player 4 reads none of
        # these (0x47f939); an inactive player reads only its inactive byte (0x47f96c); the
        # unit counter is read only when the structure counter is 0, and the empty-cycle byte
        # only when both are 0 (0x47f998). atualizar_ia does not consume the values it skips.
        estado, estruturas, unidades = EstadoIA(), 0, 0
        if jogador < 4:
            estado.inativo = m.u8(contexto + 4)
            if not estado.inativo:
                estruturas = m.u32(0x4dfaa8 + 4 * jogador)
                if estruturas == 0:
                    unidades = m.u16(0x4e1928 + 2 * jogador)
                    if unidades == 0:
                        estado.ciclos_sem_efetivo = m.u8(contexto + 9)

        def kernel(endereco, *valores):
            if endereco == 0x47d314:
                rotina, sitio = 'iaSolver', 0x47f945 if jogador == 4 else 0x47fa12
            else:
                rotina, sitio = SITIOS_IA[endereco]
            nomes = ARGUMENTOS_IA.get(endereco, ('jogador',))
            return self.chamar(rotina, sitio, **dict(zip(nomes, valores)))

        ativo = jogador < 4 and not estado.inativo
        try:
            atualizar_ia(jogador, missao, estado, estruturas, unidades, kernel)
        finally:
            # The original stores the counter (0x47f998 inc / 0x47f9c0 clear) for every
            # active player and the inactive byte only on the tenth empty cycle (0x47f9d4).
            if ativo:
                m.u8(contexto + 9, estado.ciclos_sem_efetivo)
                if estado.inativo:
                    m.u8(contexto + 4, estado.inativo)
        return 1


def calcular_quadro(memoria, provedores):
    q = Quadro(memoria, provedores)
    m = memoria

    def fim(endereco):
        if endereco == SAIDA_LIMPA:
            m.u8(0x5099b0, 0)
        return dict(saida=endereco, chamadas=q.chamadas)

    q.chamadas.append(dict(sitio=0x42d2de, rotina='PlayerAttaqueReset'))   # 0x46d628: ret
    if q.chamar('EvenementEnCours', 0x42d2e3) & 0xff:
        return fim(SAIDA_EPILOGO)
    if m.u8(0x4e2f28) == 0:
        indice = m.u8(0x4e1d18)
        faixa = 2 + m.u8(0x4e1c18 + indice) % 2
        m.u8(0x4e1d18, indice + 1)
        q.chamar('MCICD_Play', 0x42d328, faixa=faixa, edx=0)
    rede = m.u8(0x4e0730)
    local = m.u8(0x508041)
    for jogador in range(4 if rede else 5):
        tipo = q.chamar('PlayerGetType', 0x42d379, jogador=jogador) & 0xff
        if tipo == 1:
            if jogador == local:
                q.chamar('InputGame', 0x42d33b, jogador=jogador)
                q.chamar('InputSend', 0x42d342, jogador=jogador)
            else:
                q.chamar('InputReceive', 0x42d34b, jogador=jogador)
        elif tipo == 2:
            missao = q.chamar('MissionGetNum', 0x42d354) & 0xff
            q.calcul_next_reflect(jogador, missao)
            if jogador == local:
                q.chamar('InputGame', 0x42d36c, jogador=jogador)
    m.u8(0x4e2480, local)
    for jogador in range(4):
        q.chamar('ProcessInputGame', 0x42d3b0, jogador=jogador)
    estado = m.u8(0x4e2f78)
    if not (estado == 0x12 or (estado == 0x10 and m.u8(0x4e0730))):
        return fim(SAIDA_LIMPA)
    q.chamar('MessageBoxCalcul', 0x42d3e1)
    q.chamadas.append(dict(sitio=0x42d3e6, rotina='GameNextFrame'))
    m.u32(0x496d40, m.u32(0x496d40) + 1)
    for sitio, rotina in ((0x42d3eb, 'CalculIconeAction'), (0x42d3f0, 'ProjectileCalcul'),
                          (0x42d3f5, 'CalculEnginNextEtape'), (0x42d3fa, 'CalculBatimentNextEtape'),
                          (0x42d3ff, 'RechercheCalcul'), (0x42d404, 'PlayerInitAllianceCompteur'),
                          (0x42d409, 'SetUpdateChamp'), (0x42d40e, 'UpdateChamp'), (0x42d413, 'CalculMatiere')):
        q.chamar(rotina, sitio)
    q.chamar('CalculCompteurMarche', 0x42d41f, jogador=m.u8(0x508041))
    q.chamar('CalculCompteurProposition', 0x42d42d, jogador=m.u8(0x508041), edx=0)
    q.chamar('NextAnimTerrain', 0x42d441, x=m.u16(0x508720), y=m.u16(0x508722))
    if m.u8(0x4e0730):
        q.chamar('NextAnimVegetFullMap', 0x42d44f)
    else:
        q.chamar('NextAnimVeget', 0x42d467, x=m.u16(0x508720), y=m.u16(0x508722))
    q.chamar('PlayerAttaqueCalculSympa', 0x42d46c)
    if m.u8(0x4e0730):
        return fim(SAIDA_LIMPA)
    resultado = q.chamar('TestFinDeMission', 0x42d481, jogador=m.u8(0x508041)) & 0xff
    m.u8(0x4e05a0, resultado)
    if not resultado:
        return fim(SAIDA_LIMPA)
    if q.chamar('MissionGetNum', 0x42d48f) & 0xffff == 6 and m.u32(0x4e061c) == 0:
        q.chamar('MessageBoxSet', 0x42d4b1, mensagem=10, duracao=500)
    contador = (m.u32(0x4e061c) + 1) & 0xffffffff
    m.u32(0x4e061c, contador)
    if s32(contador) < 100:     # jl 0x42d4e2: signed compare
        return fim(SAIDA_LIMPA)
    q.chamar('PlaySnd_StopAllSound', 0x42d4c8)
    q.chamar('MenuInit', 0x42c931, jogador=m.u8(0x508041), estado=0x13, ecx=contador)
    m.u8(0x5099b0, 0)       # the tail jumps back to 0x42d4e2
    return dict(saida=SAIDA_MENU_FIM, chamadas=q.chamadas)
