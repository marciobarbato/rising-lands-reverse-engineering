# Origem dos campos de ataque: inicialização e persistência

**Não foi identificado um atribuidor direto de 2 ou 3 a `unidade+0x8A` nesta
edição do EXE.** Foram identificadas oito escritas diretas nesse byte: todas
produzem 0 ou 1. Há caminhos de carregamento que recebem esses valores de
arquivos sem normalizá-los; isso não demonstra que alguma partida os produza.

A inicialização de `+0x79/+0x7A` vem de `EnginSetTypeCaract` (`0x457350`).
`EnginSetType` (`0x457B87`) zera `+0x8B`, mas conserva `+0x8A` e não limpa
antecipadamente `+0x79/+0x7A`. Esses dois últimos só mudam nos ramos de tipo
que possuem uma escrita explícita. Não são quatro campos sempre zerados juntos.

Traduções em [inicializacao_ataque.py](inicializacao_ataque.py), comparações
em [test_inicializacao_ataque.py](test_inicializacao_ataque.py), bancada em
[bancada_inicializacao.py](bancada_inicializacao.py). Os nomes franceses vêm
dos símbolos já extraídos do executável; os nomes Python descrevem o escopo.

## Escritas em +0x8A

| Instrução | Contexto | Valor escrito |
|---|---|---|
| `0x445A05` | `SetEnginLanceSortilege` (`0x4459C4`) | 0 |
| `0x445AB3`, `0x445AD1` | `SetAttaqueEngin` (`0x445A36`) | 0 |
| `0x451E08` | `CalculAttaqueEngin`, preparação concluída | 1 |
| `0x452A3A` | Fim do ciclo com espera zerada | 0, através de AH |
| `0x452AF6` | Subestado 2, espera acaba | 1 |
| `0x452B6C` | Revalidação de alcance/mira falha | 0 |
| `0x4531FE` | `EnginRestaureEtat` (`0x45315F`), restauração de magia | 0 |

O caso por registrador merece cuidado: `0x452461` carrega AH com `+0x8B`;
`TEST AH,AH` e `JE 0x452A3A` permitem a escrita somente quando AH é **zero**.
Não é uma atribuição arbitrária do contador ao subestado.

Os aparentes candidatos `0x42752C`, `0x427B8C` e `0x427BAC` pertencem a
`BatimentNextEtape`. ESI é calculado a partir de **0x49A0C8**, a tabela de
construções, não do ponteiro de unidades em **[0x4E19A0]**. O stride 276 é
igual nas duas tabelas, por isso procurar apenas o deslocamento produz enganos.
Também há falsos positivos nas tabelas de saltos `0x4479B4` e `0x4572E8`.

[rastrear_campos.py](rastrear_campos.py) gera
[rastreio-campos.json](evidencias/rastreio-campos.json) com:

- Seção BEGTEXT inteira `[0x401000, 0x493C00)`, 1.995 símbolos e 184.246
  instruções decodificadas; reinício a cada símbolo e registro de 214 bytes
  tratados como dados pelo decodificador.
- 124 candidatos de escrita que sobrepõem os quatro offsets, incluindo
  palavras/dwords e registrador EBP como possível base. 76 são escritas de
  unidade, 37 de construção, dois são tabelas e nove ficam como outros objetos
  ou decodificações não confirmadas.
- Uma segunda varredura, iniciada em cada byte, das formas usuais MOV/INC/DEC
  e operações imediatas que podem sobrepor `+8A`. Ela conserva os candidatos
  desalinhados para inspeção e não confunde uma instrução sem o prefixo `66`
  com uma escrita efetiva de quatro bytes.
- Ajustes/LEAs com os deslocamentos exatos e chamadas diretas dos inicializadores.

**Limite:** essa auditoria não é uma prova completa de aliases ou de fluxo de
controle. Escritas por ponteiros ajustados de outras formas, cópias genéricas,
dados externos e memória preexistente não podem ser descartados pela busca
de deslocamentos. “Fases legadas ou sem produtor nesta versão” é uma hipótese,
não um nome confirmado nem motivo para removê-las da máquina traduzida.

## Quem inicializa +0x79 e +0x7A

`EnginSetTypeCaract`, AX = índice de unidade, lê o tipo em `+1` e despacha pela
tabela de 26 entradas em `0x4572E8`. A tradução reproduz **todas as escritas no
registro**, não somente os campos investigados: giro, passos, parâmetros de
quadros e outros bytes brutos. A tabela Python é uma transcrição explícita;
os resultados esperados não são gerados pelo emulador.

