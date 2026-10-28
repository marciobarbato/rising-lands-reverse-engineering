# Custos e início da aprendizagem

Continuação de 28/10/2026 em [aprendizagem.py](aprendizagem.py). Original:
RISING.EXE brasileiro, SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Nenhum original ou documento compartilhado foi alterado.

| Nome original | Endereço | API / domínio |
|---|---|---|
| SortilegeGetCoutApprentissage | `0x4746fe` | `custos(tipo)` |
| InitApprentissage | `0x422d9f` | `iniciar(jogador, tipo)` |
| ApprentissageSortTerminer | `0x421250` | `terminar_biblioteca(indice)`, somente construção tipo 6 |

As três entradas foram executadas até RET no x86 original. InitApprentissage
termina pelo epílogo compartilhado `0x42399a`. O término explícito é uma rotina
independente; CalculTroupe contém um corpo inline equivalente no ramo biblioteca.
A tradução Python compartilha a implementação sem afirmar que existe uma
chamada entre esses dois corpos no executável.

## Acessor de custos

AL é o tipo de sortilégio. A tabela fica em `0x497174`, com cinco registros
de 46 bytes. O acessor grava somente words nos três ponteiros recebidos:

| Offset do tipo | Conteúdo | Ponteiro de saída |
|---|---|---|
| `+4` | comida | EDX |
| `+2` | pedra | EBX |
| `+6` | peças | ECX |

O Python retorna `Saldos(comida, pedra, pecas, quarto=0)`. O quarto valor é
conveniência da API existente, não uma quarta saída original. As comparações
conferem os seis bytes escritos e os bytes vizinhos preservados. A API não
representa ponteiros sobrepostos nem saídas que apontem para a própria tabela.

Os cinco registros originais do EXE foram adicionados a
[parametros-producao.json](evidencias/parametros-producao.json). Seus valores
iniciais são:

| Tipo | Nome | Tempo | Comida | Pedra | Peças |
|---|---|---:|---:|---:|---:|
| 0 | VISION | 820 | 4 | 2 | 6 |
| 1 | PETRIFICATION | 150 | 6 | 4 | 8 |
| 2 | MIROIR | 220 | 8 | 6 | 10 |
| 3 | ARMURE | 130 | 10 | 8 | 12 |
| 4 | NOVA | 220 | 12 | 10 | 14 |

São dados estáticos do EXE, não a afirmação de que esses são os custos durante
uma partida. O RISING.INI contém valores diferentes, incluindo COUTPIECE=0 nas
cinco seções. O carregador da configuração não foi traduzido/executado nesta
fase; os testes identificam expressamente qual corpus foi usado.

## Ordem de InitApprentissage

AL=jogador e DL=tipo. Essa ordem difere de InitRecruteTroupe. A rotina resolve
a seleção word `0x495be0 + jogador*2` e a construção de 276 bytes em `0x49a0c8`.

1. Lê `construção+0x74`. Se for diferente de zero, retorna sem ler custos,
   debitar ou alterar a construção. Um tipo de sortilégio inválido também é
   ignorado nesse retorno antecipado.
2. Consulta os três custos, depois debita **comida** pelo jogador do comando.
3. Se esse jogador tem armazéns, recalcula o indicador de estoque com a fórmula
   já traduzida. O recálculo ocorre inclusive se o custo debitado for zero.
4. Debita **pedra** e repete o recálculo. O custo de **peças é ignorado**.
5. Só depois dos dois débitos e recálculos escreve quatro campos:
   byte `+0x74=1`, byte `+5=4`, dword `+0x8c=1`, byte `+0x7b=tipo`.

Todos os outros campos são preservados, incluindo dono, tipo da construção,
`+0x7a`, coordenadas de saída e a Bag de colonos. Não confere tipo 6,
proprietário, invenção, disponibilidade, estado `+5` ou progresso anterior.
Uma seleção `0xffff` não é tratada como sentinela: o original calcula e acessa
o ponteiro; o Python rejeita o índice fora do buffer.

**Não há teste de suficiência dentro de InitApprentissage.** Os débitos
individuais de EnleveMatiere reduzem total e RMI até zero, conforme as traduções
anteriores. Portanto, uma chamada com saldos insuficientes ainda inicia o
trabalho. Isso é comportamento dessa rotina, não uma prova de que a interface
normal sempre permite enviar tal comando.

Com armazéns presentes e capacidade unitária zero, o IDIV em `0x422e62`
provoca exceção depois do débito de comida. Pedra não foi debitada, e os quatro
campos de início não foram escritos. A API levanta ZeroDivisionError mantendo
esse estado parcial; não faz rollback. A segunda divisão está em `0x422edf`,
mas não foi artificialmente tornada falha após uma primeira divisão bem-sucedida.

