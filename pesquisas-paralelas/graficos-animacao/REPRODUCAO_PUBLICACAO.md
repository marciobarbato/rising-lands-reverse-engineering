# Publicação parcial no Git e recuperação local

A entrega local **completa** está em `entregas/2026-10-27-soldado-v1/`:
1.120 arquivos de conteúdo, mais `MANIFESTO.json` e `SHA256SUMS`.
SHA-256 do manifesto:
`56d17ebe830036ac9e115549b640f994587590f61b7bcd650fecbf0f3eca5671`.
A verificação local passou. Essa pasta não foi modificada após congelada.

`INVENTARIO_PUBLICACAO.json` e `publicacao-pathspec.txt` delimitam os arquivos
pertinentes à publicação. Esses dois arquivos operacionais, `ESTADO.md` e a
prévia intermediária ficam fora da seleção; o documento presente está incluído.
O estado das etapas de staging e commit fica registrado separadamente em
`ESTADO.md`, sem alterar a entrega congelada.

## O que publicar

Código Python, documentação, templates HTML, assembly extraído, tabelas,
atlas/demonstração, resultados e manifestos de proveniência, tanto na área de
trabalho quanto na revisão congelada. A lista explícita evita adicionar fontes
originais por engano. Os artefatos visuais são recortes/decodificações necessárias
à pesquisa; não constituem uma licença de redistribuição dos gráficos do jogo.

## O que fica local

- Conteúdo de `fontes/`, exceto seu manifesto: EXE, CMP, PIE, INI, ETA e referência.
- Conteúdo de `snapshot/COMMIT/`: recuperável com `git show COMMIT:caminho`.
- Conteúdo de `dependencias/`, exceto seu manifesto: bibliotecas locais copiadas.
- A mesma exclusão vale dentro de `entregas/2026-10-27-soldado-v1/`.
- Caches, builds, temporários e a imagem intermediária `previa.png`.

O manifesto congelado continua descrevendo a entrega **completa**. Um clone
contendo apenas a seleção proposta não deve ser apresentado como pacote íntegro:
o verificador vai acusar os arquivos ausentes. O HTML, atlas e tabelas incorporam
o necessário para inspeção, mas a API/validação do corpus exigem as fontes locais.

## Recuperar os arquivos omitidos sem alterar a revisão

Executar a partir de `pesquisas-paralelas/graficos-animacao`, mantendo o checkout
do repositório principal com o commit base disponível. O exemplo monta uma
**nova pasta** de recuperação. Não escreve dentro de uma entrega existente,
não modifica Git e não baixa fontes. Ausência ou hash divergente é erro explícito.

```sh
python3 -B - <<'PY'
from pathlib import Path
import hashlib, json, subprocess
from verificar_manifesto import verificar

raiz = Path.cwd().resolve()
revisao = raiz / 'entregas/2026-10-27-soldado-v1'
destino = raiz / 'recuperacao-soldado-v1'
destino.mkdir(exist_ok=False)
manifesto = json.loads((revisao / 'MANIFESTO.json').read_text())
fontes = json.loads((revisao / 'fontes/manifesto.json').read_text())
deps = json.loads((revisao / 'dependencias/manifesto.json').read_text())
origens = {x['copia']: x['origem'] for x in fontes}
origens.update({x['caminho']: x['origem'] for x in deps})
commit = manifesto['commit_base']
prefixo = 'snapshot/' + commit + '/'
repo = raiz.parents[1]
for item in manifesto['arquivos']:
    relativo = item['caminho']
    existente = revisao / relativo
    if existente.is_file():
        dados = existente.read_bytes()
    elif relativo in origens:
        dados = Path(origens[relativo]).read_bytes()
    elif relativo.startswith(prefixo):
        dados = subprocess.check_output([
            'git', '-C', str(repo), 'show', commit + ':' + relativo[len(prefixo):]])
    else:
        raise FileNotFoundError('Arquivo publicado ausente: ' + relativo)
    if hashlib.sha256(dados).hexdigest() != item['sha256']:
        raise ValueError('SHA-256 divergente: ' + relativo)
    alvo = destino / relativo
    alvo.parent.mkdir(parents=True, exist_ok=True)
    alvo.write_bytes(dados)
for nome in ('MANIFESTO.json', 'SHA256SUMS'):
    (destino / nome).write_bytes((revisao / nome).read_bytes())
print(verificar(destino))
PY
```

Se os caminhos originais mudaram, localizar os arquivos correspondentes pelo
SHA-256 e adaptar somente o mapa `origens` do procedimento de recuperação.
As dependências nativas registradas são macOS arm64; substituí-las por outra
compilação exige uma nova revisão e novo manifesto. A API normal não necessita
de dependências externas.

## Procedimento de publicação em janela Git coordenada

Somente após autorização e concessão de janela pela coordenação, revisar a lista,
a branch, o HEAD esperado e a situação do índice. Executar staging e commit em
etapas separadas; autorização para staging não autoriza o commit. Os comandos
abaixo descrevem o procedimento, sem representar seu estado de execução:

```sh
git -C '/Users/marcio/git/Rising Lands/engenharia-reversa' add --pathspec-from-file='pesquisas-paralelas/graficos-animacao/publicacao-pathspec.txt'
git -C '/Users/marcio/git/Rising Lands/engenharia-reversa' diff --cached --check -- pesquisas-paralelas/graficos-animacao
git -C '/Users/marcio/git/Rising Lands/engenharia-reversa' diff --cached --stat -- pesquisas-paralelas/graficos-animacao
```

Após a revisão do índice, somente em uma etapa de commit autorizada:

```sh
git -C '/Users/marcio/git/Rising Lands/engenharia-reversa' commit --only --pathspec-from-file='pesquisas-paralelas/graficos-animacao/publicacao-pathspec.txt' -m 'Valida sprites de parada e movimento do Soldado'
```

A exclusão de originais é intencional; não usar `git add` na pasta inteira.
Não há necessidade de repetir emulação, abrir servidor ou ampliar pesquisa para
essa publicação. Preservar o índice e os arquivos das demais frentes.
