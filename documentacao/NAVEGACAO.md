# Navegação integrada ao movimento das unidades

`MundoNavegacao`, em [`navegacao_unidades.py`](../ferramentas/navegacao_unidades.py),
escolhe o próximo passo, desvia localmente e solicita uma rota quando necessário.
O passo escolhido usa o avanço físico, ocupação, visão, minimapa e mensagens já
reconstruídos em [AVANCO_CHEGADA.md](AVANCO_CHEGADA.md). As tarefas de grupo podem
emitir a ordem, aguardar a mudança de estado e retomar depois do movimento.

As consultas, a geração de regiões e o controle de navegação foram traduzidos
para Python. **A busca geral ainda executa as rotinas originais em Unicorn**,
por meio de `SolucionadorOriginal`, explicitamente fornecido ao mundo. Não há
uma tradução completa de `CheminCalcul` ou evidência suficiente para chamá-lo de
A*. O executável Windows não é iniciado; a bancada usa memória sintética,
intervalos de código declarados e limites de execução.

O backend opcional `SolucionadorParcialPython` já traduz preparação, ajuste,
inspeção inicial, seleção, teste de linha, otimização e serialização. O nome
anterior `SolucionadorComOtimizacaoPython` continua disponível como alias. Veja
[PREPARACAO_CANDIDATOS.md](PREPARACAO_CANDIDATOS.md) e
[OTIMIZACAO_CAMINHOS.md](OTIMIZACAO_CAMINHOS.md) para o contrato, a comparação
com a referência e as partes da busca que ainda continuam originais.

## Reproduzir

Execute dentro de `engenharia-reversa`:

```sh
# Desvio local: Python, sem Unicorn.
python3 ferramentas/demonstrar_desvios.py

# Inclui parede com passagem, parede fechada e destino bloqueado.
python3 ferramentas/demonstrar_desvios.py --original

# Preparação, início/seleção dos candidatos e otimização em Python.
python3 ferramentas/demonstrar_desvios.py --misto

# Suíte comum e suíte diferencial opcional.
python3 ferramentas/validar.py
python3 ferramentas/validar.py --emular
```

A opção `--original` exige as dependências e a permissão para memória JIT
descritas em [EMULACAO.md](EMULACAO.md). Os resultados ficam em
[`desvios-local.json`](../relatorios/desvios-local.json) e
[`desvios-original.json`](../relatorios/desvios-original.json).
O relatório identifica expressamente o uso do algoritmo original.

Na API, o desvio local usa `MundoNavegacao(largura, altura)`. Para habilitar
a busca geral, forneça `solucionador=SolucionadorOriginal()`. Cada mundo deve
ter sua própria instância do solucionador: os buffers internos pertencem a um
único contexto global de busca. Sem solucionador, a necessidade de busca geral
gera `NotImplementedError`.

## Evidências e consultas de passagem

| Endereço | Nome original | Uso nesta etapa |
|---|---|---|
| `0x44246e` | `EnginOccupeCase` | Consultar célula atual e célula reservada |
| `0x446693` | `ChercheIndiceEngin` | Localizar ocupante entre os 800 registros |
| `0x442668` | `EnginPeutPasser` | Consultar máscara e pegada; devolver até quatro candidatos |
| `0x448d08` | `EnginNextCase` | Escolher passo direto ou iniciar o pedido de busca |
| `0x448b9f` | `EnginNextCaseChemin` | Escolher célula da rota ou invalidá-la |
| `0x44930c` | `DeplaceEngin` | Despachar os estados de navegação |
| `0x449176` | `EnginDebloqueNextCase` | Tentar liberar passagem com ordens a outras unidades |
| `0x44330c` | `EnginChercheCaseLibre` | Procurar célula livre no ramo de desbloqueio |
| `0x42ee1c` | `Chemin_Remap` | Gerar componentes naturais e limitar o mapa |
| `0x4752b8` | `TerrainEstObstacleNaturel` | Classificar terreno por tile e objeto |

