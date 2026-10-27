# CalculAttaqueEngin: animação, emissão e subestados

Tradução em [animacao_disparo.py](animacao_disparo.py), referência em
[00451914.asm](evidencias/00451914.asm). O corpo em `0x451914` recebe AX como
índice; despacha pelo byte **+0x8a**, distinto do estado principal em **+0x02**.
O contexto Python é independente de movimento/economia. Não duplica dano nem
simula voos de projéteis; comunica efeitos externos por chamadas explícitas.

## Resultado e endereços

| Endereço | Rotina / trecho | Resultado recuperado |
|---|---|---|
| `0x451914` | `CalculAttaqueEngin` | Despacho 0/1/2/3 e no-op para valores maiores que 3 |
| `0x451957` | Subestado 0 | Alcance/linha, parada da busca, mira, giro e recarga |
| `0x4523dc` | Subestado 1 | Avanço da animação, quadro de disparo, emissão e fim do ciclo |
| `0x452aa7` | Subestado 2 | Espera u8, animação especial e revalidação ao expirar |
| `0x452b7c` | Subestado 3 | Estado principal para 7, referência ffff e limpeza de quadros |
| `0x4479c4` | `AnimAttaqueEngin` | Contadores e dois conjuntos de quadro/período |
| `0x447977` | `AnimAttaqueTermineEngin` | Predicado separado: tipo 2 e quadro +a4 igual a 1 |
| `0x448599` / `0x4484a7` | `RotateEngin` / `RotateTourEngin` | Giro local de corpo/torre, sem avanço espacial |
| `0x4511a5` | `TypeEnginGetSortieProjectile` | Tabelas de saída, orientação de corpo ou torre |
| `0x410fcc` | `AffCorpsEnginDecalage` | Deslocamentos por tipo somados à saída |
| `0x46e44c` | `ProjectileInit` | Fronteira de emissão; original executado na bancada |
| `0x46e208` / `0x46e049` | `ProjectileSet` / `ProjectileLineaire` | Preparação original de um slot livre no ensaio adicional |
| `0x450874` | `InfligeDegat` | Fronteira de dano; sem nova tradução aritmética |

O [manifesto](evidencias/manifesto.json) tem 69 intervalos, SHA-256 original,
constantes e tabelas de despacho. Os offsets de saída e deslocamento do corpo
estão em [dados-disparo.json](evidencias/dados-disparo.json), extraídos do EXE
original por [extrair_evidencias.py](extrair_evidencias.py). Os testes conferem
esses dados executando as rotinas originais, não só relendo o JSON.

## Avanço da animação

`AnimAttaqueEngin` usa a tabela em `0x4479b4`:

- Subestado 0: período **+a7**, quantidade de quadros **+a5**.
- Subestado 1: período **+a8**, quantidade **+a6**.
- Subestados 2/3 ou maiores: não avança por essa rotina.

O contador **+a9** incrementa em oito bits. Só quando fica **igual** ao período
ele zera e o quadro **+a4** vira `(quadro + 1) % quantidade`. A soma do quadro
é promovida para 32 bits antes do módulo: quadro 255 + 1 é 256 nesse cálculo.
Período zero espera o contador dar a volta; quantidade zero provoca divisão
por zero no original e `ZeroDivisionError` no Python, caso o ramo seja alcançado.

Tipos que passam por esses laços: **0, 1, 2, 3, 4, 8, 11, 14, 15, 18..25**.
Os tipos **5, 6, 7, 9, 10, 12, 13, 16 e 17** não avançam aqui. Isso não quer
dizer que não possuam animação no jogo: há outras rotinas e fases.

## Subestados

### 0 — preparar, apontar e esperar carga

Sem deslocamento em +86/+87, exige alcance e linha de tiro. Ao passar,
substitui +7e por +7c, limpa +88 e libera o contexto de busca se seu dono é a
unidade. Calcula a orientação requerida, gira corpo ou torre quando necessário
e retorna nesse passo; o início do ataque só é reavaliado no próximo despacho.

Com mira alinhada, exige `+102 >= RECHARGE - modificador3`; ao carregar, zera
+102, põe **+8a=1** e limpa +a4/+a9, exceto no tipo 16. Tipos 14/16 com +da
zero chamam `SetDeplaceEngin` com destino +7c. A tradução emite esse pedido e
delega seu efeito, sem chamar o módulo de movimento.

Se o primeiro portão falha, atualiza o destino quando necessário e chama
`DeplaceEngin` (`0x44930c`). O caso de distância mínima contra tipo 16 conserva
as duas chamadas de direção/vizinho do original, sem reinterpretá-las como uma
regra ideal de recuo. Tipos que ignoram linha têm um retorno especial nesse
caminho. Alcance, linha, mira e valores de célula continuam sob os contratos
das etapas anteriores.

