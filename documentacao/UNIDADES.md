# Reconstrução do carregador de unidades

Implementação: [regras.py](../ferramentas/regras.py). Evidência:
[carregador_atributos.asm](../evidencias/carregador_atributos.asm) e
[carregador_danos.asm](../evidencias/carregador_danos.asm).

## Tipos em memória

São 26 registros de `0x32` (50) bytes a partir de `0x4965ae`. Essa tabela contém
atributos por **tipo**, não o estado de cada unidade no mapa. A tabela de
instâncias usa registros separados com passo `0x114` (276) bytes.

| Offset no tipo | Tipo | Significado | Padrão ao ler INI |
|---|---|---|---:|
| `0x00` | `u16` | Tempo de recrutamento, `TMPSRECRUTE` | 120 |
| `0x02` | `u16` | Custo de comida, `COUTPATATE` | 1 |
| `0x04` | `u16` | Custo de peças, `COUTPIECE` | 1 |
| `0x06` | `u16` | Custo de pedra, `COUTROCHE` | 1 |
| `0x08` | `u16` | Vida máxima, preservada; 100 nos 26 tipos originais | — |
| `0x0a` | 1 byte | Campo anterior preservado; sem semântica atribuída | — |
| `0x0b` | `u8` | Blindagem, `BLINDAGE` | 5 |
| `0x0c` | `char[30]` | Seção francesa antes da carga; nome localizado depois | Nome anterior |
| `0x2a` | `u16` | Raio de visão, `RAYON` | 5 |
| `0x2c` | `u16` | **Quadrado** do alcance `PORTEE` | `1²` |
| `0x2e` | `u16` | Fadiga, `FATIGUE` | 3.000 |
| `0x30` | `u16` | Recarga, `RECHARGE` | 100 |

O arquivo INI normalmente fornece os valores, substituindo os padrões. O
extrator preserva ambos os aspectos: usa os padrões recuperados nas entradas
ausentes e armazena os valores originais do INI no JSON.

As instruções `MOV ... AL` e `MOV ... AX` truncam para 8 e 16 bits. O alcance é
multiplicado e o resultado armazenado em 16 bits. A reconstrução replica isso;
não interpreta o overflow como uma regra de design desejada.

## Pseudocódigo explicativo em português

Este trecho resume a lógica observada; nomes e tipos são reconstruídos.

```c
bonus_capitao = ler_inteiro_ini("DIVERS", "BONUSCAPITAINE", 2);
carregar_linha_de_danos(26, "MINE");

for (id_tipo = 0; id_tipo < 26; ++id_tipo) {
    tipo = base_tipos + id_tipo * 50;
    secao = tipo->nome;  // Francês, embutido no EXE antes da carga.
    carregar_linha_de_danos(id_tipo, secao);

    tipo->blindagem = (uint8_t)ler_inteiro_ini(secao, "BLINDAGE", 5);
    tipo->raio_visao = (uint16_t)ler_inteiro_ini(secao, "RAYON", 5);
    alcance = ler_inteiro_ini(secao, "PORTEE", 1);
    tipo->alcance_quadrado = (uint16_t)(alcance * alcance);
    tipo->fadiga = (uint16_t)ler_inteiro_ini(secao, "FATIGUE", 3000);
    tipo->recarga = (uint16_t)ler_inteiro_ini(secao, "RECHARGE", 100);
    tipo->recrutamento = (uint16_t)ler_inteiro_ini(secao, "TMPSRECRUTE", 120);
    tipo->comida = (uint16_t)ler_inteiro_ini(secao, "COUTPATATE", 1);
    tipo->pedra = (uint16_t)ler_inteiro_ini(secao, "COUTROCHE", 1);
    tipo->pecas = (uint16_t)ler_inteiro_ini(secao, "COUTPIECE", 1);
    ler_nome_ini(secao, "NAME", tipo->nome, 30);
}
```

`ler_nome_ini` representa `GetPrivateProfileStringA`, com capacidade para 29
bytes mais NUL. A implementação independente mantém bytes posteriores ao NUL
quando já existiam; eles não fazem parte do nome visível.

## Matriz de danos

A alocação em `0x441a1b` cria 27 ponteiros, cada um para 27 bytes. Os tipos 0..25
usam as seções francesas da tabela. A linha 26 é carregada da seção `MINE`.
Cada linha vem de uma lista de inteiros separados por vírgulas, chave `DEGAT`.

A ordem das primeiras 26 colunas coincide com a ordem dos tipos embutidos no
EXE, que também é descrita nos comentários do INI. A coluna 26 é indicada ali
como dano a construções (`Batiment`). O rótulo dessa coluna é apoiado pelo
comentário do arquivo; a aplicação final de dano a uma construção não foi
descompilada nesta etapa.

| Exemplo | Valor recuperado |
|---|---:|
| Soldado: comida | 6 |
| Soldado: tempo de recrutamento | 800 unidades internas |
| Soldado contra soldado | 20 na matriz de entrada |
| Soldado contra construção | 2 na matriz de entrada |
| Capitão: alcance do INI | 8 |
| Capitão: alcance armazenado | 64 |
| Bônus do capitão | 2; aplicação ainda não reconstruída |

Não se deve deduzir que dano seja simplesmente `matriz - blindagem`, nem que
recrutamento 800 corresponda a 800 ms ou a uma quantidade conhecida de segundos.
Essas conversões exigem seguir as rotinas consumidoras.

## Resultado utilizável

[unidades.json](../relatorios/unidades.json) contém nomes, IDs, atributos,
matriz de dano e bytes reconstruídos dos registros de tipos. O campo
`registro_memoria_hex` é o resultado da reconstrução estática, não uma captura
de memória de uma execução do jogo. O [catálogo](../relatorios/UNIDADES.md)
oferece uma leitura compacta em português.

O estado individual de dono, posição, vida e carga está descrito em
[INSTANCIAS.md](INSTANCIAS.md), incluindo a distinção entre disco e memória.