As novas exportações ficam em [`evidencias/navegacao`](../evidencias/navegacao)
e [`evidencias/regioes`](../evidencias/regioes). Elas complementam os trechos
anteriores de caminhos e movimento. O pseudocódigo automático conserva os
avisos de assinatura Watcom; as traduções foram conferidas com as instruções.
O hash do EXE original continua sendo
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

[`passagem_unidades.py`](../ferramentas/passagem_unidades.py) preserva as diferenças
entre os predicados do movimento e os da busca geral:

- `EnginOccupeCase` considera as células `0x08` e `0x7c`, estado 14 e modo
  `0xab`. Com máscara 1, qualquer modo não zero é excluído desse predicado.
- Os tipos 3, 11–16 e 25 ocupam quatro células: `c`, `c-1`, `c-257`, `c-256`.
  As subtrações da consulta são de 32 bits; a escrita da ocupação continua
  reduzindo a u16, conforme as respectivas funções originais.
- `ChercheIndiceEngin` exige estado vivo e byte `0x72` não zero. Entre ocupantes
  terrestres conserva o último candidato; um modo não zero pode encerrar a
  procura antes. O tipo 16 só participa com modo 50.
- `EnginPeutPasser` aceita ocupação própria e células sem os bits consultados.
  Nos demais casos coleta candidatos e verifica a exceção dos tipos 12/15
  contra determinados tipos adversários. A consulta não aplica dano.

A reserva do próximo passo retira a reserva antiga, reinsere a posição atual,
ocupa a célula escolhida e grava `0x7c` e a direção `0x90`. Se a passagem exigir
efeitos de atropelamento dos tipos 12/15, o modelo recusa a execução antes de
reservar o passo; esses efeitos de combate ainda não foram integrados.

## Movimento direto e estados de caminho

`EnginNextCase` calcula a direção `d` para o destino. As três tentativas do
original são **`d`, `d-2`, `d`**, com normalização em 1..16. A terceira repete
a primeira; não foi trocada por uma alternativa presumida. Se uma tentativa
bloqueada for exatamente a célula de destino, o destino é cancelado para a
célula reservada atual e a busca da própria unidade é liberada.

| Byte `0x88` | Comportamento reconstruído |
|---|---|
| 0 | Escolher passo direto quando deslocamentos forem zero; permitir física |
| 1 | Voltar a 0, sem avanço nessa atualização |
| 2 | Não executar ação nesse despachante |
| 3 | Esperar o contexto global livre e solicitar busca; um passo já iniciado pode continuar |
| 4 | Continuar cálculo ou tratar seu resultado |
| 5 | Escolher célula da rota e permitir física |
| 6 | Incrementar contador u8; quando igual a 20, voltar a 3 |

O estado 4 passa para 5 quando há sucesso. Com status 2, o ramo preserva a
atribuição do destino alternativo do original, sem reinterpretar o valor.
Uma falha com status 8 entra na espera 6. Outras falhas passam pelo desbloqueio
original; se ele não encontrar solução, o destino vira a célula `0x7c` e o
estado volta a 0. O backend copia de volta os registros alterados por eventuais
ordens a aliados. Esse ramo ainda precisa de cenários específicos de tráfego.

Ao consumir uma rota, a próxima célula vem do final ativo do buffer de 512 bytes.
Uma célula bloqueada ou rota vazia limpa `0x88/0x8b`, permitindo voltar à
tentativa direta e pedir outra busca. A contagem só diminui após a chegada física.
O modelo preserva também a parte inativa do buffer para comparação integral.

## Geração dos rótulos de região

A busca geral precisa de uma grade de regiões coerente com o terreno. Uma grade
zerada pode produzir resultados parciais que não contornam uma parede, mesmo
quando a colisão está marcada. A nova implementação em
[`regioes_mapa.py`](../ferramentas/regioes_mapa.py) segue `Chemin_Remap`:

1. Identificar obstáculo natural quando o tile menor que 702 tem marcador
   não zero, ou o objeto pertence a 1..11.
2. Classificar essas células por `atributos & 1`; as demais recebem classe zero.
   A colisão de unidades, isoladamente, não cria componente natural.
