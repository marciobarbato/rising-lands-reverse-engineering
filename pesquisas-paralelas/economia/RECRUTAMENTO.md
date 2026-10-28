# Início e consultas de recrutamento

Esta continuação traduz o início econômico de recrutamento, suas consultas
e três acessores usados por elas. Implementação em [recrutamento.py](recrutamento.py),
referência em [bancada_recrutamento.py](bancada_recrutamento.py) e casos em
[testes/test_recrutamento.py](testes/test_recrutamento.py). São 22 testes novos
(13 locais e nove diferenciais), com 2.777 execuções x86 delimitadas.

O EXE brasileiro continua sendo a referência, SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Os nomes vêm do SBL verificado pelo exportador. Originais e documentos gerais
foram somente lidos; todas as alterações desta etapa permanecem nesta pasta.
Não houve uso do Ghidra nem tradução de geometria, caminhos ou movimento.

## Rotinas traduzidas

| Endereço | Nome | Método de Recrutamento | Convenção original |
|---|---|---|---|
| `0x4283e2` | InitRecruteTroupe | `iniciar` | AL=tipo de unidade, DL=jogador; AL=0/1 |
| `0x420ba5` | SortEnRecrutement | `sortilegio_em_recrutamento` | AL=tipo, DL=jogador; AL=booleano |
| `0x420bdf` | EnginEnRecrutement | `unidade_em_recrutamento` | AL=tipo, DL=jogador; AL=booleano |
| `0x423f83` | GetStatusRecrute | `status` | AL=tipo, DL=jogador; EAX=progresso |
| `0x423f9d` | CalculStatusRecrute | `calcular_status` | AX=construção, DL=tipo; EAX=progresso |
| `0x423e65` | CalculNovaRecrute | `progresso_nova` | AX=construção; EAX=progresso |
| `0x4410b7` | EnginGetTimeRecrute | `tempo_unidade` | AL=tipo; AX=tempo |
| `0x47476a` | SortilegeGetTimeAprentissage | `tempo_sortilegio` | AL=tipo; AX=tempo |
| `0x441108` | EnginGetVieMax | `vida_maxima_unidade` | AX=unidade; AX=vida máxima |

InitRecruteTroupe é traduzida com dependência explícita para
RechercheDecalageSortie (`0x41d1d0`). Essa rotina escolhe uma posição de saída
consultando geometria/ocupação e permanece sob responsabilidade do outro
subsistema. Não foi substituída por um retorno fictício na bancada.

GetStatusRecrute cai diretamente em CalculStatusRecrute, que salta para um
corpo anterior, `0x423eb2..0x423f83`. Esse corpo é exportado como trecho auxiliar.
CalculNovaRecrute termina em `0x423eb1`; o corpo seguinte não pertence a ela.
O sufixo `0x428640..0x428691`, exposto como `concluir_saida`, é uma continuação
da API, não um décimo símbolo original independente.

## Memória e entradas

| Origem | Buffer/campo Python | Layout confirmado |
|---|---|---|
| `0x495be0` | `selecoes` | Quatro índices u16 de construção, por jogador |
| `0x49a0c8` | `mundo.estruturas` | Registros de 276 bytes já usados pela economia |
| `0x4965ae` | `tipos_unidades` | 26 × 50 bytes; tempo +0, comida +2, peças +4, pedra +6, vida +8 |
| `0x497174` | `tipos_sortilegios` | Cinco registros de 46 bytes; tempo u16 em +0 |
| Ponteiro `0x4e19a0` | `unidades` | 800 × 276 bytes; tipo no byte +1 |
| `0x495bf0` | `periodo_nova` | Divisor u16 de CalculNovaRecrute; valor 50 no EXE |

O mundo é compartilhado com EconomiaConstrucoes. Os quatro buffers novos
são copiados pelo construtor. Os padrões da API são sintéticos: seleções
0xffff, tabelas/unidades zeradas e período 50. Não equivalem à carga do jogo.

## Início: ordem e efeitos confirmados

