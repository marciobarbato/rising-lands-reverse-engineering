# BatimentEnleveMatiere e BatimentCalculResource

Continuação de 27/10/2026, restrita a `pesquisas-paralelas/economia`, sem
operações Git e sem alterações em arquivos originais ou compartilhados.
As duas rotinas foram traduzidas e comparadas com instruções do EXE original
SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Não foi necessário usar Ghidra nem investigar movimento ou busca de caminhos.

## Rotinas e API

| Entrada x86 | Nome original | Método em EconomiaConstrucoes | Argumentos originais |
|---|---|---|---|
| `0x4235bd` | BatimentEnleveMatiere | `retirar(jogador, recurso, quantidade)` | BL=jogador, AL=recurso, DX=quantidade |
| `0x423355` | BatimentCalculResource | `recalcular_recursos(jogador)` | AL=jogador |

Ambos os métodos estão em [construcoes.py](construcoes.py). Nenhum deles recebe
índice de construção. O saldo econômico continua em `0x4e2ea8` e o registro de
capacidade/indicador por jogador em `0x4dfb2c + jogador*6`.
O retorno Python é `None`: não se atribui significado aos registradores de
trabalho que o x86 deixa na saída.

Evidências: [débito](evidencias/004235bd.asm),
[recálculo](evidencias/00423355.asm) e
[epílogo compartilhado](evidencias/00423025.asm).
BatimentCalculResource salta para `0x423025`, dentro do trecho de StockPossible,
apenas para restaurar pilha/registradores e retornar. A bancada executa esse
epílogo; não substitui o salto nem executa StockPossible inteiro.

## Comportamento confirmado

BatimentEnleveMatiere normaliza os argumentos e chama a primitiva EnleveMatiere
em `0x4235d8`. Não consulta disponibilidade, não recebe sucesso/fracasso de
compra e não interrompe o débito por falta de armazéns. EnleveMatiere reduz o
saldo total e a parcela RMI separadamente, com piso zero em cada um.

Só depois do débito, se o número de armazéns for positivo, consulta o estoque
atual via GetRessourceStock e escreve o indicador em `0x4dfb30 + jogador*6`.
Se não há armazéns, preserva o indicador anterior, inclusive quando ele está
desatualizado ou é diferente de zero.

BatimentCalculResource não debita nem credita. Normaliza AL, retorna sem
alterações se o jogador for 4..255 e também retorna se não houver armazéns.
Para os demais casos, consulta estoque e escreve somente o byte do indicador.
Não modifica saldos, quantidade de armazéns ou capacidade unitária.

As instruções de recálculo repetem a mesma fórmula nas duas rotinas:

```python
estoque_comida = (total_comida - rmi_comida) & 65535
estoque_pedra = (total_pedra - rmi_pedra) & 65535
soma = (estoque_comida + estoque_pedra) & 65535
quociente = soma // numero_armazens
nivel = ((quociente * 7) // capacidade_por_armazem) & 255
```

- Peças e o quarto registro não entram na soma. Um débito de peças ainda
  recalcula o indicador de comida/pedra.
- `DIV BX` usa DX:AX com DX zerado: o numerador é a soma truncada em 16 bits.
- A divisão pelo número de armazéns ocorre **antes** de multiplicar por sete.
  Com estoque 29, dois armazéns e capacidade unitária 100, o nível é zero;
  uma fórmula única `29*7//200` daria um.
- O resultado final é truncado para byte, sem saturação em sete. Estoque
  65.535 com um armazém de capacidade 1 gera `(65535*7)&255 = 249`.
- Não há corte do estoque pela capacidade. Saldos inconsistentes continuam
  podendo produzir underflow u16 e níveis altos ou com wrap.
- Leituras dword sobre saídas word na pilha não mudam esses efeitos observados;
  os testes variam os bytes altos da pilha local e confrontam o estado completo.

O Python compartilha `recalcular_recursos` dentro de `retirar` porque as fórmulas
são iguais. O x86 **não chama BatimentCalculResource** de dentro de
BatimentEnleveMatiere; o corpo está duplicado no original.

## Divisão por zero e ordem dos efeitos

Com número de armazéns zero, a divisão é evitada, mesmo se a capacidade
unitária também for zero. Com armazéns positivos e capacidade unitária zero:

