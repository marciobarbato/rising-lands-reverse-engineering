# Estado da pesquisa e continuidade

## Concluído nesta etapa

- Repositório Git independente em `Rising Lands/engenharia-reversa`.
- Inventário e identificação do executável local.
- 36 trechos x86 exportados com bytes e anotações.
- Leitores CMP e ETA independentes, em português, com validação de limites.
- Sequência de carregamento dos 38 mapas reconciliada com o código original.
- Carregador dos atributos dos tipos reconstruído e matrizes de dano extraídas.
- Renderização estática do terreno da missão 1 com IDs corrigidos.
- Testes sintéticos e contra o corpus real.
- Ghidra e JDK portáteis instalados, com descompilador nativo ARM64 compilado.
- 255 rotinas exportadas e sete assinaturas de acessores corrigidas.
- Propriedade, coordenadas, vida e campos de carga das 2.604 entradas de unidades.
- Rotina de cura reconstruída e máximo de vida localizado na tabela de tipos.
- Primitivas de movimento e quatro parâmetros dos 26 inicializadores reconstruídos.
- Adições, reduções e aplicação de dano comparadas com o x86 original.
- Laço Windows, atualização antes do desenho e divisor F1–F4 rastreados.
- Contadores de ciclo, recarga e gerador aleatório reconstruídos e emulados.
- Comparação de regiões sob ocupantes, máscaras, alianças, passagem e espera reconstruídas.
- Preparação, busca e pós-processamento originais executados em nove mapas sintéticos.
- Despachante de IA reconstruído; etapas de estruturas, recursos e tarefas localizadas.
- 61 testes aprovados, incluindo 19.194 execuções na bancada, sem iniciar o jogo.
  O teste da orquestração da IA substitui os corpos das etapas internas.

## Questões em aberto

| Tema | Evidência disponível | Trabalho necessário |
|---|---|---|
| Caminhos e colisão | Primitivas reconstruídas e oráculo x86 em nove cenários | Traduzir busca/pós-processamento, gerar regiões e integrar movimento direto e consumo |
| IA | Ordem das etapas e inativação confirmadas; interpretador localizado | Recuperar tabela de opcodes e implementar uma tarefa completa |
| Movimento e tempo | Direções, giro, prefixo, parâmetros e ciclo antes do desenho confirmados | Medir taxa efetiva, descontos, chegada completa, ocupação e visão |
| Combate | Aritmética parcial de dano, consulta de proximidade e cura confirmadas | Alvos, alcance, cadência, tecnologias e efeitos de morte |
| Economia | Custos e blocos de recursos | Associar IDs internos, produção, consumo e filas |
| Construções | Primeiro bloco indexado do ETA | Identificar tipos, campos, posição e estados |
| Instâncias de unidades | Dono, coordenadas, vida e cópia disco→RAM confirmados | Completar ordens, significado dos estados e campos derivados |
| Campanha | Blocos variáveis e textos de missões | Decifrar condições, eventos e vitória/derrota |
| Sufixo ETA | Tamanho constante e hashes por mapa | Mapear as camadas restantes e seus consumidores |
| Névoa e sprites | Referências no renderizador | Reproduzir composição, visibilidade e animação |
| Som, vídeo e rede | Imports DirectSound, MCI e DirectPlay | Identificar formatos, fluxos e protocolos |
| Salvamento | Caminhos adjacentes de leitura | Comparar formato de campanha com snapshots de partida |

## Próxima investigação recomendada

Prosseguir a partir de [CAMINHOS.md](CAMINHOS.md) e [IA.md](IA.md).
A preparação é `0x43b30b`; o solucionador principal é `0x42f214`, seguido de
`0x42e890`. A bancada já executa esses trechos, mas a tradução independente
continua parcial. Integrar a escolha direta, o desvio e o consumo da rota.
Para a IA, seguir a inicialização da tabela de operações `0x514910` e recuperar
uma tarefa completa. Ainda é necessário medir a taxa efetiva do ciclo identificado
em [CADENCIA.md](CADENCIA.md).
Uma execução controlada do jogo poderá confrontar movimento, visibilidade e
combate numa partida. Ainda não há runtime Windows preparado nem validação
de gameplay integrado. Os testes atuais emulam instruções isoladas.

## Como registrar uma nova descoberta

Para cada campo ou rotina, registrar o hash do binário, endereço ou offset,
instrução que sustenta a interpretação, exemplos do corpus e nível de certeza.
Adicionar teste quando houver uma propriedade observável independente. Para
hipóteses, conservar o nome neutro dos dados até encontrar evidência suficiente.

O CD e o protótipo externo não precisam ser alterados para continuar a pesquisa.
Esta etapa não aplicou correções a esses arquivos. Também não configurou remoto
Git nem publicou os resultados.