InitRecruteTroupe resolve a seleção do jogador, lê os três custos do tipo e
chama TestRessource. Insuficiência retorna zero sem cobrar ou modificar a
construção. O ponteiro da construção é calculado antes, mas só é acessado
depois do teste: até seleção 0xffff pode retornar zero se faltarem recursos.
Com saldo suficiente, essa seleção inválida causaria acesso fora da tabela;
a API levanta ValueError nesse ponto.

Os tipos de construção aceitos são **1, 2, 5, 13, 15, 16, 18 e 20**. O byte
`+0x74` deve ser zero. Qualquer outro tipo ou flag ocupada retorna zero sem
cobrança. A rotina não confere dono `+4`, estado principal `+5`, tecnologia,
compatibilidade entre unidade/construção ou permissão de recrutamento. Esses
requisitos, se aplicáveis, pertencem aos chamadores; não foram inventados na
tradução. O jogador de DL paga mesmo se a construção tem outro dono.

Após aceitar, a ordem é comida (ID 1), pedra (ID 2), peças (ID 0). Cada débito
usa EnleveMatiere e é seguido pelo recálculo do indicador quando há armazéns,
inclusive quando o custo é zero. A composição Python reutiliza `mundo.retirar`;
no x86 esse recálculo está embutido no corpo de InitRecruteTroupe.

A fórmula preserva soma de estoques u16 e duas divisões, conforme
[RETIRADA_RECALCULO.md](RETIRADA_RECALCULO.md). Com armazéns positivos e
capacidade unitária zero, a divisão em `0x4284e6` falha depois do débito de
comida, antes de pedra, peças e campos de recrutamento. Não há rollback.
O teste de suficiência não torna essa sequência uma transação indivisível.

Depois dos três débitos, grava:

| Campo da construção | Valor |
|---|---|
| `+0x74`, byte | 1 |
| `+0x7a`, byte | 0 |
| `+5`, byte | 4 |
| `+0x8c`, dword | 1 |
| `+0x7b`, byte | Tipo de unidade solicitado |
| `+0x7e`, word | 0 |
| `+0x80`, `+0x82`, words | 0, exceto tipo 20, que preserva ambos |

Em seguida, relê a seleção do jogador e chama RechercheDecalageSortie. Só
depois escreve a célula devolvida em `+0x7c` e retorna AL=1. Não rejeita célula
0xffff nesse sufixo. Os outros campos permanecem intactos.

Sem callback, `iniciar` lança `SaidaRecrutamentoPendente` **depois de cobrar
e ocupar a construção**. A exceção não significa recusa ou rollback. Uma nova
chamada a iniciar normalmente retorna falso por `+0x74=1`; não é a forma de
retomar. Resolvida a dependência, usar `concluir_saida(indice, celula)`, ou
fornecer de início `escolher_saida(indice)` que implemente a dependência inteira.
O callback recebe o índice da seleção relida, enquanto o sufixo grava na
construção original, cujo ponteiro já foi conservado pelo chamador.

## Consultas e progresso

SortEnRecrutement e EnginEnRecrutement possuem a mesma regra: seleção 0xffff
é falsa; nos demais casos, comparam AL com `+0x7b`. Não consultam `+0x74`,
estado, dono ou progresso. Podem retornar verdadeiro para uma construção
inativa que conserva o tipo solicitado. Também aceitam qualquer byte de tipo
nessa comparação, pois não acessam as tabelas de tipos.

CalculStatusRecrute retorna zero para índice 0xffff. Nos demais casos, usa
o **tipo da construção** para escolher o divisor de `progresso_u32 = [+0x8c]`:

| Tipos da construção | Divisor |
|---|---|
| 1, 2, 5, 13, 15, 16, 20 | Tempo de recrutamento do tipo recebido em DL |
| 6 | Tempo de aprendizagem do sortilégio recebido em DL |
| 14 | Vida máxima da unidade cujo índice está em `+0x88` |
| 18 com `+0x7a=0` | Tempo do tipo recebido em DL |
| 18 com `+0x7a!=0` | Vida máxima da unidade referenciada em `+0x88` |
| Demais | Retorno zero, sem consultar divisor |

