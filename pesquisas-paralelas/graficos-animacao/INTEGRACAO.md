# Contrato para o aplicativo macOS

Consumir uma cópia integral de `entregas/2026-10-28-sequenciais-v6/`, verificando
`MANIFESTO.json`. Não importar a área de trabalho desta frente nem os leitores
de outras frentes. Esta entrega não modifica `visualizador-mac`.

## API Python sem x86

`graficos.py` usa apenas a biblioteca padrão. Todas as entradas são relativas à
pasta do próprio módulo, nunca ao diretório corrente ou ao checkout principal.

```python
from graficos import Catalogo, consultar, avancar_animacao, posicao_desenho

catalogo = Catalogo()  # fontes/manifesto.json acompanha a revisão
mapa = consultar(tipo=0, estado='parado', direcao=1)
assert mapa['arquivo_cmp'] == 'TROOPS.CMP'
assert mapa['indice_local'] == 738      # base 0
assert mapa['indice_global'] == 2083    # base 0
assert mapa['id_motor'] == 2084         # base 1

png_rgba = catalogo.imagem_png(tipo=0, estado='parado', direcao=1)
# NSData/NSImage(data:) pode receber esses bytes pelo bridge existente.
# Preservar o retângulo PNG inteiro: 68 × 61 neste caso.

x, y = posicao_desenho(celula_x=7, celula_y=15, origem_x=3, origem_y=11)
assert (x, y) == (88, 106)
# Aplicar depois origem física do viewport e a escala. Eixo y cresce para baixo.

fase, contador = avancar_animacao(fase=2, contador=0)  # (2, 1)
fase, contador = avancar_animacao(fase, contador)     # (3, 0)
mapa_andando = consultar(tipo=0, estado='andando', direcao=9, fase=fase)
assert mapa_andando['id_motor'] == 2117
```

`Catalogo.quadro(id_motor)` retorna `Quadro(largura, altura, pixels, opacidade,
offset_cabecalho, comprimido)`. `pixels` contém índices de paleta; `opacidade`
tem um byte 0/255 por pixel. `rgba()` e `png()` são conversores independentes.
`Catalogo.banco(nome)` permite acesso aos seis bancos, sem atribuir semântica a
quadros não mapeados. O primeiro acesso verifica SHA-256 e mantém cache só em RAM.

`compor_indices(destino, largura, altura, quadro, x, y, recorte=None)` retorna
uma nova superfície indexada. O recorte tem limites inclusivos `(l,t,r,b)`.
Isso implementa a cópia básica de `PasteBobCmp`, não os efeitos por jogador.

## Estado que o consumidor precisa entregar

| Campo na RAM original de 276 bytes | Papel neste contrato |
|---|---|
| `+0x01 u8` | tipo: 0/5/6/7/9 validados |
| `+0x02 u8` | estado 2 passa pelo desenho de movimento; 7 é repouso observado |
| `+0x08 u16` | célula atual: x = baixo byte, y = alto byte |
| `+0x0a u16` | predicado de bolsa vazia/não vazia para tipos 5/6/7 |
| `+0x86/+0x87 i8` | deslocamentos em pixels, somados antes da âncora |
| `+0x91 u8` | orientação atual 1..16; não usar a desejada `+0x90` |
| `+0xa4 u8` | fase 0..7 |
| `+0xa5 u8` | quantidade 8 para Soldado |
| `+0xa7 u8` | período 2 para Soldado |
| `+0xa9 u8` | contador com aritmética de oito bits |

`consultar(..., estado='parado')` significa **parada já estabelecida pela
rotina original**, e fixa a fase conforme o tipo (2 para Soldado). Não usar essa opção para qualquer unidade
momentaneamente sem deslocamento durante um giro/transição. Para inspecionar o
campo `+0xa4` bruto pelo mesmo ramo gráfico, usar `estado='andando', fase=valor`.
O adaptador não traduz todos os códigos de estado da simulação.

### Variantes dos trabalhadores na v2

Tipos aceitos: **0 Soldado, 5 Fazendeiro, 6 Mecânico, 7 Construtor, 9 Colono**.
Os tipos 5/6/7 exigem um argumento adicional, `bolsa_u16`, que deve vir dos
dois bytes em `+0x0a` da instância recomposta, little-endian. Zero escolhe a
variante vazia; qualquer outro valor u16 escolhe a não vazia. Não usar apenas
o primeiro byte. Sem esse campo a consulta falha explicitamente.

