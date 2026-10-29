'use strict';
const $=id=>document.getElementById(id);
let image=null,seq=0,pending=new Map();
function request(operation,extra={}){return new Promise((resolve,reject)=>{const id=++seq;const timer=setTimeout(()=>{pending.delete(id);reject(Error('Tempo limite na inspeção.'));},60000);pending.set(id,{resolve,reject,timer});window.webkit.messageHandlers.engine.postMessage({id,action:'playback',operation,...extra});});}
window.receive=response=>{const p=pending.get(response.id);if(!p)return;clearTimeout(p.timer);pending.delete(response.id);response.ok?p.resolve(response.playback):p.reject(Error(response.error));};
function row(values){const tr=document.createElement('tr');for(const v of values){const td=document.createElement('td');td.textContent=String(v);tr.append(td);}return tr;}
function blocks(){if(!image)return;const filter=$('filter').value.toLowerCase();const found=image.memory.filter(b=>`${b.name} ${b.base}`.toLowerCase().includes(filter));$('blocks').replaceChildren(...found.slice(0,100).map(b=>row([b.name,b.base,b.bytes,b.sha256])));$('block-count').textContent=`${image.blocks} blocos · ${image.bytes} bytes · ${found.length} resultados`}
function apply(value){image=value;$('phase').replaceChildren(...['state_s0',...value.phases].map(name=>{const o=document.createElement('option');o.value=name;o.textContent=name;return o;}));$('phase').value=value.phase;$('status').textContent=`${value.scenario}\n${value.phase} · resumo verificado · ${value.checkpoint_verified?'checkpoint igual':'sem checkpoint nesta fase'}\n${value.verified_phases}/257 fases e ${value.verified_checkpoints}/11 checkpoints verificados\nEstado: ${value.summary_sha256}`;$('words').replaceChildren(...Object.entries(value.observed).map(([name,w])=>row([name,w.address,w.value,`0x${w.value.toString(16)}`])));const r=value.render;$('render-status').textContent=(r.status==='full'?'Composição completa':r.status==='partial'?'Imagem parcial · parada explícita':'Render interrompido')+'\n'+(r.stop?`${r.stop.endereco}: ${r.stop.detalhe}`:(r.detail||''));$('render-image').hidden=!r.image;if(r.image)$('render-image').src=r.image;else $('render-image').removeAttribute('src');for(const id of ['phase','previous','next','go-frame','reset'])$(id).disabled=false;$('previous').disabled=value.phase_index<0;$('next').disabled=value.phase_index>=256;blocks();}
async function run(operation,extra={}){try{for(const id of ['phase','previous','next','go-frame','reset'])$(id).disabled=true;apply(await request(operation,extra));}catch(e){if(image)apply(image);$('status').textContent='Falha na inspeção: '+e.message;}}
$('phase').onchange=()=>run('phase',{phase:$('phase').value});$('previous').onclick=()=>run('phase',{phase:image.phase_index===0?'state_s0':image.phase_index-1});$('next').onclick=()=>run('phase',{phase:image.phase_index+1});$('go-frame').onclick=()=>run('frame',{frame:Number($('frame').value)});$('reset').onclick=()=>run('reset');$('filter').oninput=blocks;$('read-form').onsubmit=async event=>{event.preventDefault();try{const r=await request('read',{address:$('address').value,size:Number($('size').value)});$('read-result').textContent=r.read_hex;}catch(e){$('read-result').textContent=e.message;}};
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
 $('frame').value='128';$('go-frame').click();await until(()=>image.phase==='frame128'&&!$('phase').disabled,'frame 128');
 check('DOM frame selection reaches frame128',image.observed.counter.value===128);
 check('missing previous surface shown without fallback image',image.render.code==='missing_previous_surface'&&$('render-image').hidden&&!$('render-image').hasAttribute('src')&&$('render-status').textContent.includes('Missing previous surface'));
 $('filter').value='dgroup';$('filter').dispatchEvent(new Event('input'));
 check('DOM block filter', $('blocks').children.length===1&&$('blocks').textContent.includes('dgroup'));
 $('reset').click();await until(()=>image.phase==='state_s0'&&!$('phase').disabled,'reset');
 check('DOM reset preserves initial state identity',image.summary_sha256===initial);
 return {passed:true,tests,commit:image.commit,scenario:image.scenario,render:image.render.status};
};
window.playbackReady=run('open');
