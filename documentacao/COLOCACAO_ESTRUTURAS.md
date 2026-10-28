# Colocação de estruturas, muros e portões

Esta etapa traduz `PlaceBatiment` e seus auxiliares locais, continuando o
[tratamento do terreno](TERRENO_ESTRUTURAS.md). O chamador agora pode fornecer
um registro preparado e deixar a tradução escolher o primeiro tile do tipo,
ou seguir o caminho específico de muro/portão, conforme o original.

O trabalho foi feito no branch **`codex/nucleo-construcoes`**, a partir de
`3f5c84f12141d9c327a5256aa233ace77aa2035e`, numa worktree própria chamada
`engenharia-reversa-nucleo`. O checkout de `main` e as pesquisas paralelas
permanecem separados. Não houve merge das outras frentes nem alteração de
seus arquivos.

## Rotinas e evidências

| Original francês | Endereço | Tradução Python |
|---|---|---|
| `ValideHerse` | `0x41ac8b` | `validar_portao` |
| `ChercheMurCombinaisons` | `0x41c18a` | `combinacao_muro` |
| `SetMurAllentour` | `0x41c251` | `atualizar_muros_vizinhos` |
| `PlaceBatiment` | `0x41c4ac` | `colocar_estrutura` |

O código está em [`colocacao_estruturas.py`](../ferramentas/colocacao_estruturas.py).
[`manifesto.json`](../evidencias/colocacao-estruturas/manifesto.json) contém os
quatro intervalos, hashes, a tabela de saltos em `0x41c454`, os destinos por tipo
e os primeiros tiles extraídos dos ramos. Os bytes iniciais dos IDs de objetos
em `0x495bf8/0x495bf9` também foram registrados: muro **254**, portão **253**.
O SHA-256 do EXE original continua
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

```sh
python3 -B ferramentas/extrair_colocacao_estruturas.py
python3 -B ferramentas/demonstrar_colocacao_estruturas.py
python3 -B ferramentas/validar.py
python3 -B ferramentas/validar.py --emular
```

Os comandos devem ser executados na raiz desta worktree. Somente o extrator
precisa de Capstone; a execução Python e a demonstração não dependem de EXE,
Unicorn ou JIT. A comparação diferencial exige o original e Unicorn/JIT.

## Contrato de colocação

`mundo.colocar_estrutura(indice, mascara_tipo20=None)` usa a célula de origem
u16 em `+0x02` e o tipo em `+0x08`, nos registros de 276 bytes. Não exige um
predicado adicional de atividade, não escolhe um slot livre e não altera dono
ou estado. O índice é truncado a u16 e limitado aos 1.000 registros; o domínio
de tipos implementado é 0..21.

Para os tipos diferentes de 9 e 12, seleciona o primeiro tile pela tabela
original e chama a aplicação de terreno já traduzida. Por exemplo, o tipo 0
começa em `0x2fa`, o tipo 1 em `0x2be` e os tipos 15/20 em `0x3c3`. A aplicação
percorre o retângulo, preserva slots compactos e segue o contrato anterior.
O tipo 20 continua exigindo os 20 bytes de sua máscara em RAM; a colocação não
substitui esses dados pela máscara estática.

Os IDs de objetos são entradas explícitas do mundo, `objeto_muro` e
`objeto_portao`, com os valores iniciais extraídos do EXE. As consultas e a
bancada preservam o byte baixo caso sejam fornecidos outros valores.

### Muro, tipo 9

1. Calcular a combinação com base nos objetos vizinhos e no objeto atual.
2. Guardá-la como u16 em `+0x7c`.
3. Escrever o objeto de muro na célula de origem.
4. Ativar somente o bit 0 dos atributos, pela máscara **1**.
5. Inserir o rótulo de estrutura com slot 0 por `Chemin_ModifieZone`, modo 3.

Esse caminho conserva o tile. O literal 3 no registrador `EBX` serve ao modo
de modificação de região; a máscara de atributos transmitida em `EDX` é 1.
O diferencial do trajeto verificou essa distinção com o bit 1 previamente zerado.

A consulta de combinação considera muro **ou portão** nos vizinhos, com bits
oeste=8, sul=4, leste=2 e norte=1. Devolve a combinação menos um quando não
zero; ausência de vizinhos também devolve zero. Se o objeto central já for
portão, devolve zero após consultar os vizinhos.