```python
import struct
from graficos import consultar, Catalogo, posicao_desenho

# No bridge real: bolsa = struct.unpack_from('<H', registro_ram, 0x0a)[0]
bolsa = 256  # primeiro byte zero, segundo byte diferente de zero
mapa = consultar(tipo=7, estado='parado', direcao=9, bolsa_u16=bolsa)
assert mapa['variante'] == 'bolsa_nao_vazia'
assert (mapa['fase'], mapa['indice_local'], mapa['id_motor']) == (3, 163, 1509)
assert mapa['ancoragem']['x'] == 26
assert posicao_desenho(4, 4, tipo=7) == (102, 102)
imagem = Catalogo().imagem_png(tipo=7, estado='parado', direcao=9, bolsa_u16=bolsa)
```

`posicao_desenho` aceita `tipo` como argumento nomeado; omiti-lo conserva a
âncora do Soldado. `Catalogo.imagem_png` encaminha `bolsa_u16` à consulta.
Não usar a âncora do Soldado para os outros tipos. As âncoras e fases de parada
estão na tabela do README; a quantidade 8 e o período inicial 2 são comuns
aos cinco tipos. Soldado e Colono não dependem da bolsa.

O novo JSON `artefatos/associacoes-unidades.json` contém 1.152 linhas. Inclui
`variante`, `bolsa_u16` e `condicao_variante`; os valores 0/1 nas linhas são
representantes das duas classes do predicado, não os únicos valores possíveis.
O adaptador não identifica qual recurso é carregado. Para inspecionar uma fase
bruta do campo `+0xa4`, usar `estado='andando'`, inclusive quando o estado RAM
for 7; `parado` aplica a fase estabelecida própria do tipo.

Os oito Colonos do ETA de exemplo estão em estado 14. O consumidor não deve
desenhar esses registros pelo ramo 2/7 apenas porque o tipo 9 foi validado.

Ao retomar movimento, preservar o contador fornecido pela simulação. A API não
pressupõe que todo movimento comece na fase 0 ou que a parada zere `+0xa9`.
Uma chamada de `avancar_animacao` corresponde apenas ao trecho efetivamente
executado, não ao callback do renderizador. O integrador controla a frequência.

## Composição indexada na v3

`composicao.py` usa somente Python padrão. `encaminhamento(tipo, estado_u8,
auxiliar_8a=None)` traduz o despacho de `AffEngin` para os cinco tipos. Estados
1, 22 e 24 exigem o byte `+0x8a`, sem valor implícito. A rota `sem_desenho`
significa retorno sem camada nesta função. Outras rotas identificam o handler;
a presença de uma rota não valida quadros de ataque, trabalho, construção ou morte.

```python
from graficos import Catalogo, png
from composicao import tabela_sombra, compor_unidade, encaminhamento

c = Catalogo()
paleta = c.paleta()  # RGB inicial corrigido: 768 bytes
# Parâmetros explícitos do exemplo; não configuração global inferida de uma partida.
tabela = tabela_sombra(paleta, percentual=60, ciclos=())
fundo = bytes([82]) * (128 * 128)
indices, plano = compor_unidade(
    c, fundo, 128, 128, tipo=7, estado_u8=7, direcao=9, fase=3,
    bolsa_u16=256, x=64, y=48, tabela=tabela)
assert [c['id_motor'] for c in plano['camadas']] == [10784, 1509]
rgba = b''.join(paleta[i*3:i*3+3] + b'\xff' for i in indices)
imagem_composta = png(128, 128, rgba)  # bytes para NSImage(data:)
assert encaminhamento(9, 14)['rota'] == 'sem_desenho'
```

`x,y` são a origem da célula já projetada na superfície; `dx,dy` são i8.
O recorte opcional `(esquerda,topo,direita,fundo)` é inclusivo. Coordenadas e
retângulos devem permanecer no domínio de 16 bits usado pelo original; não se
promete equivalência para overflow de coordenadas. A origem da sombra é
`(x+dx+2,y+dy+26)`; o corpo usa a âncora específica do tipo.

