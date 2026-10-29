"""Replay frozen original queue cases through the bounded Python provider."""
from audio_queue_fixtures import QueueFixtureMemory,ScriptedCOM
from fila_audio import AudioQueue
from bancos_som import DependenciaSom


def replay(case):
    fixture=case['input'];memory=QueueFixtureMemory.restore(fixture['memory']);plan=ScriptedCOM(fixture['com'])
    q=AudioQueue(memory,plan);steps=[];r=fixture['regs'];args=fixture['arguments'];operation=fixture['operation'];stop=None
    try:
        if 'sequence' in fixture:
            for request in fixture['sequence']:
                r=request['regs'];args=request['arguments']
                value=q.post(r['EAX'],r['EDX'],r['EBX'],r['ECX'],args[0])
                steps.append(dict(eax=hex(value),memory=memory.snapshot()))
        elif operation in ('is_playing','is_stopped','is_looped'):value=q.status(r['EAX'],operation[3:])
        elif operation=='stop_buffer':value=q.stop_buffer(r['EAX'])
        elif operation=='compact':value=q.compact(r['EAX'],r['EDX'])
        elif operation=='destroy_waiting':value=q.destroy_waiting(r['EAX'])
        elif operation=='permute':q.permute(r['EAX'],r['EDX']);value=None
        elif operation=='sort':q.sort();value=None
        elif operation=='destroy_logical':q.destroy_logical(r['EAX']);value=None
        elif operation=='transfer_to_playing':value=q.transfer_to_playing(r['EAX'])
        elif operation=='transfer_to_waiting':value=q.transfer_to_waiting(r['EAX'])
        elif operation=='insert':value=q.insert(r['EAX'],r['EDX'],r['EBX'],r['ECX'],args[0])
        elif operation=='post':value=q.post(r['EAX'],r['EDX'],r['EBX'],r['ECX'],args[0])
        elif operation=='set_volume':value=q.set_volume(r['EAX'],r['EDX'])
        elif operation=='stop_handle':value=q.stop_handle(r['EAX'])
        elif operation=='replace_physical':value=q.replace_slot(r['EAX'])
        elif operation=='replace_logical':value=q.replace_slot(r['EAX'],True)
        elif operation=='find_physical':value=q.find_loaded(r['EAX'],r['EDX'])
        elif operation=='find_logical':value=q.find_loaded(r['EAX'],r['EDX'],True)
        elif operation=='destroy_physical':q.destroy_physical(r['EAX']);value=None
        elif operation=='destroy_only':q.destroy_only_sound(r['EAX']);value=None
        elif operation=='duplicate':value=q.duplicate_buffer(r['EAX'])
        elif operation=='create_logical':value=q.create_logical(r['EAX'],r['EDX'])
        elif operation=='clear_list':value=q.clear_list()
        elif operation=='manage':value=q.manage()
        else:raise ValueError('Unknown replay operation')
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
