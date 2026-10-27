# Contornos dos obstáculos e busca independente em Python

O corpo que constrói os dois percursos de `CheminCalcul` foi traduzido para
[`contornos_caminhos.py`](../ferramentas/contornos_caminhos.py), nas classes de
ocupação **1, 2 e 3**, que cobrem os 26 tipos da tabela estudada.
[`solucionador_python.py`](../ferramentas/solucionador_python.py) liga essa etapa
à preparação, seleção, otimização e serialização já reconstruídas. Esse backend
não carrega o EXE nem importa Unicorn.

O domínio atual recusa estruturas codificadas na grade de regiões e ordens de
desbloqueio que exigiriam mover um aliado. Consultas de passagem por ocupantes
são suportadas no cálculo; efeitos de atropelamento e outras ações físicas
continuam sujeitos aos limites do modelo de movimento.

## Reproduzir

```sh
# Busca e movimento Python, sem JIT ou execução do EXE.
python3 ferramentas/demonstrar_desvios.py --python
python3 ferramentas/validar.py

# Referência x86 e comparação diferencial completa.
python3 ferramentas/demonstrar_desvios.py --original
python3 ferramentas/validar.py --emular
```

O novo relatório é [`desvios-python.json`](../relatorios/desvios-python.json).
Ele identifica `executa_x86=false`, classes suportadas e limitações, além das
etapas e dos custos dos contornos. O catálogo de mensagens previamente extraído
continua sendo lido do JSON versionado; não é necessário ler o EXE para executar
essa demonstração.

Na API, use `MundoNavegacao(..., solucionador=SolucionadorCaminhosPython())`.
Cada mundo deve ter sua própria instância, pois o buscador mantém os dois buffers
e a lista de regiões entre buscas, como o contexto global original.

## Evidências e sequência

O binário continua identificado pelo SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
As instruções usadas estão na exportação existente de
[`CheminCalcul`](../evidencias/ghidra/0042f214.asm).

| Trecho | Efeito reconstruído |
|---|---|
| `0x430bc5..0x431ec8` | Escolher o próximo passo do primeiro contorno |
| `0x431ec8` em diante | Registrar obstáculo deixado, regiões, ocupantes e passo |
| Até `0x4355ab` | Testar saída em direção ao destino e completar o primeiro buffer |
| `0x4355ab` em diante | Reiniciar na origem, conservar regiões iniciais e trocar o sentido |
| Até `0x43b073` | Construir o segundo buffer e tratar falhas dos dois lados |

Os corpos repetidos de passagem foram associados às primitivas já verificadas.
O oráculo executa as instruções originais sem substituir chamadas internas e
para antes da escolha final dos candidatos.

### Escolha do próximo passo

O contorno aponta para a última célula de obstáculo. Testa a direção calculada
pelos sinais de x/y. Ao recusar passagem, guarda a célula testada e gira dois
índices no círculo de 16 orientações: **-2 no primeiro candidato, +2 no segundo**.
A procura termina se voltar à célula de obstáculo ou após dez tentativas.

A célula anterior testada é uma saída importante. Mesmo havendo um passo livre,
se ela for `0xffff`, o original marca o custo como inválido. A tradução conserva
essa condição de borda.

Na pegada de quatro células, o registro do obstáculo deixado consulta a âncora,
esquerda, diagonal superior esquerda e posição superior. Só considera colisões
que não pertençam à pegada do passo escolhido. Os testes de diferença dessa
consulta usam a aritmética observada no original.

### Regiões e ocupantes

Cada passo pode adicionar uma região ao conjunto que está sendo contornado.
O rótulo da origem é descartado, e os identificadores de unidades podem expandir
as quatro subcélulas. Os registros de ocupantes conservam dono/aliança, prioridade
de adversário e a fase em que foram encontrados.

Ao começar o segundo lado, o contador da lista volta à quantidade inicial.
Os dados depois dessa contagem permanecem no buffer. Os dois buffers de rota,
os registros e a lista de 255 palavras preservam os resíduos inativos relevantes.

### Quando o percurso deixa o obstáculo

Depois de um passo, a rotina testa uma linha em direção ao destino. Ela pode
deixar o contorno quando essa linha não encontra uma região já registrada.
Uma colisão numa região ainda não conhecida não necessariamente impede essa
saída: o movimento direto e uma busca posterior continuam fazendo parte do fluxo.

Portanto, o buffer pode representar apenas um desvio parcial. O custo conta
os passos do contorno e não equivale obrigatoriamente à contagem final do buffer.
O último vizinho livre pode ser acrescentado sem aumentar esse custo.

O original limita as rotas a 255 células e as inspeções de linha a 255 iterações.
O último acréscimo também incrementa a fase. O efeito do primeiro lado é zerado
ao iniciar o segundo, enquanto o do segundo permanece no estado final.

Se ambos os lados ficarem inválidos, a rotina devolve status 8 com buffers vazios
ou status 6 quando restarem passos parciais. Um teste de região anterior pode
recusar o pedido com status 7 antes de qualquer contorno.

## Backend independente e bancada mista

`SolucionadorCaminhosPython` realiza toda a busca suportada em Python. O campo
de ponteiro de rota do contexto usa, por padrão, identificadores lógicos 1..800;
o modelo não os desreferencia. A validação pode fornecer os endereços da memória
sintética para comparar o contexto byte a byte com o x86. Isso não altera a rota.

O backend misto agora também usa os contornos Python nas três classes. A bancada
x86 executa somente o prólogo/guardas e o epílogo dessa chamada; a referência
`SolucionadorOriginal` continua executando o algoritmo original inteiro.
O desbloqueio administrativo ainda pode usar funções originais no backend misto.

No backend independente, o ramo de desbloqueio que não encontra um aliado
parado pode terminar em Python. Caso seja necessário ordenar que um aliado
se afaste, há recusa explícita: essa operação ainda precisa ser traduzida.

## Comparações e resultados

A suíte completa passou com **155 testes e 36.157 execuções x86 delimitadas**,
sem falhas, erros ou testes ignorados. Sem emulação, passam 74 testes comuns;
os 81 opcionais ficam explicitamente ignorados no relatório local.

A matriz de contornos cobre os 26 tipos nos cenários de parede/obstáculo,
104 mapas determinísticos, 96 combinações de ocupantes e dois casos de falha.
Compara custos, ambos os buffers completos de 512 bytes, registros de ocupantes,
lista inteira de regiões, contagem e fase. Além disso, 78 buscas completas
comparam o backend independente e o original nos três mapas para todos os tipos.

Os trajetos com quatro obstáculos e um caso de colisão nova são comparados
após cada atualização até a mensagem e a retomada da tarefa. Um teste separado
bloqueia os imports de `emulador`, `unicorn` e dos backends x86 e reproduz a
demonstração usando somente Python.

| Cenário demonstrado | Atualizações | Posição final |
|---|---:|---|
| Obstáculo simples | 130 | `(10,4)` |
| Parede com passagem | 279 | `(10,4)` |
| Parede fechada | 52 | `(5,4)`, pedido cancelado |
| Destino bloqueado | 114 | `(9,4)`, pedido cancelado |

Na parede com passagem, os custos continuam `[65535, 7]`; o segundo percurso
vence. A mensagem de término continua distinta da comprovação de chegada ao
destino solicitado, conforme [NAVEGACAO.md](NAVEGACAO.md).

Continuam pendentes a grade auxiliar e o contorno de estruturas codificadas,
as ordens de desbloqueio a aliados, a inicialização integral dos mapas reais
e a validação numa partida. O modo Python demonstrado não significa que
economia, combate, interface ou renderização completos já estejam reconstruídos.
