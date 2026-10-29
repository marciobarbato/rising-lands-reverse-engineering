"""Core's som(nome, registradores, pilha) -> EAX over explicit live memory.

No initialization, device, allocator, callback, or unchanged-EAX fallback.
The unopened-display domain is the accepted private image (Manage may clear
its dirty word). Initialized replay requires an exact frozen native case.
"""
import json
from pathlib import Path

import ambiente_audio
from bancos_som import DependenciaSom
from fila_audio import AudioQueue
from audio_queue_fixtures import ScriptedCOM, decode
from fluxo_pedidos_audio import ARGUMENTS, u32

OWNED=Path(__file__).resolve().parent
ENTRIES={'PlaySnd_PostSound':0x48aa79,'PlaySnd_StopSound':0x48aac0,'PlaySnd_Manage':0x48aaca}
OPERATIONS={'PlaySnd_PostSound':'post','PlaySnd_StopSound':'stop_handle','PlaySnd_Manage':'manage'}


class LiveAudioMemory:
    """Adapter for Core u8/u16/u32(addr, value=None), vista(addr, size).

    No copy: queue writes, caller handles and all aliases stay in the caller's
    memory. The existing queue uses explicit w8/w16/w32/read/write/view names.
    """
    def __init__(self,memory): self.memory=memory
    def u8(self,a): return self.memory.u8(a)
    def u16(self,a): return self.memory.u16(a)
    def u32(self,a): return self.memory.u32(a)
    def w8(self,a,v): self.memory.u8(a,v&255)
    def w16(self,a,v): self.memory.u16(a,v&65535)
    def w32(self,a,v): self.memory.u32(a,v&0xffffffff)
    def view(self,a,n): return self.memory.vista(a,n)
    def read(self,a,n): return bytes(self.view(a,n))
    def write(self,a,data): self.view(a,len(data))[:]=data


def _snapshot_matches(memory,snapshot):
    return all(memory.read(int(r['base'],16),len(decode(r['zlib_base64'])))==decode(r['zlib_base64']) for r in snapshot)


def native_case(artifact,name):
    """Read a case only from the committed initialized reference corpus."""
    allowed=('captura-fila-audio-original-v9.json','captura-continuacao-audio-original-v3.json',
             'captura-dictador-audio-original-v3.json')
    if artifact not in allowed: raise ValueError('Unknown initialized native corpus')
    document=json.loads((OWNED/'evidencias'/artifact).read_bytes())
    return next(c for c in document['cases'] if c['name']==name)


class SoundRequestProvider:
    """Explicit domain: ``unopened-display`` or ``captured-initialized``.

    ``memory`` is the queue memory interface; use LiveAudioMemory for Core.
    ``stream`` is optional, but when supplied ``phase`` and ``caller_return``
    must be set before every call. Logging precedes effects and dependency stops.

    Initialized replay additionally takes (artifact, case name). It admits only
    the exact frozen input and each recorded sequence transition, and supplies
    precisely that case's declared platform transcript. It does not establish
    real device initialization or general initialized mission playback.
    """
    def __init__(self,memory,*,domain,stream=None,capture=None):
        self.memory,self.domain,self.stream=memory,domain,stream
        self.phase=self.caller_return=None
        self.step=0; self.case=None
        if domain=='unopened-display':
            if capture is not None: raise ValueError('Display domain takes no initialized fixture')
            fixture=json.loads((OWNED/'evidencias/m3-pedidos-original-v1.json').read_bytes())['cases'][0]['input']
            self.private=fixture['memory'][:2]
            self.queue=AudioQueue(memory,None)
        elif domain=='captured-initialized':
            if capture is None: raise ValueError('Initialized domain requires a frozen capture identity')
            self.case=native_case(*capture)
            if self.case['stop']: raise ValueError('An unresolved native case is not a runnable provider domain')
            self.plan=ScriptedCOM(self.case['input']['com'])
            self.queue=AudioQueue(memory,self.plan)
        else: raise ValueError('Unknown sound provider domain')

    def _display_domain(self,address):
        m=self.memory
        for region in self.private:
            base=int(region['base'],16); expected=bytearray(decode(region['zlib_base64']))
            actual=bytearray(m.read(base,len(expected)))
            if base<=0x498f5c<base+len(expected):
                offset=0x498f5c-base
                if m.u32(0x498f5c) not in (0,1): raise DependenciaSom(address,'Uncaptured sound dirty word')
                actual[offset:offset+4]=expected[offset:offset+4]
            if actual!=expected: raise DependenciaSom(address,'Outside accepted unopened private sound image')

    def __call__(self,nome,registradores,pilha):
        if nome not in ENTRIES: raise DependenciaSom(0x48aa79,'Unsupported sound entry: '+nome)
        names,count=ARGUMENTS[nome]
        if len(pilha)!=count: raise ValueError('Sound argument stack length')
        regs={k:u32(registradores[k]) for k in names}; args=[u32(v) for v in pilha]
        if self.stream is not None:
            if self.phase is None or self.caller_return is None: raise ValueError('Sound stream needs call-site context')
            self.stream.append(self.phase,self.caller_return,nome,regs,args)
        entry=ENTRIES[nome];m=self.memory
        if self.domain=='unopened-display':
            self._display_domain(entry)
            reference=regs.get('EBX') if nome=='PlaySnd_PostSound' else regs.get('EAX')
            if nome!='PlaySnd_Manage' and (nome!='PlaySnd_PostSound' or regs['EAX'] in (0x41,0x42,0x50)):
                if m.u32(reference)!=0xffffffff: raise DependenciaSom(entry,'Unopened display requires a free caller handle')
        else:
            f=self.case['input']; requests=f.get('sequence',[f])
            if self.step>=len(requests): raise DependenciaSom(entry,'Frozen initialized sequence exhausted')
            request=requests[self.step]
            before=f['memory'] if self.step==0 else self.case['steps'][self.step-1]['memory']
            if request['operation']!=OPERATIONS[nome]:
                raise DependenciaSom(entry,'Outside frozen initialized request sequence')
            expected_regs={k:u32(request['regs'][k]) for k in names}
            if request['operation']!=OPERATIONS[nome] or regs!=expected_regs or args!=request['arguments'] or not _snapshot_matches(m,before):
                raise DependenciaSom(entry,'Outside frozen initialized request/state transition')
        if nome=='PlaySnd_PostSound': result=self.queue.post(regs['EAX'],regs['EDX'],regs['EBX'],regs['ECX'],args[0])
        elif nome=='PlaySnd_StopSound': result=self.queue.stop_handle(regs['EAX'])
        else: result=self.queue.manage()
        if self.case is not None: self.step+=1
        return result
