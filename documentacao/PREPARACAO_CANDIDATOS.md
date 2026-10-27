# Preparação do destino e etapas dos candidatos em Python

Esta etapa traduz `Chemin_Verouille` (`0x43b30b`) e duas partes de `CheminCalcul`:
a inspeção inicial de obstáculos e a escolha final entre os dois candidatos.
Também liga a serialização já reconstruída ao backend parcial. O movimento,
a visão e as mensagens continuam usando as implementações anteriores.

Nesta etapa inicial, o intervalo de construção `0x430b7e..0x43b073` ainda era
original emulado. Ele foi depois traduzido nas classes 1..3, conforme
[CONTORNOS.md](CONTORNOS.md). Estruturas codificadas e ordens de desbloqueio
a aliados foram traduzidas depois, em
[ESTRUTURAS_DESBLOQUEIO.md](ESTRUTURAS_DESBLOQUEIO.md).

| Implementação | Responsabilidade |
|---|---|
| [`preparacao_destino.py`](../ferramentas/preparacao_destino.py) | Contexto, passagem do destino, ajuste por anéis e comparação de regiões |
| [`candidatos_rota.py`](../ferramentas/candidatos_rota.py) | Vizinhança inicial, obstáculos, regiões, ocupantes, escolha e desempate |
| [`solucionador_misto.py`](../ferramentas/solucionador_misto.py) | Integração Python/x86 com checkpoints explícitos |
| [`bancada_preparacao.py`](../ferramentas/bancada_preparacao.py) | Referência original e transferência dos campos reconstruídos |

As evidências são as exportações existentes de
[`Chemin_Verouille`](../evidencias/ghidra/0043b30b.asm) e
[`CheminCalcul`](../evidencias/ghidra/0042f214.asm), confrontadas com os símbolos
franceses. Não foram inferidos novos nomes para os parâmetros não explicados.
O SHA-256 do original permanece
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

## Reproduzir

```sh
python3 -m unittest discover -s testes -p 'test_preparacao.py' -v
python3 ferramentas/demonstrar_desvios.py --misto
python3 ferramentas/validar.py --emular
```

O primeiro comando usa somente Python. Os outros ainda exigem Unicorn/JIT para
o núcleo de contorno, conforme [EMULACAO.md](EMULACAO.md). A demonstração grava
[`desvios-misto.json`](../relatorios/desvios-misto.json), com preparações,
inspeções iniciais, escolhas e otimizações identificadas separadamente.

A API atual é `SolucionadorParcialPython`. O nome anterior,
`SolucionadorComOtimizacaoPython`, continua disponível como alias. A referência
`SolucionadorOriginal` permanece sem essas substituições.

## Preparação do destino

O contrato observado recebe início em AX, destino em DX, unidade em BX, máscara
em CL e buffer/flags na pilha. A tradução calcula um `PreparacaoDestino`; a
ponte aplica seus campos à memória da bancada:

- Busca ocupada, unidade responsável, ponteiro da rota, dono, classe e máscara.
- Flags em `0x4e0f34/35`, sucesso/conclusão, status e alternativa inicial `0xffff`.
- Contagem ativa da rota zerada, com a cauda preservada.
- Início/destino em `0x4e0f44/46` escritos somente se a preparação ficar pendente.
  Uma recusa ou conclusão imediata conserva os extremos anteriores nesses globais.

Se a consulta de passagem no destino falhar, o original procura uma alternativa.
A direção dessa consulta usa os sinais entre início e destino solicitado e é
mantida durante a procura; não é recalculada para cada candidato.

### Anéis e casos de borda

Os raios vão de **1 a 29**. Antes de examinar cada anel, se a distância de
Chebyshev até a origem for igual ao raio, a origem é aceita como alternativa,
sem repetir sua consulta de passagem. Início igual ao pedido também retorna
a origem nesse ramo. Um pedido bloqueado fora do mapa retorna `0xffff`.

A ordem de exame é a linha superior, a inferior, a lateral esquerda e a direita.
Foram preservadas estas instruções do original:

- Nas linhas horizontais, o teste aceita `x == largura`.
- Nas laterais, a comparação superior usa `x_do_destino + j - raio` contra a
  **altura**, enquanto a inferior usa y.
- A célula examinada na lateral começa uma linha acima do y usado na condição.
  Por exemplo, no raio 1 de `(5,5)`, as duas últimas consultas repetem `(4,4)`
  e `(6,4)` depois das linhas superior e inferior.

A tradução não normaliza essas consultas para um anel geométrico presumido.
O caso foi comparado também em mapas retangulares, onde x e y têm limites diferentes.

Depois do ajuste, a comparação de região resolve uma camada de ocupação. Para
unidade, lê `0xfa + subcélula*2`; para estrutura, lê `0xcc + subcélula*2` no seu
registro. Não resolve recursivamente o valor encontrado. O teste de limites e
regiões precede o tratamento de `0xffff`: em mapas menores que 256×256, esse
sentinela normalmente produz status 7; com regiões iguais e coordenada dentro
de 256×256, pode chegar ao status 6.

