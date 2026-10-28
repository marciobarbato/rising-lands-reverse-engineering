# Continuidade v3 — paleta, sombra e estado 14

Base principal: snapshot `1c8ebdd43b0a820652b7cb852ae1fe218d4dea5e`.
Predecessor próprio: `0c76b34a017c185ab24344137a1cb52266b599d2`.
`evidencias/proveniencia-v3.json` registra caminhos, commits e SHA-256 dos dez
arquivos predecessores consultados por `git show`, mais os três manifestos de
fontes, snapshot e dependências reutilizados. Nenhum módulo vivo de outra frente
foi importado. Nenhum arquivo original, entrega v1/v2 ou visualizador foi editado.

## Resultados confirmados

| Vínculo | Código original | Verificação |
|---|---|---|
| PIE → RGB inicial | `LoadPalette 0x4798e9`; deslocamento em `0x47998d` | 768 bytes reais, fixture com todos os valores u8 e primeira cor não preta |
| RGB → preparo DirectDraw | `0x43ee31..0x43ee8d` | 256 triplas iguais, parada anterior à interface COM |
| Estado → handler | `AffEngin 0x41591f..0x415a57` | 5.105 entradas; cinco tipos, todos os estados, todos os valores de +0x8a nos três estados condicionais |
| Estado 14 → retorno sem desenho | `0x415a1c..0x415a23` | Oito Colonos serializados no ETA, memória e superfície inalteradas |
| Paleta/parâmetros → tabela de sombra | `CalculOmbrage 0x45f940`, `Distance3d 0x4795af` | Quatro tabelas completas de 256 bytes |
| Máscara CMP + índice de fundo → novo índice | `PasteOmbreCmp 0x45b796`, `MemOmbreCopy 0x45f7ba` | 256 fundos uniformes, dez recortes/posições e fixture de literal zero |
| Sombra → corpo | `AffEngin`, `AffDeplaceEngin`, `AffCorpsEngin`, blitters | 512 superfícies finais, até retorno, sob precondições registradas |

O símbolo `AffHangar` em `0x415a56` é um `RET` também alcançado pelo epílogo de
`AffEngin`. A delimitação por símbolo usada anteriormente excluía esse byte.
A v3 inclui `[0x41591f,0x415a57)` e conserva seu hash. Isso corrige o limite da
desmontagem e da bancada; não modifica o executável.

## Correção da paleta

As v1/v2 adotavam a aproximação do leitor commitado: `(v&63)*4+3` para valores
não nulos. A rotina original executa `SHL byte,2`, força RGB da entrada 0 a zero
e entrega essas triplas ao preparo de DirectDraw. A API atual e as imagens
regeneradas seguem `(v<<2)&255`; 660 componentes do PLATGAME.PIE diferem da v2.
Os índices dos CMP, máscaras, associações e tempos por chamada permanecem iguais.
DirectDraw/Windows não foram inicializados: o ensaio confere o buffer preparado,
não captura a saída de uma placa de vídeo original.

## Sombra e parâmetros ainda externos

A tabela 256→256 usa percentual u8 explícito e intervalos cíclicos excluídos.
As exceções 5→223, 6→222, 7→221 e 8..15→167 independem da multiplicação RGB.
Fora delas, cada canal é multiplicado pelo percentual, dividido por 100 e
truncado em byte. A cor mais próxima usa distância quadrática, empate pelo
menor índice; 0 começa como candidato mesmo se estiver num intervalo excluído.

`ProgInit` contém `mov edx,60` em `0x474ea0` e chama `CalculOmbrage` em
`0x474eff`, com diversas funções intermediárias. A preservação de EDX por toda
essa cadeia **não foi demonstrada**. A contagem de ciclos é zero na imagem PE,
e há chamadas de `SetCyclage` depois do cálculo, mas também não se executou toda
a inicialização. Portanto “60, ciclos vazios” é uma configuração explícita de
ensaio, não um estado global confirmado. A API não oferece esses valores como
padrões implícitos. O algoritmo foi comparado em 0/60/100 sem exclusões e 255
com exclusões `[0,15]`, `[32,63]`, `[200,210]`.

Para integrar uma partida, é necessário fornecer **os 256 bytes da tabela de
sombra original**, ou paleta no instante de cálculo + percentual + intervalos.
A paleta corrente de exibição pode já ter sofrido ciclagem; não recalcular a
tabela a cada frame sem evidência desse comportamento.

## Estado 14 e contrato ETA

O resultado confirmado é local à chamada de `AffEngin`: o estado 14 retorna
sem consultar CMP nem desenhar corpo ou sombra. Nenhum sprite plausível é
atribuído a esse estado. Oito registros do MONDE01.ETA chegam a esse caminho
quando seus bytes são usados diretamente, sem pós-processamento do carregador.

Cada registro de disco tem 784 bytes; `raw[:140]+raw[652:]` produz 272 bytes,
não os 276 da instância RAM. Os quatro restantes foram zerados na bancada e
não são lidos pelo caminho testado. A diferença é explícita no relatório.
O significado do estado após o carregador exige uma instância final ou uma
rotina completa de pós-processamento validada. Não concluir que esses Colonos
ficam invisíveis na partida.

## Limites da composição e próximos casos independentes

A comparação conjunta usa jogador 0, estado 2, orientação ímpar 1..15,
oito fases, todas as variantes dos cinco tipos. Usa `+0x74=100`, `+0xba=0` e
efeitos em `+0xdc` inativos para não desenhar indicadores auxiliares. Não há
regras de fadiga, experiência, combate ou economia implementadas aqui. As
direções pares e parada foram confirmadas quanto à seleção na v1/v2; a nova
demo aplica a mesma fase/mesmo quadro com a tabela explícita.

`composicao.py` e `graficos.py` não usam Unicorn. `validar_composicao.py` depende
de Unicorn e executa somente intervalos permitidos; `CalculOmbrage` é dividido
em 514 segmentos sem alterar instruções, registradores ou pilha entre segmentos.
Cada segmento tem limite de instruções e 2 s; o loop externo tem 256 cores.
Os únicos stubs são IO/alocação do carregamento. O ensaio de despacho para na
entrada dos handlers; não executa ataques ou suas regras.

Inferência visual: o contorno pontilhado e a posição da máscara sob os pés são
coerentes com os sprites. Isso não foi usado como prova de ID, ancoragem ou ordem.
Continuam como hipóteses: extrapolar sombra/âncora a outros tipos ou deduzir
ordenação global da cena a partir desta chamada individual.

Próxima etapa independente: rastrear o descritor gráfico das construções e
objetos do mapa até o bloco correspondente de ETA; separar ordenação global,
sombra, seleção e indicadores. O consumidor já pode usar o marco de unidades
sem esperar por essas pesquisas. As revisões congeladas exigem novo identificador
para qualquer mudança. O commit desta continuação foi autorizado pelo usuário;
somente arquivos desta frente entram na seleção, sem push.
