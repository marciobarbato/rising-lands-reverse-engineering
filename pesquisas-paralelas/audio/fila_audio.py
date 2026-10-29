"""Bounded original queue admission, record movement and explicit COM status.

All state comes from caller-owned read/write/view memory. Constructors neither
initialize audio nor supply a backend response. Unknown branches stop after
retaining earlier effects. No mixer or asynchronous device state is invented.
"""
from bancos_som import BancoSom,DependenciaSom,carregar_info_som
from adpcm_som import criar_superficie_som
from types import SimpleNamespace

TABLE,STRIDE,INDEX=0x52137c,44,0x498f68


def _u32(value):return value&0xffffffff

def _i32(value):return value-0x100000000 if value&0x80000000 else value


class _LiveVariantCounter:
    def __init__(self,memory):self.memory=memory
    @property
    def contador_variantes(self):return self.memory.u32(0x5221bc)
    @contador_variantes.setter
    def contador_variantes(self,value):self.memory.w32(0x5221bc,value)


class _QueuePCMFiles:
    def __init__(self,queue,device):self.queue,self.device=queue,device
    def posicionar(self,handle,offset,origin):
        return self.queue.call('_llseek',handle,(offset,origin),0x48c05e)['hresult']
    def ler(self,handle,size):
        answer=self.queue.call('_hread',handle,(self.device.lock_pointer,size),0x48c042)
        data=bytes.fromhex(answer['value'])
        if len(data)>size or answer['hresult']!=len(data):
            raise DependenciaSom(0x48c042,'Read answer outside captured explicit-byte domain')
        return data


class _QueuePCMDevice:
    """Adapter to the already validated Stage-1 PCM body; no device defaults."""
    def __init__(self,queue):self.queue=queue;self.buffers={};self.created_size=None;self.lock_pointer=None
    def criar(self,descriptor,wave):
        q=self.queue
        answer=q.call('CreateSoundBuffer',q.memory.u32(0x522228),(descriptor.hex(),wave.hex(),0),0x48b834)
        if type(answer.get('value')) is not int or not 0<=answer['value']<=0xffffffff:
            raise DependenciaSom(0x48b834,'CreateSoundBuffer requires an explicit u32 output pointer write')
        self.created_size=int.from_bytes(descriptor[8:12],'little')
        return answer['value']
    def travar(self,pointer,offset,size,flags):
        answer=self.queue.call('Lock',pointer,(offset,size,flags),0x48c097)
        outputs=answer.get('value')
        if not isinstance(outputs,dict) or set(outputs)!={'pointer','size'}:
            raise DependenciaSom(0x48c097,'Lock requires explicit pointer and byte-count writes')
        if any(type(outputs[key]) is not int or not 0<=outputs[key]<=0xffffffff for key in outputs):
            raise ValueError('Lock output pointer and size require u32 values')
        if outputs['size']!=size or size!=self.created_size:
            raise DependenciaSom(0x48c097,'Wrapped/short Lock outputs outside captured PCM domain')
        self.lock_pointer=outputs['pointer'];self.buffers[pointer]=self.queue.memory.view(self.lock_pointer,size)
        return 0
    def destravar(self,pointer,offset,size,second,second_size):
        return self.queue.call('Unlock',pointer,(self.lock_pointer+offset,size,second,second_size),0x48c0b5)['hresult']