| Tipo | +79: projétil | +7A: quadro de emissão |
|---|---:|---:|
| 0 | conserva | 6 |
| 1 | 25 | 1 |
| 2 | 1 | 7 |
| 3 | 26 | 4 |
| 4 | conserva | 5 |
| 5, 6, 7 | conserva | conserva |
| 8 | 9 | 6 |
| 9, 10 | conserva | conserva |
| 11 | 27 | 1 |
| 12 | 22 | 0 |
| 13, 14 | conserva | conserva |
| 15 | 1 | 0 |
| 16, 17 | conserva | conserva |
| 18 | 17 | 2 |
| 19, 20 | conserva | conserva |
| 21 | 24 | 6 |
| 22 | 23 | 6 |
| 23 | 23 | 5 |
| 24 | conserva | conserva |
| 25 | 26 | 1 |

Não preencher “conserva” com zero, nem deduzir +79 do tipo da unidade. O código
de emissão tem exceções adicionais: por exemplo, tipo 25 usa o projétil 33
nesse caminho apesar de seu +79 ser inicializado com 26. Continuam valendo
as regras de [ANIMACAO_DISPARO.md](ANIMACAO_DISPARO.md).

Prólogo comum: `+BC=255`, `+DB=8`, `+DA=1`, `+F9=0`, `word(+102)` recebe
**somente o byte baixo** de RECHARGE em `0x4965DE + tipo*50`. Tipos acima de
25 também executam esse prólogo antes de retornar, lendo além da tabela de
tipos válidos; os testes desse caso não os transformam em tipos suportados.

Tipo 4 consulta modificador 12 e escreve `+DA=(10+mod12)&255`; donos 4/200
produzem modificador zero. Tipo 6 força visão +BB=5. Tipos 16/17 põem +AB=50;
17 também limpa/reconfigura +94/+95/+96/+A4. Nenhum ramo escreve +8A ou +8B.

## Quem inicializa +0x8B

`EnginSetType` (`0x457B87`) recebe **AX=índice, DX=célula, BL=direção, CL=tipo**.
Em `0x457CA1`, escreve **+8B=0**. Inicializa posição atual/passo/destino,
campos locais de orientação e ordem, limpa a busca se pertence à unidade e
chama `EnginSetTypeCaract`. Estado principal 0/4 é preservado; os demais viram 7.

A rotina lê apenas o byte baixo de visão e alcance² da tabela de tipos.
Não se deve quadrar de novo o alcance. Após caracterizar, consulta
`EnginTypeGetCapacite` e modificador 1 para preparar a estrutura de carga
local. Na tradução, essas consultas são callbacks explícitos; não há leitura
ou alteração de saldos, inventários globais ou navegação. Os testes executam
os getters originais dentro da chamada completa.

Chamadas diretas encontradas:

| Local da CALL | Chamador | Inicializador |
|---|---|---|
| `0x420F69` | `SortieTroupe` | `EnginSetType` |
| `0x422AE8` | `CalculTrajectoire` | `EnginSetType` |
| `0x457F1F` | `CreerEngin` | `EnginSetType` |
| `0x47AF35` | `LezardRun` | `EnginSetType` |
| `0x457D86` | `EnginSetType` | `EnginSetTypeCaract` |
| `0x46ADA6` | `LoadEngin` de missão | `EnginSetTypeCaract` |

`+8B` não é exclusivo do ataque: navegação escreve zero/incrementa esse byte,
e os controladores de trabalho, reparação, transporte e construção escrevem
esperas de **10, 20 ou 50** e as decrementam. O inventário completo de
instruções está no JSON de rastreio. Exemplos: `0x4494FC` incrementa em
`DeplaceEngin`; `0x44A785` atribui 20 em `CalculPiege`; `0x44B75B` atribui 50
em `CalculReparer`; `0x44EB20` atribui 10 em `EnginCalculTransporte`.

`SetAttaqueEngin` e seu `ResetOrdre` não zeram +8B. O teste nativo passa pelos
dois corpos, para 26 tipos e esperas 0/1/20/50/255, e observa apenas +8A sendo
escrito entre os quatro campos. Não se deve acrescentar uma limpeza de +8B
ao aceitar a ordem. A modelagem de movimento/trabalho permanece nas outras
frentes, sem ser duplicada aqui.

## Carregadores: uma entrada possível para valores externos

Há dois símbolos chamados `LoadEngin`, além de `LoadEnginGame`:

