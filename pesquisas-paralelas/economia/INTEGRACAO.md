# Entrega ao chat principal

Esta pasta é autônoma. Nenhum arquivo compartilhado foi alterado e nenhum
projeto Ghidra foi aberto/criado. Os commits autorizados no `main` se limitam
a esta pasta e preservam os arquivos e o índice dos demais chats.
Os comandos de teste usam `-B` e o código de validação desabilita bytecode para
não criar caches nos módulos compartilhados lidos pela pesquisa.

## Como incorporar

1. Revisar [README.md](README.md), os ASM e o relatório com 161 testes aprovados
   e 46.274 execuções x86 (incluindo 88 exceções, três limites esperados e
   paradas em dependências/sufixos delimitados em cada documento).
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

## Extração de recursos e regeneração de campos

`RecursosTerreno`, em `extracao.py`, compartilha `m.terreno` e copia os buffers
de minas, mosaicos e atributos. Não criar outra instância de TerrenoSacolas
para este componente: tipos, quantidades e RNG devem ser os mesmos do depósito.

```python
from extracao import RecursosTerreno

r = RecursosTerreno(m.terreno, minas=tabela_de_80_bytes,
                    mosaicos=grade_de_131072_bytes,
                    atributos=grade_de_65536_bytes,
                    linha=linha_salva, atualizar=flag_salva,
                    periodo=periodo_atual, tempo=tempo_atual)

quantidade = r.recolher_mina(celula)  # Só reduz a reserva da mina.
# A Bag da unidade e a entrega ao depósito pertencem aos chamadores.
r.tempo = novo_tempo & 0xffffffff
r.agendar_campos()
r.atualizar_campos()  # Uma linha; manter a ordem original de chamadas.
```

Sincronizar `r.minas`, `r.mosaicos`, `r.linha` e `r.atualizar`, além dos buffers
e da semente de `m.terreno`. Atributos são apenas lidos por estas rotinas;
atualizá-los a partir do subsistema responsável quando necessário. Os padrões
do construtor são sintéticos, não substituem a carga/inicialização original.

`retirar_mina(indice, quantidade)` recebe índice; `recolher_mina(celula)` e
os métodos de trabalho recebem célula. `indice_mina` devolve 0xffff quando
ausente. `destruir_mina` altera somente os mosaicos e mantém a reserva.
`retirar_sacola` devolve zero tanto para peças quanto para ausência: não usar
o retorno como teste de sucesso. `recolher_campo` não devolve quantidade.

Não ligar essas operações diretamente ao crédito do jogador sem passar pelos
chamadores de armazenamento/transporte apropriados. Não mudar a ordem das
células, usar RNG independente ou atualizar a grade em uma cópia: plantas
criadas à direita podem ser processadas na mesma linha. Os limites da API,
os wraps originais e os 15 endereços estão em
[EXTRACAO_CAMPOS.md](EXTRACAO_CAMPOS.md).

## Início e consultas de recrutamento

`Recrutamento`, em `recrutamento.py`, recebe o mesmo `EconomiaConstrucoes`.
Fornecer `selecoes` (8 bytes), `tipos_unidades` (1300 bytes),
`tipos_sortilegios` (230 bytes), `unidades` (220800 bytes) e `periodo_nova`.
Os buffers são copiados; manter essas vistas sincronizadas com o mundo.

`iniciar(tipo_unidade, jogador, escolher_saida=callback)` aplica as verificações,
os débitos e os campos da construção. O callback recebe seu índice, deve executar
RechercheDecalageSortie (`0x41d1d0`) e devolver a célula. A tradução não escolhe
uma posição provisória nem implementa essa dependência de geometria/ocupação.

Sem callback, `SaidaRecrutamentoPendente` interrompe **após a cobrança e mudança
de estado**. Conservar o estado aplicado e concluir com
`concluir_saida(indice, celula)` depois de resolver a dependência. Não repetir
`iniciar` nem fazer rollback automático. ZeroDivisionError no recálculo também
pode deixar débito parcial aplicado, conforme a ordem original.

`status(tipo, jogador)` usa a seleção; `calcular_status(indice, tipo)` recebe a
construção diretamente. O tipo vem do argumento, e não de +0x7b. Em reparos,
o divisor é a vida máxima da unidade referenciada em +0x88. Não saturar o
resultado em 100 nem transformar as consultas `*_em_recrutamento` em testes
de atividade: elas apenas comparam o tipo guardado. `progresso_nova` conserva
o wrap u32 do produto por 100.

Os 546 testes até a dependência e os 128 sufixos isolados não comprovam sucesso
de ponta a ponta. Não promover esta etapa como fila completa ou criação de
unidades. Endereços, campos, domínio e testes estão em
[RECRUTAMENTO.md](RECRUTAMENTO.md).

## Avanço de produção

Promover também `producao.py` e integrar `Producao` à mesma instância de
`Recrutamento`. A tabela de construções é copiada; os demais buffers são
compartilhados através de `r`:

```python
from producao import Producao

p = Producao(r, tipos_construcoes=bloco_1144_bytes_desde_495d8c,
             ajuste_hospital=byte_495be8)
p.avancar_unidade(indice_construcao)     # ConstruitPerso 0x423b9b
# Avanço isolado; para o fluxo completo da biblioteca, usar Aprendizagem abaixo:
p.avancar_sortilegio(indice_construcao)  # ConstruitSort 0x423d14
```

