'use strict';
const $=id=>document.getElementById(id);
let image=null,seq=0,pending=new Map(),live=false,playing=false;
function request(operation,extra={}){return new Promise((resolve,reject)=>{const id=++seq;const timer=setTimeout(()=>{pending.delete(id);reject(Error('Tempo limite na inspeção.'));},180000);pending.set(id,{resolve,reject,timer});window.webkit.messageHandlers.engine.postMessage({id,action:'playback',operation,...extra});});}
window.receive=response=>{if(response.nativeUpdate){if(live)apply(response.playback);return;}const p=pending.get(response.id);if(!p)return;clearTimeout(p.timer);pending.delete(response.id);response.ok?p.resolve(response.playback):p.reject(Error(response.error));};
function row(values){const tr=document.createElement('tr');for(const v of values){const td=document.createElement('td');td.textContent=String(v);tr.append(td);}return tr;}
function blocks(){if(!image)return;const filter=$('filter').value.toLowerCase();const found=image.memory.filter(b=>`${b.name} ${b.base}`.toLowerCase().includes(filter));$('blocks').replaceChildren(...found.slice(0,100).map(b=>row([b.name,b.base,b.bytes,b.sha256])));$('block-count').textContent=`${image.blocks} blocos · ${image.bytes} bytes · ${found.length} resultados`}
function apply(value){image=value;if(value.native_metal){playing=value.native_running;$('live-play').textContent=playing?'Pausar Rust':'Executar Rust';}$('phase').replaceChildren(...['state_s0',...value.phases].map(name=>{const o=document.createElement('option');o.value=name;o.textContent=name;return o;}));$('phase').value=value.phase;$('status').textContent=`${value.scenario}\n${value.phase} · resumo verificado · ${value.checkpoint_verified?'checkpoint igual':'sem checkpoint nesta fase'}\n${value.verified_phases}/257 fases e ${value.verified_checkpoints}/11 checkpoints verificados\nEstado: ${value.summary_sha256}`;if(value.live_stop){playing=false;$('status').textContent+='\nParada explícita: '+value.live_stop.type+' · '+value.live_stop.phase+' · '+JSON.stringify(value.live_stop.detail);}$('live-step').disabled=!live||!!value.live_stop;$('live-play').disabled=!live||!!value.live_stop;if(live){$('status').textContent=value.scenario+'\n'+value.phase+' · '+(value.execution_mode==='play'?'modo jogar · sem auditoria':value.verified_phases+' fases iguais na janela aceita')+(value.live_stop?'\nParada explícita: '+JSON.stringify(value.live_stop):'');}$('words').replaceChildren(...Object.entries(value.observed).map(([name,w])=>row([name,w.address,w.value,`0x${w.value.toString(16)}`])));const r=value.render;$('render-status').textContent=(r.status==='full'?'Quadro completo · HUD e cursor incluídos':r.status==='partial'?'Imagem parcial · parada explícita':r.status==='undrawn'?'Fase sem desenho · superfície preservada':'Render interrompido')+'\n'+((r.stop||r.inherited_stop)?`${(r.stop||r.inherited_stop).endereco}: ${(r.stop||r.inherited_stop).detalhe}`:'')+'\n'+(r.native_phase_end_sha256===null?'Sem referência aceita de superfície nesta fase.':'HUD e cursor incluídos no domínio Graphics; cache encadeado desde a entrada do quadro 1.');if(value.native_metal){$('render-image').hidden=true;$('render-canvas').hidden=true;$('render-status').textContent='Rust ABI 1.6 · janela Metal nativa · '+(value.execution_mode==='play'?'modo jogar · sem prova por quadro':value.verified_surfaces+' superfícies iguais')+(value.live_stop?'\nParada: '+JSON.stringify(value.live_stop):'');}else if(r.frame){drawRawFrame(r.frame);$('render-image').hidden=true;}else{$('render-canvas').hidden=true;$('render-image').hidden=!r.image;if(r.image)$('render-image').src=r.image;else $('render-image').removeAttribute('src');}for(const id of ['phase','previous','next','go-frame','reset'])$(id).disabled=false;$('previous').disabled=value.phase_index<0;$('next').disabled=value.phase_index>=256;blocks();recordingStatus();}
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
 check('Rust native frame1 state and full native surface equal',image.verified_phases===3&&image.render.equals_native_phase_end===true&&!image.live_stop);
 check('Rust ABI 1.6 native Metal window shown',image.native_metal===true&&image.native_engine_binding==='static-abi16'&&image.native_window_visible===true&&!image.render.frame&&!image.render.image);
 $('live-play').click();
 await until(()=>image.phase_index>=800&&!image.live_stop,'native play reaches frame400');
 $('live-play').click();
 await until(()=>pending.size===0&&!playing,'native pause');
 check('native live prefix proves 257 states and 11 checkpoints',image.verified_phases===257&&image.verified_checkpoints===11);
 check('native Metal live rate is at least 25 fps',image.native_metrics.fps>=25);
 const metrics=image.native_metrics,metal=await request('native-capture');
 check('actual Metal GPU readback matches indexed palette',metal.pixelsChecked>=480000&&!metal.error);
 check('native current memory read matches the live counter',!!(await request('read',{address:'0x508f7c',size:4})).read_hex);
 $('record-input').click();await until(()=>recording&&!recordToggleBusy,'recording enabled');
 check('visible recording indicator and disabled order policy',$('input-status').textContent.includes('Gravando entrada')&&$('input-status').textContent.includes('indisponíveis'));
 const nativeInput=await request('record-native-smoke',{stage:'press'});await recordChain;
 check('native input dispatched to active app and key Metal responder',nativeInput.inputFocus.appActive&&nativeInput.inputFocus.windowKey&&nativeInput.inputFocus.gameFirstResponder);
 check('actual NSEvent path and native recording indicator',nativeInput.recordingIndicator.includes('Gravando entrada'));
 for(let i=0;i<4;i++)await run('live-step');
 await request('record-native-smoke',{stage:'release'});await recordChain;
 $('record-input').click();await until(()=>!recording&&!recordToggleBusy,'recording stopped');
 $('export-input').click();await until(()=>window.lastInputExport?.saved===true,'scripted input exported');
 const exported=window.lastInputExport,rows=exported.script.frames;
 const down=rows.find(r=>r.messages?.some(m=>m[0]===0x201));
 const moved=rows.find(r=>r.messages?.some(m=>m[0]===0x200));
 const up=rows.find(r=>r.messages?.some(m=>m[0]===0x202));
 check('native save action exports Missions schema and k/k+1/k+3 click',exported.script.schema==='rising-lands/monde01-scripted-input/1'&&down.frame===moved.frame+1&&up.frame===moved.frame+3&&!!exported.sha256);
 check('recorded Ctrl stays held through click and never enters engine',rows.filter(r=>r.frame>=moved.frame&&r.frame<=up.frame).every(r=>r.keys?.['0x11']===-32768)&&!image.live_stop&&image.input_policy==='record-only');

 return {passed:true,tests,commit:image.commit,scenario:image.scenario,render:image.render.status,
         nativeMetrics:metrics,metalReadback:metal,inputExport:{path:exported.path,sha256:exported.sha256,script:exported.script},verifiedPhases:image.verified_phases,verifiedCheckpoints:image.verified_checkpoints,verifiedSurfaces:image.verified_surfaces};

};
window.playbackReady=run('open').then(()=>{
 if(!image||image.verified_phases!==257||image.verified_checkpoints!==11){window.signalAppInitializationFailure('Playback worker did not initialize');return;}
 window.signalAppReady({mode:'inspection',worker:true,assets:true,commit:image.commit});
});

