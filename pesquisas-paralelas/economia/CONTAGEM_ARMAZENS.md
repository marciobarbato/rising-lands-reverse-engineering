# BatimentInitCave: contagem e capacidade derivada

Pesquisa de 27/10/2026. Tradução de `0x419112` em
`EconomiaConstrucoes.inicializar_armazens`, dentro de [construcoes.py](construcoes.py).
Referência: [00419112.asm](evidencias/00419112.asm), do RISING.EXE brasileiro
SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Toda a implementação, documentação, exportações e validação desta entrega
ficam em `pesquisas-paralelas/economia`; nenhum projeto Ghidra foi usado.

## O que a rotina realmente faz

BatimentInitCave não recebe argumentos semânticos. Percorre os jogadores 0..3
e, para cada um, limpa uma linha de 22 contagens e examina os **1000 registros**
da tabela de construções em `0x49a0c8`, passo `0x114` (276 bytes).

Uma construção entra na contagem quando o byte em `+5` é diferente de zero
e o dono em `+4` é o jogador da linha. O tipo em `+8` escolhe o contador a
incrementar. Não testa vida, estágio de construção, ocupantes, tecnologia,
distância ou se a construção é especificamente um armazém.

| Endereço | Layout | Escrita da rotina |
|---|---|---|
| `0x49a070 + jogador*22 + tipo` | 4 linhas × 22 bytes | Contagem u8 por jogador/tipo |
| `0x4dfb2c + jogador*6` | Primeiro word do registro econômico de capacidade | Cópia zero-estendida da contagem do tipo 3 |
| `0x4dfb4c + jogador` | Quatro bytes | Cópia da contagem do tipo 18 |

Os nomes embutidos na tabela de tipos confirmam **3=CAVE (ARMAZÉM)** e
**18=HELIOPORT**; o tipo 21 é TENTE. Os registros e nomes estão no
[manifesto](evidencias/manifesto.json). A tabela de contagens ocupa 88 bytes e
termina exatamente onde começa a tabela de construções, em `0x49a0c8`.

Pseudocódigo correspondente:

```python
for jogador in range(4):
    zerar_22_contadores(jogador)
    for indice in range(1000):
        construcao = estruturas[indice]
        if construcao.estado_5 != 0 and construcao.dono_4 == jogador:
            contagem[jogador][construcao.tipo_8] += 1  # byte, com wrap
    contagem_tipo18[jogador] = contagem[jogador][18]
    numero_armazens[jogador] = contagem[jogador][3]  # byte → u16
```

A rotina restaura EBX, ECX, EDX, ESI e EDI e preserva EBP. Seu salto final
para `0x41db1e` executa um epílogo compartilhado, exportado em
[0041db1e.asm](evidencias/0041db1e.asm). A bancada executa esse epílogo original.

## Atualização da capacidade e limites numéricos

**Confirmado por instruções e comparação diferencial:**

- A rotina atualiza o **número de armazéns**, não a capacidade por armazém.
  Preserva o word em `0x4dfb2e + jogador*6`, o indicador em `0x4dfb30 + jogador*6`
  e o byte seguinte. A capacidade unitária 100 vem de BatimentAlloc, em
  `0x419040`, não de BatimentInitCave.
- Não chama consultas de saldo, crédito, débito ou recálculo do indicador.
  Uma capacidade unitária zero não provoca divisão por zero nesta rotina.
- Contagens anteriores são substituídas, e não acumuladas. Mudanças de dono,
  inativação e reativação aparecem na recontagem seguinte.
- Estados 1, 2, 4, 7 e 255 contam da mesma forma: basta `+5 != 0`. O nome
  “ativa” neste documento descreve esse teste, não uma classificação completa
  dos estados de gameplay.
- Donos fora de 0..3 são ignorados pelas quatro passagens.
- O incremento é **u8**: 255 armazéns dão 255, 256 dão zero, 257 dão um,
  511 dão 255, 512 dão zero e 1000 dão 232. A cópia final para u16 não recupera
  os bits perdidos. O contador de heliportos sofre o mesmo wrap.

Isso afeta a capacidade usada por BatimentAjouteMatiere:

```python
capacidade_efetiva_u16 = (contagem_u8 * capacidade_unitaria_u16) & 65535
```

Com 256 armazéns, a recontagem fornece zero: as rotinas econômicas subsequentes
podem seguir o ramo “sem armazéns” e preservar o indicador antigo. Os testes
integram contagem, recálculo e débito para conferir esse resultado.

