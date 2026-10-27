# Entrega ao chat principal

Esta pasta é autônoma. Nenhum arquivo compartilhado foi alterado e nenhum
projeto Ghidra foi aberto/criado. Os commits autorizados no `main` se limitam
a esta pasta e preservam os arquivos e o índice dos demais chats.
Os comandos de teste usam `-B` e o código de validação desabilita bytecode para
não criar caches nos módulos compartilhados lidos pela pesquisa.

## Como incorporar

1. Revisar [README.md](README.md), os ASM e o relatório com 84 testes aprovados
   e 13.858 execuções x86 (incluindo 40 exceções e três limites esperados).
   Executar `validar.py --emular` se houver Unicorn/JIT.
2. Incorporar `economia.py` em `ferramentas/` ou manter a pesquisa como módulo
   independente. O código de produção depende só da biblioteca padrão.
   `bancada_economia.py` e os testes usam caminhos relativos à pasta atual;
   adaptar `PASTA` ao movê-los. Nenhuma promoção de arquivos foi feita aqui.
3. Conectar a carga existente com
   `Economia.de_recursos_eta(eta['recursos_por_tipo'])`. Para importar memória
   já existente/salva, usar `Economia(bloco_de_128_bytes)`; o construtor copia
   os bytes. O estado atualizado está em `economia.memoria`.
4. Usar `Recurso.COMIDA`, `Recurso.PEDRA`, `Recurso.PECAS` nos débitos/créditos.
   Os métodos recebem `(jogador, recurso, quantidade)`, nessa ordem Python.
   A convenção x86 é AL=recurso, DX=quantidade, BX=jogador.
5. Passar custos de unidade por `custos_unidade(registro_de_50_bytes)` e testar
   `e.suficiente(jogador, custos.comida, custos.pedra, custos.pecas)` antes de
   autorizar uma compra. Não converter os débitos isolados em uma transação que
   rejeita insuficiência sem distinguir essa nova política do comportamento original.
6. Ao ligar as operações RUL, preservar a ordem dos índices da IA:
   0=comida, 1=pedra, 2=peças. Ela difere dos IDs das mutações.
   `B_Test*` retorna 1/-1, e seu limiar é signed32.
7. Usar `recurso_necessario` apenas para reproduzir o helper original:
   retorno 0 também ocorre quando só faltam peças. Não usar como substituto
   de `suficiente`. Os wrappers de custo usam índices válidos 0..2.

Exemplo de uso após disponibilizar o módulo no caminho de importação:

```python
from economia import Economia, Recurso, custos_unidade

e = Economia.de_recursos_eta(eta['recursos_por_tipo'])
custos = custos_unidade(registro_tipo)
if e.suficiente(jogador, custos.comida, custos.pedra, custos.pecas):
    e.debitar(jogador, Recurso.COMIDA, custos.comida)
    e.debitar(jogador, Recurso.PEDRA, custos.pedra)
    e.debitar(jogador, Recurso.PECAS, custos.pecas)
```

O exemplo só reproduz teste e débitos; a criação/inicialização da unidade e a
fila da construção exigem o restante de InitRecruteTroupe. Crédito direto via
`e.creditar` reproduz a primitiva. O depósito com capacidade agora usa
`EconomiaConstrucoes.adicionar`; veja o contrato abaixo.

## Depósito com capacidade e excedentes

Promover também `construcoes.py` e seus testes/bancada, ajustando os caminhos
somente quando o chat principal decidir integrar os arquivos. Exemplo:

```python
from construcoes import Capacidades, EconomiaConstrucoes, TerrenoSacolas

m = EconomiaConstrucoes(
    economia=e,
    capacidades=Capacidades(bloco_24_bytes_desde_4dfb2c),
    estruturas=registros_de_construcoes,
    terreno=TerrenoSacolas(tipos, quantidades, semente),
)
resultado = m.adicionar(jogador, id_recurso, quantidade, indice_construcao)
```

O objeto `e` é compartilhado; capacidades e terreno fornecidos também.
`registros_de_construcoes` é copiado para `m.estruturas`; sincronizar esse buffer
ao integrar com um mundo existente. São registros de 276 bytes, base original
`0x49a0c8`. `Capacidades` e `TerrenoSacolas` copiam seus buffers de entrada;
exportar as respectivas propriedades `memoria`, `tipos`, `quantidades` e `semente`.

Não substituir a conta por `max(capacidade - estoque, 0)`: o original pode
mandar um crédito u16 grande quando o estoque já excede o limite. Também não
trocar as duas divisões do nível por uma divisão única.

Tipo 4 sem alojamento levanta `RetiradaColonoPendente`, antes dos efeitos da
dependência `BatimentRetireColon`. Um integrador que disponha dessa rotina pode
passar `retirar_colono(indice)`; o callback deve aplicar seus efeitos reais.
O teste local com callback verifica apenas o contrato e não valida essa rotina.
Os 64 casos x86 desse ramo param na entrada da dependência, sem substituí-la.

As grades de sacolas têm 65.536 bytes cada; não são as grades de movimento.
A procura por espaço usa só os tipos/quantidades e o gerador de `0x497164`.
Não ligar este caminho a busca de rotas ou à geometria de colisão.
O retorno `ResultadoDeposito` é diagnóstico da nova API, não retorno do x86:
`credito_enviado` não é necessariamente o aumento real do saldo, e um pedido
de sacolas pode ser recusado pelo terreno incompatível.

## Débito e recálculo do indicador

