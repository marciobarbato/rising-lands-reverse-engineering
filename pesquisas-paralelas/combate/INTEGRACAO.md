# Handoff para o chat principal

A entrega está isolada nesta pasta. O escopo autorizado do commit é somente
esta pasta, no branch `main`, preservando as alterações dos chats paralelos.
Arquivos originais foram somente lidos.
A versão validada tem **78 testes aprovados e 182.491 execuções x86 delimitadas**;
ver [relatório](validacao-emulada.json) e [pesquisa técnica](README.md).

## Contrato de dados

Importar `alvos_alcance.py`, `mira_angular.py`, `animacao_disparo.py` e
`inicializacao_ataque.py` e `projeteis.py` como módulos separados. Nenhum depende de `movimento`,
`combate`, economia ou tarefas; usam biblioteca padrão, dados extraídos e consultas locais.

- `unidades`: sequência de 800 registros `bytes`/`bytearray`, cada um com 276 bytes.
- `indice`: ID válido 0..799. `0xffff` representa ausência de alvo.
- `grade`: mapeamento célula -> palavra u16; entradas ausentes equivalem a `ffff`.
- `mascaras`: cinco bytes de aliança, preservando o sentido da relação.
- Célula é `x + 256*y`, mesmo em mapas com largura inferior a 256.
- Funções de leitura não alteram os registros. Os efeitos locais de
  `alvos_alcance.py` retornam uma **cópia**; animação e inicialização alteram
  os registros mutáveis fornecidos. Respeitar a docstring de cada entrada.

Para um mundo com `unidades` contíguas, a adaptação mínima é:

```python
registros = [memoryview(mundo.unidades)[i*276:(i+1)*276] for i in range(800)]
alvo = encontrar_alvo(registros, indice, grade_espacial, mascaras)
```

Isso é uma proposta de adaptação; não foi gravado ou integrado em `MundoUnidades`.

## Sequência sugerida de integração

1. Conservar o ponto de chamada original: `elegivel_busca_automatica(registro)`
   são apenas os portões locais de `0x4546bc`, não todo o despacho do tick.
   `encontrar_alvo` reproduz a preferência de scan dos tipos 2/8 e a grade;
   não trocar por uma busca universal do inimigo mais próximo.
2. Depois de encontrar alvo, usar `reacao_alvo_automatico` para distinguir
   mensagem `0x49`, ordem modo 1 ou nenhuma ação. Entrega de mensagens fica com
   a implementação existente do chat principal.
3. Ao emitir `SetAttaqueEngin`, conferir `ordem_ja_definida` antes de qualquer
   reset. Caso seja diferente, chamar o `ResetOrdre` já existente e **depois**
   aplicar `ordem_apos_reset`. Uma ordem recusada ainda pode ter causado reset.
4. Nos estados 1/24, consultar `alvo_ordem_valido` antes de usar a referência.
   Alvo inválido: controle 2 recebe mensagem `0x4a`; outro controle segue o
   ramo original de movimento/limpeza. A pesquisa não executa esses efeitos.
5. No subestado zero, resolver `a_portee` e a célula para `linha_de_tiro`.
   `preparar_inicio` reproduz o portão de alcance/linha/deslocamento, mas ainda
   falta parar a navegação e alinhar corpo. Não chamar o cálculo de dano aqui.
6. Após alinhamento, `iniciar_ciclo_apos_mira` verifica torre/recarga e retorna
   registro novo mais motivo (`girar_torre`, `aguardar_recarga`, `ciclo_iniciado`).
   Seu domínio começa em `0x451d4d`: não substitui o giro anterior do corpo.
7. Somente após o contador de espera original expirar, usar a regra de
   `manter_ciclo_apos_espera`, fornecendo alcance e `engin_vise_cible` de
   `mira_angular.py`. Essa consulta de alinhamento está traduzida e validada;
   não altera a orientação nem substitui as rotinas que giram corpo/torre.

## Dependências que devem permanecer explícitas

`a_portee` recebe `modificador4` já consultado. Ele é somado ao quadrado
armazenado, **sem quadrar novamente**. `arma_carregada` e
`iniciar_ciclo_apos_mira` recebem `RECHARGE` e modificador 3 já resolvidos;
o avanço do contador continua em `ferramentas/combate.py`.

