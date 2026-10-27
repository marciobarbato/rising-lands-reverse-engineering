# IA: despacho por jogador e tarefas

Foi reconstruída a **orquestração** em [`ia.py`](../ferramentas/ia.py), a partir
de `0x47f927`. As decisões internas de economia, combate e campanha ainda não
formam uma IA independente. O callback obrigatório representa essas etapas
não traduzidas, sem inventar comportamentos para substituí-las.

A etapa seguinte recuperou os nomes franceses do SBL e o programa RULE,
descritos em [SIMBOLOS.md](SIMBOLOS.md). A máquina parcial em
[TAREFAS.md](TAREFAS.md) já executa criação, subtarefas, espera e conclusão.

## Entrada e ordem de execução

O fluxo do ciclo do jogo passa por `0x47fbea`, que reduz os argumentos a oito
bits e chama `0x47f927` com jogador em EAX e missão em EDX. O invólucro retorna
AL=1 após a chamada; esse valor não é o código de resultado do despachante.

Para jogadores 0..3, `0x47f927`:

1. Retorna zero se o byte `0x51a990 + jogador*16` estiver ativo.
2. Consulta o dword `0x4dfaa8 + jogador*4` e a contagem u16 de unidades em
   `0x4e1928 + jogador*2`. Quando ambos são zero, incrementa em oito bits
   o byte `0x51a995 + jogador*16`; caso contrário, zera esse byte.
3. Quando o contador fica **igual a 10**, chama `0x483d95`, ativa o byte
   de inatividade e retorna zero. Valores acima de 10 não acionam a condição
   até o contador circular novamente. O primeiro dword permanece com nome
   neutro: ainda não foi provado que ele conte construções.
4. Executa as etapas abaixo na ordem indicada e para no primeiro retorno
   não zero. O código `0x1a1a000e` também interrompe a sequência.

| Ordem | Endereço | Argumentos confirmados | Evidência sobre o conteúdo |
|---:|---|---|---|
| 1 | `0x482936` | Jogador | O corpo apenas retorna zero nesta versão |
| 2 | `0x48453c` | Jogador | Verificação periódica, varredura de 1.000 registros de estruturas e inclusão/consulta de tarefas |
| 3 | `0x485183` | Jogador | Verificação periódica, consulta de recursos e configuração de tarefas; política econômica ainda parcial |
| 4 | `0x4866d7` | Jogador e missão | Etapa dependente de missão; decisões específicas ainda não traduzidas |
| 5 | `0x47d314` | Ponteiro `0x5148b0 + jogador*16` | Interpretação e encadeamento de tarefas |

O jogador 4 segue um ramo distinto: chama `0x47b283` e depois `0x47d314`.
Esse ramo ocorre antes da consulta de inatividade/contadores. Não se deduz
que jogador 4 tenha exatamente a mesma política dos jogadores comuns.

## Periodicidade das decisões

`0x48453c` consulta `ciclo % período == 0`, com ciclo em `0x508f7c` e período
u32 em `0x51b8a4 + jogador*124`. `0x485183` usa o mesmo ciclo e um período
em `0x51ba7c + jogador*168`. Logo, nem toda decisão roda em toda atualização.
A duração em segundos depende da cadência real do jogo, ainda não medida.
Um período zero causaria divisão por zero nesse caminho; não há base para
inventar um valor padrão.

Na segunda etapa, a varredura usa base `0x49a0c8`, passo 276 e 1.000 registros;
consulta atividade em `0x41a735`, dono no byte +4 e uma palavra no offset +6.
As chamadas `0x47d98b` e `0x47d920` consultam/incluem tarefas. A associação
com decisões específicas de construção precisa seguir os opcodes dessas tarefas.

## Interpretador de tarefas

`0x47d314` começa pelo índice armazenado no contexto de 16 bytes do jogador.
Índices `-1` encerram a lista. Os registros de tarefas usam passo 96 na base
`0x512320`; metadados de operação usam passo 20 na base `0x514910`.
O nome original dessa função é `iaSolver`. O código trata ligações, estado,
resultados e chamadas de operações. O programa e seus 140 nomes de operações
foram recuperados do RULE/SBL; os efeitos de mundo continuam parcialmente desconhecidos.

Se a lista começa em `-1`, o retorno depende de `0x514904`: zero quando esse
global é não zero, `0x1a1a000e` quando ele é zero. Esses códigos são preservados
como números, sem supor que signifiquem vitória, erro ou falta de recursos.
A rotina `0x483d95`, chamada no décimo ciclo sem os dois efetivos, manipula
listas de grupos/unidades antes da inativação. Isso ainda não prova uma
condição final de derrota da missão.

## Validação e grau de confiança

O teste diferencial executa as instruções originais de `0x47f927` em 450
combinações: cinco jogadores, contadores 0/8/9/10/255, inatividade/efetivo e
seis pontos de retorno. Compara código retornado, sequência e argumentos das
chamadas, contador e flag de inatividade.

**Os corpos das etapas são substituídos nesse teste por retornos controlados.**
Isso valida o fluxo do despachante, não as decisões internas das etapas.
A injeção de retorno não zero na primeira etapa é um teste artificial do
controle de fluxo; o corpo real de `0x482936` sempre retorna zero.

As regras de aliança e de interação local entre unidades foram executadas
sem substituição das chamadas e estão descritas em [CAMINHOS.md](CAMINHOS.md).
Há ainda uma rotina por unidade em `0x483ed7`, cujo nome original é
`iagMessTestSendMessageEngin`; seu mecanismo de mensagens ainda precisa ser traduzido.

## Próximo passo

Implementar os efeitos de uma operação de mundo e suas mensagens, partindo do
programa já extraído e da máquina parcial em [TAREFAS.md](TAREFAS.md). O tipo 16
liga consultas de posição à operação `V_DeplacerUnite`; uma tarefa de recursos
permitirá confrontar produção, estoque e disponibilidade de unidades. Os nomes
originais das etapas são `iagUnitNoyau`, `iagVilleNoyau`, `iagRessNoyau`,
`iagWarNoyau` e `iaSolver`. As assinaturas Watcom inferidas pelo Ghidra ainda
exigem conferência no assembly.