class AudioQueue:
    def __init__(self,memory,external):
        self.memory,self.external=memory,external

    def call(self,name,pointer,args,site):
        if self.external is None:raise DependenciaSom(site,'Explicit external answer required: '+name)
        try:answer=self.external.answer(name,pointer,list(args))
        except ValueError as exc:raise DependenciaSom(site,str(exc)) from exc
        if type(answer.get('hresult')) is not int or not 0<=answer['hresult']<=0xffffffff:
            raise ValueError('External answer requires an explicit u32 result')
        return answer

    def status(self,pointer,kind):
        if not pointer:return 1 if kind=='stopped' else 0
        answer=self.call('GetStatus',pointer,(),{'playing':0x48bea0,'stopped':0x48bed0,'looped':0x48beeb}[kind])
        if type(answer.get('value')) is not int or not 0<=answer['value']<=0xffffffff:
            raise DependenciaSom(0x48bea3,'GetStatus must explicitly write a u32 status word')
        value=answer['value']
        return int(value&5==0) if kind=='stopped' else int(bool(value&({'playing':1,'looped':4}[kind])))

    def stop_buffer(self,pointer):
        if self.status(pointer,'stopped'):return 1
        return int(self.call('Stop',pointer,(),0x48bfa9)['hresult']==0)

    def _index(self,value,site):
        if type(value) is not int or not 0<=value<=70:raise DependenciaSom(site,'Queue record index outside 0..70')
        return value

    def address(self,index):return TABLE+self._index(index,0x48a218)*STRIDE

    def maximum(self):
        value=self.memory.u32(INDEX)
        if not 19<=value<=70:raise DependenciaSom(0x48aefa,'Waiting maximum index outside 19..70')
        return value

    def reserve(self):
        value=self.maximum()
        if value==70:return 0xffffffff
        self.memory.w32(INDEX,value+1);return value+1

    def give_back(self):
        value=self.maximum()
        if value!=19:self.memory.w32(INDEX,value-1)

    def compact(self,address,clear):
        m=self.memory;self._index((address-TABLE)//STRIDE,0x48af1b)
        if (address-TABLE)%STRIDE:raise DependenciaSom(0x48af1b,'Unaligned queue record')
        reference=m.u32(address+40);saved=m.u32(reference)
        if self.maximum()==19:return 0
        if clear:m.w32(reference,0xffffffff)
        last=self.address(self.maximum())
        if last!=address:
            m.write(address,m.read(last,44))
            m.w32(m.u32(address+40),saved)
        m.w8(self.address(self.maximum())+8,0)
        m.w32(INDEX,self.maximum()-1)
        return 1

    def destroy_waiting(self,index):
        m=self.memory;r=self.address(index);maximum=self.maximum()
        if index==maximum:
            m.w32(INDEX,maximum-1);m.w8(r+8,0);return 0
        saved=m.u32(m.u32(r+40))
        if maximum==19:return 1
        last=self.address(maximum)
        if last!=r:
            m.write(r,m.read(last,44));m.w32(m.u32(r+40),saved)
        m.w32(INDEX,self.maximum()-1);m.w8(last+8,0)
        return 1

    def permute(self,a,b):
        m=self.memory
        for r in (a,b):
            if (r-TABLE)%44:raise DependenciaSom(0x48b317,'Unaligned queue record')
            self._index((r-TABLE)//44,0x48b317)
        temporary=m.read(a,44);m.write(a,m.read(b,44));m.write(b,temporary)
        first_ref,second_ref=m.u32(a+40),m.u32(b+40)
        first,second=m.u32(first_ref),m.u32(second_ref)
        m.w32(first_ref,second);m.w32(second_ref,first)
        first,second=m.u32(a+32),m.u32(b+32)
        m.w32(a+32,second);m.w32(b+32,first)

    def sort(self):
        # WaitSnd_Trier is an original literal RET, proven in the native capture.
        if self.memory.u32(0x521f84)==1:self.memory.w32(0x521f84,0)

    def destroy_buffer(self,slot):
        m=self.memory;pointer=m.u32(slot)
        if pointer:
            self.call('Release',pointer,(),0x48b7a4);m.w32(slot,0)

    def destroy_logical(self,slot):
        m=self.memory
        if self.status(m.u32(slot),'playing'):self.stop_buffer(m.u32(slot))
        self.destroy_buffer(slot);m.w32(slot+4,0)
        maximum=_i32(m.u32(0x498f64))
        if maximum<0:return
        if maximum>9:raise DependenciaSom(0x48add9,'Logical table maximum outside -1..9')
        last=0x52216c+maximum*8
        if slot!=last:
            m.w32(slot,m.u32(last));m.w32(slot+4,m.u32(last+4))
            m.w32(m.u32(slot+4)+32,slot)
            m.w32(last,0);m.w32(last+4,0)
        m.w32(0x498f64,maximum-1)

    def replace_slot(self,slot,logical=False):
        m=self.memory;base,counter=(0x52216c,0x498f64) if logical else (0x52211c,0x498f60)
        maximum=_i32(m.u32(counter))
        if not -1<=maximum<=9:raise DependenciaSom(0x48ad3c if logical else 0x48abdc,'Slot maximum outside -1..9')
        if maximum<0:return 0
        if not base<=slot<=base+9*8 or (slot-base)%8:raise ValueError('Unaligned or undeclared sound slot')
        last=base+maximum*8
        if slot!=last:
            m.w32(slot,m.u32(last));m.w32(slot+4,m.u32(last+4));m.w32(m.u32(slot+4)+32,slot)
            m.w32(last,0);m.w32(last+4,0)
        m.w32(counter,maximum-1);return 1

    def find_loaded(self,sound_id,bank,logical=False):
        m=self.memory;base,counter=(0x52216c,0x498f64) if logical else (0x52211c,0x498f60)
        maximum=_i32(m.u32(counter))
        if not -1<=maximum<=9:raise DependenciaSom(0x48aeb3 if logical else 0x48acd3,'Slot maximum outside -1..9')
        for i in range(maximum+1):
            slot=base+i*8;r=m.u32(slot+4)
            if m.u32(r)==sound_id and m.u32(r+4)==bank:return r if logical else slot
        return 0

    def destroy_physical(self,slot):
        m=self.memory
        if self.status(m.u32(slot),'playing'):self.stop_buffer(m.u32(slot))
        self.destroy_buffer(slot);m.w32(slot+4,0)

    def duplicate_buffer(self,pointer):
        device=self.memory.u32(0x522228)
        if not device or not pointer:return 0
        answer=self.call('DuplicateSoundBuffer',device,(pointer,),0x48bfe6)
        if answer['hresult']:return 0
        output=answer.get('value')
        if type(output) is not int or not 0<=output<=0xffffffff:
            raise DependenciaSom(0x48bfea,'DuplicateSoundBuffer requires explicit u32 output write')
        if output:self.call('SetPosition',output,(0,),0x48bffd)
        return output

    def create_logical(self,pointer,record):
        m=self.memory;maximum=_i32(m.u32(0x498f64))
        if not -1<=maximum<=9:raise DependenciaSom(0x48ae5f,'Logical maximum outside -1..9')
        if maximum==9:return 0
        maximum+=1;m.w32(0x498f64,maximum)
        output=self.duplicate_buffer(pointer);slot=0x52216c+maximum*8;m.w32(slot,output)
        if not output:return 0
        m.w32(slot+4,record);return slot

    def clear_list(self):
        m=self.memory
        for base in (0x52216c,0x52211c):
            for i in range(10):
                slot=base+i*8;pointer=m.u32(slot)
                if not pointer:continue
                r=m.u32(slot+4)
                if m.u8(r+8)==1 and self.status(pointer,'stopped'):self.stop_handle(m.u32(r+40))
        if m.u32(0x521f90):raise DependenciaSom(0x48a0a1,'Dictator lifecycle not yet captured')
        return 1

    def transfer_to_waiting(self,index):
        m=self.memory;source=self.address(index);new=self.reserve()
        if new==0xffffffff:return 0
        destination=self.address(new)
        m.write(destination,m.read(source,44));m.w8(destination+8,2)
        m.w32(destination+32,0);m.w32(m.u32(destination+40),new)
        slot,kind=m.u32(source+32),m.u32(source+36);m.w8(source+8,0)
        if kind==1:self.destroy_logical(slot)
        else:self.destroy_physical(slot)
        return 1

    def transfer_to_playing(self,index):
        m=self.memory;destination=next((i for i in range(20) if m.u8(self.address(i)+8)==0),None)
        if destination is None:return 0
        source,target=self.address(index),self.address(destination)
        m.write(target,m.read(source,44));m.w32(m.u32(target+40),destination)
        m.w32(m.u32(target+32)+4,target);m.w8(target+8,1)
        return self.compact(source,False)

    def load_info(self,record,sound_id,bank,flags,volume):
        m=self.memory;b=BancoSom(m.view(bank,28),bank)
        b.cabecalho=m.view(b.ponteiro_cabecalho,b.quantidade*12)
        return carregar_info_som(_LiveVariantCounter(m),m.view(record,44),sound_id,b,flags,volume)

    def destroy_only_sound(self,r):
        m=self.memory;slot=m.u32(r+32)
        if not slot:return
        if not self.status(m.u32(slot),'stopped'):self.stop_buffer(m.u32(slot))
        if m.u32(r+36)==1:
            self.destroy_logical(slot);m.w32(r+32,0);return
        self.destroy_physical(slot)
        promoted=self.find_loaded(m.u32(r),m.u32(r+4),True)
        if not promoted:self.replace_slot(slot);return
        logical=m.u32(promoted+32)
        m.w32(slot,m.u32(logical));m.w32(slot+4,promoted);m.w32(logical,0);m.w32(logical+4,0)
        m.w32(promoted+32,slot);self.replace_slot(logical,True);m.w32(promoted+36,0)

    def stop_handle(self,reference):
        m=self.memory;index=m.u32(reference)
        if index==0xffffffff:return 0
        r=self.address(index)
        if m.u8(r+8)==1:self.destroy_only_sound(r)
        if m.u32(m.u32(r+40))!=0xffffffff and m.u8(r+8):
            if m.u8(r+8)==2:self.compact(r,True)
            else:m.w32(m.u32(r+40),0xffffffff);m.w8(r+8,0);m.w32(r+32,0)
        return 1

    def set_volume(self,reference,volume):
        m=self.memory;index=m.u32(reference)
        if index==0xffffffff:return 0
        r=self.address(index)
        if not m.u8(r+8):return 1
        m.w32(r+16,volume)
        if m.u16(m.u32(r+24)+4)==256:return 0
        if not volume:self.stop_handle(reference)
        elif m.u8(r+8)==1:m.w32(0x521f88,1);m.w32(r+20,1)
        return 1

    def insert(self,sound_id,bank,reference,flags,volume):
        m=self.memory;index=m.u32(reference)
        if index!=0xffffffff:
            r=self.address(index)
            if volume==0 and m.u16(m.u32(r+24)+4)!=256:
                self.stop_handle(reference);return 1
            if m.u32(r)==sound_id and m.u32(r+4)==bank:
                self.set_volume(reference,volume);return 1
            if m.u8(r+8)==1:
                self.stop_handle(reference);index=self.reserve();m.w32(reference,index)
                if index==0xffffffff:return 0
                m.w32(0x521f84,1)
            r=self.address(m.u32(reference))
            self.load_info(r,sound_id,bank,flags,volume)
            m.w32(r+40,reference);m.w8(r+8,2);return 1
        index=self.reserve()
        if index==0xffffffff:return 0
        r=self.address(index)
        if not self.load_info(r,sound_id,bank,flags,volume):self.give_back();return 0
        m.w32(reference,index);m.w32(r+40,reference);m.w8(r+8,2);m.w32(r+20,0);m.w32(0x521f84,1)
        return 1

    def post(self,selector,sound_id,reference,flags,volume):
        banks={0x41:0x521fc8,0x42:0x521fe4,0x50:0x522000}
        if selector not in banks:return sound_id # Original EAX is EDX, not invented zero.
        return self.insert(sound_id,banks[selector],reference,flags&255,volume)

    def volume_word(self,r):
        m=self.memory;multiplier=m.u8(m.u32(r+28)+13) or 256
        if m.u16(m.u32(r+24)+4)==256:m.w32(r+16,256)
        lookup=_i32(_u32(_u32(m.u32(r+16)*multiplier)*m.u32(0x498f58)))>>20
        if not 0<=lookup<=16:raise DependenciaSom(0x48a5c2,'Volume lookup outside captured table domain')
        return m.u32(0x498f14+lookup*4)

    def start_buffer(self,r):
        m=self.memory;pointer=m.u32(m.u32(r+32));volume=self.volume_word(r)
        if not pointer:return 0
        if self.status(pointer,'playing'):return 1
        if self.call('SetPosition',pointer,(0,),0x48bf3a)['hresult']:return 0
        if self.call('SetVolume',pointer,(volume,),0x48bf45)['hresult']:return 0
        return int(self.call('Play',pointer,(0,0,int(m.u32(r+12)==1)),0x48bf62)['hresult']==0)

    def create_pending_pcm(self,r):
        m=self.memory;bank=BancoSom(m.view(m.u32(r+4),28),m.u32(r+4));header=m.read(m.u32(r+28),16)
        if header[12]!=0 or bank.em_memoria!=0:
            raise DependenciaSom(0x48aad4,'Queue bridge currently captures file-backed PCM only')
        device=_QueuePCMDevice(self);files=_QueuePCMFiles(self,device)
        system=SimpleNamespace(directsound=device,arquivos=files)
        globals_=SimpleNamespace(directsound=m.u32(0x522228))
        pointer,_=criar_superficie_som(system,globals_,bank,header)
        slot=0x52211c+8*m.u32(0x498f60);m.w32(slot,pointer)
        if not pointer:return 0
        m.w32(slot+4,r);m.w32(r+32,slot);m.w32(r+36,0)
        result=self.start_buffer(r);self.transfer_to_playing((r-TABLE)//STRIDE);m.w32(0x521f84,1)
        return result

    def manage(self):
        m=self.memory
        for base in (0x52216c,0x52211c):
            for i in range(10):
                slot=base+i*8;pointer=m.u32(slot)
                if not pointer:continue
                r=m.u32(slot+4)
                if m.u8(r+8)==1 and self.status(pointer,'stopped'):self.stop_handle(m.u32(r+40))
        if m.u32(0x521f90):raise DependenciaSom(0x48a0a1,'Dictator lifecycle not yet captured')
        if m.u32(0x521f88) or m.u32(0x498f5c):
            for i in range(20):
                r=self.address(i)
                if not m.u8(r+8) or m.u32(m.u32(r+40))==0xffffffff:continue
                slot=m.u32(r+32)
                if not slot or not m.u32(slot):continue
                if m.u32(r+20)!=1 and not m.u32(0x498f5c):continue
                value=self.volume_word(r)
                self.call('SetVolume',m.u32(slot),(value,),0x48a5d5);m.w32(r+20,0)
            m.w32(0x521f88,0)
        m.w32(0x498f5c,0)
        if self.maximum()<=19:return 1
        if self.maximum()!=20:
            raise DependenciaSom(0x48a80c,'Multiple pending requests outside captured Manage domain')
        r=self.address(self.maximum())
        if m.u16(m.u32(r+24)+4)==256:raise DependenciaSom(0x48a702,'Dictator request creation not yet captured')
        if _i32(m.u32(0x498f60))!=-1:
            raise DependenciaSom(0x48acd3,'Loaded physical-slot lookup/lifecycle not yet captured')
        m.w32(0x498f60,m.u32(0x498f60)+1)
        return self.create_pending_pcm(r)
