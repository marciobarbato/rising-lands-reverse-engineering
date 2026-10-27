# BatimentAjouteMatiere: capacidade e excedentes

Continuação de 27/10/2026, limitada a `pesquisas-paralelas/economia`.
Implementação: [construcoes.py](construcoes.py). Referência:
[0042340f.asm](evidencias/0042340f.asm), do EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Nenhum projeto Ghidra, arquivo original, subsistema de movimento ou operação Git
foi necessário. As bancadas e leitores existentes foram importados somente para leitura.

## Resultado e escopo da tradução

O corpo econômico e as decisões de `BatimentAjouteMatiere` foram traduzidos.
Os ramos comuns executam também as chamadas originais de crédito, sacolas e
procura de espaço durante a validação. O ramo especial do tipo 4 foi traduzido
até sua dependência de retirada de colono, que exige implementação externa.

| Endereço | Nome original | Cobertura Python / x86 |
|---|---|---|
| `0x42340f` | BatimentAjouteMatiere | Capacidade, crédito, indicador, excedentes, contador do tipo 4 e contrato da dependência |
| `0x46769d` | GetRessourceStock | Consulta de estoque já traduzida na primeira etapa; chamada original mantida |
| `0x4678f2` | AjouteMatiere | Crédito já traduzido; chamada original mantida |
| `0x4470d2` | BagAccepte | Ramo DL=1, usado pelo tipo 4: ocupação+1 <= limite |
| `0x4761a9` | TerrainDeposeSac | Laço de quantidade u16, chamando CreerSac por unidade |
| `0x47605d` | CreerSac | Criação, incremento u8, recusa e transbordo de pilhas |
| `0x4757af` | SacCherchePlace | Procura em cinco anéis, ordem de visita e escolha aleatória |
| `0x475763` | TerrainAccepteSac | Predicado equivalente às verificações embutidas na procura |
| `0x4704dc` | Random | Fórmula e atualização do estado `0x497164` reproduzidas |
| `0x41dde0` | BatimentRetireColon | **Não traduzida**; 64 comparações param na entrada real, sem executar seus efeitos |

Não há substituição de chamadas internas na bancada de referência. Um gancho
registra os argumentos das chamadas sem modificar registradores, memória ou fluxo.
Nas entradas que exigem retirar colono, a parada em `0x41dde0` é declarada;
o restante dessa chamada não integra a alegação de equivalência.

## Estruturas, tipos e capacidade

`BatimentAjouteMatiere` recebe AL=recurso, DX=quantidade, BL=jogador e
CX=índice da construção. A tabela de construções começa em `0x49a0c8`, com
registros de 276 bytes. O jogador do argumento é usado nas contas; o dono em
`construção+4` não o substitui.

| Campo da construção | Uso observado nesta rotina |
|---|---|
| `+2`, u16 | Célula da construção, coordenadas x e y nos dois bytes |
| `+8`, u8 | Tipo que seleciona os ramos |
| `+0x0e`, u16 | Limite do BagAccepte, acessado por `bag+2` |
| `+0x72`, u16 | Ocupação do BagAccepte, acessada por `bag+0x66` |
| `+0x78`, u16 | Contador do ramo tipo 4, incrementado somente se menor que 5 |

A tabela original de tipos em `0x495d8c`, passo 52, confirma os nomes:
2=SANCTUAIRE, 3=CAVE (ARMAZÉM no INI brasileiro), 4=CULTURE.
Os 52 bytes e os nomes desses três tipos estão no [manifesto](evidencias/manifesto.json).
O nome de tipo não foi usado sozinho para deduzir sua função.

Os quatro registros de capacidade começam em `0x4dfb2c`, passo seis:

| Offset | Tipo | Significado confirmado |
|---|---|---|
| `+0` | u16 | Número de armazéns do jogador |
| `+2` | u16 | Capacidade por armazém; inicializada com 100 por BatimentAlloc |
| `+4` | u8 | Indicador de ocupação calculado pela rotina |
| `+5` | u8 | Byte preservado, sem interpretação atribuída |

Evidência do significado: `BatimentInitCave` (`0x419112`) conta construções
ativas por tipo e copia a contagem de tipo 3 para o primeiro word em
`0x419140`. `InitBatimentPlayer` (`0x41be88`) incrementa esse word quando o
tipo é 3 (`0x41bfd7..0x41bf61`). BatimentAlloc escreve 100 no segundo word
em `0x419040`. Essas rotinas foram inspecionadas estaticamente, sem tradução
de toda a inicialização ou de suas chamadas de unidades/tecnologias.

## Cálculo confirmado

Para tipos diferentes de 4, sendo todos os operandos quantidades u16:

```python
q = quantidade & 65535
s = (estoque_comida + estoque_pedra) & 65535
c = (numero_armazens * capacidade_por_armazem) & 65535

if numero_armazens == 0:
    credito = 0
    excedente = q
    # Não chama AjouteMatiere nem altera o indicador.
else:
    credito = q
    excedente = 0
    if s + q > c:
        credito = (c - s) & 65535
        excedente = (q + s - c) & 65535
    AjouteMatiere(recurso, credito, jogador)
    indicador = (((s + credito) & 65535) // numero_armazens * 7)
    indicador = (indicador // capacidade_por_armazem) & 255
```

**Detalhes confirmados por testes diferenciais:**

- O limite compartilha **estoque de comida e pedra**, excluindo RMI. Peças
  não entram na soma, embora um crédito de peças passe pelo mesmo teste.
- Igualdade cabe: só há excesso se `s+q > c`.
- Tanto a soma inicial de estoque quanto o produto de capacidade são u16.
  Os cálculos de `c-s` e de excesso também chegam truncados aos consumidores.
- Não há `max(c-s, 0)`. Com estoque 150, capacidade 100 e entrada 10, o original
  envia crédito 65.486 à primitiva e gera excedente 60. Pelo wrap da primitiva,
  um saldo 150 passa a 100 nesse exemplo.
- O nível usa **duas divisões inteiras**, primeiro por número de armazéns,
  depois por capacidade unitária. Não é uma divisão única por capacidade total.
- O numerador da primeira divisão é truncado para u16 pelo `DIV word`.
- O nível usa o crédito calculado antes de AjouteMatiere aplicar o teto de
  9.999. Assim, pode divergir de um nível recalculado a partir do saldo final.
- Se há armazéns e a capacidade unitária é zero, `IDIV` em `0x423501` falha
  **depois do crédito**. Não há rollback. Python levanta ZeroDivisionError
  no mesmo ponto semântico, preservando a alteração já feita no saldo.
- O corpo lê saídas u16 como dwords em alguns pontos da pilha. As escritas
  relevantes dependem dos bits baixos; 1.024 casos também variam a sujeira
  da pilha local para conferir que a tradução não depende de seus bits altos.

`StockPossible` (`0x422fde`) é uma consulta diferente: soma totais de comida e
pedra, enquanto BatimentAjouteMatiere usa estoques. Não se deve unificá-las
numa política supostamente mais consistente; StockPossible não foi traduzida aqui.

## Destino do excedente

Quando `excedente & 65535` não é zero:

| Tipo | Recurso | Célula entregue a TerrainDeposeSac |
|---|---|---|
| 3, CAVE | 1, comida | `(posição + 0x202) & 65535` |
| 3, CAVE | Qualquer outro | `(posição + 3) & 65535` |
| 2, SANCTUAIRE | Qualquer recurso | `(posição + 0x303) & 65535` |
| Demais tipos comuns | Qualquer recurso | Nenhuma chamada: excedente sem depósito |

Essas adições operam no inteiro da célula, podendo carregar x para y. Elas não
consultam dimensões do mapa ou acessibilidade. Não substituí-las por uma soma
independente de coordenadas. A validação inclui bordas e wrap no endereço u16.

Exemplo: um armazém de capacidade 100 com estoque 60 de comida e 30 de pedra
recebe 20 de comida. São enviados 10 ao crédito e 10 sacolas para `posição+0x202`;
RMI permanece igual, e o indicador passa a 7. Se a célula de destino tem outro
tipo de conteúdo, o pedido não vira sacolas e não retorna ao saldo do jogador.

## Sacolas e procura de espaço

As grades são apontadas por `0x507d74` (tipo) e `0x507dac` (quantidade), cada
uma com 65.536 bytes. O tipo codificado é `0x42 + id_recurso`: peças 0x42,
comida 0x43 e pedra 0x44. A rotina aceita também o quarto ID, gerando 0x45.

`TerrainDeposeSac` chama CreerSac uma vez por unidade. CreerSac:

1. Recusa uma célula com conteúdo diferente de zero e do tipo solicitado.
2. Em célula vazia, escreve tipo e quantidade 1, sobrescrevendo quantidade antiga.
3. Em célula do mesmo tipo, incrementa a quantidade em **u8**.
4. Se o resultado excede 31, desfaz o incremento e chama SacCherchePlace.
5. Tenta criar de novo na célula devolvida, sem testar um sentinela de erro.

SacCherchePlace aceita a origem se estiver vazia ou com o mesmo tipo e
quantidade **diferente** de 31. Caso contrário, procura em anéis de raio 1..5.
Para cada deslocamento de -raio..raio, visita esquerda e direita, e depois
cima e baixo quando não se trata dos cantos. Testa limites fixos 0..255.
Não lê grades de ocupação, colisão, regiões ou caminhos.

Cada anel avança o gerador de `0x497164` e usa seu resto por `8*raio` como
ordinal. A contagem de candidatos começa em 1. Resto zero ou maior que a
quantidade disponível faz passar ao anel seguinte, mesmo havendo lugar.
O parâmetro 49 colocado em EAX antes da chamada não limita o sorteio:
o gerador original ignora seu EAX de entrada e devolve o novo estado inteiro.

