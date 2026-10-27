# Mapa de rotinas e evidências

Endereços virtuais para a base preferencial `0x00400000` do executável cujo hash
está no relatório de análise e no manifesto. Nomes atribuídos pela pesquisa; não são símbolos
originais. Os trechos da raiz de `evidencias` incluem bytes, permitindo conferir
alinhamento. As exportações em `evidencias/ghidra` contêm endereços e instruções.

| Endereço | Nome atribuído / observação | Evidência |
|---|---|---|
| `0x4186ba` | Carregar um banco CMP | [ASM](../evidencias/carregador_cmp.asm) |
| `0x41877a` | Agregar seis bancos CMP | [ASM](../evidencias/agregador_cmp.asm) |
| `0x41068e` | Desenhar região de terreno | [ASM](../evidencias/entrada_render_terreno.asm) |
| `0x474b08` | Preparar telas usando a origem da visualização | [ASM](../evidencias/origem_visualizacao.asm) |
| `0x45c779` | Compor quadro comprimido sobre outro destino | [ASM](../evidencias/composicao_cmp.asm) |
| `0x441792` | Ler linha da matriz de danos do INI | [ASM](../evidencias/carregador_danos.asm) |
| `0x44188b` | Carregar atributos dos 26 tipos | [ASM](../evidencias/carregador_atributos.asm) |
| `0x441a1b` | Alocar estruturas e chamar carregadores de unidades | [ASM](../evidencias/alocacao_unidades.asm) |
| `0x458420` | Abrir arquivo usando handle global | [ASM](../evidencias/leitura_arquivo.asm) |
| `0x45844c` | Fechar arquivo global | [ASM](../evidencias/leitura_arquivo.asm) |
| `0x458461` | Ler bytes no destino EAX, tamanho EDX | [ASM](../evidencias/leitura_arquivo.asm) |
| `0x45848b` | Reposicionar arquivo, deslocamento EAX, origem DL | [ASM](../evidencias/leitura_arquivo.asm) |
| `0x46c2cf` | Carregar mapa de campanha e inicializar estado | [ASM](../evidencias/carregador_mapa.asm) |
| `0x46799c` | Atribuir valor a registro de recurso | [ASM](../evidencias/atribuir_recurso.asm) |
| `0x46acbf` | Ler unidades do ETA e executar pós-processamento | [ASM](../evidencias/carregador_unidades_eta.asm) |
| `0x47534a` | Ler quantidade e registros de quatro bytes | [ASM](../evidencias/tabela_47534a.asm) |
| `0x47c24d` | Ler tabela com registros de tamanho indicado | [ASM](../evidencias/tabela_47c24d.asm) |
| `0x47bcc7` | Ler pares de dois e quatro bytes | [ASM](../evidencias/tabela_47bcc7.asm) |
| `0x47c04a` | Ler tabela com passo de dez bytes em RAM | [ASM](../evidencias/tabela_47c04a.asm) |
| `0x458b05` | Ler dez registros no corpus observado | [ASM](../evidencias/tabela_458b05.asm) |
| `0x47c30f` | Ler e descartar 16 bytes | [ASM](../evidencias/descartar_bytes_eta.asm) |
| `0x47c404` | Ler quatro listas com cem entradas de três bytes | [ASM](../evidencias/listas_jogadores_eta.asm) |
| `0x47ac30` | Ler e ajustar tabela final antes do fechamento | [ASM](../evidencias/tabela_47ac30.asm) |
| `0x477042` | Direção entre duas células | [ASM](../evidencias/direcao_entre_celulas.asm) |
| `0x4770ee` | Vizinho com verificação de bordas | [ASM](../evidencias/celula_vizinha.asm) |
| `0x479555` | Distância quadrática de coordenadas u16 | [ASM](../evidencias/distancia_quadratica.asm) |
| `0x448599` | Giro entre 16 orientações | [ASM](../evidencias/orientacao_unidade.asm) |
| `0x448704` | Integrar deslocamento, progresso e chegada | [ASM do prefixo](../evidencias/inicio_passo_unidade.asm) |
| `0x457122` | Acrescentar vida e limitar ao máximo do tipo | [ASM](../evidencias/cura_unidade.asm) |
| `0x428cc0` | Consultar modificador por dono, tipo e código | [ASM](../evidencias/consulta_modificador.asm) |
| `0x457350` | Inicializar parâmetros da instância conforme tipo | [Ghidra](../evidencias/ghidra/00457350.asm) |
| `0x4502f0` | Aplicar modalidades de dano; reconstrução parcial | [Ghidra](../evidencias/ghidra/004502f0.asm) |
| `0x4500e4` | Procurar unidade do mesmo dono dentro de raio | [Ghidra](../evidencias/ghidra/004500e4.asm) |

## Convenções e limites da desmontagem

O Capstone traduz instruções, mas não recupera automaticamente os tipos e a
semântica do programa. A varredura linear das seções executáveis pode encontrar
dados embutidos. `referencias_candidatas` em `executavel.json` é uma lista de
pistas; não é um grafo completo e validado de chamadas.

Os trechos são selecionados. Alguns incluem saltos para epílogos compartilhados
fora do intervalo exportado; não devem ser apresentados como funções C completas.
O carregador de atributos, por exemplo, sai para `0x44ea60`. A documentação de
campos resulta das instruções presentes, não de uma assinatura C presumida.

## Continuar no Ghidra

O Ghidra oferece descompilação, grafos, referências e automação, conforme seu
[repositório oficial](https://github.com/NationalSecurityAgency/ghidra).
Ele foi instalado em `.local/` e utilizado para analisar a cópia normalizada
do PE, com projeto, configurações e logs dentro do repositório.

Para usar os resultados desta etapa:

1. Consultar [GHIDRA.md](GHIDRA.md) e executar `python3 ghidra/analisar.py`.
2. Abrir com `python3 ghidra/executar.py gui ghidra/projetos/RisingLands.gpr`.
3. Selecionar `RISING-analise.exe` e navegar até os endereços desta tabela.
4. Conferir limites de funções, saltos para epílogos comuns e tabelas embutidas.
5. Atribuir os nomes portugueses, comentários e estruturas recuperadas.
6. Conferir convenções de chamada por registradores antes de confiar nas
   assinaturas sugeridas pelo descompilador.
7. Exportar pseudocódigo com a versão do Ghidra e o hash de entrada registrados.

O pseudocódigo produzido por um descompilador continua sendo uma reconstrução.
Tipos, argumentos e laços precisam ser confrontados com o assembly e com testes.
