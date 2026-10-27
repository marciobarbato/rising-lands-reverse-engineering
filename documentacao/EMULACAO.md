# Validação diferencial com instruções x86

O Ghidra ajuda a localizar rotinas e interpretar dados. Para conferir a
reconstrução, a bancada [`emulador.py`](../ferramentas/emulador.py) carrega seções
do **executável original identificado por hash** no Unicorn 2.1.4 e executa
somente os intervalos declarados pelo teste, com memória e registradores sintéticos.

Essa etapa complementa a análise estática: executa instruções de rotinas isoladas,
mas não inicia o executável Windows, não resolve imports, não oferece Win32,
não cria uma partida e não executa a cópia normalizada do Ghidra.

## Reproduzir

```sh
python3 -m pip install --no-cache-dir --target .local/python -r requirements-emulacao.txt
python3 ferramentas/validar.py --emular
```

No sandbox desta sessão, a criação de memória JIT do Unicorn provocou `SIGILL`
no macOS. A mesma bancada funciona com a execução autorizada fora dessa restrição.
Nenhuma alteração global de segurança foi aplicada. A biblioteca fica em
`.local/python`, dentro do repositório. Distribuição oficial:
[Unicorn no PyPI](https://pypi.org/project/unicorn/2.1.4/).

Sem Unicorn ou sem permissão para JIT:

```sh
python3 ferramentas/validar.py
# Ou, sem gerar relatório:
sh testar.sh
```

Os testes de emulação ficam explicitamente ignorados por padrão. A execução
completa também pode ser solicitada por `RISING_EMULAR=1 sh testar.sh`.
Os relatórios `validacao-local.json` e `validacao-emulada.json` registram testes,
falhas, erros, motivos de testes ignorados e número de execuções x86 delimitadas.

## Cobertura

| Rotina/trecho | Verificação |
|---|---|
| `0x457122` | Cura: 2.000 entradas determinísticas aleatórias e três casos de limite |
| `0x477042`, `0x479555` | Direção e distância: 1.024 pares para cada função |
| `0x4770ee` | Vizinhos: interiores, cantos, bordas, dimensões 1..256 e direções pares |
| `0x448599`, `0x4490fd` | Giro e permissão de avanço: todas as combinações de 16 direções |
| `0x448704` | Prefixo do passo: 1.024 casos, incluindo overflow e desconto |
| `0x457350` | Quatro parâmetros de movimento em todos os 26 ramos de tipo |
| Trechos de `0x4502f0` | Adições, redução e aplicação de dano, incluindo zero com proteção |
| `0x4500e4` | Consulta de proximidade com tipos, donos e distâncias diferentes |

Cada chamada tem limite de um segundo e 20.000 instruções; um gancho recusa
saltos para fora dos trechos autorizados. O verificador exige alcançar uma
parada declarada, de modo que timeout ou limite de instruções não contam como sucesso.
As comparações usam bytes do original, não assembly recompilado a partir da
mesma fórmula Python — isso reduz o risco de um teste repetir o erro da implementação.

As restrições não substituem o sandbox do sistema: são limites funcionais da
bancada. A equivalência é local às entradas e aos trechos examinados. Ainda
será necessário confrontar uma partida real para validar a simulação integrada.
