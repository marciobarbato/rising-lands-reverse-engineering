/*
 * Native Unicorn 2.1.4 memory/block hooks for the comparison policy's pass 2.
 *
 * Equivalent, access for access, to the Python closures of
 * pesquisas-paralelas/missoes/politica_comparacao_quadros.ganchos (owned by
 * Missions, reused read-only):
 *
 *   - display-root context tracker: a stack of (entry ESP, return address).
 *     At each block in the hooked code range, entries are popped while
 *     ESP > entry ESP, or while the block is the top entry's return address
 *     with ESP == entry ESP + 4 (the root's RET landed, so a following call at
 *     the same depth is outside it).  A block at a root address pushes
 *     (ESP, [ESP]) unless that exact pair is already on top (re-entry after an
 *     emulation stop).  The context of an access pops while ESP > entry ESP
 *     and is "display" when the stack is non-empty, else "logic".  Exactly as
 *     in Python, an access pops only when its context is evaluated: a target
 *     hook evaluates it at the first watched byte of the access, a surface
 *     hook always.
 *   - target hooks: for every byte of the access that is a watched address,
 *     count (address, kind, context, phase, EIP).  EIP is read once per
 *     access.  Overlapping Python hook ranges fire the Python closure once per
 *     range; the "multiple" callback reproduces that with a per-address
 *     multiplicity table (number of Python ranges containing the access
 *     address), so one native hook can stand for all of them.
 *   - surface hooks: count (kind, context, phase, EIP if logic else '*').
 *
 * Aggregates are kept in insertion order (first occurrence) so Python can
 * rebuild its dictionaries with identical key order.  The engine API is
 * reached through function pointers handed over by Python from the very
 * libunicorn the engine was created with; nothing is linked.
 *
 * Built only by ferramentas/compilar_ganchos_nativos.py, which defines
 * GANCHOS_IDENTIDADE (sha256 of this source and the build flags).
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#ifndef GANCHOS_IDENTIDADE
#error "Build with ferramentas/compilar_ganchos_nativos.py"
#endif

#define GANCHOS_ABI 1

typedef struct uc_struct uc_engine;
typedef int (*f_reg_read)(uc_engine *, int, void *);
typedef int (*f_mem_read)(uc_engine *, uint64_t, void *, uint64_t);
typedef int (*f_emu_stop)(uc_engine *);

enum { LEITURA = 0, ESCRITA = 1 };
enum { LOGICA = 0, EXIBICAO = 1 };
enum { TAB_ACESSOS = 0, TAB_SUPERFICIE = 1 };
enum { ERRO_NENHUM = 0, ERRO_MEMORIA = 1, ERRO_LEITURA_PILHA = 2, ERRO_REGISTRADOR = 3 };

#define BIT_ALVO 0x01u
#define PAGINAS (1u << 20)

typedef struct {
    uint64_t k1;   /* address << 32 | EIP */
    uint64_t k2;   /* phase << 32 | wildcard << 16 | kind << 8 | context */
    uint64_t n;
} Entrada;

typedef struct {
    Entrada *e;
    uint32_t ne, cap;
    uint32_t *idx;   /* entry index + 1, 0 = empty */
    uint32_t mascara;
} Tabela;

typedef struct {
    uint32_t esp, ret;
} Raiz;

struct Rastreador;
typedef struct {
    struct Rastreador *r;
    int tipo;
} DadosGancho;

typedef struct Rastreador {
    uint32_t abi;
    f_reg_read reg_read;
    f_mem_read mem_read;
    f_emu_stop emu_stop;
    int reg_esp, reg_eip;
    uint32_t *raizes;
    uint32_t nraizes;
    Raiz *pilha;
    uint32_t npilha, cappilha;
    uint8_t **paginas;  /* per 4 KiB page: bit 0 watched, bits 1..7 multiplicity */
    uint32_t fase;
    Tabela tab[2];
    int erro;
    uint64_t erro_detalhe;
    uint64_t estat[4];  /* blocks, target callbacks, surface callbacks, context evaluations */
    DadosGancho dados[2];
} Rastreador;

static uint64_t misturar(uint64_t a, uint64_t b) {
    uint64_t x = a * 0x9e3779b97f4a7c15ULL ^ (b + 0x632be59bd9b4e019ULL + (a << 6) + (a >> 2));
    x ^= x >> 30;
    x *= 0xbf58476d1ce4e5b9ULL;
    x ^= x >> 27;
    x *= 0x94d049bb133111ebULL;
    x ^= x >> 31;
    return x;
}

