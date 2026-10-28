# Continuidade v6 — códigos 54/66/67/68 e cobertura da missão 1

Revisão: `2026-10-28-sequenciais-v6`. Branch: `codex/graficos-animacao`.
Predecessor próprio: `d96034af2a264e77dc49269c6e0fe563cfddabf4`.
Snapshot principal: `1c8ebdd43b0a820652b7cb852ae1fe218d4dea5e`.
Repositório: `/Users/marcio/git/Rising Lands/engenharia-reversa`.
Fontes originais somente leitura: `/Users/marcio/git/Rising Lands/source/cd/`.
Caminhos/commits/SHA-256 em `evidencias/proveniencia-v6.json`,
`fontes/manifesto.json`, `snapshot/manifesto.json`, `dependencias/manifesto.json`.
EXE: `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Nenhuma entrega congelada anterior foi modificada.

## Resultado verificável

Os códigos **66 e 67**, que representam os 16 objetos sem associação da v5,
foram ligados aos CMPs por código e comparação x86. O mesmo ramo também cobre
**68**, validado sinteticamente; o código **54** tem um caminho fixo próprio.
São **48 CMPs distintos**, **147 associações** e mais quatro códigos gráficos.
A API unificada `consultar_objeto_v6` aceita 51 códigos; o leitor ampliado
cobre **486/486 objetos não zero serializados** em `MONDE01.ETA`.
Isso não equivale à missão completamente carregada ou à cena final validada.

A inspeção visual sugere fragmentos cinzentos no 66, formas alaranjadas no 67 e
blocos cinzentos no 68. Esses nomes são rótulos de aparência. Não confirmam
recurso, quantidade, coleta, consumo ou outra regra econômica.

## Código → auxiliar → CMP → operações

`AffVegetTerrain` em **0x410085** testa o código em 0x410104..0x41011c.
O código 66 entra em **0x4104af**, deslocando x em −4. Códigos 67 e 68 entram
em **0x4104b1**, sem esse deslocamento. O auxiliar vem da camada apontada por
`0x507dac`, indexada pela célula recebida em EBX, `y*256+x`.
O corpo em 0x4104be..0x410504 calcula:

```text
fase_visual = floor(auxiliar_u8 / 2)
id_motor = 0x2a47 + 16*(codigo - 66) + fase_visual
indice_global = id_motor - 1
indice_local_OTHERS = id_motor - 7640
```

| Código | ID motor, auxiliar 0..31 | Local OTHERS | Global | Offset x,y |
|---|---|---|---|---|
| 66 | 10823..10838 | 3183..3198 | 10822..10837 | −4,0 |
| 67 | 10839..10854 | 3199..3214 | 10838..10853 | 0,0 |
| 68 | 10855..10870 | 3215..3230 | 10854..10869 | 0,0 |
| 54 | 10823 fixo, auxiliar ignorado | 3183 | 10822 | −4,0 |

Cada par 0/1, 2/3, …, 30/31 escolhe o mesmo quadro. **Fase visual aqui é um
índice**, não uma animação temporal comprovada. A API exige auxiliar 0..31 para
66..68, cobrindo os 16 CMPs próprios de cada sequência. O original aceita o byte
inteiro e calcula índices também para 32..255: as capturas desses casos estão
registradas, mas atravessam as sequências seguintes. Não são expostas como
mapeamento válido do tipo. Nenhuma verificação original de faixa foi inventada.

O código 54 é reconhecido em **0x41059a**, ramo **0x41053d**. Usa sempre 10823;
seu auxiliar não participa do desenho. A ancoragem é a origem lógica da célula
32×32, com os offsets acima, sem recentralizar o retângulo CMP.

Descoberta/iluminação usam os predicados já validados na v5: descoberta exige
`(flag & 31)==0`; iluminação, `(flag & 16)==0`. Sem descoberta, não há camada.
Com iluminação, uma cópia. Sem iluminação, o ramo **0x410509..0x410538** copia
e depois aplica **sombra com o mesmo ID e posição**. O caminho 54 faz o mesmo
em 0x41055b..0x410582. O passe `AffVeget` de sprites não desenha esses códigos.

A sombra remapeia o destino pela máscara do CMP e tabela de 256 bytes. Não usa
uma segunda sequência escura nem alpha preto. Literal zero permanece opaco.
Os testes usam a tabela original do ensaio v3, percentual 60 e ciclos vazios,
como entradas declaradas; a inicialização global final segue não comprovada.

## O trecho de carregamento e o ETA

O laço de `MissionLoad` **0x46c3de..0x46c40a** percorre 65536 células.
Se o código é 54, grava **66 e auxiliar 1**; caso contrário, preserva os dois
bytes. Foi executado integralmente em duas fixtures: as camadas da missão 1 e
uma matriz contendo todos os 256 códigos × todos os 256 auxiliares. Resultado:
zero alterações na missão 1 e 256 conversões na fixture sintética. Os blocos de
atributos e terreno foram preservados. Não foram substituídas chamadas no laço.

`normalizar_inicio` reproduz apenas esse trecho, em cópias novas das camadas.
Não executa o restante de MissionLoad, MissionPlaceTerrain ou atualizações da
simulação. O leitor ETA fornece estado **de disco**; as flags por jogador são
entradas externas e não são derivadas do bloco de atributos do arquivo.

Os 16 registros reais são 7 de código 66 e 9 de código 67, com auxiliares
1..14. Seus dois estados de iluminação produziram 32 comparações de superfícies
originais. Exemplos verificáveis:

| Célula | Código / auxiliar | Offset objeto / auxiliar | ID |
|---|---|---|---|
| (54,4) | 66 / 5 | 0x3043a / 0x4043a | 10825 |
| (42,13) | 67 / 6 | 0x30d2e / 0x40d2e | 10842 |
| (16,48) | 67 / 14 | 0x33014 / 0x43014 | 10846 |

`artefatos/exemplos-eta-v6.json` mantém os 486 registros e identifica `catalogo`
v5/v6. O leitor antigo continua com cobertura 470, preservando seu contrato.
`consultar_objeto_v6` encaminha os códigos antigos à API v5 sem mudar o resultado.

## Avanço e contrato externo

`NextAnimVeget` **0x4772ec..0x4774fa** foi executada para os quatro códigos,
todos os auxiliares u8 e quatro resíduos do relógio: **4.096 casos**. Código,
auxiliar e cursor aleatório foram preservados. O ramo de despacho em
0x477485..0x4774b8 desvia desses códigos antes das atualizações.

Isso confirma somente a ausência de avanço **nessa rotina**. Não confirma que
o auxiliar seja imutável no jogo. Sua origem/alteração por outras rotinas e
regras econômicas pertencem a contrato externo; esta pesquisa gráfica não as
implementa. A página permite percorrer valores para inspeção em cinco valores
por segundo, sem simular um período original.

## Entrega e validação

- **73 testes Python**, sem x86, passaram em 4,466 s de suíte. As dez novas
  regressões usam capturas e hashes originais como oráculo, além dos contratos
  de rejeição, normalização e integridade dos artefatos.
- **10.387 execuções x86 delimitadas**, **3.605.938 instruções**, 4,718 s observados.
  Incluem 6.144 capturas (todos os auxiliares, três visibilidades, dois passes),
  4.096 casos de NextAnimVeget, duas normalizações completas, leitura ETA e banco.
- **142 buffers 160×160 idênticos**: 98 sequências/iluminação, 12 recortes e
  32 casos dos registros ETA. Blitters originais executados integralmente.
- Navegador: **291 planos gráficos** e **98 buffers completos** JS/Python;
  pareamento, passo 31→0, iluminação, ocultação, forma 54, transformação,
  reprodução/pausa, registros ETA, sombras e âncora inspecionados. Sem erros de
  console. Captura em `validacao/demo-sequenciais-verificada.png`.

O EXE é conferido por SHA-256 antes da emulação. Processo próprio, intervalos
permitidos, timeout de 2 s e máximo de 1 milhão de instruções por execução.
IO/alocação somente no carregamento de bancos, FileRead no trecho ETA e blitters
somente nas capturas são substituídos. Pixels, normalização e NextAnimVeget não
usam stubs. Nenhum jogo/Ghidra ou processo de outra frente foi manipulado.

**Dependência x86 explícita:** `validar_sequenciais.py`, por `BancadaObjetos` e
`bancada_x86.py`, exige Unicorn 2.1.4 local. A API `sequenciais.py`, atlas,
demonstração e testes Python usam somente biblioteca padrão. Nenhuma nova
extração Capstone foi necessária: os intervalos já estavam nas evidências
commitadas, cujos hashes/bytes são revalidados pelos testes anteriores.

## Lacunas e próximo caso independente

Continuam pendentes: origem/alteração do auxiliar fora de NextAnimVeget,
carregador completo, outros códigos, todos os estados especiais, ordenação
global e configuração global de sombra. A cobertura 486/486 refere-se somente
às camadas de objetos **serializadas da missão 1**. Não generalizar para todas
as missões nem converter nomes de aparência em regras econômicas.

Próximo caso gráfico: seleção e barras de vida das unidades já mapeadas, com
contrato explícito para os campos fornecidos pelo simulador. Não é necessário
esperar respostas das outras frentes para rastrear esses caminhos de desenho.