### 1 — animar e emitir no quadro marcado

Primeiro chama `AnimAttaqueEngin`. **Depois** do avanço, o disparo ocorre se
`+a9 == 0` e `+a4 == +7a`. A referência é resolvida mesmo quando o estado
principal não produz tiro nesse ponto.

- Estado principal **1**: pode pedir som, diminui +da dos tipos 14/16 se não
  zero e escolhe dano direto ou emissão conforme **+78**.
- Estado principal **24**: chama `SortilegeEffet(indice, +f4, +b8)` e depois
  `ResetOrdre`; esses efeitos permanecem callbacks externos.
- Outros estados principais: não executam disparo nesse trecho.

O quadro de disparo é um marcador bruto em **+7a**, não a quantidade total
de quadros. Tipos que não animam nessa rotina podem passar repetidamente pelo
mesmo quadro marcado se outro código não modificar seus campos.

Depois dos efeitos, se +a9 e +a4 estão zerados:

- Se **+8b=0**, põe +8a=0 e zera +102; conserva a exceção de quadro do tipo 16.
- Se **+8b!=0**, decrementa +8b. Tipo 3 põe +a4=5; tipo 11 põe +a4=0.
  O ramo não atribui +8a=2.

### 2 — espera e revalidação

Tipo 16 anima com +a7/+a5; tipo 17 delega `AnimBallonStatic`. Os demais não
animam por esse caminho. Se +8b é 1, tipos diferentes de 16 zeram os campos
de quadro/contador antes do decremento.

+8b é decrementado em oito bits **sem teste prévio de zero**: 0 vira 255 e
continua no subestado 2. Ao chegar a zero, põe +8a=1 e limpa quadro/contador
dos tipos diferentes de 16. Tipos 14/16 com +da=0 pedem `SetDeplaceEngin`;
os demais exigem alcance e mira, voltando a +8a=0 se alguma consulta falhar.

### 3 — encerrar a ordem local

Se estado principal não é 0/4, escreve **7** e libera a busca pertencente à
unidade. Em todos os casos põe +b8=ffff e limpa +a4/+a9. **Não zera +8a**.

As instruções de RNG/animação em `0x452b8b..0x452bf5` não são alcançadas pelo
despacho válido desse ramo: tipos diferentes de 16 saltam o bloco, e o próprio
tipo 16 também sai das comparações posteriores. A bancada verifica 26 tipos
e recusa executar RNG fora dos intervalos declarados.

Não há atribuição a **+8a=2 ou 3** no corpo de `CalculAttaqueEngin`. A origem
dessas fases foi investigada em [INICIALIZACAO_ATAQUE.md](INICIALIZACAO_ATAQUE.md):
não foi identificado um atribuidor direto de 2/3; carregadores preservam
valores externos. A tradução não inventa a transição
`0 -> 1 -> 2 -> 3` como ciclo universal.

## Contrato das emissões

`ContextoAtaque.efeito_externo(nome, argumentos)` deve estar definido quando
um efeito for alcançado. A chamada é registrada em `ctx.chamadas`; ausência
de implementação causa `NotImplementedError`. Um callback sem efeito precisa
ser escolhido explicitamente pelo chamador. O contexto/registro já contém as
escritas anteriores à chamada; o callback pode aplicar os efeitos que lhe cabem.

O pedido de `ProjectileInit` tem a seguinte tupla, conferida com registradores
e os cinco argumentos da pilha originais:

```text
(tipo_projetil, origem_celula, alvo_celula, modo, indice_atacante,
 orientacao, deslocamento_x_s16, deslocamento_y_s16, flag_16_17)
```

Com **+78!=0**, o tiro comum usa tipo +79, origem +08, alvo resolvido e modo 1.
Corpo fornece +91 e torre 12/15 fornece +94 à consulta dos offsets. Tipos
1/21/11 dispensam esses offsets. O tipo 11 recalcula direção com 32 setores.
A flag final é 1 somente em modo 1 contra alvo tipo 16/17.

Casos especiais confirmados:

- Tipo **3**: somente projétil **26**, colocado na célula alvo.
- Tipo **11**: tiro comum **e outro projétil 26** na célula alvo.
- Tipo **25**: somente projétil **33** na célula alvo.
- Com **+78=0**, tipos grandes usam a célula resolvida; pequenos usam a célula
  vizinha na orientação +91. Chama `InfligeDegat(celula, 1, indice, 0, 0)`.
  Tipo **16** ainda emite projétil **8** nessa célula antes do dano.

