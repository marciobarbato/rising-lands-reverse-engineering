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
| `0x454530` | Acúmulo de recarga e limiares negativos |
| `0x475014`, `0x417909` | Contadores de ciclo, overflow e seleção de desenho |
| `0x4181a1` | Tratamento de F1–F4 para alterar divisor de desenho |
| `0x489728` | Gerador aleatório no caminho positivo, incluindo semente zero |
| `0x46d838`, `0x42d4f8` | Alianças direcionais, regiões sob unidades/estruturas e bordas |
| `0x42eba4`, `0x42ece0` | 1.501 cenários em duas variantes de passagem, com chamadas originais |
| `0x43ec0c`, `0x43eb64` | Máscaras, objeto 0xfd, ocupação própria e bordas |
| `0x43b2be`, `0x4704dc`, `0x4494fc` | Serialização de rotas, RNG separado e 256 contadores de espera |
| `0x47f927` | 450 cenários de orquestração, com as etapas internas substituídas |
| `0x43b30b`, `0x42f214`, `0x42e890` | Nove cenários sintéticos, chamadas originais sem substituição |

Cada chamada tem limite de um segundo e, por padrão, 20.000 instruções; um gancho recusa
saltos para fora dos trechos autorizados. O verificador exige alcançar uma
parada declarada, de modo que timeout ou limite de instruções não contam como sucesso.
As comparações usam bytes do original, não assembly recompilado a partir da
mesma fórmula Python — isso reduz o risco de um teste repetir o erro da implementação.

As restrições não substituem o sandbox do sistema: são limites funcionais da
bancada. A equivalência é local às entradas e aos trechos examinados. Ainda
será necessário confrontar uma partida real para validar a simulação integrada.

## Escopo das novas bancadas

A suíte possui 104 testes; a execução emulada registra 23.501 chamadas delimitadas.
O teste de IA em `test_emulacao_caminhos_ia.py` intercepta apenas sete endereços
explícitos de etapas e injeta retornos. Valida o despachante e seus argumentos,
mas não o conteúdo dessas etapas. Essa diferença é deliberada e registrada em
[IA.md](IA.md); não constitui validação da IA completa.

`python3 ferramentas/bancada_caminhos.py` reproduz nove cenários e grava
`relatorios/caminhos-experimentos.json`. Esse experimento executa as chamadas
originais de preparação, busca e pós-processamento, mas fornece grades sintéticas.
Rotas curtas ou sucesso do buscador não equivalem à chegada da unidade; veja
[CAMINHOS.md](CAMINHOS.md). A suíte também reproduz o relatório e confere
adjacência, limites e células bloqueadas nas rotas emitidas.

A bancada agora configura descritores de segmentos x86 planos de 32 bits.
Isso permite executar as rotinas de strings do Watcom que copiam DS para ES,
sem depender de seletores nulos implícitos do Unicorn. Não adiciona APIs Windows
nem permite memória além das regiões mapeadas e intervalos de código declarados.

A bancada `bancada_tarefas.py` compara criação, espera, subtarefas, conclusão e
reutilização com a tabela inteira de 100 tarefas (9.600 bytes), contextos e
contador global. Suas chamadas de listas e operações nativas não são substituídas.
Também foram conferidos os 140 nomes do RULE com o resolvedor x86 e a âncora
`_debugGetPC`, usando uma entrada do SBL por chamada para respeitar o limite
de 20.000 instruções. Detalhes em [TAREFAS.md](TAREFAS.md).

## Ordens de movimento com efeitos

A bancada `bancada_ordens.py` estende a máquina de tarefas com os intervalos
originais de `V_DeplacerUnite`, `V_DeplaceGroupe`, consultas, `ResetOrdre`,
`SetDeplaceEngin`, teste de caixa, liberação de estrutura e percurso de grupo.
Os dez testes diferenciais novos executam todas essas chamadas sem interceptá-las.

São comparados os registros completos de unidades, estruturas e grupos, a grade
de objetos, os globais de busca/iteração e, na integração, tarefas e listas.
A extensão acrescentou 1.584 chamadas à suíte. A demonstração opcional gera um
relatório separado com outras 15 chamadas; elas não entram na contagem da suíte.
Veja [ORDENS_MOVIMENTO.md](ORDENS_MOVIMENTO.md) para casos e limites. A emissão
da ordem não executa a física, visão ou chegada da unidade.

## Avanço físico, visão e mensagens

`bancada_avanco.py` acrescenta os intervalos de avanço, ocupação, visão, minimapa,
fadiga, conclusão do estado 2, percurso da rota e entrega de mensagens. Para
as chamadas mais longas de visão/percurso, declara explicitamente um máximo de
1.000.000 de instruções, mantendo o limite de um segundo e a lista de intervalos.
As demais chamadas conservam o padrão de 20.000 instruções.

Os oito testes diferenciais novos e quatro testes do coordenador acrescentaram
650 chamadas à suíte. A comparação do trajeto completo usa as funções originais
em sequência, com paradas declaradas nos ramos do despacho ainda não traduzidos;
não executa o ciclo de partida inteiro. Não substitui chamadas internas.

`demonstrar_chegada.py --emular` gera um relatório separado com 104 execuções,
que não entram na contagem da suíte. Veja [AVANCO_CHEGADA.md](AVANCO_CHEGADA.md)
para a distinção entre célula atravessada, destino final e mensagem recebida.
