"""Frozen original inputs, real production delegates, optional fresh stopped/full x86."""
import argparse
import json
import hashlib
import subprocess
from pathlib import Path

from ambiente_ia_runtime import ROOT
from capturar_reinicio_ia import ARQUIVO, REGIOES_SEGMENTOS, _expandir, aplicar_delta, executar_nativo
from memoria_ia_runtime import MemoriaDeclarada
from oraculo_reinicio_ia import DADOS_BASE, ESTRUTURAS, imagem_base
from reinicio_ia import REGIOES_REINICIO, DependenciaIA
from reinicio_ia_compartilhado import ReinicioIACompartilhado, MundoUnidades, Mercado, Economia


def montar(imagem):
    """Fixture only: explicit aliases of the frozen original input, no adapter defaults."""
    mundo = MundoUnidades()
    mundo.unidades = imagem.unidades
    mundo.estruturas = imagem.vista(ESTRUTURAS, 276000)
    mundo.grupos = imagem.vista(0x51a9e0, 3200)
    mundo.grupo_em_iteracao = int.from_bytes(imagem.vista(0x51b844, 4), 'little')
    mundo.unidade_em_iteracao = int.from_bytes(imagem.vista(0x51b848, 2), 'little')
    economia = Economia()
    economia.memoria = imagem.vista(0x4e2ea8, 128)
    mercado = Mercado(economia)
    mercado.jogadores = imagem.jogadores
    memoria = MemoriaDeclarada(imagem.segmentos(), REGIOES_REINICIO + REGIOES_SEGMENTOS)
    return ReinicioIACompartilhado(memoria, mundo, mercado, imagem.vista(0x496fe4, 1),
                                 pesquisa64=imagem.vista(0x5080f4, 64))


def validar(emular=False):
    documento = json.loads(ARQUIVO.read_text())
    base, resultados = imagem_base(), []
    if emular:
        from inventario_ia_runtime import OriginalImage
        original = OriginalImage()
    for caso in documento['casos']:
        if caso['rotina'] != '0x0047f36e':
            continue
        inicial = aplicar_delta(base, _expandir(caso['imagem_inicial']))
        imagem = inicial.copia()
        provedor = montar(imagem)
        observacoes = _expandir(caso['observacoes'])
        esperado = [(o['nome'], o['sitio'], tuple(o['argumentos'])) for o in observacoes]
        parada, eax = None, None
        try:
            eax = provedor()
        except DependenciaIA as erro:
            parada = dict(name=erro.rotina, site=f'0x{erro.sitio:08x}')
        assert provedor.chamadas == esperado[:len(provedor.chamadas)], caso['caso']
        if parada is None:
            assert provedor.chamadas == esperado, caso['caso']
            assert imagem.hashes() == caso['final'], caso['caso']
            assert f'0x{eax:08x}' == caso['eax'], caso['caso']
        assert provedor.mundo.grupo_em_iteracao == int.from_bytes(imagem.vista(0x51b844,4),'little')
        assert provedor.mundo.unidade_em_iteracao == int.from_bytes(imagem.vista(0x51b848,2),'little')
        if emular:
            # On dependency the final attempted provider entry has not executed.
            antes = len(provedor.chamadas)-1 if parada else None
            nativo = executar_nativo(original, 0x47f36e, inicial, None, parar_antes=antes)
            assert imagem == nativo['imagem'], caso['caso']
            novas_chamadas = [(o['nome'],o['sitio'],tuple(o['argumentos'])) for o in nativo['observacoes']]
            assert novas_chamadas == (provedor.chamadas[:-1] if parada else provedor.chamadas), caso['caso']
            if not parada:
                assert eax == nativo['eax'], caso['caso']
        resultados.append(dict(case=caso['caso'], production_delegates=True, callback_replay=False,
                               complete=parada is None, dependency=parada, provider_calls=len(provedor.chamadas),
                               inherited_player_controls=list(inicial.jogadores[1::20]), iterator_aliases_equal=True,
                               original_provider_sequence_equal=True, final_image=imagem.hashes(),
                               fresh_native_image_equal=True if emular else None,
                               segments=nativo['segmentos'] if emular else None))
    assert len(resultados) == 11
    assert next(r for r in resultados if r['case']=='ia_reset_monde01')['complete']
    fontes = ('pesquisas-paralelas/ia-runtime/reinicio_ia_compartilhado.py',
        'pesquisas-paralelas/ia-runtime/reinicio_ia.py','pesquisas-paralelas/ia-runtime/memoria_ia_runtime.py',
        'ferramentas/ordens_unidades.py','ferramentas/consultas_unidades.py','ferramentas/emulador.py',
        'pesquisas-paralelas/missoes/consultas_missao.py','pesquisas-paralelas/economia/economia.py',
        'pesquisas-paralelas/economia/mercado.py','pesquisas-paralelas/combate/ataque_vivo.py',
        'pesquisas-paralelas/economia/consultas_reinicio_economia.py')
    return dict(native=emular, cases=resultados, whole_mission_load=False, actual_program_player_controls=False,
                base_revision=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),
                source_sha256={nome:hashlib.sha256((ROOT/nome).read_bytes()).hexdigest() if (ROOT/nome).is_file() else None
                               for nome in fontes},
                original_capture_sha256=hashlib.sha256(ARQUIVO.read_bytes()).hexdigest(),
                scope='Same frozen original inputs; real Core/Economy/Missions delegates and exact host aliases. Inherited fixture controls, no startup defaults.',
                unresolved_owner_primitives=['EnginGetEtat', 'EnginSetPlayer'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emular', action='store_true')
    parser.add_argument('--relatorio', type=Path, required=True)
    args = parser.parse_args()
    relatorio = validar(args.emular)
    args.relatorio.parent.mkdir(parents=True, exist_ok=True)
    args.relatorio.write_text(json.dumps(relatorio, indent=1)+'\n')
    print('Cases:', len(relatorio['cases']), 'complete:', sum(c['complete'] for c in relatorio['cases']),
          'named stops:', sum(not c['complete'] for c in relatorio['cases']))
