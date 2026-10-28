# Combate: seleção de alvos e condições de ataque

Pesquisa independente, ampliada por etapas. Todos os arquivos novos estão
nesta pasta. Documentos gerais, ferramentas compartilhadas, originais e
configurações são somente lidos. O usuário autorizou o commit desta pesquisa
no branch `main`; cada nova etapa permanece restrita a esta pasta.
Não foi necessário abrir Ghidra.

Foram lidos `documentacao/COMBATE.md`, `INSTANCIAS.md`, `EMULACAO.md`,
`CONTINUIDADE.md`, `ferramentas/combate.py`, testes anteriores, símbolos SBL e
exportações existentes. A aritmética de dano e o avanço da recarga já recuperados
não foram duplicados. O novo predicado de arma carregada complementa o avanço.

## Entrega e reprodução

| Arquivo | Conteúdo |
|---|---|
| [alvos_alcance.py](alvos_alcance.py) | Traduções independentes; registros brutos de 276 bytes |
| [mira_angular.py](mira_angular.py) | EnginViseCible e quantização de AngleCalcul em 8/32 setores |
| [animacao_disparo.py](animacao_disparo.py) | Subestados 0/1/2/3, animação e solicitações de disparo |
| [projeteis.py](projeteis.py) | Pool de 100 registros, inicialização e incrementos lineares |
| [PROJETEIS.md](PROJETEIS.md) | Campos, despacho por tipo, efeitos imediatos e limites |
| [bancada_projeteis.py](bancada_projeteis.py) | Referência x86 com memória e efeitos observados |
| [test_projeteis.py](test_projeteis.py) | 11 testes novos, 12.196 chamadas originais |
| [avanco_projeteis.py](avanco_projeteis.py) | Animação lógica, distribuição de impacto e avanço de 16 tipos lineares |
| [AVANCO_PROJETEIS.md](AVANCO_PROJETEIS.md) | Ordem dos efeitos, chegada, RNG e diferenças nas bordas |
| [bancada_avanco_projeteis.py](bancada_avanco_projeteis.py) | X86 original de avanço/impacto, com observação do RNG |
| [test_avanco_projeteis.py](test_avanco_projeteis.py) | 12 testes adicionais e 21.780 execuções x86 delimitadas |
| [maquina_projeteis.py](maquina_projeteis.py) | Despacho completo de Avance e 30 passagens de Calcul sobre o pool vivo |
| [MAQUINA_PROJETEIS.md](MAQUINA_PROJETEIS.md) | Tipos 30/33, expiração, consultas de magia e ordem de processamento |
| [bancada_maquina_projeteis.py](bancada_maquina_projeteis.py) | X86 original com pausas/retomadas sem alterações de estado |
| [test_maquina_projeteis.py](test_maquina_projeteis.py) | 12 testes adicionais e 9.235 execuções x86 delimitadas |
| [inicializacao_ataque.py](inicializacao_ataque.py) | Características por tipo, inicialização e trechos de pós-carga |
| [INICIALIZACAO_ATAQUE.md](INICIALIZACAO_ATAQUE.md) | Rastreio de +79/+7A/+8A/+8B e limites da conclusão sobre fases 2/3 |
| [rastrear_campos.py](rastrear_campos.py) | Auditoria estática e 2.604 registros dos 38 mapas originais |
| [test_inicializacao_ataque.py](test_inicializacao_ataque.py) | 15 testes adicionais, 12.178 chamadas originais |
| [ANIMACAO_DISPARO.md](ANIMACAO_DISPARO.md) | Máquina recuperada, efeitos delegados e cobertura x86 |
| [bancada_animacao.py](bancada_animacao.py) | Referência de animação/emissão com checkpoints nomeados |
| [test_animacao_disparo.py](test_animacao_disparo.py) | 19 testes adicionais, 7.066 chamadas originais |
| [MIRA_ANGULAR.md](MIRA_ANGULAR.md) | Resolução da célula, cálculo angular e validação detalhada |
| [test_mira_angular.py](test_mira_angular.py) | Contratos e diferenciais da mira completa e trigonometria original |
| [bancada_combate.py](bancada_combate.py) | Adaptador local, somente leitura do módulo `ferramentas/emulador.py` |
| [test_alvos_alcance.py](test_alvos_alcance.py) | Casos de contrato e comparações contra instruções originais |
| [validar.py](validar.py) | Executa só esta pesquisa e grava JSON nesta pasta |
| [extrair_evidencias.py](extrair_evidencias.py) | Extração direta de bytes/assembly do EXE original |
| [evidencias/manifesto.json](evidencias/manifesto.json) | 88 intervalos com limites/hashes, constantes e despachos |
| [evidencias/dados-disparo.json](evidencias/dados-disparo.json) | Tabelas extraídas de saída de projétil e deslocamento por tipo |
| [validacao-local.json](validacao-local.json) | 38 contratos aprovados, 64 diferenciais ignorados explicitamente |
| [validacao-emulada.json](validacao-emulada.json) | 102 testes aprovados, zero falhas/erros/ignorados, 213.506 chamadas x86 delimitadas |
| [INTEGRACAO.md](INTEGRACAO.md) | Contratos e sequência de integração para o chat principal |