| Entrada | Formato/caminho | Efeito sobre os campos |
|---|---|---|
| `0x46ACBF` | Missão ETA: 140 bytes, pula 512, lê `tamanho-652` no offset +8C | +79/+7A/+8A/+8B vêm no prefixo; unidade existente é recaracterizada |
| `0x46B01E` | Save: lê o tamanho u16 do cabeçalho em cada registro | Conserva os quatro campos; não chama `EnginSetTypeCaract` |
| `0x479D10` | Outro leitor indexado: sempre 276 bytes | Leitura bruta do registro inteiro, sem filtro desses campos |

`SauveEngin` (`0x46B119`) grava tamanho 276 e os registros existentes, além
das rotas separadas. Isso permite **persistir** fases 2/3 já presentes, mas
não explica quem as produziu originalmente.

`preparar_apos_carga_missao` traduz o trecho **0x46AD8B..0x46B019**, após as
leituras e após a escrita +BD no slot ordinal feita em 0x46AD83. Não inclui
essa escrita sobre outra unidade nem o laço/I/O. Estado zero retorna; estado
4 passa por `ExisteEngin`, que nesse contexto só verifica “diferente de zero”.
O trecho executa a caracterização e preserva +8A/+8B, inclusive 2/3 fornecidos
na entrada. Depois sobrescreve a recarga com a **palavra inteira**, +DA=10
para tipo 4, +DA=0 para 14/16 e alguns campos de proprietário/áudio/visibilidade.
Não usar o resultado de `caracterizar_tipo` sozinho como pós-carga final.

`preparar_apos_carga_game` traduz **0x46B08F..0x46B0E3**: +BD=0,
dword(+110)=0 e dword(+104)=FFFFFFFF. Todo o restante é conservado.
Os testes cobrem os 256 valores de +8A para cada tipo 0..25.

A bancada para antes de `FileRead` e compara endereço/tamanho dos pedidos.
**Não executa I/O/Windows, não injeta um retorno de sucesso na CPU e não
alega emular o carregador completo.** Os testes de pós-carga começam com
registros sintéticos já disponíveis em memória.

## Conferência dos mapas originais

O leitor existente de ETA foi reutilizado somente para consulta. Os **38
arquivos** de `source/cd/WORLD`, **2.604 registros**, têm **+8A=0 e +8B=0**.
Os hashes por arquivo e histogramas dos quatro campos estão no rastreio.
São valores serializados, não amostras de uma partida. A conclusão não se
estende a saves externos, versões diferentes ou todos os estados possíveis.

## Validação e integração

Esta etapa acrescenta **15 testes**, sendo cinco contratos e dez diferenciais,
com **12.178 execuções x86 delimitadas**:

| Grupo | Execuções |
|---|---:|
| Caracterização: 256 valores de tipo × três preenchimentos | 768 |
| Todas as trocas 26×26, duas caracterizações encadeadas | 1.352 |
| EnginSetType completo: tipos, IDs, estados, donos e busca | 1.008 |
| Tipo 4: todos os modificadores u8, seis donos | 1.536 |
| Ordem original preservando espera | 130 |
| Caracterização seguida de despacho de ataque, 26 tipos | 52 |
| Pedidos de leitura dos dois formatos de registro | 26 |
| Pós-carga de missão: 26 tipos × cinco estados × cinco fases | 650 |
| Pós-carga de save: 26 tipos × 256 fases | 6.656 |

Comparam-se os **276 bytes inteiros**, os quatro globais locais da busca e
as escritas observadas por hooks de memória nos campos investigados. Os
hooks observam o original, sem modificar instruções. Registros com lixo
determinístico e transições entre tipos revelam as preservações que se
perderiam se todos os cenários começassem zerados. Os dados sintéticos usados
para testar tipos inválidos são restaurados entre testes, pois seus índices
ultrapassam a tabela e podem coincidir com outras tabelas do executável.

Reprodução nesta pasta:

```sh
python3 -B extrair_evidencias.py
python3 -B rastrear_campos.py
python3 -B validar.py --emular
```

O [relatório completo](validacao-emulada.json) registra **90 testes e 204.271
execuções**, sem falhas. A execução sem `--emular` passa 32 contratos e ignora
58 diferenciais explicitamente. O manifesto contém 85 intervalos originais.

Para integrar depois: selecionar a entrada de inicialização correta, fornecer
`CaracteristicasTipo` já carregadas e consultas de capacidade/modificadores,
usar um contexto de busca explicitamente adaptado e conservar todos os bytes
não escritos. Reutilizar `recompor_memoria` existente para ETA; não copiar nem
reimplementar o leitor. Não acrescentar transições para 2/3, não zerar +8B ao
ordenar ataque, nem recalcular +79/+7A ao carregar um save. Nenhuma integração
foi feita nesta entrega. A origem histórica/externa de fases 2/3 e a execução
completa de carregadores continuam fora do resultado confirmado.
