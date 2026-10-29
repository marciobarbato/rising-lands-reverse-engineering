"""Synthesize a static-only graph from the separately committed original evidence."""
import hashlib
import json
from pathlib import Path

OWNED=Path(__file__).resolve().parent


def generate():
    evidence_path=OWNED/'evidencias/original-player-action-bytes.json'
    evidence=json.loads(evidence_path.read_text())
    context_path=OWNED/'evidencias/monde01-action-context.json'
    context=json.loads(context_path.read_text())
    routines={r['name']:r for r in evidence['routines']}
    owners={}
    groups={
        'ai-runtime': ['InputGame','InputReceive','InputSend','SetPlayerOrdre','ProcessInputGame','InitInputPlayer',
                       'CalculGame','ProgIteration','GrabAllInput','MenuInit','EnginNextEtape','BatimentNextEtape',
                       'CalculEnginNextEtape','CalculBatimentNextEtape'],
        'macos': ['WndProc','_WinMain@16','KeyboardInit','KeyPressed','KeyUnPressed','KeyTestRelease','MouseInit','MouseZone','MouseEstDeplacer'],
        'core': ['Deselection','SetConstruitBatimentSelect','SetDeplaceEnginSelect','SetAttaqueEnginSelect',
                 'SetRecolteEnginSelect','SetTransporteEnginSelect','SelectionEngin','EnginAddSelection','DeSelectionGroupe',
                 'SelectionAddEngin','DeselectionEngin','BatimentSelection','BatimentDeselectionner','SetDeplaceEngin','SetEnginConstruitBatiment','SetRecolteEngin',
                 'SetTransporteEngin','ResetOrdre','DeplaceEngin','PlaceBatiment','BatimentAlloc'],
        'economy': ['CalculConstruireBatiment','CalculWorkEngin','CalculTransporteEngin','ConstruitPerso','InitRecruteTroupe',
                    'CalculTroupe','TerrainRecolte','MineRecolte','BatimentConstruction','InitBatimentPlayer','BatimentConstruit',
                    'BatimentAjouteMatiere','TerrainRetireMatiere','SetDepotEnginSelect','SetMineEnginSelect',
                    'SetRamasseEnginSelect','RechercheCalcul','CalculMatiere','CreerBatiment','TestRessource','EnleveMatiere','GetRessourceStock'],
        'combat': ['SetAttaqueEngin','CalculAttaqueEngin','ProjectileInit','ProjectileCalcul','InfligeDegat'],
        'missions': ['TestFinDeMission','TestFinDeMission6','MissionNext','MissionReStart','MissionLoad','PartieGetResultat','BatimentGetTypeName'],
    }
    for owner,names in groups.items():
        for name in names:owners[name]=[owner]
    owners['CalculConstruireBatiment']=['economy','core']
    owners['CreerBatiment']=['economy','core']
    owners['BatimentConstruction']=['economy','core']
    def owner(name):
        if name.startswith('USER32.dll!'): return ['macos']
        if name.startswith('PlaySnd_') or name.startswith('MCICD_'):return ['audio']
        return owners.get(name,['coordinator-unassigned'])
    nodes={}
    def node(name,address,kind='routine'):
        if name not in nodes:
            nodes[name]=dict(id=name,address=address,kind=kind,owners=owner(name),
                             naming_evidence='imported original symbol' if kind=='routine' else 'original PE import table',
                             runtime_reachability='not established by this static map')
    edges=[]
    relevant=set(owners)|set(routines)
    for name,routine in routines.items():
        node(name,routine['address'])
        nodes[name]['byte_evidence']=dict(path=str(evidence_path.relative_to(OWNED)),routine=name,
            start=routine['address'],end_exclusive=routine['end_exclusive'],sha256=routine['sha256'])
        for call in routine['calls']:
            target=call['callee']
            if target not in relevant and not target.startswith('USER32.dll!'):continue
            node(target,call['target'],'import_slot' if call['kind']=='iat_indirect' else 'routine')
            edges.append(dict(source=name,target=target,site=call['site'],bytes_hex=call['hex'],
                              target_address=call['target'],kind=call['kind'],claim='byte-proven encoding',
                              scope='decoded candidate call inside next-symbol interval; no dynamic execution/reachability claim'))
    commands=[]
    for case in evidence['command_table']['cases']:
        commands.append(dict(code_u16=case['command_u16'],table_entry=case['table_entry'],branch=case['branch'],
                             possible_calls=case['direct_calls'],claim='byte-proven table plus static branch traversal',
                             runtime_reachability='not established; neither accepted M2.2 nor this map supplies player input'))
    def edge_sites(source,target):return [e['site'] for e in edges if e['source']==source and e['target']==target]
    actions=[
        dict(id='select',commands=[1,2,3,36],producer_sites=['0x0042b9aa','0x0042ba20'],
             stages=['InputGame','SetPlayerOrdre','ProcessInputGame','SelectionEngin','EnginAddSelection','BatimentSelection'],
             data=['command +2/+4 u16 selection geometry or reference, depending on tag',
                   'selection count u16 at 0x508728 + player*512; u16 entries at +2',
                   'unit pool pointer u32 at 0x4e19a0, stride 276; owner +0 u8, type +1 u8, state +2 u8'],
             gap='Click/drag hit-testing and modifiers must be traced with original scripted Windows inputs; rectangle and single-index variants differ.'),
        dict(id='move',commands=[5],producer_sites=['0x0042a488','0x0042ad8e','0x0042b82a','0x0042bbd6'],
             stages=['InputGame','SetPlayerOrdre','ProcessInputGame','SetDeplaceEnginSelect','SetDeplaceEngin','EnginNextEtape','DeplaceEngin'],
             data=['packet +2 u16 cell -> SetDeplaceEnginSelect DX',
                   'selection iteration checks owner/alive; original call at 0x473ed2',
                   'unit +0x110 u32 receives frame counter 0x508f7c at 0x473ee2; state/path setters can reset prior orders'],
             gap='Actual path branch, destination acceptance and subsequent movement are not executed here.'),
        dict(id='construct_objective_cave',commands=[4],producer_sites=['0x0042a03c'],
             stages=['InputGame','SetPlayerOrdre','ProcessInputGame','SetConstruitBatimentSelect','SetEnginConstruitBatiment',
                     'EnginNextEtape','CalculConstruireBatiment','CreerBatiment','BatimentConstruction'],
             data=['packet +2 u8 type -> DL; packet +4 u16 cell -> BX at ProcessInputGame call 0x45ef9b',
                   'selected unit must have type +1 == 7; branch at 0x473a71/74',
                   'original type 7 name BATISSEUR; accepted M1 unit 12 is player 0/type 7',
                   'setter writes unit +2 u8 = 11, +0xbe u8 requested type, +0xb2 u16 cell; original type 3 name CAVE',
                   'CreerBatiment has TestRessource/EnleveMatiere calls and physical placement; completion calls BatimentHabitable and BatimentModifyMap'],
             gap='No proof yet that selecting the CAVE UI emits tag 4/type 3, which site/cell passes gates, or that construction completes on MONDE01.'),
        dict(id='gather_food_and_stone',commands=[6,7,8,18,19],producer_sites=['0x0042b486','0x0042b61c'],
             stages=['InputGame','SetPlayerOrdre','ProcessInputGame','SetRecolteEnginSelect','SetTransporteEnginSelect',
                     'SetRecolteEngin','SetTransporteEngin','EnginNextEtape','CalculWorkEngin','CalculTransporteEngin',
                     'TerrainRecolte','MineRecolte','TerrainRetireMatiere','BatimentAjouteMatiere'],
             data=['tag 7: packet +2 u16 cell -> SetRecolteEnginSelect; tag 8 -> SetTransporteEnginSelect',
                   'tags 6/7/8/19 share a later SetDepotEnginSelect call at 0x45f037 using +4 u8, +6 u16, +8 u8',
                   'harvest setter writes unit +2 u8 = 5; transport setter writes +2 u8 = 18',
                   'work branch calls TerrainRecolte/MineRecolte; deposit callers mutate building/resource providers'],
             gap='Local producer for tag 8 and exact UI choice between mining/harvest/bag/cave actions are not established. No natural resource delivery was executed.'),
        dict(id='recruit_or_produce',commands=[17],producer_sites=[],
             stages=['InputGame','SetPlayerOrdre','ProcessInputGame','InitRecruteTroupe','BatimentNextEtape','CalculTroupe','ConstruitPerso'],
             data=['ProcessInputGame 0x45f19f loads packet +2 u8 into AX; owner goes to EDX; call 0x45f1a9',
                   'InitRecruteTroupe reads selected structure u16 at 0x495be0 + 2*player and calls cost/capacity gates',
                   'This is unit recruitment, not a claim that it manufactures food/stone. Resource gathering is a separate route.'],
             gap='The MONDE01 menu producer, available worker types, charges and production completion need original input captures.'),
        dict(id='attack',commands=[14],producer_sites=['0x0042a52c','0x0042a5e6','0x0042aecf'],
             stages=['InputGame','SetPlayerOrdre','ProcessInputGame','SetAttaqueEnginSelect','SetAttaqueEngin','EnginNextEtape',
                     'CalculAttaqueEngin','ProjectileInit','ProjectileCalcul','InfligeDegat'],
             data=['packet +2 u8 attack mode and +4 u16 reference; selected-building branch instead calls BatimentInitAttaqueSelect at 0x45f13f',
                   'SetAttaqueEngin calls ResetOrdre at 0x445a7b; accepted order state +2 = 1, mode +0xb7 u8, reference +0xb8 u16',
                   'ranged/projectile and direct-damage calls are separate conditional paths, not one mandatory sequence'],
             gap='No attack selection/targeting trace or combat result from player input is claimed. AI raid coverage is owned elsewhere.'),
    ]
    for action in actions:
        action['claim']='static synthesis of byte-proven local edges and published owner contracts'
        action['stages_are_not_a_direct_call_sequence']=True
        action['successful_MONDE01_effect']='not proven'
        action['owners']=sorted({o for n in action['stages'] for o in owner(n)})
    branch_sites=[('CalculGame','0x0042d4d4','0x0042c92c'),('CalculGame','0x0042ca7b','0x0042ca9d')]
    transitions=[]
    for name,site,target in branch_sites:
        ins=next(i for i in routines[name]['instructions'] if i['address']==site)
        transitions.append(dict(source=name,site=site,target=target,bytes_hex=ins['hex'],mnemonic=ins['mnemonic'],claim='byte-proven relative branch encoding'))
    graph=dict(schema='rising-lands/monde01-player-action-static-graph/1',scope='MONDE01 M3 planning; static only; no translations or native action execution',
        baseline='daa6ed2da79827b2472929f7e5c82aad1d631782',intact_executable_sha256=evidence['intact_executable_sha256'],
        provenance=[dict(path=str(p.relative_to(OWNED)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in (evidence_path,context_path)],
        nodes=list(nodes.values()),edges=edges,command_dispatch=dict(table_address='0x0045ed20',entry_width_bytes=4,
            guard=dict(site='0x0045eddb',maximum_tag=39),indirect_jump_site='0x0045edeb',cases=commands),
        input_packet=dict(pointer_table_address='0x004e2458',player_index_scale_bytes=4,packet_bytes=10,
            fields=[dict(offset=i,width_bytes=2,role='command tag' if i==0 else 'tag-specific argument') for i in (0,2,4,6,8)],
            setter='SetPlayerOrdre',setter_address='0x0045ecd4',setter_input='AL player; DX tag; BX arg+2; CX arg+4; two caller-stack words for +6/+8',
            consumer='ProcessInputGame',clear_range='0x0045f2de..0x0045f323',semantics='one slot per player, not a new wire/input protocol',claim='byte-proven layout/stores'),
        memory_contracts=[
            dict(id='mouse_coordinates',addresses=['0x005099a8','0x005099aa'],width_bytes=2,
                 writers=['WndProc','ProgIteration'],readers=['InputGame'],claim='byte-proven operand locations; runtime timing unproven'),
            dict(id='mouse_event_flags',addresses=['0x005099ae','0x005099af','0x005099b0','0x005099b1','0x005099b2'],width_bytes=1,
                 writers=['WndProc','ProgIteration'],readers=['InputGame'],claim='byte-proven flag accesses; per-branch read/write subsets are in routine memory_operands'),
            dict(id='command_slot',pointer_table='0x004e2458',pointer_width_bytes=4,index_scale_bytes=4,record_bytes=10,
                 fields=[dict(offset=o,width_bytes=2) for o in (0,2,4,6,8)],writers=['SetPlayerOrdre','ProcessInputGame'],
                 readers=['ProcessInputGame','InputSend'],claim='byte-proven stores/dispatch; InputReceive network delivery remains external'),
            dict(id='selection_area',base='0x00508728',player_stride_bytes=512,count_width_bytes=2,index_width_bytes=2,index_start_offset=2,
                 readers=['SetConstruitBatimentSelect','SetDeplaceEnginSelect','SetAttaqueEnginSelect'],
                 claim='byte-proven wrapper reads; selection mutation routines have their own operand evidence'),
            dict(id='unit_order_record',pointer_slot='0x004e19a0',pointer_width_bytes=4,stride_bytes=276,
                 fields=[dict(offset=0,width_bytes=1,role='owner'),dict(offset=1,width_bytes=1,role='type'),dict(offset=2,width_bytes=1,role='state'),
                         dict(offset=0xb2,width_bytes=2,role='order cell/reference'),dict(offset=0xbe,width_bytes=1,role='requested building type'),
                         dict(offset=0xb7,width_bytes=1,role='attack mode'),dict(offset=0xb8,width_bytes=2,role='attack reference'),
                         dict(offset=0x110,width_bytes=4,role='movement order counter copy')],
                 claim='byte-proven setter/wrapper operands; not every action writes every field'),
            dict(id='end_conditions',base='0x004e1d20',count=10,stride_bytes=10,
                 fields=[dict(offset=0,width_bytes=1,role='condition type'),dict(offset=1,width_bytes=1,role='padding')]+[
                     dict(offset=o,width_bytes=2,role='condition parameter') for o in (2,4,6,8)],
                 writers=['MissionLoad initialization outside this map'],readers=['TestFinDeMission'],claim='accepted M1 bytes plus original evaluator operands'),
            dict(id='end_result',fields=[dict(address='0x004e1d84',width_bytes=1,role='result latch'),
                                        dict(address='0x004e05a0',width_bytes=1,role='AL result copy'),
                                        dict(address='0x004e061c',width_bytes=4,role='end counter')],
                 writers=['TestFinDeMission','CalculGame'],readers=['PartieGetResultat','CalculGame'],claim='byte-proven stores/calls; victory/defeat meaning is static interpretation')],
        actions=actions,
        end_of_mission=dict(stages=['CalculGame','TestFinDeMission','PartieGetResultat','MenuInit','MissionNext'],
            static_calls=dict(test=edge_sites('CalculGame','TestFinDeMission'),menu=edge_sites('CalculGame','MenuInit'),next=edge_sites('CalculGame','MissionNext')),
            data=['condition table 0x4e1d20: 10 records x 10 bytes; type u8, padding u8, four u16 parameters',
                  'latch/result byte 0x4e1d84; per-condition marks 0x4e1d88..0x4e1d91; word 0x4e1a3a==0 forces result with latch 0',
                  'CalculGame stores AL to 0x4e05a0 and increments u32 0x4e061c when nonzero; >=100 requests MenuInit mode 0x13',
                  'PartieGetResultat returns byte 0x4e1d84; successful next path calls MissionNext and stores progression data',
                  'MissionNext increments mission byte 0x496fe4 before MakeMissionName/FileExists; it is not itself MissionLoad'],
            branches=transitions,claim='byte-proven local stores/calls; victory/defeat label is static interpretation',
            runtime_transition='not executed; no M3/M4 acceptance or next mission behavior claimed'),
        unresolved=[
            'No human input occurs in the accepted M2.2 sequence; none of these action routes is dynamically accepted.',
            'InputReceive is a separate network branch for remote humans; no new packet or input protocol is proposed.',
            'Linear LLVM disassembly is bounded by next imported symbol, not proven function extents; candidate edges can include unreachable code. Exact encoded calls are checked, dynamic reachability is not.',
            'Shared tails can jump outside an exported interval; graph is not a complete control-flow closure.',
            'General computed branches and indirect calls are not resolved except the 40-entry ProcessInputGame table.',
            'Building placement, resource availability, terrain cell choice, UI hover context and command producer gaps need original scripted-input coverage.',
            'Windows messages are platform inputs; macOS event mapping remains a separate owner-defined contract.'])
    path=OWNED/'callgraph.json';path.write_text(json.dumps(graph,indent=2)+'\n')
    print(json.dumps(dict(nodes=len(nodes),edges=len(edges),commands=len(commands),actions=len(actions),output=str(path))))


if __name__=='__main__':generate()