Para modo 3, fornecer `celula_construcao(referencia)` (`0x41aee2`) e, quando
o ramo pedir contato, `adjacente_construcao(referencia, celula_atacante)`
(`0x42381f`). Para estado 24, fornecer `alcance_magia(id_f4)` (`0x4746c9`).
`alvo_ordem_valido` no modo 3 precisa de `construcao_invalida(referencia)`
(`BatimentEnDestruction`, `0x41a70b`) e `dono_construcao(referencia)`
(`BatimentGetPlayer`, `0x41a08c`). Ausência de callback necessário produz
`NotImplementedError`.

A célula de linha de tiro em modo 1 é `alvo +0x7c`; modo 5 usa a referência de
célula. Para modo 3, o código original também pode pedir
`BatimentGetCaseAdjacent` (`0x4239a0`) quando `+0xb0` é 0/1, antes de cair no
centro da construção. Essa resolução ainda não está na função Python de linha.

Para `engin_vise_cible`, fornecer `celula_construcao` e, se `+b0` é 0/1 no
modo 3, `celula_construcao_adjacente(referencia, atacante_mais_7c)`. Este último
retorna uma **célula ou ffff**, não o booleano de `adjacente_construcao`.
Preservar as chamadas mesmo nos tipos 12/15: eles resolvem o alvo de novo e
miram no centro. O corpo compara com `+91` em oito direções ímpares; as torres
comparam com `+94` em 32 setores. Detalhes e modos indefinidos em
[MIRA_ANGULAR.md](MIRA_ANGULAR.md).

Não utilizar a validade de uma ordem como filtro inicial de seleção: os
critérios são diferentes no original. Não exigir `+0x72/estado` no caminho de
grade nem tornar alianças simétricas para “uniformizar” os resultados.

## Máquina de animação e emissão

`ContextoAtaque` recebe registros mutáveis, recarga por tipo, modificadores,
terreno/dimensões e callbacks de consulta/efeito. `calcular_ataque(ctx, indice)`
reproduz um despacho de `0x451914`; `ctx.chamadas` registra os efeitos externos.
`BuscaAtaque` contém quatro globais locais, sem vincular o contexto de navegação.

O backend `efeito_externo(nome, argumentos)` é obrigatório ao alcançar um
efeito; não assumir sucesso silencioso. Os nomes vêm dos símbolos originais:
`ProjectileInit`, `InfligeDegat`, `SortilegeEffet`, `ResetOrdre`, `SetDeplaceEngin`,
`DeplaceEngin`, `AnimBallonStatic`, `EnginGetVolume` e `PlaySnd_PostSound`.
O Python seleciona e ordena os pedidos, preservando as escritas anteriores;
cabe ao backend aplicar os efeitos externos, que podem modificar o registro.

Não acrescentar transições automáticas para +8a=2/3: esse corpo não as escreve.
O subestado 3 também não limpa o próprio +8a. O quadro +7a, o decremento u8 de
+8b e os casos de emissão especial estão em [ANIMACAO_DISPARO.md](ANIMACAO_DISPARO.md).
O pool agora tem uma implementação separada, descrita abaixo. Dano continua
externo; os testes nativos exercitam seus ramos declarados e conferem os
argumentos. Movimento/áudio/balão param na entrada.

## Pool de projéteis

`PoolProjeteis(memoria, efeito_externo, raio_magia)` recebe os 5.600 bytes
mutáveis de 100 registros. Não zerar registros automaticamente ao carregar ou
reusar posições: `resetar` limpa somente +02; `definir` preserva campos sem
escrita no ramo selecionado. `livre` retorna 100 se não houver espaço.

O pedido existente `ProjectileInit` encaixa diretamente em
`pool.iniciar(*argumentos)`. A API retorna índice ou 100 por conveniência;
isso não modela o valor de EAX após o Set nativo. Se o pool estiver cheio,
não transformar a ausência de projétil em cancelamento do ciclo de ataque.
A cadeia foi comparada com o x86 apenas no teste, sem registrar um backend
na aplicação principal.

