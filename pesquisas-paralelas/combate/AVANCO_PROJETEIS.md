# Avanço linear, animação lógica e distribuição do impacto

Implementação em [avanco_projeteis.py](avanco_projeteis.py), sobre o pool
independente de [projeteis.py](projeteis.py). Esta etapa cobre o voo linear
e a chegada dos tipos **1..5, 9..13, 17, 20..23 e 29**. Não integra unidades
ao movimento, não desenha sprites e não duplica a aritmética de dano.

## Rotinas recuperadas

| Endereço | Símbolo | Tradução / domínio |
|---|---|---|
| `0x46E52C` | `ProjectileAnim` | `animar_projetil`: todos os 256 valores do byte de tipo |
| `0x46E5FE` | `ProjectileInfligeDegat` | `infligir_dano_projetil`: centro e vizinhos, delegando cada `InfligeDegat` |
| `0x46EAF8` | `ProjectileAvance` | `avancar_linear`: os 16 tipos indicados, com chegada e criação de filhos |
| `0x46EF66` | Trecho do avanço | Contador, filho secundário, linha e acumulador |
| `0x46FB1A` | Despacho de chegada | Diferencia dano, efeitos de chegada e desativação |
| `0x46F4DE` | Chegada dos tipos 20/22/29 | Dano e tentativas de criar efeitos em área |
| `0x46FAD8` | Chegada do tipo 1 | Dano e tentativa de criar um efeito 6/7/8 |
| `0x4704DC` | `Random` | Executado no x86; permanece consulta externa em Python |

O [manifesto](evidencias/manifesto.json) registra hashes e limites dos bytes
originais. Foram exportados os corpos de Anim, InfligeDegat e Avance, além de
Random. **Exportar o corpo inteiro de Avance não significa traduzi-lo inteiro.**
Os tipos fora do domínio de `avancar_linear` causam `NotImplementedError`
antes de qualquer escrita, mesmo se o ramo nativo desse tipo seria um no-op.

## Animação lógica: +18 e o byte global de incremento

`animar_projetil(registro, incremento)` recebe uma view mutável de 56 bytes;
`incremento` representa o byte em `0x508F7C`. Não altera o estado global e não
consulta +02. O próprio `ProjectileCalcul` chama Anim para todos os 100 slots,
incluindo os inativos.

| Tipo | Atualização de +18 |
|---|---|
| 1..5, 17 | `(quadro + incremento_u8) & 3` |
| 20..23 | `(quadro + incremento_u8) & 7` |
| 29/30, quadro menor que 12 | `quadro+1`, ignorando o incremento global |
| 29/30, quadro pelo menos 12 | `(quadro+1)%20`; se resultado zero, substitui por 12 |
| 6..8, 14..16, 18/19, 24..28, 31..34 | Incremento de um em u8 |
| 0, 9..13, 35..255 | Preserva o quadro |

A expressão dos tipos 29/30 é calculada em 32 bits: quadro 255 vai para 16,
não para zero. No ciclo normal, os quadros passam de 0 a 12 e depois circulam
em 12..19. Quadros externos fora desse ciclo conservam o comportamento bruto
do original, sem normalização adicional.

Isso traduz contadores do registro, não a seleção de imagens ou o desenho.
Não altera os arquivos ou o trabalho do chat de gráficos.

## Ordem de um avanço linear

`avancar_linear(pool, indice, aleatorio)` executa a sequência abaixo:

1. Tipo 29 retorna imediatamente enquanto +18 é menor que 12.
2. Incrementa +03 em oito bits, incluindo wrap de 255 para zero.
3. Se +19 não zero e +03 **igual** a +04, tenta criar o tipo seguinte.
4. Se +34 não zero, avança a linha uma vez e, quando +23 não zero, soma
   `u16(+28)` ao acumulador dword +24, com wrap de 32 bits.
5. Se +34 **já era zero** nesse ponto, processa a chegada.

Portanto, o despacho que faz +34 passar de 1 para 0 ainda não aplica o impacto.
O próximo despacho faz isso. Os ramos lineares examinados não verificam
obstáculos, ocupação ou alvo em movimento no meio da trajetória: preservam o
alvo +16. Isso não é uma afirmação sobre todos os tipos do jogo.

