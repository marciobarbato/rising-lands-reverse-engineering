# Prompts para chats paralelos

Cada bloco pode ser copiado para um chat separado. O chat principal continua
responsável por caminhos/movimento, revisão das integrações e commits do
repositório. As pastas exclusivas evitam conflitos nos arquivos e no índice Git.

## Economia

```text
Continue a engenharia reversa de Rising Lands, priorizando consulta, crédito
e débito dos recursos dos jogadores.

Repositório: /Users/marcio/git/Rising Lands/engenharia-reversa
Sua pasta exclusiva:
/Users/marcio/git/Rising Lands/engenharia-reversa/pesquisas-paralelas/economia

Leia a documentação e o código existentes. Outro chat cuida dos caminhos,
contornos e movimento; não trabalhe nesses subsistemas.

Crie ou altere arquivos somente na sua pasta exclusiva. Não altere documentos,
relatórios, configurações ou código fora dela. Não faça operações Git que
alterem arquivos, branches ou índice; os commits ficam com o chat principal.
Use os arquivos originais somente para leitura. Se usar Ghidra, crie um projeto
próprio na sua pasta; não abra o projeto compartilhado.

Traduza rotinas identificadas para Python, documente em português e compare
com o x86 original quando possível. Separe evidência confirmada de hipótese.
Ao terminar, informe arquivos, endereços, testes, limitações e integração.
```

## Combate

```text
Continue a engenharia reversa de Rising Lands, investigando seleção de alvos,
verificações de distância/alcance e condições para iniciar ou manter ataques.

Repositório: /Users/marcio/git/Rising Lands/engenharia-reversa
Sua pasta exclusiva:
/Users/marcio/git/Rising Lands/engenharia-reversa/pesquisas-paralelas/combate

Leia a documentação e as implementações existentes para evitar duplicar a
aritmética de dano já reconstruída. Outros chats cuidam dos caminhos/movimento
e da economia; não trabalhe nesses subsistemas.

Crie ou altere arquivos somente na sua pasta exclusiva. Não altere documentos,
relatórios, configurações ou código fora dela. Não faça operações Git que
alterem arquivos, branches ou índice; os commits ficam com o chat principal.
Use os arquivos originais somente para leitura. Se usar Ghidra, crie um projeto
próprio na sua pasta; não abra o projeto compartilhado.

Traduza rotinas identificadas para Python, documente em português e compare
com o x86 original quando possível. Distinga fatos confirmados de hipóteses.
Mantenha as rotinas independentes, sem integrar ao movimento ou à economia.
Ao terminar, informe arquivos, endereços, testes, limitações e integração.
```

## Aplicativo de acompanhamento no Mac M4

```text
Crie um aplicativo executável no macOS Apple Silicon para acompanhar
visualmente o estado da engenharia reversa de Rising Lands.

Repositório: /Users/marcio/git/Rising Lands/engenharia-reversa
Sua pasta exclusiva:
/Users/marcio/git/Rising Lands/engenharia-reversa/pesquisas-paralelas/visualizador-mac

Outros chats pesquisam caminhos/movimento, economia e combate. Não altere
arquivos deles ou arquivos principais do repositório. Não faça operações
Git que alterem arquivos, branches ou índice.

Entregue dist/RisingLands-Preview.app dentro da sua pasta exclusiva.
Quero abrir o aplicativo no Mac M4 e acompanhar os recursos reconstruídos.

Requisitos:
- Janela com mapa, unidades e obstáculos. Use gráficos originais quando os
  extratores existentes permitirem; identifique representações provisórias.
- Seleção de unidade e emissão de ordens de movimento.
- Exibição de rota, destino, posição, colisões e estado da unidade.
- Pausar, continuar, avançar uma atualização e ajustar velocidade.
- Economia/combate somente quando houver implementações verificadas das
  pesquisas paralelas. Identifique recursos disponíveis, experimentais e pendentes.
- Priorize o backend SolucionadorCaminhosPython documentado em CONTORNOS.md.
  Identifique dependências de x86/Unicorn e não invente sucesso de funções ausentes.
- Mostre o commit principal e a procedência das pesquisas utilizadas.

Use snapshots da versão commitada do principal e das pesquisas concluídas.
Não importe arquivos ainda sendo editados pelos outros chats. Registre hashes
e procedência de cada snapshot. Crie adaptadores locais, sem mudar o principal.
Use os arquivos originais do jogo somente para leitura.

Mantenha código, dependências, temporários, snapshots e builds na sua pasta.
Forneça um comando simples para atualizar os snapshots, testar e reconstruir
o aplicativo, com instruções em português.

Execute o build e teste a abertura no Mac, preservando as proteções do macOS.
Se uma etapa depender de uma ação minha, conclua as demais e explique qual.
A demonstração deve refletir o estado real da reconstrução, distinguindo
comportamentos confirmados de elementos apenas visuais.
```

Antes de incorporar uma pesquisa ao principal, conferir suas evidências e testes.
Um snapshot do visualizador não deve publicar código em edição nem modificar os
arquivos do jogo original.
