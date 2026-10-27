# InitBatimentPlayer e InitBatimentNeutre

Tradução de `0x41be88` e `0x41c017`, do RISING.EXE brasileiro SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Código em [proprietarios.py](proprietarios.py), referência em
[bancada_proprietarios.py](bancada_proprietarios.py) e testes em
[testes/test_proprietarios.py](testes/test_proprietarios.py).
Toda a entrega fica em `pesquisas-paralelas/economia`, incluindo o commit no
`main` autorizado pelo usuário. Arquivos de outros chats não integram o commit.

## Contrato das rotinas

Ambas recebem **AX=índice de construção, DL=jogador**. O índice é u16 e o
jogador é u8. Elas aplicam efeitos de ganho/neutralização, mas **não escrevem o
dono em +4 nem o estado em +5**. Também não atualizam a matriz de 88 contagens
por tipo reconstruída por BatimentInitCave.

As chamadas diretas encontradas são `0x41fa9a`, em BatimentLogeEngin, e
`0x41e0d7`, em BatimentRetireColon. No primeiro caminho, há escrita do dono
em `0x41fa77` antes de InitBatimentPlayer. Isso sustenta a separação entre
atribuir propriedade e executar seus efeitos. Os chamadores completos não
foram traduzidos nesta fase.

| Tipo | InitBatimentPlayer | InitBatimentNeutre |
|---|---|---|
| 3, CAVE | Incrementa número de armazéns u16 e recalcula indicador se não virar zero | Decrementa u16; estado +5=3 evita retirada/depósito; outros estados chamam TerrainDeposeMatiere duas vezes |
| 6, BIBLIOTHEQUE | Incrementa contador u8 em `0x4dfb48+j` | Decrementa u8; se o resultado for zero, reseta cinco flags e a lista de ordens de magia |
| 18, HELIOPORT | Prepara chegada de balão, incrementa contador u8 do tipo 18 e pode inserir pendência do tipo de unidade 16 | Prepara saída de balão, decrementa contador u8 do tipo 18 e pode limpar essa pendência |
| 20, MONASTEREFUSION | Sem efeito | Zera bytes +0x7a/+0x104 e escreve dword 1 em +0x108 |
| Demais tipos | Sem efeito | Sem efeito |

As bifurcações foram exercitadas para **todos os 256 valores do byte de tipo**.
Os nomes constam dos registros originais preservados no
[manifesto](evidencias/manifesto.json), não de semelhança visual das construções.

## Armazéns: contagem incremental e indicador

O ganho usa `INC word` em `0x4dfb2c+j*6`; a neutralização usa `DEC word`.
Não há saturação: 65.535+1 dá zero e 0−1 dá 65.535. Isso difere da recontagem
global, cujos contadores u8 fazem 256 virar zero.

Após o incremento, a rotina só recalcula o indicador se a contagem resultante
for positiva. Usa a soma u16 dos estoques de comida e pedra, divisão por número
de armazéns, multiplicação por sete, divisão pela capacidade unitária e escrita
do byte final. A fórmula coincide com BatimentCalculResource já traduzido.
Uma capacidade unitária zero causa exceção em `0x41bfbe`, depois do incremento;
o incremento não é revertido e o indicador anterior fica preservado.

Na neutralização, **não há recálculo direto incondicional**. Se o byte +5 é 3,
a rotina retorna depois do decremento. Em outros estados, as alterações de
saldo e o recálculo dependem do conteúdo dos estoques e de TerrainDeposeMatiere.

## Matéria retirada na neutralização

InitBatimentNeutre chama `TerrainDeposeMatiere` (`0x41bb8a`) com modo 0 e depois
modo 1, célula `(posição+0x202)&65535` e flag de pilha zero. A tradução cobre
esse domínio específico do helper, sem alegar seu caminho de recuperação de
custos quando a flag é diferente de zero.