O significado de +78 continua bruto; esses caminhos estão confirmados, mas
não se renomeia o campo como uma propriedade completa de armas.

Áudio tem os pedidos `EnginGetVolume` e `PlaySnd_PostSound`. Este último recebe
`(80, (tipo<<16)|0x2300, 0, volume, indice)`: o índice representa o destino do
handle em +104. A tradução limpa +f9 no ponto observado; a escrita do handle
fica com o backend de som. Não há chamada Win32/DirectSound pela implementação.

## Validação e limites

Esta etapa acrescenta **19 testes** (cinco de contrato e 14 diferenciais) e
**7.066 execuções x86 delimitadas**. A suíte completa tem **67 testes aprovados,
170.295 execuções, zero falhas/erros/ignorados**, registrados em
[validacao-emulada.json](validacao-emulada.json).

| Conferência nova | Execuções |
|---|---:|
| Animação e predicado de término: tipos, fases e bordas u8 | 3.744 |
| Giro de corpo/torre | 1.200 |
| Saída de projétil e deslocamento por tipo/orientação | 896 |
| Subestado 0: preparação, giro, recarga, linha, mínimo e destino | 234 |
| Subestado 1: quadro marcado, disparo e fim de animação | 312 |
| Corpo a corpo com consultas de dano originais, sem ocupantes | 26 |
| Subestado 2: contador, rotor e revalidação | 200 |
| Subestado 3 e fases inválidas, sem executar RNG | 312 |
| Construções: três fases, adjacência e centro | 72 |
| Magia 255 e ResetOrdre original | 6 |
| Fronteiras nomeadas de balão/som | 2 |
| Emissão com um slot livre e ProjectileSet original | 1 |
| Índice atacante 7 | 1 |
| Ciclo contínuo de 60 atualizações | 60 |

São comparados os **276 bytes do atacante**, os quatro globais de busca e a
sequência/argumentos dos efeitos. O ensaio contínuo conserva memória entre
atualizações; a recarga avança separadamente, sem inferir duração em segundos.

Nos testes de emissão, o x86 executa `ProjectileInit` com pool cheio; um teste
adicional oferece slot livre e executa `ProjectileSet`/`ProjectileLineaire`,
verificando a criação do registro. A tradução Python valida a **solicitação de
emissão**, não todo o conteúdo/voo desse registro. Retornos de pool cheio não
mudam a decisão de controle posterior nessa rotina.

No corpo a corpo, a referência executa `InfligeDegat` e as consultas originais
com células sem ocupantes elegíveis. Isso verifica o pedido e o retorno sem
revalidar a aritmética de dano. Estado principal 24 é exercitado com magia ID
255 (ramo original sem efeito), seguido do reset original; o adaptador de teste
aplica o contrato já conhecido de reset ao mundo Python. Não valida os cinco
efeitos de magia implementados pelo jogo.

Movimento (`SetDeplaceEngin`/`DeplaceEngin`), balão e áudio param **na entrada**
da função externa no x86. Os registros e argumentos anteriores ao efeito são
conferidos nesse checkpoint. Não há troca dessas chamadas por código falso na
CPU, e não se alega execução de seus corpos. No Python o integrador fornece
os callbacks; a bancada não integra o coordenador à física do projeto.

Geometria de construção continua por consultas explícitas, conferidas com
footprints cheios 1x1/3x3. O domínio é tipos 0..25, referências válidas, modos
1/3/5, células u16 e registros de 276 bytes. Modos/footprints indefinidos e
backend de efeitos completo continuam fora da equivalência declarada.

## Uso e continuação

```python
ctx = ContextoAtaque(registros_mutaveis, recargas=recargas_por_tipo,
    descoberto=consulta_de_visibilidade, efeito_externo=backend_de_efeitos)
calcular_ataque(ctx, indice)
```

Fornecer terreno, dimensões, modificadores e callbacks de construção/magia
quando necessários. `BuscaAtaque` é um contexto **local** de quatro campos;
qualquer adaptação ao contexto geral fica para o chat principal. A lista de
chamadas é cumulativa: pode ser limpa entre passos para inspecionar cada tick.

Reprodução: `python3 -B validar.py --emular`, com JIT do Unicorn permitido.
Sem JIT, `python3 -B validar.py` executa 22 contratos e ignora explicitamente
45 diferenciais. Nenhuma etapa inicia o jogo.

A inicialização de +8b/+7a/+79 e o rastreio de fases 2/3 estão em
[INICIALIZACAO_ATAQUE.md](INICIALIZACAO_ATAQUE.md). Próximos passos: reconstruir
o pool/voo/impacto de projéteis como backend separado e validar
magias válidas. Som e `AnimBallonStatic` permanecem efeitos delegados.
