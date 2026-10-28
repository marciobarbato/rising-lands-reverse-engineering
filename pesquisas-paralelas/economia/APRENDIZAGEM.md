# Conclusão da aprendizagem na biblioteca

Continuação de 28/10/2026, limitada a esta pasta. Implementação em
[aprendizagem.py](aprendizagem.py). Executável brasileiro, SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Nomes e endereços conferidos com RISING.SBL e os bytes originais.

## Rotinas e alcance

| Nome original | Endereço | API Python / alcance |
|---|---|---|
| CalculTroupe | `0x4259e6` | `calcular_biblioteca(indice)`: ramo tipo 6 completo |
| SortilegeEstRealisable | `0x474958` | `disponivel(jogador, tipo)` |
| SortilegeSetRealisable | `0x474974` | `liberar(jogador, tipo)` |
| SortilegeEstInvente | `0x474991` | `inventado(jogador, tipo)` |
| SortilegeSetInvention | `0x4749ad` | `marcar_inventado(jogador, tipo)` |
| SortilegeResetRealisable | `0x4749ca` | `zerar_disponiveis(jogador)` |
| SortilegeResetTechnologie | `0x4749f2` | `zerar_tecnologia()` |
| SortilegeSetTechnologie | `0x474a38` | `atualizar_ordens(jogador)` |
| SortilegeInitTechnologie | `0x474a95` | `inicializar_ordens()` |
| BatimentSetTechnologie | `0x41c76c` | `atualizar_pesquisas_biblioteca(jogador)`: somente DL=6 |

Também foram exportados os acessores usados pelo corpo inline de produção:
BatimentGetColons (`0x41a4c4`), BatimentGetType (`0x41a4f4`) e
BatimentGetCapacite (`0x41f3ed`). Seus efeitos correspondem à contagem e ao
divisor já incorporados em [producao.py](producao.py).

O ramo biblioteca fica em `0x425e99..0x4260aa`, com despacho pela entrada
`0x4259e6` e retorno pelo epílogo `0x42640d`/`0x41db1d`. O avanço está inline;
não há chamada a ConstruitSort nesse caminho. O Python reaproveita o algoritmo
equivalente já traduzido. A referência x86 executa a entrada normal e todas
as dependências originais até RET, sem callbacks, sufixos sintéticos ou mocks.

**CalculTroupe não está inteiramente traduzida.** A API rejeita construções
de outro tipo antes de alterar estado. Criação, saída, reparo e movimento de
unidades presentes em outros ramos não fazem parte desta entrega. O mesmo
limite vale para os tipos diferentes de 6 em BatimentSetTechnologie.

## Duas tabelas, dois conjuntos de opções

Cada tabela tem 20 bytes, no formato `jogador*5 + tipo`:

| Endereço | Campo do modelo | Significado confirmado pelas operações |
|---|---|---|
| `0x508f30` | `propriedade.sortilegios` | Marca os tipos incluídos nas ordens do tipo de unidade 4 |
| `0x508f44` | `inventados` | Participa da seleção de pesquisas oferecidas pela biblioteca |

Os quatro acessores de flags recebem AL=jogador e **DX=tipo**, não DL.
As consultas devolvem o byte original, inclusive valores como 128 e 255.
Os setters gravam exatamente 1. Nenhum deles refaz listas automaticamente.
“Inventado” e “disponível” seguem os nomes/consumidores do original; não são
sinônimos, nem provam por si só todo o fluxo de descoberta e uso em gameplay.

SortilegeSetTechnologie reinicializa a Bag de ordens do tipo de unidade 4,
com capacidade 5, e insere todos os tipos cujo byte disponível seja diferente
de zero. O endereço passa pela tabela de ponteiros em `0x4e19b8`; no modelo,
o offset é `jogador*2704 + 4*104` dentro de `propriedade.ordens`.
SortilegeInitTechnologie aplica a operação aos quatro jogadores sem zerar flags.

BatimentSetTechnologie com DL=6 reconstrói a Bag em
`0x4dd6e8 + jogador*2288 + 6*104`, representada por `propriedade.pendencias`.
Inclui tipos com `inventado != 0` e `disponivel == 0`. AL>=4 retorna sem efeito,
uma guarda existente no original. Essa lista contém opções de pesquisa;
não se identificou nela uma fila FIFO de trabalhos agendados.

As duas listas são compactadas em ordem crescente de tipo, com etiqueta 4 e
valor word igual ao tipo. BagInit zera cabeçalho, 30 valores, 30 etiquetas e
o contador word `+0x66`, preservando os seis bytes `+0x60..+0x65`. BagPrend
incrementa tanto o word `+0` como o word `+0x66` por inserção. O helper Python
implementa apenas essa reconstrução após reset, não uma BagPrend genérica.

SortilegeResetRealisable zera só os cinco bytes disponíveis do jogador.
SortilegeResetTechnologie zera ambas as tabelas para os quatro jogadores.
Nenhum dos resets atualiza as Bags. Isso é diferente de inicializar ordens.

## Ordem da conclusão

1. O despacho identifica o tipo 6. Se `+0x74` for zero, retorna imediatamente,
   **antes** da primeira consulta de tempo. Isso difere de chamar ConstruitSort
   isoladamente, que consulta o tipo mesmo quando a flag está zero.
