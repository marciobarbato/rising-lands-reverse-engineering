# Estado da pesquisa e continuidade

## Concluído nesta etapa

- Repositório Git independente em `Rising Lands/engenharia-reversa`.
- Inventário e identificação do executável local.
- Vinte trechos x86 exportados com bytes e anotações.
- Leitores CMP e ETA independentes, em português, com validação de limites.
- Sequência de carregamento dos 38 mapas reconciliada com o código original.
- Carregador dos atributos dos tipos reconstruído e matrizes de dano extraídas.
- Renderização estática do terreno da missão 1 com IDs corrigidos.
- Testes sintéticos e contra o corpus real.
- Ghidra e JDK portáteis instalados, com descompilador nativo ARM64 compilado.
- 250 rotinas exportadas e sete assinaturas de acessores corrigidas.
- Propriedade, coordenadas, vida e campos de carga das 2.604 entradas de unidades.
- Rotina de cura reconstruída e máximo de vida localizado na tabela de tipos.

## Questões em aberto

| Tema | Evidência disponível | Trabalho necessário |
|---|---|---|
| Caminhos e colisão | Grade de atributos, protótipo com A* | Localizar o algoritmo original e decifrar bits de terreno |
| Movimento e tempo | Imports de relógio e atributos de unidades | Rastrear passo de simulação e atualização de posição |
| Combate | Matriz, blindagem, alcance quadrático | Seguir cálculo de dano, seleção de alvo, bônus e morte |
| Economia | Custos e blocos de recursos | Associar IDs internos, produção, consumo e filas |
| Construções | Primeiro bloco indexado do ETA | Identificar tipos, campos, posição e estados |
| Instâncias de unidades | Dono, coordenadas, vida e cópia disco→RAM confirmados | Completar ordens, significado dos estados e campos derivados |
| Campanha | Blocos variáveis e textos de missões | Decifrar condições, eventos e vitória/derrota |
| Sufixo ETA | Tamanho constante e hashes por mapa | Mapear as camadas restantes e seus consumidores |
| Névoa e sprites | Referências no renderizador | Reproduzir composição, visibilidade e animação |
| Som, vídeo e rede | Imports DirectSound, MCI e DirectPlay | Identificar formatos, fluxos e protocolos |
| Salvamento | Caminhos adjacentes de leitura | Comparar formato de campanha com snapshots de partida |

## Próxima investigação recomendada

Rastrear o movimento a partir de `0x448f50`, a integração do passo em `0x448704`
e a orientação em `0x448599`. As posições reais da primeira missão já permitem
substituir coordenadas inventadas em uma futura reimplementação independente.
Também seguir o dano em `0x4502f0`, distinguindo os modos e modificadores.
A conversão dos contadores para segundos depende do relógio da simulação.

## Como registrar uma nova descoberta

Para cada campo ou rotina, registrar o hash do binário, endereço ou offset,
instrução que sustenta a interpretação, exemplos do corpus e nível de certeza.
Adicionar teste quando houver uma propriedade observável independente. Para
hipóteses, conservar o nome neutro dos dados até encontrar evidência suficiente.

O CD e o protótipo externo não precisam ser alterados para continuar a pesquisa.
Esta etapa não aplicou correções a esses arquivos. Também não configurou remoto
Git nem publicou os resultados.