A rotina não tem retorno booleano semântico; `iniciar` retorna None.
O estado distingue recusa por ocupação e início aplicado. Não usar `if iniciar(...)`
como teste de sucesso nem acrescentar recusa automática por saldo insuficiente
à tradução fiel.

## Contexto da interface: confirmado estaticamente

Foram exportados três trechos de contexto, explicitamente separados de funções
e de testes executados até RET:

- Em InputGame, o caminho que chega a `0x42bf6b` testa comida, pedra e peças
  com TestRessource. Se o teste passa, prepara o comando `0x23` em `0x42bf78`.
  O trecho inclui a seleção válida e o desvio do tipo 20 para outro caminho.
- Em ProcessInputGame, `0x45f246..0x45f257` lê o tipo do comando, passa o jogador
  em EAX e chama InitApprentissage em `0x45f24d`, sem usar um retorno booleano.
- Em IconeFillContenu, o teste em `0x45e203` recebe comida e pedra, mas EBX=0
  para peças. O custo de peças foi consultado, porém não entra nesse teste.

Os três pontos não foram executados como interface completa. A hipótese de
que a checagem prévia basta em todo estado de gameplay não foi assumida: a
tradução mantém a diferença entre testar uma proposta e aplicar o comando.
Também não altera o tratamento divergente de peças observado nesses trechos.

## Término explícito e ciclo completo

ApprentissageSortTerminer recebe AX=índice e não testa atividade, progresso ou
tempo. No domínio tipo 6, libera o sortilégio para o **dono da construção**,
refaz as duas listas e limpa os campos descritos em [APRENDIZAGEM.md](APRENDIZAGEM.md).
`terminar_biblioteca` preserva esse caráter incondicional. A verificação de
limiar pertence a `calcular_biblioteca`, que continua sendo a atualização normal.

No original, outros tipos passam por outros ramos de BatimentSetTechnologie;
o tipo 20 também preserva `+0x80/+0x82` na limpeza. A API não finge cobrir esses
casos: rejeita tipos diferentes de 6 antes dos efeitos do término explícito.

Início e conclusão não escolhem necessariamente o mesmo jogador. Se o comando
do jogador 1 aponta para uma biblioteca do jogador 3, o primeiro paga e o
segundo recebe a disponibilidade ao concluir. A referência valida esse estado
inconsistente; não foi demonstrado que a interface o produz em partida.

Foram testados 20 ciclos com os cinco registros do EXE e quatro jogadores:
entrada original de InitApprentissage, chamadas originais sucessivas de
CalculTroupe até a conclusão e uma chamada adicional já inativa. O estado de
memória é mantido entre chamadas. Nenhum helper é substituído por Python.
Essa sequência manual não equivale a executar a agenda ou a interface do jogo.

## Validação e integração

Nove testes locais e sete diferenciais novos. As 1.849 execuções x86 incluem
1.833 retornos normais e 16 exceções de divisão por zero esperadas:

| Grupo | Execuções |
|---|---:|
| Custos u16, passos, argumentos altos e bytes vizinhos de saída | 256 |
| 256 tipos de construção, livres e ocupados | 512 |
| Saldos/RMI, custos, índices, capacidade e pilha suja variados | 512 |
| Exceções após comida, incluindo débito zero | 16 |
| Término explícito sem exigir progresso | 256 |
| Cinco acessores reais e 20 ciclos completos | 257 |
| Início/conclusão com jogador do comando diferente do dono | 40 |

As comparações incluem saldos, capacidades, registros completos, terreno,
unidades, seleções, tabelas de tipos, flags, Bags e guardas. O traço confere
ordem dos débitos e ausência de chamada a TestRessource no início. CPUs novas
são usadas para cada exceção esperada. Os testes anteriores de conclusão
também foram repetidos após compartilhar sua implementação Python.

```python
# a é a instância de Aprendizagem já ligada ao mesmo mundo/propriedade.
custos = a.custos(tipo_sortilegio)
a.iniciar(jogador_do_comando, tipo_sortilegio)
# Nas atualizações do ramo biblioteca, sem avançar uma segunda vez antes:
a.calcular_biblioteca(indice_biblioteca)
```

Sincronizar seleções e a tabela de tipos de sortilégio em Recrutamento.
Não reconsultar e cobrar novamente os custos nas atualizações. Usar
`terminar_biblioteca` somente quando o chamador original pedir término
incondicional; não substitui o cálculo do limiar. Os métodos existentes de
listas e disponibilidade continuam compartilhados com PropriedadeConstrucoes.

Guardas adicionais Python: jogador 0..3, tipo 0..4 após truncamento u8 e índice
dentro do buffer. O início preserva a ordem da guarda de ocupação antes da
validação do tipo. Não se reivindica equivalência para acessos fora das tabelas.
Escalonamento, carregador INI, uso de sortilégios e conclusão de unidades ainda
estão pendentes. Busca de caminhos, contornos e movimento não foram alterados.