static void falhar(Rastreador *r, uc_engine *uc, int erro, uint64_t detalhe) {
    if (!r->erro) {
        r->erro = erro;
        r->erro_detalhe = detalhe;
    }
    if (uc && r->emu_stop)
        r->emu_stop(uc);
}

static int tabela_iniciar(Tabela *t) {
    t->ne = 0;
    t->cap = 1024;
    t->e = malloc(sizeof(Entrada) * t->cap);
    t->idx = calloc(2048, sizeof(uint32_t));
    t->mascara = 2047;
    return t->e && t->idx;
}

static void tabela_liberar(Tabela *t) {
    free(t->e);
    free(t->idx);
    memset(t, 0, sizeof(*t));
}

static int tabela_reindexar(Tabela *t, uint32_t tamanho) {
    uint32_t *novo = calloc(tamanho, sizeof(uint32_t));
    if (!novo)
        return 0;
    uint32_t m = tamanho - 1;
    for (uint32_t i = 0; i < t->ne; i++) {
        uint32_t h = (uint32_t)misturar(t->e[i].k1, t->e[i].k2) & m;
        while (novo[h])
            h = (h + 1) & m;
        novo[h] = i + 1;
    }
    free(t->idx);
    t->idx = novo;
    t->mascara = m;
    return 1;
}

static int tabela_somar(Tabela *t, uint64_t k1, uint64_t k2, uint64_t n) {
    uint32_t h = (uint32_t)misturar(k1, k2) & t->mascara;
    for (;;) {
        uint32_t i = t->idx[h];
        if (!i)
            break;
        Entrada *e = &t->e[i - 1];
        if (e->k1 == k1 && e->k2 == k2) {
            e->n += n;
            return 1;
        }
        h = (h + 1) & t->mascara;
    }
    if (t->ne == t->cap) {
        if (t->cap >= 0x40000000u)
            return 0;
        Entrada *novo = realloc(t->e, sizeof(Entrada) * (size_t)t->cap * 2);
        if (!novo)
            return 0;
        t->e = novo;
        t->cap *= 2;
    }
    t->e[t->ne] = (Entrada){k1, k2, n};
    t->idx[h] = ++t->ne;
    if ((uint64_t)t->ne * 2 > t->mascara)
        return tabela_reindexar(t, (t->mascara + 1) * 2);
    return 1;
}

static void tabela_limpar(Tabela *t) {
    t->ne = 0;
    memset(t->idx, 0, sizeof(uint32_t) * ((size_t)t->mascara + 1));
}

static inline uint8_t marca(const Rastreador *r, uint64_t a) {
    if (a >> 32)
        return 0;
    const uint8_t *p = r->paginas[a >> 12];
    return p ? p[a & 0xfff] : 0;
}

static uint8_t *pagina(Rastreador *r, uint64_t a) {
    uint8_t **p = &r->paginas[a >> 12];
    if (!*p)
        *p = calloc(4096, 1);
    return *p;
}

static int ler_u32_reg(Rastreador *r, uc_engine *uc, int reg, uint32_t *saida) {
    uint64_t v = 0;
    if (r->reg_read(uc, reg, &v) != 0) {
        falhar(r, uc, ERRO_REGISTRADOR, (uint64_t)reg);
        return 0;
    }
    *saida = (uint32_t)v;
    return 1;
}

static int contexto(Rastreador *r, uc_engine *uc) {
    uint32_t esp;
    r->estat[3]++;
    if (!ler_u32_reg(r, uc, r->reg_esp, &esp))
        return LOGICA;
    while (r->npilha && esp > r->pilha[r->npilha - 1].esp)
        r->npilha--;
    return r->npilha ? EXIBICAO : LOGICA;
}

static int eh_raiz(const Rastreador *r, uint64_t endereco) {
    for (uint32_t i = 0; i < r->nraizes; i++)
        if (r->raizes[i] == endereco)
            return 1;
    return 0;
}

/* ------------------------------------------------------------ hook callbacks */