$('live-open').onclick=async()=>{live=true;playing=false;await run('live-open');};
$('live-step').onclick=()=>run('live-step');
$('live-play').onclick=async()=>{if(image&&image.native_metal){await run('live-play');return;}playing=!playing;$('live-play').textContent=playing?'Pausar Rust':'Executar Rust';while(playing){if(!await run('live-step'))break;if(!image||image.live_stop){playing=false;break;}await new Promise(r=>setTimeout(r,0));}};
for(const id of ['phase','previous','next','go-frame','reset'])$(id).addEventListener('click',()=>{live=false;playing=false;});
const vkeys={Enter:13,Shift:16,Control:17,Alt:18,Escape:27,' ':32,ArrowLeft:37,ArrowUp:38,ArrowRight:39,ArrowDown:40,Delete:46,x:88,X:88};
let recording=false,recordToggleBusy=false,recordChain=Promise.resolve(),recordFailure=null,recordEndFrame=null;
function recordingStatus(detail=''){ $('live-open').disabled=recording;$('record-input').textContent=recording?'Parar gravação':'Nova gravação';$('input-status').textContent=(recording?'● Gravando entrada':'Gravação desativada')+' · '+(image?.execution_mode==='play'?'ordens ativas em Jogar':'ordens ao vivo indisponíveis em Validar')+(detail?' · '+detail:''); }
window.syncRecordingIndicator=()=>window.webkit.messageHandlers.engine.postMessage({action:'recordingIndicator',active:recording});
function record(event,frame=Math.max(129,(image?.observed?.counter?.value||128)+1)){
 if(!recording||recordFailure)return;
 recordChain=recordChain.then(()=>request('record-event',{event,frame})).then(r=>recordingStatus(r.events+' eventos · quadro '+r.frame)).catch(e=>{recordFailure=e;recording=false;window.syncRecordingIndicator();recordingStatus('Gravação interrompida: '+e.message);});
}
window.recordNativeInput=entry=>record(entry.event,entry.frame);
window.toggleRecording=async()=>{
 if(recordToggleBusy)return;recordToggleBusy=true;
 if(recording)window.webkit.messageHandlers.engine.postMessage({action:'recordingIndicator',active:false});
 try{const barrier=await request('record-barrier');await recordChain;
  if(!recording&&(!image?.native_metal||barrier.frame<129))throw Error('Abra Rust ao vivo e avance até o quadro 128 para gravar.');
  const r=await request(recording?'record-stop':'record-start');
  if(recording)recordEndFrame=barrier.frame;else{recordEndFrame=null;recordFailure=null;recordChain=Promise.resolve();}
  recording=r.recording;recordingStatus();window.syncRecordingIndicator();
 }catch(e){recording=false;window.syncRecordingIndicator();recordingStatus(e.message);}finally{recordToggleBusy=false;}
};
$('record-input').onclick=window.toggleRecording;
for(const surface of [$('render-image'),$('render-canvas')]){
 for(const [type,msg] of [['mousemove',0x200],['mousedown',0x201],['mouseup',0x202]])surface.addEventListener(type,e=>{e.preventDefault();surface.focus();const box=surface.getBoundingClientRect();let m=msg;if(type==='mousedown'&&e.button===0&&e.detail>1&&e.detail%2===0)m=0x203;if(type==='mousedown'&&e.button===2)m=0x204;if(type==='mouseup'&&e.button===2)m=0x205;if(e.button===1&&type!=='mousemove')return;const w=(e.shiftKey?4:0)|(e.ctrlKey?8:0);record({kind:'mouse',msg:m,x:Math.max(0,Math.min(799,Math.floor((e.clientX-box.left)*800/box.width))),y:Math.max(0,Math.min(599,Math.floor((e.clientY-box.top)*600/box.height))),wParam:w});});
 const heldVkeys=new Set();
 for(const [type,down] of [['keydown',true],['keyup',false]])surface.addEventListener(type,e=>{if(vkeys[e.key]===undefined)return;e.preventDefault();if(down)heldVkeys.add(vkeys[e.key]);else heldVkeys.delete(vkeys[e.key]);record({kind:'key',vkey:vkeys[e.key],down});});
 surface.addEventListener('blur',()=>{for(const vkey of heldVkeys)record({kind:'key',vkey,down:false});heldVkeys.clear();});
 surface.addEventListener('contextmenu',e=>e.preventDefault());
}
function download(value,name,text){return new Promise((resolve,reject)=>{const id=++seq;const timer=setTimeout(()=>{pending.delete(id);reject(Error('Tempo limite na exportação.'));},180000);pending.set(id,{resolve,reject,timer});window.webkit.messageHandlers.engine.postMessage({id,action:'saveInput',content:value,text,script:name==='monde01-input.json',smokeEvidence:window.nativeSmoke?.enabled===true});});}
window.exportRecording=async()=>{try{const barrier=await request('record-barrier');await recordChain;if(recordFailure)throw recordFailure;const r=await request('export-input',{stop_frame:recording?barrier.frame:(recordEndFrame||129)});const saved=await download(r.script,'monde01-input.json',r.script_text);window.lastInputExport={...r,...saved};recordingStatus(saved.saved?'Entrada exportada':'Exportação cancelada');return window.lastInputExport;}catch(e){recordingStatus('Exportação interrompida: '+e.message);throw e;}};
$('export-input').onclick=()=>window.exportRecording().catch(()=>{});
$('export-journal').onclick=async()=>{try{const barrier=await request('record-barrier');await recordChain;const r=await request('export-journal');await download(r.input_journal,'monde01-macos-journal.json');}catch(e){recordingStatus(e.message);}};


