# Estruturas nos caminhos e afastamento de bloqueadores

A busca independente em Python agora trata as estruturas codificadas com
`0x8000`, mantém sua grade de cores e emite ordens para afastar unidades
bloqueadoras. A integração usa o mesmo avanço físico e as mensagens já
reconstruídos. As comparações continuam executando os bytes do EXE original
em memória sintética, sem iniciar uma partida.

## Reproduzir

```sh
python3 ferramentas/extrair_pegadas_estruturas.py
python3 ferramentas/demonstrar_estruturas.py
python3 ferramentas/validar.py
python3 ferramentas/validar.py --emular
```

A demonstração gera
[`estruturas-desbloqueio-python.json`](../relatorios/estruturas-desbloqueio-python.json)
sem EXE, Unicorn ou JIT. O extrator lê o EXE identificado pelo hash, sem executá-lo;
não é necessário executá-lo para usar as constantes de geometria já versionadas.

| Cenário sintético | Resultado |
|---|---|
| Parede de estruturas | A unidade contorna a parede e chega a `(10,4)` em 279 atualizações |
| Dois aliados bloqueadores | Ambos recebem ordens no ciclo 3 e terminam em `(2,3)` e `(2,2)`; todos os movimentos terminam no ciclo 22 |

No segundo caso, o destino do solicitante está numa região inacessível. Sua
ordem termina por cancelamento, com a mensagem correspondente. O cenário
comprova as ordens emitidas e o movimento dos bloqueadores; não comprova que
esse solicitante alcançou o destino.

## Rotinas e fontes

| Original | Endereço | Tradução |
|---|---|---|
| `BatimentTailleGet` | `0x41a996` | `tamanho_estrutura` |
| `GetBatimentCaseList` | `0x41a9c3` | `celulas_estrutura` |
| `BatimentCollision` | `0x41ab5c` | `colisao_estrutura` |
| `BatimentOccupeCase` | `0x41aff8` | `estrutura_ocupa_celula` |
| `Chemin_ModifieZone`, modos 1/3 | `0x43e138` | `modificar_regiao_estrutura` |
| `Remplit` | `0x43e464` | `CoresEstruturas.preencher` |
| `AlloueCouleur` / `LibereCouleur` | `0x43e5a0` / `0x43e5d5` | `alocar` / `liberar` |
| `MurAjoute` / `MurRetire` | `0x43e616` / `0x43e8b7` | `adicionar_muro` / `retirar_muro` |
| `EnginChercheCaseLibre` | `0x44330c` | `procurar_celula_livre` |
| `EnginDebloqueNextCase` | `0x449176` | `afastar_bloqueadores` |

As novas exportações estão em
[`evidencias/estruturas-desbloqueio/`](../evidencias/estruturas-desbloqueio/exportacao.tsv).
Os corpos anteriormente exportados estão em
[`navegacao/`](../evidencias/navegacao/00449176.asm),
[`avanco-chegada/`](../evidencias/avanco-chegada/0043e138.asm) e
[`ghidra/`](../evidencias/ghidra/0042f214.asm).
O pseudocódigo automático pode atribuir argumentos aos registradores errados;
a tradução segue o assembly e as comparações diferenciais.

## Geometria de construções

Os 1.000 registros de estruturas começam em `0x49a0c8`, com passo 276.
Os campos usados nesta etapa são:

| Offset | Uso observado |
|---|---|
| `+0x02`, u16 | Célula de origem do retângulo |
| `+0x04`, byte | Dono |
| `+0x08`, byte | Tipo, usado como índice da tabela de dimensões e das máscaras |
| `+0xcc + subcélula*2`, u16 | Região preservada sob a ocupação |

O byte `+0x08` **não é um estado**. A busca dá tratamento especial ao **tipo 9**
nos registros de obstáculos. Não se deve interpretar a comparação com 9 como
“estrutura pronta” ou “estado ativo”.

