# Estado da pesquisa e continuidade

## Retomada de 28/10/2026 — terreno de construções

Foram traduzidas `BatimentModifyTerrain`, `ResetBatimentTerrainModify` e
`ResetCheminTerrainModify`, com integração em `MundoNavegacao` e demonstrações
de percurso após aplicação/remoção de edifícios. O contrato e as evidências
estão em [TERRENO_ESTRUTURAS.md](TERRENO_ESTRUTURAS.md). A numeração compacta das
células bloqueadoras e a diferença da máscara em RAM do tipo 20 foram
preservadas. Os relatórios atuais do núcleo incluem esta etapa e continuam
separados das validações das pesquisas paralelas.

O carregamento/remapeamento integral de construções em mapas reais e o ciclo
completo de colocação/demolição continuam pendentes. A consolidação abaixo
registra a situação histórica de 27/10, não o andamento posterior das outras
frentes; elas não foram alteradas nesta retomada.

## Consolidação documental de 27/10/2026

A rodada de pesquisa foi encerrada. Esta reconciliação registra os
achados existentes, sem implementar código, integrar o runtime ou executar
novas suítes. **A engenharia reversa e a reimplementação completa do jogo não
estão finalizadas.** As pendências abaixo orientam uma eventual retomada;
não representam trabalho em execução nesta consolidação.

| Entrega | Commit de referência | Fontes e resultado registrado |
|---|---|---|
| Núcleo de caminhos, movimento, estruturas e tarefas | `1c8ebdd43b0a820652b7cb852ae1fe218d4dea5e` | [Documentação da etapa](ESTRUTURAS_DESBLOQUEIO.md); [177 testes / 41.031 execuções x86](../relatorios/validacao-emulada.json) |
| Combate | `88876ba9526f2caa1ba3c84b2c2662ce118fd4f0` | [Contrato](../pesquisas-paralelas/combate/INTEGRACAO.md); [67 testes / 170.295 execuções x86](../pesquisas-paralelas/combate/validacao-emulada.json) |
| Economia | `50b2b2ebe09d0c50542e09d0f145f6e7fb2af982` | [Contrato](../pesquisas-paralelas/economia/INTEGRACAO.md); [108 testes / 19.499 execuções x86](../pesquisas-paralelas/economia/validacao-emulada.json) |
| Gráficos e animação, primeiro marco Soldado | Revisão local congelada `2026-10-27-soldado-v1`, ainda não versionada; commit bloqueado | [20 testes Python / 4.814 execuções x86; 12.156 descritores e 144 associações](../pesquisas-paralelas/graficos-animacao/entregas/2026-10-27-soldado-v1/VALIDACAO.md) |

As três validações commitadas são independentes. Não há soma de testes ou de
execuções x86 apresentada como suíte integrada. O relatório de economia inclui
48 exceções e três limites esperados, além das paradas declaradas nas fronteiras
de dependências. Os resultados não comprovam uma partida completa. Nenhuma
suíte foi executada novamente para preparar este documento.
Os resultados gráficos pertencem à revisão local congelada, também independente;
não constituem uma quarta validação integrada nem uma entrega versionada.

Todas essas pesquisas usam a edição brasileira de `RISING.EXE`, SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Os nomes franceses recuperados do SBL são conservados como evidência do código
original; as interpretações e os contratos estão documentados em português.

## Marcos do núcleo até `1c8ebdd`

