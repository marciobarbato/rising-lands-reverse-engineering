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
- 46 testes aprovados, incluindo 10.736 execuções na bancada, sem iniciar o jogo.

## Questões em aberto

| Tema | Evidência disponível | Trabalho necessário |
|---|---|---|
| Caminhos e colisão | Grade de atributos, protótipo com A* | Localizar o algoritmo original e decifrar bits de terreno |
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

Medir a taxa efetiva do ciclo identificado em [CADENCIA.md](CADENCIA.md).
Completar os efeitos de chegada em `0x448704` e a busca de caminho
em `0x43b30b`. No combate, seguir o preenchimento da tabela de modificadores
`0x4dfba0` e a grade `0x4e0f38`, que afeta o bônus de proximidade.

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