**O jogador usado pelos dois depósitos vem do byte global `0x4dfab8`.** Ele pode
ser diferente do jogador passado em DL para diminuir o número de armazéns.
A API mantém esse dado como `jogador_deposito`, sem atribuir um significado
mais amplo à variável global.

Seja `S` o estoque u16 do recurso, `N` o número de armazéns desse jogador após
os efeitos já aplicados, e `Q` a quantidade calculada:

```python
if S > 0:
    Q = (S // N) >> 1 if N > 0 else S
    EnleveMatiere(recurso, Q, jogador_global)
    if N > 0:
        recalcular_indicador(jogador_global)
else:
    Q = 0

deposito_comida = Q            # modo 0
deposito_pedra = Q >> 1        # modo 1: redução adicional
```

O débito continua reduzindo total e RMI separadamente. Por isso, retirar Q
não implica necessariamente reduzir o estoque calculado pela mesma quantidade.
Se o recálculo divide por zero, a falha ocorre depois do débito: em modo comida,
`IDIV` está em `0x41bccf`; o modo pedra tem seu `IDIV` em `0x41be27`.
Os testes de exceção da neutralização exercitam o primeiro desses caminhos.

Os pedidos de comida e pedra usam **a mesma célula**. CreerSac recusa conteúdo
de tipo incompatível, de modo que a comida colocada primeiro pode impedir
que a pedra debitada apareça no terreno. Não há restituição nesse caminho.
O modelo preserva a tentativa e a possível recusa, sem redistribuir a pedra.

## Bibliotecas, permissões e listas

O contador do tipo 6 é um byte: ganho 255→0 não limpa permissões; perda 0→255
também não. A limpeza só ocorre quando o decremento resulta em zero.

Nesse ramo, SortilegeResetRealisable (`0x4749ca`) zera cinco bytes em
`0x508f30+j*5`. SortilegeSetTechnologie (`0x474a38`) obtém a lista de ordens do
tipo 4 e a reinicializa com capacidade 5. Como as cinco flags acabaram de ser
zeradas, seu laço não reinsere ordens. Essa é a composição traduzida aqui;
o helper de tecnologia isolado com flags não zeradas não foi implementado.

BagInit (`0x447148`) zera cabeçalho, 30 IDs, 30 tags e o word +0x66. Preserva
os seis bytes +0x60..+0x65. Os testes usam dados não nulos nesses bytes para
conferir a preservação, em vez de representar a lista por uma coleção nova.

## Heliportos, pendências e dependências de movimento

O bloco de controle de balão começa em `0x4e1a14`, passo oito por jogador.
Quando seu contador u16 já é positivo, BallonPrepareArrivee (`0x441baa`) apenas
o incrementa. Quando é zero, a rotina pode criar/reposicionar unidade e emitir
ordens de movimento. Esse caminho exige o callback `preparar_chegada(jogador)`;
na ausência dele, Python levanta `DependenciaBalaoPendente` **antes da chamada**.

BallonPrepareSortie (`0x441d4f`) retorna com contador zero; se ele é maior que
um, apenas decrementa. O caso um→zero passa a manipular unidade e movimento:
exige `preparar_saida(jogador)`, também antes de aplicar efeitos da dependência.
O callback deve implementar a rotina inteira correspondente, não apenas ajustar
o contador. Não há simulação de sucesso ou callback fictício na referência x86.

Depois dessa etapa, as contagens do tipo 18 em `0x4dfb4c+j` são alteradas em u8.
A decisão sobre a pendência compara **o contador do dono atual em construção+4**
com TypeEnginGetNb desse dono, tipo 16, na tabela `0x4e1a3c`, passo 52.
Já o contador alterado e a lista de pendência usam o jogador do argumento.
As duas identidades foram variadas independentemente nos testes.