| Rotina | Instrução que falha | Estado econômico após a falha |
|---|---|---|
| BatimentEnleveMatiere | `IDIV EBX` em `0x423635` | Débito já aplicado; indicador anterior preservado |
| BatimentCalculResource | `IDIV EBX` em `0x4233cb` | Saldos e indicador anterior preservados |

Python levanta `ZeroDivisionError` nesses casos, sem rollback. Dezesseis casos
emulados verificam a exceção original, o endereço da falha e a memória restante.
Cada caso usa uma CPU Unicorn nova para não herdar estado interno de exceção.

Exemplo: comida com RMI 100 e total 150; retirada de 80 resulta em RMI 20,
total 70 e estoque 50. Se há um armazém com capacidade unitária zero, o débito
permanece mesmo com falha no cálculo posterior do indicador.

## Validação diferencial

[testes/test_retirada_recalculo.py](testes/test_retirada_recalculo.py) acrescenta
oito testes locais e seis diferenciais. As chamadas internas são originais,
sem mocks, substituições de retorno ou interceptação dos efeitos econômicos.
Ganchos registram argumentos do débito e jogador da consulta sem alterá-los.

| Grupo novo | Execuções x86 |
|---|---:|
| Recálculo em estados variados e pilha suja | 1.024 |
| Débito, truncamentos AL/BL/DX e recálculo | 1.024 |
| Jogadores 4..255: retorno sem acessar as tabelas | 252 |
| Limites numéricos e underflow | 168 |
| Sequências de depósito, retirada e recálculo | 384 |
| Divisão por zero e ordem dos efeitos | 16 exceções esperadas |
| **Total novo** | **2.868** |

Comparam-se os 128 bytes econômicos, os 24 de capacidade, registros de
construções, as duas grades completas de sacolas e as sementes dos geradores,
além de guardas adjacentes. Para ausência de armazéns ou jogador inválido, os
traços confirmam que GetRessourceStock não foi chamado. Para retirada, também
confirmam exatamente uma chamada EnleveMatiere com argumentos truncados.

Estas duas entradas e suas chamadas têm limite de 20.000 instruções e timeout
de um segundo por execução. Os 2.852 casos que não provocam exceção alcançam
o retorno declarado. A sequência integrada compara o estado após cada etapa,
sem recarregar ou reconstruir a memória original entre elas.

Ao concluir esta etapa, eram **53 testes aprovados** e **11.880 execuções x86**:
11.853 paradas declaradas, 24 exceções de divisão por zero esperadas e três
limites de execução esperados herdados dos testes de sacolas. As 64 paradas na
dependência de colono pertencem à etapa anterior de adição, não a estas rotinas.
O relatório completo está em [validacao-emulada.json](validacao-emulada.json).

A contagem global foi traduzida depois em [CONTAGEM_ARMAZENS.md](CONTAGEM_ARMAZENS.md).
Os totais correntes da suíte estão no [README.md](README.md) e no relatório.

## Integração e limites

```python
# Depois de construir EconomiaConstrucoes com os buffers do mundo:
m.retirar(jogador, id_recurso, quantidade)
m.recalcular_recursos(jogador)  # Só quando o chamador original requer recálculo separado.
```

`retirar` já recalcula quando há armazéns; uma chamada adicional é desnecessária
para reproduzir apenas BatimentEnleveMatiere. A primitiva `Economia.debitar`
continua disponível para os chamadores originais que fazem o débito diretamente.
Não substituir todas as chamadas da primitiva pelo wrapper sem conferir o fluxo.

BatimentCalculResource possui a proteção AL>=4 no original. BatimentEnleveMatiere
não protege jogador/recurso contra acesso fora das tabelas; a API Python rejeita
esses casos depois do truncamento. A equivalência dos débitos é, portanto,
delimitada aos jogadores e recursos 0..3, como nos registros conhecidos.

Não foi iniciada uma partida ou validada a frequência de chamada desse recálculo
no ciclo completo. Atualizações de contagem/capacidade por construções e
tecnologias continuam parciais. A interpretação de RMI como provisão inicial
permanece hipótese de design; a subtração e os efeitos registrados aqui são
fatos confirmados de instruções e testes.

Arquivos novos desta continuação: este documento, o teste dedicado e o ASM do
epílogo. Foram atualizados `construcoes.py`, `bancada_construcoes.py`, o exportador,
o validador, os relatórios e os guias locais. Nada foi promovido para pastas
compartilhadas; veja [INTEGRACAO.md](INTEGRACAO.md).