Executar nesta pasta:

```sh
python3 -B extrair_evidencias.py
python3 -B rastrear_campos.py
python3 -B validar.py
python3 -B validar.py --emular
```

`-B` impede gerar caches nas ferramentas compartilhadas. A extração reutiliza
Capstone de `source/python`; a emulação reutiliza Unicorn de `.local/python`.
Não se instala ou altera dependência. No sandbox macOS desta sessão, uma chamada
de prova encontrou a restrição de JIT (`SIGILL`, código 132). A validação
diferencial foi executada com permissão de JIT fora dessa restrição.

O hash obrigatório de `source/cd/INSTALHD/RISING.EXE` é:

```text
6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
```

Os nomes franceses são os símbolos existentes de `RISING.SBL`. As novas
evidências contêm bytes do **EXE original**, não a cópia de cabeçalhos PE
normalizados usada pelo Ghidra. Os arquivos que cobrem trechos de funções
maiores não alegam ser funções completas. A tabela em `0x446aa4..0x446b0c`
aparece como dados, não como instruções.

## Rotinas e certeza

| Endereço | Símbolo / trecho | Tradução e evidência |
|---|---|---|
| `0x453d7d` | `TypeEnginPeutAttaquer` | Filtro de par de tipos; 676 combinações x86 |
| `0x453da2` | `EnginTrouveCibleScan` | Varredura por ID, função original inteira |
| `0x453f74` | `EnginTrouveCible` | Grade e preferência dos tipos 2/8, função original inteira |
| `0x446fbf` | `EnginEstEnnemi` | Predicado de donos e aliança direcional |
| `0x46d838` | `PlayerEstAllie` | Consulta preservada; já havia tradução em caminhos |
| `0x44246e` | `EnginOccupeCase` | Ocupação usada pela adjacência, tipos 0..25 |
| `0x4468e4` | `EnginAdjacent` | Área de contato com outra unidade, função original inteira |
| `0x446b0c` | `EnginAdjacentCase` | Área de contato com célula, função original inteira |
| `0x446cb5` | `EnginAPortee` | Modos 1/3/5; geometria de construção e magia via callbacks |
| `0x446eed` | `EnginAPorteeMinimale` | Exclusão de distância² <= 4 contra tipo 16 |
| `0x4517a2` | `EnginLigneDeTir` | Marcha por sinais; célula alvo previamente resolvida no Python |
| `0x451464` | `EnginViseCible` | Consulta completa de corpo/torre, modos 1/3/5 e casos adicionais documentados |
| `0x4796cb` | `AngleCalcul` | Quantização angular no domínio u8 e resoluções 8/32; chamadas x87 originais na bancada |
| `0x45173f` | `EnginEstCharge` | Predicado de recarga; sem duplicar o incremento existente |
| `0x445a36` | `SetAttaqueEngin` | Identidade da ordem e efeitos locais após `ResetOrdre` |
| `0x4546bc..0x4547e0` | Dentro de `EnginNextEtape` | Portões de aquisição automática e classificação da reação |
| `0x456886..0x4568a8` | Mesmo despachante, estados 1/24 | Validade da referência antes de chamar `CalculAttaqueEngin` |
| `0x451957..0x4519bd` | Dentro de `CalculAttaqueEngin` | Portão de preparação, original com alcance/linha sem substituições |
| `0x451d4d..0x451e22` | Mesmo cálculo | Torre, recarga e escritas para iniciar ciclo, corpo já alinhado |
| `0x452b10..0x452b78` | Mesmo cálculo | Revalidação após espera; trechos com consultas como entradas |
| `0x451914` / `0x4479c4` | `CalculAttaqueEngin` / `AnimAttaqueEngin` | Subestados e avanço de quadros traduzidos; [detalhes](ANIMACAO_DISPARO.md) |
| `0x46e44c` | `ProjectileInit` | Pool/inicialização traduzidos e emissão validada com pool cheio e slots livres |
| `0x46eaf8` | `ProjectileAvance` | Todos os tipos; linha, chegada, círculo 30, sorteio 33 e expiração |
| `0x46fc0f` | `ProjectileCalcul` | Animação geral e 30 passagens com atividade/+01 consultados ao vivo |

