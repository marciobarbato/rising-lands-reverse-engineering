# Formatos de arquivos

Todos os números multibyte dos formatos abaixo são **little-endian**. Os offsets
são relativos ao início do arquivo, exceto quando explicitamente indicados como
endereços virtuais do executável.

## CMP: sequência de quadros comprimidos

Evidências: [carregador_cmp.asm](../evidencias/carregador_cmp.asm) e
[composicao_cmp.asm](../evidencias/composicao_cmp.asm).

| Offset | Tipo | Significado |
|---|---|---|
| `0` | `u16` | Quantidade de quadros |
| `2` | sequência | Quadros, um após o outro |

Cada quadro começa com `u16 largura`, `u16 altura`, `u32 tamanho_comprimido`,
seguidos por exatamente `tamanho_comprimido` bytes de comandos. Não há paleta
embutida nesse cabeçalho.

| Byte de comando | Interpretação comprovada no corpus |
|---|---|
| `0x00` | Não avança pixels; o byte de comando é consumido |
| `0x01..0x7f` | Avança essa quantidade de pixels transparentes |
| `0x81..0xff` | Copia `256 - comando` bytes literais |
| `0x80` | Não observado nos oito arquivos; rejeitado por este leitor |

O byte `0x80` merece cuidado: a sequência `NEG BL`/`MOVSX` da rotina examinada
não produz +128. Não se generalizou o caso ausente do corpus. Foram examinados
2.089.436 comandos, com 1.062 ocorrências de zero e nenhuma de `0x80`.

O jogo desenha sobre um destino existente, pulando regiões transparentes. O
extrator cria uma imagem isolada e preenche essas regiões com índice zero.
Isso é suficiente para recuperar os quadros; não reproduz todas as composições
de sprites, névoa e efeitos do motor.

| Arquivo | Quadros |
|---|---:|
| `BLOCS.CMP` | 1.345 |
| `TROOPS.CMP` | 2.848 |
| `BUILDING.CMP` | 611 |
| `CREATURE.CMP` | 1.920 |
| `INVENTE.CMP` | 72 |
| `MENU.CMP` | 40 |
| `OTHERS.CMP` | 4.517 |
| `VEHICULE.CMP` | 915 |

O agregador do jogo concatena seis bancos gráficos; os demais são carregados
separadamente. IDs de gráficos no motor não devem ser presumidos iguais aos
índices locais de cada arquivo. Para o terreno de `BLOCS`, o acesso confirmado
é `quadros[id - 1]`, com tiles de 32 × 32 pixels.

## PIE: paleta parcialmente recuperada

| Offset | Tamanho | Conteúdo observado |
|---|---:|---|
| `0` | 3 | Assinatura ASCII `Pie` |
| `3` | 4 | Fora do escopo do leitor de paleta |
| `7` | 2 | Quantidade de cores, 256 |
| `9` | 768 | Componentes RGB, 256 triplas |

A expansão usada para cada componente é `v = byte & 63`; se `v == 0`, resulta
zero; caso contrário, `4*v + 3`. Nos índices de cor **16 a 254**, o resultado de
`PLATGAME.PIE` coincide byte a byte com a paleta em `CHARGE.LZS`, offset 12.
Os índices 0..15 e 255 não foram declarados equivalentes. Isso valida a paleta
utilizada aqui, não constitui um decodificador completo de PIE ou LZS.

## ETA V0.3: cabeçalho e camadas

Evidência principal: [carregador_mapa.asm](../evidencias/carregador_mapa.asm).
O jogo pula quatro bytes; o leitor adiciona uma checagem explícita de `V0.3`.

| Offset | Tamanho | Campo | Confiança |
|---|---:|---|---|
| `0x00000` | 4 | Assinatura `V0.3` | Confirmado nos 38 mapas |
| `0x00004` | 65.536 | Camada de atributos, `u8[256×256]` | Layout confirmado; bits não decifrados |
| `0x10004` | 131.072 | IDs de terreno, `u16[256×256]` | Confirmado |
| `0x30004` | 65.536 | Camada denominada objetos, `u8[256×256]` | Leitura confirmada; catálogo parcial |
| `0x40004` | 65.536 | Camada denominada variantes, `u8[256×256]` | Leitura confirmada; semântica parcial |
| `0x50004` | 8 | Quatro valores do recurso interno 1 | Confirmado pela chamada a `0x46799c` |
| `0x5000c` | 8 | Quatro valores do recurso interno 2 | Confirmado |
| `0x50014` | 8 | Quatro valores do recurso interno 0 | Confirmado |
| `0x5001c` | 2 | Largura jogável | Confirmado |
| `0x5001e` | 2 | Altura jogável | Confirmado |
| `0x50020` | 16 | Quatro pares `u16 x, u16 y` de origem da visualização | Uso no renderizador confirmado |
| `0x50030` | variável | Primeiro bloco indexado | Ver sequência abaixo |

