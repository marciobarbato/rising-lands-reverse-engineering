# Máquina completa de avanço e expiração dos projéteis

[maquina_projeteis.py](maquina_projeteis.py) completa o despacho de
`ProjectileAvance` e traduz a ordem de `ProjectileCalcul`. Reutiliza o pool,
a linha, a animação e os pedidos de impacto já recuperados. A aritmética de
dano continua no backend existente. Nenhuma integração foi aplicada ao mundo,
ao movimento, à economia ou ao desenho.

## Endereços e evidências

| Endereço | Rotina ou trecho | Resultado desta etapa |
|---|---|---|
| `0x46EAF8` | `ProjectileAvance` | `MaquinaProjeteis.avancar`: despacho dos 256 bytes de tipo |
| `0x46EB47` | Tipo 33 | Sorteio da célula, criação do filho e pedido de dano |
| `0x46EEAD` | Tipo 28 | Duração u16, raio e pedido de extinção |
| `0x46EEE7` / `0x46EEF9` | Tipos 24/25 | Dano no quadro 32, com efeito adicional no tipo 25 |
| `0x46EF37` / `0x46EF4E` | Expirações | Comparação exata do quadro com 32/16 |
| `0x46EF58` | Tipos 29/30 | Espera enquanto quadro menor que 12, depois avanço linear |
| `0x46F088` | Chegada do tipo 30 | Círculo de raio 7, dano e filhos por célula |
| `0x46FBB6` | Efeitos temporários | Desativação antes do sorteio e de `CreerExplosion` |
| `0x46FC0F` | `ProjectileCalcul` | Animação geral, 30 varreduras e limpeza de +01 |
| `0x47474F` | `SortilegeGetTempsFin` | Consulta original observada; callback em Python |
| `0x475710` | `CreerExplosion` | Original executado; backend de dois buffers somente no teste |
| `0x476E82` | `EteintTerrain` | Argumentos/retorno observados, sem células iluminadas no ensaio |

O corpo de [Avance](evidencias/0046eaf8.asm) e o de
[Calcul](evidencias/0046fc0f.asm) já estavam exportados. Esta etapa acrescenta
as três evidências de duração/explosão/extinção ao
[manifesto](evidencias/manifesto.json), agora com 88 intervalos.
`EteintTerrain` retorna pelo epílogo compartilhado em `0x476E7B`, já contido
na evidência de `IllumineTerrain`; a bancada permite esse caminho original.

## Despacho confirmado de Avance

`avancar(indice)` não consulta +02. O chamador normal, Calcul, faz esse filtro.
As comparações de expiração abaixo são de **igualdade**, não `>=`. Se o quadro
já passou do limite, esse ramo não expira naquela chamada.

| Tipos | Condição e sequência |
|---|---|
| 0, 35..255 | Nenhuma escrita ou efeito |
| 1..5, 9..13, 17, 20..23 | Avanço linear e chegada da [etapa anterior](AVANCO_PROJETEIS.md) |
| 29/30 | Mesmo núcleo linear somente com +18 >= 12; chegada de 30 descrita abaixo |
| 6..8, 18/19, 34 | +18 == 32: limpa +02, sorteia efeito e chama `CreerExplosion` |
| 14..16 | +18 == 16: limpa +02 |
| 24 | +18 == 32: wrapper de dano, depois limpa +02 |
| 25 | +18 == 32: wrapper de dano, sorteio, `CreerExplosion`, depois limpa +02 |
| 26/27 | +18 == 8: limpa +02; o dano imediato de 26 já ocorreu em Set |
| 28 | +18 == duração u16 da magia 0: consulta raio, chama `EteintTerrain`, limpa +02 |
| 31/32 | +18 == 32: limpa +02 |
| 33 | +18 == 20: sorteio e impacto descritos abaixo |

Nos efeitos temporários, `56 + (Random % 6)` produz o tipo 56..61, com divisão
sem sinal. O marcador de Random é `0x2E` no grupo 6..8/18/19/34 e `0x2D` em 25.
O destino de `CreerExplosion` é a palavra +16. O pai de tipo 25 permanece
ocupado durante essa chamada; no primeiro grupo, já está desativado.

