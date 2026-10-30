"""Frame-addressed input interchange. No game memory, engine calls or wall clock.

Missions owns validation and literal per-poll semantics. Reference poll schedules
are requests, not predicted control flow; WndProc flag stores are game outputs.
"""
import ast
import copy
from functools import lru_cache
import hashlib
import json
from pathlib import Path

SCHEMA = 'rising-lands/monde01-scripted-input/1'
VKEYS = (13,16,17,18,27,32,37,38,39,40,46,88)
MESSAGE_VKEYS=VKEYS+tuple(range(0x30,0x3a))
MESSAGES = (0x100,0x101,*range(0x200,0x206))
SCANS = {13:0x1c,16:0x2a,17:0x1d,18:0x38,27:1,32:0x39,37:0x4b,38:0x48,39:0x4d,40:0x50,46:0x53,88:0x2d}

SCANS.update({0x30:0x0b,**{k:k-0x31+2 for k in range(0x31,0x3a)}})

@lru_cache(maxsize=8)
def owner_contract(root):
    """Load only the owner's pure schema definitions, never its emulator harness.

    This is the unchanged validator AST, not a second validator implementation.
    A new dependency fails explicitly rather than substituting another validator.
    """
    path=Path(root)/'pesquisas-paralelas/missoes/m3/entrada_roteirizada.py'
    tree=ast.parse(path.read_text());names={'ESQUEMA','QUADRO_INICIAL','MENSAGENS','_inteiro','carregar_entrada'}
    nodes=[n for n in tree.body if (isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names) or
           (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets))]
    found={n.name for n in nodes if isinstance(n,ast.FunctionDef)}
    if found!={'_inteiro','carregar_entrada'}:raise ValueError('MissionsInputContractUnavailable')
    namespace={};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),namespace)
    if namespace['ESQUEMA']!=SCHEMA or namespace['QUADRO_INICIAL']!=128:raise ValueError('MissionsInputContractVersionMismatch')
    return namespace,hashlib.sha256(path.read_bytes()).hexdigest()


def integer(value):
    if type(value) is not int:raise ValueError('A game-frame integer is required')
    return value


def coordinates(x,y):
    if not (type(x) is int and type(y) is int and 0<=x<800 and 0<=y<600):raise ValueError('Cursor outside 800x600')
    return x,y


def canonical(value):
    return (json.dumps(value,ensure_ascii=False,sort_keys=True,indent=1)+'\n').encode('utf-8')


class ScriptedInput:
    def __init__(self,root,data):
        if isinstance(data,(bytes,str)):data=json.loads(data)
        self.root=Path(root).resolve();owner,_=owner_contract(str(self.root))
        self.frames,self.stop_frame=owner['carregar_entrada'](data)
        if self.stop_frame<128:raise ValueError('Script stop precedes frame128')
        self.metadata=copy.deepcopy({k:v for k,v in data.items() if k!='frames'})
        self.metadata['stop_frame']=self.stop_frame

    def export(self):
        data=copy.deepcopy(self.metadata);data['frames']=[]
        for frame,(cursor,messages,keys) in sorted(self.frames.items()):
            row={'frame':frame}
            if cursor is not None:row['cursor']=list(cursor)
            if messages:row['messages']=[list(x) for x in messages]
            if keys:row['keys']={hex(k):v for k,v in sorted(keys.items())}
            data['frames'].append(row)
        return data

    def export_bytes(self):return canonical(self.export())


class FrameAnswerMapper:
    """Consume explicit poll requests in order, exactly as Missions' handlers do."""
    def __init__(self,script,*,hwnd):
        if type(hwnd) is not int or not 0<=hwnd<=0xffffffff:raise ValueError('Explicit original HWND required')
        self.script=script;self.hwnd=hwnd;self.frame=128;self.cursor=(0,0);self.queue=[];self.keys={};self.pending=None;self.translated=False

    def begin_frame(self,frame):
        if type(frame) is not int or not self.frame<frame<=self.script.stop_frame:raise ValueError('Poll frames must advance within the script')
        if self.queue or self.pending is not None:raise ValueError('Unconsumed frame messages')
        # A cursor declaration holds through skipped frames; keys never do.
        for k in sorted(k for k in self.script.frames if self.frame<k<=frame):
            cursor,_,_=self.script.frames[k]
            if cursor is not None:self.cursor=cursor
        _,messages,keys=self.script.frames.get(frame,(None,(),{}))
        if any(self.script.frames[k][1] for k in self.script.frames if self.frame<k<frame):raise ValueError('Skipped frame with messages')
        self.frame=frame;self.queue=list(messages);self.keys=dict(keys)

    def declared_answers(self):
        """The ABI consumes these declarations; its emitted poll sites verify them.

        Only an explicit cursor change is sent. Omitted cursor holds in the engine,
        and key answers are the full literal table for this frame (no key carry).
        """
        cursor=self.script.frames.get(self.frame,(None,(),{}))[0]
        return dict(cursor=cursor,messages=list(self.queue),keys=dict(self.keys))

    def poll(self,kind,*,phase,site,vk=None):
        if phase not in (f'between_frames{self.frame}',f'frame{self.frame}'):raise ValueError('Poll phase/frame mismatch')
        address=int(site,0) if isinstance(site,str) else site
        if type(address) is not int or not 0<address<=0xffffffff:raise ValueError('Original poll return address required')
        row=dict(frame=self.frame,phase=phase,kind=kind,site=hex(address))
        if kind=='cursor':row.update(x=self.cursor[0],y=self.cursor[1])
        elif kind=='key':
            if type(vk) is not int or not 0<vk<256:raise ValueError('Invalid poll vkey')
            row.update(vk=vk,value=self.keys.get(vk,0))
        elif kind=='peek_message':row['message']=list(self.queue[0]) if self.queue else None
        elif kind=='get_message':
            if not self.queue or self.pending is not None:raise ValueError('GetMessageA without a pending queue entry')
            self.pending=self.queue.pop(0);self.translated=False;row['message']=list(self.pending)
        elif kind=='translate_message':
            if self.pending is None or self.translated:raise ValueError('TranslateMessage without GetMessageA')
            self.translated=True;row['result']=0
        elif kind=='dispatch_message':
            if self.pending is None or not self.translated:raise ValueError('DispatchMessageA without TranslateMessage')
            row.update(message=list(self.pending),hwnd=self.hwnd,wndproc='0x4181a1');self.pending=None;self.translated=False
        else:raise ValueError('Unsupported poll request: '+str(kind))
        return row

    def finish(self):
        if self.queue or self.pending is not None:raise ValueError('Unconsumed final messages')


