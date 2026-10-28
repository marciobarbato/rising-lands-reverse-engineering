# Mercado: consulta e avaliação de propostas

Continuação de 28/10/2026 no branch `codex/economia-mercado`, em worktree
separada. As alterações pertencem somente a `pesquisas-paralelas/economia`.
O checkout compartilhado continua no `main`; seus arquivos e índice não são
usados para preparar esta entrega. Sem Ghidra, execução de Windows ou alterações
nos subsistemas de busca de caminhos, contornos e movimento.

## Rotinas e domínio traduzido

| Endereço | Símbolo SBL | API em `Mercado` |
|---|---|---|
| `0x462a58` | GetNbRessource | `quantidade_recurso(jogador, recurso)` |
| `0x466bac` | EvalueCoutProposition | `avaliar(jogador)` |
| `0x46d817` | PlayerGetType | `tipo_jogador(jogador)` |
| `0x46d838` | PlayerEstAllie | `aliado(jogador, outro)`, domínio 0..3 |
| `0x46dc6c` | PlayerGetSympathie | `simpatia(jogador, outro)`, domínio 0..3 |

`EvalueCoutProposition` recebe jogador em AL, soma a proposta e grava dois
words. Não verifica saldo, não aceita a proposta, não transfere recursos e não
limpa quantidades. A API retorna None; não interpreta EAX como sucesso.
O epílogo compartilhado real fica em `0x4661d3..0x4661da`.

`GetNbRessource` recebe **AL=recurso e DL=jogador**, consulta os totais com
GetRessource e retorna um EAX inteiro: 0=peças, 1=comida, 2=pedra. Para qualquer
outro ID u8 devolve 65535, inclusive 3. Essa consulta não devolve estoque
`total-RMI`, nem o quarto registro da tabela econômica.

Os métodos Python protegem jogadores/contatos fora de 0..3, após truncar u8.
Exceção: `tipo_jogador` reproduz o retorno 2 do original para AL>=4.
A proteção dos outros métodos é adicional: o x86 pode ler fora das quatro
linhas. `PlayerEstAllie` original aceita igualdade antes de conferir os limites
e permite índice 4 em parte do caminho; esses acessos não são emulados pela API.

## Estado confirmado pelas instruções

| Base original | Buffer Python | Organização |
|---|---|---|
| `0x496f8c` | `contatos` | Quatro bytes, contato de cada jogador |
| `0x496fb0` | `precos_unidades` | 26 preços globais u8 |
| `0x496fcc` | `precos_recursos` | Três preços globais u8: peças, comida, pedra |
| `0x4e29bc` | `unidades_oferecidas` | Quatro linhas × 26 quantidades u16 |
| `0x4e2a8c` | `unidades_pedidas` | Quatro linhas × 26 quantidades u16 |
| `0x4e2cfc` | `recursos_oferecidos` | Quatro linhas × três quantidades u16 |
| `0x4e2d14` | `recursos_pedidos` | Quatro linhas × três quantidades u16 |
| `0x4e2930` | `indicadores` | Um word por jogador |
| `0x4e2948` | `diferenca` | Um word global, sobrescrito a cada avaliação |
| DWORD em `0x5080a8` | `jogadores` | Ponteiro para quatro registros de 20 bytes |

Nos registros dos jogadores: +1 é o tipo lido por PlayerGetType, +6 contém
bits de aliança, +12 contém quatro simpatias u16, reinterpretadas como signed16
pelo avaliador. `PlayerEstAllie(a,b)` testa o bit b do jogador a; quando a=b,
retorna 1 sem consultar esse bit. Não supor simetria das máscaras ou simpatias.
`simpatia` já expõe o signed16 usado pelo chamador; o original retorna os bits
em AX e o chamador executa MOVSX.

As duas metades da proposta são lidas na **linha do jogador avaliado**, mesmo
as quantidades pedidas ao contato. Os preços são independentes dos custos de
recrutamento e aprendizagem. Os rótulos oferecido/pedido são corroborados pelos
acessos de MarcheDebarasseMiniDonne/Veut; a ordem dos recursos aparece também
no trecho `0x464bee..0x464c1a`, que reordena peças/comida/pedra para TestRessource.
Esses chamadores foram inspecionados, não traduzidos integralmente nesta fase.

Os preços estáticos do EXE estão em `evidencias/parametros-mercado.json`:

- Recursos: peças=2, comida=1, pedra=1.
- Unidades, IDs 0..25: `10,13,22,18,20,10,13,10,16,5,10,25,35,30,25,45,0,0,0,0,0,0,0,0,0,25`.

Esses valores vêm diretamente da imagem PE com hash conferido. Não foi
reconstruído o ciclo que carrega ou modifica preços; não afirmar que esses
valores permanecem constantes numa partida. O construtor usa zeros sintéticos
quando um buffer é omitido e não carrega esses padrões automaticamente.

## Fórmulas confirmadas e limites aritméticos

Sejam O a soma oferecida e P a soma pedida. Cada uma soma 26 produtos
`quantidade_u16 × preço_u8` de unidades e três produtos de recursos.
O máximo é 484.631.325, que cabe em signed32. Os produtos seguintes podem
exceder signed32 e devem conservar apenas os 32 bits inferiores.

Para jogador j e contato c, a aliança usada é sempre `aliado(c,j)`.
A simpatia usada é `simpatia(c,j)` quando tipo(j) != 2, mas **inverte para
`simpatia(j,c)` quando tipo(j) == 2**. Não se atribui aqui um nome de gameplay
ao valor 2; a bifurcação numérica está confirmada pelo x86.

