# Portões: comandos, colisão e passagem de unidades

Esta etapa traduz os **efeitos de simulação** dos portões. Mantém o contador
`+0x76`, decide quando iniciar transições e modifica atributos/regiões nos pontos
observados no x86. Não associa sprites, quadros CMP, paletas ou FPS. A frente de
gráficos continua separada; nenhuma de suas implementações foi alterada.

## Rotinas e contrato

| Original francês | Endereço | Tradução |
|---|---|---|
| `HerseEnAnimation` | `0x4191fd` | `portao_em_transicao` |
| `HerseEstBaisser` | `0x41934f` | `portao_na_fase15` |
| `HerseEstLever` | `0x419379` | `portao_na_fase0_31` |
| `HerseEstFace` | `0x4193ac` | `portao_horizontal` |
| `BaisseTouteHerse` | `0x4193d4` | `solicitar_liberacao_portoes` |
| `RemonteTouteHerse` | `0x4195ca` | `solicitar_bloqueio_portoes` |
| `ChercheEtatHerse` | `0x419917` | `alternar_portoes` |
| `BatimentNextEtape`, tipo 12 | `0x427bb7..0x427d5d` | `avancar_estado_portao` |

O código está em [`portoes.py`](../ferramentas/portoes.py). Os índices u16 são
limitados aos 1.000 registros de 276 bytes. `avancar_estado_portao` exige tipo 12;
os predicados e comandos auxiliares não inventam esse filtro para os registros
que o original consulta. A célula é `x + 256*y`.

Os 11 trechos de evidência, incluindo prólogo e epílogos compartilhados, estão
no [manifesto](../evidencias/portoes/manifesto.json). A entrada do tipo 12 na
tabela de `BatimentNextEtape` foi conferida em `0x4268ac`, com destino `0x427bb7`.
O SHA-256 do EXE original permanece
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

```sh
python3 -B ferramentas/extrair_portoes.py
python3 -B ferramentas/demonstrar_portoes.py
python3 -B ferramentas/validar.py
python3 -B ferramentas/validar.py --emular
```

Execute na raiz da worktree `engenharia-reversa-nucleo`, branch
`codex/nucleo-construcoes`. O extrator usa Capstone. A demonstração funciona
apenas em Python; a validação diferencial usa o original e Unicorn/JIT.

## Contador e efeitos físicos

O contador é um byte no registro da estrutura, não um ID de sprite. Os
predicados consideram 0, 15 e 31 estáveis. Outros valores são transição.
O teste de orientação usa o **u16 inteiro** em `+0x7c`: zero é horizontal;
qualquer outro valor segue o ramo vertical.

`alternar_portoes(celula, indice)` ignora o pedido se o registro de referência
estiver em transição. Se ele estiver em 15, chama o pedido de bloqueio; em 0/31,
chama o pedido de liberação. Os auxiliares diretos reproduzem as rotinas internas
sem acrescentar essa guarda em todos os membros do conjunto.

`avancar_estado_portao(indice)` incrementa o byte somente em transição. O
incremento é u8; se o resultado for pelo menos 31, escreve zero. Portanto 255
também volta a zero por overflow, e valores brutos altos não são tratados como
novos quadros visuais.

| Transição observada | Efeito no terreno |
|---|---|
| Alcançar 15 | Limpar bit 0 dos atributos; remover o rótulo do portão e atualizar as cores |
| Voltar a zero | Ativar bit 0; inserir novamente o rótulo e atualizar as cores |
| Permanecer em 0, 15 ou 31 | Não reparar nem normalizar atributos/regiões por conta própria |

As regiões usam os modos 1/3 de `Chemin_ModifieZone`, com o slot zero em `+0xcc`.
Durante um ciclo coerente, a passagem só é liberada ao alcançar 15 e volta a ser
bloqueada ao retornar a zero. Não se convertem as chamadas em segundos nem se
assume que o desenho consome cada valor do contador.

## Pedidos para um conjunto de portões

Os comandos usam `objeto_portao`, cujo valor inicial é 253, e a orientação do
registro fornecido. Eles percorrem uma linha de objetos, sem acrescentar filtros
de dono ou atividade que não existem nesses corpos originais.

### Pedido de liberação

`BaisseTouteHerse` caminha primeiro para oeste/norte e depois percorre a linha
para leste/sul. Cada célula com objeto de portão e rótulo de estrutura incrementa
o byte `+0x76` do índice extraído do rótulo. Não exige que o registro encontrado
seja tipo 12 nem que seu contador já esteja estável.

