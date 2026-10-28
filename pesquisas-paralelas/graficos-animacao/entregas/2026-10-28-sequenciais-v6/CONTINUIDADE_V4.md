# Continuidade v4 — Santuário e recoloração

Revisão: `2026-10-28-santuario-v4`. Predecessor próprio:
`b67215a3870d17a51b063cb9d82ea391c1852f56`. Snapshot principal:
`1c8ebdd43b0a820652b7cb852ae1fe218d4dea5e`.
Caminhos e SHA-256 em `evidencias/proveniencia-v4.json`,
`fontes/manifesto.json`, `snapshot/manifesto.json`, `evidencias/manifesto.json`.
Os insumos originais e as entregas anteriores não foram alterados.

## Resultado verificável

O tipo de construção **2**, chave `SANCTUAIRE`, nome brasileiro **SANTUÁRIO**,
foi ligado a 30 quadros de terreno e 43 quadros de fachada. A fachada habitada,
modo 5, campo +0x06 zero, desenha sete camadas. As associações são confirmadas
por código e comparação x86; os nomes descritivos das camadas são rótulos de
inspeção visual e não atribuem função econômica ou de combate.

`construcoes.py` consulta e compõe em Python padrão. `gerar_construcoes.py`
produz `artefatos/demo-santuario.html`, dois atlas, comparação dos cinco
jogadores, tabela CSV/JSON de 73 linhas e exemplo ETA. HTML e API não usam x86.
O primeiro marco das cinco unidades segue disponível, sem mudanças na API.

## ETA → registro → terreno → fachada

1. `MONDE01.ETA`, bloco em `0x50030`: quantidade 1, tamanho 204. O índice 0
   precede o registro em `0x50036`. Campos: origem (12,11) em +2/+3; jogador
   0 em +4; modo 5 em +5; auxiliar u16 zero em +6; tipo 2 em +8.
2. `LoadMission`, trecho `0x46c517..0x46c578`, lê os 204 bytes diretamente
   para `0x49a0c8 + indice*276`. A comparação executa esse trecho com leitura
   de arquivo em memória. Não representa a execução integral do carregador.
3. Tabela `0x495d8c`, 22 registros de 52 bytes. Tipo 2 em `0x495df4`:
   dimensões u16 6×5, ponteiro de máscara `0x495c30`, chave INI em +19.
   `BatimentGetTypeName` em `0x418af7` confirma essa estrutura. O INI fornece
   o nome brasileiro. Os demais 21 tipos receberam somente catálogo de
   identidade; isso não valida seus gráficos.
4. `PlaceBatiment` (`0x41c4ac`), ramo tipo 2 em `0x41c4e7`, escolhe terreno
   base 732. `BatimentModifyTerrain` (`0x41ba49`) coloca IDs **732..761**
   em ordem de linhas, 6×5. O resultado coincide com o terreno já serializado
   na missão 1. Cada ID é de BLOCS.CMP, local/global = ID−1.
5. A máscara tem 17 células ocupadas. `Chemin_ModifieZone` (`0x43e138`)
   grava `0x8000 | indice_construcao<<5 | ordinal_ocupado` na camada de
   ocupação apontada por `0x4e0f38`. O ordinal conta somente células marcadas.
   `MurAjoute` (`0x43e616`), atualização de cache de conectividade, foi
   substituído por retorno: não é consultado pelo caminho de desenho testado.
   Não se afirma validar navegação ou toda a colocação de edifícios no jogo.
6. `AffBatiments` (`0x407dd3`) consulta ocupação, jogador, modo e descoberta;
   `CaseEstDecouverte` (`0x4766d6`) usa o bit 0x10 da camada do jogador.
   O switch de terreno em `0x40f23b` reconhece ID **749** e salta a
   `0x408577`. Esse ID está na célula relativa **(5,2)**, absoluta **(17,13)**,
   ocupação `0x800f`. O ramo subtrai **(150,93)** da posição dessa célula.
7. `BatimentEstHabiter` (`0x41a5b8`) e `BagContientTroupe` (`0x44724a`)
   retornam verdadeiro para o exemplo. As unidades usadas nessa consulta
   foram recompostas em 272 bytes, com quatro bytes finais zero não lidos
   pelo trecho. A API exige `habitado` externo; não implementa regra econômica.

Os 30 quadros do terreno foram ligados ao tipo por colocação original, leitura
ETA e inspeção de `AffTerrain` (`0x41068e`). A página monta essas 30 células
antes da fachada para inspeção. Não foi executado o percurso completo de
`AffTerrain` com vegetação, neblina e outros objetos; a composição global
intercalada do mundo permanece em aberto.

## Camadas e fases confirmadas

A, B e C são os dwords em `0x508f7c`, `0x508f80`, `0x508f84`.
P é a célula empacotada **y×256+x** recebida em EBX por `AffBatiments`.
Coordenadas abaixo relativas ao canto superior esquerdo da célula gatilho.

