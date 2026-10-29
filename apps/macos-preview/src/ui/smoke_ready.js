'use strict';
// Native smoke instrumentation only; it does not advance game state or relax
// any assertion. A bounded diagnostic delay exercises slow initialization.
(()=>{
 const send=(action,extra)=>{if(window.nativeSmoke?.enabled)window.webkit.messageHandlers.engine.postMessage({action,...extra});};
 window.reportSmokeProgress=stage=>send('smokeProgress',{stage,diagnostics:window.smokeDiagnostics?window.smokeDiagnostics():{}});
 window.signalAppInitializationFailure=error=>send('appInitializationFailed',{error:String(error)});
 window.signalAppReady=async info=>{
  if(!window.nativeSmoke?.enabled)return;
  try{
   if(info.worker!==true||info.assets!==true||!info.commit)throw Error('Incomplete application readiness');
   const delay=window.nativeSmoke.readyDelayMs||0;
   if(delay)await new Promise(resolve=>setTimeout(resolve,delay));
   send('appReady',{protocol:1,...info});
  }catch(error){window.signalAppInitializationFailure(error);}
 };
})();
