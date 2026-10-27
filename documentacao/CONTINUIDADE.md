# Estado da pesquisa e continuidade

## Concluído nesta etapa

- Repositório Git independente em `Rising Lands/engenharia-reversa`.
- Inventário e identificação do executável local.
- 36 trechos x86 exportados com bytes e anotações.
- Leitores CMP e ETA independentes, em português, com validação de limites.
- Sequência de carregamento dos 38 mapas reconciliada com o código original.
- Carregador dos atributos dos tipos reconstruído e matrizes de dano extraídas.
- Renderização estática do terreno da missão 1 com IDs corrigidos.
- Testes sintéticos e contra o corpus real.
- Ghidra e JDK portáteis instalados, com descompilador nativo ARM64 compilado.
- Exportações em 333 endereços distintos e sete assinaturas de acessores corrigidas.
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
- 155 testes aprovados e 36.157 execuções x86 delimitadas, incluindo 152 dos backends
  de navegação. Validação registrada em `relatorios/validacao-emulada.json`, sem iniciar o jogo.
  O teste do despachante superior substitui etapas; os testes da máquina de tarefas
  e das operações suportadas executam suas chamadas originais.

## Questões em aberto

| Tema | Evidência disponível | Trabalho necessário |
|---|---|---|
| Caminhos e colisão | Núcleo das classes 1..3 em Python, ligado à física e conferido com o x86 | Completar cores/contornos de estruturas, ordens a aliados bloqueadores e tráfego/mapas reais |
| IA | Máquina de tarefas e ordens de movimento individuais/de grupo com efeitos confirmados | Completar seleção espacial da tarefa 16, mensagens e operações de economia/guerra |
| Movimento e tempo | Desvios locais e gerais ligados ao avanço, ocupação, visão/minimapa, conclusão e mensagens | Completar despacho, fome/armadilhas, atropelamento e medir a taxa efetiva |
| Combate | Aritmética parcial de dano, consulta de proximidade e cura confirmadas | Alvos, alcance, cadência, tecnologias e efeitos de morte |
| Economia | Custos e blocos de recursos | Associar IDs internos, produção, consumo e filas |
| Construções | Primeiro bloco indexado do ETA | Identificar tipos, campos, posição e estados |
| Instâncias de unidades | Dono, coordenadas, vida e cópia disco→RAM confirmados | Completar ordens, significado dos estados e campos derivados |
| Campanha | Blocos variáveis e textos de missões | Decifrar condições, eventos e vitória/derrota |
| Sufixo ETA | Tamanho constante e hashes por mapa | Mapear as camadas restantes e seus consumidores |
| Névoa e sprites | Referências no renderizador | Reproduzir composição, visibilidade e animação |
| Som, vídeo e rede | Imports DirectSound, MCI e DirectPlay | Identificar formatos, fluxos e protocolos |
| Salvamento | Caminhos adjacentes de leitura | Comparar formato de campanha com snapshots de partida |

## Próxima investigação recomendada

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
[OTIMIZACAO_CAMINHOS.md](OTIMIZACAO_CAMINHOS.md). Prosseguir com as ordens de
desbloqueio a aliados e a grade auxiliar de cores/contornos de estruturas antes de
testar obstáculos de construções e ampliar cenários com várias unidades.
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
