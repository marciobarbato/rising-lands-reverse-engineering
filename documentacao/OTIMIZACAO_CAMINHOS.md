# Otimização de caminhos reconstruída em Python

Foram traduzidas `TestLigneOptimise` (`0x42d674`) e `OptimiseChemin`
(`0x42e890`), em [`otimizacao_caminhos.py`](../ferramentas/otimizacao_caminhos.py).
O backend [`solucionador_misto.py`](../ferramentas/solucionador_misto.py) já usa
essas traduções durante a busca e entrega a rota ao movimento das unidades.
A preparação e o ajuste do destino agora também têm tradução, assim como a
inspeção inicial e a escolha dos candidatos. O corpo de construção/contorno dos
percursos continua original; veja [PREPARACAO_CANDIDATOS.md](PREPARACAO_CANDIDATOS.md).

O nome das duas funções vem de `RISING.SBL`. As evidências anteriores já
continham os corpos necessários: [`0042d674.asm`](../evidencias/caminhos-auxiliares/0042d674.asm)
e [`0042e890.asm`](../evidencias/caminhos-ia/0042e890.asm).
O executável usado na comparação permanece identificado pelo SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

## Reproduzir

```sh
# Propriedades do código independente, sem Unicorn.
python3 -m unittest discover -s testes -p 'test_otimizacao.py' -v

# Integração parcial: preparação, seleção, otimização e movimento Python.
python3 ferramentas/demonstrar_desvios.py --misto

# Referência: todas as funções da busca originais.
python3 ferramentas/demonstrar_desvios.py --original

# Comparações isoladas e integradas com a referência x86.
python3 ferramentas/validar.py --emular
```

Os modos `--misto`, `--original` e a validação emulada exigem Unicorn e memória
JIT; consulte [EMULACAO.md](EMULACAO.md).
O relatório novo é [`desvios-misto.json`](../relatorios/desvios-misto.json).
Cada cenário identifica quantas células entraram e saíram da otimização Python.
As opções `--original` e `--misto` são mutuamente exclusivas.

## Teste de linha: contrato observado

`TestLigneOptimise` recebe origem em AX, destino em DX, ponteiro do buffer de
células em EBX e ponteiro de contador u32 em ECX. Consulta o contexto global
de unidade, dono, classe e máscara preparado pela busca. Não altera a posição
da unidade nem reserva células.

A sequência reconstruída é:

1. Zerar o flag `0x4e1771`, que permitiria aliados parados.
2. Calcular a direção pelos sinais das diferenças de x/y, com as tabelas em
   `0x496388..0x496393`. Para células iguais, a tabela produz direção 5.
3. Consultar a passagem na primeira célula vizinha **antes de zerar o contador**.
   Se essa consulta falhar, retornar falso, conservando contador e buffer.
4. Se a consulta passar, zerar o contador e começar na origem. Enquanto a célula
   atual for diferente do destino, verificar passagem, gravar a célula e
   recalcular a direção para o próximo passo.
5. Parar com falha se a passagem for recusada ou a vizinhança resultar em
   `0xffff`. O prefixo escrito e o contador parcial ficam preservados.
6. Parar também após 255 iterações, retornando verdadeiro nesse caso.

O percurso **inclui a origem e exclui o destino**. A direção acompanha os
sinais restantes em cada passo: pode começar na diagonal e terminar no eixo.
Origem igual ao destino ainda passa pela consulta inicial da célula vizinha;
não é um retorno imediato universal.

`ResultadoLinha` preserva o retorno, a sequência escrita e o contador.
`contador=None` representa o caso em que o ponteiro de contador não foi escrito.
Não se deve transformar automaticamente uma falha em buffer vazio nem interpretar
o retorno positivo como prova de chegada ao destino, por causa do limite de 255.

### Passagem usada pela otimização

O predicado considera a máscara de terreno, o tratamento especial do objeto
`0xfd`, a ocupação própria e os identificadores de ocupantes na grade de regiões.
Classe 1 consulta uma célula; classes 2/3 consultam quatro e recusam x=0 ou y=0.
A ocupação própria considera a posição `0x08`, conforme esse corpo original.

Para outra unidade, consulta as primitivas de aliança, direção, movimento e
exceção entre tipos já reconstruídas em `caminhos.py`. A recusa de aliados
parados decorre do flag zerado na entrada. A consulta de movimento
`EnginPeutPasser` tem outro contrato, descrito em [NAVEGACAO.md](NAVEGACAO.md).

## Duas passagens sobre a rota

O buffer de entrada de `OptimiseChemin` tem contador u16 e até 255 células em
**ordem direta**, antes da inversão para consumo pela unidade.

