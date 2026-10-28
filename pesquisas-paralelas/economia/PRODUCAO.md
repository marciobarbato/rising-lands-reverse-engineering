# Avanço de produção de unidades e sortilégios

Continuação de 28/10/2026. Tradução em [producao.py](producao.py), sem alterar
subsistemas de unidades, movimento ou geometria. Original brasileiro, SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Os nomes vêm de RISING.SBL. A economia ainda não está concluída.

## Rotinas e dependências confirmadas

| Nome original | Endereço | Tradução / uso |
|---|---|---|
| ConstruitPerso | `0x423b9b` | `Producao.avancar_unidade(indice)` |
| ConstruitSort | `0x423d14` | `Producao.avancar_sortilegio(indice)` |
| BagContient, somente DL=1 | `0x4471b8` | `contar_unidades(indice, tipo=9)` |
| EnginGetTimeRecrute | `0x4410b7` | Acessor já traduzido em Recrutamento |
| SortilegeGetTimeAprentissage | `0x47476a` | Acessor já traduzido em Recrutamento |
| __CHP | `0x48c43e` | Truncamento x87; efeitos numéricos incorporados no incremento |
| __init_8087 | `0x48e588` | Evidência estática do controle x87; sem tradução do runtime |
| __init_80x87 | `0x4903a6` | Evidência estática de FLDCW; sem tradução do runtime |

As duas rotinas de avanço foram executadas da entrada até RET. A referência
executa as dependências originais e o epílogo compartilhado `0x41db1e`, sem
substituir chamadas por respostas Python. ConstruitSort termina no corpo
compartilhado `0x423ce5` de ConstruitPerso.

## Estado e ordem de execução

AX é o índice da construção, cujo registro tem 276 bytes em `0x49a0c8`.
O retorno semântico é AL, preservando EBX, ECX, EDX, ESI, EDI e EBP.

| Campo da construção | Leitura nesta etapa |
|---|---|
| `+0x08`, byte | Tipo de construção |
| `+0x0c`, Bag de 104 bytes | Referências às unidades presentes |
| `+0x74`, byte | Flag: zero impede avanço |
| `+0x7b`, byte | Tipo da unidade ou do sortilégio solicitado |
| `+0x8c`, dword | Contador de progresso, único campo alterado |

1. ConstruitSort consulta o tempo de `+0x7b` **antes** de verificar atividade;
   descarta esse primeiro resultado. ConstruitPerso não faz essa consulta inicial.
2. Progresso zero ou flag `+0x74` zero: AL=0, sem modificar o registro.
3. Consulta o tempo u16 de `+0x7b` e compara `tempo * 100` com o progresso u32.
   Progresso maior ou igual ao limite: AL=1, sem alterar nada. Tempo zero também
   leva a esse retorno quando o progresso é positivo.
4. Abaixo do limite, conta colonos na Bag, calcula o incremento e soma a
   `+0x8c`; retorna AL=1. Não limita a soma ao limiar nem a uma porcentagem.

**AL=1 não significa produção concluída.** Também ocorre após um avanço que
continua abaixo do limite. Não há limpeza de `+0x74`, retirada de colonos,
criação de unidade, concessão de sortilégio, cobrança ou devolução de recursos.
Não há verificação de proprietário, estado `+5` ou compatibilidade entre tipo
de construção e produto. A conclusão e a frequência de chamada dependem dos
chamadores, ainda não traduzidos nesta fase.

## Contagem e divisor

A chamada é BagContient(Bag=construção+0x0c, DL=1, BX=9). O tipo de unidade 9
é COLON/COLONO na tabela já reconstruída em `relatorios/unidades.json`.
No modo 1, cada slot é processado assim:

- Percorre a capacidade word `Bag+2`, sem consultar a ocupação do cabeçalho.
- Exige etiqueta 1 no byte `Bag+0x42+slot`.
- Lê o índice word `Bag+6+2*slot`; busca o tipo no byte `unidades[indice*276+1]`.
- Conta quando esse tipo coincide com BX. Referências duplicadas contam de novo.

As duas rotinas usam `contagem & 0xffff`. No domínio de até 30 slots, esse AND
não altera a contagem. A Bag e os registros das unidades são apenas lidos.

O divisor bruto é o byte `+18` de cada registro de 52 bytes da tabela em
`0x495d8c`. O ajuste ocorre em AL, com wrap u8, antes da conversão para ponto
flutuante. O byte de hospital vem de `0x495be8`, inicialmente 5 no EXE.

| Tipo de construção | Divisor efetivo | Coeficiente |
|---|---|---:|
| 14, GARAGE | `(bruto - 1) & 255` | 10.0 |
| 19, HOSPI | `(bruto - ajuste_hospital) & 255` | 100.0 |
| Demais tipos | `bruto` | 100.0 |

Nos dados originais, CASERNE tem bruto 8, BIBLIOTHEQUE 3, GARAGE 4 e HOSPI 7.
Os 22 registros, seus bytes, nomes, valores e endereços estão em
[parametros-producao.json](evidencias/parametros-producao.json), extraídos
diretamente do EXE. O uso de `+18` como divisor é confirmado. Interpretá-lo
como uma capacidade geral de trabalhadores e explicar os postos reservados
de garagem/hospital ainda exige outros consumidores; não se renomeou o campo
na tabela compartilhada com base apenas nessa hipótese.

## Arredondamento x87 preservado

`__init_8087` lê o word `0x4993dc`, cujo valor no EXE é `0x127f`, e chama
`__init_80x87`. Este executa FNINIT e carrega a palavra recebida com FLDCW.
Esse controle seleciona precisão de 53 bits, arredondamento ao mais próximo
e exceções mascaradas. É evidência estática da configuração inicial; não prova
que todo chamador em uma partida conserva o controle sem alteração.

