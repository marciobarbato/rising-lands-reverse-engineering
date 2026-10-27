# Relatório de engenharia reversa

## Objeto e método

A análise usa o executável local `../source/cd/INSTALHD/RISING.EXE`, com 665.600
bytes e SHA-256:

```text
6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
```

A pesquisa foi estática: leitura PE, strings, referências, desmontagem x86,
reconstrução de leitores e confronto com o corpus completo de 38 mapas e oito
arquivos gráficos. O executável Windows não foi executado. Não se recuperaram
símbolos originais, projetos de compilação ou uma decompilação integral.

**Confirmado** significa sustentado por instruções específicas ou bytes de
arquivos; **inferido** significa interpretação compatível ainda sem validação
dinâmica; **desconhecido** significa que a pesquisa preserva os dados sem inventar
uma interpretação. Nomes descritivos não são símbolos encontrados no EXE.

## Arquitetura observada

O cabeçalho PE informa máquina `0x14c` (x86), base preferencial `0x00400000` e ponto
de entrada `0x0048d3c8`. As seções incluem `BEGTEXT`, `DGROUP`, `.bss`, `.idata`,
`.reloc` e `.rsrc`. O campo `VirtualSize` é zero nas seções deste arquivo; o
relatório preserva isso e não o confunde com inexistência dos dados.

Uma string interna identifica o runtime WATCOM C/C++32. Isso sustenta a associação
com essa cadeia de ferramentas, mas não comprova a versão exata do compilador
nem se cada módulo foi escrito em C ou C++. As rotinas internas examinadas usam
registradores para argumentos; não é correto aplicar `cdecl` indistintamente.
As APIs Windows importadas usam chamadas indiretas pela IAT.

| Subsistema | Evidência | Alcance da conclusão |
|---|---|---|
| Janela e eventos | `CreateWindowExA`, `PeekMessageA`, `DispatchMessageA` | Uso de Win32 confirmado |
| Desenho | `DDRAW.dll!DirectDrawCreate` e rotinas de tiles | DirectDraw confirmado; pipeline completo pendente |
| Som | `DSOUND.dll!DirectSoundCreate` | Dependência confirmada; mixer não reconstruído |
| Vídeo | `MSVFW32.dll!MCIWndCreateA` | Interface de vídeo importada |
| Multijogador | `DPLAYX.dll`, ordinais 1 e 2 | Dependência confirmada; nomes dos ordinais não presumidos |
| Temporização | `GetTickCount`, `timeGetTime` | Fontes de tempo disponíveis; frequência da simulação desconhecida |
| Configuração | `GetPrivateProfileIntA`, `GetPrivateProfileStringA` | Leitura direta de INI confirmada nos carregadores |

O inventário completo está em [executavel.json](../relatorios/executavel.json).

## Descobertas de código

### Atributos das unidades

O carregador `0x44188b` percorre **26 tipos**, usando registros de **50 bytes** a
partir de `0x4965ae`. A seção do INI vem do nome francês embutido no registro.
Depois de ler os atributos, `NAME` substitui esse texto pelo nome localizado.
Assim, `VOLEUR` aparece como **ARQUEIRO** nesta edição; a tradução literal do
identificador interno seria enganosa.

O alcance `PORTEE` é elevado ao quadrado antes de ser armazenado (`0x4419ac` e
`0x4419bf`). Para o capitão, a entrada 8 resulta em 64. Isso é compatível com
comparações de distâncias quadráticas, mas a comparação final no combate ainda
precisa ser rastreada. Valores de fadiga e recrutamento não foram convertidos
arbitrariamente para segundos.

`0x441792` carrega 27 valores de `DEGAT` para cada atacante. A alocação em
`0x441a1b` cria 27 linhas de 27 bytes, sendo a linha adicional usada para `MINE`.
A matriz contém valores de entrada; não equivale à fórmula final de dano, que
pode considerar blindagem, bônus e estado da unidade.