A primeira passagem procura, a partir de cada célula, a célula mais distante
na sequência que ainda seja adjacente a ela. Ao encontrá-la, conserva os dois
extremos e elimina o trecho intermediário. O teste usa diferenças x/y em oito
bits; a tradução preserva inclusive a adjacência com overflow entre 0 e 255.

A segunda passagem começa pela primeira célula compactada. Testa linhas até
candidatos mais adiante, em ordem decrescente, deixando a última célula para o
consumo posterior do laço. Quando encontra uma linha permitida, acrescenta as
células emitidas e continua a partir do candidato. Caso contrário, copia a célula
atual e avança uma posição.

Tentativas de linha recusadas podem escrever células depois do contador ativo.
O original não limpa essa cauda. Por isso `otimizar_rota` recebe e devolve os
**512 bytes completos**, e os testes comparam também as células fora da parte
ativa. Entradas com contagem maior que 255 são recusadas. Uma escrita que
ultrapassaria a capacidade do buffer também é recusada explicitamente.

Entre as duas passagens, o original calcula uma tabela de diferenças de direção
na pilha (`0x42e96c..0x42ea5d`). A leitura das instruções posteriores mostra que
essa tabela não é consultada na reconstrução da rota. A tradução conserva as
transformações e os efeitos observáveis, sem reproduzir esse cálculo local sem
consumidor. A comparação inclui o buffer inteiro e o flag global afetado.

## Integração e referência independente

`SolucionadorParcialPython` é a opção explícita atual; o nome anterior
`SolucionadorComOtimizacaoPython` continua como alias. A primeira integração
parava em `OptimiseChemin` e retomava o chamador em `0x43b2be`. Agora também foram
traduzidas a preparação, a inspeção inicial e a seleção, e a bancada para antes
da escolha em `0x43b073`. A seleção entrega o candidato à mesma otimização Python;
a serialização já reconstruída grava a rota invertida e o epílogo original
é retomado em `0x43b300`. Veja os checkpoints atuais em
[PREPARACAO_CANDIDATOS.md](PREPARACAO_CANDIDATOS.md).

O corpo que constrói os dois percursos ainda é executado no EXE original emulado.
As retomadas conservam a pilha preparada pelo prólogo e usam os limites de
endereço, tempo e instruções da bancada. Cada trecho retomado entra na contagem
de execuções delimitadas.

O relatório identifica a substituição. `SolucionadorOriginal` continua executando
as duas funções originais, sem essa troca, e permanece a referência. A comparação
integrada usa uma bancada independente para conferir caminho, física, visão,
minimapa e tarefas a cada atualização.

## Cobertura e resultados

Na etapa de otimização, a suíte passou com **129 testes e 31.118 execuções x86**.
Com a preparação e as etapas dos candidatos, são **144 testes e 32.623 execuções
x86 delimitadas**, sem testes ignorados. Sem emulação, passam 70 testes comuns
e os 74 opcionais ficam explicitamente ignorados no relatório local.

As comparações isoladas executam **833 testes de linha e 124 otimizações** no
original, cobrindo os 26 tipos, oito direções, células iguais, máscaras, objeto
`0xfd`, bordas, ocupação própria, outros ocupantes, alianças, limites e laços.
As rotas incluem 100 caminhadas determinísticas com bloqueios e cauda inicial
não zerada. Cinco testes comuns verificam propriedades sem depender do x86.

Nos testes integrados, o backend com otimização Python reproduziu os quatro
trajetos anteriores e o caso de um obstáculo surgindo durante o movimento,
incluindo os buffers de rota, posições, colisão, visão, minimapa, mensagem e
retomada da tarefa. O relatório de demonstração mantém os resultados:

| Cenário | Atualizações | Posição final | Otimizações Python |
|---|---:|---|---:|
| Obstáculo simples | 130 | `(10,4)` | 0 |
| Parede com passagem | 279 | `(10,4)` | 1 |
| Parede sem passagem | 52 | `(5,4)` | 0 |
| Destino bloqueado | 114 | `(9,4)` | 0 |

Na parede com passagem, o candidato de oito células também sai com oito nesse
exemplo. A comparação isolada cobre os casos em que a sequência se modifica.
Os cancelamentos continuam gerando a mensagem de término descrita em
[NAVEGACAO.md](NAVEGACAO.md); a posição final é registrada separadamente do pedido.

## Continuação

A otimização, a preparação/ajuste, a inspeção inicial e a seleção já têm tradução.
Ainda falta o corpo de construção/contorno dos candidatos em `CheminCalcul`.
O backend misto continua exigindo o EXE e Unicorn para essa parte.
Também permanecem as limitações sobre construções, tráfego, combate,
animação e partida completa registradas em [CONTINUIDADE.md](CONTINUIDADE.md).
