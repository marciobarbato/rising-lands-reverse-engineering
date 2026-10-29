"""Replay frozen original queue cases through the bounded Python provider."""
from audio_queue_fixtures import QueueFixtureMemory,ScriptedCOM
from fila_audio import AudioQueue
from bancos_som import DependenciaSom


def dispatch(q,operation,r,args):
    if operation in ('is_playing','is_stopped','is_looped'):return q.status(r['EAX'],operation[3:])
    elif operation=='stop_buffer':return q.stop_buffer(r['EAX'])
    elif operation=='compact':return q.compact(r['EAX'],r['EDX'])
    elif operation=='destroy_waiting':return q.destroy_waiting(r['EAX'])
    elif operation=='permute':q.permute(r['EAX'],r['EDX']);return None
    elif operation=='sort':q.sort();return None
    elif operation=='destroy_logical':q.destroy_logical(r['EAX']);return None
    elif operation=='transfer_to_playing':return q.transfer_to_playing(r['EAX'])
    elif operation=='transfer_to_waiting':return q.transfer_to_waiting(r['EAX'])
    elif operation=='insert':return q.insert(r['EAX'],r['EDX'],r['EBX'],r['ECX'],args[0])
    elif operation=='post':return q.post(r['EAX'],r['EDX'],r['EBX'],r['ECX'],args[0])
    elif operation=='set_volume':return q.set_volume(r['EAX'],r['EDX'])
    elif operation=='stop_handle':return q.stop_handle(r['EAX'])
    elif operation=='replace_physical':return q.replace_slot(r['EAX'])
    elif operation=='replace_logical':return q.replace_slot(r['EAX'],True)
    elif operation=='find_physical':return q.find_loaded(r['EAX'],r['EDX'])
    elif operation=='find_logical':return q.find_loaded(r['EAX'],r['EDX'],True)
    elif operation=='destroy_physical':q.destroy_physical(r['EAX']);return None
    elif operation=='destroy_only':q.destroy_only_sound(r['EAX']);return None
    elif operation=='duplicate':return q.duplicate_buffer(r['EAX'])
    elif operation=='create_logical':return q.create_logical(r['EAX'],r['EDX'])
    elif operation=='clear_list':return q.clear_list()
    elif operation=='manage':return q.manage()
    else:raise ValueError('Unknown replay operation')

def replay(case):
    fixture=case['input'];memory=QueueFixtureMemory.restore(fixture['memory']);plan=ScriptedCOM(fixture['com'])
    q=AudioQueue(memory,plan);steps=[];stop=None;value=None
    try:
        for request in fixture.get('sequence',[fixture]):
            value=dispatch(q,request['operation'],request['regs'],request['arguments'])
            if 'sequence' in fixture:steps.append(dict(eax=hex(value),memory=memory.snapshot()))
    except DependenciaSom as exc:stop=str(exc);value=None
    return dict(output=memory.snapshot(),value=value,steps=steps,stop=stop,com=plan.calls,unused_com=len(plan.responses))


def compare(case):
    actual=replay(case);failures=[]
    if actual['output']!=case['output']:failures.append('memory')
    if actual['steps']!=case.get('steps',[]):failures.append('sequence steps')
    if actual['com']!=case['com']:failures.append('external calls')
    if actual['unused_com']!=case['unused_com']:failures.append('unused external answers')
    if bool(actual['stop'])!=bool(case['stop']):failures.append('dependency stop')
    if actual['value'] is not None and case['eax'] is not None and actual['value']!=int(case['eax'],16):failures.append('EAX')
    return failures,actual
