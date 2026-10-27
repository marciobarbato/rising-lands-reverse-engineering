# Gráficos e animação — primeiro marco

**Soldado, tipo 0: parada e movimento mapeados e comparados com o x86 original.**
O adaptador e a demonstração funcionam sem Unicorn e sem executar o EXE.

Revisão congelada: `entregas/2026-10-27-soldado-v1/`. A pasta da revisão contém
seu próprio `MANIFESTO.json` e `SHA256SUMS`. Não editar uma revisão publicada.

## Abrir e consultar

- [Demonstração independente](artefatos/demo.html): HTML autônomo, sprites incorporados,
  controles de direção, fase, passo a passo, ampliação e ancoragem. Abrir no navegador.
- [Atlas dos 64 quadros](artefatos/atlas-soldado.png) e [oito paradas](artefatos/parada-soldado.png).
- [Associações CSV](artefatos/associacoes.csv) e [JSON](artefatos/associacoes.json): 144 linhas,
  contando 16 orientações × 8 fases de movimento e 16 paradas.
- [API para o aplicativo](INTEGRACAO.md), [validação](VALIDACAO.md) e
  [registros da missão 1](artefatos/exemplos-eta.json).

```sh
python3 -B graficos.py --tipo 0 --estado parado --direcao 1
python3 -B -m unittest -v test_graficos
```

Os comandos acima são somente leitura, inclusive dentro da entrega congelada.
Usar `-B` evita criação de caches. Python 3.9 ou superior; nenhuma dependência
externa para consultar, decodificar, gerar PNG ou executar os testes Python.

## Fontes e isolamento

Repositório consultado: `/Users/marcio/git/Rising Lands/engenharia-reversa`.
Snapshot: **`1c8ebdd43b0a820652b7cb852ae1fe218d4dea5e`**. Foram copiados 942 arquivos
commitados de leitores, testes, relatórios, documentação e evidências, excluindo
as pesquisas paralelas. `snapshot/manifesto.json` registra cada caminho e SHA-256.
Nenhuma importação usa os módulos do checkout em edição por outros chats.

Fontes do jogo: `/Users/marcio/git/Rising Lands/source/cd/`. Cópias conferidas
estão em `fontes/cd/`; caminhos originais, cópias e hashes estão em
`fontes/manifesto.json`. SHA-256 de `RISING.EXE`:
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

A referência `pesquisas-paralelas/visualizador-mac/referencias/tela-original.png`
foi copiada com hash para `fontes/tela-original.png`. Serviu exclusivamente para
inspeção de aparência: **não é evidência de índices, fases ou temporização**.
O Soldado extraído apresenta as roupas azuis/amarelas, espada e escudo visíveis
nessa referência; essa observação é uma inferência visual independente da prova
por código. Nenhum arquivo do visualizador foi modificado.

## Ordem e índices confirmados

`LoadSTRATBank` (`0x41877a`) lê a tabela de seis ponteiros em `0x495bc8`.
Faz uma passagem pelos cabeçalhos para somar as quantidades e outra para carregar
os quadros, acrescentando cada ponteiro na posição seguinte. Cada descritor
em RAM tem `u16 largura`, `u16 altura`, `u32 tamanho`, `u32 ponteiro_comandos`.
`ProgInit` liga o resultado a `SetBank` em `0x474e9b..0x474eaa`.
`SetBank` grava o vetor em `0x508f6c`. `PasteBobCmp`, em `0x45b259`, consulta
`vetor[id_motor*4 - 4]`: o ID do motor começa em 1.

| CMP | Quadros | Índices globais, base 0 | IDs do motor, base 1 |
|---|---:|---:|---:|
| BLOCS | 1345 | 0–1344 | 1–1345 |
| TROOPS | 2848 | 1345–4192 | 1346–4193 |
| VEHICULE | 915 | 4193–5107 | 4194–5108 |
| CREATURE | 1920 | 5108–7027 | 5109–7028 |
| BUILDING | 611 | 7028–7638 | 7029–7639 |
| OTHERS | 4517 | 7639–12155 | 7640–12156 |

`MENU.CMP` e `INVENTE.CMP` não pertencem a essa concatenação. Seus leitores
foram conferidos, mas esta entrega não atribui a eles IDs desse banco.

