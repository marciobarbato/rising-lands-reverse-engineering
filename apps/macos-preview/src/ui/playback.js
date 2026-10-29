'use strict';
const $=id=>document.getElementById(id);
let image=null,seq=0,pending=new Map(),live=false,playing=false;
function request(operation,extra={}){return new Promise((resolve,reject)=>{const id=++seq;const timer=setTimeout(()=>{pending.delete(id);reject(Error('Tempo limite na inspeção.'));},180000);pending.set(id,{resolve,reject,timer});window.webkit.messageHandlers.engine.postMessage({id,action:'playback',operation,...extra});});}
window.receive=response=>{const p=pending.get(response.id);if(!p)return;clearTimeout(p.timer);pending.delete(response.id);response.ok?p.resolve(response.playback):p.reject(Error(response.error));};
function row(values){const tr=document.createElement('tr');for(const v of values){const td=document.createElement('td');td.textContent=String(v);tr.append(td);}return tr;}
function blocks(){if(!image)return;const filter=$('filter').value.toLowerCase();const found=image.memory.filter(b=>`${b.name} ${b.base}`.toLowerCase().includes(filter));$('blocks').replaceChildren(...found.slice(0,100).map(b=>row([b.name,b.base,b.bytes,b.sha256])));$('block-count').textContent=`${image.blocks} blocos · ${image.bytes} bytes · ${found.length} resultados`}
function apply(value){image=value;$('phase').replaceChildren(...['state_s0',...value.phases].map(name=>{const o=document.createElement('option');o.value=name;o.textContent=name;return o;}));$('phase').value=value.phase;$('status').textContent=`${value.scenario}\n${value.phase} · resumo verificado · ${value.checkpoint_verified?'checkpoint igual':'sem checkpoint nesta fase'}\n${value.verified_phases}/257 fases e ${value.verified_checkpoints}/11 checkpoints verificados\nEstado: ${value.summary_sha256}`;if(value.live_stop){playing=false;$('status').textContent+='\nParada explícita: '+value.live_stop.type+' · '+value.live_stop.phase+' · '+JSON.stringify(value.live_stop.detail);}$('live-step').disabled=!live||!!value.live_stop;$('live-play').disabled=!live||!!value.live_stop;if(live){$('status').textContent=value.scenario+'\n'+value.phase+' · '+value.verified_phases+' fases iguais na janela aceita'+(value.live_stop?'\nParada explícita: '+JSON.stringify(value.live_stop):'');}$('words').replaceChildren(...Object.entries(value.observed).map(([name,w])=>row([name,w.address,w.value,`0x${w.value.toString(16)}`])));const r=value.render;$('render-status').textContent=(r.status==='full'?'Quadro completo · HUD e cursor incluídos':r.status==='partial'?'Imagem parcial · parada explícita':r.status==='undrawn'?'Fase sem desenho · superfície preservada':'Render interrompido')+'\n'+((r.stop||r.inherited_stop)?`${(r.stop||r.inherited_stop).endereco}: ${(r.stop||r.inherited_stop).detalhe}`:'')+'\n'+(r.native_phase_end_sha256===null?'Sem referência aceita de superfície nesta fase.':'HUD e cursor incluídos no domínio Graphics; cache encadeado desde a entrada do quadro 1.');$('render-image').hidden=!r.image;if(r.image)$('render-image').src=r.image;else $('render-image').removeAttribute('src');for(const id of ['phase','previous','next','go-frame','reset'])$(id).disabled=false;$('previous').disabled=value.phase_index<0;$('next').disabled=value.phase_index>=256;blocks();}
async function run(operation,extra={}){try{for(const id of ['phase','previous','next','go-frame','reset'])$(id).disabled=true;apply(await request(operation,extra));return true;}catch(e){if(image)apply(image);playing=false;$('live-step').disabled=true;$('live-play').disabled=true;$('status').textContent='Falha na inspeção: '+e.message;return false;}}
$('phase').onchange=()=>{live=false;playing=false;return run('phase',{phase:$('phase').value});};$('previous').onclick=()=>run('phase',{phase:image.phase_index===0?'state_s0':image.phase_index-1});$('next').onclick=()=>run('phase',{phase:image.phase_index+1});$('go-frame').onclick=()=>run('frame',{frame:Number($('frame').value)});$('reset').onclick=()=>run('reset');$('filter').oninput=blocks;$('read-form').onsubmit=async event=>{event.preventDefault();try{const r=await request('read',{address:$('address').value,size:Number($('size').value)});$('read-result').textContent=r.read_hex;}catch(e){$('read-result').textContent=e.message;}};
window.runSmokeTests=async()=>{
 await window.playbackReady;
 const tests=[];
 const check=(label,condition)=>{if(!condition)throw Error(label);tests.push(label);};
 const until=async(condition,label)=>{const limit=Date.now()+20000;while(!condition()){if(Date.now()>limit)throw Error(label);await new Promise(r=>setTimeout(r,25));}};
 check('257 summaries and 11 checkpoints shown',image&&image.verified_phases===257&&image.verified_checkpoints===11&&$('status').textContent.includes('257/257'));
 check('captured blocks listed', $('blocks').children.length>0);
 const initial=image.summary_sha256;
 $('phase').value='between_frames';$('phase').dispatchEvent(new Event('change'));
 await until(()=>image.phase==='between_frames'&&!$('next').disabled,'phase selector');
 $('next').click();await until(()=>image.phase==='frame1'&&!$('phase').disabled,'next phase');
 check('DOM next phase reaches frame1',image.observed.counter.value===1);
 $('address').value='0x508f7c';$('size').value='4';$('read-form').requestSubmit();
 await until(()=>$('read-result').textContent==='01000000','memory read');
 check('DOM memory read returns captured counter',true);
 $('previous').click();await until(()=>image.phase==='between_frames'&&!$('phase').disabled,'previous phase');
 $('frame').value='12';$('go-frame').click();await until(()=>image.phase==='frame12'&&!$('phase').disabled,'frame 12');
 check('DOM frame selection reaches frame12',image.observed.counter.value===12);
 check('Graphics full image with HUD and cursor shown',!$('render-image').hidden&&$('render-image').src.startsWith('data:image/png')&&$('render-status').textContent.includes('HUD')&&image.render.hud===true);
 check('undrawn frame preserves the full native phase-end surface',image.render.status==='undrawn'&&!image.render.stop&&!image.render.inherited_stop&&image.render.equals_native_phase_end===true);
 $('filter').value='dgroup';$('filter').dispatchEvent(new Event('input'));
 check('DOM block filter', $('blocks').children.length===1&&$('blocks').textContent.includes('dgroup'));
 $('reset').click();await until(()=>image.phase==='state_s0'&&!$('phase').disabled,'reset');
 check('DOM reset preserves initial state identity',image.summary_sha256===initial);
 $('live-open').click();await until(()=>image.mode==='live-rust-no-input'&&!$('live-step').disabled,'live S0');
 check('DOM opens real Rust S0 with record-only inputs',image.input_policy==='record-only');
 $('live-step').click();await until(()=>image.phase==='load_tail'&&!$('live-step').disabled,'live load tail');
 $('live-step').click();await until(()=>image.phase==='frame1'&&!$('live-step').disabled,'live frame1');
 check('Rust live frame1 state and full native surface equal',image.verified_phases===3&&image.render.equals_native_phase_end===true&&!image.live_stop);
 return {passed:true,tests,commit:image.commit,scenario:image.scenario,render:image.render.status};
};
window.playbackReady=run('open').then(()=>{
 if(!image||image.verified_phases!==257||image.verified_checkpoints!==11){window.signalAppInitializationFailure('Playback worker did not initialize');return;}
 window.signalAppReady({mode:'inspection',worker:true,assets:true,commit:image.commit});
});

