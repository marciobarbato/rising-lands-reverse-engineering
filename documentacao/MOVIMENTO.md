# Movimento: direções, passo e parâmetros por tipo

Implementação independente: [`movimento.py`](../ferramentas/movimento.py).
Os testes diferenciais comparam cada primitiva com instruções do EXE original
em memória emulada. Ainda não é um sistema completo de movimento: colisões,
rota, ocupação, visão e o relógio que chama essas rotinas permanecem parciais.

## Direção e vizinhança

`0x477042` recebe duas células em `AX` e `DX`, separa x/y com passo 256 e retorna
em `AL` uma direção baseada apenas no sinal das diferenças. Células iguais
retornam zero. Não há cálculo de ângulo contínuo ou escolha pelo eixo dominante.

| Direção | Variação x | Variação y | Sentido no mapa |
|---:|---:|---:|---|
| 1 | -1 | 0 | Esquerda |
| 3 | -1 | -1 | Superior esquerdo |
| 5 | 0 | -1 | Acima |
| 7 | +1 | -1 | Superior direito |
| 9 | +1 | 0 | Direita |
| 11 | +1 | +1 | Inferior direito |
| 13 | 0 | +1 | Abaixo |
| 15 | -1 | +1 | Inferior esquerdo |

`0x4770ee` calcula a célula vizinha para essas direções, usando largura e altura
em `0x497168` e `0x49716a`. Retorna `0xffff` quando o passo sai pela borda.
Direções pares ou não reconhecidas devolvem a célula original. A função não
consulta obstáculos. A reconstrução exige que a célula inicial esteja no mapa;
não inventa um tratamento para entradas inválidas do jogo.

## Giro

`0x448599` trabalha com 16 orientações, nos campos `0x90` (desejada) e `0x91`
(atual). Quando são diferentes, incrementa o contador `0x92` em oito bits.
Só gira se o contador for **igual** ao período `0x93`; depois zera o contador.
Gira uma posição pelo caminho mais curto, com empate de meia volta resolvido
diminuindo a orientação. Há volta de 16 para 1 e vice-versa.

Assim, período zero não significa giro imediato: depende do overflow do contador.
A rotina também escreve `0xda = 2*(direção desejada - 1)+1` para tipos 12 e 15;
esse efeito auxiliar não integra a primitiva pública `atualizar_orientacao`.

O trecho `0x4490fd..0x44915d` permite avançar quando a orientação atual está
a até duas posições da direção desejada no círculo de 16. Testes cobrem todas
as 256 combinações válidas de direções.

## Avanço entre células

`0x448704` recebe o índice em `AX` e um desconto em `DL`. Calcula em oito bits
`passo = campo_0x98 - desconto`, soma/subtrai o passo dos deslocamentos `0x86`
e `0x87` conforme a direção, e o acumula em `0x97`.

Quando o progresso fica maior que 31, o restante da rotina zera os deslocamentos
e o progresso e copia a célula `0x7c` para `0x08`, além de atualizar ocupação,
visão e outros efeitos. O excesso é descartado nesse caminho: 33 volta a zero,
não sobra 1. A implementação `integrar_prefixo_passo` devolve os bytes anteriores
a esses efeitos e informa `chegou`; não simula a atualização do mundo.

Movimentos diagonais recebem o mesmo incremento nos dois eixos, sem fator
`1/sqrt(2)` nesse trecho. Isso não prova a duração global de uma ordem diagonal:
é necessário acompanhar o despacho e possíveis descontos. A chamada em
`0x44916c` fornece desconto zero.

## Inicialização por tipo

`0x457350` usa a tabela de saltos em `0x4572e8` para definir valores por tipo.
Foram recuperados quatro campos e conferidos executando os 26 ramos originais.
Tabela completa: [`movimento-tipos.json`](../relatorios/movimento-tipos.json).

| Exemplo | Incremento `0x98` | Período de giro | Quadros de movimento | Período da animação |
|---|---:|---:|---:|---:|
| Soldado | 2 | 1 | 8 | 2 |
| Capitão | 3 | 1 | 8 | 2 |
| Druída | 1 | 1 | 8 | 3 |
| Speeder | 8 | 1 | 3 | 1 |
| Bunker | 3 | 2 | 3 | 2 |
| Helicóptero | 8 | 2 | 8 | 2 |
| Balão | 1 | 2 | 3 | 4 |

Um soldado com incremento 2 e desconto zero precisa de 16 chamadas efetivas à
integração para completar o contador de uma célula. **Isso não estabelece 16
frames, 16 ms ou uma duração em segundos.** O [ciclo principal](CADENCIA.md)
atualiza o mundo antes do desenho e pode pular desenhos; a taxa efetiva depende
da execução e ainda não foi medida.

## Caminhos ainda parciais

- `0x448d08` tenta direção direta e desvios; falha pode mudar o estado para 3.
- `0x448b9f` lê a rota da tabela em `0x4e1924` quando o estado é 5.
- `0x44930c` despacha estados 0, 1, 3, 4, 5 e 6 e pode chamar `0x43b30b`.
- `0x43b30b` prepara a solicitação e ajusta o destino; `0x42f214` constrói
  candidatos e `0x42e890` pós-processa a rota. O algoritmo não foi identificado como A*.
- As primitivas de ocupação e passagem foram reconstruídas; a bancada executa
  nove cenários sintéticos no solucionador original. Detalhes e limites em
  [CAMINHOS.md](CAMINHOS.md).

Evidências com bytes: `direcao_entre_celulas.asm`, `celula_vizinha.asm`,
`orientacao_unidade.asm` e `inicio_passo_unidade.asm`, na pasta `evidencias`.
