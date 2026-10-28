"""Adaptadores das entregas concluídas. Importações só dos snapshots locais."""
from pathlib import Path
import dataclasses,hashlib,json,os,struct,sys
ROOT=Path(os.environ.get('RISING_APP_ROOT',Path(__file__).resolve().parent))
if not (ROOT/'snapshot.json').exists():ROOT=ROOT.parent
SOURCE=json.loads((ROOT/'snapshot.json').read_text())
UNIFIED='features' in SOURCE
if UNIFIED:
    RESEARCH={}
    for domain,title in (('economia','Economia'),('combate','Combate')):
        prefix='pesquisas-paralelas/'+domain+'/'
        files=[{**f,'path':f['path'][len(prefix):]} for f in SOURCE['files'] if f['path'].startswith(prefix)]
        RESEARCH[domain]={'path':SOURCE['snapshot']+'/'+prefix.rstrip('/'),'title':title,
                          'sha256':hashlib.sha256(json.dumps(files,sort_keys=True).encode()).hexdigest(),
                          'files':files,'commit':SOURCE['commit']}
else:
    RESEARCH=json.loads((ROOT/'research.json').read_text())['research']
for m in RESEARCH.values():sys.path.insert(0,str(ROOT/m['path']))
from economia import Economia, Recurso, custos_unidade
from construcoes import EconomiaConstrucoes,RetiradaColonoPendente
import alvos_alcance as alvo
from mira_angular import engin_vise_cible,mira_requerida

class BancadaPesquisa:
    def __init__(self,mission,catalog):
        self.catalog=catalog;self.economy=Economia.de_recursos_eta(mission['recursos_por_tipo'])
        self.buildings=EconomiaConstrucoes(economia=self.economy)
        self.buildings.estruturas[8]=3
        struct.pack_into('<H',self.buildings.estruturas,2,0x0808)
        self.buildings.capacidades.configurar(0,1,100)
        self.last='Saldos carregados do ETA. Construção tipo 3 e capacidade 1 × 100 são estado de bancada.'
        self.last_combat=None
    @staticmethod
    def integer(value,low,high):
        if isinstance(value,bool) or not isinstance(value,int) or not low<=value<=high:raise ValueError('Parâmetro fora do domínio da bancada')
        return value
    def mutate(self,msg):
        op=msg.get('operation');player=self.integer(msg.get('player',0),0,3)
        resource=self.integer(msg.get('resource',1),0,2);qty=self.integer(msg.get('quantity',0),0,1000)
        if op=='credit':self.economy.creditar(player,resource,qty);self.last=f'AjouteMatiere: crédito direto {qty}; não é produção.'
        elif op=='debit':self.economy.debitar(player,resource,qty);self.last=f'EnleveMatiere: débito {qty}, com piso zero; não é compra/recrutamento.'
        elif op=='deposit':
            r=self.buildings.adicionar(player,resource,qty,0);self.last='BatimentAjouteMatiere: '+json.dumps(dataclasses.asdict(r),ensure_ascii=False)
        elif op=='withdraw':self.buildings.retirar(player,resource,qty);self.last='BatimentEnleveMatiere: débito e recálculo do indicador executados.'
        elif op=='recalculate':self.buildings.recalcular_recursos(player);self.last='BatimentCalculResource: indicador recalculado; saldos preservados.'
        else:raise ValueError('Operação econômica desconhecida')
        return self.last
    def state(self):
        bags=[{'pos':[c&255,c>>8],'resource':self.buildings.terreno.tipos[c]-0x42,'quantity':v} for c,v in enumerate(self.buildings.terreno.quantidades) if v]
        return {'balances':[self.economy.consultar(p)._asdict() for p in range(4)],'rmi':[self.economy.consultar_rmi(p)._asdict() for p in range(4)],'stock':[self.economy.consultar_estoque(p)._asdict() for p in range(4)],'capacity':list(self.buildings.capacidades.parametros(0)),'level':self.buildings.capacidades.nivel(0),'bags':bags,'last':self.last,'combat':self.last_combat,'sources':[{'name':n,'title':m['title'],'sha256':m['sha256'],'files':len(m['files']),'commit':m.get('commit')} for n,m in RESEARCH.items()]}
    def combat(self,world,indice,target):
        if world is None:raise ValueError('Use o laboratório para consultas de combate; a RAM da missão não está carregada por completo.')
        self.integer(indice,0,2);self.integer(target,0,2)
        if indice==target:raise ValueError('Escolha outra unidade como alvo')
        records=[bytearray(world.ler_unidade(i)) for i in range(800)]
        u=records[indice];tipo=self.catalog[u[1]]
        selected=alvo.encontrar_alvo(records,indice,{c:r for c,r in enumerate(world.regioes) if r&0xc000==0x4000},bytes(5))
        em_alcance=alvo.a_portee(records,indice,1,target)
        linha=alvo.linha_de_tiro(u,alvo.palavra(records[target],0x7c),{i:t for i,t in enumerate(world.tiles) if t},world.largura,world.altura)
        # Ordem somente em cópia: não conecta a animação/dano ainda ausentes ao tick vivo.
        needed=not alvo.ordem_ja_definida(u,1,target)
        if needed:
            clone=__import__('copy').deepcopy(world);clone.redefinir_ordem(indice)
            u,accepted=alvo.ordem_apos_reset(clone.ler_unidade(indice),indice,1,target);records[indice]=u
        else:accepted=True
        mira=mira_requerida(records,indice) if accepted else None
        aligned=engin_vise_cible(records,indice) if accepted else False
        valid=alvo.alvo_ordem_valido(records,indice) if accepted else False
        ready=alvo.arma_carregada(alvo.palavra(u,0x102),tipo['recarga'])
        cycle=alvo.iniciar_ciclo_apos_mira(u,tipo['recarga'])[1] if accepted and aligned else 'alinhamento pendente'
        costs=custos_unidade(bytes.fromhex(tipo['registro_memoria_hex']))
        result={'attacker':indice,'target':target,'enemy':alvo.engin_est_ennemi(u[0],records[target][0],bytes(5)),'automaticTarget':None if selected==65535 else selected,'range':em_alcance,'line':linha,'orderAcceptedOnCopy':accepted,'orderValid':valid,'aim':mira,'aligned':aligned,'loaded':ready,'entryGate':alvo.preparar_inicio(u,em_alcance,linha) if accepted else False,'cycleGate':cycle,'unitCosts':costs._asdict(),'canAfford':self.economy.suficiente(0,*costs[:3]),'damageApplied':False,'note':'Consulta e prévia da ordem sobre cópia. Não executa tiro, projétil, animação ou dano.'}
        self.last_combat=result;return result
