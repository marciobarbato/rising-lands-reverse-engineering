"""Original-only whole-remap observations; refuses to overwrite any capture."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import time
import zlib

from cenarios_conclusao_remapeamento import CASOS_CONCLUSAO, preparar_conclusao

RAIZ = Path(__file__).resolve().parents[1]


def blocos(dados):
    return {a: dict(size=len(b), sha256=hashlib.sha256(b).hexdigest(),
                    zlib_base64=base64.b64encode(zlib.compress(b)).decode('ascii'))
            for a, b in dados.items()}


def capturar(nomes, destino):
    if destino.exists():
        raise FileExistsError(f'Preserve existing original-only observation: {destino}')
    from bancada_conclusao_remapeamento import BancadaConclusaoRemapeamento, REGISTRADORES_CHAMADOR
    from emulador import HASH_ORIGINAL, x86, unicorn
    from vinculos_declarados import ParadaVinculoDeclarado
    b = BancadaConclusaoRemapeamento()
    documento = dict(original_sha256=HASH_ORIGINAL, translation_executed=False,
                     scope='Whole unpatched Chemin_Remap over explicit inherited fixtures and five declared resource imports; no MissionLoad',
                     cases=[], capture_completed_as_expected=False)
    inicio = time.monotonic()
    falha_inesperada = False
    for nome in nomes:
        mundo, fonte = preparar_conclusao(nome)
        b.carregar_conclusao(mundo, nome)
        antes = b.imagem_inteira()
        execucoes, retomadas, lacos = b.execucoes, b.retomadas_vinculos, b.retomadas_laco
        comeco = time.monotonic()
        observado = dict(name=nome, source=fonte, initial=blocos(antes))
        try:
            regs = b.concluir_original()
            observado.update(outcome='original_return', eax=hex(regs['EAX']), consumed_al=regs['EAX'] & 255)
            if nome in ('component_lock_unavailable', 'component_lock_null', 'cleanup_unavailable'):
                falha_inesperada = True
            if any(regs[n] != v for n, v in REGISTRADORES_CHAMADOR.items() if n != 'EAX'):
                falha_inesperada = True
        except ParadaVinculoDeclarado as erro:
            observado.update(outcome='declared_fixture_stop', exception_type=type(erro).__name__, reason=str(erro))
            esperado = {'component_lock_unavailable': ('GlobalLock', '0x42efd1'),
                        'cleanup_unavailable': ('GlobalUnlock', '0x42ef5d')}.get(nome)
            evento = b.vinculos_declarados.eventos[-1]
            if esperado is None or (evento['name'], evento['caller_return']) != esperado:
                falha_inesperada = True
        except Exception as erro:
            observado.update(outcome='native_or_harness_failure', exception_type=type(erro).__name__, reason=str(erro))
            # A literal NULL from the second lock is deliberately offered to
            # observe the unchecked original store, not declared successful remap.
            if (nome != 'component_lock_null' or not isinstance(erro, unicorn.UcError)
                    or erro.errno != unicorn.UC_ERR_WRITE_UNMAPPED
                    or b.cpu.reg_read(x86.UC_X86_REG_EIP) != 0x42efd9):
                falha_inesperada = True
            else:
                observado.update(outcome='expected_original_null_lock_fault', native_error_number=erro.errno)
        observado.update(final=blocos(b.imagem_inteira()), native_state=b.estado_conclusao(),
                          bounded_segments=b.execucoes-execucoes,
                          binding_resumptions=b.retomadas_vinculos-retomadas,
                          preserved_loop_resumptions=b.retomadas_laco-lacos,
                          seconds=time.monotonic()-comeco,
                          esp=hex(b.cpu.reg_read(x86.UC_X86_REG_ESP)))
        observado['expected_observation'] = not falha_inesperada
        documento['cases'].append(observado)
        print(nome, observado['outcome'], observado['bounded_segments'], flush=True)
        if falha_inesperada:
            break
    documento.update(capture_completed_as_expected=not falha_inesperada and len(documento['cases']) == len(nomes),
                     original_returns=sum(c['outcome'] == 'original_return' for c in documento['cases']),
                     original_success_al_returns=sum(c.get('consumed_al') == 1 for c in documento['cases']),
                     declared_resource_stops=sum(c['outcome'] == 'declared_fixture_stop' for c in documento['cases']),
                     expected_original_null_lock_faults=sum(c['outcome'] == 'expected_original_null_lock_fault' for c in documento['cases']),
                     seconds=time.monotonic()-inicio, original_entries=dict(b.origens_conclusao),
                     bounded_segments=b.execucoes, binding_resumptions=b.retomadas_vinculos,
                     preserved_loop_resumptions=b.retomadas_laco,
                     maximum_segment_instructions=getattr(b, 'maximo_instrucoes', None),
                     failed_native_segment=getattr(b, 'ultima_falha', None),
                     import_resolutions=b.importacoes_declaradas)
    with destino.open('x') as arquivo:
        arquivo.write(json.dumps(documento, indent=2)+'\n')
    return documento


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--casos', nargs='+', choices=CASOS_CONCLUSAO, default=CASOS_CONCLUSAO)
    p.add_argument('--relatorio', type=Path, default=Path('relatorios/capturas-conclusao-remapeamento-original.json'))
    args = p.parse_args()
    destino = args.relatorio if args.relatorio.is_absolute() else RAIZ/args.relatorio
    raise SystemExit(0 if capturar(args.casos, destino)['capture_completed_as_expected'] else 1)