O incremento de +24 é **sem sinal**, mesmo quando `ProjectileLineaire` produziu
uma palavra +28 com bit 15 ligado. O preparo e o incremento têm interpretações
assinadas distintas; a tradução mantém ambas.

### Criação secundária

A tentativa chama Set na primeira posição livre com:

```text
tipo = (tipo atual + 1) & 255
origem = +14, alvo = +16, modo = +1F, atacante = +20, direção = +22
dx = s16(+10), dy = s16(+12), flag = +23
```

Usa a **origem salva**, não a posição corrente +0C/+0E do pai. +19 é limpo
depois da tentativa, inclusive quando o pool está cheio. Não há nova tentativa
nem fila. +04 é o limiar dessa criação; não foi identificado como velocidade.

O corpo de Avance não testa atividade. Um teste adicional chama diretamente
um registro inativo e confirma que ele pode ser escolhido como o próprio filho.
Os campos são relidos após Set, inclusive o restante da linha. No uso normal,
o despachante de `ProjectileCalcul` filtra atividade antes de chamar Avance.
Se esse alias artificial produzir uma chegada do tipo 30, a tradução para no
limite explícito, após as escritas anteriores; não inventa o efeito ausente.

## Distribuição dos pedidos de dano

`infligir_dano_projetil(pool, indice)` chama primeiro:

```text
InfligeDegat(+16, +1F, +20, +22, +23)
```

Depois desse retorno, relê o tipo. Somente **20, 22 e 29** expandem a área:

| Ordem | Deslocamento | Condição |
|---:|---|---|
| 1 | Esquerda (−1, 0) | x > 0 |
| 2 | Direita (+1, 0) | x < 255 |
| 3 | Superior esquerdo (−1, −1) | x > 0 e y > 0 |
| 4 | Superior (0, −1) | y > 0 |
| 5 | Superior direito (+1, −1) | x < 255 e y > 0 |
| 6 | Inferior esquerdo (−1, +1) | x > 0 e y < 255 |
| 7 | Inferior (0, +1) | y < 255 |
| 8 | Inferior direito (+1, +1) | x < 255 e y < 255 |

Nos tipos 20/22, cada vizinho recebe modo +1F, atacante +20, direção +22 e
**flag zero**. No tipo 29, recebe **modo 4**, atacante +20, o byte de tipo
como direção e flag zero. O primeiro vizinho do tipo 29 usa o tipo salvo em
BL; os posteriores releem +00. As releituras após callbacks são preservadas.

Os limites são 0..255, independentes da largura/altura do mapa carregado.
O centro é chamado mesmo na borda. Não filtra inimigos ou aliados aqui;
esses critérios e a aplicação efetiva pertencem ao `InfligeDegat` existente.

## Chegada, RNG e efeitos

| Tipo que chega | Sequência |
|---|---|
| 1 | Pedido de dano; Random; tentativa de filho 6/7/8 na célula alvo; desativação |
| 9, 17, 21, 23 | Pedido de dano; desativação |
| 20, 22, 29 | Pedido de dano em área; Random e tentativa de filho por célula do laço; desativação |
| 2..5, 10..13 | Apenas desativação |

“Pedido de dano” usa o wrapper anterior, incluindo seus vizinhos quando
aplicável. O pai continua ativo até todas as tentativas terminarem; sua posição
não fica disponível antecipadamente para um filho. O efeito já inicializado
como tipo 26 continua aplicando dano em Set, conforme a etapa anterior.

`aleatorio(marcador) -> u32` fornece Random ao avanço. O marcador observado em
EAX é `0x30` na chegada do tipo 1 e `0x2F` nos tipos 20/22/29. **Não é um
limite de sorteio:** o corpo de Random ignora o EAX de entrada e atualiza o
estado global `0x497164`. O chamador divide o resultado por 3 e escolhe
`6 + resto`. Isso preserva a divisão sem sinal.

Random é consultado **mesmo sem espaço no pool**. O backend não deve trocar
a ordem “sortear, procurar livre, criar se possível” por um teste prévio de
capacidade. Os filhos usam a origem do efeito, destino +16 do pai, modo,
atacante, direção e flag do pai, mas dx/dy iguais a zero.

### Diferença confirmada nas bordas dos efeitos

Os tipos 20/22/29 iniciam um retângulo de até 3×3 células ao redor do alvo,
reduzido para duas colunas/linhas na borda. Depois de cada linha, o x86 soma
**256−altura** ao cursor, embora o cursor tenha avançado pela **largura**.
A instrução está em `0x46F587`.

