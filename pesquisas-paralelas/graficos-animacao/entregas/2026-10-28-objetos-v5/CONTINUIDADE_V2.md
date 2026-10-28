# Continuidade — unidades e variantes de bolsa

Esta revisão amplia o marco do Soldado com os tipos 5/6/7/9. Não abrange
produção, coleta, custos, combate, escolha de alvo ou alterações do aplicativo.
Todas as escritas ocorreram em `pesquisas-paralelas/graficos-animacao/`.

## Base reprodutível

- Repositório: `/Users/marcio/git/Rising Lands/engenharia-reversa`.
- Snapshot principal reutilizado: `1c8ebdd43b0a820652b7cb852ae1fe218d4dea5e`,
  942 arquivos em `snapshot/COMMIT/`, com manifesto de caminhos e SHA-256.
- Predecessor desta pesquisa: commit `e531dbbdbe650ae2cbdeab03567981d2d8cd15bd`.
  Os fontes predecessores consultados via `git show` e seus hashes estão em
  `evidencias/proveniencia-v2.json`. Não se importam fontes de outros chats.
- EXE brasileiro: `fontes/cd/INSTALHD/RISING.EXE`, origem
  `/Users/marcio/git/Rising Lands/source/cd/INSTALHD/RISING.EXE`, SHA-256
  `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
- CMP, PIE, INI, ETA e referência visual mantêm os hashes e caminhos de
  `fontes/manifesto.json`; Capstone/Unicorn mantêm `dependencias/manifesto.json`.
- A referência de aparência continua sem valor probatório para índices/fases.

A pesquisa e o congelamento v2 foram concluídos sem operações Git de escrita.
Depois de congelada a revisão, o usuário autorizou diretamente commitar esta
continuação sem alterar o trabalho dos outros chats. A publicação usa somente
os caminhos desta frente e exclui insumos locais. A revisão congelada conserva
o documento anterior a essa autorização; nenhuma revisão congelada foi editada.

## Cadeia de evidência nova

1. Tipo → registro de 50 bytes em `0x4965ae + tipo*50`, chave INI em +12.
2. `EnginSetTypeCaract` → oito quadros, período 2 e oscilação zero para 5/6/7/9.
3. `EnginEnArret` → fases 5/2/3/5; preservação do contador.
4. `AffEngin` estados 2/7 → `AffDeplaceEngin` e tabela `0x412328`.
5. Tipos 5/6/7 → `BagVide` em `0x4470b9`: testa somente u16(+0x0a).
6. Base gráfica selecionada + direção pareada × oito + fase → ID CMP.
7. Tabela `0x410f64` → âncora própria do tipo, independente da variante.
8. `AffCorpsEngin` → blitter base; comparação dos pixels completos em 448 casos.

O predicado é confirmado por leitura e execução original, não deduzido a partir
dos volumes visíveis nos sprites. Não inferir que u16(+0x0a) seja quantidade de
um recurso particular. A simulação deve fornecer esse campo no contrato.

## Lacunas e próximo passo

- Transformação da sombra, paletas por jogador e composição global permanecem
  sem implementação. A sombra comum ID 10784 é capturada antes do corpo.
- Estado 14 dos oito Colonos do ETA não se tornou validado por validar o tipo.
- Outros 21 tipos e animações de trabalho/ataque continuam sem associação.
- Construções, árvores/pedras, outros objetos ETA, seleção e HUD ficam para
  próximos marcos. Próxima investigação sugerida: ligação entre os estados
  serializados e o despacho gráfico, seguida da transformação da sombra.

Não há informação externa pendente para consumir os cinco tipos nos casos
confirmados. A API exige os campos ausentes em vez de escolher uma variante.
O consumidor deve usar uma cópia íntegra da nova entrega e conferir o manifesto.