$('live-open').onclick=async()=>{live=true;playing=false;await run('live-open');};
$('live-step').onclick=()=>run('live-step');
$('live-play').onclick=async()=>{playing=!playing;$('live-play').textContent=playing?'Pausar Rust':'Executar Rust';while(playing){if(!await run('live-step'))break;if(!image||image.live_stop){playing=false;break;}await new Promise(r=>setTimeout(r,0));}};
for(const id of ['phase','previous','next','go-frame','reset'])$(id).addEventListener('click',()=>{live=false;playing=false;});
const vkeys={Enter:13,Shift:16,Control:17,Alt:18,Escape:27,' ':32,ArrowLeft:37,ArrowUp:38,ArrowRight:39,ArrowDown:40,Delete:46,x:88,X:88};
function record(event){request('record-event',{event}).then(r=>{$('input-status').textContent='Somente gravação · quadro '+r.frame;}).catch(e=>{$('input-status').textContent=e.message;});}
const surface=$('render-image');
for(const [type,msg] of [['mousemove',0x200],['mousedown',0x201],['mouseup',0x202]])surface.addEventListener(type,e=>{e.preventDefault();surface.focus();const box=surface.getBoundingClientRect();let m=msg;if(type==='mousedown'&&e.button===0&&e.detail>1&&e.detail%2===0)m=0x203;if(type==='mousedown'&&e.button===2)m=0x204;if(type==='mouseup'&&e.button===2)m=0x205;if(e.button===1&&type!=='mousemove')return;const w=(e.buttons&1?1:0)|(e.buttons&2?2:0)|(e.shiftKey?4:0)|(e.ctrlKey?8:0);record({kind:'mouse',msg:m,x:Math.floor((e.clientX-box.left)*800/box.width),y:Math.floor((e.clientY-box.top)*600/box.height),wParam:w});});
const heldVkeys=new Set();
for(const [type,down] of [['keydown',true],['keyup',false]])surface.addEventListener(type,e=>{if(vkeys[e.key]===undefined)return;e.preventDefault();if(down)heldVkeys.add(vkeys[e.key]);else heldVkeys.delete(vkeys[e.key]);record({kind:'key',vkey:vkeys[e.key],down});});
surface.addEventListener('blur',()=>{for(const vkey of heldVkeys)record({kind:'key',vkey,down:false});heldVkeys.clear();});
function download(value,name){return new Promise((resolve,reject)=>{const id=++seq;const timer=setTimeout(()=>{pending.delete(id);reject(Error('Tempo limite na exportação.'));},180000);pending.set(id,{resolve,reject,timer});window.webkit.messageHandlers.engine.postMessage({id,action:'saveInput',content:value,script:name==='monde01-input.json'});});}
$('export-input').onclick=async()=>{try{const r=await request('export-input');await download(r.script,'monde01-input.json');}catch(e){$('input-status').textContent='Exportação interrompida: '+e.message;}};
$('export-journal').onclick=async()=>{try{const r=await request('export-journal');await download(r.input_journal,'monde01-macos-journal.json');}catch(e){$('input-status').textContent=e.message;}};

surface.addEventListener('contextmenu',e=>e.preventDefault());
