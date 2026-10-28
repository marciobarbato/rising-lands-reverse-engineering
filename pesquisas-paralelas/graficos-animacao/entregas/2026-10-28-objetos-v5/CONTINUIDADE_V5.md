# Continuidade v5 — objetos, árvores e dois passes

Revisão: `2026-10-28-objetos-v5`. Predecessor próprio:
`46e826c7c112a2ddda4376d8587500cc7e742f68`. Snapshot principal:
`1c8ebdd43b0a820652b7cb852ae1fe218d4dea5e`.
Repositório lido: `/Users/marcio/git/Rising Lands/engenharia-reversa`.
Fontes originais: `/Users/marcio/git/Rising Lands/source/cd/`; cópias privadas
em `fontes/cd/`. Caminhos, commits e SHA-256 estão em
`evidencias/proveniencia-v5.json`, `fontes/manifesto.json`,
`snapshot/manifesto.json`, `dependencias/manifesto.json` e `evidencias/manifesto.json`.
EXE: `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Somente esta pasta foi escrita; insumos e entregas anteriores foram preservados.

## Resultado verificável

**47 códigos de objetos, 156 quadros CMP e 344 associações validados** por
leitura do original e comparação x86. Códigos **1..11** têm aparência de árvores
ou grupos; **12..22**, vegetação baixa; **28..52**, detalhes do solo, incluindo
pedras, tocos e plantas. Essas classificações são inferências visuais; não
atribuem recurso, capacidade de coleta ou qualquer função econômica.

Todos os quadros são de OTHERS.CMP: IDs **10517..10672**, índices locais
**2877..3032**, globais **10516..10671**. As 344 linhas distinguem código,
iluminação, componente e fase; sombras compartilhadas aparecem mais de uma vez.
Direção não se aplica a esses objetos e está explicitamente nula.

`objetos.py` consulta, avança uma árvore e compõe cada passe em Python padrão.
A demonstração `artefatos/demo-objetos.html` incorpora os quadros e funciona
offline. O primeiro marco das cinco unidades e o Santuário seguem disponíveis.

## ETA e visibilidade

`MissionLoad`, trecho **0x46c3a2..0x46c3de**, lê quatro blocos em sequência.
Foram executadas as quatro leituras com FileRead em memória; seus bytes e hashes
coincidem com o arquivo. A parada é anterior ao pós-processamento da missão.

| Bloco | Offset ETA V0.3 | Tamanho | Ponteiro global |
|---|---|---:|---|
| Atributos | 0x00004 | 65536 | 0x507da8 |
| Terreno, u16 | 0x10004 | 131072 | 0x507d70 |
| Objetos, u8 | 0x30004 | 65536 | 0x507d74 |
| Auxiliares, u8 | 0x40004 | 65536 | 0x507dac |

A célula é `y*256+x`. `MONDE01.ETA` contém 486 objetos não zero; **470** são
cobertos: 38 árvores, 308 vegetações baixas e 124 detalhes de solo. Os outros
16 são código 66 (7) e 67 (9), mantidos sem associação. Código 52 não ocorre
nesse ETA, mas foi validado com entrada sintética na bancada. Os dados estão
em `artefatos/exemplos-eta-objetos.json`, com offsets e auxiliar de cada célula.
Não se afirma que o objeto de disco permanece igual após o carregador completo:
por exemplo, o trecho estático 0x46c3f6..0x46c404 transforma 54 em 66, auxiliar 1.

As flags de descoberta e iluminação vêm de camadas **por jogador**, não do
bloco de atributos do ETA. A API exige os dois bytes. Cada predicado foi testado
para todos os 256 valores:

- `TerrainEstDecouvert` **0x4766f0**: `(descoberta & 31) == 0`, ponteiro em
  `0x507d78 + 4*jogador`.
- `CaseEstIlluminee` **0x47693a**: `(iluminacao & 16) == 0`, ponteiro em
  `0x507d88 + 4*jogador`, retorno compartilhado em 0x4766e8.

Não confundir o primeiro com `CaseEstDecouverte`, usado pelo Santuário, que
consulta somente o bit 0x10. Se não descoberto, nenhum desses objetos é pintado.
Se descoberto e sem iluminação, são selecionados CMPs escuros próprios.

## Dois passes e ancoragem

`AffVegetTerrain` **0x410085..0x41068e** desenha 12..22 e 28..52.
O chamador `AffTerrain` o invoca após pintar uma célula de terreno (0x4107b0).
`AffVeget` **0x415acf..0x416864** desenha 1..11; `AffSprite` o invoca em
0x416b8a antes das chamadas de construções/unidades daquela célula. Esses
chamadores foram lidos estaticamente; não se executou a ordenação global da cena.
Os dois passes testados foram executados até o retorno, incluindo o retorno
compartilhado 0x410b38..0x410b40. O passe não correspondente produz zero camadas.

O despacho de AffVeget usa REPNE SCASB, ECX=24, bytes em 0x415a58 e tabela de
24 ponteiros em 0x415a6f. O último byte consultado sobrepõe o primeiro byte da
tabela de ponteiros; sua duplicação mantém o ramo padrão. Os bytes, ponteiros e
256 rotas calculadas estão em `evidencias/despacho-objetos.json`. Isso é análise
estática de despacho, não validação de gráficos de todos os 256 códigos.

Nas árvores, o auxiliar 0..3 é somado aos IDs base abaixo. Para corpo sem
iluminação, somar também **92**; o ID da sombra não muda. As posições são
relativas à origem lógica da célula de 32×32. A sequência é **corpo, sombra**,
repetida para cada componente do grupo; não agrupar todas as sombras antes.

| Código | Pares: corpo base@(x,y) → sombra base@(x,y) |
|---|---|
| 1 | 10525@(2,−27) → 10553@(9,13) |
| 2 | 10521@(−4,−36) → 10549@(6,21) |
| 3 | 10517@(−3,−83) → 10545@(16,6) |
| 4 | 10517@(3,−89) → 10545@(22,0); 10525@(−3,−19) → 10553@(4,21) |
| 5 | 10517@(−4,−91) → 10545@(15,−2); 10525@(−7,−24) → 10553@(0,16); 10521@(15,−34) → 10549@(25,23) |
| 6 | 10537@(−4,−25) → 10565@(9,16) |
| 7 | 10533@(−7,−43) → 10561@(14,14) |
| 8 | 10529@(−11,−65) → 10557@(12,13) |
| 9 | 10529@(−15,−75) → 10557@(8,3); 10537@(7,−17) → 10565@(20,24) |
| 10 | 10529@(−7,−74) → 10557@(16,4); 10533@(−18,−40) → 10561@(3,17); 10537@(11,−17) → 10565@(24,24) |
| 11 | 10541@(−5,−36) → 10569@(14,14) |

Para 12..22, ID = `0x2941+codigo+(64 se escuro)`, uma cópia simples.
Offsets por código: 12=(0,0), 13=(16,16), 14=(0,0), 15=(18,11), 16=(18,0),
17=(18,25), 18=(0,25), 19=(0,0), 20=(0,0), 21=(−3,−5), 22=(−1,−1).
Para 28..52, ID = `0x293c+codigo+(64 se escuro)`, offset (0,0).
Ambas as famílias ignoram o auxiliar; não têm chamada separada de sombra nesses
passes. Não concluir que toda cor escura contida em seus CMPs seja transparência.

A máscara CMP determina os pixels opacos; literal zero continua opaco.
Sombras remapeiam o **destino** pela tabela de 256 índices, preservando recorte.
Percentual 60/ciclos vazios são parâmetros declarados deste ensaio, não estado
global de partida comprovado. A API exige a tabela explicitamente.

## Avanço condicionado das árvores

`NextAnimVeget` **0x4772ec..0x4774fa**, retorno compartilhado em
0x475bf8..0x475bfe, usa o relógio A em 0x508f7c. Para códigos 1..11:

1. Se `A & 3 != 0`, mantém fase e cursor sem consumir a tabela.
2. Caso contrário, lê `tabela[ cursor ]` em **0x4e1c18**, e incrementa o
   cursor u8 em **0x4e1d18**, inclusive de 255 para 0.
3. Se `byte_lido & 3 == 0`, fase = `(auxiliar+1)&3`; senão mantém o auxiliar.

A tabela e o cursor são compartilhados. Duas janelas de 3×2 células confirmam
varredura por linhas, consumo somente pelas árvores e preservação das demais
células. A API modela uma árvore por chamada; o consumidor mantém tabela,
cursor e ordem. Não há probabilidade presumida, taxa em segundos ou sequência
aleatória inventada. Renderização aceita auxiliar 0..3; o avanço aceita u8
bruto para reproduzir os casos de borda, sem usar fase inválida como sprite.

`NextAnimVegetFullMap` (0x4774fa..) está extraída, mas recebeu somente leitura
estática. Os outros ramos de NextAnimVeget não foram generalizados para códigos
23..27 ou 53..255. Não se confirma regeneração, coleta, consumo ou dano.

## Validação e dependências

- **63 testes Python** passaram. As dez regressões novas conferem flags,
  capturas, superfícies, avanço, cursor compartilhado, ETA e artefatos.
- **6.442 execuções x86 delimitadas**, 4.372.520 instruções, 5,647 s observados:
  512 predicados, 1.344 capturas, 4.096 avanços fase/relógio/cursor, 256 fases
  brutas, 36 objetos estáticos, duas janelas e **193 buffers completos idênticos**.
  Também estão incluídos o carregador parcial e o banco original.
- Buffers: 88 árvores/fases/iluminação + 72 estáticos/iluminação + 33 recortes.
  Os blitters originais foram executados integralmente nesses 193 casos.
- Navegador: 160 planos e 102 buffers contra Python; iluminação, ocultação,
  passes, controle de fases, sombras, âncora e cálculo de avanço inspecionados.
  Captura: `validacao/demo-objetos-verificada.png`.

Cada execução x86 confere hash do EXE, intervalos permitidos, timeout de 2 s,
teto de 1 milhão de instruções e parada obrigatória. IO/alocação são substituídos
no banco; FileRead no trecho ETA; blitters somente nos ensaios de captura.
Visibilidade, animação e ensaios de pixels não usam stubs. Nenhum jogo, Ghidra
compartilhado ou processo de outra frente foi aberto/manipulado.

`validar_objetos.py` depende de **Unicorn**, assim como as bancadas anteriores;
`extrair_evidencias.py` usa **Capstone** ao extrair assembly. `objetos.py`,
consulta, composição, geração dos atlas, HTML e testes Python não usam x86.
Os relatórios x86 anteriores foram reutilizados sem serem reexecutados nesta v5.

## Lacunas preservadas e próximo caso independente

Permanecem sem contrato: códigos 23..27 e 53..255 (inclusive os 16 registros
66/67), pós-processamento completo do ETA, inicialização/distribuição da tabela
aleatória, taxa de chamadas, ordem global e estado global da sombra. O domínio
de coordenadas segue o original de 16 bits, sem prometer equivalência em overflow.
Os nomes visuais não validam semântica econômica. A referência enviada pelo
usuário continua sendo somente referência de aparência.

Próximo caso independente: rastrear a renderização dos códigos 66/67 da missão 1,
separando inicialização e estados transitórios. Depois, modos adicionais do
Santuário e os indicadores gráficos de seleção/barras. Não há dependência de
respostas dos chats de combate, economia, alvos ou aplicativo macOS.
