# Pool e preparação dos projéteis

Tradução independente em [projeteis.py](projeteis.py). Esta etapa continua a
fronteira `ProjectileInit` de `CalculAttaqueEngin`: recupera a seleção de um
registro livre, sua inicialização e o incremento linear. Não altera o movimento
de unidades, a economia, o desenho ou a aritmética de dano já reconstruída.

## Rotinas e evidência

| Endereço | Símbolo original | Python / contrato |
|---|---|---|
| `0x46E00A` | `ProjectileReset` | `PoolProjeteis.resetar`: limpa somente +02 |
| `0x46E02C` | `ProjectileExiste` | `existe`: byte bruto de atividade em AL |
| `0x46E422` | `ProjectileGetLibre` | `livre`: primeiro inativo, ou **100** |
| `0x46E44C` | `ProjectileInit` | `iniciar`: procura posição e chama Set se disponível |
| `0x46E208` | `ProjectileSet` | `definir`: escritas comuns, despacho de tipo e efeitos |
| `0x46E049` | `ProjectileLineaire` | `preparar_linha`: estado inteiro de Bresenham |
| `0x46E4CA` | `ProjectileCalculLineaire` | `calcular_linha`: no máximo um incremento |

As sete rotinas foram executadas diretamente do EXE original na
[bancada](bancada_projeteis.py). Assembly e hashes estão no
[manifesto](evidencias/manifesto.json), incluindo os 33 destinos da tabela em
`0x46E184` (tipos 1..33). Tipo 0 e tipos 34..255 executam somente as escritas
comuns: isso é um fato do despacho, não uma declaração de tipos válidos no jogo.

Evidência estática adicional, sem tradução nem execução completa nesta etapa:
`ProjectileAlloc` (`0x46DFA0`) pede 5.600 bytes e guarda o ponteiro em
`0x5080F0`; `LoadProjectile` (`0x46DFBA`) e `SaveProjectile` (`0x46DFE2`)
pedem 100 leituras/escritas sequenciais de 56 bytes. O conteúdo dos registros
inativos também participa desses laços. Não foi executado I/O nem inferido que
o alocador zera a memória.

## Pool, chamada e campos preservados

O pool tem **100 registros de 56 bytes**. `+02 != 0` significa ocupado.
`ProjectileExiste` não normaliza o resultado para 0/1. `Reset` zera apenas
esses 100 bytes; o conteúdo anterior dos demais campos permanece.

```text
ProjectileSet: AX=índice, DL=tipo, BX=origem, CX=alvo
  pilha: modo, atacante, direção, dx, dy, flag (seis posições de 32 bits)
  RET 24
ProjectileInit: AL=tipo, DX=origem, BX=alvo, CL=modo
  pilha: atacante, direção, dx, dy, flag (cinco posições de 32 bits)
  RET 20
```

Origem/alvo/atacante são u16, modo/direção/flag/tipo são u8 e dx/dy são s16.
Os argumentos na pilha ocupam quatro bytes, mas as rotinas leem apenas as
larguras indicadas. Os testes envenenam os bits altos para conferir isso.

`iniciar` usa a primeira posição com +02 zero. Se todas estiverem ocupadas,
retorna sem gravar nem emitir efeitos. Não há fila, substituição ou recuperação
do projétil mais antigo nesse corpo. A API Python retorna o índice escolhido
ou 100 por conveniência; **esse contrato não é atribuído ao EAX nativo após
uma criação**, porque Set altera o registrador. `definir` aceita sobrescrever
uma posição ocupada. Os índices Python devem estar em 0..99; o x86 usa AX sem
verificar o limite em Set/Existe.

| Offset | Escrita comum de Set / uso confirmado |
|---|---|
| +00..+03 | Tipo; 1; atividade 1; contador 0 |
| +04 | Preservado no caminho comum; limiar do contador em certos ramos |
| +05..+07 | Preservados |
| +08 dword | Posição compactada, escrita somente por preparação linear |
| +0C/+0E word | `(origem.x*32+dx, origem.y*32+dy)`, com wrap u16 |
| +10/+12 word | Deslocamentos dx/dy |
| +14/+16 word | Células de origem e destino |
| +18/+19 byte | Ambos zero; ramos específicos alteram +19 |
| +1A/+1C word | 12 e zero; ramos específicos substituem |
| +1E | Preservado |
| +1F/+20/+22/+23 | Modo u8, atacante u16, direção u8, flag u8 |
| +24 dword / +28 word | Ambos zero; alguns ramos substituem |
| +2A..+35 | Estado da linha; preservado se não houver preparo linear |
| +36/+37 | Preservados |