Esses resultados são **confirmados no código e nos cenários sintéticos
descritos**, não por observação de uma partida. Os limites de cada tradução
estão nas docstrings e na seção de limitações abaixo.

## Escolha do alvo

### Scan: primeiro ID elegível

`EnginTrouveCibleScan` percorre IDs 0..799 em ordem crescente. Exige:

1. Estado `+0x02` diferente de 0 e 4.
2. Campo `+0x72` diferente de zero.
3. Predicado de inimigo do dono do atacante para o candidato.
4. Dono do candidato diferente de 200, inclusive depois do caso especial 4.
5. Filtro do par de tipos.
6. Distância² entre `+0x08` do atacante e do candidato <= `(+0xbb)²`.

Retorna o **primeiro** que passa. A distância é quadrática, sem raiz e sem
wrap em 16 bits na comparação. Não há ordenação por proximidade nesse caminho.
Não consulta vida `+0x9a`, recarga ou alcance de ataque `+0xb0`.

O predicado de inimigo aceita donos diferentes se algum é 4 **antes** de
examinar 200. Portanto, `EnginEstEnnemi(consultante=4, unidade=200)` é verdadeiro;
o scan recusa esse candidato pelo teste separado. Para os demais casos, 200,
igualdade e aliança do consultante para o dono do alvo impedem a hostilidade.

### Grade: menor distância e empate por ordem espacial

`EnginTrouveCible` chama o scan primeiro somente para os tipos 2 (capitão) e
8 (arqueiro). Se ele encontrar alguém, retorna imediatamente; pode preferir
um ID distante a um inimigo mais próximo. Se não encontrar, usa a grade.

O caminho de grade percorre o quadrado de visão em ordem de **y crescente,
depois x crescente**, recortado a 0..255 em cada eixo. Não lê largura/altura
efetiva do mapa. Aceita ocupação com `(palavra & 0xc000) == 0x4000` e extrai
`(palavra & 0x3ff8) >> 3`. Os três bits inferiores não fazem parte do ID.

Recusa dono 200, aliança e pares de tipos proibidos. Conserva o mínimo de
distância² dentro do círculo de visão; empate não substitui o candidato
anterior. Mede a **célula visitada na grade**, não `+0x08` do registro apontado.
Isso importa para footprints com várias células e grades inconsistentes.

Diferenças confirmadas em relação ao scan:

- Não repete estado nem `+0x72`; uma entrada sintética com estado zero pode
  ser selecionada se estiver na grade. A consistência da grade real é externa.