O tipo 28 captura o quadro **antes** de `SortilegeGetTempsFin(0)` e compara
o byte expandido com a palavra inteira retornada. Duração 256/65535 não é
truncada para oito bits e nunca iguala o quadro. Quando há igualdade, captura
o byte baixo de +20 antes de consultar `SortilegeGetRayonEffet(0)` e solicita:

```text
EteintTerrain(alvo_u16, raio_u16, atacante_byte_baixo)
```

O tipo 28 mantém +02 durante esse efeito e só o limpa no retorno. O significado
do terceiro argumento continua bruto: a pesquisa não o converte em um jogador.

## Tipo 30: círculo e ordem dos efeitos

Na chegada, escreve **15** no byte global `0x4DFB44`, representado pelo campo
local `MaquinaProjeteis.campo_4dfb44`. Seu uso visual ou temporal não foi
identificado nesta etapa; não se atribui um nome como tremor de câmera.

Captura a célula alvo +16 e percorre linhas crescentes de y, com x crescente
dentro de cada linha. Inclui somente coordenadas 0..255 e distância quadrada
ao centro `<= 49`. No interior da grade, são **149 células**. Os limites são
os da célula u16, independentemente das dimensões do mapa carregado.

Para cada célula, preserva esta ordem:

1. `InfligeDegat(celula, 4, atacante_u16, tipo_atual, 0)` diretamente.
2. `Random` com marcador `0x2F`, escolhendo tipo `6 + resultado % 3`.
3. Busca a primeira posição livre e, se houver, chama Set do filho.

Não existe um pedido de dano central adicional. O filho usa a célula corrente
como origem, mas conserva destino +16, modo, atacante, direção e flag do pai;
dx/dy são zero. O tipo do pai e seus argumentos são relidos nos pontos do
original. O pai só é desativado depois de terminar o laço inteiro. Pool cheio
não evita consumo de RNG nem pedidos de dano.

O cursor deste laço usa a largura da linha corretamente. A diferença
`256-altura` observada nos efeitos 20/22/29 pertence àquele outro trecho e
continua preservada na implementação anterior.

## Tipo 33: filho com destino antigo, dano no destino escolhido

No quadro 20, captura +16 antes da primeira consulta Random (`0x29`). Resultado
ímpar conserva a célula. Resultado par escolhe dentro de um retângulo 3×3
centrado nela e recortado em 0..255: consulta **y primeiro** (`0x2A`, módulo
altura) e depois x (`0x2B`, módulo largura). Esse retângulo inclui o centro,
portanto um resultado par também pode conservar a célula original.

Depois consulta `Random(0x2C)` e tenta criar filho 6/7/8 na célula escolhida.
Nessa chamada, o destino +16 do pai **ainda é o antigo**. Só depois da tentativa
de Set escreve a célula escolhida em +16, chama `ProjectileInfligeDegat` e
desativa o pai. Essa ordem vale também quando não há slot livre.

Os marcadores não são limites de sorteio: `Random` ignora EAX de entrada.
O Python recebe seus resultados por callback, sem duplicar o gerador.

## Calcul: pool vivo em 30 passagens

`calcular(incremento_animacao)` corresponde a uma chamada de `0x46FC0F`:

1. Chama a animação para os **100 slots**, ativos ou não, em ordem de ID.
2. Executa exatamente 30 passagens. Em cada passagem, visita os IDs 0..99 e
   chama Avance se o registro naquele momento tem +02 != 0 e +01 == 0.
3. Ao fim de **cada** passagem, limpa +01 dos 100 slots, incluindo os inativos.

Não faz uma cópia prévia da lista de ativos. Filhos em IDs ainda não visitados
podem ser processados na mesma passagem quando Set deixa +01=0. IDs já
visitados esperam a próxima passagem. +01 inicial não zero suprime apenas a
primeira passagem, se nenhum efeito voltar a escrevê-lo. A animação inicial
acontece antes das criações; um filho novo não a recebe retroativamente.

O número 30 é confirmado pelo laço. Não determina 30 quadros por segundo,
30 ticks reais ou duração em segundos. O chamador global e o desenho continuam
fora desta entrega.

## Validação diferencial

