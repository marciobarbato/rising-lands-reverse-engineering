# Engenharia reversa de Rising Lands — edição brasileira

Repositório independente dentro da pasta `Rising Lands`, com pesquisa, código e
documentação em português. Os arquivos originais são lidos de `../source/cd`;
o CD, os assets e o protótipo preexistentes continuam fora deste repositório.

Esta entrega reconstrói partes verificáveis do carregamento do jogo a partir de
`RISING.EXE` e dos dados do CD. **Não é o código-fonte original recuperado, nem uma
reimplementação completa do jogo.** Parte dos nomes foi atribuída pela pesquisa;
1.995 registros de símbolos originais foram depois recuperados de `RISING.SBL`.

## Resultados

- Executável PE x86 de 32 bits identificado por SHA-256, com imports e evidências de runtime Watcom.
- 36 trechos x86 com endereços, bytes e anotações para acompanhar a análise.
- Carregamento dos atributos de 26 tipos de unidade reconstruído em Python.
- Matriz de dano com 27 entradas por atacante, incluindo o tratamento da mina.
- Estrutura de leitura dos 38 mapas ETA recuperada até o fechamento do arquivo nesse caminho.
- Oito arquivos CMP decodificados: 12.268 quadros gráficos.
- Terreno da missão 1 reconstruído com IDs começando em 1, como no renderizador original.
- Testes de regressão com entradas sintéticas, arquivos reais e falhas de formato.
- Ghidra portátil instalado e exportações em 333 endereços distintos, com assinaturas corrigidas de sete acessores.
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
- 129 testes passando, com 31.118 execuções x86 delimitadas; o teste do despachante superior substitui suas etapas internas.

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
Use `--misto` para executar a busca com `OptimiseChemin` e `TestLigneOptimise`
traduzidos para Python. A preparação e a geração dos candidatos ainda dependem
do original emulado.

## Organização

| Pasta | Conteúdo |
|---|---|
| `ferramentas/` | Extrator PE, leitores CMP/ETA e reconstrução do carregador de atributos |
| `documentacao/` | Análise técnica em português com evidências e hipóteses |
| `evidencias/` | Trechos x86 selecionados do executável identificado |
| `relatorios/` | Manifesto de hashes, dados recuperados e terreno da missão 1 |
| `testes/` | Casos sintéticos e validação contra o corpus local |
| `ghidra/` | Instalador, launcher, scripts de anotação e análise |

Os relatórios são versionados para permitir comparação entre descobertas. Os
testes que dependem do CD são explicitamente marcados como ignorados se ele
não estiver disponível; os demais continuam executando. Nenhum remoto Git foi configurado.