Fornecer `efeito_externo(nome, argumentos)` para `InfligeDegat`,
`DecouvreTerrain` e `IllumineTerrain`, e `raio_magia(id)` para
`SortilegeGetRayonEffet`. Dano do tipo 26 acontece já na inicialização; não
aplicá-lo de novo por considerar todo efeito um projétil em voo. O tipo 28 usa
o byte baixo do atacante como terceiro argumento de visibilidade, consulta
o raio duas vezes e conserva a ordem descrita em [PROJETEIS.md](PROJETEIS.md).

`preparar_linha(registro)` e `calcular_linha(registro)` operam em uma view
mutável de 56 bytes. A segunda avança no máximo um passo e não desativa o
registro ao terminar. Não equivale ao tick completo: faltam a animação, o
despacho `ProjectileCalcul`, `ProjectileAvance`, colisão e impacto. O campo
+04 é um limiar de contador no consumidor examinado, não velocidade confirmada.

## Inicialização e persistência dos campos

`caracterizar_tipo(u, recarga, modificador12)` traduz `EnginSetTypeCaract`
(`0x457350`). Preserva +8A/+8B; os campos +79/+7A só mudam nos tipos com
escrita explícita. O modificador é uma consulta `(dono, tipo) -> u8`, necessária
para tipo 4 com dono diferente de 4/200. A recarga inicial usa apenas o byte baixo.

`definir_tipo(u, indice, celula, direcao, tipo, caracteristicas,
capacidade_tipo, modificador, busca)` traduz `EnginSetType` (`0x457B87`).
Fornecer `CaracteristicasTipo(visao, alcance_quadrado, recarga)` já carregadas,
`capacidade_tipo(tipo)` e `modificador(dono, tipo, id)` para IDs 1/12 (valores u8
resolvidos). `busca` segue o contrato local de `BuscaAtaque`. A função zera +8B
e preserva +8A; não cria uma unidade na grade nem atualiza a economia.

Escolher o caminho correto ao carregar:

- ETA: reutilizar o leitor e a recomposição de memória existentes; aplicar
  `preparar_apos_carga_missao` somente no ponto correspondente a 0x46AD8B.
  A escrita anterior de +BD no slot ordinal e o laço/I/O não estão incluídos.
  A pós-carga repõe a recarga u16 inteira e sobrescreve +DA de alguns tipos.
- Save: `preparar_apos_carga_game` corresponde somente a 0x46B08F..0x46B0E3;
  não recaracteriza +79/+7A e preserva +8A/+8B.

Não acrescentar a limpeza de +8B em `SetAttaqueEngin`: o corpo original e seu
reset preservam esse contador compartilhado. Não inventar atribuições a
+8A=2/3: foram encontradas oito escritas diretas de unidade, todas com valor
0/1. Os carregadores preservam valores externos, mas nenhum dos 2.604 registros
dos 38 mapas do CD contém essas fases. A origem permanece não identificada;
isso não é prova de que sejam impossíveis durante uma partida.

As tabelas por tipo, limites da auditoria estática, 15 testes novos e exemplos
de escritas de outros subsistemas estão em
[INICIALIZACAO_ATAQUE.md](INICIALIZACAO_ATAQUE.md). Os novos módulos permanecem
independentes; nenhuma adaptação ao mundo compartilhado foi aplicada.

## Reproduzir a conferência sem afetar o trabalho dos outros chats

Nesta pasta, executar `python3 -B validar.py --emular` com Unicorn e JIT
permitido. Sem JIT, `python3 -B validar.py` executa 26 testes de contrato
e marca 52 diferenciais como ignorados. Os relatórios ficam aqui.

O teste antigo de fragmentos de manutenção fornece consultas como entradas;
o novo teste executa alcance/mira originais em 676 cenários. O teste antigo de
ordem começa **após** `ResetOrdre`; o novo ensaio de preservação de +8B executa
ambos os corpos em 130 casos. Nenhum deles valida o ciclo completo. A seleção, a mira, as
adjacências, os alcances suportados e a linha executam suas chamadas originais,
sem substituir funções internas. Construções usam memória sintética 1x1/3x3.

Próximos passos: investigar a origem histórica/externa de +8A=2/3, completar
a geometria de construções e o backend separado de avanço/colisão/impacto.
A aritmética de dano já existente permanece
sob o contrato documentado em `documentacao/COMBATE.md`.
