# Aplicação e limpeza do terreno de construções

Retomada de 28/10/2026: foram traduzidos os chamadores que percorrem a máscara
inteira de uma construção e aplicam os efeitos ao terreno. Antes, o núcleo
permitia inserir/remover rótulos de células isoladas; agora também percorre o
edifício, escreve os tiles, ativa a colisão e remove objetos conforme o x86.

## Implementação e evidências

| Original francês | Endereço | API de `MundoNavegacao` |
|---|---|---|
| `BatimentModifyTerrain` | `0x41ba49` | `aplicar_terreno_estrutura(indice, origem, primeiro_tile, mascara_tipo20=None)` |
| `ResetBatimentTerrainModify` | `0x41b888` | `resetar_terreno_estrutura(indice, modo)` |
| `ResetCheminTerrainModify` | `0x41b78f` | `remover_regioes_estrutura(indice)` |

A tradução está em [`terreno_estruturas.py`](../ferramentas/terreno_estruturas.py).
Os três métodos do mundo apenas encaminham a chamada; não presumem uma ordem
completa de construir ou demolir. O uso continua independente de EXE, Unicorn
e JIT. A bancada em [`bancada_terreno_estruturas.py`](../ferramentas/bancada_terreno_estruturas.py)
executa os originais, inclusive os auxiliares internos e epílogos compartilhados.

[`evidencias/terreno-estruturas/manifesto.json`](../evidencias/terreno-estruturas/manifesto.json)
registra sete intervalos, endereços, bytes, hashes e a tabela consultada pelo
aplicador. Os ASM são extraídos diretamente do PE identificado pelo SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Esta etapa usa Capstone para extração; não abre o projeto Ghidra compartilhado.

```sh
python3 -B ferramentas/extrair_terreno_estruturas.py
python3 -B ferramentas/demonstrar_terreno_estruturas.py
python3 -B ferramentas/validar.py
python3 -B ferramentas/validar.py --emular
```

Somente a extração lê o EXE. A demonstração usa dados sintéticos e constantes
versionadas; os testes diferenciais requerem o EXE e Unicorn/JIT.

## Aplicação: retângulo, máscara e slots compactos

O índice identifica um dos 1.000 registros com passo 276. O tipo vem de `+0x08`.
As dimensões são lidas em `0x495d8c/+2`, com passo 52 por tipo. A origem e o
primeiro tile são **argumentos do chamador**; aplicar o terreno não atualiza
a origem `+0x02` guardada no registro.

O retângulo é percorrido de cima para baixo e da esquerda para a direita:

1. Escrever o tile e incrementar seu ID para a próxima célula, com wrap u16.
2. Se a máscara da célula for não zero, ativar o bit 0 dos atributos e chamar
   `Chemin_ModifieZone`, modo 3, que preserva a região e atualiza as cores.
3. Zerar o objeto da célula, inclusive nas posições sem colisão.

Os slots em `+0xcc` e os cinco bits baixos do rótulo da estrutura **só contam
posições com colisão**, e não todas as posições do retângulo. Por exemplo, a
máscara do tipo 0 ocupa as posições retangulares 0, 1, 3, 4, mas usa os slots
0, 1, 2, 3. O slot avança mesmo se `Chemin_ModifieZone` recusar uma inserção
por sobreposição. Os atributos e os tiles ainda são alterados nessa posição.

O original não recorta esse percurso pelas dimensões jogáveis: as células
recebidas pelos auxiliares são truncadas a u16. Os ensaios de borda preservam
esse comportamento. As rotinas de cores testam os limites de cada vizinho,
sem exigir que a célula inicial já esteja dentro do mapa; isso também foi
corrigido no componente Python anterior.

## Exceção do tipo 20: máscara em RAM

A tabela usada por `BatimentModifyTerrain` contém um ponteiro no offset `+8`
de cada registro de tipo. Para 21 dos 22 tipos, ele aponta para a mesma máscara
estática consultada por `BatimentCollision`. **O tipo 20 é diferente:**

| Consumidor | Origem da máscara do tipo 20 |
|---|---|
| Aplicação de terreno | 20 bytes em RAM, `0x4dfb9c` |
| Limpeza de colisão e remoção de regiões | Máscara estática compartilhada com o tipo 15, `0x495d1c` |

A distinção vem da entrada 20 da tabela no manifesto e do seletor já exportado
em [`BatimentCollision`](../evidencias/estruturas-desbloqueio/0041ab5c.asm).

A região de RAM não tem bytes de arquivo que determinem seu estado durante uma
partida. A API exige `mascara_tipo20=bytes_de_20_posicoes`; ausência ou tamanho
incorreto é recusado **antes de alterar qualquer dado**. Não assume uma máscara
zerada nem copia silenciosamente a máscara estática do tipo 15.

