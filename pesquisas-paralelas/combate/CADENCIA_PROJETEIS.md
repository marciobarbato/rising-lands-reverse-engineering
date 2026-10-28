# Chamador dos projéteis e apresentação do impacto

Esta continuação identifica os portões locais anteriores a `ProjectileCalcul`
e o consumidor do byte escrito pelo tipo 30. A tradução está em
[cadencia_projeteis.py](cadencia_projeteis.py), independente do laço do jogo e
do renderizador. Reutiliza os contadores já existentes em
`ferramentas/cadencia.py` **somente nos testes**; não duplica sua aritmética.

## Evidência e nível de certeza

| Endereço | Rotina/trecho | Resultado |
|---|---|---|
| `0x42C868` | `CalculGame` | Chamador identificado por símbolo e referências |
| `0x42D14C..0x42D184` | Retorno do caminho de menu | Traduzido e comparado por entradas de estado/flag |
| `0x42D2E3..0x42D2F0` | Portão de evento | Executa a consulta nativa `EvenementEnCours` |
| `0x42D3C0..0x42D3E1` | Portão final do bloco | Estado relido depois de processar jogadores/comandos |
| `0x42D3F0` | `CALL ProjectileCalcul` | Executado até retornar em `0x42D3F5` |
| `0x42D3F5` | `CALL CalculEnginNextEtape` | Fronteira posterior; atualização de unidades não executada |
| `0x475014..0x475041` | Contadores de `ProgIteration` | Original executado; tradução anterior reutilizada |
| `0x43F14F..0x43F220` | Início de `DDFlipPage` | Dois bytes globais e retângulo de origem traduzidos/validados |

[rastrear_cadencia_projeteis.py](rastrear_cadencia_projeteis.py) percorre a
seção BEGTEXT reiniciando a decodificação em cada símbolo e procura `CALL
rel32` para `ProjectileCalcul` também por byte. Encontra **um** candidato,
em `0x42D3F0`, confirmado no fluxo de `CalculGame`. O
[relatório](evidencias/rastreio-cadencia-projeteis.json) registra bytes,
endereços e hashes do EXE e dos símbolos. Isso não prova ausência de chamadas
indiretas ou de aliases arbitrários.

Nove intervalos foram acrescentados ao [manifesto](evidencias/manifesto.json),
totalizando 97. Ele também registra os 25 destinos da tabela de despacho de
`CalculGame` em `0x42C804`. Os trechos são bytes do EXE original, sem Ghidra.

## Três portões distintos

As funções Python reproduzem decisões em pontos específicos. **Não devem ser
combinadas como três condições de um único tick**, pois há caminhos distintos
e chamadas que podem modificar o estado entre elas.

### Retorno do caminho de menu: 0x42D14C

`continuar_apos_menu(estado_entrada, estado_atual, campo_4e0730)` permite seguir
para `0x42D2DE` somente quando:

- O byte de estado salvo na entrada de `CalculGame` era **16**.
- O byte atual `0x4E0730` não é zero.
- O estado atual `0x4E2F78`, relido após o tratamento de entrada, é **16 ou 18**.

O estado salvo fica no local `[ESP+0x104]` nesse ponto. Não substituí-lo pelo
estado atual. O significado geral de `0x4E0730` permanece bruto nesta entrega.
O caminho de teclado/menu anterior não é executado pela bancada.

A tabela de despacho encaminha estado 18 diretamente para `0x42D2DE`, sem
passar por esse portão. Há ainda um caminho de inicialização que alcança o
mesmo ponto por queda de fluxo após reiniciar contadores. Portanto, o teste
de menu não é uma condição necessária para todos os ciclos de simulação.

### Evento: 0x42D2E3

Depois da chamada em `0x42D2DE`, o original chama `EvenementEnCours`
(`0x4581B6`), que retorna o byte em `0x4E1B0E`. Se não zero, salta para o
epílogo `0x42D4EA`; se zero, continua em `0x42D2F0`.
`continuar_apos_evento(campo_4e1b0e)` traduz essa decisão, incluindo valores
diferentes de 0/1. A bancada executa a consulta nativa, sem substituir seu retorno.

### Estado relido após jogadores/comandos: 0x42D3C0

O laço intermediário processa jogadores/comandos e depois relê `0x4E2F78`.
`permitir_bloco_projeteis(estado_atual, campo_4e0730)` aceita:

```text
estado == 18  OU  (estado == 16 E campo_4e0730 != 0)
```

Outros estados saltam para `0x42D4E2`. O resultado não garante sozinho que a
rotina será chamada: a função começa **depois** dos portões anteriores. Os
comandos intermediários permanecem externos e não foram integrados ao modelo.