- Repositório Git independente em `Rising Lands/engenharia-reversa`.
- Inventário e identificação do executável local.
- 36 trechos x86 exportados com bytes e anotações.
- Leitores CMP e ETA independentes, em português, com validação de limites.
- Sequência de carregamento dos 38 mapas reconciliada com o código original.
- Carregador dos atributos dos tipos reconstruído e matrizes de dano extraídas.
- Renderização estática do terreno da missão 1 com IDs corrigidos.
- Testes sintéticos e contra o corpus real.
- Ghidra e JDK portáteis instalados, com descompilador nativo ARM64 compilado.
- Exportações em 345 endereços distintos e sete assinaturas de acessores corrigidas.
- Propriedade, coordenadas, vida e campos de carga das 2.604 entradas de unidades.
- Rotina de cura reconstruída e máximo de vida localizado na tabela de tipos.
- Primitivas de movimento e quatro parâmetros dos 26 inicializadores reconstruídos.
- Adições, reduções e aplicação de dano comparadas com o x86 original.
- Laço Windows, atualização antes do desenho e divisor F1–F4 rastreados.
- Contadores de ciclo, recarga e gerador aleatório reconstruídos e emulados.
- Comparação de regiões sob ocupantes, máscaras, alianças, passagem e espera reconstruídas.
- Preparação, busca e pós-processamento originais executados em nove mapas sintéticos.
- Despachante de IA reconstruído; etapas de estruturas, recursos e tarefas localizadas.
- 1.995 símbolos originais extraídos do SBL e importados no Ghidra.
- RULE decodificado: 1.157 instruções, 64 entradas (42 ativas), 140 nomes resolvidos.
- Máquina de tarefas parcial: criação, espera, subtarefas, retomada e liberação.
- Consumo da rota localizado após a chegada da unidade à célula.
- Ordens individuais e de grupo reconstruídas, incluindo ResetOrdre e efeitos auxiliares.
- Consultas de tipo e estado ocioso ligadas à máquina de tarefas.
- Cinco demonstrações de tarefas com efeitos, também executadas no x86 original.
- Avanço físico em terreno comum: ocupação, visão, minimapa, rota e fadiga com reservas.
- Conclusão de movimento no estado 7 e mensagens por mudança de estado.
- Espera/retomada da tarefa de grupo conectada a um trajeto de duas células.
- Consultas de passagem, desvio direto e estados de navegação traduzidos.
- Componentes naturais com quatro/oito vizinhos e limites do mapa reconstruídos.
- Busca geral original emulada ligada à física, visão, mensagens e tarefas.
- Quatro trajetos com obstáculos e uma colisão surgindo durante a rota comparados ao x86.
- TestLigneOptimise e OptimiseChemin traduzidos, com buffers completos conferidos.
- Backend opcional com otimização Python integrado à busca e aos trajetos/mensagens.
- Preparação do destino e ajuste por anéis traduzidos, com particularidades das bordas preservadas.
- Inspeção de obstáculos, regiões e ocupantes, escolha dos candidatos e serialização em Python.
- Corpo dos dois contornos traduzido nas classes 1..3, incluindo pegadas de quatro células.
- Backend independente para os 26 tipos, com preparação, contorno, escolha e otimização sem EXE/Unicorn.
- Trajetos e mensagens comparados por atualização com a referência x86 e reproduzidos com imports de emulação bloqueados.
- Cores/contornos de estruturas, geometria dos 22 tipos e ordens a aliados bloqueadores traduzidos.
- Duas demonstrações adicionais com estruturas, ordens, avanço físico e mensagens conferidos no x86.
- 177 testes aprovados e 41.031 execuções x86 delimitadas, incluindo 152 dos backends
  de navegação. Validação registrada em `relatorios/validacao-emulada.json`, sem iniciar o jogo.
  O teste do despachante superior substitui etapas; os testes da máquina de tarefas
  e das operações suportadas executam suas chamadas originais.

## Achados das pesquisas paralelas

### Combate — entregue, sem integração ao mundo compartilhado

Os módulos autônomos cobrem seleção e manutenção de alvos, alcance e linha de
tiro, mira angular, animação/emissão e inicialização/persistência dos campos de
ataque. O [contrato](../pesquisas-paralelas/combate/INTEGRACAO.md) distingue
consultas, cópias de registros e mutações, além de declarar callbacks necessários
para construções, mensagens e efeitos externos.

A tradução não fornece um ciclo de combate integrado. Pool, voo e impacto de
projéteis, dano aplicado pelo backend, áudio, mensagens e conexão com a navegação
continuam dependências explícitas. A comparação de geometria de construções usa
memória sintética 1×1/3×3. Testes que começam após `ResetOrdre` ou recebem consultas
resolvidas não comprovam todo o encadeamento anterior.

A origem de **`+0x8A=2/3` permanece não identificada**. A auditoria encontrou
escritas diretas com 0/1, e nenhum dos 2.604 registros dos 38 mapas contém 2/3.
Os carregadores preservam valores externos; isso não prova que as fases sejam
impossíveis numa partida e não autoriza inventar transições automáticas.
Ver [INICIALIZACAO_ATAQUE.md](../pesquisas-paralelas/combate/INICIALIZACAO_ATAQUE.md).

### Economia — entregue, sem promoção para `ferramentas/`