Evidências: `evidencias/0041877a.asm`, `00418590.asm`, `00474beb.asm`,
`0045b247.asm` e `tabelas.json`. Na bancada, os **12.156 descritores e blocos
comprimidos** coincidiram com os arquivos, sem deslocamento entre bancos.

## Tipo 0 → direção → fase → CMP

O primeiro registro da tabela de tipos, `0x4965ae`, contém `SOLDAT` no offset
`+0x0c`; `RISING.INI`, seção `SOLDAT`, fornece `NAME=SOLDADO`.
O registro de instância tem tipo em `+1`. `AffEngin` (`0x41591f`) encaminha
os estados 2 e 7 para `AffDeplaceEngin` (`0x412390`). O salto indexado por tipo
em `0x412328` conduz o tipo 0 a `0x412cfe`.

Esse ramo calcula, usando orientação `+0x91`, quantidade `+0xa5` e fase `+0xa4`:

```text
grupo_direcional = floor((direcao + 1) / 2) - 1 = floor((direcao - 1) / 2)
id_motor = 0x822 + grupo_direcional * quantidade_quadros + fase
indice_global = id_motor - 1
indice_local_TROOPS = indice_global - 1345
```

`EnginSetTypeCaract`, ramo `0x45761b`, estabelece quantidade 8 e período 2.
Há oito conjuntos de sprites para 16 orientações internas. As direções ímpares
foram associadas aos deltas da grade executando `0x477042`. As pares reutilizam
o conjunto anterior pela fórmula; não representam oito novos desenhos.
N/S aqui significam acima/abaixo da tela, não coordenadas geográficas.

| Orientações | Delta da direção ímpar | Sentido | Movimento: local base 0 | Parado: local / global / ID |
|---|---|---|---|---|
| 1–2 | −1, 0 | O | 736–743 | 738 / 2083 / 2084 |
| 3–4 | −1, −1 | NO | 744–751 | 746 / 2091 / 2092 |
| 5–6 | 0, −1 | N | 752–759 | 754 / 2099 / 2100 |
| 7–8 | +1, −1 | NE | 760–767 | 762 / 2107 / 2108 |
| 9–10 | +1, 0 | L | 768–775 | 770 / 2115 / 2116 |
| 11–12 | +1, +1 | SE | 776–783 | 778 / 2123 / 2124 |
| 13–14 | 0, +1 | S | 784–791 | 786 / 2131 / 2132 |
| 15–16 | −1, +1 | SO | 792–799 | 794 / 2139 / 2140 |

### Parada e relógio da animação

`EnginEnArret` (`0x448194`, ramo `0x4481c7`) fixa `+0xa4=2` para o tipo 0.
O caminho do estado 2 em `EnginNextEtape` (`0x4563da..`) chama essa rotina
quando a célula e a orientação desejadas foram alcançadas, depois passa ao
estado 7. Portanto a parada estabelecida usa a **terceira fase**, não a primeira.
Esse encadeamento superior foi lido estaticamente; a atribuição da fase e o
desenho dos estados 2/7 foram executados na bancada. Estado 7 pode alterar
orientação ocasionalmente: a demo permite inspeção de direção fixa e não simula
essa escolha aleatória.

Movimento: `+0xa9 = (+0xa9 + 1) & 255`. Somente quando `+0xa9 == +0xa7`,
zera o contador e calcula `+0xa4 = (+0xa4 + 1) % +0xa5`.
Isso foi comparado em `AnimDeplaceEngin` (`0x448088`) e no caminho de movimento
efetivo `0x448f50..0x449048`, parando antes do giro e do avanço físico.
Sem próximo passo nesse caminho, o contador fica intacto. Contador já superior
ao período precisa dar a volta; período zero também depende do overflow.

A sequência cíclica é 0,1,2,3,4,5,6,7. Partindo da parada em fase 2 e contador
zero, as fases após chamadas são 2,3,3,4,…,1,2. **Duas chamadas não significam
dois quadros apresentados nem duração fixa em segundos.** O estado real do
contador deve vir da simulação; a demonstração escolhe contador inicial zero.
`AnimArretEngin` existe e incrementa fase, mas não se deve aplicá-la por seu nome
para animar o Soldado parado; o caminho observado fixa a fase 2.

### Ancoragem