O fator K é `80 + simpatia + 40 × aliado(c,j)`. Define-se D(x,y) como divisão
signed32 que primeiro reinterpreta x após wrap e trunca o quociente para zero.

| Caso | Valor ajustado A | Indicador antes de truncar u16 | Diferença antes de truncar u16 |
|---|---|---|---|
| tipo != 2 | D(O×K,100) | D(A×100,P) se P!=0; senão 200 se A!=0, ou 0 | A−P |
| tipo == 2 | D(P×100,K) | D(A×100,O) se O!=0; senão 100 | A−O |

Os dois produtos por 100 também sofrem wrap signed32. Não substituir IDIV
por `//` em valores negativos e não fundir as duas divisões em uma razão única.
O word do indicador não é limitado a 0..100. A diferença é guardada como bits
u16, sem saturação; não assumir uma única interpretação signed nos consumidores.

Exemplos validados contra as instruções:

- O=P=100, simpatia zero, sem aliança: tipo !=2 gera indicador 80 e diferença
  65516 (bits de −20); tipo 2 gera 125 e 25.
- Ambos os lados vazios: tipo !=2 gera indicador 0; tipo 2 gera 100, quando
  K!=0. Isso não demonstra aceitação de uma troca vazia pelo fluxo completo.
- O=199, P=3, K=−1: A=−1; a segunda divisão produz −33, guardado como 65503.
- Tipo 2 com K=0 falha no IDIV em `0x466d94`, inclusive com proposta vazia.
  Indicadores, diferença e demais buffers permanecem intactos.

O contexto estático `0x4674b1..0x4674c6` lê o indicador como word sem sinal e
o compara com 100. Não foi executado esse fluxo completo de interface. Os casos
de overflow, preços máximos e estados inconsistentes são testes de fidelidade
aritmética; não são alegações de estados alcançáveis normalmente ou de exploração.

## Validação

`testes/test_mercado.py` acrescenta dez testes locais e sete diferenciais:

| Grupo | Execuções x86 |
|---|---:|
| 256 IDs de recurso × quatro jogadores | 1.024 |
| Tipos de jogador, máscaras direcionais e simpatias | 1.392 |
| Cada componente da proposta, com preços brutos do EXE | 232 |
| Tipos, simpatias, alianças, lados vazios e limites u16 | 648 |
| Estados aleatórios, preços u8, quantidades u16 e contato próprio | 1.024 |
| Produtos máximos, sinais e vetor numérico explícito | 21 |
| Divisão por zero, com CPU nova por caso | 16 |
| **Total desta etapa** | **4.357** |

São 4.341 execuções desde a entrada até RET e 16 exceções esperadas. A bancada
executa os três acessores reais e GetRessource; não substitui chamadas por mocks.
Compara buffers inteiros, saldos, bytes vizinhos, pilha ao retornar e os
registradores preservados pelo avaliador. Ganchos somente observam a ordem de
consultas e todas as escritas na imagem PE: em avaliações normais há exatamente
dois MOV word; nos demais caminhos testados não há escrita nesses buffers.
Unicorn pode informar no gancho os bits altos do registrador de origem; o
registro das escritas usa o tamanho efetivo da instrução e confere os bytes reais.

Os acessores de jogador são validados somente no domínio declarado acima.
Não são executados o carregador, a interface, APIs Windows ou uma partida.
O hash original e os limites de execução seguem a bancada existente.

## Integração e reprodução no branch isolado

Importar `Mercado` de `mercado.py` e passar a mesma `Economia` já usada pelo
mundo: `mercado = Mercado(mundo.economia, jogadores=bloco_80_bytes, **buffers)`.
`buffers` contém os nomes e blocos da tabela de estado. Todos são copiados;
sincronizar os buffers de entrada antes da chamada e exportar `indicadores` e
`diferenca` depois. Não criar um saldo independente nem debitar ao avaliar.

`mercado.quantidade_recurso(j, id)` é somente consulta. `mercado.avaliar(j)`
modifica as saídas e retorna None; não usá-lo como autorização de compra.
Não calcular uma proposta por contato usando a linha do contato: ambas as
quantidades pertencem a j. Não substituir essas tabelas pelos custos de tipos.

Na worktree `/Users/marcio/git/Rising Lands/engenharia-reversa-economia`, que
compartilha o diretório pai de `source`, executar:

```sh
python3 -B pesquisas-paralelas/economia/extrair_evidencias.py
python3 -B pesquisas-paralelas/economia/validar.py
PYTHONPATH='/Users/marcio/git/Rising Lands/engenharia-reversa/.local/python' \
  python3 -B pesquisas-paralelas/economia/validar.py --emular
```

O PYTHONPATH permite ler Unicorn já instalado no checkout original. Não copia
dependências nem altera configuração compartilhada. `-B` impede bytecode nos
módulos lidos. Os relatórios são gravados somente na economia desta worktree.
A suíte completa está resumida em README.md e nos dois JSON de validação.

O usuário autorizou push e integração no `main` remoto na continuação de
[transferências](TRANSFERENCIAS_MERCADO.md), preservando o checkout compartilhado.
A promoção para módulos compartilhados e a combinação das suítes continuam
sob responsabilidade do chat principal.

## Pendências explícitas

`VideMatiere` (`0x4663eb`) foi traduzida e validada na continuação
[TRANSFERENCIAS_MERCADO.md](TRANSFERENCIAS_MERCADO.md), confirmando os créditos
diretos em RMI/total. Faltam os chamadores completos da troca,
a atualização dos preços, aceitação/cancelamento e a execução
integral da troca. A preparação/movimentação das unidades será mantida como
dependência do subsistema responsável. A economia ainda não está concluída.