Para essa configuração, a sequência reproduzida é:

```python
bonus = int((contagem / divisor) * float(coeficiente))
incremento = 100 + (bonus & 0xffff)
progresso = (progresso + incremento) & 0xffffffff
```

O x86 faz FDIV, FMUL, armazena um double, recarrega-o, chama __CHP e usa FISTP
dword. __CHP troca temporariamente o byte alto do controle para `0x1f`, aplica
FRNDINT em direção a zero e restaura o controle anterior. A tradução conserva
os dois arredondamentos binary64 antes do truncamento. Não substituir essa
expressão por `contagem * coeficiente // divisor`.

Caso diferencial: `contagem=29`, `divisor=100`, `coeficiente=100`. Com controle
`0x127f`, a multiplicação resulta em um valor abaixo de 29; o bônus é 28 e o
incremento 128. Partindo de progresso 1, Python e x86 chegam a 129. Com controle
`0x037f`, de precisão 64 bits, o mesmo x86 chega a 130. Essa diferença também
foi testada em ConstruitSort; a API Python suporta a configuração inicial,
não pretende emular configurações x87 arbitrárias.

Com divisor zero, FDIV/FISTP não equivalem a uma divisão inteira que lança
ZeroDivisionError. Nas execuções com exceções mascaradas, FISTP grava
`0x80000000`, tanto para contagem zero como positiva; o AND `0xffff` produz
zero. O incremento final é **100**. A bancada confere o inteiro escrito
depois de FISTP. A tradução não modela flags de exceção da FPU, seu estado
completo nem exceções desmascaradas.

Mesmo com zero colonos, divisor positivo produz incremento 100. Por exemplo,
com tempo 10, progresso 999, dois colonos e divisor 8, uma chamada chega a 1124,
retorna 1 e mantém a flag ativa; chamadas seguintes deixam o contador em 1124.
A consulta de status já traduzida devolve 112, sem saturação em 100.

## Validação

São oito testes locais e sete diferenciais novos. A comparação inclui as
estruturas completas, saldos, capacidades, terreno, semente, unidades, tabelas
de tipos, seleções e guardas; verifica também os registradores preservados,
restauração do controle x87 e pilha x87 vazia. Os ganchos da bancada apenas
observam entradas de helpers e o inteiro produzido por FISTP.

| Grupo | Execuções x86 |
|---|---:|
| 31 contagens × 256 divisores × 2 coeficientes no ConstruitPerso completo | 15.872 |
| Ajustes u8 de garagem/hospital nas duas rotinas | 2.048 |
| Estados variados, 22 tipos, saldos e campos opacos | 512 |
| Bag modo 1, capacidades 0..30 e seis alvos BX | 186 |
| Flags, tempos, índices, limiares e ordem dos acessores | 156 |
| 24 avanços e consultas por cada um dos 26 tipos reais e cinco sortilégios | 1.488 |
| Comparação dos controles 0x127f e 0x037f | 4 |
| **Total novo** | **20.266** |

Os tempos de unidade do teste sequencial vêm dos 26 registros reconstruídos
no relatório existente. Os cinco tempos de sortilégio são sintéticos; não se
executou seu carregador. Os testes de avanço usam o original completo;
as sequências que começam em `iniciar` usam o início Python já validado e
callback explícito para a saída, sem alegar um recrutamento completo x86.

Reprodução a partir de `engenharia-reversa`:

```sh
python3 -B pesquisas-paralelas/economia/extrair_evidencias.py
python3 -B pesquisas-paralelas/economia/validar.py
python3 -B pesquisas-paralelas/economia/validar.py --emular
```

O Unicorn necessita de execução com permissão para seu JIT neste ambiente.
Não se abre projeto Ghidra nem se escreve nas ferramentas compartilhadas.

## Limites e integração

`Producao(recrutamento, tipos_construcoes=bloco, ajuste_hospital=valor)`
compartilha a instância de Recrutamento e, por ela, o mundo econômico.
Somente copia a tabela de tipos de construção (1144 bytes). Os valores padrão
de tabela/unidades são sintéticos; fornecer os dados reais e sincronizar os
buffers copiados por Recrutamento. O ajuste padrão 5 vem do EXE, mas deve ser
sincronizado com o byte vivo se outro subsistema o alterar.

Chamar `avancar_unidade(indice)` ou `avancar_sortilegio(indice)` na ordem
estabelecida pelo chamador original, mantendo seu controle da finalização.
Não usar o booleano como sinal para criar uma unidade. Não reiniciar a cobrança
nem zerar a flag quando o contador ultrapassar o tempo. Ver
[INTEGRACAO.md](INTEGRACAO.md) para composição com a etapa anterior.

Proteções adicionais da API Python: índice dentro do buffer fornecido (até
1000 registros), tipos de construção 0..21, tipos de unidade 0..25/sortilégio
0..4, capacidade da Bag 0..30 e referências de unidades 0..799. Só valida uma
referência se sua etiqueta for 1. O original não impõe todas essas guardas;
não se reivindica equivalência para acessos fora das tabelas. Em particular,
índice `0xffff` não é uma sentinela tratada nestas duas rotinas.

A emulação não inicia uma partida nem reproduz escalonamento, conclusão,
criação de unidades, aprendizagem efetiva, filas completas, transporte,
consumo/fome ou mercado. Esses fluxos continuam pendentes, juntamente com
as dependências econômicas registradas nas etapas anteriores.
