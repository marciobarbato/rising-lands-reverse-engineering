# Transferências de recursos do mercado

Continuação de 28/10/2026 no branch `codex/economia-mercado`, usando a worktree
isolada `engenharia-reversa-economia`. Todas as alterações são desta pasta.
O usuário autorizou push e integração no `main` remoto ao concluir a validação;
o checkout local compartilhado e seu índice são preservados.

## Rotina e dependências confirmadas

`VideMatiere` ocupa `0x4663eb..0x466533` (fim exclusivo), com nome do SBL e bytes
do mesmo EXE brasileiro identificado nas fases anteriores. Tradução:
`TransferenciasMercado.transferir(jogador, outro)`, em `transferencias_mercado.py`.

No x86: **AL=jogador da proposta, DL=outro jogador**. A rotina salva EBX, ECX,
ESI e EDI, preserva EBP e termina em RET. EDX não é preservado. O método Python
retorna None; não atribui significado econômico ao EAX de trabalho.

As dependências são executadas integralmente na comparação x86:

| Entrada | Rotina | Uso |
|---|---|---|
| `0x46d817` | PlayerGetType | Verifica o tipo antes de cada um dos seis passos |
| `0x4235bd` | BatimentEnleveMatiere | Débito e recálculo do pagador de tipo 1 |
| `0x46792c` | EnleveMatiere | Reduz total e RMI com piso zero |
| `0x46769d` | GetRessourceStock | Consulta estoque para recálculo quando há armazéns |

Não há chamadas a TestRessource, AjouteMatiere ou BatimentAjouteMatiere neste
fluxo. Não há criação de sacolas nem movimentação/criação de unidades.

## Duas etapas, ambas na linha do primeiro jogador

Para j=primeiro argumento e k=segundo argumento, a sequência confirmada é:

1. Percorrer recursos **0=peças, 1=comida, 2=pedra** da linha j em
   `0x4e2cfc`, quantidade u16 oferecida. Se tipo(j)==1, debitar j e recalcular
   seu indicador. Em seguida, creditar a quantidade inteira em k.
2. Percorrer os mesmos três IDs da linha j em `0x4e2d14`, quantidade u16
   pedida. Se tipo(k)==1, debitar k e recalcular seu indicador. Em seguida,
   creditar a quantidade inteira em j.

Cada linha tem seis bytes. A segunda etapa também lê a linha de **j**, não a
de k. A tabela de contatos não é consultada; o segundo argumento determina o
destinatário/pagador, mesmo quando diverge do contato registrado.

Somente o valor numérico 1 do tipo ativa o débito. Os demais valores u8
continuam recebendo/fornecendo créditos, sem débito correspondente. O teste
cobre todos os 256 tipos, mas não atribui um nome de gameplay a cada valor nem
afirma que todos esses estados sejam alcançáveis numa partida normal.

Não se verificam preço, simpatia, aliança, indicador da proposta ou suficiência.
Os buffers de quantidades, jogadores, contatos, preços, indicador da proposta e
diferença global ficam intactos. A função não limpa a proposta: repetir a chamada
repete os efeitos econômicos. Sua integração precisa respeitar o chamador real.

## Crédito direto em total e RMI

Para um registro de oito bytes em `0x4e2ea8 + jogador*32 + recurso*8`:

```text
RMI_novo   = (RMI_antigo   + quantidade) & 65535
total_novo = (total_antigo + quantidade) & 65535
```

Na primeira etapa, o x86 grava total em `0x46643f` e RMI em `0x466449`.
Na segunda, grava RMI em `0x4664cd` e total em `0x4664dc`. A tradução conserva
essa ordem, além dos valores finais. O mostrador (+4), flags (+6), byte +7 e
o quarto registro econômico permanecem intactos.

Não usar `Economia.creditar` nesse caminho: AjouteMatiere só aumenta total e
aplica teto 9.999 após o wrap, enquanto VideMatiere aumenta os dois words e
**não aplica esse teto**. Não usar o depósito com capacidade no lugar do crédito:
não há limite por armazém, recálculo do receptor ou descarte/criação de excedentes.
Mesmo sem armazéns, o receptor recebe a quantidade inteira.

A diferença `(total-RMI)&65535` do receptor permanece igual após cada crédito,
inclusive quando os words transbordam. Isso decorre das duas somas em u16 e foi
conferido em testes; não implica que todo o ciclo, que também contém débitos,
preserve o estoque de cada jogador.

**Novo fato sobre RMI:** não representa apenas uma parcela carregada inicialmente
do ETA. O mercado também a aumenta durante a execução. O nome completo da sigla
e sua interpretação de design continuam sem confirmação. A hipótese anterior
de parcela fora do estoque ainda descreve a consulta, mas precisa contemplar
essas entradas do mercado.

## Débitos e falhas parciais