As dimensões iniciais vêm de `0x495d8c/+2`, com passo 52. As 22 máscaras são
referidas pelo seletor em `0x41ab5c`. A extração reproduzível está em
[`pegadas-estruturas.json`](../relatorios/pegadas-estruturas.json), e as constantes
independentes estão em [`pegadas_estruturas.py`](../ferramentas/pegadas_estruturas.py).

A lista de células inclui o retângulo inteiro, de baixo para cima e da esquerda
para a direita, com wrap u16. A consulta de ocupação só aceita posições cuja
máscara seja não zero e usa soma de 32 bits: nas bordas, não é equivalente a
consultar a lista com wrap. Algumas células do retângulo não bloqueiam passagem.

## Regiões preservadas e cores auxiliares

O rótulo de uma estrutura é:

```text
0x8000 | (índice << 5) | subcélula
```

A inserção dos modos 1/3 de `Chemin_ModifieZone` só substitui rótulos menores
que `0x4000`. Guarda a região anterior no registro, escreve o rótulo e chama
`MurAjoute`. A remoção exige que o rótulo corresponda exatamente ao índice e à
subcélula; então restaura a região salva e chama `MurRetire`. Não altera a máscara
física do terreno: essa atualização pertence ao chamador.

Apesar dos nomes franceses com `Mur`, esses modos atualizam as cores das
células de estruturas recebidas pelo chamador. Não se deve restringi-los
automaticamente ao tipo 9.

A grade apontada por `0x4e156c` contém 65.536 bytes. Uma cor representa um
componente de obstáculos e não tem relação com a paleta gráfica. A lista de
regiões do contorno usa **`0x8000 | cor`**, em vez do índice da estrutura.
Assim, várias estruturas adjacentes podem pertencer ao mesmo obstáculo.

O alocador conserva os 256 bytes em `0x4e1570` e os 256 flags em `0x4e1670`.
A inicialização de `Chemin_Remap` deixa 255 cores livres, enumeradas 1..255,
com todos os flags em 1. A primeira alocação devolve 255. Zero indica esgotamento;
liberações repetidas e a liberação de zero são ignoradas.

`Remplit` usa quatro vizinhos, na ordem oeste, norte, leste, sul. Preserva uma
pilha de 1.024 palavras, com posições úteis 1..1.023, e termina antecipadamente
quando ela enche. A tradução conserva a cauda inativa e o mesmo limite.
Trocar uma cor por ela mesma é recusado na API Python: o x86 pode não terminar
nesse caso. As chamadas válidas do alocador usam uma nova cor diferente.

`MurAjoute` captura as quatro cores vizinhas, aloca uma nova, preenche os
componentes correspondentes, colore a célula inserida e libera as cores antigas.
`MurRetire` zera a célula e atribui cores novas aos componentes que se separaram.
As consultas repetem a comparação com a cor capturada para não recolorir o mesmo
componente várias vezes.

## Estruturas nos candidatos e contornos

[`candidatos_rota.py`](../ferramentas/candidatos_rota.py) e
[`contornos_caminhos.py`](../ferramentas/contornos_caminhos.py) agora normalizam
os rótulos pela cor da **célula efetivamente consultada**. Isso também vale para
as quatro subcélulas das unidades grandes e para o teste de saída por linha.

Antes da deduplicação pela cor, a observação de uma estrutura do tipo 9 pode
alterar o registro de dez bytes do candidato:

| Campo | Uso |
|---|---|
| u16 `+2` | Índice da estrutura |
| byte `+5` | Estrutura registrada |
| byte `+7` | É adversária |
| byte `+9` | Fase do contorno |

A aliança é consultada do dono da estrutura para o dono solicitante. O primeiro
registro elegível é mantido até aparecer um adversário, que tem preferência.
Mesmo uma segunda estrutura da mesma cor pode substituir esse registro.
A seleção final já traduzida pode usar esses dados no ramo de status 5.