Quando largura e altura diferem, as origens dos filhos se deslocam entre
linhas. Para alvo `(0,1)` / `0x0100`, os seis pedidos de dano têm células:

```text
256, 257, 0, 1, 512, 513
```

Já as origens dos seis efeitos criados são:

```text
0, 1, 255, 256, 510, 511
```

Ambas as sequências foram comparadas com o x86. A intenção dessa diferença e
seu aspecto numa partida real permanecem desconhecidos. Não corrigir o cursor
para uma grade ideal ao integrar a reconstrução.

## Validação e alcance das conclusões

Esta etapa acrescenta **12 testes**, seis de contrato e seis diferenciais,
com **21.780 execuções x86 delimitadas**. A suíte completa passou com
**90 testes, 204.271 execuções, zero falhas/erros/ignorados**. Sem emulação,
passam 32 contratos e os 58 diferenciais são ignorados explicitamente.

| Comparação | Execuções x86 |
|---|---:|
| Animação: 256 tipos, 12 quadros e quatro incrementos | 12.288 |
| Wrapper de dano: 256 tipos em nove células de borda/interior | 2.304 |
| Avanço de memória bruta, contadores e filhos | 1.536 |
| Chegada, bordas e zero/uma/nove posições livres | 300 |
| Reutilização do próprio registro inativo como filho | 16 |
| Animação e avanço desde Set até a chegada | 5.336 |

[test_avanco_projeteis.py](test_avanco_projeteis.py) compara os **5.600 bytes**
do pool, a ordem/argumentos de cada `InfligeDegat`, os marcadores/resultados
de Random e todos os parâmetros de Set. Inclui:

- Todos os 256 bytes de tipo na animação, quadros nas bordas e incrementos
  globais 0/1/2/255, com registros ativos e inativos.
- Todos os tipos no wrapper de dano; cantos/bordas e mapa sintético 16×12
  para comprovar que a expansão continua limitada à grade 256×256.
- Contadores u8, flags, palavras/posições brutas, soma dword e pool saturado.
- Chegadas com zero, uma ou nove posições livres, incluindo efeitos nas bordas.
- Sequências de Set até a desativação, com avanço e animação originais.
- Alias de um registro inativo escolhido como seu próprio filho.

O RNG nativo executa integralmente. A bancada observa seus retornos e os
fornece como **resultados da consulta externa** ao Python, comparando também
quantidade, ordem e uso. Não há troca de CALLs por mocks no x86 e não se alega
uma validação nova da fórmula do RNG Python.

O `InfligeDegat` nativo executa com grade vazia e unidades inativas. Os
testes validam a seleção das células e os pedidos, **não dano em vítimas,
morte ou efeitos em construções**. Nove buscas nativas de 800 unidades
precisam de um orçamento maior que o teste de impacto único: a bancada usa
até 500.000 instruções, mantendo um segundo por chamada e os intervalos
explicitamente permitidos.

Os totais reproduzíveis estão em [validacao-emulada.json](validacao-emulada.json)
e [validacao-local.json](validacao-local.json). Executar nesta pasta:

```sh
python3 -B validar.py
python3 -B validar.py --emular
```

## Integração e próximo trecho

Manter o pool separado e fornecer seu backend de `InfligeDegat`, reutilizando
a aritmética já existente. Passar a consulta RNG existente por callback;
nenhum módulo de caminhos ou economia é importado por esta implementação.
`animar_projetil` recebe explicitamente o incremento global de animação.

Não executar automaticamente “uma animação + um avanço” por frame do jogo:
as sequências do teste apenas comparam as mesmas chamadas nas duas versões.
O despachante `ProjectileCalcul` (`0x46FC0F`) tem uma ordem própria de 30
passagens e do portão +01, ainda não integrada nem traduzida nesta etapa.

Continuam pendentes os demais ramos de Avance: tipo 30 e sua área maior
(`0x46F088`), tipo 33 e seu impacto sorteado (`0x46EB47`), tipo 28 e
`EteintTerrain`, além dos efeitos temporários que chamam `CreerExplosion`.
As chamadas de desenho permanecem fora desta pesquisa. A leitura estática
localizou esses ramos; não se atribui equivalência dinâmica aos que não foram
executados pelos testes desta entrega.