- Consulta `PlayerEstAllie(candidato, atacante)`, sentido inverso ao scan.
  Não repete o atalho de hostilidade do dono 4. Máscaras assimétricas produzem
  escolhas diferentes; não se deve uni-los num filtro genérico de “inimigo”.
- Compara distância e melhor valor em **16 bits** (`0x454199..0x4541a3`).
  Distâncias acima de 65.535 dão wrap nesse trecho. Quatro casos isolados
  executam essas instruções, incluindo visão 255; a seleção inteira foi
  comparada em raios pequenos, não no quadrado inteiro de visão 255.

`TypeEnginPeutAttaquer` não é um predicado unário de capacidade do atacante.
Recebe tipo do atacante em `AL` e do alvo em `DL`: recusa alvo tipo 10 ou 17;
aceita alvo tipo 16 somente para atacante 2 ou 8; aceita os demais pares.

## Alcance, adjacência e linha

`EnginAPortee`: `AX=atacante`, `DL=modo`, `BX=referência`; resultado booleano
em `AL`. O corpo não valida a referência nem repete filtros de seleção.

| Modo | Célula para distância |
|---:|---|
| 1 | `alvo + 0x7c`, célula do passo; não `alvo + 0x08` |
| 3 | Resultado de `BatimentGetCase(referência)` em `0x41aee2` |
| 5 | Palavra `atacante + 0xb8`; a consulta de adjacência ainda recebe `BX` |

A origem é `atacante + 0x08`. O limite normal é
`(byte[+0xb0] + modificador4) & 0xffff`; a distância² deve ser <= limite.
`+0xb0` já contém o quadrado truncado na carga: **não elevar novamente ao quadrado**.
O modificador é somado a esse valor, não ao raio linear.

Antes da comparação normal, há exceções:

- Estado do atacante 24: substitui a base por `SortilegeGetPortee(+0xf4)`;
  continua somando modificador 4 e compara diretamente a distância². Não
  quadrar o valor do acessor. A intenção dos dados de magia ainda não foi analisada.
- Fora do estado 24, atacante tipo 16 exige **igualdade de células** e retorna
  esse resultado; não cai no teste de raio quando diferentes.
- Se `+0x78 == 0` ou atacante tipo 1/4/21, tenta adjacência primeiro.
  Sucesso aceita contato sem exigir o limite quadrático. Falha ainda cai no raio.

As adjacências incluem a área ocupada e uma margem de uma célula. O tamanho é
2x2 para os tipos 3, 11, 12, 13, 14, 15, 16 e 25; 1x1 para os demais 0..25.
`+0x86/+0x87` diferentes de zero impedem a consulta de contato do atacante.
No contato entre unidades, `EnginOccupeCase` examina `+0x08` e `+0x7c` do alvo,
o campo bruto `+0xab` e rejeita estado 14. A célula de contato pode ser
diagonal. As subtrações e bordas peculiares do original foram preservadas e
comparadas, inclusive perto de 0 e 65.535.

`EnginAPorteeMinimale` é verdadeiro salvo quando modo 1, alvo tipo 16 e
distância² <= 4, usando novamente origem `+0x08` e alvo `+0x7c`. O cálculo de
ataque contém a mesma condição expandida em `0x45202d..0x4520dc`; o raio normal
sozinho não representa essa condição de aproximação/recuo.

`EnginLigneDeTir` retorna verdadeiro sem consultar terreno para tipos
4, 8, 12, 22 e 23. Para os demais, sai de `atacante +0x7c`, recalcula o sinal de
dx/dy a cada passo e consulta `TerrainEstMontagne` (`0x47653c`). Bloqueia IDs
de terreno `0x1dd <= id < 0x260` antes do alvo. Uma montanha **na célula alvo**
é aceita. Não é Bresenham; não testa unidades, construções, visão ou alianças.
A versão Python recebe a célula alvo resolvida e não importa o módulo de movimento.

## Iniciar e manter a ordem

Há três decisões distintas:

1. **Adquirir automaticamente:** no trecho estudado de `EnginNextEtape`, tipos
   0/1/2/3/8/11/12/15/16/18..25 podem alcançar a busca; estados 1 e 19 não buscam;
   tipo 16 requer `+0xda != 0`. São portões locais, após etapas anteriores da
   atualização. Ao encontrar alvo, controle de jogador 2 entrega mensagem
   `0x49`; nos demais, somente estado 7 chama `SetAttaqueEngin` com modo 1.
2. **Emitir ordem:** `SetAttaqueEngin` evita trabalho se estado=1 e modo/referência
   já coincidem. Caso contrário chama `ResetOrdre` **antes** das recusas. Recusa
   tipos 5/6/7/9/10/13, modos fora de 1/3/5 e alvo igual a si em modo 1.
   Aceitação põe estado=1, `+0x8a=0`, modo em `+0xb7`, referência em `+0xb8`.
   Não consulta alcance, aliança, vida, recarga ou elegibilidade do alvo aqui.
3. **Começar ciclo de ataque:** no subestado `+0x8a=0` de `CalculAttaqueEngin`,
   `+0x86/+0x87` precisam estar zerados, `EnginAPortee` e `EnginLigneDeTir`
   precisam ser verdadeiros. Depois vem parar a navegação/apontar o corpo.
   Após esse alinhamento, tipos 12/15 ainda esperam `+0x94 == +0xda` (torre).
   Só então exige contador `+0x102 >= RECHARGE - modificador3`, comparação
   assinada em 32 bits; diferença negativa significa carregada até em zero.
   Ao iniciar, zera `+0x102`, põe `+0x8a=1` e limpa `+0xa4/+0xa9`, exceto tipo 16.

Nos estados 1 e 24, o despachante valida uma ordem contra unidade antes de
chamar o cálculo: referência != `ffff`, alvo com estado !=0/4, dono !=200 e
`+0x72 !=0`. Não consulta vida, filtro de tipos ou aliança novamente. Contra
construção exige referência !=ffff, `BatimentEnDestruction` falso e dono !=200.
Os demais modos passam por esse portão. Alvo inválido leva a mensagem `0x4a`
para controle 2; no outro ramo chama movimento para `+0x7e` e limpa `+0xb8`.
Esses efeitos de mensagem/movimento são apenas documentados, sem integração.

Depois de expirar a espera em `+0x8b`, o trecho `0x452b10..0x452b78` mantém o
ciclo dos tipos 14/16 sem repetir alcance/mira ali. Outros tipos precisam de
`EnginAPortee` e `EnginViseCible`; falha põe `+0x8a=0` para preparar de novo.
O teste antigo de fragmentos fornece resultados das consultas como **entradas
de registradores**. A continuação em [MIRA_ANGULAR.md](MIRA_ANGULAR.md) também
testa 676 cenários desse portão executando alcance e mira originais, com toda
a trigonometria, sem substituir consultas.

## Inicialização e origem dos campos

`EnginSetTypeCaract` (0x457350) inicializa +79/+7A somente nos ramos que
os escrevem; `EnginSetType` (0x457B87) zera +8B e preserva +8A. A auditoria
não identificou atribuidor direto de +8A=2/3; carregadores preservam valores
externos. Os 38 mapas do CD têm +8A/+8B zerados nos 2.604 registros.
As traduções e os limites dessa conclusão estão em
[INICIALIZACAO_ATAQUE.md](INICIALIZACAO_ATAQUE.md).

## Testes e limitações

As 213.506 execuções do relatório contam chamadas delimitadas de entrada/trecho,
não cada `CALL` interna. Toda chamada recusa execução fora dos intervalos
declarados e exige alcançar uma parada. No despacho completo, cada pausa e
retomada conta como uma execução, mantendo o estado da CPU. Limites: um
segundo por chamada,
20.000 instruções normalmente, 100.000 na linha, 500.000 no avanço/impacto
de projéteis e 1.000.000 na seleção.