Cada débito de um jogador tipo 1 usa BatimentEnleveMatiere, preservando o piso
zero independente de total e RMI. Uma quantidade superior ao saldo não reduz o
crédito seguinte: a rotina usa a quantidade original da proposta. Isso descreve
o corpo isolado; não prova que o fluxo completo aceite propostas sem cobertura.

Quantidade zero também chama o débito/recálculo. Com armazéns positivos e
capacidade por armazém zero, o IDIV em `0x423635` falha **após debitar peças**:

- Falha na primeira etapa: o débito de peças de j já ocorreu, mas seu crédito
  para k e todos os passos posteriores não ocorreram.
- Falha na segunda etapa: toda a oferta já foi debitada/creditada, e o débito
  de peças de k ocorreu; o crédito pedido para j e os passos seguintes não.

Não há rollback. `ZeroDivisionError` no Python deixa o mesmo estado parcial.
Não repetir automaticamente a operação depois da falha. Jogadores de outros
tipos não executam o débito e, portanto, não encontram esse divisor, mesmo se
suas capacidades estiverem zeradas com armazéns positivos.

j==k também é processado. Para tipo 1, cada débito seguido do crédito da mesma
quantidade pode elevar um saldo insuficiente até aquela quantidade. Para outros
tipos, as duas metades apenas acrescentam recursos com wrap. Não converter essa
entrada num retorno sem efeitos. A API protege índices u8 fora de 0..3 antes
de qualquer escrita; essa proteção adicional não existe no corpo original.

## Validação diferencial

`testes/test_transferencias_mercado.py` acrescenta 12 testes locais e oito
diferenciais. Os testes executam os bytes originais até RET, ou até a exceção
esperada; não há mocks de dependências nem cortes nos débitos/recálculos.

| Grupo | Execuções x86 |
|---|---:|
| Estados arbitrários, bits altos e pilha suja | 1.024 |
| Todos os tipos em cada lado | 512 |
| Tipos sem débito, capacidade zero com armazéns | 255 |
| Limites de RMI, total, quantidade e tipo | 128 |
| Primeiro e segundo argumento iguais | 64 |
| 32 sequências com transferência repetida | 64 |
| 32 ciclos de avaliação, transferência, seis consultas e reavaliação | 288 |
| Falhas na primeira/segunda etapa, inclusive quantidade zero | 56 |
| **Total desta etapa** | **2.391** |

São 2.335 execuções até RET e 56 exceções esperadas. Cada cenário de exceção usa
uma CPU nova para não reutilizar o estado interno de falha do Unicorn.
Nos ciclos, a memória x86 permanece entre as chamadas; só a preparação normal
dos registradores/pilha é repetida pela bancada.

Comparam-se os 128 bytes econômicos, capacidades, estruturas, terrenos de
sacolas, RNG, todos os buffers do mercado, jogadores e guardas. Um snapshot
contínuo também confere os vizinhos/lacunas das tabelas. Ganchos de observação
verificam as chamadas, seus argumentos, a ordem dos 12 créditos word e os
endereços/tamanhos de todas as escritas na imagem PE. Os registradores
preservados e o equilíbrio da pilha são conferidos no retorno normal.

O caso de transferência para o próprio jogador, o saldo insuficiente e os tipos
incomuns são provas de fidelidade ao corpo x86, não de regras desejáveis para um
jogo novo. Nenhuma partida nem interface completa foi executada.

## Integração

```python
from mercado import Mercado
from transferencias_mercado import TransferenciasMercado

mercado = Mercado(mundo.economia, jogadores=bloco_80_bytes, **buffers_mercado)
trocas = TransferenciasMercado(mercado, mundo)
trocas.transferir(jogador_da_proposta, outro_jogador)  # Retorna None.
```

`mundo` é o EconomiaConstrucoes já existente. O construtor exige identidade
entre `mercado.economia` e `mundo.economia`; não duplicar esses saldos.
Mercado copia os buffers fornecidos: sincronizar as propostas e registros de
jogador antes de chamar. Depois, exportar a memória econômica e capacidades,
inclusive se houver exceção. Não executar um crédito adicional no integrador.

Os comandos de reprodução, dependências lidas pelo PYTHONPATH e hash original
estão em [MERCADO_PROPOSTAS.md](MERCADO_PROPOSTAS.md). O exportador atual contém
102 símbolos, sete trechos auxiliares e cinco contextos; suas 753 referências
diretas são candidatas obtidas por varredura, não prova de alcançabilidade.

Consulta, avaliação e transferência econômica agora estão traduzidas. Ainda
faltam os chamadores completos: `MatiereEstDemander` (`0x464ba2`), a decisão e
limpeza de `CalculValeur` (`0x466533`), atualização dos preços e cancelamento.
Troca/posicionamento de unidades permanece dependência do subsistema responsável.
Não iniciar a tradução de caminhos, obstáculos ou movimento para completar
esses fluxos. A economia como um todo continua parcial.
