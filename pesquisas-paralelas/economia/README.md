# Economia: consultas, crédito e débito

Pesquisa de 27/10/2026, isolada nesta pasta. Os arquivos originais, o código
preexistente, os relatórios gerais e o projeto Ghidra compartilhado foram usados
somente para leitura. Não houve uso de Ghidra. A autorização de commit no `main`
vale para esta entrega, limitada aos arquivos desta pasta de economia.
Busca de caminhos, contornos de obstáculos e movimento ficaram fora do escopo.

**Resultado:** as primitivas de recursos, o corpo econômico de
`BatimentAjouteMatiere` e o depósito de sacolas estão traduzidos em Python.
Também estão traduzidos o débito de `BatimentEnleveMatiere` e o recálculo de
`BatimentCalculResource`, conforme [RETIRADA_RECALCULO.md](RETIRADA_RECALCULO.md).
`BatimentInitCave` também foi traduzido, reconstruindo contagens por tipo e
número de armazéns, sem redefinir capacidade unitária ou indicador:
[CONTAGEM_ARMAZENS.md](CONTAGEM_ARMAZENS.md).
Os efeitos incrementais de ganho e neutralização estão traduzidos em
[PROPRIEDADE_CONSTRUCOES.md](PROPRIEDADE_CONSTRUCOES.md), com dependências
explícitas para os caminhos de criação/movimento de balões.
Extração de minas, coleta de sacolas/campos e regeneração estão traduzidas em
[EXTRACAO_CAMPOS.md](EXTRACAO_CAMPOS.md), sem incorporar o transporte das unidades.
**108 testes passaram**, com 19.499 execuções x86: 19.448 paradas declaradas,
48 exceções de divisão por zero e três limites de execução esperados.
Não houve testes ignorados na execução emulada. O ramo de retirada de colono
tem dependência explícita; veja [capacidade e excedentes](CAPACIDADE_EXCEDENTES.md).

## Fontes e reprodução

Executável brasileiro: `source/cd/INSTALHD/RISING.EXE`, SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Endereços virtuais na base PE preferencial `0x400000`. Os nomes franceses vêm
do catálogo existente de `RISING.SBL`; seu método de endereçamento está em
`documentacao/SIMBOLOS.md`. Não foram inferidos apenas pela aparência do código.

Leituras iniciais: README geral, CONTINUIDADE, ROTINAS, EMULACAO, SIMBOLOS,
UNIDADES, FORMATOS e código dos leitores/bancadas. A implementação das mutações
e consultas foi confrontada diretamente com os bytes do EXE original.

Comandos a partir de `/Users/marcio/git/Rising Lands/engenharia-reversa`:

```sh
python3 -B pesquisas-paralelas/economia/extrair_evidencias.py
python3 -B pesquisas-paralelas/economia/validar.py
python3 -B pesquisas-paralelas/economia/validar.py --emular
```

O primeiro usa `pefile` e `capstone` já presentes em `../source/python`, verifica
o hash do EXE e grava os trechos nesta pasta. O segundo passa 58 testes Python
e ignora explicitamente 50 testes diferenciais. O terceiro exige Unicorn,
reutilizado de `.local/python`, e executa todos os 108 testes. Nenhum comando
invoca o gerador de relatórios geral ou altera arquivos fora desta pesquisa.
O uso de `-B` evita caches de bytecode nos módulos compartilhados importados.

No sandbox macOS, a tentativa de execução x86 terminou com SIGILL (código 132),
como já descrito em EMULACAO. A execução autorizada com memória JIT passou;
nenhuma configuração de segurança global foi alterada. Os resultados salvos
estão em [validacao-local.json](validacao-local.json) e
[validacao-emulada.json](validacao-emulada.json).

## Layout confirmado

A tabela começa em `0x4e2ea8`. `LoadGameRessource` (`0x46ab21`) lê 128 bytes e
`SauveRessource` (`0x46ab33`) grava os mesmos 128 bytes, sem conversão.
São quatro jogadores, cada um com quatro registros de oito bytes:

```text
endereço = 0x4e2ea8 + jogador * 32 + id_recurso * 8
```

| Offset no registro | Tipo | Fato observado |
|---|---|---|
| `+0` | u16 | Parcela denominada RMI pela consulta original; atribuída e debitada |
| `+2` | u16 | Saldo total retornado por GetRessource; recebe crédito e débito |
| `+4` | u16 | Valor de apresentação convertido por IntToBCD/BCDToInt em CalculMatiere |
| `+6` | u8 | Bits por dígito usados pela animação em CalculMatiere |
| `+7` | u8 | Byte preservado; nenhuma semântica confirmada nesta pesquisa |

O quarto registro existe e é percorrido por `CalculMatiere`. As consultas de
alto nível retornam apenas os três recursos conhecidos e uma quarta saída zero;
não retornam o saldo desse quarto registro. Seu nome econômico permanece aberto.

| ID usado nas mutações | Recurso confirmado | Índice usado nas operações de IA |
|---:|---|---:|
| 0 | Peças (`COUTPIECE`) | 2 |
| 1 | Comida/batatas (`COUTPATATE`) | 0 |
| 2 | Pedra (`COUTROCHE`) | 1 |
| 3 | Registro sem nome confirmado | A saída de índice 3 das consultas é sempre zero |

A associação não depende das quantidades iniciais dos mapas. O carregador de
tipos associa as chaves INI aos campos `+2` comida, `+4` peças, `+6` pedra,
conforme UNIDADES.md. `EnginGetRessource` (`0x4410d2`) devolve esses campos na
ordem comida, pedra, peças. `InitRecruteTroupe` lê seus custos em `0x428430` e
debita respectivamente o ID 1 em `0x428488`, o ID 2 em `0x428507` e o ID 0 em
`0x428583`. A identificação é, portanto, sustentada por uma cadeia direta.

## Rotinas traduzidas e convenções de chamada

Nas três mutações, **AL é o recurso, DX a quantidade e BX o jogador**.
O jogador tem 16 bits nesses acessos, embora as consultas recebam jogador u8.
Não se deve trocar AL por BX ao adaptar uma bancada Watcom.

| Entrada | Nome original | Tradução / comportamento |
|---|---|---|
| `0x467640` | GetRessourceRMI | `consultar_rmi`: RMI de comida/pedra, peças=0, quarto=0 |
| `0x467670` | GetRessource | `consultar`: totais de comida, pedra, peças; quarto=0 |
| `0x46769d` | GetRessourceStock | `consultar_estoque`: total menos RMI para os três recursos, em u16 |
| `0x4676e5` | TestRessource | `suficiente`: compara custos unsigned com totais, aceitando igualdade |
| `0x4678f2` | AjouteMatiere | `creditar`: altera somente total; truncamento u16 antes do teto 9.999 |
| `0x46792c` | EnleveMatiere | `debitar`: reduz total e RMI separadamente, com piso zero |
| `0x46799c` | SetMatiere | `atribuir`: RMI=total=DX, mostrador=0, flags=0, preserva +7 |
| `0x4410d2` | EnginGetRessource | `custos_unidade`: campos dos tipos de 50 bytes, ordem comida/pedra/peças |
| `0x41aace` | BatimentGetRessource | `custos_construcao`: campos contíguos a partir de `0x495d98`, passo 52 |
| `0x45d753` | BatimentRessourceNecessaire | `recurso_necessario` com custos da construção |
| `0x45d7cf` | TroupeRessourceNecessaire | Mesmo núcleo comum com custos da unidade |
| `0x481372` | I_CombienCouteUnite | `custo_ia` aplicado aos custos da unidade |
| `0x481399` | I_CombienCouteBatiment | `custo_ia` aplicado aos custos da construção |
| `0x4813b8` | B_TestStock | `testar_ia(..., estoque=True)`: saldo de estoque >= limiar signed32 |
| `0x481400` | B_TestRessource | `testar_ia`: saldo total >= limiar signed32 |
| `0x485fb9` | iagRessGetPlayerWealth | `riqueza_ia`: soma dos três estoques u16, sem pesos |