Cobertura: matriz 26x26 de tipos; 125 casos de donos; 160 mundos determinísticos
com 14 candidatos mais cenários de preferência/empate/grade inconsistente;
400 casos de ocupação/adjacência com três chamadas cada; 600 casos de alcance
mais 600 de mínimo; 60 casos de construções sintéticas; 260 linhas; 400 recargas
e 400 trechos de início; 364 efeitos locais de ordem; 104 portões completos de
preparação; 145 validades de referência; portões locais de aquisição automática
e fragmentos de manutenção. A mira acrescenta 145.092 chamadas, detalhadas em
[MIRA_ANGULAR.md](MIRA_ANGULAR.md). As escritas locais de ordem/início são comparadas
com os **276 bytes** do registro, preservando os demais campos.
A máquina acrescenta outras 7.066 execuções, incluindo emissão e um ciclo
contínuo de 60 passos, descritos em [ANIMACAO_DISPARO.md](ANIMACAO_DISPARO.md).
A inicialização e a pós-carga acrescentam 12.178 execuções, descritas em
[INICIALIZACAO_ATAQUE.md](INICIALIZACAO_ATAQUE.md).
O pool e a linha acrescentam 12.196 execuções, comparando os 5.600 bytes e
a cadeia de ataque até a emissão, descritas em [PROJETEIS.md](PROJETEIS.md).
A etapa de [avanço e impacto](AVANCO_PROJETEIS.md) acrescenta 21.780 execuções
e compara a animação lógica,
o wrapper de dano, os 16 ramos lineares de Avance e suas chegadas. Reutiliza
o contrato de dano e consulta Random externamente, sem duplicar essas fórmulas.
A [máquina completa de projéteis](MAQUINA_PROJETEIS.md) acrescenta 9.235
execuções: todos os ramos restantes e as 30 passagens de Calcul, comparando
também o byte global do tipo 30, dois buffers de efeitos e a ordem dos IDs.

Limites deliberados:

- `+0x72`, `+0x78` e `+0xab` mantêm nomes brutos. Seu uso é confirmado;
  “colocado na grade”, “possui projétil” e “camada aérea” são **hipóteses de
  significado**, não nomes de campo já estabelecidos por esta entrega.
- A intenção da assimetria de alianças e do wrap de distância não é conhecida.
  São comportamentos confirmados, sem conclusão de que apareçam normalmente.
- Callbacks de construção/magia são valores já resolvidos. A geometria original
  foi executada em testes contra construções artificiais de footprint cheio
  1x1/3x3, sem traduzir todos os tipos de construção ou feitiços.
- IDs válidos de unidade são 0..799, registros com 276 bytes, tipos de geometria
  0..25 e células u16. IDs de grade 800..2047 e referências inválidas fazem o
  Python falhar explicitamente; o x86 poderia acessar memória fora da tabela.
- Modos fora de 1/3/5 em `EnginAPortee` usam local não inicializado no x86;
  o Python os recusa. Não se inventa uma distância para eles.
- A linha só suporta origem/alvo válidos nas dimensões fornecidas. Não emula
  ciclos, sentinelas ou leituras inválidas causadas por um mundo inconsistente.
- A mira angular está traduzida no domínio u8 e resoluções 8/32; não se afirma
  equivalência bit a bit dos intermediários x87 nem suporte a todos os modos
  indefinidos do original. Construções continuam por callbacks explícitos.
- Os subestados de animação/disparo estão traduzidos, com callbacks obrigatórios
  para efeitos externos e checkpoints antes de movimento, áudio e balão.
  O pool e o incremento linear estão em `projeteis.py`; `avanco_projeteis.py`
  acrescenta 16 ramos lineares e suas chegadas. `maquina_projeteis.py` completa
  o despacho e a expiração. Som, dano em vítimas, iluminação real, morte,
  cadência em segundos e tecnologia não foram traduzidos como sistema completo.
  Não há alegação
  de simulação completa de combate nem confronto com gameplay real.
