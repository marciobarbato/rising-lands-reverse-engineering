# Extração de minas, coleta e regeneração de campos

Etapa de 27/10/2026. Tradução em [extracao.py](extracao.py), referência em
[bancada_extracao.py](bancada_extracao.py) e testes em
[testes/test_extracao.py](testes/test_extracao.py). Foram traduzidas 15 rotinas,
com 24 testes novos e 5.641 execuções x86. A suíte acumulada passou 108 testes
e 19.499 execuções, sem testes ignorados na execução emulada.

O EXE e o SBL foram usados somente para leitura, com os hashes verificados
pelo exportador e pela bancada existentes. Não houve uso de Ghidra, execução
de uma partida ou implementação de movimento, caminhos ou contornos.

## Rotinas e convenções confirmadas

| Endereço | Nome original | Método de RecursosTerreno | Entrada e saída semânticas |
|---|---|---|---|
| `0x47544c` | MineGetIndice | `indice_mina` | AX=célula; AX=índice ou 0xffff |
| `0x4754a7` | MineSetWork | `iniciar_trabalho_mina` | AX=célula |
| `0x4754de` | MineEndWork | `encerrar_trabalho_mina` | AX=célula |
| `0x475515` | MineDetruire | `destruir_mina` | AX=índice da mina |
| `0x475541` | MineGetCapacite | `capacidade_mina` | AX=índice; AX=reserva |
| `0x47554f` | MineRetire | `retirar_mina` | AX=índice, DX=quantidade; AX=retirada efetiva |
| `0x4755a7` | MineRecolte | `recolher_mina` | AX=célula; AX=zero ou um |
| `0x476662` | TerrainRetireMatiere | `retirar_sacola` | AX=célula; AL=recurso, com zero ambíguo |
| `0x4781e8` | TerrainRecolte | `recolher_campo` | AX=célula; sem quantidade de saída |
| `0x478247` | TerrainEstChampi | `e_campo` | AX=célula; AL=booleano |
| `0x47826c` | PatateAugmentable | `pode_crescer` | AX=célula; AL=booleano |
| `0x4782b4` | NouvellePatate | `nova_planta` | AX=célula; AL=booleano |
| `0x478319` | ScanNouvellePatate | `propagar_planta` | AX=célula; AL residual não modelado |
| `0x475328` | SetUpdateChamp | `agendar_campos` | Lê tempo/período globais |
| `0x478806` | UpdateChamp | `atualizar_campos` | Lê e atualiza linha/flag globais |

Os ASM correspondentes estão em `evidencias/`. O recorte de UpdateChamp acaba
no RET, antes dos bytes em `0x478a01`. LoadMine (`0x47534a`) e LoadMissionMine
(`0x47539c`) também foram exportados para comprovar o layout, mas **seu I/O
não foi traduzido ou emulado**.

## Estado compartilhado

| Endereço original | Representação | Uso confirmado |
|---|---|---|
| `0x509954` | `minas`, 20 registros de quatro bytes | Origem u16 em +0, reserva u16 em +2 |
| Ponteiro `0x507d74` | `terreno.tipos`, 65.536 bytes | Objetos, sacolas e estágios de campos |
| Ponteiro `0x507dac` | `terreno.quantidades`, 65.536 bytes | Quantidades de sacolas; também contadores nas minas |
| Ponteiro `0x507d70` | `mosaicos`, 65.536 u16 little-endian | IDs de terreno consultados na propagação e alterados no esgotamento |
| Ponteiro `0x507da8` | `atributos`, 65.536 bytes | Somente consulta do bit 0 para impedir nascimento |
| `0x497164` | `terreno.semente`, u32 | Random compartilhado com sacolas |
| `0x4973e8` | `linha`, u16 | Linha atual da passagem de atualização |
| `0x4973ea` | `periodo`, u16 | Divisor usado para agendar a passagem |
| `0x508f7c` | `tempo`, u32 | Dividendo do agendamento |
| `0x509952` | `atualizar`, u8 | Flag de início/continuação |

A tradução recebe o mesmo `TerrenoSacolas` usado por `EconomiaConstrucoes`.
Os demais buffers são copiados pelo construtor. Os atributos não são alterados
por nenhuma destas rotinas; seu significado global e sua manutenção continuam
com os subsistemas responsáveis. A consulta local ao bit 0 não implementa
colisão ou busca de caminhos. O RNG de `0x498db4` permanece intacto.

## Minas