`compor_unidade` só compõe corpo nos estados 2/7. Outras rotas `corpo_base`
levantam `NotImplementedError`: saber o handler não valida todos seus caminhos
internos. As rotas `sem_desenho` permanecem disponíveis.

`compor_unidade` retorna `(bytes_indices, plano)` e mantém a fase bruta mesmo
no estado 7. A demonstração aplica a fase de parada estabelecida explicitamente.
Ataque/trabalho/construção/morte levantam `NotImplementedError`, não produzem
sprites aproximados. `sem_desenho` retorna o fundo intacto e `camadas=[]`.

O contrato de composição usa jogador 0 e efeitos/indicadores auxiliares inativos:
na bancada, `+0x74 u16 = 100`, `+0xba = 0`, `+0xdc = 0`, demais campos conforme
inicialização sintética registrada. Não simula regras de fadiga ou experiência.
Para um renderer que desenha só essas duas camadas, os indicadores devem ser
tratados separadamente; não apresentar esta função como cena completa.

`compor_sombra(destino,w,h,quadro,x,y,tabela,recorte=None)` permite aplicar só
uma máscara validada. Cores dos literais são ignoradas, inclusive literal zero:
o índice do fundo seleciona a tabela. Na composição de unidades, aplicar a sombra **antes** do corpo.
As árvores da v5 têm outra ordem: corpo e depois sombra, repetidos em grupos.

`tabela_sombra(paleta, percentual=..., ciclos=...)` exige o percentual u8 e uma
sequência de intervalos inclusivos `(início,fim)` excluídos da busca. Índices 5–7
viram 223–221; 8–15 viram 167. Os demais usam distância RGB quadrática após
multiplicação inteira pelo percentual; empate mantém o menor índice, e 0
permanece candidato inicial mesmo dentro de um intervalo excluído. Ciclagem
posterior da paleta não é reproduzida. O consumidor pode fornecer diretamente
os 256 bytes da tabela original se os tiver, sem recalculá-la.

Os oito Colonos em estado 14 foram testados com a recomposição ETA de 272 bytes
mais cauda de quatro bytes zero não lida pelo caminho. O consumidor precisa
fornecer estado **após** seu carregador; não transformar o estado de disco numa
regra permanente de visibilidade.

## Santuário — API v4 independente

`construcoes.py` não importa Unicorn. `consultar_santuario` retorna um plano
com as sete camadas, já com índices local/global, ordem, offsets, operação e
evidência. Só aceita tipo 2, modo 5, `habitado=True` e `auxiliar_06=0`.
Outros casos levantam `NotImplementedError`; não recebem uma imagem aproximada.

```python
from graficos import Catalogo, png
from construcoes import consultar_santuario, compor_fachada, tabelas_jogador

c = Catalogo()
plano = consultar_santuario(
    tipo=2, modo=5, habitado=True, auxiliar_06=0,
    jogador=1, relogios=(0, 0, 0), celula_mapa=(17, 13))
assert [q['id_motor'] for q in plano['camadas']] == [
    7032, 7050, 7034, 7042, 7059, 7067, 7058]
# Fundo/terreno já composto pelo consumidor; exemplo com índice uniforme.
indices = compor_fachada(c, bytes([82]) * (320*320), 320, 320,
    plano, 224, 160, tabelas=tabelas_jogador())
paleta = c.paleta()
rgba = b''.join(paleta[v*3:v*3+3] + b'\xff' for v in indices)
imagem = png(320, 320, rgba)  # NSData → NSImage(data:)
```

`celula_mapa` é a posição **absoluta do gatilho**, não a origem da construção:
na missão 1, origem (12,11), gatilho (17,13). O gatilho fica no deslocamento
(5,2) do terreno 6×5, ID 749. A coordenada de tela `(224,160)` acima é a
origem dessa célula projetada no viewport. O corpo usa o offset (−150,−93).
Não recentralizar quadros nem posicionar a fachada no centro do terreno.

O integrador verifica visibilidade/ocupação antes de chamar a API. A fachada
não substitui `AffBatiments` inteiro: fica antes de 0x40f342, sem indicadores
posteriores. O terreno utiliza IDs 732..761 em ordem de linhas. A demo o monta
antes da fachada para inspeção; a ordem global com unidades/vegetação ainda
precisa ser investigada. `compor_fachada` não pinta terreno implicitamente.