| Situação | Status | Concluída | Sucesso |
|---|---:|---:|---:|
| Pedido livre, mesma região, células distintas | 1 | 0 | 0 |
| Alternativa encontrada, células distintas | 2 | 0 | 0 |
| Início igual ao destino efetivo | 1 ou 2 | 1 | 1 |
| Limites/regiões recusados | 7 | 1 | 0 |
| Sentinela depois de passar no teste de região | 6 | 1 | 0 |

## Início dos candidatos

O trecho `0x42f247..0x430b7e` foi condensado a partir das consultas de passagem
repetidas no x86. A classe 1 examina oito vizinhos nas direções ímpares. As demais
classes usam doze posições ao redor da pegada de quatro células; a tabela foi
extraída de `0x496228` e sua correspondência de direções de `0x496288`.

Cada recusa pode contribuir para:

1. O obstáculo inicial mais alinhado ao destino. A diferença de direção é
   normalizada no círculo de 16 ou 12 posições; empate conserva o primeiro.
2. Uma lista de regiões/ocupantes bloqueadores, com duplicatas e região da
   origem descartadas. A palavra da região da origem vem do u16 `0xfa` da unidade.
3. Um registro de dez bytes para ocupantes, conservando a preferência por
   adversários. A relação de aliança desse registro parte do **dono do ocupante**
   para o solicitante, preservando a assimetria da tabela.

Ocupantes com bit de classe 4 podem acrescentar as quatro subcélulas à lista.
As partes inativas dos buffers e da lista não são limpas. A grade auxiliar de
cores e os registros de estruturas foram acrescentados em
[ESTRUTURAS_DESBLOQUEIO.md](ESTRUTURAS_DESBLOQUEIO.md), removendo a recusa inicial.

Se nenhuma posição consultada estiver livre, a integração Python limpa a rota,
conclui sem sucesso e devolve status 8. O controle do movimento entra na espera
e solicita nova busca depois do contador já descrito em [NAVEGACAO.md](NAVEGACAO.md).

## Seleção final e serialização

`selecionar_candidato` traduz `0x43b073..0x43b2a9`. O custo `0xffff` marca a
contagem do respectivo buffer como 255. Quando os dois contadores são 255,
os flags e os registros de ocupantes podem selecionar os ramos de status 4/5.
Foram conservados dois comportamentos incomuns:

- As comparações `CMP AL,AL` em `0x43b11b` e `0x43b1e9` fazem o primeiro registro
  elegível prevalecer quando ambos existem.
- Alguns desses ramos escrevem a contagem no **segundo** buffer, mesmo quando
  selecionam o primeiro. A tradução preserva essa escrita e os dois buffers.

Nos demais casos, o menor custo u16 vence. No empate, `0x4704dc` avança o gerador
em `0x497164`; o primeiro candidato vence se os dois bits baixos forem zero,
caso contrário vence o segundo. O contador 255 selecionado produz status 3.
A recorrência traduzida conserva divisão sem sinal e overflow de 32 bits.

A otimização Python recebe o candidato selecionado. A serialização inverte
suas células ativas para consumo pela unidade e preserva a cauda da rota de
saída. Sucesso/conclusão são gravados como no original.

## Integração e cobertura

Na integração inicial, o backend parava em `0x42f247`, preparava a vizinhança
em Python e retomava o original até `0x43b073`. Esse corpo agora também é Python
nas três classes. A bancada mista conserva o prólogo/guardas e o epílogo original
em `0x43b300`; o backend independente de [CONTORNOS.md](CONTORNOS.md) dispensa
essas chamadas x86.

Os testes diferenciais incluem 288 preparações isoladas, 240 inspeções iniciais,
400 escolhas e 78 buscas completas nos três mapas para os 26 tipos, além de
um caso cercado com status 8. Conferem os campos de contexto, a preservação
dos extremos anteriores, buffers completos, regiões, registros e locais usados
no checkpoint. A referência e a tradução partem do mesmo estado anterior;
os resultados nativos não são reaproveitados para preencher uma escrita ausente.

Na etapa de preparação, a suíte passou com **144 testes e 32.623 execuções x86 delimitadas**,
sem falhas, erros ou testes ignorados. Sem emulação, passam 70 testes e os
74 opcionais ficam explicitamente ignorados no relatório local.

Os trajetos integrados continuam conferindo cada atualização até a mensagem e
a retomada da tarefa, incluindo um obstáculo surgindo durante o percurso.
Na parede com passagem, os custos observados foram `[65535, 7]`, com seleção do
segundo candidato. O trajeto continuou terminando em `(10,4)` na atualização 279.

O corpo de construção/contorno já foi traduzido nas três classes, incluindo
as grades auxiliares das estruturas e ordens a aliados bloqueadores. Falta ampliar
tráfego e inicializar os mapas reais por inteiro. As limitações de
combate, animação e partida completa permanecem em [CONTINUIDADE.md](CONTINUIDADE.md).