[test_maquina_projeteis.py](test_maquina_projeteis.py) acrescenta seis contratos
e seis testes diferenciais. A comparação cobre os 5.600 bytes do pool, o byte
`0x4DFB44`, dois buffers de 65.536 bytes, a ordem de IDs processados, a atividade
do pai durante efeitos e todos os argumentos e resultados de consultas.

Esta etapa soma **9.235 execuções x86 delimitadas**. A regressão completa
passou com **102 testes e 213.506 execuções**, zero falhas, erros ou ignorados.
Sem emulação, passam 38 contratos e os 64 diferenciais ficam explicitamente
ignorados. A contagem inclui fatias de uma mesma chamada, conforme descrito abaixo.

| Comparação | Execuções delimitadas |
|---|---:|
| Todos os bytes de tipo e dez quadros | 2.560 |
| Tipo 30: círculo, recorte e saturação | 1.734 |
| Tipo 33: célula e saturação | 60 |
| Tipo 28: duração/argumentos | 70 |
| Calcul: inativos e filhos antes/depois do pai | 2.974 |
| Calcul misto | 1.837 |

- 2.560 cenários: 256 tipos × dez quadros, incluindo limites e memória bruta.
- 18 chegadas do tipo 30: nove centros, com zero ou 99 slots inicialmente livres;
  verificação independente da quantidade de células do círculo.
- 60 casos do tipo 33: seis centros, cinco sementes e pool livre/saturado.
- 70 casos do tipo 28: cinco durações, sete quadros e dois atacantes.
- Calcul com pool inteiramente inativo e 27 chamadas encadeadas, variando ID
  do pai e +01, incluindo filhos antes/depois do pai e reutilização de slots.
- Um Calcul misto com área, sorteio, expiração, extinção e criação de filhos.

O RNG e as chamadas x86 internas executam as instruções originais. A bancada
observa os retornos de Random e os fornece como entrada externa do modelo,
comparando quantidade, marcadores, ordem e uso. Não substitui CALLs ou instrui
o x86 a seguir os resultados Python.

O tipo 30 pode chamar o dano 149 vezes, e Calcul pode executar muitos Avance.
Para manter limites verificáveis, a emulação para antes de Avance e de cada
célula aceita do tipo 30. Retoma a instrução parada sem alterar registradores,
pilha ou memória; cada fatia tem limite de um segundo/500.000 instruções,
com guarda adicional de 20.000 retomadas. O relatório conta **cada fatia** como
uma execução x86 delimitada, não como uma chamada completa nem cada CALL.

Os totais por teste e da regressão estão em
[validacao-emulada.json](validacao-emulada.json) e
[validacao-local.json](validacao-local.json). Para reproduzir nesta pasta:

```sh
python3 -B validar.py
python3 -B validar.py --emular
```

Limites: o dano original executa com grade vazia e 800 unidades inativas.
`EteintTerrain` usa dimensões zero e raio 0..7: confirma chamada e retorno,
sem validar alteração de iluminação em células. `CreerExplosion` executa o
corpo original, que só grava tipo/quadro se o byte de efeito da célula estiver
livre; o backend equivalente de dois buffers existe **somente no teste**.
Isso não valida renderização, duração visual, vítimas, construções ou gameplay.
Callbacks que alterem arbitrariamente o pool durante uma consulta não foram
submetidos a uma matriz diferencial completa.

## Integração posterior

Usar `MaquinaProjeteis(pool, aleatorio, tempo_magia, campo_4dfb44)` com o mesmo
`PoolProjeteis` da emissão. Fornecer `tempo_magia(id) -> u16`,
`pool.raio_magia(id) -> u16`, `aleatorio(marcador) -> u32` e o backend do pool
para `InfligeDegat`, `CreerExplosion` e `EteintTerrain`. Os efeitos de Set
`DecouvreTerrain`/`IllumineTerrain` continuam necessários quando alcançados.

Não chamar Anim novamente junto de `calcular`: a máquina já executa a varredura
de animação. Não substituir as 30 passagens por um Avance por slot. Conservar
a API parcial `avancar_linear` para seus callers existentes; ela ainda recusa
tipos fora dos 16 anteriores. A máquina completa usa o mesmo núcleo interno
e acrescenta o despacho de chegada de 30. Detalhes de adaptação para o chat
principal estão em [INTEGRACAO.md](INTEGRACAO.md).