Foram traduzidos consultas e créditos/débitos de recursos, custos, depósitos
com capacidade/excedentes, retirada e recálculo do indicador, contagem de
armazéns, efeitos econômicos de ganho/neutralização de construções e **15
rotinas de minas, coleta e regeneração de campos**. As fontes, buffers, wraps,
ordem dos sorteios e dependências estão no
[contrato](../pesquisas-paralelas/economia/INTEGRACAO.md) e em
[EXTRACAO_CAMPOS.md](../pesquisas-paralelas/economia/EXTRACAO_CAMPOS.md).

As operações de terreno não representam o transporte nem o crédito final ao
jogador. Dependências de retirada de colono e criação/movimento de balões podem
interromper o domínio suportado; as bancadas correspondentes param na entrada
dessas dependências. Permanecem pendentes transporte completo, consumo/fome,
mercado, filas/recrutamento, tecnologias e ligação dos chamadores à agenda do
jogo. O significado completo de RMI e de alguns campos neutros não foi provado.

### Gráficos e animação — revisão local congelada; commit bloqueado

O primeiro marco cobre somente o **Soldado, tipo 0**, com parada/movimento,
associações de orientação/fase, ancoragem, transparência e cópia gráfica básica.
A revisão local está em
`pesquisas-paralelas/graficos-animacao/entregas/2026-10-27-soldado-v1/`, com
**1.120 arquivos de conteúdo**. O SHA-256 de `MANIFESTO.json`, conferido nesta
reconciliação, é
`56d17ebe830036ac9e115549b640f994587590f61b7bcd650fecbf0f3eca5671`.
O snapshot-base é `1c8ebdd43b0a820652b7cb852ae1fe218d4dea5e`.

A [validação local da revisão](../pesquisas-paralelas/graficos-animacao/entregas/2026-10-27-soldado-v1/VALIDACAO.md)
registra 20 testes Python e 4.814 execuções x86 aprovados, 12.156 descritores
do banco concatenado e 144 associações de orientação/fase. O carregamento dos
bancos substitui I/O e alocação; a chamada de sombra é interceptada para registrar
argumentos. Isso não equivale a executar DirectDraw nem o renderizador completo.

Segundo a coordenação, o commit está **bloqueado**: o chat de gráficos solicitou
confirmação humana para substituir sua instrução original de proibição de Git
e não aceitou a autorização repassada. Sua janela Git foi suspensa, sem staging.
Não há hash de commit gráfico a aguardar ou registrar neste encerramento.
A revisão congelada, as fontes, dependências e snapshots integrais permanecerão
locais e não serão incluídos no commit documental. Essas referências locais
não estarão disponíveis apenas clonando os commits de combate/economia/núcleo.

Permanecem sem validação completa os outros 25 tipos, construções e objetos,
ordenação da cena, transformação de sombra, efeitos, paletas por jogador, HUD,
minimapa e ligação ao simulador/aplicativo macOS. A demonstração independente
não comprova uma missão nem temporização em segundos do jogo original.

## Questões em aberto

| Tema | Evidência disponível | Trabalho necessário |
|---|---|---|
| Caminhos e colisão | Núcleo das classes 1..3 em Python, ligado à física e conferido com o x86 | Ampliar tráfego e inicializar mapas reais com o ciclo completo de estruturas |
| IA | Máquina de tarefas e ordens de movimento individuais/de grupo com efeitos confirmados | Completar seleção espacial da tarefa 16, mensagens e operações de economia/guerra |
| Movimento e tempo | Desvios locais e gerais ligados ao avanço, ocupação, visão/minimapa, conclusão e mensagens | Completar despacho, fome/armadilhas, atropelamento e medir a taxa efetiva |
| Combate | Seleção, alcance, linha de tiro, mira, animação/emissão e inicialização traduzidos em pesquisa autônoma; aritmética de dano no núcleo | Resolver origem de `+0x8A=2/3`, pool/voo/impacto, efeitos externos e integração do ciclo |
| Economia | Recursos, depósitos, armazéns, efeitos de propriedade e extração/regeneração traduzidos em pesquisa autônoma | Transporte completo, consumo/fome, mercado, filas, tecnologias e ligação aos chamadores |
| Construções | Geometria inicial dos 22 tipos, regiões/cores e efeitos econômicos de propriedade documentados | Completar carga, construção/demolição, dependências de colono/balão, produção e estados |
| Instâncias de unidades | Dono, coordenadas, vida e cópia disco→RAM confirmados | Completar ordens, significado dos estados e campos derivados |
| Campanha | Blocos variáveis e textos de missões | Decifrar condições, eventos e vitória/derrota |
| Sufixo ETA | Tamanho constante e hashes por mapa | Mapear as camadas restantes e seus consumidores |
| Névoa e sprites | Visão parcial no núcleo; revisão Soldado congelada localmente, ainda não versionada | Resolver confirmação Git na frente gráfica em eventual retomada; ampliar tipos/camadas e integrar composição/visibilidade |
| Som, vídeo e rede | Imports DirectSound, MCI e DirectPlay | Identificar formatos, fluxos e protocolos |
| Salvamento | Caminhos adjacentes de leitura | Comparar formato de campanha com snapshots de partida |

