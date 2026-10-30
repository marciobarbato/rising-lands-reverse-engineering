"""Export intact transport instructions and hunger checks; never execute a translation.

Run with ``python3 -B pesquisas-paralelas/economia/extrair_transporte.py``.
The existing extractor supplies the hash-checked original PE reader and the
mechanical Capstone/manifest writer. Its predecessor output is not changed.
"""
from pathlib import Path

import extrair_ciclo_trabalho as exportador


def extrair():
    anteriores = exportador.SAIDA, exportador.INTERVALOS, exportador.TABELAS
    try:
        exportador.SAIDA = Path(__file__).resolve().parent / 'evidencias/transporte'
        exportador.INTERVALOS = (
            ('CalculDechargeCaveEngin', 0x44e35c, 0x44ea67),
            ('EnginCalculTransporte and shared epilogue', 0x44ea78, 0x44f2a3),
            ('CalculTransporteEngin', 0x44f2d4, 0x44f8a7),
            ('shared register restore', 0x440d58, 0x440d5e),
            ('EnginNextEtape saved-state checks', 0x454c93, 0x455554),
            ('EnginNextEtape target-release continuation', 0x4567b7, 0x4567ce),
        )
        exportador.TABELAS = (
            ('CalculDechargeCaveEngin phases', 0x44e34c, 4),
            ('EnginCalculTransporte phases', 0x44ea68, 4),
            ('CalculTransporteEngin types 11..17', 0x44f2a4, 7),
            ('CalculTransporteEngin vehicle phases', 0x44f2c0, 5),
        )
        return exportador.extrair()
    finally:
        exportador.SAIDA, exportador.INTERVALOS, exportador.TABELAS = anteriores


if __name__ == '__main__':
    print('Exported intervals:', len(extrair()['intervals']))