O resultado é divisão inteira unsigned, sem multiplicação por 100 e sem
saturação. O tipo do argumento é usado mesmo se diverge de `+0x7b`; os ramos
de vida máxima ignoram esse argumento. Atividade não é verificada.
Divisor zero provoca exceção em `0x423eca`, também para numerador zero.
GetStatusRecrute apenas resolve a seleção do jogador antes desse cálculo.

CalculNovaRecrute calcula `(([+0x108] * 100) & 0xffffffff) // periodo_u16`.
O produto transborda em 32 bits antes da divisão, e o resultado não é limitado
a 100. Índice 0xffff retorna zero antes de consultar o divisor; período zero
com índice válido provoca exceção em `0x423ea8`.

É confirmado que esses valores alimentam consultas de progresso. Sua unidade
de tempo em segundos não está estabelecida; não converter os tempos para ms.
Os nomes sugerem recrutamento e aprendizagem, mas esta etapa não implementa
o avanço por tick, conclusão da produção, criação de unidades ou fila FIFO.

## Validação e alcance

| Grupo novo | Execuções x86 |
|---|---:|
| Início nos 256 tipos de construção, livres/ocupados | 512 |
| Inícios com custos/saldos u16, estados, donos, índices e pilha preenchida | 512 |
| Recusas por saldo, incluindo seleção inválida não acessada | 192 |
| Duas consultas de recrutamento, sentinelas e inatividade | 512 |
| Status direto/wrapper: 256 tipos e ramos adicionais | 515 |
| Nova: produto u32 e sentinela | 257 |
| Sufixo isolado com frame de pilha sintético | 128 |
| Divisões por zero: capacidade, tempo de unidade/sortilégio, vida, Nova | 40 |
| 26 tipos reais: tempo, vida, custos/início e status; cinco tempos sintéticos de sortilégio | 109 |
| **Total** | **2.777** |

Destes, **2.063 são retornos de rotinas completas suportadas, 546 param na
entrada de RechercheDecalageSortie, 128 executam somente o sufixo e 40 conferem
exceções esperadas**. Os 546 casos validam cobrança e mudança de estado até a
dependência; não provam o retorno bem-sucedido da função inteira. Os 128 casos
preparam um frame sintético e iniciam em `0x428640`, sem fingir executar ou
retomar o helper de saída. O teste de callback é local e verifica apenas o
contrato. Não há substituição de chamadas na referência executada.

As comparações incluem todos os buffers modelados, campos preservados,
guardas, traço de débito e registradores preservados nas recusas. As exceções
usam CPUs novas, evitando o estado residual de exceção do Unicorn. A bancada
impõe hash do EXE, intervalos permitidos, timeout de um segundo e limite
de 20.000 instruções por chamada. Não foi iniciada uma partida.

A suíte acumulada registra **130 testes aprovados e 22.276 execuções x86**,
incluindo 88 exceções e três limites esperados. Há 22.185 paradas declaradas,
das quais 64 são na retirada de colono, 32 nas dependências de balão e 546 na
saída de recrutamento; também incluem os 128 sufixos isolados. Nenhum teste foi
ignorado na execução emulada. Em modo local, passam 71 e são ignorados 59
diferenciais. Ver [validacao-emulada.json](validacao-emulada.json).

O corpus de tipos vem dos registros já reconstruídos em
`relatorios/unidades.json`; a carga INI original não foi executada. A API
protege jogadores 0..3, construções presentes no buffer, 26 tipos de unidade,
cinco de sortilégio e 800 unidades. O original pode acessar fora desses
domínios; essa diferença não é apresentada como equivalência validada.

O manifesto contém chamadas diretas candidatas de ProcessInputGame e
V_BatimentRecruteUnite para InitRecruteTroupe, além das consultas por AffChrono
e IconeFillContenu. A varredura não prova os fluxos completos desses chamadores.
Permanecem pendentes avanço/conclusão, produção efetiva, filas e integração
com as rotinas responsáveis pela saída. Mercado, consumo/fome e transporte
completo também permanecem pendentes.