**Bordas e estados problemáticos confirmados:**

- Ao não escolher lugar em cinco anéis, retorna `0xffff`. CreerSac interpreta
  isso como a célula real `(255,255)`: pode depositar ali ou recusar o conteúdo
  incompatível. Dois testes integrados conferem esses resultados.
- Para pilhas com quantidade 32..254, a criação pode repetir a mesma célula
  indefinidamente: a procura considera a origem aceitável, mas a criação
  desfaz o incremento acima de 31. Três casos conferem o limite do x86, sem
  apresentá-lo como retorno normal.
- Quantidade 255 passa a zero pelo incremento u8 e termina. Não é saturada em 31.
- `TerrenoSacolas.criar` usa um limite funcional de 10.000 tentativas e levanta
  `LimiteDeposito` se necessário. Esse limite pertence à tradução, não ao jogo.

## Tipo 4, CULTURE

Esse ramo ignora a quantidade de recurso recebida e não chama AjouteMatiere.
BagAccepte é chamado com ponteiro `construção+0x0c` e DL=1. Se
`ocupação + 1 <= limite`, incrementa o contador u16 em `+0x78` somente enquanto
ele é menor que 5. Um contador que já está acima de 5 é preservado.

Se não há alojamento, chama BatimentRetireColon com o índice da construção.
Depois lê sua posição atual, incrementa **apenas AH em 2** (y com wrap de byte)
e pede **uma sacola de comida**, independentemente do recurso recebido.
A tradução exige callback explícito `retirar_colono(indice)`. Na ausência dele,
levanta `RetiradaColonoPendente` antes de inventar os efeitos da dependência.

O teste local com callback verifica o contrato e a sacola posterior. Os 64
casos x86 de recusa param na entrada `0x41dde0`, comparando memória e argumento.
Não validam retirada, criação ou liberação de unidades e não executam movimento.

## Testes desta continuação

| Grupo novo | Chamadas delimitadas / resultado esperado |
|---|---:|
| Capacidade, overflow, créditos e pilha suja | 1.024 |
| Destinos do excedente e sacolas originais | 384 |
| Pilhas cheias e célula incompatível | 96 |
| Tipo 4 com alojamento e contador | 256 |
| Tipo 4 parado em BatimentRetireColon | 64 |
| Procura por espaço, bordas, ordem e semente | 512 |
| CreerSac e TerrainDeposeSac | 192 |
| Falta de lugar, uso da célula 0xffff | 2 |
| Divisão por zero, falha após crédito | 8 exceções esperadas |
| Pilhas corrompidas sem término | 3 limites esperados |
| **Total novo** | **2.541** |

Ao concluir esta etapa de adição, eram **39 testes aprovados** e 9.012 execuções
x86. Destas, 9.001 alcançam parada declarada, oito conferem a exceção e três
conferem o limite de execução. As 64 paradas de dependência fazem parte das
9.001, não são chamadas completas a BatimentRetireColon.

O débito de construções e o recálculo foram depois traduzidos e validados em
[RETIRADA_RECALCULO.md](RETIRADA_RECALCULO.md). Os totais correntes da suíte estão
no [README.md](README.md) e no relatório de validação emulada.

São comparados os 128 bytes econômicos, os 24 bytes de capacidades, a tabela
fornecida de construções, as duas grades inteiras de sacolas e a semente.
Guardas conferem escritas vizinhas e preservação do outro gerador em `0x498db4`.
Traços também comparam os argumentos reais de crédito e depósito de sacolas.
BatimentAjouteMatiere e TerrainDeposeSac permitem até 1.000.000 de instruções;
CreerSac e SacCherchePlace isolados conservam o padrão de 20.000. Cada execução
tem timeout de um segundo e intervalos de código declarados. Não inicializa o Windows.

## Limites e integração

Não foi observada uma partida. A recontagem global foi depois traduzida em
[CONTAGEM_ARMAZENS.md](CONTAGEM_ARMAZENS.md). A atualização incremental da
capacidade por destruição, tecnologia ou transferência ainda continua parcial.
A geração de produção e o transporte também não foram reconstruídos.
O significado preciso do contador do tipo CULTURE ainda requer outros
consumidores; a operação de incremento até 5 é confirmada.

`EconomiaConstrucoes` recebe o estado econômico, capacidades, registros de
construções e grades de sacolas. A API valida comprimentos e índices, ao
contrário do código original sem proteção. `ResultadoDeposito` é um diagnóstico
novo: `credito_enviado` registra o operando da primitiva, e `pedido_sacolas`
registra a tentativa, sem prometer que o terreno a aceitará.
As instruções de promoção e sincronização dos buffers estão em
[INTEGRACAO.md](INTEGRACAO.md).