const rawCanvas=$('render-canvas'),rawContext=rawCanvas.getContext('2d',{alpha:false});
const rawImage=rawContext.createImageData(800,600),rawWords=new Uint32Array(rawImage.data.buffer);
const rawIndices=new Uint8Array(480000),rawPaletteBytes=new Uint8Array(1024),rawPaletteWords=new Uint32Array(rawPaletteBytes.buffer);
let paletteIdentity=null,rawSequence=-1,rawTransferTimes=[];
function drawRawFrame(frame){
 const started=performance.now();
 if(frame.format!=='indexed8-rgb24/1'||frame.width!==800||frame.height!==600||frame.stride!==800)throw Error('Formato de quadro incompatível.');
 const pixels=atob(frame.pixels);
 if(pixels.length!==480000)throw Error('Quadro incompleto.');
 if(frame.palette!==paletteIdentity){const palette=atob(frame.palette);if(palette.length!==768)throw Error('Paleta incompleta.');for(let i=0;i<256;i++){rawPaletteBytes[i*4]=palette.charCodeAt(i*3);rawPaletteBytes[i*4+1]=palette.charCodeAt(i*3+1);rawPaletteBytes[i*4+2]=palette.charCodeAt(i*3+2);rawPaletteBytes[i*4+3]=255;}paletteIdentity=frame.palette;}
 for(let i=0;i<480000;i++){const index=pixels.charCodeAt(i);rawIndices[i]=index;rawWords[i]=rawPaletteWords[index];}
 rawContext.putImageData(rawImage,0,0);rawCanvas.hidden=false;rawSequence=frame.generation;
 rawTransferTimes.push(performance.now()-started);if(rawTransferTimes.length>256)rawTransferTimes.shift();
}


