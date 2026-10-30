"""Bounded raid AI hit/death/target-loss composition on live original tables.

No task solver or AI frame is advanced. These are the synchronous effects
reached by messages 44/48/49/4a for the raid's behaviour9 group. Other handlers
remain named dependencies at their original indirect-call targets.
"""
from abi_luta_fatal_combate import M32, DependenciaLutaFatal, registradores_exigidos, unidade
from alvos_alcance import a_portee, engin_est_ennemi
from chamadas_quadro_core import caso_estrutura
from reinicio_ia import _Rotinas


class MensagensLuta:
    def __init__(self, memoria, combate, *, adjacente_estrutura=None):
        self.m,self.combate=memoria,combate
        self.adjacente_estrutura=adjacente_estrutura
        self.grupos=_Rotinas(memoria,None)

    def _group(self, index):
        if index==0xffffffff: return 0
        if index>=100: raise ValueError('Protected AI group index requires 0..99')
        return 0x51a9e0+32*index

    def _war(self, owner, conflict):
        if owner>4 or conflict>=16: raise ValueError('Protected raid battle requires owner0..4 and conflict0..15')
        return 0x51bcfc+4420*owner+40+272*conflict

    def _prob_return(self, task, result):
        if task>=100: raise ValueError('Protected task index requires 0..99')
        r=0x512320+96*task;m=self.m
        m.u8(r+0x5e,0);m.u8(r+0x5f,1);m.u32(r+0x14,0);m.u32(r+0x54,result)
        return dict(EAX=r,EDX=task)

    def _war_return(self, owner, conflict, result):
        task=self.m.u32(self._war(owner,conflict)+8)
        return dict(EAX=task,EDX=conflict) if task==M32 else self._prob_return(task,result)

    def _ref(self, encoded):
        encoded&=65535
        if encoded&0x8000:
            index=encoded&0x7fff
            if index>=1000: raise ValueError('Protected battle structure requires0..999')
            return 0x49a0c8+276*index,True
        return unidade(self.m,encoded),False

    def _owner(self, encoded):
        r,building=self._ref(encoded)
        return self.m.u8(r+(4 if building else 0))

    def _health(self, encoded):
        r,building=self._ref(encoded)
        return (self.m.u16(r+10)-self.m.u16(r+6)) if building else self.m.u16(r+0x9a)

    def _priority(self, encoded):
        r,building=self._ref(encoded)
        kind=self.m.u8(r+(8 if building else 1))
        if kind>=(22 if building else 26): raise ValueError('Unknown participating battle type')
        return self.m.u32((0x498d5c if building else 0x498cf4)+4*kind)

    def _damage(self, unit, target):
        source=self.m.u8(unidade(self.m,unit)+1)
        r,building=self._ref(target);kind=26 if building else self.m.u8(r+1)
        if source>=26 or kind>26: raise ValueError('Unknown participating damage type')
        table=self.m.u32(self.m.u32(0x4e199c)+4*source)
        return self.m.u8(table+kind)

    def _range(self, unit, encoded):
        rec=unidade(self.m,unit);owner=self.m.u8(rec);kind=self.m.u8(rec+1)
        modifier=self.combate.bonus.consultar(owner,kind,4)
        building=bool(encoded&0x8000);target=encoded&0x7fff if building else encoded
        def adjacent(index,cell):
            if self.adjacente_estrutura is None:
                raise DependenciaLutaFatal('BatimentAdjacent',0x42381f,(index,cell))
            return self.adjacente_estrutura(index,cell)
        return a_portee(self.combate.unidades,unit,3 if building else 1,target,modifier,
                        celula_construcao=lambda i:caso_estrutura(self.m,i)['EAX']&65535,
                        adjacente_construcao=adjacent)

    def _order(self, unit, encoded):
        self.combate.definir_ataque(unit,3 if encoded&0x8000 else 1,encoded&0x7fff if encoded&0x8000 else encoded)

    def _assign(self, war, index):
        """0x487eef: fill an enemy's assigned damage, in-range pass then fallback."""
        m=self.m;group=self._group(m.u32(war))
        if not group: return 0
        head=m.u16(group+0x10)
        if not m.u16(group+0x12) or head==65535: return head
        entry=war+16+8*index;encoded=m.u16(entry)
        assigned=m.u16(entry+2);health=self._health(encoded)
        for near in (True,False):
            u=m.u16(group+0x10);seen=set()
            while u!=65535 and assigned<health:
                if u in seen: raise ValueError('Cyclic original unit group')
                seen.add(u);r=unidade(m,u)
                if m.u16(r+0xb8)==65535 and (not near or self._range(u,encoded)):
                    damage=self._damage(u,encoded)
                    if damage>0:
                        assigned+=damage;self._order(u,encoded)
                u=m.u16(r+0x108)
        m.u16(entry+2,assigned)
        return war

    def _add_enemy(self, owner, conflict, encoded):
        """0x487b78: ordered priority/life insertion; returns AL and false-path EDX."""
        m=self.m
        if self._owner(encoded)==owner: return False,conflict
        war=self._war(owner,conflict);count=m.u16(war+14)
        if count>=32: return False,owner*68
        priority=self._priority(encoded)&255;position=-1;candidate=-1
        for i in range(count):
            e=war+16+8*i
            if m.u16(e)==encoded:
                d=i if m.u16(e+2) else self._assign(war,i)
                return False,d
            old_priority=m.u16(e+4)
            if old_priority==priority:
                if self._health(encoded)<self._health(m.u16(e)): candidate=i
            elif old_priority<priority:
                position=candidate if candidate!=-1 else i;break
        if position==-1:
            position=count;e=war+16+8*count
            m.u16(e+4,priority);m.u16(e,encoded);m.u16(e+2,0)
        else:
            for i in range(count-1,position-1,-1):
                old=war+16+8*i;new=old+8
                m.u32(new,m.u32(old));m.u32(new+4,m.u32(old+4))
            e=war+16+8*position
            m.u16(e+2,0);m.u16(e+4,priority);m.u16(e,encoded)
        m.u16(war+14,count+1)
        return True,self._assign(war,position)

    def _remove_enemy(self, owner, conflict, encoded):
        m=self.m
        if self._owner(encoded)==owner or encoded==65535: return
        war=self._war(owner,conflict);count=m.u16(war+14)
        for i in range(count):
            if m.u16(war+16+8*i)!=encoded: continue
            for j in range(i,count-1):
                src=war+16+8*(j+1);dst=src-8
                m.u32(dst,m.u32(src));m.u32(dst+4,m.u32(src+4))
            m.u16(war+14,count-1);return

    def _unlock(self, unit, conflict):
        m=self.m;r=unidade(m,unit);owner=m.u8(r);target=m.u16(r+0xb8)
        if target==65535: return
        war=self._war(owner,conflict)
        for i in range(m.u16(war+14)):
            e=war+16+8*i
            if m.u16(e)==target:
                m.u16(e+2,max(0,m.u16(e+2)-self._damage(unit,target)));return

    def _new_target(self, unit, conflict):
        m=self.m;owner=m.u8(unidade(m,unit));war=self._war(owner,conflict)
        if not m.u16(war+14):
            cell=m.u32(war+4);radius=m.u16(war+12)
            x,y=cell&255,cell>>8;best=65535;best_priority=0
            players=m.u32(0x5080a8);masks=bytes(m.u8(players+20*i+6) for i in range(5))
            for cy in range(max(0,y-radius),min(255,y+radius)+1):
                for cx in range(max(0,x-radius),min(255,x+radius)+1):
                    tile=cy*256+cx;value=m.u16(m.u32(0x4e0f38)+2*tile)
                    if value&0xc000==0x4000:
                        candidate=(value&0x3ff8)>>3;r=unidade(m,candidate)
                        if m.u8(r+2) not in (0,4) and m.u16(r+0x7c)==tile and engin_est_ennemi(owner,m.u8(r),masks):
                            p=self._priority(candidate)
                            if p>best_priority: best,best_priority=candidate,p
                    if value&0x8000:
                        index=(value&0x7fe0)>>5;r=0x49a0c8+276*index
                        if index>=1000: raise ValueError('Invalid grid structure')
                        if m.u8(r+5) and m.u8(r+5)!=3 and engin_est_ennemi(owner,m.u8(r+4),masks):
                            p=self._priority(index|0x8000)
                            if p>best_priority: best,best_priority=index|0x8000,p
            if best==65535: return best
            self._add_enemy(owner,conflict,best)
        count=m.u16(war+14)
        for near in (True,False):
            for i in range(count):
                e=war+16+8*i;encoded=m.u16(e)
                if self._health(encoded)<=m.u16(e+2) or near and not self._range(unit,encoded): continue
                damage=self._damage(unit,encoded)
                if damage>0:
                    m.u16(e+2,m.u16(e+2)+damage);self._order(unit,encoded);return encoded
        encoded=m.u16(war+16)
        m.u16(war+18,m.u16(war+18)+self._damage(unit,encoded))
        self._order(unit,encoded)
        return encoded

    def mensagem(self, unit, message, argument):
        m=self.m;unit&=65535;r=unidade(m,unit);owner=m.u8(r);message&=255
        player_type=2 if owner>=4 else m.u8(m.u32(0x5080a8)+20*owner+1)
        out=dict(EAX=player_type,EBX=unit,EDX=argument&M32)
        if player_type!=2: return out
        group_index=m.u32(r+0x10c);group=self._group(group_index)
        index=(message-0x41)&255
        out['EAX']=index
        if index>11 or message==0x47 or not group: return out
        conflict=m.u32(group+12)
        if message==0x44:
            if conflict!=M32:
                self._unlock(unit,conflict)
                out['EBX']=M32
                out.update(self._war_return(owner,conflict,M32))
            quantity=m.u16(group+18)
            result=self.grupos.unit_remove_from_group(group_index,unit)
            out.update(EAX=result,EDX=(quantity-1)&M32 if result==0 else 65535)
            flags=m.u32(group+28);task=m.u32(group+8)
            if flags and task!=M32: out.update(self._prob_return(task,1 if flags&1 else M32))
            return out
        behaviour=m.u8(group+27);out['EAX']=behaviour
        if behaviour==255:
            if message==0x4a:
                out['EAX']=conflict
                if conflict!=M32:
                    out['EBX']=1;out.update(self._war_return(owner,conflict,1))
            return out
        slot={0x48:0,0x49:8,0x4a:4}.get(message)
        if slot is None: raise DependenciaLutaFatal(f'iagUnitSendMessage message0x{message:x}',0x482a49,(unit,message,argument))
        handler=m.u32(m.u32(0x498e94+4*behaviour)+slot);out['EAX']=handler
        if not handler:
            if message==0x4a:
                out['EAX']=conflict
                if conflict!=M32:
                    out['EBX']=1;out.update(self._war_return(owner,conflict,1))
            return out
        expected={0x48:0x489bc8,0x49:0x489b5a,0x4a:0x489ca2}[message]
        if behaviour!=9 or handler!=expected:
            raise DependenciaLutaFatal(f'iagUnitSendMessage handler0x{handler:x}',handler,(unit,argument&65535))
        if message in (0x48,0x49):
            out.update(EAX=r,EDX=argument&65535)
            if conflict==M32: return out
            added,d=self._add_enemy(owner,conflict,argument&65535)
            out.update(EAX=int(added),EDX=d)
            if added: out.update(self._war_return(owner,conflict,M32))
            return out
        if conflict!=M32:
            mode=m.u8(r+0xb7)
            if mode in (1,3):
                encoded=m.u16(r+0xb8)|(0x8000 if mode==3 else 0)
                self._remove_enemy(owner,conflict,encoded)
            target=self._new_target(unit,conflict)
        else: target=65535
        if target==65535:
            self.combate.mundo.definir_movimento(unit,m.u16(r+0x7c));m.u16(r+0xb8,65535)
        # The outer message4a resumes the war task after the handler returns.
        conflict=m.u32(group+12)
        if conflict!=M32:
            out['EBX']=1;out.update(self._war_return(owner,conflict,1))
        else: out.update(EAX=M32,EDX=r)
        return out

    def chamar(self, nome, regs, *, chamada=None):
        if nome!='iagUnitSendMessage': raise KeyError(nome)
        out=registradores_exigidos(nome,0x4829c8 if chamada is None else chamada,regs)
        out.update(self.mensagem(out['EAX'],out['EDX'],out['EBX']))
        return out
