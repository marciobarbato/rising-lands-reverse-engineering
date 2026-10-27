# Símbolos originais e regras da IA

`RISING.SBL` e `RISING.RUL`, presentes no CD, permitem recuperar os nomes originais
franceses e associá-los às instruções do executável. Os identificadores são
preservados; as explicações e nomes da reconstrução independente estão em português.
Isso recupera símbolos e regras compiladas, não os arquivos-fonte originais.

## Reproduzir a extração

```sh
python3 ferramentas/extrair_ia.py
```

O comando verifica o hash do EXE estudado e grava apenas relatórios neste
repositório. Os leitores em `ferramentas/simbolos_ia.py` não precisam de Ghidra
nem de Unicorn. As fontes e seus hashes estão em
[`fontes-ia.json`](../relatorios/fontes-ia.json).

| Arquivo | Tamanho | Resultado |
|---|---:|---|
| `RISING.SBL` | 51.451 bytes | 1.995 registros de símbolos, 1.960 endereços distintos |
| `RISING.RUL` | 26.199 bytes | 1.157 registros de instruções, 64 entradas de tipos |

Há 42 tipos de tarefa com entrada diferente de zero. O programa referencia
140 nomes de operações nativas, resolvidos em 136 endereços distintos.
Alguns nomes são aliases da mesma função.

## SBL: XOR e endereçamento

O carregador `0x48d5fd` lê o arquivo e aplica XOR `0xff` a **todos** os bytes,
conforme o laço `0x48d67c..0x48d687`. Depois da transformação, o arquivo contém:

1. Pares de dwords: deslocamento da função e offset do nome no próprio arquivo.
2. Par terminador com primeiro dword `0xffffffff`.
3. Strings terminadas em zero, normalmente com um espaço antes do terminador.

**Não há cabeçalho de versão.** O primeiro dword, 3, é o deslocamento do símbolo
`___begtext`. Interpretá-lo como versão deslocaria toda a tabela.

`0x48d74b` procura `_debugGetPC ` e calcula:

```
base_dos_simbolos = 0x48ff7f - deslocamento_de__debugGetPC
                  = 0x401000
endereco = base_dos_simbolos + deslocamento
```

Essa base é diferente do ImageBase `0x400000` do PE. Somar diretamente o ImageBase
produziria endereços errados por 4.096 bytes.

O catálogo preserva todos os registros, inclusive oito nomes repetidos em
endereços diferentes. Para consultas por nome, a reconstrução mantém a primeira
ocorrência. O resolvedor original percorre a tabela em ordem e busca o nome
solicitado acrescido de espaço. O teste emulado confere os **140 nomes efetivamente
usados pelo RUL**, uma entrada real por vez, além do cálculo da base pela âncora.
Não se afirma equivalência para consultas arbitrárias por fragmentos de nome.

Catálogos: [`simbolos-originais.json`](../relatorios/simbolos-originais.json) e
[`simbolos-originais.tsv`](../relatorios/simbolos-originais.tsv).

## Nomes que esclarecem a pesquisa

| Endereço | Nome original | Interpretação em português |
|---|---|---|
| `0x42d4f8` | `Chemin_Accessible` | Consulta de acessibilidade por regiões |
| `0x42e890` | `OptimiseChemin` | Pós-processamento do caminho |
| `0x42f214` | `CheminCalcul` | Cálculo de caminho |
| `0x43b30b` | `Chemin_Verouille` | Preparação e reserva do contexto de busca |
| `0x43ec0c` | `LocalTerrainEnCollision` | Teste local de colisão no terreno |
| `0x448b9f` | `EnginNextCaseChemin` | Próxima célula da rota |
| `0x44930c` | `DeplaceEngin` | Atualização do deslocamento da unidade |
| `0x47b283` | `AvanceMonstre` | Atualização dos monstros |
| `0x47d314` | `iaSolver` | Interpretador das tarefas |
| `0x47d7ec` | `iaProbNew` | Alocação de tarefa |
| `0x47d920` | `iaProbPost` | Inclusão de tarefa na lista do jogador |
| `0x47e437` | `iaProbLoadBinaryRules` | Carregamento de regras binárias |
| `0x482936` | `iagUnitNoyau` | Núcleo de unidades; corpo vazio nesta versão |
| `0x48453c` | `iagVilleNoyau` | Núcleo da cidade |
| `0x485183` | `iagRessNoyau` | Núcleo de recursos |
| `0x4866d7` | `iagWarNoyau` | Núcleo de guerra |

O nome sozinho não prova comportamento. `B_AccessibiliteChemin`,
`B_AccessibiliteBatiment` e `B_Bidon` apontam para `0x47f31c`, que retorna 1
sem consultar o mapa. Já `B_GicleUniteAmieDeZone`, `B_TestUniteAmieSurZone`
e `B_TestUniteEnnemieSurZone` apontam para `0x47f322`, que retorna -1.
`Chemin_Accessible` é uma função diferente, com consulta real à grade.

## RULE: formato do programa

O carregador `0x47e437` fornece a evidência de layout:

| Offset | Tipo | Campo |
|---:|---|---|
| `0x00` | 4 bytes | Assinatura ASCII `RULE` |
| `0x04` | u32 | Valor 26.055 no corpus; não é consultado nesse carregador |
| `0x08` | u32 | Tamanho da área de strings: 2.915 |
| `0x0c` | u16 | Número de registros: 1.157; limite do carregador: 1.200 |
| `0x0e` | u16 | Número de entradas de tipos: 64; limite: 64 |
| `0x10` | registros de 20 bytes | Instruções |
| após registros | u16 por tipo | Índice de entrada da tarefa; zero significa ausente |
| após entradas | bytes | Nomes de operações terminados em zero |

Cada instrução contém cinco u32: operação, formato de argumentos, desvio de
sucesso, desvio de falha e constante. Se o bit 31 da operação estiver ativo,
os 31 bits inferiores são um offset para o nome na área de strings. Na carga,
o nome é resolvido para um endereço nativo. Sem esse bit, os valores de 1 a 63
representam chamadas a tipos de subtarefa.

Os quatro primeiros registros são reservados. Os destinos 0 e 3 encerram a
tarefa sem escrever um resultado novo no pai; 1 conclui com resultado 1 no pai;
2 conclui com resultado -1. Destinos a partir de 4 continuam no índice indicado.
Os detalhes de argumentos e suspensão estão em [TAREFAS.md](TAREFAS.md).

O leitor independente também verifica offsets, terminadores, referências e
tamanho exato do arquivo. Essas verificações de integridade são mais estritas
que algumas verificações do carregador original; não se afirma equivalência
para arquivos corrompidos.

O grafo completo foi extraído em [`regras-ia.json`](../relatorios/regras-ia.json),
com os índices de ocorrência de cada operação e os pontos de entrada das tarefas.

## Ghidra

Os 1.995 registros foram importados para o namespace `OriginaisSBL`; o relatório
está em `evidencias/simbolos-importados.tsv`. O script
`ghidra/scripts/ImportarSimbolosOriginais.java` acrescenta os rótulos sem apagar
anotações anteriores. Também permite criar funções selecionadas em entradas
confirmadas pelo SBL que a análise automática não havia reconhecido.

O projeto continua em `ghidra/projetos/`, local e ignorado pelo Git. O TSV, o
script e as novas exportações são versionados para permitir reconstruí-lo.
As convenções de chamada inferidas pelo Ghidra continuam exigindo conferência
no assembly, mesmo quando o nome original está disponível.