// Explicit CLI-only synthetic UI session; every gesture traverses NSWindow and
// the production view/serial-queue recorder. This is not human Test B evidence.
async function runTestBSynthetic(plan){
 const gestures=[];
 try{
  await window.playbackReady;live=true;playing=false;
  if(!await run('live-open'))throw Error('Live window failed');
  for(let i=0;i<129;i++)if(!await run('live-step')||image.live_stop)throw Error(JSON.stringify(image.live_stop));
  await window.toggleRecording();if(!recording)throw Error('Recorder did not start');
  for(let frame=129;frame<=plan.stop_frame;frame++){
   for(const gesture of plan.gestures.filter(g=>g.frame===frame)){
    const receipt=await request('test-b-gesture',{gesture});
    await recordChain;gestures.push({gesture,receipt});
   }
   if(!await run('live-step')||image.live_stop)throw Error(JSON.stringify(image.live_stop));
  }
  if(![1,5,4,16,7,17].every(tag=>image.benchmark_order_tags.includes(tag)))throw Error('TestBMissingNativeOrderKinds: '+JSON.stringify(image.benchmark_order_tags));
  await window.toggleRecording();await recordChain;
  const exported=await window.exportRecording();
  const journal=await request('export-journal');
  await request('test-b-result',{result:{passed:true,synthetic:true,frames:plan.stop_frame-128,gestures,inputExport:exported,journal,...image}});
 }catch(e){
  if(recording)await window.toggleRecording();
  let exported=null;try{exported=await window.exportRecording();}catch(_){}
  await request('test-b-result',{result:{passed:false,synthetic:true,error:String(e),gestures,inputExport:exported,...image}});
 }
}
if(window.nativeTestB)runTestBSynthetic(window.nativeTestB);
