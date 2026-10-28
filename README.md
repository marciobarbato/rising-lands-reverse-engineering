# Engenharia reversa de Rising Lands — edição brasileira

Repositório independente dentro da pasta `Rising Lands`, com pesquisa, código e
documentação em português. Os arquivos originais são lidos de `../source/cd`;
o CD, os assets e o protótipo preexistentes continuam fora deste repositório.

Esta entrega reconstrói partes verificáveis do carregamento do jogo a partir de
`RISING.EXE` e dos dados do CD. **Não é o código-fonte original recuperado, nem uma
reimplementação completa do jogo.** Parte dos nomes foi atribuída pela pesquisa;
1.995 registros de símbolos originais foram depois recuperados de `RISING.SBL`.

## Retomada do núcleo — 28/10/2026

O desenvolvimento desta frente segue no branch `codex/nucleo-construcoes`,
com checkout próprio em `engenharia-reversa-nucleo`. `PlaceBatiment`, a escolha
do primeiro tile, os caminhos de muro/portão e a atualização dos muros vizinhos
estão traduzidos; veja [COLOCACAO_ESTRUTURAS.md](documentacao/COLOCACAO_ESTRUTURAS.md).
A suíte do núcleo passou com 209 testes e 46.223 execuções x86 delimitadas,
sem testes ignorados.
O remoto `origin` foi configurado pelo usuário em
[rising-lands-reverse-engineering](https://github.com/marciobarbato/rising-lands-reverse-engineering).

Foram traduzidas a aplicação do terreno de edifícios completos e suas rotinas
de limpeza, com máscara de colisão, slots compactos, tiles, objetos, regiões e
cores. Há três trajetos demonstráveis em Python, incluindo a remoção de uma
construção durante o movimento. Veja [TERRENO_ESTRUTURAS.md](documentacao/TERRENO_ESTRUTURAS.md).
A API mantém explícita a máscara em RAM exigida pelo tipo 20. Os relatórios de
validação refletem a etapa mais recente desta retomada; a consolidação abaixo é histórica.

## Consolidação das entregas — 27/10/2026

Esta rodada de pesquisa foi encerrada para consolidação documental. As pesquisas de combate e economia
foram commitadas em pastas próprias no `main`; seus módulos continuam separados
do simulador central. A engenharia reversa e o jogo completo permanecem incompletos.

| Frente | Referência | Validação registrada, por frente |
|---|---|---|
| Núcleo: caminhos, unidades e tarefas | `1c8ebdd43b0a820652b7cb852ae1fe218d4dea5e` | [177 testes; 41.031 execuções x86 delimitadas](relatorios/validacao-emulada.json) |
| Combate | `88876ba9526f2caa1ba3c84b2c2662ce118fd4f0` | [67 testes; 170.295 execuções x86 delimitadas](pesquisas-paralelas/combate/validacao-emulada.json) |
| Economia | `50b2b2ebe09d0c50542e09d0f145f6e7fb2af982` | [108 testes; 19.499 execuções x86 delimitadas](pesquisas-paralelas/economia/validacao-emulada.json) |
| Gráficos e animação: Soldado | Revisão local `2026-10-27-soldado-v1`, ainda não versionada; commit bloqueado | [20 testes Python; 4.814 execuções x86; 12.156 descritores e 144 associações](pesquisas-paralelas/graficos-animacao/entregas/2026-10-27-soldado-v1/VALIDACAO.md) |

Esses resultados pertencem a suítes independentes; **não devem ser somados como
validação integrada**. Na economia, a contagem inclui 48 exceções e três limites
esperados, discriminados no relatório. A consolidação documental não executa
novamente essas suítes nem integra os módulos ao runtime.

A entrega gráfica local contém 1.120 arquivos de conteúdo, com manifesto SHA-256
`56d17ebe830036ac9e115549b640f994587590f61b7bcd650fecbf0f3eca5671` e snapshot-base
`1c8ebdd43b0a820652b7cb852ae1fe218d4dea5e`. Segundo a coordenação, seu commit
permanece bloqueado pela confirmação humana solicitada no chat de gráficos para
substituir a proibição original de Git. A revisão, suas fontes, dependências e
snapshots integrais permanecerão locais; não estão incluídos no commit documental.

Os contratos de [combate](pesquisas-paralelas/combate/INTEGRACAO.md) e
[economia](pesquisas-paralelas/economia/INTEGRACAO.md) descrevem entradas, efeitos
delegados e dependências pendentes. O estado, as fontes e a continuidade estão em
[CONTINUIDADE.md](documentacao/CONTINUIDADE.md).

## Resultados

- Executável PE x86 de 32 bits identificado por SHA-256, com imports e evidências de runtime Watcom.
- 36 trechos x86 com endereços, bytes e anotações para acompanhar a análise.
- Carregamento dos atributos de 26 tipos de unidade reconstruído em Python.
- Matriz de dano com 27 entradas por atacante, incluindo o tratamento da mina.
- Estrutura de leitura dos 38 mapas ETA recuperada até o fechamento do arquivo nesse caminho.
- Oito arquivos CMP decodificados: 12.268 quadros gráficos.
- Terreno da missão 1 reconstruído com IDs começando em 1, como no renderizador original.
- Testes de regressão com entradas sintéticas, arquivos reais e falhas de formato.
- Ghidra portátil instalado e exportações em 345 endereços distintos, com assinaturas corrigidas de sete acessores.
- Dono, posição e vida das 2.604 entradas de unidades, distinguindo arquivo e efeitos da carga.
- Cura com limite de vida reconstruída, incluindo aritmética de 16 bits.
- Direção, giro, vizinhança, prefixo do passo e parâmetros de movimento dos 26 tipos.
- Aritmética parcial de dano, incluindo comportamentos de borda do original.
- Ciclo de simulação/desenho rastreado; recarga, contadores e gerador aleatório reconstruídos.
- Regiões sob ocupantes, máscaras de terreno, alianças, passagem entre unidades e espera por nova busca reconstruídas.
- Despacho da IA por jogador reconstruído e nove cenários de busca executados no código original.
- 1.995 símbolos originais franceses recuperados e importados no Ghidra.
- Programa de IA extraído: 1.157 instruções, 42 tipos registrados e 140 nomes de operações.
- Máquina parcial de tarefas com criação, espera, subtarefas, retomada e liberação verificadas sem substituir chamadas.
- Ordens individuais e de grupo ligadas às tarefas, com efeitos sobre unidades, busca e referências de estruturas.
- Demonstração reproduzível de cinco cenários, comparada com as chamadas originais.
- Avanço físico em rota fornecida, ocupação, visão/minimapa e conclusão da ordem reconstruídos.
- Mensagens por estado ligadas à espera/retomada de tarefas, com um trajeto de duas células conferido no x86.
- Desvios locais, regiões naturais e controle de navegação em Python, ligados à busca geral original emulada.
- Quatro trajetos com obstáculos e nova colisão durante a rota conferidos com as rotinas originais.
- Teste de linha e otimização de rotas traduzidos para Python e integrados à busca em um backend opcional.
- Preparação, construção dos dois contornos, seleção e otimização em Python nas classes 1..3, cobrindo os 26 tipos.
- Backend independente de caminhos e demonstração de movimento sem carregar o EXE ou Unicorn.
- Estruturas nos contornos, grade de cores com união/separação, geometria dos 22 tipos e ordens para afastar aliados bloqueadores.
- Marco do núcleo `1c8ebdd`: 177 testes passando, com 41.031 execuções x86 delimitadas; o teste do despachante superior substitui suas etapas internas.
- Pesquisa autônoma de combate: seleção de alvos, alcance, linha de tiro, mira, animação/emissão e inicialização dos campos de ataque. A origem de `+0x8A=2/3` continua sem prova.
- Pesquisa autônoma de economia: consultas e mutações de recursos, depósitos, contagem de armazéns, efeitos econômicos de propriedade e 15 rotinas de minas, coleta e regeneração de campos. Transporte completo, consumo, mercado e filas continuam pendentes.

## Leitura recomendada

1. [Relatório da engenharia reversa](documentacao/ANALISE.md): descobertas e limites.
2. [Formatos dos arquivos](documentacao/FORMATOS.md): offsets e sequência de leitura.
3. [Carregador de unidades](documentacao/UNIDADES.md): layout em memória e pseudocódigo.
4. [Catálogo das unidades](relatorios/UNIDADES.md): nomes portugueses, custos e atributos.
5. [Mapa das rotinas](documentacao/ROTINAS.md): onde conferir cada conclusão.
6. [Lacunas e próximos passos](documentacao/CONTINUIDADE.md).
7. [Instâncias das unidades](documentacao/INSTANCIAS.md) e [Ghidra local](documentacao/GHIDRA.md).
8. [Movimento](documentacao/MOVIMENTO.md), [combate](documentacao/COMBATE.md) e [validação emulada](documentacao/EMULACAO.md).
9. [Ciclo do jogo e frequência de desenho](documentacao/CADENCIA.md).
10. [Busca de caminhos e ocupação](documentacao/CAMINHOS.md) e [despacho da IA](documentacao/IA.md).
11. [Símbolos franceses e formato RULE](documentacao/SIMBOLOS.md) e [máquina de tarefas](documentacao/TAREFAS.md).
12. [Efeitos das ordens de movimento](documentacao/ORDENS_MOVIMENTO.md).
13. [Avanço físico e mensagens de chegada](documentacao/AVANCO_CHEGADA.md).
14. [Navegação integrada e desvios de obstáculos](documentacao/NAVEGACAO.md).
15. [Otimização de caminhos reconstruída](documentacao/OTIMIZACAO_CAMINHOS.md).
16. [Preparação do destino e etapas dos candidatos](documentacao/PREPARACAO_CANDIDATOS.md).
17. [Contornos dos obstáculos e busca independente](documentacao/CONTORNOS.md).
18. [Prompts para pesquisas paralelas e aplicativo Mac](documentacao/PROMPTS_PARALELOS.md).
19. [Estruturas e afastamento de bloqueadores](documentacao/ESTRUTURAS_DESBLOQUEIO.md).
20. [Contrato da pesquisa de combate](pesquisas-paralelas/combate/INTEGRACAO.md).
21. [Contrato da pesquisa de economia](pesquisas-paralelas/economia/INTEGRACAO.md).
22. [Aplicação e limpeza do terreno de construções](documentacao/TERRENO_ESTRUTURAS.md).
23. [Colocação de estruturas, muros e portões](documentacao/COLOCACAO_ESTRUTURAS.md).

## Reproduzir

Execute dentro deste repositório. Python 3.9 ou superior; o extrator PE usa
`pefile` e `capstone`. Os leitores de mapas, gráficos e testes não dependem de Pillow.
Se as bibliotecas já existentes em `../source/python` estiverem disponíveis, elas
são reutilizadas automaticamente. Para uma instalação isolada:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python ferramentas/analisar.py
```

Com as dependências existentes nesta máquina:

```sh
python3 ferramentas/analisar.py
python3 ferramentas/extrair_ia.py
sh testar.sh
```

Outro local para o CD extraído:

```sh
python3 ferramentas/analisar.py --cd /caminho/para/cd
```

O comando escreve somente `relatorios/` e `evidencias/`, dentro deste repositório.
Não baixa arquivos nem executa o EXE. Recusa outros hashes do executável porque
os endereços estudados são específicos desta versão. A imagem do terreno não
inclui unidades, construções dinâmicas, névoa de guerra ou simulação.

Para registrar a validação comum, execute `python3 ferramentas/validar.py`.
A [validação opcional com Unicorn](documentacao/EMULACAO.md) executa somente
trechos x86 isolados, sem iniciar o jogo. O relatório completo está em
[validacao-emulada.json](relatorios/validacao-emulada.json).

Para percorrer um trajeto com obstáculo, execute
`python3 ferramentas/demonstrar_desvios.py`. Para incluir paredes e a busca geral
original emulada, use `python3 ferramentas/demonstrar_desvios.py --original`.
Os relatórios distinguem destino solicitado, destino efetivo e posição final;
o término da ordem também pode resultar de cancelamento por falta de passagem.
Use `--python` para executar a busca, o avanço e as mensagens sem EXE ou Unicorn.
O cálculo suporta as três classes de ocupação, incluindo estruturas com suas
cores auxiliares e ordens a aliados bloqueadores. A demonstração
`python3 ferramentas/demonstrar_estruturas.py` exercita esses casos. `--misto` conserva a bancada x86
para comparar as traduções e os efeitos administrativos ainda não portados.

## Organização

| Pasta | Conteúdo |
|---|---|
| `ferramentas/` | Extrator PE, leitores CMP/ETA e reconstrução do carregador de atributos |
| `documentacao/` | Análise técnica em português com evidências e hipóteses |
| `evidencias/` | Trechos x86 selecionados do executável identificado |
| `relatorios/` | Manifesto de hashes, dados recuperados e terreno da missão 1 |
| `testes/` | Casos sintéticos e validação contra o corpus local |
| `ghidra/` | Instalador, launcher, scripts de anotação e análise |
| `pesquisas-paralelas/` | Entregas autônomas, com contratos e validações próprios; não integradas automaticamente ao núcleo |

Os relatórios são versionados para permitir comparação entre descobertas. Os
testes que dependem do CD são explicitamente marcados como ignorados se ele
não estiver disponível; os demais continuam executando. As frentes mantêm seus
próprios branches e checkouts para preservar o trabalho em paralelo.