Entradas externas: tipo +8, modo +5, jogador +4, auxiliar u16 +6 do registro
de construção; resultado de `BatimentEstHabiter`; célula do gatilho; superfície,
recorte inclusivo e relógios. `ler_estruturas_eta(bytes)` lê estritamente o bloco
204 bytes de ETA V0.3, sem pós-processamento ou simulação de regras.

`relogios=(A,B,C)` são u32 em 0x508f7c/80/84. `avancar_relogios` reproduz
somente o prefixo de `ProgIteration`: incrementa A, incrementa B quando o novo
A é par, incrementa C quando divisível por três. Preserva overflow; não converte
para segundos nem presume que B/C sejam divisões de A em um estado arbitrário.

`tabelas_jogador()` fornece cinco tabelas originais de 256 índices; o argumento
opcional `faixas` aceita as três faixas de oito índices de
`evidencias/identidade-construcoes.json`. `compor_fachada` exige as tabelas
explicitamente. Quatro camadas remapeiam a cor da fonte em 160..167; três
usam cópia simples. A máscara CMP é preservada. O exemplo retorna PNG composto;
para desenhar camadas diretamente em Swift, usar ordem/offsets/operação do plano.
Não estender a composição de unidades da v3 a outros jogadores só pela existência
dessas tabelas: o contrato dessa API permanece separado.

Coordenadas e recortes devem ficar no domínio de 16 bits do original, sem
provocar overflow nas somas. O comparador cobre cinco jogadores e quatro
recortes, além das fases; não valida efeitos de clipping específicos de outros
modos de construção. [Continuidade v4](CONTINUIDADE_V4.md) detalha as evidências.

## Objetos do terreno — API v5 independente

`objetos.py` usa somente biblioteca padrão. `consultar_objeto` aceita códigos
1..22 e 28..52 e devolve `terreno` e `sprites` como listas separadas de camadas.
Cada camada contém arquivo CMP, ID base 1, índices local/global base 0, sequência,
fase, operação, ordem, offsets x/y, confiança e evidência. Código sem comparação
levanta `NotImplementedError`; não recebe uma imagem por semelhança.

```python
from graficos import Catalogo, png
from composicao import tabela_sombra
from objetos import consultar_objeto, compor_passe, avancar_arvore

c = Catalogo()
plano = consultar_objeto(5, auxiliar_u8=1, descoberta_u8=0, iluminacao_u8=0)
assert plano['terreno'] == []
assert [q['id_motor'] for q in plano['sprites']] == [
    10518, 10546, 10526, 10554, 10522, 10550]
paleta = c.paleta()
# Entradas declaradas de inspeção: não representam inicialização global provada.
sombra = tabela_sombra(paleta, percentual=60, ciclos=())
indices = compor_passe(c, bytes([82]) * (160*160), 160, 160,
    plano, 'sprites', 64, 108, tabela_sombra=sombra)
rgba = b''.join(paleta[v*3:v*3+3] + b'\xff' for v in indices)
imagem = png(160, 160, rgba)  # bytes para NSData / NSImage(data:)

# Tabela sintética explícita; no consumo real, fornecer os 256 bytes do simulador.
proximo = avancar_arvore(fase_u8=3, relogio_u32=0,
    indice_aleatorio_u8=255, tabela_aleatoria=bytes(256))
assert proximo == {'fase': 0, 'indice': 0, 'consumiu': True}
```

`x,y` são a origem da célula projetada na superfície. Preservar todos os offsets,
dimensões e a ordem das camadas. `compor_passe` retorna os bytes indexados;
`recorte=(l,t,r,b)` é inclusivo. Manter coordenadas no domínio de 16 bits sem
overflow. Não há alpha preto de sombra: a máscara remapeia o destino pela tabela.
**Nas árvores, corpo → sombra, repetidos componente a componente.** Não reordenar
usando a regra sombra → corpo das unidades. A API não determina ordem global
entre células, objetos, construções e unidades.