O único campo alterado é `r.mundo.estruturas[indice*276+0x8c:...+4]`.
Preservar a ordem de chamadas e manter a conclusão no chamador responsável.
Retorno verdadeiro não confirma conclusão; não criar unidade, ensinar
sortilégio, limpar flags ou cobrar de novo com base nesse booleano.
O contador pode ultrapassar `tempo*100` e não satura.

O cálculo numérico depende do controle x87 inicial 0x127f: não substituir a
sequência de divisão/multiplicação em double por uma divisão inteira. Divisor
zero mascarado gera incremento 100. A contagem usa slots etiquetados como
unidades e o tipo do registro referenciado; não usar só a ocupação da Bag.
Sincronizar também a tabela de tipos de construção e o byte de ajuste do
hospital. Contratos, endereços, guardas adicionais e evidências estão em
[PRODUCAO.md](PRODUCAO.md). Não se estabeleceu o escalonamento dessas chamadas
nem se executou a finalização da produção de unidades.

## Conclusão da aprendizagem na biblioteca

Reutilizar as mesmas instâncias de Producao e PropriedadeConstrucoes. Elas
devem apontar para o mesmo `EconomiaConstrucoes`; o construtor verifica isso.

```python
from aprendizagem import Aprendizagem

a = Aprendizagem(p, propriedade_existente, inventados=bloco_20_bytes_desde_508f44)
a.calcular_biblioteca(indice_construcao)  # CalculTroupe 0x4259e6, somente tipo 6.
```

O método já avança e conclui a aprendizagem; não chamar `avancar_sortilegio`
antes dele na mesma atualização. A API retorna None, e os efeitos ficam nos
buffers compartilhados: `propriedade.sortilegios`, `propriedade.ordens`,
`propriedade.pendencias` e `r.mundo.estruturas`. O buffer `inventados` é copiado
e permanece distinto dos disponíveis em `propriedade.sortilegios`.

Sincronizar as duas tabelas de 20 bytes e as duas famílias de Bags com o jogo.
Os setters/resets de flags não refazem listas automaticamente; conservar a
ordem original das chamadas. A conclusão chama liberar, reconstruir ordens e
reconstruir opções da biblioteca, depois limpa os campos da construção.
Não cobrar recursos novamente. Guardas, endereços e campos preservados estão
em [APRENDIZAGEM.md](APRENDIZAGEM.md).

Somente o ramo tipo 6 de CalculTroupe e o ramo DL=6 de BatimentSetTechnologie
foram traduzidos. Não substituir os despachos completos por esses métodos.
O início da aprendizagem e a agenda de atualização continuam pendentes.

## Atualizações de documentação sugeridas, não realizadas

- FORMATOS.md: substituir a lacuna dos IDs iniciais por comida=1, pedra=2,
  peças=0, citando os débitos de InitRecruteTroupe.
- ROTINAS.md: adicionar os acessores e mutações `0x467640..0x4679d0`.
- CONTINUIDADE.md: marcar consultas, crédito/débito, recálculo do indicador,
  depósito, contagens, efeitos econômicos de propriedade, extração no terreno,
  regeneração de campos, avanço de produção e conclusão da biblioteca como traduzidos;
  conservar os demais chamadores completos,
  tecnologias, transporte, consumo e filas como pendências.
- SIMBOLOS.md/IA.md: registrar os diferentes índices da IA e o retorno 1/-1.
- EMULACAO.md/validação geral: integrar os 73 testes diferenciais sem somar
  automaticamente as contagens desta pesquisa à suíte compartilhada.

## Próximas investigações de economia

1. Completar a dependência `0x41dde0` BatimentRetireColon, se/quando o chat
   responsável por unidades disponibilizar seus efeitos. A entrada e o retorno
   necessário para o ramo tipo 4 estão documentados nesta pesquisa.
2. Ligar os efeitos incrementais traduzidos aos chamadores de colonização e
   neutralização, mantendo criação/movimento de balões no subsistema responsável.
   Completar tecnologia e o restante de TerrainDeposeMatiere fora da flag zero.
3. Recrutamento: ligar a dependência de saída de InitRecruteTroupe, traduzir
   conclusão de unidades/escalonamento e completar o fluxo das filas. O início econômico e
   as consultas estão em [RECRUTAMENTO.md](RECRUTAMENTO.md); o avanço já está em
   [PRODUCAO.md](PRODUCAO.md). A conclusão da biblioteca está em
   [APRENDIZAGEM.md](APRENDIZAGEM.md); investigar seu início e demais ramos de tecnologia.
   Não interpretar AL=1 dos helpers de avanço como produto concluído.
4. Mercado e trocas em `0x466533..0x467640`: preços, propostas e transferências.
5. Confirmar o significado de RMI, o quarto registro e o byte +7 em gameplay
   ou por outros consumidores, preservando nomes neutros enquanto não confirmado.
6. Integrar as primitivas de extração aos chamadores de unidades e à agenda
   de CalculGame, preservando a ordem dos sorteios. A duração de trabalho,
   consumo/fome e o transporte completo continuam pendentes.

Esses itens não dependem de alterar busca de caminhos, contornos ou movimento.
O chat principal continua responsável pela promoção para pastas compartilhadas,
documentos gerais e suíte compartilhada. O commit autorizado desta entrega
se restringe à pasta economia e preserva os arquivos dos outros chats.