Os acessores de recursos usam EAX, EDX, EBX e ECX como ponteiros de saída para
quatro words, e o jogador u8 no primeiro argumento de pilha; o retorno remove
quatro bytes (`ret 4`). `TestRessource` recebe custos em AX=comida, DX=pedra,
BX=peças e jogador na pilha; somente AL deve ser interpretado como booleano.
Os acessores de custo recebem AL=tipo e escrevem nos ponteiros EDX=comida,
EBX=pedra, ECX=peças. Os wrappers de IA recebem EAX apontando para argumentos;
índice no dword +0, limiar/tipo no dword +4 e jogador no byte +0x1c.

`GetRessource`, `GetRessourceStock`, os wrappers de IA e os helpers de falta
compartilham epílogos ou corpos por saltos. A bancada autoriza esses trechos
reais; não presume que toda função termine antes do símbolo seguinte.

## Aritmética e casos relevantes

As regras abaixo são confirmadas por instruções e pelos testes diferenciais:

```python
atribuir: RMI = total = valor & 0xffff
creditar: total = min((total + quantidade) & 0xffff, 9999)
debitar: total = max(total - (quantidade & 0xffff), 0)
         RMI   = max(RMI   - (quantidade & 0xffff), 0)
estoque: (total - RMI) & 0xffff
```

- O teto de 9.999 é aplicado só pelo crédito; atribuição aceita qualquer u16.
  `65535 + 1` resulta em zero, não 9.999. Creditar zero a 12.000 reduz para 9.999.
- O débito não rejeita a operação por insuficiência, não retorna sucesso de
  compra e não possui rollback. `TestRessource` é uma consulta separada.
- Um estado inconsistente com total menor que RMI produz estoque grande por
  underflow u16. A tradução preserva o comportamento, sem corrigir o estado.
- RMI de peças existe no registro e é debitado, mas `GetRessourceRMI` devolve
  zero para peças. `GetRessourceStock` usa o RMI real desse registro.
- `B_TestStock` e `B_TestRessource` devolvem 1 ou -1, não booleano 0/1. Seu
  limiar é comparado como signed32; `0xffffffff` equivale a -1.
- O helper de falta verifica comida primeiro e pedra depois, retornando 1, 2
  ou 0. Ele **ignora peças**. Um retorno zero não prova recursos suficientes.
  Já `TestRessource` testa os três custos.

Exemplo confirmado localmente e reproduzido pelas mesmas primitivas emuladas:

| Operação sobre comida | RMI | Total | Estoque calculado |
|---|---:|---:|---:|
| Atribuir 100 | 100 | 100 | 0 |
| Creditar 40 | 100 | 140 | 40 |
| Debitar 80 | 20 | 60 | 40 |
| Debitar 30 | 0 | 30 | 30 |
| Debitar 1.000 | 0 | 0 | 0 |

## Ligação com os dados reais

Os quatro u16 em `ETA + 0x50004` são comida (ID 1); os quatro em `+0x5000c`
são pedra (ID 2); os quatro em `+0x50014` são peças (ID 0). `LoadRessource`
(`0x46aa96`) chama SetMatiere para esses 12 valores; MissionLoad também possui
as três sequências. Todos os 38 mapas foram lidos pelo leitor ETA existente.

`Economia.de_recursos_eta(eta['recursos_por_tipo'])` é um adaptador novo que
aplica essas atribuições. As tabelas resultantes foram comparadas com 456
chamadas reais a SetMatiere, inclusive preservação do quarto registro e do byte
+7. **Não foi executado LoadRessource com seu I/O original**; o leitor existente
fornece os valores. O teste compara também os offsets brutos dos arquivos.

Os 26 registros de tipo reconstruídos em `relatorios/unidades.json` foram
conferidos com os acessores Python e x86. Isso valida a ligação com o trabalho
prévio; não equivale a executar GetPrivateProfileIntA ou o carregador INI.

## Evidências estáticas adicionais e hipóteses

**Capacidade e excedentes agora traduzidos:**