2. Com flag ativa, o corpo inline consulta o tempo uma vez. Progresso `+0x8c`
   zero retorna sem avanço nem conclusão. Com progresso positivo, consulta
   novamente o tempo e aplica o avanço já documentado em [PRODUCAO.md](PRODUCAO.md).
3. Consulta o tempo uma terceira vez e compara o progresso atualizado com
   `tempo*100`, sem saturação. Abaixo do limite, retorna com o novo contador.
4. Ao atingir ou ultrapassar o limite, chama, nesta ordem:
   SortilegeSetRealisable, SortilegeSetTechnologie e BatimentSetTechnologie.
   O jogador vem do proprietário byte `construção+4`, não da seleção da interface.
5. Limpa o estado da construção conforme a tabela abaixo.

| Campo | Valor depois da conclusão |
|---|---|
| word `+0x78` e word `+0x86` | `0xffff` |
| byte `+0x7b` | `0xff` |
| words `+0x7c`, `+0x7e`, `+0x80`, `+0x82` | zero |
| byte `+0x74` e dword `+0x8c` | zero |
| byte `+5` | conserva 3; qualquer outro valor vira 5 |

Os outros bytes são preservados, incluindo `+0x75..0x77`, `+0x7a`, `+0x84`,
`+0x88` e a Bag de colonos. Não há crédito, débito, devolução, retirada de colono
ou criação de unidade. A conclusão não verifica previamente a flag “inventado”:
mesmo se ela estiver zero, o tipo em produção pode ser marcado disponível.

Não há retorno semântico de conclusão em AL/EAX nesta rotina; a API retorna
None e o estado registra os efeitos. Uma segunda chamada após a conclusão
retorna pela flag zero, sem tentar consultar o novo tipo `0xff`.

O arredondamento x87 inicial `0x127f` continua necessário. Com tempo 10,
progresso 871, 29 colonos e divisor 100, o incremento é 128: chega a 999 e
ainda não conclui. Na chamada seguinte, conclui e zera o contador. Substituir
a operação por uma divisão inteira mudaria a chamada em que a conclusão ocorre.
Tempo zero com progresso positivo conclui imediatamente; progresso zero com
flag ativa não conclui. Divisor zero mascarado mantém o incremento 100.

## Testes e evidências

Nove testes locais e sete diferenciais novos, com 3.732 execuções x86:

| Grupo | Execuções |
|---|---:|
| Consultas e setters: quatro jogadores, cinco tipos, quatro valores de byte | 320 |
| Todas as 32×32 combinações de flags, nas duas reconstruções de listas | 2.048 |
| Todos os valores de AL na guarda de BatimentSetTechnologie, DL=6 | 256 |
| Sequências de resets e reconstrução global das ordens | 256 |
| Bibliotecas com saldos, campos opacos, tempos, flags e limiares variados | 512 |
| Sequências completas, chamadas após conclusão e fronteira de arredondamento | 82 |
| Todos os valores do estado `+5`, mais duas inativas com tipo `0xff` | 258 |

Todos alcançam RET normal. Não foram adicionadas paradas de dependência ou
exceções esperadas nesta fase. As comparações cobrem estruturas completas,
recursos, capacidades, unidades, terreno, semente, tabelas de tipos, seleções,
as duas tabelas de flags, as duas famílias de Bags, buffers de propriedade e
guardas. Verificam também registradores preservados, controle/pilha x87 e a
ordem dos três efeitos de conclusão. Os ganchos apenas observam a execução.

Os tempos de sortilégio e estados deste corpus são sintéticos; não se executou
o carregador original. O teste de perda da última biblioteca é uma composição
Python com a tradução anterior de InitBatimentNeutre: confere que disponibilidade
é zerada e invenções são mantidas, sem alegar uma nova execução x86 desse fluxo.

```sh
python3 -B pesquisas-paralelas/economia/extrair_evidencias.py
python3 -B pesquisas-paralelas/economia/validar.py
python3 -B pesquisas-paralelas/economia/validar.py --emular
```

O último comando exige Unicorn e permissão para seu JIT neste ambiente. O
exportador inclui 93 símbolos e cinco trechos auxiliares; ter ASM exportado
não significa que todos os ramos da rotina estejam traduzidos. Os relatórios
de validação são gravados somente nesta pasta.

## Integração e limites

Construir `Aprendizagem(p, propriedade, inventados=bloco_20_bytes)` com a mesma
instância de EconomiaConstrucoes em produção e propriedade. O construtor exige
essa identidade para evitar atualizar mundos diferentes. Reutiliza as flags
e Bags da propriedade; copia somente o novo buffer de invenções. Os padrões
são sintéticos. Sincronizar os buffers com o estado real do jogo.

No ramo da biblioteca, chamar `calcular_biblioteca(indice)` **em lugar de**
chamar primeiro `avancar_sortilegio`: o método já inclui o avanço e duplicar
as chamadas altera o progresso. Outros tipos continuam com seu próprio fluxo.
O início da aprendizagem, a agenda de CalculTroupe, o uso dos sortilégios e os
outros ramos de tecnologia ainda estão pendentes.

Guardas adicionais Python: jogador 0..3 nos acessores/ordens, tipo 0..4 após
truncar DX, índice dentro do buffer e as guardas de produção/Bag existentes.
O original pode acessar fora das tabelas; esses casos não são equivalência
validada. A guarda AL>=4 da reconstrução de pesquisas é original e preservada.
Nenhuma partida foi iniciada; não se simulam configurações x87 arbitrárias.
