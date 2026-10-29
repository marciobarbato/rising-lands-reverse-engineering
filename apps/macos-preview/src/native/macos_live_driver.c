/* App orchestration/transport only. Actual logic and pixels come from Rust ABI1.3. */
#include "MacOSLiveDriver.h"
#include "rising_engine.h"
#include <CommonCrypto/CommonDigest.h>
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef struct {uint32_t base,length,offset;} Entry;
typedef struct {uint32_t offset,length,zero;} Span;
extern int32_t macos_projection_validate(const uint8_t*,uint32_t,const Entry*,uint32_t);
extern int32_t macos_projection_sha256(const uint8_t*,uint32_t,const Span*,uint32_t,uint8_t*);
#define FN(name) __typeof__(&name) name
struct MacOSLiveDriver {
 void *library;
 FN(rl_versao); FN(rl_criar_mundo); FN(rl_carregar_blocos); FN(rl_passo_quadro);
 FN(rl_liberar_mundo); FN(rl_projetar_tudo); FN(rl_erro_mensagem);
 FN(rl_render_criar); FN(rl_render_geracao); FN(rl_render_quadro); FN(rl_render_liberar);
 RlMundo world; RlRenderer renderer; RlFrameInput input,phase2;
 MacOSLiveStatus status;
 uint8_t pixels[480000],palette[768];
 uint8_t *bulk,*surface_hashes,*state_hashes; uint32_t bulk_capacity,surface_count,state_count,audit_limit;
 Entry *entries; Span *spans; uint32_t entry_count,span_count;
};
uint32_t macos_live_abi_version(void){return 1;}
uint32_t macos_live_engine_binding(void){
#ifdef MACOS_STATIC_ENGINE
 return 1;
#else
 return 0;
#endif
}
uint32_t macos_live_status_size(void){return sizeof(MacOSLiveStatus);}
static uint64_t now(void){struct timespec t;clock_gettime(CLOCK_MONOTONIC,&t);return (uint64_t)t.tv_sec*1000000000+t.tv_nsec;}
static uint32_t le(const uint8_t*p){return p[0]|((uint32_t)p[1]<<8)|((uint32_t)p[2]<<16)|((uint32_t)p[3]<<24);}
static uint8_t *file(const char *root,const char *name,uint32_t *length){
 char path[4096];snprintf(path,sizeof(path),"%s/%s",root,name);FILE*f=fopen(path,"rb");if(!f)return NULL;
 if(fseek(f,0,SEEK_END)){fclose(f);return NULL;}long n=ftell(f);rewind(f);
 if(n<=0||n>128*1024*1024){fclose(f);return NULL;}uint8_t*p=malloc((size_t)n);if(!p){fclose(f);return NULL;}
 if(fread(p,1,(size_t)n,f)!=(size_t)n){free(p);p=NULL;}fclose(f);if(p)*length=(uint32_t)n;return p;
}
static int fail(MacOSLiveDriver*d,int code,const char*context){
 d->status.stopped=1;uint32_t n=0;char detail[320]={0};
 d->rl_erro_mensagem(NULL,0,&n);if(n&&n<=sizeof(detail))d->rl_erro_mensagem((uint8_t*)detail,n,&n);
 snprintf(d->status.message,sizeof(d->status.message),"%s · quadro %llu · ABI %d: %s",context,(unsigned long long)(d->status.frames+1),code,detail);return code?code:5;
}
static int proof(MacOSLiveDriver*d,uint32_t index,uint32_t phase,MacOSPhaseObserver observer,void*ctx){
 d->status.phase_index=index;d->status.stop_phase=phase;
 uint64_t t=now();
 if(index<d->audit_limit){
  uint32_t n=0;int c=d->rl_projetar_tudo(d->world,d->bulk,d->bulk_capacity,&n);
  if(c)return fail(d,c,"projeção de prova");
  if(macos_projection_validate(d->bulk,n,d->entries,d->entry_count)||macos_projection_sha256(d->bulk,n,d->spans,d->span_count,d->status.state_sha)||memcmp(d->status.state_sha,d->state_hashes+32*index,32)){
   d->status.stopped=1;snprintf(d->status.message,sizeof(d->status.message),"StateProofMismatch na fase %u",index);return 5;
  }
  d->status.phases_equal++;
  const uint32_t checkpoints[]={1,31,32,45,50,51,52,64,100,101,128};
  if(phase==3)for(unsigned i=0;i<11;i++)if((index/2)==checkpoints[i])d->status.checkpoints_equal++;
 }
 if(observer&&observer(ctx,d->world,index,phase)){d->status.stopped=1;snprintf(d->status.message,sizeof(d->status.message),"PhaseObserverRejected %u",index);return 5;}
 d->status.proof_ns+=now()-t;return 0;
}
#ifdef MACOS_STATIC_ENGINE
#define LOAD(name) do {d->name=&name;} while(0)
#else
#define LOAD(name) do { d->name=(__typeof__(d->name))dlsym(d->library,#name);if(!d->name){snprintf(error,capacity,"Missing ABI symbol %s",#name);goto bad;} } while(0)
#endif
MacOSLiveDriver *macos_live_create(const char*library,const char*root,char*error,uint32_t capacity){
 MacOSLiveDriver*d=calloc(1,sizeof(*d));if(!d)return NULL;d->status.phase_index=UINT32_MAX;
#ifndef MACOS_STATIC_ENGINE
 d->library=dlopen(library,RTLD_NOW|RTLD_LOCAL);if(!d->library){snprintf(error,capacity,"%s",dlerror());goto bad;}
#endif
 LOAD(rl_versao);LOAD(rl_criar_mundo);LOAD(rl_carregar_blocos);LOAD(rl_passo_quadro);LOAD(rl_liberar_mundo);LOAD(rl_projetar_tudo);LOAD(rl_erro_mensagem);
 LOAD(rl_render_criar);LOAD(rl_render_geracao);LOAD(rl_render_quadro);LOAD(rl_render_liberar);
 if(d->rl_versao()!=0x10003){snprintf(error,capacity,"ABI1.3 required");goto bad;}
 uint32_t n=0;uint8_t*s0=file(root,"s0.bin",&n);if(!s0){snprintf(error,capacity,"Missing S0");goto bad;}
 d->bulk_capacity=n;d->bulk=malloc(n);uint32_t count=n>=4?le(s0):0,off=4;if(!count||count>65536){free(s0);goto bad;}RlBloco*blocks=calloc(count,sizeof(*blocks));
 if(!d->bulk||!blocks||count>65536){free(s0);free(blocks);goto bad;}
 for(uint32_t i=0;i<count;i++){if((uint64_t)off+8>n){free(s0);free(blocks);goto bad;}blocks[i].address=le(s0+off);blocks[i].length=le(s0+off+4);off+=8;if((uint64_t)off+blocks[i].length>n){free(s0);free(blocks);goto bad;}blocks[i].data=s0+off;off+=blocks[i].length;}
 int c=d->rl_criar_mundo(0x10003,20,0,&d->world);if(!c)c=d->rl_carregar_blocos(d->world,blocks,count);free(blocks);free(s0);if(c){fail(d,c,"S0");snprintf(error,capacity,"%s",d->status.message);goto bad;}
 uint8_t*in=file(root,"input1.bin",&n);if(!in||n!=sizeof(d->input)){free(in);goto bad;}memcpy(&d->input,in,n);free(in);
 in=file(root,"input2.bin",&n);if(!in||n!=sizeof(d->phase2)){free(in);goto bad;}memcpy(&d->phase2,in,n);free(in);
 RlRenderBytes assets[9]={0};uint8_t*back[9]={0};char name[40];
 for(unsigned i=0;i<9;i++){snprintf(name,sizeof(name),"asset%u.bin",i);back[i]=file(root,name,&n);assets[i]=(RlRenderBytes){back[i],n};if(!back[i]){for(unsigned j=0;j<=i;j++)free(back[j]);goto bad;}}
 uint8_t*surface=file(root,"surface.bin",&n);RlRenderBytes sd={surface,n};uint8_t*keys=file(root,"keys.bin",&n);RlRenderBytes kd={keys,n};uint8_t*payloads=file(root,"cache.bin",&n);RlRenderBytes pd={payloads,n};
 uint32_t cursor_size=0;uint8_t*cursor=file(root,"cursor.bin",&cursor_size);RlRenderCache cache={kd,pd,cursor&&cursor_size==4?le(cursor):UINT32_MAX};
 if(surface&&keys&&payloads&&cursor)c=d->rl_render_criar(d->world,assets,9,&sd,&cache,&d->renderer);else c=1;
 if(surface&&sd.length==480000)memcpy(d->pixels,surface,480000);
 free(surface);free(keys);free(payloads);free(cursor);for(unsigned i=0;i<9;i++)free(back[i]);
 if(c){fail(d,c,"renderer create");snprintf(error,capacity,"%s",d->status.message);goto bad;}
 d->entries=(Entry*)file(root,"entries.bin",&n);d->entry_count=n/sizeof(Entry);if(!d->entries||n%sizeof(Entry))goto bad;
 d->spans=(Span*)file(root,"spans.bin",&n);d->span_count=n/sizeof(Span);if(!d->spans||n%sizeof(Span))goto bad;
 d->state_hashes=file(root,"states.bin",&n);if(!d->state_hashes||n%32||n<257*32)goto bad;d->state_count=n/32;d->audit_limit=257;
 d->surface_hashes=file(root,"surfaces.bin",&n);if(!d->surface_hashes||n%32||n<128*32)goto bad;d->surface_count=n/32;
 in=file(root,"palette.bin",&n);if(!in||n!=768){free(in);goto bad;}memcpy(d->palette,in,768);free(in);
 return d;
 bad:if(capacity&&error[0]==0)snprintf(error,capacity,"Invalid native initialization inputs");macos_live_free(d);return NULL;
}
void macos_live_audit_window(MacOSLiveDriver*d,uint32_t phases){if(d)d->audit_limit=phases<d->state_count?phases:d->state_count;}
int32_t macos_live_advance(MacOSLiveDriver*d,MacOSPhaseObserver observer,void*ctx){
 if(!d||d->status.stopped)return 1;int c;uint64_t t;
 if(d->status.phase_index==UINT32_MAX){t=now();c=d->rl_passo_quadro(d->world,1,&d->input);d->status.logic_ns+=now()-t;if(c)return fail(d,c,"load_tail");d->input.registers=d->phase2.registers;return proof(d,0,1,observer,ctx);}
 uint64_t gen=0;uint32_t phase=0,counter=0;t=now();c=d->rl_render_geracao(d->world,&gen,&phase,&counter);if(c)return fail(d,c,"render generation");
 RlRenderResult out={0};c=d->rl_render_quadro(d->renderer,gen,1,d->pixels,sizeof(d->pixels),d->palette,sizeof(d->palette),&out);d->status.render_ns+=now()-t;
 if(c)return fail(d,c,"Rust render");d->status.generation=gen;d->status.disposition=out.disposition;
 if(out.disposition==2){d->status.stopped=1;snprintf(d->status.message,sizeof(d->status.message),"%s at 0x%08x: %s",out.stop_callee,out.stop_address,out.stop_reason);return 5;}
 t=now();CC_SHA256(d->pixels,sizeof(d->pixels),d->status.surface_sha);
 if(d->status.frames<d->surface_count){if(memcmp(d->status.surface_sha,d->surface_hashes+32*d->status.frames,32)){d->status.stopped=1;snprintf(d->status.message,sizeof(d->status.message),"SurfaceProofMismatch no quadro %llu",(unsigned long long)(d->status.frames+1));return 5;}d->status.surfaces_equal++;}
 d->status.proof_ns+=now()-t;
 t=now();c=d->rl_passo_quadro(d->world,2,&d->input);d->status.logic_ns+=now()-t;if(c)return fail(d,c,"between_frames");
 if((c=proof(d,(uint32_t)(2*d->status.frames+1),2,observer,ctx)))return c;
 t=now();c=d->rl_passo_quadro(d->world,3,&d->input);d->status.logic_ns+=now()-t;if(c)return fail(d,c,"CalculGame");
 if((c=proof(d,(uint32_t)(2*d->status.frames+2),3,observer,ctx)))return c;
 d->status.frames++;c=d->rl_render_geracao(d->world,&gen,&phase,&counter);if(c)return fail(d,c,"generation after frame");d->status.counter=counter;return 0;
}
void macos_live_status(MacOSLiveDriver*d,MacOSLiveStatus*out){if(d&&out){*out=d->status;out->world=d->world;uint64_t g=0;uint32_t p=0,c=0;if(d->rl_render_geracao(d->world,&g,&p,&c)==0)out->counter=c;}}
uint64_t macos_live_renderer(MacOSLiveDriver*d){return d?d->renderer:0;}
const uint8_t*macos_live_pixels(MacOSLiveDriver*d){return d?d->pixels:NULL;}
const uint8_t*macos_live_palette(MacOSLiveDriver*d){return d?d->palette:NULL;}
int32_t macos_live_read(MacOSLiveDriver*d,uint32_t address,uint32_t size,uint8_t*out){
 if(!d||!out||!size)return 1;uint32_t n=0;int c=d->rl_projetar_tudo(d->world,d->bulk,d->bulk_capacity,&n);if(c)return c;
 uint32_t off=4;for(uint32_t i=0;i<le(d->bulk)&&off+8<=n;i++){uint32_t base=le(d->bulk+off),len=le(d->bulk+off+4);off+=8;if((uint64_t)off+len>n)return 3;if(address>=base&&(uint64_t)address+size<=(uint64_t)base+len){memcpy(out,d->bulk+off+address-base,size);return 0;}off+=len;}return 3;
}
void macos_live_free(MacOSLiveDriver*d){if(!d)return;if(d->renderer&&d->rl_render_liberar)d->rl_render_liberar(d->renderer);if(d->world&&d->rl_liberar_mundo)d->rl_liberar_mundo(d->world);if(d->library)dlclose(d->library);free(d->bulk);free(d->surface_hashes);free(d->state_hashes);free(d->entries);free(d->spans);free(d);}