void ganchos_cb_bloco(uc_engine *uc, uint64_t endereco, uint32_t tamanho, void *dados) {
    Rastreador *r = dados;
    uint32_t esp;
    (void)tamanho;
    r->estat[0]++;
    if (!ler_u32_reg(r, uc, r->reg_esp, &esp))
        return;
    while (r->npilha) {
        Raiz topo = r->pilha[r->npilha - 1];
        if (esp > topo.esp || (endereco == topo.ret && (uint64_t)esp == (uint64_t)topo.esp + 4))
            r->npilha--;
        else
            break;
    }
    if (!eh_raiz(r, endereco))
        return;
    uint32_t ret = 0;
    if (r->mem_read(uc, esp, &ret, 4) != 0) {
        falhar(r, uc, ERRO_LEITURA_PILHA, esp);
        return;
    }
    if (r->npilha && r->pilha[r->npilha - 1].esp == esp && r->pilha[r->npilha - 1].ret == ret)
        return;
    if (r->npilha == r->cappilha) {
        uint32_t cap = r->cappilha ? r->cappilha * 2 : 64;
        Raiz *novo = realloc(r->pilha, sizeof(Raiz) * cap);
        if (!novo) {
            falhar(r, uc, ERRO_MEMORIA, 0);
            return;
        }
        r->pilha = novo;
        r->cappilha = cap;
    }
    r->pilha[r->npilha++] = (Raiz){esp, ret};
}

static void processar_alvo(Rastreador *r, uc_engine *uc, int tipo, uint64_t endereco, int tamanho, uint64_t vezes) {
    int tem_chave = 0;
    uint64_t k2 = 0;
    uint32_t eip = 0;
    r->estat[1]++;
    for (int k = 0; k < tamanho; k++) {
        uint64_t a = endereco + (uint64_t)k;
        if (!(marca(r, a) & BIT_ALVO))
            continue;
        if (!tem_chave) {
            int ctx = contexto(r, uc);
            if (r->erro || !ler_u32_reg(r, uc, r->reg_eip, &eip))
                return;
            k2 = ((uint64_t)r->fase << 32) | ((uint64_t)tipo << 8) | (uint64_t)ctx;
            tem_chave = 1;
        }
        if (!tabela_somar(&r->tab[TAB_ACESSOS], (a << 32) | eip, k2, vezes)) {
            falhar(r, uc, ERRO_MEMORIA, a);
            return;
        }
    }
}

/* One callback per Python hook range: the closure fires once. */
void ganchos_cb_alvo(uc_engine *uc, int tipo_uc, uint64_t endereco, int tamanho, int64_t valor, void *dados) {
    DadosGancho *d = dados;
    (void)tipo_uc;
    (void)valor;
    processar_alvo(d->r, uc, d->tipo, endereco, tamanho, 1);
}

/* One callback standing for every Python range containing the access address. */
void ganchos_cb_alvo_multiplo(uc_engine *uc, int tipo_uc, uint64_t endereco, int tamanho, int64_t valor,
                              void *dados) {
    DadosGancho *d = dados;
    (void)tipo_uc;
    (void)valor;
    uint64_t vezes = marca(d->r, endereco) >> 1;
    if (vezes)
        processar_alvo(d->r, uc, d->tipo, endereco, tamanho, vezes);
}

void ganchos_cb_superficie(uc_engine *uc, int tipo_uc, uint64_t endereco, int tamanho, int64_t valor,
                           void *dados) {
    DadosGancho *d = dados;
    Rastreador *r = d->r;
    (void)tipo_uc;
    (void)endereco;
    (void)tamanho;
    (void)valor;
    r->estat[2]++;
    int ctx = contexto(r, uc);
    if (r->erro)
        return;
    uint32_t eip = 0;
    uint64_t curinga = 1;
    if (ctx == LOGICA) {
        if (!ler_u32_reg(r, uc, r->reg_eip, &eip))
            return;
        curinga = 0;
    }
    uint64_t k2 = ((uint64_t)r->fase << 32) | (curinga << 16) | ((uint64_t)d->tipo << 8) | (uint64_t)ctx;
    if (!tabela_somar(&r->tab[TAB_SUPERFICIE], eip, k2, 1))
        falhar(r, uc, ERRO_MEMORIA, 0);
}

/* ------------------------------------------------------------ control API */

const char *ganchos_identidade(void) { return "ganchos_memoria abi=1 " GANCHOS_IDENTIDADE; }