`EconomiaConstrucoes.retirar(jogador, recurso, quantidade)` traduz
BatimentEnleveMatiere (`0x4235bd`). Não recebe índice de construção; a convenção
x86 é BL=jogador, AL=recurso e DX=quantidade. O método debita total e RMI mesmo
sem armazéns, e recalcula o indicador se houver armazéns. Não exige teste de
disponibilidade nem retorna sucesso de compra.

`EconomiaConstrucoes.recalcular_recursos(jogador)` traduz BatimentCalculResource
(`0x423355`), com jogador em AL. Apenas atualiza o byte do indicador; jogador
truncado fora de 0..3 e ausência de armazéns são retornos sem alterações.

Não substituir automaticamente todas as chamadas a `Economia.debitar` pelo
wrapper: o chamador original pode debitar pela primitiva e cuidar do recálculo
por outro caminho. `retirar` já executa a fórmula do indicador, sem precisar de
uma chamada adicional a `recalcular_recursos`.

A capacidade unitária zero com armazéns positivos causa `ZeroDivisionError`.
Em `retirar`, o débito anterior permanece aplicado e o indicador antigo não
é sobrescrito. O recálculo não satura o nível em sete nem corrige estoque
acima da capacidade; preservar soma u16, duas divisões e truncamento final u8.
Casos, limites e integração estão em [RETIRADA_RECALCULO.md](RETIRADA_RECALCULO.md).

## Contagem de armazéns na carga

`EconomiaConstrucoes.inicializar_armazens()` traduz BatimentInitCave (`0x419112`).
Exige **1000 registros de 276 bytes** em `m.estruturas`. Reconta todos os tipos
para jogadores 0..3, atualiza `m.contagens_por_tipo` (88 bytes),
`m.contagens_tipo18` (quatro bytes) e o word do número de armazéns nas capacidades.

Os dois buffers de contagens podem ser fornecidos ao construtor por argumentos
de mesmo nome; são copiados. Exportá-los junto aos buffers já existentes ao
sincronizar o estado do mundo. Os endereços originais são `0x49a070` e `0x4dfb4c`.

Não redefinir a capacidade por armazém para 100 nem recalcular automaticamente o
indicador aqui: a rotina original preserva ambos. As contagens são bytes;
preservar o wrap, inclusive 256 armazéns virando zero. Chamadas separadas a
`recalcular_recursos` só devem ser ligadas onde o fluxo original exigir.
O domínio e a validação estão em [CONTAGEM_ARMAZENS.md](CONTAGEM_ARMAZENS.md).

## Ganho e neutralização

`PropriedadeConstrucoes`, em `proprietarios.py`, recebe um `EconomiaConstrucoes`
compartilhado e cópias dos buffers de bibliotecas, balões, números de unidades,
pendências, ordens e permissões. Seus métodos são
`inicializar_jogador(indice, jogador)` e `inicializar_neutro(indice, jogador)`.

Eles não mudam dono/estado nem atualizam as 88 contagens por tipo. Atribuir o
dono pertence ao chamador original; não transformar os dois métodos numa troca
automática de proprietário. A contagem incremental de armazéns é u16, diferente
da recontagem global u8. A neutralização pode debitar o jogador do byte global
`0x4dfab8`, representado por `jogador_deposito`.

Os caminhos de balão que exigem criar/mover unidades levantam
`DependenciaBalaoPendente`, antes da chamada correspondente. Um integrador com
essas rotinas prontas pode fornecer `preparar_chegada`/`preparar_saida`, cada um
implementando sua dependência inteira. Não substituir por retorno fictício:
os 32 testes correspondentes só validam até a entrada original da dependência.
Domínio, endereços, layout e sincronização estão em
[PROPRIEDADE_CONSTRUCOES.md](PROPRIEDADE_CONSTRUCOES.md).

## Atualizações de documentação sugeridas, não realizadas

- FORMATOS.md: substituir a lacuna dos IDs iniciais por comida=1, pedra=2,
  peças=0, citando os débitos de InitRecruteTroupe.
- ROTINAS.md: adicionar os acessores e mutações `0x467640..0x4679d0`.
- CONTINUIDADE.md: marcar consultas, crédito/débito, recálculo do indicador,
  depósito e contagem global dos armazéns como traduzidos; conservar geração
  da produção, alterações incrementais/tecnológicas, consumo completo e filas.
- SIMBOLOS.md/IA.md: registrar os diferentes índices da IA e o retorno 1/-1.
- EMULACAO.md/validação geral: integrar os 38 testes diferenciais sem somar
  automaticamente as contagens desta pesquisa à suíte compartilhada.

## Próximas investigações de economia

1. Completar a dependência `0x41dde0` BatimentRetireColon, se/quando o chat
   responsável por unidades disponibilizar seus efeitos. A entrada e o retorno
   necessário para o ramo tipo 4 estão documentados nesta pesquisa.
2. Ligar os efeitos incrementais traduzidos aos chamadores de colonização e
   neutralização, mantendo criação/movimento de balões no subsistema responsável.
   Completar tecnologia e o restante de TerrainDeposeMatiere fora da flag zero.
3. `0x4283e2` InitRecruteTroupe: completar fila/estados sem alterar a semântica
   das três primitivas de débito. O recorte estático já está nesta pasta.
4. Mercado e trocas em `0x466533..0x467640`: preços, propostas e transferências.
5. Confirmar o significado de RMI, o quarto registro e o byte +7 em gameplay
   ou por outros consumidores, preservando nomes neutros enquanto não confirmado.

Esses itens não dependem de alterar busca de caminhos, contornos ou movimento.
O chat principal continua responsável pela promoção para pastas compartilhadas,
documentos gerais e suíte compartilhada. O commit autorizado desta entrega
se restringe à pasta economia e preserva os arquivos dos outros chats.