A rotina para antes de processar a última coluna/linha quando a varredura
alcança o valor 255. Isso foi comparado diretamente; não se substituiu essa
sequência por um percurso geométrico simétrico.

### Pedido de bloqueio

`RemonteTouteHerse` usa uma lista de 255 palavras. A sequência conserva os
testes do x86: no percurso vertical de ida, o teste de parada continua usando
a coluna; no retorno horizontal, a coluna zero encerra a coleta, podendo incluir
o começo da linha seguinte. Os slots que não forem sobrescritos permanecem na
lista; podem conter posições repetidas.

Antes de alterar qualquer contador, consulta o bit 0 dos atributos de **todas**
as posições válidas da lista. Se uma estiver bloqueada/ocupada, retorna sem
iniciar o fechamento de nenhum membro. Essa consulta inclui a reserva de passo
que o movimento já marca nos atributos.

Se a lista estiver livre, percorre os 1.000 registros e compara suas origens
com os slots. Esse caminho não usa o rótulo de regiões nem filtra tipo, dono ou
atividade. Posições repetidas podem incrementar o mesmo registro mais de uma
vez; a tradução conserva esse efeito. Grupos que excedam o armazenamento útil
de 255 slots são recusados na API, sem presumir o comportamento de corrupção
da pilha original.

As leituras de objetos continuam lineares. Quando exigem bytes antes ou depois
da grade de 65.536 posições, a API mantém a recusa explícita descrita em
[COLOCACAO_ESTRUTURAS.md](COLOCACAO_ESTRUTURAS.md), sem envolver índices negativos.

## Separação entre simulação, entrada e gráficos

O chamador fornece célula e índice já resolvidos. A escolha pelo cursor,
`HerseSousCurseur` e o consumo da ação de mouse não foram implementados aqui.
A bancada executa o prólogo, o despacho real do tipo e o ramo de avanço com a
entrada de mouse desativada por um valor de entrada em `0x5099af`.

O consumidor da simulação pode chamar:

```python
mundo.alternar_portoes(celula, indice)  # pedido já selecionado pelo chamador
mundo.avancar_estado_portao(indice)    # uma atualização de simulação
```

O contador resultante pode ser entregue ao renderizador futuramente, sob o
contrato gráfico que essa frente definir. Esta implementação não desenha nem
deduz correspondência CMP. A ordem global de atualização e a seleção de
estruturas ativas continuam responsabilidade do despachante completo.

## Demonstração e comparação

[`portoes-python.json`](../relatorios/portoes-python.json) registra uma unidade
atravessando o portão em `(6,5)` e chegando a `(10,4)`, com mensagem e conclusão
da tarefa. O cenário termina em **169 atualizações**, com a seguinte sequência:

| Atualização | Ação ou efeito |
|---:|---|
| 0 | Pedido inicia contador 1 |
| 14 | Contador chega a 15; colisão e rótulo são removidos |
| 87 | Pedido de fechamento recusado enquanto a passagem está ocupada/reservada |
| 121 | Passagem livre; pedido inicia contador 16 |
| 136 | Retorno a zero; bloqueio e rótulo são inseridos |

A bancada executa os corpos originais, com chamadas internas de atributos,
regiões e cores preservadas. A varredura de 1.000 registros usa checkpoints a
cada 32 registros, conservando a pilha e os registradores. Cada trecho mantém
os limites de um milhão de instruções e um segundo. As contagens de execuções
delimitadas não equivalem à quantidade de comandos de portão.

Os testes cobrem os 256 valores do contador, quatro predicados, bits de colisão,
grupos horizontais/verticais, ocupação, registros sem filtro adicional, resíduos
da lista e condições de borda. Conferem registros e grades completos. No trajeto,
também comparam cada atualização de movimento e a memória de tarefas. Um teste
reproduz o relatório com os imports de emulação bloqueados.
A suíte completa passou com **226 testes e 49.305 execuções x86 delimitadas**,
sem falhas, erros ou testes ignorados. Sem emulação, passam 113 testes e os
113 opcionais ficam explicitamente ignorados. Os 52 arquivos originais dos
manifestos foram conferidos por tamanho e SHA-256.
Os relatórios gerais do núcleo estão em [validação emulada](../relatorios/validacao-emulada.json)
e [validação local](../relatorios/validacao-local.json), sem somar as pesquisas paralelas.

## Continuidade

Ainda faltam a entrada completa de mouse, o despacho global e sua frequência,
as associações gráficas dos portões e a validação em missão real. Os comandos
e o avanço físico podem ser integrados sem importar os módulos da frente
gráfica. O contrato desta etapa não completa construção, demolição, economia
ou o carregamento/remapeamento integral do mundo.
