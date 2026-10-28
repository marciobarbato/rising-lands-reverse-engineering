"""Adaptador local da demonstração. Protocolo JSON por linha; sem rede ou x86."""
from pathlib import Path
import copy
import hashlib
import json
import math
import os
import struct
import sys
import time
import traceback

ROOT = Path(os.environ.get('RISING_APP_ROOT', Path(__file__).resolve().parent))
if not (ROOT/'snapshot.json').exists(): ROOT=ROOT.parent
MANIFEST=json.loads((ROOT/'snapshot.json').read_text())
SNAP=ROOT/MANIFEST['snapshot']
sys.path.insert(0,str(SNAP/'ferramentas'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from research_adapter import BancadaPesquisa
from navegacao_unidades import MundoNavegacao
from movimento import PARAMETROS_TIPOS, direcao_entre_celulas, celula_vizinha
from passagem_unidades import consultar_passagem
from caminhos import proxima_celula
PYTHON_SOLVER_AVAILABLE=(SNAP/"ferramentas/solucionador_python.py").is_file()
if PYTHON_SOLVER_AVAILABLE:
    from solucionador_python import SolucionadorCaminhosPython


def xy(c): return [c&255,c>>8]
def cell(x,y): return y*256+x


class MundoObservado(MundoNavegacao):
    """Instrumentação que preserva as chamadas e os resultados do snapshot."""
    def __init__(self,*args):
        super().__init__(*args); self.colisoes=[]; self.tick=0
    def escolher_direto(self,indice):
        origem=self.palavra(indice,8); destino=self.palavra(indice,0x7e)
        d=direcao_entre_celulas(origem,destino)
        # Registra as consultas que EnginNextCase fará, até a primeira permitida.
        for t in range(3):
            c=celula_vizinha(origem,d,self.largura,self.altura)
            if c!=65535:
                ok,candidatos=consultar_passagem(self,indice,c)
                if ok: break
                self.colisoes.append({'tick':self.tick,'unit':indice,'cell':xy(c),'reason':'ocupação / máscara de passagem','occupants':[v for v in candidatos if v!=65535]})
                if c==destino: break
            d=((d-3)%16)+1 if t==0 else ((d+1)%16)+1
        self.colisoes=self.colisoes[-160:]
        return super().escolher_direto(indice)
    def escolher_da_rota(self,indice):
        c=proxima_celula(self.rotas[indice])
        if c is not None:
            ok,candidatos=consultar_passagem(self,indice,c)
            if not ok:
                self.colisoes.append({'tick':self.tick,'unit':indice,'cell':xy(c),'reason':'rota invalidada por bloqueio','occupants':[v for v in candidatos if v!=65535]})
                self.colisoes=self.colisoes[-160:]
        return super().escolher_da_rota(indice)



class Preview:
    def __init__(self):
        self.catalog=json.loads((SNAP/'relatorios/unidades.json').read_text())['unidades']
        self.mission=json.loads((ROOT/'assets/missao01.json').read_text())
        self.backend='python' if PYTHON_SOLVER_AVAILABLE else 'local'
        self.scenario='obstaculo'; self.selected=0; self.reset('obstaculo')
    def reset(self,scenario,backend=None):
        if scenario=='jogavel' and 'features' not in MANIFEST:
            raise ValueError('A sessão jogável exige o build de uma revisão única. Execute compilar-jogável.')
        if backend is not None:
            if backend not in ("python","local"):raise ValueError("Backend desconhecido")
            if backend=="python" and not PYTHON_SOLVER_AVAILABLE:raise ValueError("Solucionador Python não consta deste snapshot")
            self.backend=backend
        if scenario not in ('obstaculo','parede','livre','missao','jogavel'): raise ValueError('Cenário desconhecido')
        self.scenario=scenario;self.tick=0;self.paused=True;self.speed=1;self.events=[];self.selected=0
        self.research=BancadaPesquisa(self.mission,self.catalog)
        self.session=None
        self.pump_fraction=0;self.pump_time=None;self.pump_intervals=[];self.pump_max=0;self.blocked={};self.requested={};self.routes={};self.trails={};self.plans={};self.errors=[]
        if scenario=='missao':
            self.world=None
            self.width=self.mission['largura'];self.height=self.mission['altura']
            self.events=[{'tick':0,'text':'Missão original em inspeção. Carga da RAM e colisões completas ainda parciais.'}]
            return
        self.width=self.height=16;self.world=MundoObservado(16,16,SolucionadorCaminhosPython() if self.backend=='python' else None)
        # Exterior natural definido antes de Chemin_Remap, como na bancada commitada.
        for y in range(256):
            start=y*256+(16 if y<16 else 0);end=(y+1)*256
            self.world.atributos[start:end]=bytes([1])*(end-start)
            self.world.objetos[start:end]=bytes([1])*(end-start)
        self.obstacles=([(6,4)] if scenario=='obstaculo' else ([(6,y) for y in range(11)] if scenario in ('parede','jogavel') else []))
        for x,y in self.obstacles:
            c=cell(x,y);self.world.atributos[c]=1;self.world.objetos[c]=1
        self.world.refazer_regioes()
        for i,(x,y,tipo) in enumerate(((2,4,0),(2,9,2),(3,12,7))):
            u=bytearray(276);u[0]=1 if i==2 else 0;u[1]=tipo;u[2]=7;u[0x72]=1;u[0x90]=u[0x91]=9
            u[0xbb]=self.catalog[tipo]['raio_visao'];u[0xb0]=self.catalog[tipo]['alcance_ataque_quadrado_u16']&255;u[0x78]=1
            u[0x98],u[0x93],u[0xa5],u[0xa7]=PARAMETROS_TIPOS[tipo]
            for off,val in ((4,20),(8,cell(x,y)),(0x7c,cell(x,y)),(0x7e,cell(x,y)),(0x9a,100),(0xb8,65535),(0xc0,65535)):
                struct.pack_into('<H',u,off,val)
            struct.pack_into('<I',u,0x10c,0xffffffff)
            self.world.escrever_unidade(i,u);self.world.ocupar(i,cell(x,y),True)
            self.world.limites_fadiga[tipo]=self.catalog[tipo]['fadiga']
            self.world.descobrir_area(cell(x,y),u[0xbb]+2,u[0]);self.world.iluminar_area(cell(x,y),u[0xbb],u[0])
            self.trails[i]=[[x,y]];self.routes[i]=[];self.plans[i]='sem ordem'
        self.log('Laboratório sintético pronto. Selecione uma unidade e clique no destino.')
        if scenario=='jogavel':
            from playable_session import SessaoJogavel
            self.session=SessaoJogavel(self)
    def log(self,text):
        self.events.append({'tick':self.tick,'text':text});self.events=self.events[-80:]
    def _index(self,value):
        if isinstance(value,bool) or not isinstance(value,int): raise ValueError('Índice inválido')
        valid=[u['indice'] for u in self.mission['unidades']] if self.scenario=='missao' else list(range(3))
        if value not in valid:raise ValueError('Unidade inexistente')
        return value
    def order(self,i,x,y):
        if self.world is None:raise ValueError('A missão 1 está em modo de inspeção. Use o laboratório para mover.')
        self._index(i)
        if self.session:self.session.controllable(i)
        if any(isinstance(v,bool) or not isinstance(v,int) for v in (x,y)) or not(0<=x<16 and 0<=y<16):raise ValueError('Destino fora do mapa')
        self.world.mover_unidade(cell(x,y),i)
        self.blocked.pop(i,None);self.requested[i]=[x,y]
        self.trails[i]=[xy(self.world.palavra(i,8))]
        self.routes[i],self.plans[i]=self.forecast(i)
        self.log(f'U{i}: ordem para ({x}, {y}); {self.plans[i]}.')
    def forecast(self,i):
        # Forecast only on a copied world; it does not replace live navigation.
        w=copy.deepcopy(self.world);route=[xy(w.palavra(i,8))]
        for _ in range(1800):
            try:w.atualizar_movimento(i)
            except NotImplementedError:return route,'rota parcial · requer função ausente'
            p=xy(w.palavra(i,8))
            if p!=route[-1]:route.append(p)
            if w.unidades[i*276+2]==7:
                return route,('prévia do motor concluída' if p==self.requested[i] else 'destino efetivo alterado pelo motor')
        return route,'prévia interrompida pelo limite de 1.800 atualizações'
    def step(self,n=1):
        if self.world is None:raise ValueError('Modo de inspeção sem simulação')
        if not isinstance(n,int) or not 1<=n<=200:raise ValueError('Quantidade de atualizações inválida')
        for _ in range(n):
            self.tick+=1;self.world.tick=self.tick
            for i in range(3):
                if i in self.blocked:continue
                before=self.world.unidades[i*276+2]
                if self.session and before==1:continue
                try:self.world.atualizar_movimento(i)
                except NotImplementedError as e:
                    self.blocked[i]=str(e);self.log(f'U{i} bloqueada: {e}');self.paused=True
                p=xy(self.world.palavra(i,8))
                if p!=self.trails[i][-1]:self.trails[i].append(p)
                if before==2 and self.world.unidades[i*276+2]==7:
                    reached=p==self.requested.get(i)
                    self.log(f'U{i}: '+('destino solicitado alcançado.' if reached else 'ordem encerrada sem alcançar o destino solicitado.'))
            if self.session:
                try:self.session.step()
                except NotImplementedError as e:
                    self.session.stop(str(e));self.paused=True
            if not self.session and all(i in self.blocked or self.world.unidades[i*276+2]!=2 for i in range(3)):
                self.paused=True
    def capabilities(self):
        return [
            {'name':'Movimento físico e ordens','status':'confirmado','detail':'Python: SetDeplaceEngin, RotateEngin, AvanceEngin e conclusão da ordem. Cenário e relógio do visualizador são sintéticos.'},
            {'name':'Colisões e desvios locais','status':'confirmado','detail':'Python: EnginPeutPasser / EnginNextCase / Chemin_Remap. Rota exibida é prévia isolada do mesmo motor, mantendo as outras unidades paradas.'},
            {'name':'Busca de caminhos em Python','status':'confirmado' if PYTHON_SOLVER_AVAILABLE else 'pendente','detail':('SolucionadorCaminhosPython: preparação, contornos, seleção e otimização, classes 1–3. Ativo. Procedência: ferramentas/solucionador_python.py; documentacao/CONTORNOS.md; relatorios/desvios-python.json, todos neste commit.' if self.backend=='python' else 'Busca geral desativada por escolha do modo local. O estado 3 fica bloqueado.') if PYTHON_SOLVER_AVAILABLE else 'O snapshot não oferece busca independente; SolucionadorOriginal exige x86/Unicorn.'},
            {'name':'Estruturas, aliados e efeitos especiais','status':'pendente','detail':'Grade auxiliar de estruturas com bit 0x8000, ordens para liberar aliados, atropelamento e efeitos não integrados continuam recusados; alguns ramos ainda exigem o original x86/Unicorn. Nenhum backend x86 é carregado.'},
            {'name':'Terreno e quadros do CD','status':'confirmado','detail':'CMP/PIE/ETA extraídos pelos leitores commitados, com SHA-256 das fontes conferido. IDs do terreno usam quadro[id − 1].'},
            {'name':'Representação de unidades e obstáculos','status':'experimental','detail':'A visão do jogo usa quadros originais ilustrativos, minimapa e HUD. Associação quadro/tipo/animação, marcadores, setas, blocos e composição do laboratório são provisórios. O screenshot enviado é referência visual, não evidência de regras.'},
            {'name':'Missão 1','status':'experimental','detail':'Terreno e posições vêm de MONDE01.ETA. Inspeção sem simulação: estruturas, objetos dinâmicos, névoa e pós-carga completa não reconstruídos nesta vista.'},
            {'name':'Economia: saldos, capacidade e excedentes','status':'confirmado','detail':'Snapshot concluído do chat de economia: consultas, crédito/débito, depósito, retirada, recálculo e sacolas. Bancada com construção sintética tipo 3 e 1 armazém × 100; produção, coleta, recrutamento e filas continuam pendentes.'},
            {'name':'Combate: seleção, alcance e mira','status':'confirmado','detail':'Snapshot concluído do chat de alvos: seleção, validade, alcance, linha, mira angular e portões de recarga. Consultas e prévia de ordem sobre cópia; animação, projéteis e dano integrado continuam pendentes.'}
        ]
    def state(self,include_map=False):
        units=[]
        if self.world is None:
            for u in self.mission['unidades']:
                units.append({'id':u['indice'],'type':u['tipo'],'name':self.catalog[u['tipo']]['nome'] if u['tipo']<26 else 'desconhecido','pos':[u['posicao']['x'],u['posicao']['y']],'offset':[0,0],'state':u['byte_estado'],'pathState':u['estado_caminho'],'direction':9,'next':xy(u['celula_passo']),'target':xy(u['celula_destino']),'requested':None,'trail':[],'route':[],'plan':'posição extraída do arquivo; sem simulação','blocked':None,'owner':u['proprietario_id'],'health':u['vida_no_arquivo']})
        else:
            for i in range(3):
                u=self.world.ler_unidade(i);signed=lambda b:b-256 if b>127 else b
                units.append({'id':i,'type':u[1],'name':self.catalog[u[1]]['nome'],'pos':xy(self.world.palavra(i,8)),'offset':[signed(u[0x86])/32,signed(u[0x87])/32],'progress':u[0x97],'state':u[2],'pathState':u[0x88],'direction':u[0x91],'next':xy(self.world.palavra(i,0x7c)),'target':xy(self.world.palavra(i,0x7e)),'requested':self.requested.get(i),'trail':self.trails[i],'route':self.routes[i],'plan':self.plans[i],'blocked':self.blocked.get(i),'owner':u[0],'health':self.world.palavra(i,0x9a)})
        result={'scenario':self.scenario,'backend':self.backend,'pythonSolverAvailable':PYTHON_SOLVER_AVAILABLE,'width':self.width,'height':self.height,'tick':self.tick,'paused':self.paused,'speed':self.speed,'selected':self.selected,'units':units,'searches':len(self.world.historico_navegacao) if self.world else 0,'collisions':self.world.colisoes[-40:] if self.world else [],'research':self.research.state(),'fog':[self.world.descoberto[0][cell(x,y)] for y in range(self.height) for x in range(self.width)] if self.world else None,'events':self.events[-12:],'commit':MANIFEST['commit'],'snapshotFiles':len(MANIFEST['files']),'capabilities':self.capabilities(),'python':sys.version.split()[0],'architecture':__import__('platform').machine()}
        if self.session:
            result['session']=self.session.state()
            result['clock']={'mode':'elapsed','rate':20,'maxCatchupSeconds':1,
                             'maximumObservedInterval':self.pump_max,
                             'recentIntervals':self.pump_intervals[-16:]}
            result['capabilities']=[
                {'name':'Sessão de treino interativa','status':'experimental','detail':'Mapa, relógio, transporte de carga e objetivos são regras declaradas deste exercício. Movimento e desvios usam as APIs recuperadas no mesmo commit.'},
                {'name':'Golpes diretos em unidades','status':'confirmado','detail':'Soldado adjacente: ordem, mira, animação, recarga e consumidor de dano em modo 1. Câmera sonora oculta; sem reação, diplomacia ou apresentação de InfligeDegat. O golpe letal pausa antes da rotina pendente.'},
                {'name':'Sacolas e depósito','status':'experimental','detail':'Retirada de uma unidade e depósito com capacidade usam as rotinas econômicas. O transporte entre células é regra do treino; não é o chamador original de coleta.'},
                {'name':'Corpos gráficos recuperados','status':'confirmado','detail':'Tipos 0/7/9 do jogador 0, estados 2/7, com paleta e opacidade recuperadas. Outros estados e o adversário usam marcadores; sombra e quadro global ainda não estão integrados.'},
                {'name':'Campanha, som, produção e morte completos','status':'pendente','detail':'Missão 1 permanece em inspeção. Áudio, carga/dispatch completos, morte visível, saída completa de recrutamento, salvar/carregar e fidelidade global não são oferecidos.'}]
            for info in units:
                u=self.world.ler_unidade(info['id'])
                if u[0]==0 and u[1] in (0,7,9) and u[2] in (2,7) and u[0xa4]<8:
                    info['spriteKey']=f'{u[1]}/{u[0x91]}/{u[0xa4]}/{int(self.world.palavra(info["id"],0xa)!=0)}'
        if include_map:
            result['atlas']=json.loads((ROOT/'assets/atlas.json').read_text())
            if (ROOT/'assets/unidades.json').exists():result['unitAtlas']=json.loads((ROOT/'assets/unidades.json').read_text())
            result['map']={'tiles':self.mission['terreno'],'attributes':self.mission['atributos'],'objects':self.mission['objetos']} if not self.world else {'tiles':[1+((x*13+y*7)%4) for y in range(16) for x in range(16)],'obstacles':self.obstacles}
        return result
    def handle(self,msg):
        action=msg.get('action')
        if action=='init':return self.state(True)
        if action=='reset':self.reset(msg.get('scenario','obstaculo'),msg.get('backend'));return self.state(True)
        if action=='select':self.selected=self._index(msg['unit'])
        elif action=='order':self.order(self._index(msg.get('unit',self.selected)),msg['x'],msg['y'])
        elif action=='pause':self.paused=True;self.pump_time=None
        elif action=='play':
            if self.world is None:raise ValueError('Modo de inspeção sem simulação')
            self.paused=False;self.pump_time=time.monotonic()
        elif action=='speed':
            speed=msg['speed']
            if isinstance(speed,bool) or speed not in (0.25,0.5,1,2,4,8):raise ValueError('Velocidade inválida')
            self.speed=speed
            if self.session and not self.paused:self.pump_time=time.monotonic()
        elif action=='step':self.paused=True;self.pump_time=None;self.step()
        elif action=='pump':
            if not self.paused:
                if self.session:
                    now=time.monotonic()
                    elapsed=max(0,now-self.pump_time) if self.pump_time is not None else 0
                    self.pump_time=now
                    self.pump_max=max(self.pump_max,elapsed)
                    self.pump_intervals.append(elapsed);self.pump_intervals=self.pump_intervals[-16:]
                    # The WebView may coalesce background timers. Account for
                    # elapsed time, bounding sleep/wake catch-up to one second.
                    self.pump_fraction+=min(elapsed,1)*20*self.speed
                else:self.pump_fraction+=2*self.speed
                n=int(self.pump_fraction+1e-8);self.pump_fraction=max(0,self.pump_fraction-n)
                if n:self.step(n)
        elif action=='economy':self.log(self.research.mutate(msg))
        elif action=='combat':self.research.combat(self.world,self._index(msg.get('unit',self.selected)),self._index(msg['target']))
        elif action=='interact':
            if not self.session:raise ValueError('Abra a sessão jogável para interagir.')
            self.session.interact(msg.get('operation'),self._index(msg.get('unit',self.selected)),msg.get('target',2))
        elif action=='state':pass
        else:raise ValueError('Ação desconhecida')
        return self.state()


def main():
    preview=Preview()
    for line in sys.stdin:
        try:
            req=json.loads(line);response={'id':req.get('id'),'ok':True,'state':preview.handle(req)}
        except Exception as e:
            response={'id':req.get('id') if isinstance(locals().get('req'),dict) else None,'ok':False,'error':str(e),'state':preview.state()}
            traceback.print_exc(file=sys.stderr)
        print(json.dumps(response,ensure_ascii=False,separators=(',',':')),flush=True)
if __name__=='__main__':main()
