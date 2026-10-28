# EnginViseCible: consulta de alinhamento angular

Implementação: [mira_angular.py](mira_angular.py). Testes:
[test_mira_angular.py](test_mira_angular.py). Esta continuação mantém toda a
entrega em `pesquisas-paralelas/combate`, sem integração ao movimento ou alteração
de fontes compartilhadas. A etapa posterior de animação recebeu autorização
explícita para versionar esta pasta no `main`.

## Resultado confirmado

`EnginViseCible` (`0x451464..0x4516d3`) recebe **AX = índice da unidade**.
O modo e a referência vêm de `+0xb7` e `+0xb8` do registro, não de outros
argumentos. Retorna em `AL` se a orientação atual coincide exatamente com a
orientação requerida. **Não gira a unidade** nem escreve sua orientação.
Não verifica alcance, terreno, dono, vida ou elegibilidade do alvo.

O Python expõe:

- `angulo_calcul(x1, y1, x2, y2, setores)`: tradução do resultado discreto de
  `AngleCalcul`, no domínio u8 e resoluções 8/32 usadas pela mira.
- `celula_alvo_mira(unidades, indice, ...)`: resolução da célula, preservando
  também a segunda consulta dos tipos com torre.
- `mira_requerida(unidades, indice, ...)`: retorna célula, resolução, offset do
  campo comparado, orientação requerida e atual, para inspeção pelo integrador.
- `engin_vise_cible(unidades, indice, ...)`: consulta booleana equivalente a AL.

## Resolução da célula alvo

A primeira etapa, `0x451490..0x451549`, inicializa a célula com `0xffff`:

| Modo em +b7 | Primeira resolução |
|---:|---|
| 1 | Palavra `+0x7c` da unidade referenciada por `+0xb8` |
| 3, com +b0 = 0/1 | `BatimentGetCaseAdjacent(referência, atacante.+0x7c)`; se retornar `ffff`, usa `BatimentGetCase` |
| 3, com +b0 diferente de 0/1 | `BatimentGetCase(referência)` |
| 5 | A própria palavra `+0xb8` |
| Outro | Conserva a sentinela explícita `ffff` nessa primeira etapa |

A origem do **cálculo angular** é `atacante.+0x08`. O passo `+0x7c` do atacante
só é usado para pedir a célula adjacente de construção. Esses valores foram
deliberadamente diferentes nas entradas diferenciais.

Depois da primeira etapa, tipos **12 (Bunker) e 15 (Sun)** resolvem a célula
novamente em `0x45161f..0x45165d`. Nos modos 1/5, repetem a mesma fonte. No
modo 3, pedem **sempre o centro** por `BatimentGetCase`, mesmo que a consulta
anterior tenha obtido adjacência. Portanto:

- Corpo pode mirar na célula adjacente encontrada.
- Torre mira no centro e descarta a primeira célula.
- As consultas iniciais ainda acontecem. Não removê-las ao adaptar a rotina.

Os callbacks são explícitos e distintos:

```python
celula_construcao(referencia)                       # 0x41aee2, retorna célula
celula_construcao_adjacente(referencia, celula_passo) # 0x4239a0, célula ou ffff
```

`celula_construcao_adjacente` não é o callback booleano `adjacente_construcao`
usado pela checagem de alcance. Ausência de consulta necessária levanta
`NotImplementedError`. A reconstrução não contém a geometria completa de
construções; o teste executa os getters e máscaras originais com prédios
sintéticos de footprint cheio 1x1/3x3.

## Quantização angular original

`AngleCalcul`, `0x4796cb..0x4798b0`, recebe `EAX=x1`, `EDX=y1`, `EBX=x2`,
`ECX=y2`, resolução u16 na pilha. Sua saída discreta fica em EAX e a rotina
remove o argumento da pilha com `RET 4`.

O trecho calcula os módulos `dx=|x1-x2|`, `dy=|y1-y2|`. Para ambos não nulos,
obtém o ângulo do quadrante por:

```text
q = acos(dx / sqrt(dx² + dy²)) * 180 / PI_ORIGINAL
PI_ORIGINAL = 3.1415926535
```

Se `dy=0`, usa q=0, incluindo a coincidência. Se `dx=0` e `dy!=0`, usa q=90.
O π imediato tem bits `0x400921fb54411744`, diferentes de `math.pi`; os bytes
e os valores das constantes estão no [manifesto](evidencias/manifesto.json).

O código transforma q conforme o quadrante:

```text
x1 > x2 e y1 >= y2: angulo = q + 180
x1 > x2 e y1 <  y2: angulo = 180 - q
x1 <= x2 e y1 > y2: angulo = 360 - q
demais:             angulo = q
```

Então `passo=360/N`; soma `passo/2`, subtrai 360 se necessário e **trunca**
`angulo/passo` para inteiro. Não usa `round()` ou arredondamento bancário.
O índice final é:

```text
((trunc(angulo/passo) % N + N - N//2) % N) + 1
```

As inclinações importam: de (0,0) para (100,41), N=8 retorna 5; para (100,42)
retorna 6. A direção baseada só nos sinais retornaria a mesma diagonal para
os dois casos e não representa esta função.

No x86 são executadas as rotinas originais:

| Endereço | Papel observado |
|---|---|
| `0x48d5ce..0x48d5f1` | Implementação de acos com raiz e atan |
| `0x48ff4a..0x48ff7f` | Teste de domínio e `FSQRT` |
| `0x48fee7..0x48fefc` | `FPATAN` no caminho sem workaround |
| `0x48c43e..0x48c45b` | Salva control word, põe RC=truncamento, `FRNDINT`, restaura control word |
| `0x47986d` | `FISTP` do valor já truncado |

`AngleQuart` (`0x479610`) contém uma operação de quadrante semelhante, mas
`AngleCalcul` a expande no próprio corpo. A validação não substitui essas
instruções por funções Python.

## Corpo, tipo 3 e torre

Para tipos diferentes de 12/15, `0x4515b6` chama `AngleCalcul` com **8 setores**,
converte o resultado para `2*setor-1` e compara com `+0x91`. Só o tipo **3
(Dell'Orso)** aplica antes `(orientacao+11)%16+1`. Não há tolerância angular.

Para tipos 12/15, `0x4516b5` usa **32 setores**, sem a conversão anterior,
comparando diretamente com `+0x94`. Não depende da orientação do corpo `+0x91`.

| Alvo relativo | AngleCalcul N=8 | Corpo comum +91 | Tipo 3 +91 | Torre +94 |
|---|---:|---:|---:|---:|
| Oeste | 1 | 1 | 13 | 1 |
| Noroeste | 2 | 3 | 15 | 5 |
| Norte | 3 | 5 | 1 | 9 |
| Nordeste | 4 | 7 | 3 | 13 |
| Leste | 5 | 9 | 5 | 17 |
| Sudeste | 6 | 11 | 7 | 21 |
| Sul | 7 | 13 | 9 | 25 |
| Sudoeste | 8 | 15 | 11 | 29 |

Células coincidentes resultam no setor de **leste**: corpo comum requer 9,
tipo 3 requer 5, torre requer 17. Isso é comportamento confirmado; não se
infere que a coincidência seja uma situação desejada ou frequente no gameplay.

## Modos e limites não normalizados

No ramo de corpo, modos fora de 1/3/5 conservam a célula `ffff`; o Python
reproduz essa sentinela. No ramo de torre, o salto de `0x451656` pode chegar ao
cálculo **sem definir EDI**, usando o registrador de entrada do chamador.
A bancada demonstra resultados diferentes com EDI=0 e EDI=ffff nesses modos.
O Python recusa esse caso com `ValueError`, em vez de inventar uma referência.

Referências de unidade fora de 0..799 são recusadas com `IndexError`. O
original poderia ler fora da tabela. Os registros esperados têm 276 bytes.

O Python usa operações `float`/`math` do host. A equivalência validada é do
**setor final e da consulta booleana**, no domínio coordenadas 0..255 e N=8/32;
não dos intermediários x87 de 80 bits, flags de exceção ou bytes altos de EAX.
A configuração sintética x87 é CW=`0x037f`, precisão estendida, exceções
mascaradas e arredondamento ao mais próximo. O flag de workaround em `0x49946c`
é zero, executando `FPATAN`; o caminho alternativo `0x491494` não foi validado.

## Validação diferencial

Os **11 testes novos** (quatro de contrato e sete diferenciais) acrescentam
**145.092 execuções x86 delimitadas**. Com a etapa posterior de animação,
a suíte atual tem **78 testes, 182.491 execuções e zero falhas/erros/ignorados** no
[relatório emulado](validacao-emulada.json).

| Grupo novo | Execuções |
|---|---:|
| Todos os 65.536 pares de módulos dx/dy em 0..255, no quadrante sudeste, para N=8 e N=32 | 131.072 |
| Quatro quadrantes, bordas e 2.048 pares de células aleatórios, nas duas resoluções | 4.744 |
| Função completa, 26 tipos, modos 1/5, orientações válidas e inválidas | 8.190 |
| Construções: adjacência, fallback e centro da torre | 360 |
| Manutenção em `0x452b10`, executando alcance e mira originais | 676 |
| Registradores, tabela inteira de unidades e control word preservados | 26 |
| Modos adicionais e dependência de EDI na torre | 24 |

Os 65.536 pares cobrem todos os módulos de diferenças possíveis entre
coordenadas u8, em um quadrante; os demais quadrantes e translações têm os
casos adicionais descritos. Não são enumerados todos os pares de células do mapa.

Na manutenção, alcance, mira, trigonometria e consultas internas percorrem
o x86 original, sem substituições. A bancada para antes dos efeitos de outros
estados. O teste antigo com AL fornecido continua identificado como teste de
fragmentos, mas já não é a única evidência para essa decisão.

As escritas de dados observadas ficam na pilha sintética. Nos testes de
preservação são conferidos os 800 registros completos, EBX/ECX/EDX/ESI/EDI/EBP,
ESP após o retorno e o control word. O executável original é somente lido e
verificado pelo SHA-256 já registrado; não há execução de Windows ou partida.

Para reproduzir tudo nesta pasta: `python3 -B validar.py --emular`, com JIT do
Unicorn permitido. Sem emulação, a suíte atual executa 26 contratos e
marca 52 diferenciais explicitamente como ignorados.