MineGetIndice percorre os vinte registros na ordem. Origem zero desativa a
entrada para essa busca. Compara a célula com origem, origem+1, origem+256 e
origem+257; as três somas são de 32 bits, **sem truncar o resultado em u16**.
Não verifica a reserva nem os mosaicos, e a primeira correspondência vence.
Há cruzamento linear entre linhas: origem `0x10ff` inclui `0x1100`. Origem
`0xffff` não inclui célula zero por wrap.

MineSetWork e MineEndWork localizam a mina e incrementam/decrementam os bytes
de quantidade na origem e na origem+1. Os dois bytes são independentes, com
wrap 255→0 ou 0→255. Não há saturação ou teste de capacidade; mina ausente
é uma operação sem efeito. A interpretação como contagem de trabalhadores
é sustentada pelos nomes e pelos chamadores, mas a rotina em si apenas
manipula esses dois bytes.

MineRetire retorna `min(quantidade_u16, reserva_u16)`. Se o pedido for menor
que a reserva, apenas a reduz. Em igualdade ou excesso, zera a reserva e grava
`0x1db` e `0x1dc` nos dois mosaicos da origem. Isso também ocorre para pedido
zero e reserva zero. A origem do registro permanece, assim como os objetos
e os contadores. MineRecolte realiza o mesmo efeito para uma unidade após
localizar a mina; uma mina ausente ou vazia retorna zero.

MineDetruire, apesar do nome, **só grava os dois mosaicos**. Não zera reserva
nem origem. A tradução mantém essa diferença; chamar esse método não impede
uma retirada posterior.

Nenhuma dessas rotinas credita o jogador. No chamador CalculWorkEngin,
`0x44c14b` chama MineRecolte; se AX for não zero, o trecho `0x44c155..0x44c172`
acrescenta um item na Bag da unidade, com palavra de recurso 2. A coleta de
campo em `0x44d079` é seguida por palavra de recurso 1 em `0x44d08f`.
Esses trechos foram conferidos estaticamente no EXE; o chamador completo
e o transporte até o depósito continuam fora desta tradução.

## Sacolas e coleta de campos

TerrainRetireMatiere retira uma unidade quando o byte de quantidade é positivo
e devolve `(tipo - 0x42) & 255`. Não valida se o tipo está entre 0x42 e 0x44.
Quando a quantidade final é zero, limpa o tipo, inclusive se a célula já
estava sem quantidade. Retorno zero significa tanto peças quanto ausência
de quantidade: o integrador deve consultar o estado anterior para distinguir.

TerrainEstChampi reconhece os tipos 0x1d..0x34, inclusive. PatateAugmentable
aceita 0x1d..0x27 e 0x29..0x33. TerrainRecolte limpa tipos 0x1d..0x32;
0x33 vira 0x29 e 0x34 vira 0x2a. Tipos externos ficam intactos. Essa rotina
não muda o byte de quantidade nem retorna quanto foi colhido.

## Nascimento, propagação e tempo

NouvellePatate exige objeto zero e bit 0 dos atributos desligado. Só então
avança Random uma vez e escreve 0x1d se o valor for par, ou 0x29 se ímpar.
Não consulta o mosaico e preserva o byte de quantidade. Uma recusa preserva
a semente. A API reutiliza a tradução já validada do Random original.

ScanNouvellePatate tenta esquerda, direita, cima e baixo, parando na primeira
criação. O mosaico deve estar em 0x84..0x86 ou 0x9d..0xdc; continuam valendo
célula vazia e bit 0 livre. Os vizinhos são índices lineares truncados em u16:
na célula zero, esquerda é 65535. Não introduzir limites por eixo ou testes
de rota. As verificações redundantes do x86 foram condensadas porque o teste
final de objeto zero já rejeita campos e sacolas. Os AL residuais não formam
um booleano consistente; `propagar_planta` retorna `None`.

SetUpdateChamp calcula `tempo_u32 % periodo_u16` e escreve flag=1 apenas
quando o resto é zero. Nos demais ticks, mantém a flag anterior. Período zero
causa exceção de divisão em `0x47533a`, sem modificar a flag. Não há evidência
nesta etapa que permita converter essas unidades de tempo em segundos.

UpdateChamp retorna sem efeito se flag=0 e linha<=1. Caso contrário, percorre
as colunas 1..254 da linha atual, na ordem e com alterações imediatas:

1. Tipo 0x1c: sorteia; resto zero por cinco tenta propagação.
2. Se a célula agora está em 0x1d..0x34, sorteia; só resto zero por dez continua.
3. Tipos 0x28 e 0x34: limpa a célula e tenta propagação.
4. Tipos 0x24..0x27 e 0x30..0x33: sorteia novamente; resto zero por cinco
   incrementa o tipo, e os outros restos tentam propagação.
5. Demais estágios reconhecidos: incrementa o tipo.

Uma planta criada à direita pode ser processada na mesma chamada. Preservar
a ordem das células e dos sorteios é necessário para reproduzir o estado.
As colunas extremas não são visitadas diretamente pelo laço, mas podem receber
plantas por propagação. Ao final, incrementa a linha; depois de 255, restaura
linha=1 e flag=0. Linha>1 mantém a passagem mesmo com flag=0. Uma flag ativa
também permite processar linha zero; não foi inventada uma correção para isso.

CalculGame chama SetUpdateChamp em `0x42d409` e UpdateChamp em `0x42d40e`.
Isso é uma ligação estática confirmada, não emulação do ciclo completo.

## Validação e limites

| Grupo novo | Execuções x86 |
|---|---:|
| Busca e capacidade em 128 tabelas, incluindo duplicatas e bordas | 896 |
| Retirada, coleta unitária e alteração dos mosaicos | 384 |
| Início/fim do trabalho, incluindo mina ausente | 256 |
| Sacolas: 256 tipos × quantidades 0, 1 e 255 | 768 |
| Campos: duas consultas e coleta para os 256 tipos | 768 |
| Nascimento: flags, ocupação e sementes | 256 |
| Propagação: prioridades, mosaicos e bordas | 256 |
| Agendamento: 128 ticks e oito divisões por zero | 136 |
| Atualização: 64 linhas e pilhas preenchidas | 64 |
| Uma passagem completa em memória persistente | 255 |
| 520 registros de minas e uma linha de cada um dos 38 mapas | 1.598 |
| Encadeamento sintético extração→sacola→coleta→crédito | 4 |
| **Total desta etapa** | **5.641** |

São 5.633 retornos normais e oito exceções esperadas. Não há parada em
dependência nesta etapa. A bancada compara minas, mosaicos, atributos, tipos,
quantidades, semente, agenda, recursos e construções, além das guardas e dos
registradores preservados. Usa bytes originais sem substituir chamadas,
intervalos permitidos, timeout de um segundo e limite de um milhão de
instruções por chamada nova.

Os testes de período zero usam uma CPU nova para cada exceção: a reutilização
do estado de exceção no Unicorn interrompeu uma primeira tentativa. A bancada
foi corrigida e a suíte completa passou; nenhum byte do EXE foi modificado.

O corpus usa as quatro camadas ETA e a tabela de quatro bytes lida por LoadMine.
O leitor existente fornece o offset do bloco; a fixture copia seus registros
para uma tabela inicialmente zerada. Também aplica a conversão documentada
de objetos 0x36 em sacolas 0x42 com quantidade um. **Não executa MissionLoad**,
não comprova todo o carregamento e usa um instante/semente sintéticos para
regeneração. Os 520 registros são a soma dos 38 arquivos, não minas de uma
única partida. Os slots não usados da fixture têm reserva zero; o LoadMine
original limpa somente a origem desses slots, preservando suas reservas antigas.

As guardas adicionais da API rejeitam índice de mina fora de 0..19, após
truncar AX; origem 0xffff quando houver escrita no par; e linha ativa acima
de 255. O x86 não possui essas proteções e pode acessar além das tabelas.
Na origem 0xffff, a rejeição ocorre antes das alterações, ao contrário dos
efeitos parciais que o original poderia produzir. Não se afirma equivalência
fora desse domínio. As outras bordas, wraps e estados inconsistentes descritos
acima foram preservados.

Continuam pendentes: chamadores completos das unidades, duração do trabalho,
transporte, fome/consumo, mercado, tecnologias e filas. Os nomes visuais das
duas famílias de plantas e o significado de todos os tipos não foram
estabelecidos por estes testes. A validação de rotinas isoladas não encerra
a engenharia reversa da economia integrada.

## Integração

Consulte [INTEGRACAO.md](INTEGRACAO.md). Os métodos não incluem automaticamente
itens em Bags nem alteram carteiras. O encadeamento sintético apenas confirma
compatibilidade dos estados entre as primitivas; não representa um trabalhador
percorrendo o mapa. O chat principal continua responsável por ligar os
chamadores e promover os arquivos para a implementação compartilhada.
