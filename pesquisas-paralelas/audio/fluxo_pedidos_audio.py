"""Ordered, lossless sound-request arguments at the original game boundary.

Only PostSound, StopSound and Manage belong to this version. Unused registers
and caller stack residue are deliberately absent; return EAX is not an input.
"""
SCHEMA = 'rising-lands/audio-request-stream/1'
ARGUMENTS = {'PlaySnd_PostSound': (('EAX','EDX','EBX','ECX'),1),
             'PlaySnd_StopSound': (('EAX',),0), 'PlaySnd_Manage': ((),0)}


def u32(value):
    if isinstance(value,str): value=int(value,16)
    if type(value) is not int or not 0<=value<=0xffffffff:
        raise ValueError('Expected explicit u32 argument')
    return value


def frame_of(phase):
    if phase=='load_tail': return 0
    for prefix in ('between_frames','frame'):
        if phase.startswith(prefix):
            suffix=phase[len(prefix):]
            if suffix=='' and prefix=='between_frames': return 1
            if suffix.isdecimal() and int(suffix)>0: return int(suffix)
    raise ValueError('Expected an accepted frame phase: '+str(phase))


class AudioRequestStream:
    """Append before provider execution, including requests that later stop.

    ``phase`` and ``caller_return`` must be set by the engine at the call site.
    The stream allocates no sound state and has no playback effects.
    """
    def __init__(self): self.events=[]

    def append(self,phase,caller_return,routine,registers,stack):
        if routine not in ARGUMENTS: raise ValueError('Unsupported request routine: '+routine)
        names,count=ARGUMENTS[routine]
        if len(stack)!=count: raise ValueError('Incorrect argument stack length for '+routine)
        self.events.append(dict(sequence=len(self.events),frame=frame_of(phase),phase=phase,
            routine=routine,caller_return=u32(caller_return),
            registers={k:u32(registers[k]) for k in names},stack_words=[u32(v) for v in stack]))

    def document(self): return dict(schema=SCHEMA,events=[dict(e,registers=dict(e['registers']),stack_words=list(e['stack_words'])) for e in self.events])


def from_boundaries(phases):
    result=AudioRequestStream()
    for phase in phases:
        for event in phase['boundaries']:
            routine=event['routine']
            if routine not in ARGUMENTS: continue
            _,count=ARGUMENTS[routine]
            result.append(phase['phase'],event['caller_return'],routine,event['registers'],event['stack_words'][:count])
    return result.document()


def validate(document):
    if set(document)!={'schema','events'} or document['schema']!=SCHEMA:
        raise ValueError('Unknown request-stream schema')
    stream=AudioRequestStream()
    for e in document['events']:
        if set(e)!={'sequence','frame','phase','routine','caller_return','registers','stack_words'}:
            raise ValueError('Malformed event fields')
        if type(e['sequence']) is not int or type(e['frame']) is not int:
            raise ValueError('Sequence and frame must be integers')
        if e['routine'] not in ARGUMENTS: raise ValueError('Unknown request routine')
        if set(e['registers'])!=set(ARGUMENTS[e['routine']][0]): raise ValueError('Malformed registers')
        stream.append(e['phase'],e['caller_return'],e['routine'],e['registers'],e['stack_words'])
        if stream.events[-1]!=e: raise ValueError('Noncanonical request event')
    return document


def compare_streams(expected,actual):
    """Exact ordered comparison, no sorting, tolerance, masks or deduplication."""
    validate(expected);validate(actual)
    a,b=expected['events'],actual['events']
    differences=[dict(sequence=i,expected=a[i] if i<len(a) else None,actual=b[i] if i<len(b) else None)
                 for i in range(max(len(a),len(b))) if i>=len(a) or i>=len(b) or a[i]!=b[i]]
    return dict(equal=not differences,expected_events=len(a),actual_events=len(b),
                mismatches=len(differences),differences=differences)
