# Combate: aritmética recuperada e limites

Implementação: [`combate.py`](../ferramentas/combate.py).
Evidência principal: [`0x4502f0`](../evidencias/ghidra/004502f0.asm).
A rotina recebe alvo em `AX`, modo em `DL`, referência de origem em `BX` e um
parâmetro auxiliar em `CL`. Ela mistura modalidades de dano e efeitos laterais.
Esta etapa reconstrói a aritmética de trechos delimitados, sem selecionar alvos,
simular projéteis ou reimplementar todos os efeitos de morte.

## Modo 1: unidade atacando unidade

No caminho `0x4503b8`, a matriz é indexada por tipo do atacante e tipo do alvo.
O cálculo acrescenta, em bytes:

1. Campo `0xf7` do atacante.
2. Modificador 5 consultado em `0x428cc0`, usando dono e tipo do atacante.
3. O byte em `0x4965ac` (`BONUSCAPITAINE`) quando a consulta `0x4500e4` retorna verdadeiro.

Os truncamentos para oito bits fazem parte do código observado. Por exemplo,
250 mais 10 vira 4. `dano_bruto_unidade` recebe o bônus de proximidade já
resolvido pelo chamador: zero quando a consulta retorna falso.

## Redução comum e aplicação à vida

Em `0x45059c`, o código subtrai o campo `0xf6` do **alvo** e o modificador 6
de `0x428cc0`. Nesta chamada, os argumentos de dono e tipo continuam vindo do
**atacante** (`EBP`), não do alvo (`ESI`). A reconstrução conserva essa leitura.
Ainda não há uma associação completa entre a tabela de modificadores e a
evolução tecnológica; não se chama esse valor automaticamente de blindagem do alvo.

Depois das subtrações, o resultado é interpretado como inteiro de oito bits
com sinal. Se for negativo, vira 1; se for zero, permanece zero. Não é
`max(1, dano)`: essa expressão mudaria o caso zero.

Em `0x450644..0x450679`, o bit 3 de `alvo + 0xdc` pode diminuir o byte de dano
em mais um. Essa proteção acontece **depois** do tratamento do sinal anterior.
O código compara a vida `u16` com o dano com sinal. Se a vida for maior, subtrai
e guarda os 16 bits inferiores; caso contrário, entra no ramo de morte.
Esse ramo escreve vida zero em `0x450763`, mas tem outros efeitos não reconstruídos.

### Caso de borda confirmado

Se o dano reduzido for zero e o bit 3 estiver ativo, o byte vira 255, interpretado
como -1. A vida aumenta um ponto, sem limite de vida máxima nesse trecho.
Exemplo emulado: vida 100 → 101. É um comportamento da aritmética original,
não uma regra desejada inventada para a reconstrução. A pesquisa não estabelece
com que frequência esse conjunto de condições ocorre em uma partida normal.

## Bônus de proximidade: o filtro de capitão não aparece

A chamada em `0x450422` põe 2 em `EAX`, coerente com o ID do capitão, e consulta
raio 10 ao redor da célula do atacante. Entretanto, `0x4500e4` sobrescreve `EAX`
antes de usá-lo. No corpo examinado, a consulta:

- Varre a grade apontada por `0x4e0f38`.
- Aceita entradas com `(valor & 0xc000) == 0x4000` e extrai o ID com
  `(valor & 0x3ff8) >> 3`.
- Compara o dono da instância com o dono solicitado.
- Compara a distância quadrática, retornando verdadeiro ao encontrar uma entrada válida.

Não compara o tipo da unidade com 2 e não exclui explicitamente a própria
unidade. O teste emulado colocou soldados, capitães, colonos e criaturas de
tipo 24 na grade: todos foram aceitos quando dono e distância coincidiam.
Também conferiu outro dono e célula fora do círculo. A conclusão vale para
**essa consulta**; a composição real da grade durante o ataque ainda pode
afetar quando o bônus é aplicado.

## Outras modalidades e questões em aberto

O modo 8 consulta a linha 26 da matriz, carregada de `MINE`, em `0x450475`.
O modo 9 começa com metade da vida em `0x450494`. Os modos 3 e 4 acessam outras
fontes e tabelas. Não foram combinados numa fórmula universal.

Faltam rastrear seleção e validade do alvo, alcance, cadência, projéteis,
tecnologias, morte completa e relação com a simulação. O `BLINDAGE` do INI é
carregado, mas sua aplicação direta não foi confirmada neste caminho.

A bancada diferencia os resultados aritméticos dos efeitos não executados.
Não inicia o jogo, e passar nesses testes não garante equivalência do combate completo.
