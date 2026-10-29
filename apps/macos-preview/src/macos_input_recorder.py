"""Record-only macOS event mapper. Never writes game memory or engine inputs.

Polls are explicit and ordered. Event arrival alone does not invent an engine
poll site. Raw event/poll journals are distinct from the Missions interchange.
"""
import copy

VKEYS = (0x0d,0x10,0x11,0x12,0x1b,0x20,0x25,0x26,0x27,0x28,0x2e,0x58)
MESSAGES = tuple(range(0x200,0x206))


class InputContractPending(RuntimeError):
    pass


class MacOSInputRecorder:
    def __init__(self):
        self.cursor=(0,0)
        self.held=set()
        self.pressed=set()
        self.queue=[]
        self.events=[]
        self.polls=[]
        self.timeline=[]
        self.last_frame=0

    def event(self, frame, event):
        if type(frame) is not int or frame<self.last_frame:
            raise ValueError('Input frames must be monotonic nonnegative integers')
        kind=event.get('kind')
        if kind=='mouse':
            msg,x,y=event['msg'],event['x'],event['y']
            w=event.get('wParam',0)
            if type(msg) is not int or msg not in MESSAGES or any(type(v) is not int for v in (x,y,w)) or not (-32768<=x<=32767 and -32768<=y<=32767) or not 0<=w<=0xffffffff:
                raise ValueError('Invalid Windows mouse message/coordinates')
            self.cursor=(x,y)
            self.queue.append(dict(msg=msg,wParam=w,lParam=((y&0xffff)<<16)|(x&0xffff)))
        elif kind=='key':
            key,down=event['vkey'],event['down']
            if type(key) is not int or key not in VKEYS or type(down) is not bool:
                raise ValueError('Unsupported key event')
            if down:
                if key not in self.held: self.pressed.add(key)
                self.held.add(key)
            else: self.held.discard(key)
        else: raise ValueError('Unsupported macOS input event')
        self.events.append(dict(frame=frame,sequence=len(self.events),event=copy.deepcopy(event)))
        self.timeline.append(dict(kind='event',index=len(self.events)-1))
        self.last_frame=frame

    def poll(self, frame, site, api, vkey=None, remove=True):
        if type(frame) is not int or frame<self.last_frame or type(site) is not int or not 0<site<=0xffffffff:
            raise ValueError('A monotonic frame and original poll address are required')
        if api=='GetCursorPos': answer=dict(x=self.cursor[0],y=self.cursor[1],result=1)
        elif api=='PeekMessageA':
            message=copy.deepcopy(self.queue[0]) if self.queue else None
            answer=dict(result=int(message is not None),message=message,remove=bool(remove))
            if message is not None and remove: self.queue.pop(0)
        elif api=='GetAsyncKeyState':
            if vkey not in VKEYS: raise ValueError('Unsupported virtual key poll')
            answer=(0x8000 if vkey in self.held else 0)|(1 if vkey in self.pressed else 0)
            self.pressed.discard(vkey)
        else: raise ValueError('Unsupported declared-answer API')
        self.polls.append(dict(frame=frame,poll=len(self.polls),site=hex(site),api=api,vkey=vkey,answer=copy.deepcopy(answer)))
        self.timeline.append(dict(kind='poll',index=len(self.polls)-1))
        self.last_frame=frame
        return answer

    def journal(self):
        return copy.deepcopy(dict(schema='rising-lands/macos-input-journal/1',policy='record-only',wndproc='0x4181a1',events=self.events,polls=self.polls,timeline=self.timeline))

    @classmethod
    def replay(cls, journal):
        if journal.get('schema')!='rising-lands/macos-input-journal/1' or journal.get('policy')!='record-only':
            raise ValueError('Unsupported input journal')
        r=cls()
        for item in journal['timeline']:
            index=item['index']
            if type(index) is not int: raise ValueError('Invalid journal index')
            if item['kind']=='event':
                if index!=len(r.events): raise ValueError('Missing/reordered journal event')
                event=journal['events'][index]
                r.event(event['frame'],event['event'])
            elif item['kind']=='poll':
                if index!=len(r.polls): raise ValueError('Missing/reordered journal poll')
                poll=journal['polls'][index]
                answer=r.poll(poll['frame'],int(poll['site'],16),poll['api'],poll['vkey'],
                              poll['answer'].get('remove',True) if isinstance(poll['answer'],dict) else True)
                if answer!=poll['answer']: raise ValueError('Recorded poll answer differs on replay')
            else: raise ValueError('Unknown journal timeline kind')
        if r.journal()!=journal: raise ValueError('Incomplete or altered input journal')
        return r

    def export_script(self, root):
        # The owner's schema/validator is required; a journal cannot be relabeled
        # as an original-consumable input file while that contract is absent.
        from pathlib import Path
        if not (Path(root)/'pesquisas-paralelas/missoes/m3/entrada_roteirizada.py').is_file():
            raise InputContractPending('Missions scripted-input schema is not integrated')
        raise InputContractPending('Missions scripted-input exporter adapter awaits contract review')