Rastreador *ganchos_criar(void *reg_read, void *mem_read, void *emu_stop, int reg_esp, int reg_eip) {
    Rastreador *r = calloc(1, sizeof(Rastreador));
    if (!r)
        return NULL;
    r->abi = GANCHOS_ABI;
    r->reg_read = (f_reg_read)reg_read;
    r->mem_read = (f_mem_read)mem_read;
    r->emu_stop = (f_emu_stop)emu_stop;
    r->reg_esp = reg_esp;
    r->reg_eip = reg_eip;
    r->paginas = calloc(PAGINAS, sizeof(uint8_t *));
    r->dados[LEITURA] = (DadosGancho){r, LEITURA};
    r->dados[ESCRITA] = (DadosGancho){r, ESCRITA};
    if (!r->paginas || !tabela_iniciar(&r->tab[0]) || !tabela_iniciar(&r->tab[1])) {
        free(r->paginas);
        tabela_liberar(&r->tab[0]);
        tabela_liberar(&r->tab[1]);
        free(r);
        return NULL;
    }
    return r;
}

void ganchos_destruir(Rastreador *r) {
    if (!r)
        return;
    for (uint32_t i = 0; i < PAGINAS; i++)
        free(r->paginas[i]);
    free(r->paginas);
    free(r->raizes);
    free(r->pilha);
    tabela_liberar(&r->tab[0]);
    tabela_liberar(&r->tab[1]);
    free(r);
}

void *ganchos_dados(Rastreador *r, int tipo) { return (tipo == ESCRITA) ? &r->dados[ESCRITA] : &r->dados[LEITURA]; }

int ganchos_definir_raizes(Rastreador *r, const uint32_t *raizes, uint32_t n) {
    uint32_t *novo = malloc(sizeof(uint32_t) * (n ? n : 1));
    if (!novo)
        return 0;
    memcpy(novo, raizes, sizeof(uint32_t) * n);
    free(r->raizes);
    r->raizes = novo;
    r->nraizes = n;
    return 1;
}

int ganchos_marcar_alvos(Rastreador *r, const uint32_t *enderecos, uint32_t n) {
    for (uint32_t i = 0; i < n; i++) {
        uint8_t *p = pagina(r, enderecos[i]);
        if (!p)
            return 0;
        p[enderecos[i] & 0xfff] |= BIT_ALVO;
    }
    return 1;
}

/* Add one Python hook range [inicio, fim] (inclusive) to the multiplicity table. */
int ganchos_somar_faixa(Rastreador *r, uint64_t inicio, uint64_t fim) {
    if (fim >> 32 || inicio > fim)
        return 0;
    for (uint64_t a = inicio; a <= fim; a++) {
        uint8_t *p = pagina(r, a);
        if (!p)
            return 0;
        if ((p[a & 0xfff] >> 1) == 0x7f)
            return 0;
        p[a & 0xfff] = (uint8_t)(p[a & 0xfff] + 2);
    }
    return 1;
}

uint32_t ganchos_multiplicidade(Rastreador *r, uint64_t a) { return marca(r, a) >> 1; }

void ganchos_definir_fase(Rastreador *r, uint32_t fase) { r->fase = fase; }

uint32_t ganchos_tamanho(Rastreador *r, int tabela) { return r->tab[tabela ? 1 : 0].ne; }

/* Columns of a table in insertion order. */
void ganchos_exportar(Rastreador *r, int tabela, uint32_t *endereco, uint32_t *eip, uint32_t *fase, uint8_t *tipo,
                      uint8_t *ctx, uint8_t *curinga, uint64_t *n) {
    Tabela *t = &r->tab[tabela ? 1 : 0];
    for (uint32_t i = 0; i < t->ne; i++) {
        const Entrada *e = &t->e[i];
        endereco[i] = (uint32_t)(e->k1 >> 32);
        eip[i] = (uint32_t)e->k1;
        fase[i] = (uint32_t)(e->k2 >> 32);
        curinga[i] = (uint8_t)(e->k2 >> 16);
        tipo[i] = (uint8_t)(e->k2 >> 8);
        ctx[i] = (uint8_t)e->k2;
        n[i] = e->n;
    }
}

void ganchos_limpar(Rastreador *r, int tabela) { tabela_limpar(&r->tab[tabela ? 1 : 0]); }

int ganchos_erro(Rastreador *r, uint64_t *detalhe) {
    if (detalhe)
        *detalhe = r->erro_detalhe;
    return r->erro;
}

uint32_t ganchos_pilha(Rastreador *r, uint32_t *saida, uint32_t max) {
    for (uint32_t i = 0; i < r->npilha && i < max; i++) {
        saida[2 * i] = r->pilha[i].esp;
        saida[2 * i + 1] = r->pilha[i].ret;
    }
    return r->npilha;
}

void ganchos_estatisticas(Rastreador *r, uint64_t *saida) { memcpy(saida, r->estat, sizeof(r->estat)); }