### Portão, tipo 12

`ValideHerse` aceita duas células de muro/portão à esquerda e à direita,
devolvendo orientação 0, ou acima e abaixo, devolvendo 1. Se ambos os encaixes
existirem, o horizontal prevalece. Sem encaixe, devolve 255 e a colocação
termina sem aplicar efeitos.

Quando aceito, grava a orientação em `+0x7c`, escreve o objeto de portão, zera
o u16 `+0x86`, ativa a máscara 1 e insere o rótulo com slot 0. O tile é
conservado. Esses efeitos não implementam abertura/fechamento nem autorização
de passagem pelo portão.

## Atualização dos muros ao redor

`mundo.atualizar_muros_vizinhos(celula)` é uma chamada separada. Consulta
oeste, leste, norte e sul. Para cada vizinho com objeto de muro e rótulo cujo
bit `0x8000` esteja ativo, extrai o índice da estrutura e atualiza seu `+0x7c`.
Não atualiza portões e não filtra pelo tipo do registro encontrado. Não foi
adicionado esse filtro, pois o x86 não o faz.

Colocar uma nova peça não atualiza automaticamente todas as peças próximas.
O consumidor deve chamar essa rotina nos pontos em que o fluxo original a
solicitar. A demonstração faz a atualização depois de colocar seu conjunto de
registros sintéticos.

```python
# Origem, tipo e demais campos do registro já preparados pelo chamador.
mundo.colocar_estrutura(indice)
mundo.atualizar_muros_vizinhos(celula)
```

## Leituras nas bordas

As consultas de objetos usam deslocamentos **lineares** na grade de 65.536
bytes. Não aplicam o teste normal de vizinhança pelo retângulo jogável.
Por exemplo, a consulta de leste na coluna 255 pode ler a coluna zero da linha
seguinte. `ValideHerse` compara com 256, conservando essa condição do original.

Não se usa `&65535` para envolver uma leitura antes do começo ou depois do fim
da grade. Quando uma consulta exige esses bytes adjacentes ainda não modelados,
a tradução levanta `NotImplementedError`. Os testes de borda diferenciados
permanecem no domínio de leituras observáveis da grade; eles não provam os
valores de memória que o jogo encontra fora dela.

## Demonstração e validação

[`colocacao-estruturas-python.json`](../relatorios/colocacao-estruturas-python.json)
registra três trajetos, com os campos de estrutura e terreno após a colocação:

| Cenário sintético | Resultado | Atualizações |
|---|---|---:|
| Edifício tipo 0 | Primeiro tile selecionado pelo tipo; desvio da máscara de colisão | 129 |
| Muro com portão válido | Nove muros e um portão vertical; unidade contorna o conjunto | 279 |
| Portão sem encaixe | Colocação recusada; caminho permanece livre | 129 |

Os três trajetos chegam a `(10,4)`, entregam a mensagem e encerram a tarefa.
A demonstração não abre o portão: o trajeto contorna o obstáculo. Um teste
separado bloqueia imports de emulação e reproduz o relatório somente em Python.

O diferencial executa os originais com suas chamadas internas, sem substituir
os auxiliares de colocação, cores ou terreno. Compara combinações de vizinhos,
IDs de objeto variáveis, preferência de orientação, todos os 22 tipos,
sobreposições e atualização dos registros ao redor. Confere registros completos,
grades, cores, rotas e, nos trajetos, a memória de tarefas por atualização.
A suíte completa do núcleo passou com **209 testes e 46.223 execuções x86
delimitadas**, sem falhas, erros ou testes ignorados. Sem emulação, passam
105 testes e os 104 opcionais ficam explicitamente ignorados. Os 52 arquivos
originais dos manifestos foram conferidos por tamanho e SHA-256.
Os resultados do núcleo estão nos relatórios
[emulado](../relatorios/validacao-emulada.json) e
[local](../relatorios/validacao-local.json), sem somar as suítes de outras frentes.

## Limites e continuidade

A colocação traduzida é a apresentação de um registro já existente no terreno,
não uma ordem completa de construir. Permanecem pendentes alocação/inicialização
dos registros, custos e progresso de construção, chamada global de atualização,
visão/minimapa de edifícios, operação do portão, demolição completa e a carga de
uma missão real. O remapeamento natural continua recusando estruturas já
inseridas. As rotinas novas não importam nem alteram os módulos dos outros chats.