## Ordem relativa: projéteis antes das unidades

O bloco aceito contém estes CALLs consecutivos:

| CALL em | Destino | Símbolo |
|---|---|---|
| `0x42D3E1` | `0x469DCE` | `MessageBoxCalcul` |
| `0x42D3E6` | `0x45D015` | `GameNextFrame` |
| `0x42D3EB` | `0x45E944` | `CalculIconeAction` |
| `0x42D3F0` | `0x46FC0F` | `ProjectileCalcul` |
| `0x42D3F5` | `0x456DB5` | `CalculEnginNextEtape` |

A bancada executa o CALL de `0x42D3F0` e o corpo de Calcul, parando antes de
executar a chamada seguinte. Confere o pool inteiro. **Inferência de ordem**:
um projétil criado por uma unidade na chamada seguinte normalmente só recebe
essa varredura de Calcul na próxima passagem do chamador. Essa conclusão não
afirma que não existam outros emissores ou chamadas indiretas. Filhos criados
dentro do próprio Calcul continuam seguindo a ordem de índices já validada
em [MAQUINA_PROJETEIS.md](MAQUINA_PROJETEIS.md).

## O parâmetro de animação é o byte baixo do contador acumulado

`ProgIteration` incrementa o **dword** `0x508F7C`, depois chama `CalculGame`
e `AffGame`. `ProjectileAnim` lê somente seu byte baixo em `0x46E5B6` e
`0x46E5CA`. Assim, o parâmetro público chamado `incremento_animacao` nas
traduções anteriores representa esse valor acumulado, **não uma diferença de
tempo nem um incremento constante de 1**. O nome da API foi preservado.

Para os tipos 1..5/17, quadros iniciados em zero e ciclos 1, 2, 3, 4 produzem
quadros **1, 3, 2, 2**. Tipos 20..23 produzem **1, 3, 6, 2**. Os outros
grupos continuam usando suas próprias regras de animação. O teste de cadeia
compara incremento dos contadores, CALL de Calcul e pool, incluindo a passagem
255→256 e o overflow de 32 bits.

Há escritas adicionais do dword: `MenuNewSelect` em `0x42C6F9` e o caminho de
inicialização em `0x42D2BE`. Este último zera os três contadores antes de
continuar para a simulação; portanto não assumir que toda primeira atualização
recebe 1. Esses caminhos foram inspecionados estaticamente, sem executar seus
menus ou carregamentos.

O laço Windows e o filtro de desenho já estão descritos em
`documentacao/CADENCIA.md`. Esta etapa não atribui FPS fixo: **30 passagens de
Calcul não significam 30 quadros por segundo**.

## Consumidor de 0x4DFB44: deslocamento vertical de apresentação

O início de `DDFlipPage` (`0x43F14F`) lê o byte em `0x4DFB44`:

1. Se zero, deslocamento = 0; não lê a tabela nem avança seu índice.
2. Caso contrário, lê `tabela[índice]`, com tabela de 256 bytes em `0x4E1C18`
   e índice u8 em `0x4E1D18`.
3. Calcula `deslocamento = valor_byte % campo_4dfb44`, usando o campo anterior.
4. Incrementa o índice com wrap u8.
5. Se o contador global é par, decrementa `0x4DFB44` em um.

Não chama `Random(0x4704DC)` nesse trecho. A tabela e o índice são compartilhados:
`CalculGame` também os consome em `0x42D2F9..0x42D328`. A forma de preenchimento
da tabela não foi reconstruída; os testes fornecem tabelas sintéticas.

O campo de impacto limita o deslocamento, com valor máximo `campo-1`. Tipo 30
escreve 15, portanto limita o deslocamento dessa apresentação a 0..14. Se o
campo é 1, a consulta/avanço de índice ainda acontece, mas o deslocamento é
zero; em ciclo par, o campo passa a zero depois da consulta.

O decremento acontece **por execução de DDFlipPage com ciclo par**, não por
varredura dos projéteis. Apresentações só em ciclos ímpares não o reduzem;
duas apresentações no mesmo ciclo par podem reduzi-lo duas vezes. O divisor
de desenho pode alterar essa sequência. A bancada compõe o filtro existente
com o trecho original; não executa o renderizador ou o ciclo Windows inteiro.

### Retângulo preparado antes da chamada gráfica

`preparar_apresentacao_impacto` retorna um `PreparacaoImpacto` imutável com
os dois bytes atualizados, deslocamento y e o retângulo de origem
`(left, top, right, bottom)`. Para largura de tela diferente de 800:

```text
(0, deslocamento, largura_celulas*32, altura_celulas*32)
```

Para largura exatamente 800, usa `m = s8(byte_alto(dword_508f8d)) * 32`:

```text
(m, m+deslocamento, largura_celulas*32-m, altura_celulas*32-m)
```

`0x508F8D` é uma leitura **desalinhada** de dword; seu byte alto é assinado
pela instrução `SAR 24`. Não substituir por uma flag booleana. As dimensões
em células são palavras u16. Os testes incluem byte alto negativo e dimensões
extremas sem tentar normalizar retângulos degenerados do original.

O retângulo é passado à chamada indireta de cópia em `0x43F244`. O deslocamento
é aplicado à borda superior da origem, enquanto a inferior permanece fixa;
não representar isso como uma translação integral do retângulo. A bancada
para em `0x43F220`, antes da montagem/chamada gráfica. **Confirmado**: alteração
da origem vertical e decaimento do limite. **Interpretação visual**: mecanismo
compatível com tremor de impacto; seu aspecto final não foi observado no jogo.

A auditoria encontra ainda escritas de 20 em `0x41A430`, `0x41EE34` e
`0x41EF87`, respectivamente em símbolos de dano, venda e destruição de
construções. Não são traduzidas ou integradas aqui; o byte não é exclusivo
do tipo 30. A apresentação também tem callers fora do jogo em andamento,
registrados no relatório, portanto não presumir uma única chamada por ciclo.

## Validação e limites

[test_cadencia_projeteis.py](test_cadencia_projeteis.py) acrescenta **11 testes**:
cinco contratos e seis diferenciais. Compara:

- Todos os bytes de estado/evento, estados salvos distintos e flags 0/1/2/255.
- Todos os valores do campo de impacto, seis valores de tabela, quatro ciclos
  e dois índices, incluindo wrap 255→0 e tabela preservada.
- Todos os bytes altos do dword desalinhado, larguras 640/800/801 e dimensões
  normais/extremas; retângulo inteiro comparado com os quatro dwords da pilha.
- Contadores originais até Calcul e sua volta antes das unidades, com pool
  completo comparado e aritmética do contador reutilizada.
- Uma cadeia de impacto tipo 30 até a preparação da apresentação.
- Apresentações encadeadas em 120 ciclos com divisores de desenho 1/2/3/4.

| Comparação | Execuções x86 delimitadas |
|---|---:|
| Portões e estados salvos | 5.376 |
| Campo de impacto, módulo, paridade e índice | 12.288 |
| Retângulo e byte alto assinado | 1.536 |
| Contadores → CALL de Calcul → fronteira das unidades | 762 |
| Tipo 30 → preparação da apresentação | 47 |
| Sequências com divisor de desenho | 730 |
| **Total desta etapa** | **20.739** |

A regressão completa passou com **113 testes e 234.245 execuções x86
delimitadas**, zero falhas, erros ou ignorados. Sem emulação, passam 43
contratos e os 70 diferenciais são ignorados explicitamente. A contagem
inclui as pausas/retomadas da bancada de Calcul, conforme a etapa anterior.

Os resultados totais estão em [validacao-emulada.json](validacao-emulada.json)
e [validacao-local.json](validacao-local.json). Chamadas originais não são
substituídas. Os portões começam nos endereços declarados, com estado/local de
pilha fornecidos como entradas; isso **não valida o CalculGame inteiro**.
Permanecem fora: entrada de teclado/mouse, jogadores/comandos, chamadas de
unidades, vítimas/construções, APIs gráficas, preenchimento da tabela visual
e duração real em segundos. Não houve alteração nos módulos compartilhados.

Reprodução nesta pasta:

```sh
python3 -B extrair_evidencias.py
python3 -B rastrear_cadencia_projeteis.py
python3 -B validar.py
python3 -B validar.py --emular
```

## Orientação para o chat principal

Ao integrar, conservar o ponto de chamada de Calcul **antes** da atualização
das unidades e fornecer o byte baixo do contador atual, após os resets do
caminho escolhido. Os predicados de menu/evento/bloco servem aos seus pontos
originais; não antecipar a leitura do estado para antes dos comandos.

O helper visual retorna estado e retângulo sem modificar o pool ou desenhar.
Seu caller futuro deverá compartilhar a tabela/índice com os demais
consumidores e atualizar o mesmo byte que o tipo 30 escreve. O decremento
pertence à apresentação efetivamente executada. A adaptação ao renderizador
fica para o responsável por gráficos; esta pesquisa não a aplica.