## Continuidade para uma eventual retomada

Combate e economia permanecem em suas pastas autônomas. Antes de uma integração
futura, consultar os respectivos `INTEGRACAO.md`, preservar suas dependências e
definir ensaios do encadeamento completo. A última validação do núcleo continua
separada dos relatórios dessas frentes. A entrega gráfica local deverá ser consumida
pela revisão congelada e pelo manifesto acima, respeitando sua condição de não
versionada. Uma eventual decisão de versioná-la depende da confirmação pendente
no chat responsável; este encerramento não resolve essa confirmação.

Nenhuma dessas etapas está sendo iniciada neste encerramento documental.

Prosseguir a partir de [NAVEGACAO.md](NAVEGACAO.md), [CAMINHOS.md](CAMINHOS.md)
e [IA.md](IA.md).
A preparação é `0x43b30b`; o solucionador principal é `0x42f214`, seguido de
`0x42e890`. A bancada já executa esses trechos, mas a tradução independente
continua parcial. A escolha direta, o desvio, o consumo e a nova busca estão
ligados ao movimento por `MundoNavegacao`. `SolucionadorCaminhosPython` executa
o núcleo das três classes sem emulação; `SolucionadorOriginal` permanece como
referência e `SolucionadorParcialPython` conserva a ponte com os trechos
administrativos originais. Veja [CONTORNOS.md](CONTORNOS.md),
[PREPARACAO_CANDIDATOS.md](PREPARACAO_CANDIDATOS.md) e
[OTIMIZACAO_CAMINHOS.md](OTIMIZACAO_CAMINHOS.md). As ordens de desbloqueio a
aliados e a grade auxiliar de cores/contornos foram traduzidas em
[ESTRUTURAS_DESBLOQUEIO.md](ESTRUTURAS_DESBLOQUEIO.md). Prosseguir com o ciclo
completo de remapeamento/inserção de estruturas em mapas reais e ampliar tráfego.
Para a IA, seguir [SIMBOLOS.md](SIMBOLOS.md) e [TAREFAS.md](TAREFAS.md).
A tabela `0x514910` vem de `RISING.RUL`; seus 140 nomes foram resolvidos pelo SBL.
As operações `V_DeplacerUnite` e `V_DeplaceGroupe` já estão integradas conforme
[ORDENS_MOVIMENTO.md](ORDENS_MOVIMENTO.md). Completar o prefixo espacial 422..426
da tarefa 16. O avanço, a conclusão e a retomada por mensagem
já estão conectados conforme [AVANCO_CHEGADA.md](AVANCO_CHEGADA.md), para uma rota
fornecida em terreno comum, e agora também com os desvios de [NAVEGACAO.md](NAVEGACAO.md).
Integrar fome/armadilhas e despachos adicionais de
mensagem. Ainda é necessário medir a taxa efetiva do ciclo identificado
em [CADENCIA.md](CADENCIA.md).
Uma execução controlada do jogo poderá confrontar movimento, visibilidade e
combate numa partida. Ainda não há runtime Windows preparado nem validação
de gameplay integrado. Os testes atuais emulam instruções isoladas.

## Como registrar uma nova descoberta

Para cada campo ou rotina, registrar o hash do binário, endereço ou offset,
instrução que sustenta a interpretação, exemplos do corpus e nível de certeza.
Adicionar teste quando houver uma propriedade observável independente. Para
hipóteses, conservar o nome neutro dos dados até encontrar evidência suficiente.

O CD e o protótipo externo não precisam ser alterados para continuar a pesquisa.
Esta etapa não aplicou correções a esses arquivos. Também não configurou remoto
Git nem publicou os resultados.