A posição física de uma célula é `y*256 + x`. A largura jogável apenas recorta
a região utilizada. A camada de atributos não é tratada como uma máscara de
caminhabilidade completamente conhecida; `atributo == 0` é a simplificação do
protótipo preexistente.

O carregador transforma entradas `0x36` da camada de objetos em `0x42`, ajustando
a variante correspondente para 1 (`0x46c3f6..0x46c404`). Os relatórios preservam
os valores originais e contam as conversões na área jogável; a rotina original
percorre a grade inteira de 65.536 células.

Os recursos são mantidos pelos números internos 1, 2 e 0. A associação entre
esses números e comida/pedra/peças ainda precisa de uma referência direta no
código da economia; o formato não assume essa correspondência pela aparência
dos valores iniciais.

### Blocos variáveis, na ordem de leitura

`N` e `S` abaixo são `u16`. Um bloco indexado contém `N,S`, depois `N` repetições
de `u16 índice` e `S bytes`. Um bloco simples contém `N,S`, seguido de `N*S` bytes.
Os nomes numéricos preservam a ausência de identificação semântica.

| Bloco | Formato no disco | Rotina |
|---|---|---|
| Estruturas | Indexado, `S=204` no corpus | `0x46c517` |
| Unidades | Indexado, `S=784` no corpus | `0x46acbf` |
| Tabela 47534a | `N` seguido de `N*4` bytes | `0x47534a` |
| Tabela 47c24d | Simples, `S=8` no corpus | `0x47c24d` |
| Tabela 47bcc7 | `N` seguido de `N` pares `u16,u32` | `0x47bcc7` |
| Tabela 47c04a | Simples, `S=10` no corpus | `0x47c04a` |
| Tabela 458b05 | Simples, `S=10`, `N=10` no corpus | `0x458b05` |
| Bytes descartados | 16 bytes, quatro grupos de quatro leituras | `0x47c30f` |
| Listas por jogador | 4×100 registros de `u16,u8` = 1.200 bytes | `0x47c404` |
| Tabela 47ac30 | Simples, `S=6`, `N=100` no corpus | `0x47ac30` |
| Sufixo não consumido | 917.504 bytes em todos os arquivos | Fora desse caminho de carga |

O relatório de cada mapa registra início, fim, tamanho e quantidade dos blocos.
Na missão 1, o primeiro bloco tem um registro, o segundo tem 16, e o último
termina em `0x539c8`; o arquivo tem 1.259.976 bytes. A diferença é `0xe0000`.

### Unidade: formato do disco versus RAM

| Região no registro de 784 bytes | Tratamento por `0x46acbf` |
|---|---|
| `0x000..0x08b` | Copia 140 bytes para o início do registro em RAM |
| `0x08c..0x28b` | Pula 512 bytes no arquivo |
| `0x28c..0x30f` | Copia 132 bytes para o offset `0x08c` em RAM |

O resultado serializado ocupa 272 bytes em registros com passo de 276 bytes.
Há pós-processamento: o carregador ajusta vários campos depois da cópia. O
extrator não apresenta os bytes concatenados como estado final completo da RAM.
O byte 1 do registro é o tipo usado para consultar a tabela de atributos; os
nomes recuperados dos mapas são associados por esse índice.

O primeiro bloco é denominado estruturas porque seu destino é uma tabela
separada e seu uso é compatível com objetos construídos. A identidade e o layout
completo de cada campo desse bloco ainda precisam ser rastreados.

### Sufixo

O leitor anterior extrai uma camada de 131.072 bytes do final do arquivo e a
chama de terreno de base. Essa observação é útil, mas esta análise ainda não
atribui semântica completa aos 917.504 bytes finais. Não os confunde com lixo,
nem os inclui no trecho comprovadamente consumido por `0x46c2cf`.

## INI e textos

Os nomes e descrições da edição brasileira são lidos em Windows-1252; o byte
DOS `0x1a` pode marcar o final dos textos. Os JSON e Markdown gerados são UTF-8.
`RISING.INI` contém chaves francesas e nomes localizados. O parser independente
é mais estrito que a API Win32 para entradas inválidas e se destina ao corpus
observado; não promete emular todas as permissividades do parser do Windows.
