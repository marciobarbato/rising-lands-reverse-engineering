# Validação do primeiro marco

Snapshot `1c8ebdd43b0a820652b7cb852ae1fe218d4dea5e`. Executável brasileiro
SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Os resultados desta revisão estão em `validacao/python.json`, `x86.json` e
`visual.json`. Evidências extraídas diretamente do EXE têm bytes e endereços em
`evidencias/`; o manifesto de trechos também identifica os intervalos e hashes.

## Testes Python

Comando na área editável: `python3 -B validar_python.py`.
**20 testes**, sem importar Unicorn ou executar instruções x86 nesse comando.
Os testes de regressão utilizam como oráculo o resultado x86 já registrado,
portanto distinguem-se da geração desse resultado.

- Integridade dos 942 arquivos do snapshot e das fontes do jogo/referência.
- Ponteiros dos bancos e saltos por tipo extraídos do PE com hash conferido.
- Identidade tipo 0 → `SOLDAT` no EXE → `SOLDADO` no INI.
- Hash dos intervalos e bytes de cada instrução nas 41 evidências extraídas.
- Índices nos limites dos seis bancos; rejeição de IDs fora do agregado.
- Decodificação dos **12.268 quadros dos oito CMP** contra o leitor commitado,
  importado somente do snapshot privado. Igualdade de dimensões e pixels.
- Literal zero opaco, pulos transparentes, truncamentos e comandos inválidos.
- 144 associações contra as capturas originais e integridade de CSV/JSON.
- Oito quadros de parada, oito fases, pareamento das 16 orientações.
- Sequência, igualdade do contador com o período e overflow de oito bits.
- Posicionamento com deslocamentos assinados; 75 hashes de superfícies x86.
- Três registros Soldado do ETA original, offsets e SHA-256 por registro.
- PNG RGBA, atlas e 64 imagens incorporadas no HTML sem script externo.
- Tipos/estados sem comprovação produzem erro, não mapeamento aproximado.

Dentro da entrega congelada, executar somente `python3 -B -m unittest -v
test_graficos`, que não regrava relatórios. Os geradores recusam escrever em
uma pasta cujo pai seja `entregas`.

## Comparações x86/Unicorn

Comando executado na área editável: `python3 -B -u validar_x86.py`.
**4.814 execuções delimitadas**, **1.254.037 instruções observadas**;
resultado **PASSOU**. Tempo observado da execução registrada: 2,406 s.
Esse tempo pertence à bancada, não à animação do jogo.

| Objeto | Comparação | Substituições / limite da conclusão |
|---|---|---|
| Agregador `0x41877a` | 12.156 descritores: ordem, largura, altura, tamanho e cada byte comprimido | Abrir/ler/fechar arquivos e alocador substituídos; os nomes e bytes vêm das cópias conferidas |
| `SetBank` `0x418590` | Vetor resultante passa ao global `0x508f6c` | Original executado |
| Inicialização tipo 0 `0x457350` | Quantidade 8 e período 2 | Original executado, registro sintético |
| Parada `0x448194` | Oito fases de entrada resultam em fase 2 e retorno verdadeiro | Nenhuma chamada substituída |
| Desenho `0x41591f` → `0x412390` → `0x411147` | 144 casos: 16 orientações, oito fases em estado 2 e fase 2 em estado 7; ID capturado na entrada de `PasteBobCmp` | A chamada de sombra é interceptada e seus argumentos registrados; o corpo, getters e testes de flags executam código original |
| Ancoragem | Sete pares de deslocamento, incluindo −128 e +127; offsets −40/−22 | Mesmo caminho de captura; jogador 0, sem efeitos especiais |
| Contadores | 4.416 casos em `0x448088` e no prefixo de `0x448f50`; todos os contadores 0..255 para período 2, mais bordas de períodos 0/1/3/255 | Sem stubs; passo já preparado no registro; para antes do giro/avanço físico |
| Sem próximo passo | Registro preservado ao retornar pelo caminho curto | Não executa preparação de rota |
| Direções | Oito deltas de célula em `0x477042` | Nenhum stub |
| Blitter `0x45b247` | 64 quadros completos, 11 recortes/posições de borda e um CMP sintético: **76 casos** | Código original de cópia executado integralmente; superfície sintética indexada; sem DirectDraw |

`x86.json` registra todas as 144 capturas e seus argumentos, os 75 hashes de
superfícies reais e as substituições. O caso sintético adicional prova que
literal zero copia preto/índice zero, enquanto um salto preserva o fundo.

A bancada verifica o hash **antes** de construir a imagem executável. Não
inicia o PE nem resolve APIs Windows. Cada chamada declara os intervalos de
código permitidos e precisa alcançar uma parada explícita; máximo de
1.000.000 de instruções e 2.000.000 µs por chamada. Qualquer endereço externo,
divergência, timeout ou acesso inválido falha o comando. Usa memória e processo
próprios; não acessa ambientes ou processos das outras frentes.

Somente `Bancada` em `bancada_x86.py` e `validar_x86.py` dependem de Unicorn.
Capstone é usado por `extrair_evidencias.py` na desmontagem. Não há dependência
x86 na consulta, nos atlas, na composição Python nem no HTML entregue.

## Verificação visual

Foi inspecionado o atlas, ajustando as células para conter o máximo de 84×67
pixels ampliado 2×. O HTML foi aberto em navegador e testado pela interface:
parada direção 1 / ID 2084; direção 9, duas chamadas, fase 3 / ID 2117;
orientação 16, fase 7, duas chamadas, fase 0 / ID 2138; retorno à parada.
A captura está em `artefatos/demo-verificada.png`.

O primeiro servidor falhou no sandbox com `PermissionError` no bind; isso não
foi interpretado como porta ocupada. Uma solicitação de execução fora do
sandbox foi aprovada pelo fluxo da ferramenta; o servidor próprio em
127.0.0.1:8879 então iniciou e a página respondeu HTTP 200. Foi encerrado pelo
controle da própria sessão após a inspeção. Nenhuma aprovação humana está
pendente e o HTML entregue não requer servidor.

Unicorn também terminou com SIGILL ao criar a CPU dentro do sandbox. As
comparações registradas foram executadas após aprovação pelo fluxo da
ferramenta. Essas tentativas que falharam não foram contabilizadas como testes
passando. Nenhum comando negado foi tratado como sucesso.

## O que os testes não provam

- Execução completa de uma missão ou taxa original em segundos.
- Estado final de toda a RAM após carregar ETA.
- Encadeamento completo da simulação: a transição superior estado 2→7 foi
  lida no assembly commitado, sem emular todo `EnginNextEtape`.
- Desenho final da sombra, efeitos especiais, paletas por jogador e DirectDraw.
- Outros tipos, construções, objetos, HUD, minimapa e ordenação completa da cena.
- Semântica de ataque, dano ou escolha do alvo.

A demonstração separa os controles didáticos das regras confirmadas. A imagem
enviada pelo usuário permanece apenas referência de aparência.
