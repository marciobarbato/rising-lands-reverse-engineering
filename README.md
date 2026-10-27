# Engenharia reversa de Rising Lands — edição brasileira

Repositório independente dentro da pasta `Rising Lands`, com pesquisa, código e
documentação em português. Os arquivos originais são lidos de `../source/cd`;
o CD, os assets e o protótipo preexistentes continuam fora deste repositório.

Esta entrega reconstrói partes verificáveis do carregamento do jogo a partir de
`RISING.EXE` e dos dados do CD. **Não é o código-fonte original recuperado, nem uma
reimplementação completa do jogo.** Os nomes de funções foram atribuídos pela pesquisa.

## Resultados

- Executável PE x86 de 32 bits identificado por SHA-256, com imports e evidências de runtime Watcom.
- 20 trechos x86 com endereços, bytes e anotações para acompanhar a análise.
- Carregamento dos atributos de 26 tipos de unidade reconstruído em Python.
- Matriz de dano com 27 entradas por atacante, incluindo o tratamento da mina.
- Estrutura de leitura dos 38 mapas ETA recuperada até o fechamento do arquivo nesse caminho.
- Oito arquivos CMP decodificados: 12.268 quadros gráficos.
- Terreno da missão 1 reconstruído com IDs começando em 1, como no renderizador original.
- Testes de regressão com entradas sintéticas, arquivos reais e falhas de formato.

## Leitura recomendada

1. [Relatório da engenharia reversa](documentacao/ANALISE.md): descobertas e limites.
2. [Formatos dos arquivos](documentacao/FORMATOS.md): offsets e sequência de leitura.
3. [Carregador de unidades](documentacao/UNIDADES.md): layout em memória e pseudocódigo.
4. [Catálogo das unidades](relatorios/UNIDADES.md): nomes portugueses, custos e atributos.
5. [Mapa das rotinas](documentacao/ROTINAS.md): onde conferir cada conclusão.
6. [Lacunas e próximos passos](documentacao/CONTINUIDADE.md).

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

## Organização

| Pasta | Conteúdo |
|---|---|
| `ferramentas/` | Extrator PE, leitores CMP/ETA e reconstrução do carregador de atributos |
| `documentacao/` | Análise técnica em português com evidências e hipóteses |
| `evidencias/` | Trechos x86 selecionados do executável identificado |
| `relatorios/` | Manifesto de hashes, dados recuperados e terreno da missão 1 |
| `testes/` | Casos sintéticos e validação contra o corpus local |

Os relatórios são versionados para permitir comparação entre descobertas. Os
testes que dependem do CD são explicitamente marcados como ignorados se ele
não estiver disponível; os demais continuam executando. Nenhum remoto Git foi configurado.
