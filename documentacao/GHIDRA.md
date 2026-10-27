# Ghidra: instalação e análise reproduzível

O Ghidra 12.2 está instalado em `.local/ghidra_12.2_PUBLIC`, com JDK Temurin
25.0.5+8 ARM64 em `.local/jdk-25.0.5+8`. Ambos ficam dentro deste repositório.
Projetos, configurações, logs, caches e temporários também são locais. Os pacotes
grandes e o projeto binário são ignorados pelo Git; scripts e evidências são versionados.

As URLs oficiais e os SHA-256 verificados estão em
[`ghidra/instalacao.json`](../ghidra/instalacao.json). O instalador foi preparado
para este Mac Apple Silicon. Como o pacote não incluía o descompilador nativo
macOS ARM64, ele foi compilado com `clang++` a partir do código incluído na distribuição.
Não foi necessário instalar componentes globais.

```sh
python3 ghidra/instalar.py
python3 ghidra/analisar.py
python3 ghidra/executar.py gui ghidra/projetos/RisingLands.gpr
```

O último comando abre a interface gráfica. A análise automatizada usa o modo
headless e não depende de abrir uma janela. O instalador exige as ferramentas
de compilação do Xcode já disponíveis na máquina. Não executa o jogo.

## Particularidade do executável Watcom

As seis seções PE do original informam `VirtualSize=0`. A primeira importação
gerou erros `Invalid file index` ao resolver imports, recursos e relocações.
`ghidra/preparar_entrada.py` cria uma cópia exclusivamente para análise e preenche
esses seis campos com `SizeOfRawData`, preservando todos os outros bytes.
São oito bytes diferentes no total, dentro dos seis campos de quatro bytes.

| Arquivo | SHA-256 |
|---|---|
| Original, somente leitura | `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb` |
| Cópia normalizada | `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0` |

O manifesto [`entrada.json`](../ghidra/entrada.json) enumera os offsets alterados.
O script rejeita versões diferentes do original. Código, dados, endereços e
comprimento são preservados. A cópia não é uma correção para jogar e não deve
ser usada para execução. O projeto atual conserva também a primeira importação;
a pesquisa utiliza `RISING-analise.exe`.

## Resultados e limites

- 255 rotinas relacionadas à tabela de unidades e suas auxiliares exportadas em C e assembly.
- Índice de todas as funções reconhecidas e referências à tabela em TSV.
- Estrutura parcial de instância com 276 bytes aplicada no projeto.
- Sete acessores recebem assinaturas explícitas com argumento em `AX` e retorno
  em `AL` ou `AX`, conforme as instruções reais.

Os resultados ficam em [`evidencias/ghidra`](../evidencias/ghidra). `OK` no índice
de exportação significa que o descompilador produziu texto, não que o texto
esteja semanticamente correto. As demais assinaturas continuam automáticas:
o compilador Watcom utiliza argumentos por registradores e compartilha epílogos
entre funções, o que confunde parte da análise. O assembly decide a interpretação.

O projeto usa a arquitetura `x86:LE:32:default` e o perfil `windows`, porque não
há perfil Watcom entre os perfis disponíveis nessa instalação. **Isso não é
evidência de compilação com Visual C++.** A identificação é a string do runtime
`WATCOM C/C++32` no próprio EXE. Ela aponta para C e/ou C++; a distinção exata
e os nomes originais do código-fonte não foram recuperados.

## Símbolos franceses originais

`python3 ferramentas/extrair_ia.py` gera `relatorios/simbolos-originais.tsv`.
O script `ImportarSimbolosOriginais.java` importa os 1.995 registros no namespace
`OriginaisSBL`, conferindo o hash da cópia normalizada. Execução:

```sh
python3 ghidra/executar.py headless ghidra/projetos RisingLands \
  -process RISING-analise.exe -noanalysis -scriptPath ghidra/scripts \
  -postScript ImportarSimbolosOriginais.java relatorios/simbolos-originais.tsv evidencias/simbolos-importados.tsv
```

Endereços adicionais depois do relatório solicitam criação de funções ainda
não reconhecidas. As 14 rotinas selecionadas da etapa de tarefas foram exportadas
em `evidencias/operacoes-ia/`, incluindo `V_Attendre` e operações aritméticas.
O nome original não elimina a necessidade de corrigir assinaturas por registradores.
Ver [SIMBOLOS.md](SIMBOLOS.md) para o formato e as duplicidades da tabela.