## Ordens para afastar unidades

[`desbloqueio_unidades.py`](../ferramentas/desbloqueio_unidades.py) reproduz as
três tentativas na direção **d, d−2, d**, preservando o terceiro teste repetido.
O ocupante vem de `ChercheIndiceEngin`: precisa estar vivo e ter o byte `+0x72`
habilitado; o tipo 16 também exige o modo 50 para ser encontrado.

Para emitir a ordem, exige **dono idêntico** e célula atual igual ao destino.
Uma aliança entre donos diferentes não basta. Não há um teste adicional de
“ocioso” nessa rotina. A procura começa na célula vizinha atingida, que pode
ser uma subcélula da pegada de uma unidade grande.

`EnginChercheCaseLibre` examina uma janela 3×3 em ordem de leitura, omitindo
sempre a posição de índice 4. O canto superior esquerdo é limitado a zero;
nas bordas, a posição omitida pode não coincidir com o centro original.
A janela não cresce para unidades grandes: cada candidato passa pelo predicado
normal de passagem, que verifica a pegada e a máscara de movimento da unidade.

Ao encontrar uma célula, a tradução chama `definir_movimento`, a implementação
de `SetDeplaceEngin` já conferida. Isso também aplica `ResetOrdre`, libera o
contexto de busca pertinente e limpa referências, inclusive os efeitos do tipo
13 sobre a estrutura anteriormente reservada.

O retorno significa **bloqueador elegível encontrado**. Ele pode ser verdadeiro
sem célula livre e sem ordem emitida. O solicitante sempre termina essa rotina
com `+0x88=1` e `+0x8b=0`; o controlador de navegação aplica depois o resultado.
Os globais `0x4e1a34` e `0x4e1a36` conservam o último bloqueador consultado e a
última célula livre procurada, inclusive os resíduos dos ramos não executados.

## Contrato de integração e limites

Use `MundoNavegacao(..., solucionador=SolucionadorCaminhosPython())`. Primeiro
reconstrua as regiões naturais; depois insira as células bloqueadoras com
`mundo.modificar_regiao_estrutura(indice, subcelula, celula, inserir=True)` e
aplique os atributos físicos correspondentes. A remoção usa `inserir=False`.
Os registros de origem, tipo e dono devem ser fornecidos pelo chamador.

O remapeamento natural com estruturas já inseridas é recusado antes de alterar
dados. O ciclo completo de reconstrução a partir dos registros de uma partida
ainda precisa ser portado. Os testes de busca que importam RAM sintética devem
fornecer regiões preservadas e cores coerentes; uma grade zerada não reconstrói
automaticamente os componentes de construções existentes.

A bancada original agora carrega as grades e os campos auxiliares. No caso de
unidades grandes sem espaço, usa checkpoints entre consultas, preservando
registradores e pilha: cada trecho mantém o limite de um milhão de instruções
e um segundo. Não substitui as chamadas internas do desbloqueio.

A validação cobre todas as classes de unidades, os 22 tipos de estruturas,
bordas e wrap, alocação/esgotamento, união/separação de componentes, registros
completos e trajetos com mensagens. A suíte completa passou com **177 testes e 41.031 execuções x86 delimitadas**,
sem erros, falhas ou testes ignorados. Sem emulação, passam 85 testes e os
92 opcionais ficam explicitamente ignorados. Os relatórios gerais de
[validação emulada](../relatorios/validacao-emulada.json) e
[validação local](../relatorios/validacao-local.json) registram os totais.
Os 52 arquivos originais dos manifestos foram novamente conferidos por tamanho
e SHA-256.

Continuam pendentes a inicialização completa dos mapas reais, o ciclo completo
de construção/demolição, tráfego mais amplo, atropelamento, combate, economia e
validação numa partida. O código desta etapa permanece no núcleo do repositório;
as pesquisas paralelas não fazem parte desta alteração.