No ganho, se contador do dono > número de unidades, verifica a lista em
`0x4dd6e8 + jogador*2288 + 0x750`. BagContient é chamado com modo 6 e valor 16:
uma correspondência existente preserva a lista; caso contrário, BagInit define
capacidade 1 e BagPrend insere tag 6/valor 16.

Na neutralização, contador do dono <= número de unidades provoca BagInit com
capacidade 1 e, em seguida, BagRetire modo 6/valor 16. A lista acabou de ser
esvaziada, portanto essa remoção não encontra item. A tradução não precisa
executar uma remoção genérica para reproduzir esse estado; a referência executa
ambas as chamadas originais.

## Validação e contagens

Foram acrescentados **11 testes locais e oito diferenciais**. A bancada mantém
as chamadas originais de saldos, Bags, contador de unidades, permissões e
depósito de sacolas. Ganchos apenas registram chamadas. Não executa Windows.

| Grupo novo | Execuções x86 |
|---|---:|
| Todos os 256 tipos, ganho e neutralização | 512 |
| Ganho de armazém: bordas u16, dados e pilha suja | 512 |
| Perda de armazém: estados, estoques e jogador global diferente | 256 |
| Bibliotecas, flags e listas | 256 |
| Heliportos com dependências que não movem unidades | 256 |
| Paradas nas dependências de chegada/saída | 32 |
| Divisão por zero, após incremento ou débito | 16 exceções esperadas |
| Sequência neutralização, atribuição externa, ganho e recontagem | 24 |
| **Total novo** | **1.864** |

São 1.816 retornos normais novos, 32 paradas de dependência e 16 exceções.
As paradas ocorrem nas entradas `0x441baa`/`0x441d4f` antes de seus efeitos;
o modelo e a referência continuam com a mesma memória nesse ponto. Não validam
os caminhos de criação/movimento dessas funções.

A suíte completa passou com **84 testes e 13.858 execuções x86**: 13.815 paradas
declaradas, 40 exceções de divisão por zero e três limites esperados. As paradas
declaradas incluem as 32 novas de balão e as 64 anteriores de retirada de colono.
Cada entrada permite até 1.000.000 de instruções, com timeout de um segundo.

Comparam-se estruturas, saldos, capacidades, contagens, grades de sacolas,
sementes, os 9.152 bytes de pendências, os 10.816 de ordens, flags, contadores
de biblioteca/balão e os 208 bytes dos números de unidades. Há guardas ao redor
dos buffers. A transferência sintética muda o dono explicitamente entre as
chamadas, sem simular os chamadores completos.

## Integração e limites

```python
p = PropriedadeConstrucoes(mundo, bibliotecas=bloco_4dfb48,
                          baloes=bloco_4e1a14, numeros_unidades=bloco_4e1a3c,
                          pendencias=bloco_4dd6e8, ordens=ordens_por_jogador,
                          sortilegios=bloco_508f30, jogador_deposito=byte_4dfab8)
p.inicializar_neutro(indice, antigo_jogador)
# Atribuição do novo dono pertence ao chamador; respeitar sua ordem original.
p.inicializar_jogador(indice, novo_jogador)
```

`mundo` é compartilhado; os demais buffers são copiados e podem ser exportados
pelas propriedades de mesmo nome. `ordens` concatena quatro blocos de 26 Bags
de 104 bytes; a referência fornece a tabela de ponteiros de `0x4e19b8`.
Não conectar essas funções automaticamente a qualquer escrita de dono sem
conferir o fluxo original, nem atualizar a matriz de contagens por tipo nelas.

O domínio protegido é jogador/dono consultado 0..3, índice presente no buffer
e até 30 slots na consulta de Bag. O original não possui todas essas proteções
e pode acessar memória fora dessas tabelas. Partida integrada, criação/movimento
dos balões, chamadores de colonização e outros modos/flags dos helpers continuam
fora da validação. Todas as rotinas e trechos exportados são evidência estática;
nem todo helper exportado tem tradução geral completa.