| Ordem / rótulo | ID do motor | Local BUILDING | Δ x,y | Operação |
|---|---|---|---|---|
| 0 corpo | 7032 | 3 | −150,−93 | jogador |
| 1 detalhe alto | 7049 + ((C+P)&7) | 20..27 | −76,−88 | jogador |
| 2 detalhe central | 7033 + ((A+P)&7) | 4..11 | −61,+2 | copiar |
| 3 detalhe direito | 7041 + ((B+P)&7) | 12..19 | +1,+38 | copiar |
| 4 bandeira esquerda | 7059 + (A&7) | 30..37 | −102,−29 | jogador |
| 5 bandeira direita | 7067 + (A&7) | 38..45 | −6,−19 | jogador |
| 6 detalhe esquerdo | 7057 + ((A+P)&1) | 28..29 | −132,−30 | copiar |

Global = ID−1; local BUILDING = ID−7029. Sequências completas e hashes dos
pixels/máscaras estão em `artefatos/associacoes-santuario.json`.

A pilha preserva EBX em `0x407ddf`. Os acessos `[esp]` em `0x4087df`,
`0x408817`, `0x40884e`, `0x4088f1` somam **a célula**, não o jogador.
A hipótese inicial de soma pelo jogador falhou já em relógios zero/jogador 0:
o código pediu 7050/7034/7042/7058. Ela foi descartada antes da publicação.
Foram então comparadas 512 combinações de relógios e 160 casos variando
coordenadas, jogador e bits altos dos relógios; todos coincidem com a fórmula.

`ProgIteration` (`0x47500e..0x475041`) incrementa A como u32. Se o novo A é
par, incrementa B; se o novo A é divisível por 3, incrementa C. Os três
incrementos preservam overflow. Partindo de (0,0,0), as fases conjuntas
repetem em 48 chamadas. Não derivar B/C de A em um estado arbitrário: a API
recebe os três contadores. A taxa original em segundos continua desconhecida.

## Cores por jogador

`CalculTabPlayer` (`0x45ff61`) inicializa cinco tabelas de 256 bytes. Somente
160..167 mudam. Fonte das três faixas: `0x496d4c`, registrada no JSON de identidade.

| Jogador | Saída para índices 160..167 |
|---|---|
| 0 | 160,161,162,163,164,165,166,167 |
| 1 | 144,145,146,148,149,150,253,254 |
| 2 | 136,137,138,139,140,141,142,143 |
| 3 | 48,50,52,54,56,58,59,61 |
| 4 | 47,47,47,47,47,47,47,47 |

`PastePlayerCmp` (`0x45c455`) chama `MemPlayerCopy` (`0x45f850`) para remapear
os índices **da fonte**; o argumento de jogador é removido com RET 4.
Máscaras CMP continuam preservadas e literal zero continua opaco. A tabela
0 é identidade. Esta é a tabela inicial original, sem efeitos posteriores de
paleta. A v4 usa essas tabelas na fachada; a composição de unidades da v3
continua limitada ao contrato de jogador 0, sem generalização automática.

## Validação e limites

- Python: **53 testes**; nenhum depende de Unicorn. Incluem integridade dos
  insumos e regressões de unidades/composição anteriores.
- Comparação original v4: **1.183 execuções delimitadas**, 41.514.049 instruções,
  50,063 s nesta máquina; 512 capturas de fases, 160 variações de célula/jogador,
  três casos negativos de visibilidade/ocupação/terreno, 258 transições dos
  relógios, cinco tabelas completas e **244 superfícies de 320×320** idênticas.
- Pixels: 5 jogadores × 48 estados coerentes dos relógios, mais quatro recortes.
  Os sete blits foram executados integralmente, sem substituir os blitters.
- Navegador: 48 planos e 15 buffers completos JS/Python conferidos; seleção de
  jogador, fase, passo 47→0, reprodução/pausa, terreno, camada e âncora inspecionados.
  Captura em `artefatos/demo-santuario-verificada.png`.

O EXE tem hash conferido antes de qualquer emulação. Cada chamada tem timeout
2 s, teto de 1 milhão de instruções e intervalos de endereço permitidos.
O caminho de desenho é parado em **0x40f342**, antes de indicadores posteriores,
incêndio, seleção e barras. Animação decorativa que faz parte dos CMPs está
incluída; o efeito de incêndio da construção não está. Não são validados
outros modos, auxiliar +6 não zero, habitação falsa, sombras de construções,
ordenação global nem seleção. Predicados negativos foram comparados, mas a
API de fachada pressupõe que o consumidor já decidiu desenhar o edifício.

Dependências x86: `bancada_x86.py`, `validar_x86.py`, `validar_trabalhadores.py`,
`validar_composicao.py`, **`validar_construcoes.py`**. Somente extração de assembly
usa Capstone. API, teste Python, atlas e demonstração não usam essas bibliotecas.

## Próximos casos independentes

Rastrear primeiro `AffVegetTerrain`/camada de objetos e árvores/pedras ETA;
depois fachada não habitada e demais modos do Santuário, com contrato explícito
para o efeito cinza. Para outros edifícios, repetir a cadeia tipo→PlaceBatiment
→gatilho de terreno→camadas antes de associar IDs. Indicadores, seleção, HUD e
minimapa ainda não foram incorporados. Nenhuma informação de combate/economia
foi modificada ou esperada de outra frente.