`BatimentAjouteMatiere` (`0x42340f`) e suas chamadas de sacolas foram traduzidos
e comparados ao original nesta continuação. O tratamento de armazéns, os
excedentes por tipo e os limites estão em [CAPACIDADE_EXCEDENTES.md](CAPACIDADE_EXCEDENTES.md).

`BatimentEnleveMatiere` (`0x4235bd`) e `BatimentCalculResource` (`0x423355`)
também foram traduzidos e comparados, incluindo seus retornos antecipados,
recálculo do indicador e exceções: [RETIRADA_RECALCULO.md](RETIRADA_RECALCULO.md).

`BatimentInitCave` (`0x419112`) reconstrói as 88 contagens u8 e atualiza o
número de armazéns e a contagem do tipo 18. O wrap 256→0 e os campos preservados
estão em [CONTAGEM_ARMAZENS.md](CONTAGEM_ARMAZENS.md).

**Confirmado estaticamente, sem tradução completa:**

- `CalculMatiere` (`0x467718`) converte mostrador e total para dígitos, altera
  bits por dígito, atualiza `+4` e força redesenho em `0x4e05a2`. O jogador
  selecionado vem de `0x508041`. Não credita produção em `+2` nesse trecho.
- `InitRecruteTroupe` (`0x4283e2`) testa os três custos antes dos débitos e ainda
  verifica estado/tipo da construção. Não basta debitar para reproduzir uma fila.
- `LoadGameRessource` e SauveRessource serializam a tabela de 128 bytes; o formato
  completo de salvamento e suas posições no arquivo não foram reconstruídos.

**Interpretação provisória:** RMI parece representar provisões iniciais ainda
disponíveis fora da parcela computada como estoque. Isso é apoiado pela carga
do ETA, pelo crédito que não altera RMI e pelo débito que o reduz até zero.
O nome completo da sigla, a justificativa de design e o vínculo com depósitos
físicos exigem outros chamadores ou uma partida observada. O código conserva
o nome original RMI, sem renomeá-lo para reserva de compras ou dívida.

## Validação e limites

| Grupo diferencial | Execuções x86 |
|---|---:|
| Três consultas, memória de saída e bytes preservados | 1.536 |
| Atribuição, crédito e débito, incluindo limites | 1.541 |
| Suficiência, com igualdade | 512 |
| Operações da IA com limiares signed | 1.024 |
| Riqueza | 256 |
| Acessores de custo e wrappers da IA com dados sintéticos | 208 |
| Helpers de falta para unidades e construções | 512 |
| Sequência de mutações seguida de consultas | 400 |
| Recursos reais dos 38 mapas e custos dos 26 tipos | 482 |
| **Subtotal: primitivas da primeira etapa** | **6.471** |

A etapa de [capacidade e excedentes](CAPACIDADE_EXCEDENTES.md) acrescenta
2.541 execuções; a de [débito e recálculo](RETIRADA_RECALCULO.md), outras 2.868;
e a de [contagem de armazéns](CONTAGEM_ARMAZENS.md), mais 114. Os
[efeitos de propriedade](PROPRIEDADE_CONSTRUCOES.md) acrescentam 1.864.
A etapa de [extração e campos](EXTRACAO_CAMPOS.md) acrescenta 5.641.
A suíte atual soma 19.499. Destas, 19.448 alcançam parada declarada (64 na entrada
de BatimentRetireColon e 32 nas dependências de balão), 48 conferem divisão por zero e três conferem o limite
no ciclo de pilhas corrompidas.

A bancada existente verifica hash, endereços permitidos, parada explícita e
timeout de um segundo por chamada. O limite padrão é de 20.000 instruções;
BatimentAjouteMatiere, TerrainDeposeSac e BatimentInitCave permitem explicitamente 1.000.000.
A bancada de extração e regeneração também permite 1.000.000 por chamada.
A extensão
local não substitui funções chamadas e não oferece APIs Windows. Nas mutações
compara os 128 bytes e guardas antes/depois; nas consultas também compara os
bytes que não deveriam ser escritos entre os ponteiros de saída. Os testes
incluem estados inconsistentes e bits altos nos argumentos de registradores.