Nomes como atividade, célula e direção derivam das leituras/escritas e dos
chamadores já reconstruídos. A interpretação visual dos campos +18/+1A/+1C,
da flag +23 e do acumulador +24 ainda depende dos consumidores completos.

## Despacho por tipo

`P` na tabela significa **preservar o valor preexistente**. Os valores são os
resultados de Set; +24/+28 podem mudar durante a preparação linear.

| Tipos | Prepara linha | +01 | +04 | +19 | +1A | +1C | Outro efeito |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | sim | 0 | 15 | 1 | 12 | 10 | — |
| 2 / 3 / 4 | sim | 1 | 10 / 8 / 4 | 1 | 12 | 0 | — |
| 5 | sim | 1 | P | 0 | 12 | 0 | — |
| 9 | sim | 0 | 2 | 1 | 5 | 5 | — |
| 10 / 11 / 12 | sim | 1 | 2 | 1 | 5 | 0 | — |
| 13 | sim | 1 | 2 | 0 | 5 | 0 | — |
| 15 / 16 | não | 1 | P | 0 | 12 | 0 | +24=12800 se flag não zero |
| 17 | sim | 0 | 15 | 0 | 12 | 10 | — |
| 20 / 21 / 22 / 23 | sim | 0 | 15 | 0 | 20 | 10 | — |
| 26 | não | 1 | P | 0 | 12 | 0 | Dano imediato |
| 28 | não | 1 | P | 0 | 12 | 0 | Descoberta e iluminação |
| 29 / 30 | sim | 1 | P | 0 | 20 | 0 | — |
| Demais bytes | não | 1 | P | 0 | 12 | 0 | — |

**+04 não foi confirmado como velocidade.** Em
[0x46EF66..0x46F07C](evidencias/0046ef66.asm), `ProjectileAvance` incrementa
+03; se +19 não zero e +03 igual a +04, tenta criar outro projétil com
`tipo+1`, depois zera +19 mesmo se o pool estiver cheio. Por isso o código
Python chama a tabela de `limites_contador`. A finalidade gráfica dessa criação
(por exemplo, rastro) permanece hipótese; não foi implementada nesta etapa.

O [despacho de ProjectileCalcul](evidencias/0046fc0f.asm) tem 30 passagens e
usa +01 como portão antes de Avance, limpando-o em outro laço. Isso sustenta
que um incremento de `calcular_linha` não equivale a um tick. Esse despacho
não foi traduzido nem associado a uma duração em segundos.

## Linha inteira e limites numéricos

O alvo da linha é o centro da célula: `(32*x+16, 32*y+16)`. As diferenças
para +0C/+0E são truncadas para s16. Os sinais produzem passos horizontais
de ±1 e verticais de ±8192. O passo diagonal soma os dois.

O original compara os módulos como **palavras assinadas** (`CMP CX,DX; JLE`).
Assim, `abs(-32768)` continua representado por `0x8000` e é tratado como
negativo nessa comparação. A tradução conserva o comportamento, inclusive
quando ele não descreve uma linha geométrica normal. Não o corrige para
inteiros Python sem limites.

Para maior M e menor m escolhidos pelo teste original:

- +34 = M; +2C = passo axial; +2A = passo diagonal.
- +32 = 2m; +30 = 2m−2M; +2E = 2m−M, todos truncados para 16 bits.
- +08 = `s16(y)*8192+s16(x)`, truncado para 32 bits.
- Com +23 não zero: +24=0 e +28=`12800/s16(M)`, divisão com truncamento
  em direção a zero; se M=0, +28=12800. Com flag zero, a função isolada
  preserva +24/+28. Set já os havia zerado antes de chamá-la.