`AffCorpsEnginDecalage`, tabela `0x410f64`, ramo `0x410fe6`: x − 40, y − 22.
O desenho soma antes os deslocamentos assinados de `+0x86/+0x87`.
`AffSprite` percorre as células em incrementos de 32 pixels. O ponto (40,22)
do retângulo CMP corresponde à origem lógica da célula, não ao centro dos pés.
A posição na tela ainda recebe a origem da superfície/viewport do integrador.
Todos os quadros usam essa âncora, mesmo tendo dimensões diferentes (máximo
84 × 67 no conjunto). Não recortar margens e recentralizar cada PNG.

## Composição e relação ETA

O leitor conserva uma máscara de opacidade: comandos positivos pulam destino;
literais copiam os valores, inclusive zero. O corpus contém comandos zero e
terminadores zero; `0x80` continua rejeitado. Todos os 12.268 quadros dos oito
arquivos coincidem com o leitor commitado quanto às dimensões e aos índices.
O blitter básico, incluindo bordas e recorte inclusivo, foi comparado pixel a
pixel. A expansão da paleta PIE segue o snapshot: `v=byte&63`, `0` para zero,
senão `4*v+3`; não foi feita nova comparação com DirectDraw.

Para o Soldado, `0x412d16..0x412d1c` pede a sombra ID **10784**,
`OTHERS.CMP` local **3144**, em célula+(2,26)+deslocamento, antes do corpo.
`PasteOmbreCmp` usa uma tabela apontada por `0x4e24b4` para transformar a cor do
destino. Sua carga e cores finais ainda não foram validadas: a demo exibe somente
o corpo, e a bancada registra a chamada da sombra sem executá-la.

`MONDE01.ETA`: três registros tipo 0, índices 0,1,2; células (7,15), (9,16),
(8,18); estado 7, orientação 1, fase 2 nos bytes serializados. Conferem com ID
2084 pela fórmula. Os offsets de arquivo e hashes dos registros constam no JSON.
A recomposição é `raw[:0x8c] + raw[0x28c:]`; não se apresenta isso como RAM
completamente pós-processada. Construções e objetos ETA não foram associados
a sprites nesta revisão.

## Confiança, lacunas e próximo contrato

**Confirmado por código e comparação x86:** concatenação, convenções de índices,
144 associações, parâmetros 8/2, fase de parada, deltas de direção, âncora,
deslocamentos, transparência e blitter básico com recorte.

**Confirmado apenas por leitura estática ou por arquivo:** encadeamento superior
da parada, chamada da sombra e sua tabela, origem lógica da grade, identidade
SOLDAT/SOLDADO e campos serializados da missão 1. A captura de desenho confirma
a ordem sombra→corpo nesse caminho, não a ordem global de toda a cena.

**Inferência visual:** aparência coerente com a referência enviada. Nenhuma
associação usa essa inferência como validação. **Hipóteses não expostas na API:**
transpor fórmulas para outros tipos, chamar fase 0 de parada, converter o período
em FPS, reaplicar a imagem de sombra como um PNG preto sem sua tabela.

Ainda faltam: outros 25 tipos, construções, árvores/pedras, camadas de objetos e
variantes ETA, ordenação completa de desenho, efeitos, transformação de sombra,
paletas por jogador, HUD, minimapa e seleção. Ataques permanecem com a frente de
combate; esta pasta poderá apenas catalogar suas imagens futuramente.

Contrato necessário ao consumidor: fornecer **tipo, orientação atual 1..16,
fase, contador, célula e deslocamentos i8**; definir quando já está na parada
estabelecida; fornecer origem da superfície. Tipos/estados sem associação dão
erro explícito. O relógio global continua sendo responsabilidade do simulador.
Não existe bloqueio externo para consumir o primeiro marco.

## Manutenção nesta pasta

```sh
python3 -B extrair_evidencias.py
python3 -B gerar_artefatos.py
python3 -B validar_x86.py       # opcional: precisa de Unicorn
python3 -B validar_python.py
python3 -B congelar.py NOVO_IDENTIFICADOR
```

Rodar geradores apenas na área editável, nunca em `entregas/`. Eles recusam a
pasta congelada. A bancada usa Capstone 5.0.9/Unicorn 2.1.4 copiados localmente;
seus hashes e origens constam em `dependencias/manifesto.json`. As bibliotecas
nativas incluídas são macOS arm64. Nenhum Ghidra foi aberto ou criado.