### Mapas e unidades serializadas

O caminho `0x46c2cf` ignora os quatro bytes iniciais, lê quatro camadas de tamanho
fixo e depois recursos, dimensões, origens de visualização e blocos variáveis.
Cada mapa mantém passo de linha de **256 células**, mesmo quando a área jogável
mede 64 × 64. O extrator evita o erro de usar a largura jogável como passo físico.

A leitura encadeada foi reconstruída até o encerramento do arquivo. Em **todos
os 38 mapas**, restam exatamente **917.504 bytes (`0xe0000`)** depois do trecho
consumido por esse caminho. Esse sufixo não é declarado conhecido apenas porque
seu tamanho é constante; ele recebe offset e hash próprios nos relatórios.

Registros de unidades têm 784 bytes no disco. O código copia 140 bytes, avança
512 bytes e copia os 132 restantes para uma estrutura com passo 276 em RAM.
Portanto, não se pode mapear o registro do disco diretamente sobre a estrutura
em memória. A alocação observada comporta 800 registros; isso não basta para
afirmar um limite global de unidades em todas as modalidades do jogo.

A missão 1 contém **16 registros de unidades**: oito colonos, três soldados,
dois fazendeiros, um incendiário, um construtor e um arqueiro. Todas pertencem
ao proprietário 0. Posições e vida foram recuperadas; os oito colonos compartilham
a célula (14, 12), em estado 14. A visibilidade de cada estado ainda exige pesquisa.
Veja [INSTANCIAS.md](INSTANCIAS.md) para as 2.604 entradas da campanha.

O Ghidra está instalado localmente e exportou 250 rotinas relacionadas às unidades.
A [receita de instalação e análise](GHIDRA.md) explica a cópia PE normalizada,
as assinaturas por registradores e as limitações do pseudocódigo automático.

### Gráficos e correções à interpretação anterior

O carregador CMP confirma cabeçalhos de largura, altura e tamanho do fluxo.
A rotina de composição `0x45c779` interpreta bytes com sinal: positivos avançam
o destino, negativos copiam literais. O leitor expande esses avanços para índice
zero em uma imagem transparente. Os oito arquivos fecharam sem sobra e sem
divergência de dimensões, totalizando 12.268 quadros.

O renderizador acessa a tabela de quadros com `[base + id*4 - 4]` em `0x41078a`.
O agregador grava o primeiro quadro na posição zero. Logo, os IDs dessa tabela
são baseados em **1**. A geração anterior em `../tools/assets.py` usa
`tiles[tile]`, que desloca o terreno em um quadro. A nova imagem usa
`quadros[id - 1]`. Isso também torna inadequado tratar o tile 134 como marcador
TEMP apenas com base na imagem produzida pelo índice anterior.

As palavras de `0x50020` são lidas para `0x508720`/`0x508722` e usadas como origem
do desenho do terreno em `0x474b6f..0x474b80` e `0x41068e`. O protótipo as chama
de `spawn` e coloca um soldado ali; essa atribuição não comprova a posição de
nascimento de uma unidade no jogo original.

O protótipo Swift foi preservado. Seu A*, velocidade de 72 pixels/s, passo de
1/60 s e escolha de animações são implementações locais; esta análise não os
classifica como algoritmos recuperados do original.

## Validação e limites

`sh testar.sh` cobre comandos CMP, arquivos truncados, expansão gráfica integral,
paleta comparada com LZS, todos os mapas, composição de unidades da primeira
missão, offsets de término e reconstrução de atributos. O mapa gerado foi
inspecionado visualmente para conferir continuidade do terreno. É uma renderização
da camada estática, não uma captura do jogo original.

Passar nos testes confirma esses leitores e invariantes do corpus. Não confirma
equivalência de gameplay: combate, IA, economia, gatilhos, salvamento completo,
áudio e rede ainda exigem pesquisa. Veja [CONTINUIDADE.md](CONTINUIDADE.md).