3. Percorrer as 65.536 células em ordem crescente e rotular componentes a partir
   de 1. Classe zero usa oito vizinhos; classe um usa quatro.
4. Depois do preenchimento, zerar rótulos fora da largura/altura e gravar
   atributo 1 nessas células. Rejeitar quantidade de rótulos maior ou igual a
   `0x4000`, reservada à codificação de ocupantes.

`refazer_regioes` também limpa os campos de busca zerados por esse ramo e
reaplica a ocupação das posições atuais e reservadas das unidades vivas.
Seu uso validado nesta etapa é a preparação do cenário, antes das ordens.
Não é um remapeamento completo de construções, cores auxiliares ou buscas
em andamento.

As demonstrações marcam o exterior de 16×16 como obstáculo natural **antes**
de rotular. Isso torna a topologia inicial explícita: o original preenche a
grade inteira antes de aplicar os limites jogáveis.

## Resultados observados

Unidade tipo 7, início `(2,4)`, destino solicitado `(10,4)`, velocidade 2.
As contagens são atualizações do coordenador, sem equivalência afirmada em segundos.

| Cenário | Atualizações | Posição final | Atingiu o pedido? | Buscas gerais |
|---|---:|---|---|---:|
| Obstáculo em `(6,4)` | 130 | `(10,4)` | Sim | 0 |
| Parede x=6, y=0..10 | 279 | `(10,4)` | Sim, passando por `(6,11)` | 1 |
| Parede x=6, y=0..15 | 52 | `(5,4)` | Não; destino cancelado após status 7 | 1 |
| Destino ocupado por obstáculo | 114 | `(9,4)` | Não; cancelamento local | 0 |

Todos os casos terminam no estado 7 e geram a mensagem do perfil 1 para a
tarefa suspensa. Portanto, **mensagem de término não comprova chegada ao destino
solicitado**. O relatório separa destino solicitado, destino efetivo e posição
final. Isso preserva o comportamento observado do original, inclusive o
resultado 1 entregue após esses cancelamentos.

## Validação e lacunas

A etapa inicial de navegação passou com **119 testes e 27.230 execuções x86**.
Com a preparação e as etapas dos candidatos, a suíte possui **144 testes e
32.623 execuções x86 delimitadas**, incluindo 205 chamadas dos backends de
navegação, sem testes ignorados. A execução
sem emulação registra explicitamente os testes opcionais ignorados.

Os testes diferenciais cobrem os 26 tipos, oito direções de deslocamento,
máscaras, pegadas, bordas, ocupantes, classificação natural, componentes com
quatro/oito vizinhos, solicitação e resposta da busca e invalidação de rota.
O preenchimento de componentes é executado no trecho original, parando antes
de `GlobalHandle`/`GlobalFree`; as APIs Windows não são simuladas.

O teste de colisão nova bloqueia `(5,7)` depois de a unidade chegar a `(5,6)`,
com uma rota ativa. O atributo de colisão muda nos dois mundos, preservando
o rótulo natural. A unidade invalida a rota, solicita outra busca e chega ao
destino. O teste exige pelo menos duas buscas e compara os estados a cada
atualização até a mensagem e a retomada da tarefa.

Nos trajetos integrados, uma bancada independente executa as funções originais
de caminho, giro, avanço, conclusão e mensagem em sequência. Após cada
atualização, os testes comparam registros completos e grades de física, visão,
minimapa e tarefas. Não substituem chamadas internas dessas rotinas. A referência
usa paradas declaradas nos pontos que excluem animação contínua e som, como
o coordenador Python; não é uma execução do laço inteiro do jogo.

O teste de linha e a otimização posterior já têm tradução independente.
Preparação/ajuste e início/seleção dos candidatos também foram traduzidos.
Continuam pendentes a construção/contorno dos dois candidatos,
a grade auxiliar de estruturas codificadas com `0x8000`, os efeitos de
atropelamento, tráfego com várias unidades, mapas reais inicializados por inteiro,
animação contínua, som e validação numa partida. O backend recusa estruturas
codificadas sem a grade auxiliar, em vez de calcular com dados ausentes.