Os diferenciais fornecem máscaras zerada, cheia e heterogêneas, conservando a
diferença entre aplicação e remoção. Dependendo desses dados, a remoção pode
deixar rótulos ou bits de colisão; isso também ocorre na execução nativa e não
foi uniformizado. A origem e atualização desses 20 bytes ao longo da partida
permanecem uma pendência do chamador. A validação não determina seu significado
por aparência, pelo nome do tipo ou por dados de outro subsistema.

## Duas limpezas de terreno e uma remoção de regiões

`ResetBatimentTerrainModify` usa a origem guardada em `+0x02`, não a origem
anteriormente recebida como argumento. O byte baixo de `modo` seleciona:

| Modo u8 | Efeito |
|---|---|
| Não zero | Limpar somente o bit 0 nas células aceitas por `BatimentCollision`; conservar os demais bits e os tiles |
| Zero | Substituir os tiles do retângulo pelo padrão de piso; conservar colisão e regiões |

O piso não restaura uma cópia dos tiles antigos. Seu cálculo é
`0x15d + ((x + posição_retangular) % 8) + 8*((y + linha) % 8)`.
O contador horizontal continua crescendo entre linhas no x86. Reiniciá-lo
em cada linha mudaria o resultado e não foi feito na tradução.

`ResetCheminTerrainModify` usa a máscara estática e os mesmos slots compactos.
Chama `Chemin_ModifieZone`, modo 1, para restaurar as regiões que ainda possuam
o rótulo exato esperado e separar componentes de cores. Essa operação não
libera atributos físicos nem altera os tiles. As três operações continuam
separadas; não são uma demolição completa.

Para aplicar e depois retirar apenas esses efeitos, com o registro já preparado:

```python
mundo.aplicar_terreno_estrutura(indice, origem, primeiro_tile)
# O chamador mantém origem, tipo, dono e estado no registro correto.
mundo.resetar_terreno_estrutura(indice, 1)
mundo.remover_regioes_estrutura(indice)
mundo.resetar_terreno_estrutura(indice, 0)
```

## Demonstração e validação

[`terreno-estruturas-python.json`](../relatorios/terreno-estruturas-python.json)
registra três trajetos até `(10,4)`, com mensagens e término da tarefa:

| Cenário | Alteração de terreno | Atualizações |
|---|---|---:|
| Edifício com máscara | Retângulo 3×4, quatro células bloqueadoras | 129 |
| Edifício retirado durante o movimento | Remoção dos quatro rótulos e da colisão no ciclo 28 | 129 |
| Parede aplicada pelas rotinas traduzidas | Onze estruturas, desvio pela busca geral | 279 |

As durações iguais dos dois primeiros casos não implicam trajetos idênticos nem
uma promessa de encurtar rotas ao remover um edifício. A demonstração reproduz
o controle de movimento já traduzido; não introduz replanejamento automático.

Os novos testes comparam os 22 tipos, origens normais/zero/wrap, ambos os modos
de limpeza, tiles com overflow, regiões heterogêneas, sobreposição e máscaras
do tipo 20. Conferem registros completos de unidades/estruturas/grupos, grades
de terreno e visão, minimapa, rotas, alocador e pilha de cores. Nos três trajetos,
também comparam cada atualização e a memória de tarefas com o x86. Um ensaio
separado bloqueia imports de emulação e reproduz a demonstração apenas em Python.

A suíte completa do núcleo passou com **193 testes e 43.170 execuções
x86 delimitadas**, sem falhas, erros ou testes ignorados. Sem emulação, passam
95 testes e os 98 opcionais ficam explicitamente ignorados. Os 52 arquivos
originais dos manifestos foram novamente conferidos por tamanho e SHA-256.

Os resultados completos do núcleo estão em
[`validacao-emulada.json`](../relatorios/validacao-emulada.json) e
[`validacao-local.json`](../relatorios/validacao-local.json). Eles não somam as
validações das pesquisas paralelas. A bancada não substitui chamadas internas
das três rotinas aqui traduzidas; animação contínua e áudio ficam fora do pulso
de movimento, conforme o contrato anterior.

## Continuidade

Ainda faltam o chamador completo de colocação/demolição, a política de origem e
primeiro tile, a máscara em RAM do tipo 20, visão/desenho de construções, efeitos
econômicos e o carregamento/remapeamento integral de uma partida real. O método
`refazer_regioes` continua recusando estruturas já inseridas; esta entrega não
transforma o remapeamento natural numa reinicialização completa do mundo.
As rotinas e demonstrações desta etapa permanecem no núcleo do repositório.