| Entrada | Origem / significado |
|---|---|
| `codigo` | u8 de objetos em `0x507d74[celula]`; disco ETA em `0x30004+celula` |
| `auxiliar_u8` | u8 em `0x507dac[celula]`; disco em `0x40004+celula` |
| `descoberta_u8` | byte na camada apontada por `0x507d78+4*jogador`; descoberto se bits 0..4 são zero |
| `iluminacao_u8` | byte na camada apontada por `0x507d88+4*jogador`; iluminado se bit 4 é zero |
| `relogio_u32` | relógio A em `0x508f7c`, na chamada de avanço |
| `tabela_aleatoria` | 256 bytes em `0x4e1c18`; entrada exigida, sem distribuição presumida |
| `indice_aleatorio_u8` | cursor compartilhado em `0x4e1d18` |

Árvores 1..11: auxiliar 0..3 seleciona a fase; fora dessa faixa a consulta
levanta `ValueError`, mesmo se o objeto estiver oculto. Demais códigos aceitos
ignoram o auxiliar u8 e têm uma camada estática. Sem descoberta, ambos os passes
ficam vazios. Sem iluminação, o corpo escolhe sequência escura; a sombra mantém
os IDs. Flags não vêm dos atributos de colisão do ETA e não são opcionais.

`avancar_arvore` não incrementa A nem escolhe valores aleatórios. Se A não é
múltiplo de quatro, mantém fase/cursor. Se é, consome exatamente um byte e avança
cursor com overflow; só incrementa fase (módulo quatro) quando o byte lido é
múltiplo de quatro. Retorna `fase`, `indice`, `consumiu` sem alterar entradas.
Aceita fase bruta u8 para reproduzir o avanço original; o desenho continua
restrito a 0..3. Chamá-la somente para 1..11; a ordem por linhas e o cursor entre
árvores devem ser mantidos pelo consumidor. Inicialização da tabela e taxa de
chamadas ainda são contratos externos, sem substitutos implícitos.

`ler_objetos_eta(bytes)` aceita ETA V0.3 completo até 0x50004 e retorna hashes
das camadas e registros não zero com célula, x/y, código, auxiliar, ID de terreno,
offsets e `mapeado`. Esse último campo identifica somente o código dentro do
contrato, não garante fase válida nem estado final após pós-processamento.
No exemplo MONDE01, 470 de 486 registros têm códigos mapeados; 66/67 ficam sem
associação. O arquivo `artefatos/associacoes-objetos.json` pode ser consumido
diretamente no bridge Swift. Nomes de classes visuais não são regras econômicas.

## Objetos sequenciais — API v6 independente

`sequenciais.py` amplia a consulta sem alterar a API v5. Para consumir todos os
51 códigos confirmados, usar `consultar_objeto_v6`. Para 54/66/67/68 isoladamente,
usar `consultar_sequencial`; ambos retornam listas `terreno` e `sprites`
compatíveis com `compor_passe` da v5.

```python
from graficos import Catalogo
from composicao import tabela_sombra
from objetos import compor_passe
from sequenciais import consultar_objeto_v6, ler_objetos_eta_v6, normalizar_inicio

c = Catalogo()
p = consultar_objeto_v6(67, auxiliar_u8=14, descoberta_u8=0, iluminacao_u8=16)
assert p['fase'] == 7
assert [(q['id_motor'], q['operacao']) for q in p['terreno']] == [
    (10846, 'copiar'), (10846, 'sombra')]
tab = tabela_sombra(c.paleta(), percentual=60, ciclos=())  # parâmetros do ensaio
indices = compor_passe(c, bytes([82])*(160*160), 160, 160,
    p, 'terreno', 64, 108, tabela_sombra=tab)
# Converter a superfície indexada para RGBA/PNG como nos exemplos anteriores.

# Entrada de disco fornecida pelo consumidor, sem inicializar o jogo.
dados = c._ler('cd/WORLD/MONDE01.ETA')  # somente no exemplo do corpus local
registros = ler_objetos_eta_v6(dados)
assert len(registros['registros']) == 486
assert all(r['mapeado'] for r in registros['registros'])
normalizado = normalizar_inicio(dados[0x30004:0x40004], dados[0x40004:0x50004])
assert normalizado['alteradas'] == []  # MONDE01 já não contém código 54
```

`codigo`, `auxiliar_u8` e flags têm as mesmas origens da API v5. Códigos 66..68
exigem auxiliar 0..31: `fase=floor(auxiliar/2)`, ID base 10823/10839/10855.
Os pares 0/1 até 30/31 são equivalentes. A consulta recusa valores 32..255,
pois o cálculo bruto atravessa outras sequências. O original não testa essa
faixa; o limite é deliberado do contrato público. Código 54 ignora qualquer
auxiliar u8 e usa sempre 10823. O offset é (−4,0) para 54/66 e (0,0) para 67/68.
Nenhum desses códigos produz camada em `sprites`.

