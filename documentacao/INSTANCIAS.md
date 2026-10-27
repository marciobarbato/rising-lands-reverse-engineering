# Instâncias de unidades: dono, posição e vida

Implementação em [`unidades.py`](../ferramentas/unidades.py). Os offsets abaixo
são relativos ao registro **em memória**, cujo passo é 276 bytes. No ETA, cada
entrada contém um ID de 16 bits seguido de 784 bytes. O carregador `0x46acbf`
copia 140 bytes, salta 512 e copia outros 132. Portanto, offsets a partir de
`0x8c` em memória correspondem a `offset + 512` no registro de disco. Os últimos
quatro bytes do passo de memória não vêm dessa cópia.

| Offset | Tipo | Interpretação | Evidência |
|---|---|---|---|
| `0x00` | u8 | Proprietário, ID bruto | Acessor `0x442045`; comparação com jogador atual em `0x410c0e..0x410c1e` |
| `0x01` | u8 | Tipo 0..25 | Acessor `0x442025` e indexação da tabela de tipos |
| `0x02` | u8 | Estado; zero falha no predicado de atividade | `0x441fff` |
| `0x08` | u16 | Célula atual: `x = valor & 255`, `y = valor >> 8` | `0x4421bf..0x4421de`; ocupação em `0x43eb64` |
| `0x7c` | u16 | Célula do passo de movimento | Comparação em `0x448fac`; transferida para `0x08` em `0x448f50` → `0x448704` |
| `0x7e` | u16 | Célula de destino passada à busca de caminho | `0x44930c` → `0x43b30b` |
| `0x88` | u8 | Estado do caminho | Despacho em `0x44930c` |
| `0x9a` | u16 | Vida | Leitura `0x45718a`, escrita `0x4571ae`, cura `0x457122` |
| `0xb0` | u8 | Alcance de ataque ao quadrado, truncado novamente para 8 bits | `0x46ae0e` |
| `0xbb` | u8 | Raio de visão, truncado para 8 bits | `0x46ade5`; consumidor `0x448905` |
| `0xbc` | u8 | Grupo, inicializado com `0xff` | `0x46ae2c`; operações de grupo ainda parciais |
| `0x102` | u16 | Campo inicializado com `RECHARGE` | Trecho final de `0x46acbf` |

IDs de proprietário observados: 0, 1, 2, 3, 4 e 200. Os nomes das facções não
foram associados. O código trata 4 e 200 de forma especial, inclusive em visão;
não se deve aplicar a eles automaticamente as mesmas regras dos jogadores 0..3.

## Valores do arquivo versus carga da missão

Para entradas consideradas ativas pelo predicado `0x441fff`, o carregador:

1. Define a vida como **100**, mesmo quando o arquivo traz outro valor.
2. Copia visão, alcance quadrático e recarga da tabela de tipos, com os truncamentos indicados.
3. Define grupo como 255 e limpa diversos campos auxiliares.
4. Define proprietário 0 para o tipo 16 e proprietário 4 para os tipos 20..24.

`apos_carga_parcial` nos relatórios reproduz somente os efeitos confirmados.
Não é snapshot da RAM: há chamadas auxiliares e campos ainda não interpretados.
Os 38 mapas contêm 2.604 entradas. Quatro têm vida 20 no arquivo e recebem 100
nesse caminho de carga. Os estados encontrados são 7 e 14. Há transições para
14 em rotinas de entrada em construções/veículos; seu significado completo
ainda exige investigação, especialmente antes de decidir visibilidade.

## Missão 1

As 16 entradas pertencem ao proprietário 0 e têm vida 100. Coordenadas em células,
com origem zero e passo vertical de 256 na codificação, independentemente da largura do mapa.

| IDs | Tipo | Posição (x, y) | Estado |
|---|---|---|---|
| 0 | Soldado | (7, 15) | 7 |
| 1 | Soldado | (9, 16) | 7 |
| 2 | Soldado | (8, 18) | 7 |
| 3..10 | Colono | (14, 12), todas as oito entradas | 14 |
| 11 | Incendiário | (11, 21) | 7 |
| 12 | Construtor | (17, 16) | 7 |
| 13 | Fazendeiro | (14, 16) | 7 |
| 14 | Fazendeiro | (12, 16) | 7 |
| 15 | Arqueiro | (13, 19) | 7 |

Dados completos: [`missao01-unidades.json`](../relatorios/missao01-unidades.json).
Todas as missões: [`unidades-campanha.csv`](../relatorios/unidades-campanha.csv).
`mapas.json` inclui também o offset de cada registro e seu hash para conferência.

## Cura recuperada

`0x457122` soma o incremento à vida, armazena os 16 bits inferiores e compara
com a vida máxima do tipo, em `tipo + 0x08`. Se o resultado excede o máximo,
limita e retorna verdadeiro. Igualdade retorna falso. O máximo é 100 nos 26
registros originais desta edição e é preservado pelo carregador de INI.

O overflow acontece **antes** do limite: `65535 + 1` resulta em zero, não 100.
`curar_com_limite` conserva esse comportamento observado. Isso não implica
que o jogo normalmente forneça valores tão grandes. A função é uma reconstrução
isolada; dano de combate, cura periódica e gatilhos de morte não estão completos.
