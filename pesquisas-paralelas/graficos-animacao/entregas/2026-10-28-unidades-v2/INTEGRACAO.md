# Contrato para o aplicativo macOS

Consumir uma cópia integral de `entregas/2026-10-28-unidades-v2/`, verificando
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
- A demo usa jogador 0, que alcança a cópia básica. Recoloração de outros
  jogadores, estados especiais e efeitos ainda não fazem parte da API.
- Sombra separada: ID 10784, local OTHERS 3144, posição célula+(2,26)+deslocamento.
  A matriz de transformação de cores não foi reconstruída. Não mascarar essa lacuna.
- Não usar transparência por `pixel == 0`; usar a máscara. Não recentralizar
  sprites de dimensões variáveis. Usar nearest-neighbor para ampliar.
- Origem lógica de célula não é centro dos pés. Se a UI usa células pelo centro,
  converter o centro para o canto lógico antes de aplicar `(−40,−22)`.
- ETA serializado exige recomposição e pós-processamento; exemplos desta entrega
  descrevem o disco. O adaptador não substitui o carregador/simulador completo.
- Nenhuma rotina de consulta, decodificação ou demonstração depende de x86.
  Somente `bancada_x86.py`/`validar_x86.py`/`validar_trabalhadores.py` dependem de Unicorn para comparação.
  `extrair_evidencias.py` depende de Capstone apenas na extração de assembly.

Verificação de consumo: `python3 -B verificar_manifesto.py CAMINHO_DA_REVISAO`.
Para uma nova pesquisa, copiar a revisão para outra pasta dentro da área
exclusiva e publicar um novo identificador; jamais regravar a revisão recebida.
