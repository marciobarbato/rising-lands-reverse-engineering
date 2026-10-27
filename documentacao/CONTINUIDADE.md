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

## Questões em aberto

| Tema | Evidência disponível | Trabalho necessário |
|---|---|---|
| Caminhos e colisão | Grade de atributos, protótipo com A* | Localizar o algoritmo original e decifrar bits de terreno |
| Movimento e tempo | Imports de relógio e atributos de unidades | Rastrear passo de simulação e atualização de posição |
| Combate | Matriz, blindagem, alcance quadrático | Seguir cálculo de dano, seleção de alvo, bônus e morte |
| Economia | Custos e blocos de recursos | Associar IDs internos, produção, consumo e filas |
| Construções | Primeiro bloco indexado do ETA | Identificar tipos, campos, posição e estados |
| Instâncias de unidades | Tipo no byte 1 e cópia disco→RAM | Identificar dono, coordenadas, vida, ordens e campos derivados |
| Campanha | Blocos variáveis e textos de missões | Decifrar condições, eventos e vitória/derrota |
| Sufixo ETA | Tamanho constante e hashes por mapa | Mapear as camadas restantes e seus consumidores |
| Névoa e sprites | Referências no renderizador | Reproduzir composição, visibilidade e animação |
| Som, vídeo e rede | Imports DirectSound, MCI e DirectPlay | Identificar formatos, fluxos e protocolos |
| Salvamento | Caminhos adjacentes de leitura | Comparar formato de campanha com snapshots de partida |

## Próxima investigação recomendada

O passo de maior utilidade é identificar posição e propriedade dos registros
de unidades. A missão 1 já oferece 16 entradas para comparar com uma execução
controlada do jogo. Isso permitirá substituir a posição de soldado inventada
no protótipo por entidades efetivamente recuperadas.

Depois, rastrear o movimento e o relógio da simulação, medindo a mesma ordem de
movimento no original. Só então calibrar velocidade, animações e busca de caminho.
O Ghidra pode ajudar a navegar essas chamadas e produzir pseudocódigo inicial.

## Como registrar uma nova descoberta

Para cada campo ou rotina, registrar o hash do binário, endereço ou offset,
instrução que sustenta a interpretação, exemplos do corpus e nível de certeza.
Adicionar teste quando houver uma propriedade observável independente. Para
hipóteses, conservar o nome neutro dos dados até encontrar evidência suficiente.

O CD e o protótipo externo não precisam ser alterados para continuar a pesquisa.
Esta etapa não aplicou correções a esses arquivos. Também não configurou remoto
Git nem publicou os resultados.