Não substituir a contagem por um inteiro Python sem limite, nem redefinir
automaticamente a capacidade para 100 ou recalcular o indicador dentro desta
função. Essas alterações deixariam de reproduzir a rotina estudada.

`InitBatimentPlayer` usa um `INC word` para o ganho incremental de armazém em
`0x41bf61`, enquanto a recontagem usa bytes. Essa diferença é confirmada
estaticamente; o fluxo completo de construção/troca de proprietário não foi
traduzido aqui. Também não se afirma que as missões normalmente alcancem a
quantidade que causa wrap.

## Chamadores e dados reais

As chamadas diretas encontradas no EXE são:

| Chamada | Contexto pelo símbolo original |
|---|---|
| `0x46bb1a` | GameLoad |
| `0x46c5b4` | MissionLoad |
| `0x46c97d` | MissionLoadName |

Em MissionLoad, o bloco de estruturas copia os prefixos indexados do ETA para
registros de 276 bytes; depois são lidos outros blocos, e BatimentInitCave é
chamado em `0x46c5b4`. A presente validação **não executa MissionLoad inteiro**.

Foram construídas 38 fixtures usando os prefixos reais de 204 bytes das
estruturas dos mapas ETA, copiados para seus índices numa tabela de 1000 slots
inicialmente zerada. Os campos relevantes `+4`, `+5`, `+8` estão nesse prefixo.
O teste compara a tradução com o x86 sobre essa memória e confere as contagens
diretamente nos registros do arquivo. Outros pós-processamentos da carga e a
partida completa não entram nessa alegação.

## Validação

Novos testes: [testes/test_init_cave.py](testes/test_init_cave.py).
Bancada: [bancada_init_cave.py](bancada_init_cave.py), sem substituir chamadas,
com intervalos explícitos, até 1.000.000 de instruções e timeout de um segundo.

| Grupo diferencial novo | Execuções x86 |
|---|---:|
| Tabelas completas com estados, donos e tipos variados | 32 |
| Bordas u8 de contagem de armazéns e heliportos | 16 |
| Prefixos de estruturas dos 38 mapas ETA | 38 |
| Contagem, recálculo e débito integrados | 24 |
| Troca de dono, inativação e reativação | 4 |
| **Total novo** | **114** |

Os sete testes locais e cinco diferenciais acrescentam 12 testes à suíte.
**65 testes passaram**, com **11.994 execuções x86** ao todo: 11.967 paradas
declaradas, 24 exceções e três limites esperados das etapas anteriores.
Todas as 114 execuções novas alcançam o retorno normal. São comparados:
as 88 contagens, os quatro bytes derivados do tipo 18, capacidades, os 276.000
bytes de estruturas, saldos, grades de sacolas, sementes e guardas adjacentes.
As entradas com registradores variados também conferem os registradores
preservados e a ausência de chamadas econômicas durante a recontagem.

## API, proteção e integração

```python
m = EconomiaConstrucoes(
    economia=e,
    capacidades=Capacidades(bloco_capacidades_24_bytes),
    estruturas=bloco_1000_registros_de_276_bytes,
    contagens_por_tipo=bloco_88_bytes_desde_49a070,
    contagens_tipo18=bloco_4_bytes_desde_4dfb4c,
)
m.inicializar_armazens()
```

Os dois buffers novos são copiados no construtor e ficam disponíveis nas
propriedades de mesmo nome para sincronização. A contagem usa o buffer
`m.estruturas`, também copiado na construção do objeto. As outras operações
continuam aceitando tabelas menores, mas esta exige os 1000 registros lidos
pelo original. `recalcular_recursos(jogador)` continua sendo operação separada.

A API rejeita construções ativas de jogadores 0..3 com tipo fora de 0..21,
antes de alterar contagens ou capacidades. O original não verifica o tipo:
um índice fora da linha pode incrementar outra linha ou a memória vizinha,
inclusive estruturas. A equivalência é delimitada aos tipos válidos dos
registros que são contados. Tipos inválidos de construções inativas ou donos
ignorados não são rejeitados, pois não indexam a tabela nessa rotina.

Não se simulam criação/movimento de unidades, efeitos de tecnologia ou carga
Windows. A recontagem está confirmada; o ciclo integral de atualização da
capacidade por todos os chamadores continua parcial. Não foi iniciada uma
partida. As orientações gerais estão em [INTEGRACAO.md](INTEGRACAO.md).

O usuário autorizou um commit desta entrega no `main`. Como a pesquisa
econômica anterior ainda não estava versionada, o commit inclui a base
necessária e esta fase, limitado aos arquivos desta pasta. Não inclui outras
pesquisas paralelas, configurações ou documentos compartilhados.