`calcular_linha` não faz nada se +34=0. Senão, usa o passo diagonal quando
`s16(+2E)>=0`, axial quando negativo, soma a correção correspondente ao erro
e decrementa +34. Extrai x com máscara 8191 e y com **SHR lógico de 13 bits**,
truncando y para u16. Não consulta atividade, +04, colisão ou alvo móvel.
Ao zerar o número de passos restantes, **não desativa o projétil**.

## Efeitos imediatos e limites da equivalência

Tipo **26** chama `InfligeDegat(alvo, modo, atacante, direção, 0)` durante Set.
Não espera a linha terminar. O Python exige `efeito_externo(nome, argumentos)`;
o backend deverá reutilizar a implementação de dano existente.

Tipo **28** faz, nesta ordem:

1. Consulta `SortilegeGetRayonEffet(0)` (`0x474734`).
2. Chama `DecouvreTerrain(alvo, (raio+2)&65535, atacante&255)` (`0x476851`).
3. Consulta **novamente** `SortilegeGetRayonEffet(0)`.
4. Chama `IllumineTerrain(alvo, raio, atacante&255)` (`0x476CB3`).

O terceiro argumento é o byte baixo do atacante recebido, **sem consulta de
dono da unidade** nesse caminho. Não substituir silenciosamente por um ID
de jogador inferido. O Python recebe a consulta `raio_magia(id)` separada dos
efeitos. Se um callback necessário faltar, lança `NotImplementedError` após
as escritas já feitas; não há rollback implícito.

Nos diferenciais, os corpos originais dessas chamadas são executados sem
substituições: dano com grade vazia; descoberta/iluminação com dimensões de
mapa zero e raio 0..10, de modo que os laços não visitem células. Comparam-se
ordem e argumentos dos efeitos e todos os bytes do pool. Isso **não valida
dano em vítimas, descoberta de células ou iluminação real**. O teste Python
adicional de raio 65535 confirma o contrato de wrap/consulta repetida, sem
alegar uma execução nativa desses laços para raios extremos.

## Validação

Esta etapa acrescenta **11 testes**, quatro de contrato e sete diferenciais,
com **12.196 execuções x86 delimitadas**. A regressão de combate totaliza
**113 testes, 234.245 execuções x86, zero falhas/erros/ignorados**.
Relatórios: [emulado](validacao-emulada.json) e [local](validacao-local.json).

| Comparação | Execuções x86 |
|---|---:|
| Reset, todas as posições livres e todos os bytes de atividade | 458 |
| Set: 256 tipos, flags 0/1/255, offsets extremos/aleatórios | 3.072 |
| Init: 256 tipos, posições 0/7/99 e pool cheio | 1.024 |
| Preparo linear: 2.240 casos, seguido de dois incrementos cada | 6.720 |
| Incremento: erro assinado, overflow da posição e contador | 80 |
| Trajetórias completas nos quadrantes/eixos/empates/coincidência | 530 |
| CalculAttaqueEngin → Init → Set, incluindo último slot e tiro duplo | 312 |

Cada diferencial local compara os **5.600 bytes**, para detectar escritas
indevidas em vizinhos e campos preservados. A cadeia de ataque compara também
os 276 bytes do atacante, os quatro globais de busca e as solicitações de
emissão. A ligação Python entre ataque e pool existe **somente no teste**;
não foi feita integração ao mundo do projeto.

Reprodução nesta pasta: `python3 -B validar.py --emular`, com o JIT local do
Unicorn permitido. Sem emulação: `python3 -B validar.py` aprova 43 contratos
e ignora explicitamente 70 diferenciais. Sementes fixas nos testes.

A continuação em [AVANCO_PROJETEIS.md](AVANCO_PROJETEIS.md) traduz
`ProjectileAnim`, `ProjectileInfligeDegat` e o avanço/chegada de 16 tipos
lineares. [MAQUINA_PROJETEIS.md](MAQUINA_PROJETEIS.md) completa os demais ramos
de `ProjectileAvance` e a ordem de `ProjectileCalcul`.
Não chamar `calcular_linha` uma vez por frame como substituição desses
consumidores. Consultas e aritmética de dano permanecem dependências explícitas.