class MacOSSessionRecorder:
    """Frame-stamped human events -> Missions file, without order injection.

    Clicks are fixed k/k+1/k+3 gestures. Moves during a click wait until k+4;
    consecutive clicks serialize. Key transitions remain at their given frames.
    """
    def __init__(self,root):
        self.root=Path(root);self.events=[];self.rows={};self.key_events=[];self.last_frame=128;self.mouse_until=128

    def _row(self,frame):return self.rows.setdefault(frame,{'frame':frame})

    def event(self,frame,event):
        integer(frame)
        if frame<129 or frame<self.last_frame:raise ValueError('Recording needs monotonic game frames >=129')
        # _event validates its complete payload before touching any row.
        value=copy.deepcopy(event);self._event(frame,value)
        self.events.append(dict(frame=frame,event=value));self.last_frame=frame

    def _event(self,frame,event):
        kind=event.get('kind')
        if kind=='mouse':
            msg=event['msg'];x,y=coordinates(event['x'],event['y']);w=event.get('wParam',0)
            if type(msg) is not int or msg not in range(0x200,0x206) or type(w) is not int or not 0<=w<=0xffffffff:raise ValueError('Invalid mouse message')
            if msg in (0x202,0x205):return  # Physical release is recorded; scripted click release is k+3.
            k=max(frame,self.mouse_until+1);lp=(y<<16)|x
            self._row(k)['cursor']=[x,y]
            if msg==0x200:self._row(k).setdefault('messages',[]).append([msg,w,lp]);return
            right=msg==0x204;mask=2 if right else 1
            for f,m,wp in ((k,0x200,w&~3),(k+1,msg,(w&~3)|mask),(k+3,0x205 if right else 0x202,w&~3)):
                self._row(f).setdefault('messages',[]).append([m,wp,lp])
            self.mouse_until=k+3
        elif kind=='key':
            key,down=event['vkey'],event['down']
            if type(key) is not int or key not in MESSAGE_VKEYS or type(down) is not bool:raise ValueError('Unsupported macOS virtual key')
            held=self._held(frame);previous=key in held
            extended=key in (37,38,39,40,46)
            lp=1|(SCANS[key]<<16)|(int(extended)<<24)|(int(18 in held)<<29)|(int(previous)<<30)|(int(not down)<<31)
            self._row(frame).setdefault('messages',[]).append([0x100 if down else 0x101,key,lp])
            self.key_events.append((frame,key,down))
        else:raise ValueError('Unsupported recorded event')

    def _held(self,frame):
        held=set()
        for f,key,down in self.key_events:
            if f<=frame:
                if down:held.add(key)
                else:held.discard(key)
        return held

    def export_script(self,*,stop_frame=None):
        end=max(129,self.last_frame,max(self.rows,default=129)) if stop_frame is None else integer(stop_frame)
        if end<max(self.last_frame,max(self.rows,default=129)):raise ValueError('Export truncates recorded/pending events')
        rows=copy.deepcopy(self.rows);held=set();transitions={}
        for f,key,down in self.key_events:transitions.setdefault(f,[]).append((key,down))
        for frame in range(129,end+1):
            for key,down in transitions.get(frame,[]):
                if down:held.add(key)
                else:held.discard(key)
            polled={hex(k):-32768 for k in sorted(held) if k in VKEYS}
            if polled:rows.setdefault(frame,{'frame':frame})['keys']=polled
        script=ScriptedInput(self.root,dict(schema=SCHEMA,name='macOS recording',start=dict(frame=128,checkpoint='M2.2 frame128'),stop_frame=end,frames=[rows[k] for k in sorted(rows)]))
        return script

    def journal(self):return copy.deepcopy(dict(schema='rising-lands/macos-frame-input-recording/1',policy='record-only',events=self.events))
