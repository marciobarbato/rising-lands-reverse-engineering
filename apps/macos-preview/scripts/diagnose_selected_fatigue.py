"""Bounded app-driver reproduction of the selected-actor renderer boundary.

This is a diagnostic, not an original equality proof or a UI throughput test.
Only S0/static inputs initialize the world. Copied projections are read at the
2952 boundary and the stop; they never feed the world or renderer.
"""
import argparse
import bisect
import hashlib
import json
from pathlib import Path
import signal
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from macos_native_driver import NativeDriver
from macos_rust_abi import Frames


def inspect(driver,engine):
    blocks=engine.snapshot(driver.status().world);bases=sorted(blocks)
    def read(address,size):
        base=bases[bisect.bisect_right(bases,address)-1]
        raw=blocks[base][address-base:address-base+size]
        if len(raw)!=size:raise ValueError('Projection read outside block: '+hex(address))
        return raw
    def number(address,size):return int.from_bytes(read(address,size),'little')
    selected=number(0x496ac2,2);mode=number(0x508f8f,1)
    units=number(0x4e19a0,4);rows=[]
    for index in range(800):
        record=read(units+276*index,276)
        if record[2] and (record[0xba] or record[0xbd] or selected==index or mode):
            rows.append(dict(index=index,address=hex(units+276*index),owner=record[0],type=record[1],state=record[2],
                material_word4=int.from_bytes(record[4:6],'little'),fatigue_life74=int.from_bytes(record[0x74:0x76],'little'),
                fatigue_word76=int.from_bytes(record[0x76:0x78],'little'),indicator_ba=record[0xba],selection_bd=record[0xbd],
                cell=int.from_bytes(record[8:10],'little'),record_sha256=hashlib.sha256(record).hexdigest(),record_hex=record.hex()))
    status=driver.status()
    return dict(completed_frames=status.frames,counter=status.counter,selected_unit=selected,selection_mode=mode,
                overlay_units=rows,surface_sha256=hashlib.sha256(driver.pixels()).hexdigest())


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('driver','library','inputs','output'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--select-frame',type=int,default=481)
    p.add_argument('--move-frame',type=int,default=493)
    p.add_argument('--pointer-frame',type=int,default=511)
    p.add_argument('--frames',type=int,default=4500)
    a=p.parse_args();signal.alarm(1140)
    if a.output.exists():p.error('Refusing to overwrite diagnostic')
    if not 129<=a.select_frame<a.move_frame<a.pointer_frame<=a.frames<=9200:p.error('Invalid diagnostic frame window')
    events={a.select_frame:[dict(kind='mouse',msg=0x201,x=560,y=528),dict(kind='mouse',msg=0x202,x=560,y=528)],
            a.move_frame:[dict(kind='mouse',msg=0x201,x=624,y=432),dict(kind='mouse',msg=0x202,x=624,y=432)],
            a.pointer_frame:[dict(kind='mouse',msg=0x200,x=400,y=272)]}
    driver=NativeDriver(a.driver,a.library,a.inputs);engine=Frames(a.library);boundaries=[]
    try:
        if driver.lib.macos_live_validation(driver.handle,0):raise RuntimeError('PlayPolicyRejected')
        if driver.advance():raise RuntimeError('LoadTailFailed')
        stop=None
        for frame in range(1,a.frames+1):
            for event in events.get(frame,[]):
                if driver.event(event):raise RuntimeError('DiagnosticEventRejected')
            if frame==2952:boundaries.append(dict(attempted_render_frame=frame,position='before-render',state=inspect(driver,engine)))
            code=driver.advance();s=driver.status()
            if code:
                stop=dict(attempted_frame=frame,code=code,disposition=s.disposition,stop_phase=s.stop_phase,
                          detail=bytes(s.message).split(b'\0')[0].decode(),state=inspect(driver,engine));break
            if frame==2952:boundaries.append(dict(attempted_render_frame=frame,position='after-complete-frame',state=inspect(driver,engine)))
        s=driver.status()
        report=dict(schema='rising-lands/macos-selected-fatigue-diagnostic/1',
            original_executable_sha256='6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb',
            world_source='S0 and four original immutable tables; real prefix and advancing play world',
            scope='Declared-frame reproduction, not a replay of the historical UI arrival times; no original equality claim',
            engine_sha256=hashlib.sha256(a.library.read_bytes()).hexdigest(),driver_sha256=hashlib.sha256(a.driver.read_bytes()).hexdigest(),
            events=events,requested_frames=a.frames,completed_frames=s.frames,boundaries=boundaries,first_stop=stop,
            audits=dict(phases=s.phases_equal,surfaces=s.surfaces_equal,checkpoints=s.checkpoints_equal,proof_ns=s.proof_ns))
        a.output.write_text(json.dumps(report,indent=1)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k not in ('boundaries','events')},indent=1))
    finally:driver.close()


if __name__=='__main__':main()