Sem descoberta, nenhuma camada. Sem iluminação, **copiar → sombra**, com o mesmo
CMP, posição e máscara. Não escolher outro banco/variante escura. A tabela de
sombra é externa e deve ter 256 bytes. Transparência usa a máscara CMP e o
recorte é inclusivo; coordenadas sem overflow no domínio original de 16 bits.

Não aplicar `avancar_arvore` a esses quatro códigos. `NextAnimVeget` preserva
seus campos em 4.096 comparações; o consumidor fornece o auxiliar atualizado
por sua simulação. Não há temporização, quantidade de recurso ou regra de coleta
nesta API. Os nomes `classe_visual` são inferências de aparência.

`normalizar_inicio(objetos, auxiliares)` exige duas camadas de 65536 bytes e
retorna cópias em `objetos`/`auxiliares`, mais os índices `alteradas`. Faz somente
54 → 66/auxiliar 1, como o laço original em MissionLoad. Não altera entradas nem
executa todo o carregador. `ler_objetos_eta_v6` mantém leitura de disco e acrescenta
`catalogo` v5/v6; `mapeado` cobre o código, não garante estado final da missão.

## Ponte mínima por JSON

```sh
python3 -B graficos.py --tipo 0 --estado andando --direcao 9 --fase 3
```

Campos principais do resultado:

```json
{
  "arquivo_cmp": "TROOPS.CMP",
  "indice_local": 771,
  "indice_global": 2116,
  "id_motor": 2117,
  "tipo": 0,
  "estado": "andando",
  "direcao": 9,
  "direcao_sprite": "L",
  "fase": 3,
  "ancoragem": {"x": 40, "y": 22, "referencia": "origem da celula de 32x32"}
}
```

O JSON real inclui sequência, período, confiança e endereços de evidência.
`vetor_mapa` só é fornecido para direções ímpares; nas pares é `null`.
`vetor_direcao_sprite` descreve a imagem compartilhada, não autoriza um passo
da simulação nas orientações pares.
Outra opção é consumir `artefatos/associacoes.json` diretamente no Swift e usar
os PNGs produzidos pelo adaptador. Não depender da página HTML para obter dados.

## Limites obrigatórios para a integração

- Tipo fora de 0/5/6/7/9: `NotImplementedError`. Estado textual fora de
  `parado/andando`, direção fora de 1..16 e fase fora de 0..7: `ValueError`.
- A composição de unidades usa jogador 0. A API v4 de Santuário aceita as
  cinco tabelas originais no contrato acima; estados especiais e efeitos
  permanecem fora dessas APIs.
- Sombra separada das unidades: ID 10784, local OTHERS 3144, posição célula+(2,26)+deslocamento.
  A matriz é produzida por `tabela_sombra` com percentual/ciclos explícitos.
  Não substituir remapeamento de destino por um PNG preto com alpha.
- Não usar transparência por `pixel == 0`; usar a máscara. Não recentralizar
  sprites de dimensões variáveis. Usar nearest-neighbor para ampliar.
- Origem lógica de célula não é centro dos pés. Se a UI usa células pelo centro,
  converter o centro para o canto lógico antes de aplicar `(−40,−22)`.
- ETA serializado exige recomposição e pós-processamento; exemplos desta entrega
  descrevem o disco. O adaptador não substitui o carregador/simulador completo.
- Nenhuma rotina de consulta, decodificação ou demonstração depende de x86.
  Somente `bancada_x86.py`/`validar_x86.py`/`validar_trabalhadores.py`/`validar_composicao.py`/`validar_construcoes.py`/`validar_objetos.py`/`validar_sequenciais.py` dependem de Unicorn para comparação.
  `extrair_evidencias.py` depende de Capstone apenas na extração de assembly.

Verificação de consumo: `python3 -B verificar_manifesto.py CAMINHO_DA_REVISAO`.
Para uma nova pesquisa, copiar a revisão para outra pasta dentro da área
exclusiva e publicar um novo identificador; jamais regravar a revisão recebida.