Não foi iniciada uma partida. Depósito com capacidade, extração no terreno e
regeneração de campos estão traduzidos. Os chamadores completos de produção
e coleta, transporte, fome, mercado, fluxo completo dos
chamadores de propriedade, tecnologia, persistência integral e filas continuam parciais.
A recontagem global e os efeitos incrementais econômicos estão traduzidos;
os caminhos de criação/movimento de balões permanecem dependências explícitas.
Os testes não alegam invariantes de gameplay para todos os estados possíveis.
As mutações Python protegem índices de jogador/recurso após truncamento;
as mutações originais não fazem essas verificações e podem acessar fora da tabela.
O retorno sem alteração para AL>=4 em BatimentCalculResource corresponde à
proteção existente nessa consulta original.
Também não se modelam registradores de trabalho ou seus valores de retorno
quando não representam uma saída semântica da rotina.

Os ASM exportados incluem rotinas apenas investigadas. O manifesto registra
referências diretas **candidatas**; a varredura linear com recuperação após
bytes inválidos pode perder chamadas ou tratar dados como código. Ela não
substitui análise de fluxo e não cobre chamadas indiretas. A cadeia usada para
identificar IDs foi conferida nos trechos dos chamadores.

## Arquivos desta entrega

- [economia.py](economia.py): tradução e adaptador dos recursos ETA.
- [bancada_economia.py](bancada_economia.py): extensão isolada do emulador existente.
- [construcoes.py](construcoes.py): crédito/débito de construções, recálculo, excedentes e sacolas.
- [bancada_construcoes.py](bancada_construcoes.py): referência x86 sem substituir chamadas internas.
- [bancada_init_cave.py](bancada_init_cave.py): contagem dos 1000 registros no x86 original.
- [proprietarios.py](proprietarios.py): ganho/neutralização, listas, permissões e depósito da matéria.
- [bancada_proprietarios.py](bancada_proprietarios.py): referência original e paradas de dependência.
- [extracao.py](extracao.py): quinze rotinas de minas, coleta e regeneração.
- [bancada_extracao.py](bancada_extracao.py): referência x86 com comparação das grades e da agenda.
- [testes/test_extracao.py](testes/test_extracao.py): 12 testes locais e 12 diferenciais.
- [testes/test_construcoes.py](testes/test_construcoes.py): dez testes locais e dez diferenciais novos.
- [testes/test_economia.py](testes/test_economia.py): dez testes locais e nove diferenciais.
- [testes/test_retirada_recalculo.py](testes/test_retirada_recalculo.py): oito testes locais e seis diferenciais.
- [testes/test_init_cave.py](testes/test_init_cave.py): sete testes locais e cinco diferenciais.
- [testes/test_proprietarios.py](testes/test_proprietarios.py): 11 testes locais e oito diferenciais.
- [validar.py](validar.py): execução e relatórios restritos a esta pasta.
- [extrair_evidencias.py](extrair_evidencias.py): exportador reproduzível do EXE.
- [evidencias/manifesto.json](evidencias/manifesto.json): endereços, hash e referências candidatas.
- `evidencias/*.asm`: trechos com bytes e endereços originais.
- `validacao-local.json` e `validacao-emulada.json`: resultados dos testes.
- [INTEGRACAO.md](INTEGRACAO.md): orientação para o chat principal.
- [CAPACIDADE_EXCEDENTES.md](CAPACIDADE_EXCEDENTES.md): análise desta continuação.
- [RETIRADA_RECALCULO.md](RETIRADA_RECALCULO.md): débito e recálculo do indicador.
- [CONTAGEM_ARMAZENS.md](CONTAGEM_ARMAZENS.md): contagem global, capacidade derivada e integração.
- [PROPRIEDADE_CONSTRUCOES.md](PROPRIEDADE_CONSTRUCOES.md): efeitos de ganho e neutralização.
- [EXTRACAO_CAMPOS.md](EXTRACAO_CAMPOS.md): endereços, fatos, limites e validação de extração/regeneração.
