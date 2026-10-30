//! Typed structure-entry effects, pinned Core entrada_estruturas54d148d.
//! Scratch GPRs are not part of these typed effect APIs.
use crate::{frame::stop,player::{self,alive,structure,unit,Memory},FrameRegisters as R,MemoriaJogo,Result};
pub fn adjacent(m:&mut MemoriaJogo,s:u16,c:u16)->Result<bool>{
 let a=structure(u32::from(s));let (x,y)=(i32::from(c&255),i32::from(c>>8));
 for dy in -1..=1{if !(0..256).contains(&(y+dy)){continue}
  for dx in -1..=1{if !(0..256).contains(&(x+dx)){continue}
   let neighbor=u32::from(c).wrapping_add((dy*256+dx)as u32)&65535;
   let origin=m.w(a+2)?;let t=m.b(a+8)?;let(w,h)=(m.w(0x495d8c+52*t)?,m.w(0x495d8e+52*t)?);
   let width=(u32::from(s)*276&0xffff0000)|w;
   for cy in 0..h{for cx in 0..w{
    if origin+(cy<<8)+cx==neighbor&&crate::frame_core::call(m,"BatimentCollision",&[m.b(a+8)?,(width*cy+cx)&65535])?&255!=0{return Ok(true)}
   }}
  }
 }Ok(false)
}
pub fn entry_cell(m:&MemoriaJogo,s:u16,u:u16)->Result<u32>{
 let a=structure(u32::from(s));let t=m.b(a+8)?;
 Ok(if t==14{((u32::from(s)*276&0xffff0000)|m.w(a+2)?)+0x402}
 else if t==8{let k=m.b(unit(m,u32::from(u))?+1)?;m.w(a+2)?+if k==3||(11..=17).contains(&k){0x403}else{0x303}}
 else{0})
}
pub fn set_enter(m:&mut MemoriaJogo,u:u16,s:u16)->Result<()> {
 let a=unit(m,u32::from(u))?;let b=structure(u32::from(s));let t=m.b(b+8)?;
 let k=if matches!(t,8|14|18){Some(m.b(a+1)?)}else{None};
 if t==8&&k!=Some(9)||t==14&&k.is_some_and(|v|(11..=17).contains(&v))&&m.b(b+5)?!=4{
  let c=entry_cell(m,s,u)?;m.sw(a+0xb2,c)?;m.sw(a+0x7e,c)?;
  crate::frame_spawn::release(m,u32::from(u))?;m.sb(a+0x88,0)?;m.sw(a+0xc0,u32::from(s))?;
  if alive(m,u32::from(u))?{m.sb(a+2,if t==8{21}else{13})?;crate::frame_spawn::release(m,u32::from(u))?;}
  return Ok(())
 }
 let mut c=crate::frame_core::building_cell(m,u32::from(s))?;
 if t==18&&k==Some(16){c=c.wrapping_add(1);m.sw(a+0xb2,c)?;}
 m.sw(a+0x7e,c)?;crate::frame_spawn::release(m,u32::from(u))?;
 m.sb(a+0x88,0)?;m.sw(a+0xc0,u32::from(s))?;
 if alive(m,u32::from(u))?{m.sb(a+2,13)?;crate::frame_spawn::release(m,u32::from(u))?;}
 Ok(())
}
pub fn retire(m:&mut MemoriaJogo,u:u16)->Result<()> {
 let a=unit(m,u32::from(u))?;let cell=m.w(a+8)?;
 crate::player_orders::call(m,"DeselectionEngin",[u32::from(u),0,0,0],0x457058)?;
 crate::frame_movement::call(m,"ResetEnginCollision",&[u32::from(u),cell])?;
 if m.w(a+8)?!=m.w(a+0x7c)?{crate::frame_movement::call(m,"ResetEnginCollision",&[u32::from(u),m.w(a+0x7c)?])?;}
 m.sb(a+0x72,0)?;let p=m.b(a)?;crate::player_sight::minimap(m,p as u8,cell as u16,5)?;
 if !matches!(p,4|200){crate::player_sight::area(m,m.w(a+8)?as u16,m.b(a+0xbb)?+m.b(a+0xf5)?,p as u8,2)?;}
 Ok(())
}
pub fn reset_type(m:&mut MemoriaJogo,u:u16)->Result<()> {
 let a=unit(m,u32::from(u))?;
 for(off,v)in[(1,9),(0x93,1),(0x98,2),(0xa7,2),(0xa8,4),(0xa5,8),(0x9d,255),(0xac,3),(0xad,3),(0x99,0),(0xbb,5)]{m.sb(a+off,v)?;}
 let b=a+10;for off in[0,0x66,4,2]{m.sw(b+off,0)?;}
 for i in 0..30{m.sw(b+6+2*i,0)?;m.sb(b+0x42+i,0)?;}m.sw(b+2,0)?;
 let maximum=m.w(0x4965b6+50*m.b(unit(m,u32::from(u))?+1)?)?;
 if maximum<m.w(a+0x9a)?{m.sw(a+0x9a,maximum)?;}Ok(())
}

fn bag(m:&mut MemoriaJogo,name:&str,a:u32,d:u32,b:u32)->Result<R>{
 crate::chain_bags::body(m,name,R{eax:a,edx:d,ebx:b,..Default::default()})
}
fn low(v:u32,b:u32)->u32{(v&!255)|(b&255)}
pub fn place_free(m:&mut MemoriaJogo,mut r:R)->Result<R>{
 let(s,u)=(r.eax&65535,r.edx&65535);let a=structure(s);let t=m.b(a+8)?;let b=a+12;
 if t==8{let n=m.w(b)?;let limit=(m.b(0x495be9)?>>1)+1;let ok=u32::from(n<limit);r.eax=low(limit,ok);r.edx=low(n,ok);return Ok(r)}
 if t!=19{let q=bag(m,"BagAccepte",b,1,r.ebx)?;let ok=u32::from(q.eax&255!=0);r.eax=low(q.eax,ok);r.edx=low(q.edx,ok);return Ok(r)}
 let rec=unit(m,u)?;let life=m.w(rec+0x9a)?;let k=m.b(rec+1)?;let max=m.w(0x4965b6+50*k)?;
 if life==max&&k!=9{r.eax=low(k,0);r.edx=low(u,0);return Ok(r)}
 let q=bag(m,"BagAccepte",b,1,life)?;
 if q.eax&255==0{r.eax=low(q.eax,0);r.edx=low(q.edx,0);return Ok(r)}
 let(mut other,mut full)=(0,0);
 for i in 0..m.w(b)?{if m.b(b+0x42+i)?!=1{continue}
  let v=unit(m,m.w(b+6+2*i)?)?;let vt=m.b(v+1)?;
  if vt!=9{other+=1}else if m.w(v+0x9a)?==m.w(0x4965b6+50*vt)?{full+=1}else{other+=1}
 }
 if k==9&&m.w(rec+0x9a)?==m.w(0x4965b6+50*m.b(rec+1)?)?{
  let limit=m.b(0x495d8c+52*m.b(a+8)?+18)?.wrapping_sub(m.b(0x495be8)?)&255;
  let ok=u32::from(full<limit);r.eax=ok;r.edx=low(full,ok);
 }else{let limit=m.b(0x495be8)?;let ok=u32::from((other&65535)<limit);r.eax=low(limit,ok);r.edx=low(other&65535,ok);}
 Ok(r)
}

/// BatimentAjouteMatiere credit path. The unported excess-sack provider remains
/// an addressed dependency after the credit, as in the reference.
pub fn credit(m:&mut MemoriaJogo,resource:u8,quantity:u16,p:u8,s:u16)->Result<()> {
 let a=structure(u32::from(s));let t=m.b(a+8)?;
 if t==4{return stop("BatimentAjouteMatiere",0x423511)}
 let cave=0x4dfb2c+6*u32::from(p);let count=m.w(cave)?;
 let excess=if count==0{u32::from(quantity)}else{
  let base=0x4e2ea8+32*u32::from(p);
  let food=m.w(base+10)?.wrapping_sub(m.w(base+8)?)&65535;
  let stone=m.w(base+18)?.wrapping_sub(m.w(base+16)?)&65535;
  let stock=(food+stone)&65535;let capacity=count*m.w(cave+2)?&65535;
  let(mut extra,mut amount)=(0,u32::from(quantity));
  if amount+stock>capacity{extra=amount.wrapping_add(stock).wrapping_sub(capacity);amount=capacity.wrapping_sub(stock);}
  let total=0x4e2eaa+32*u32::from(p)+8*u32::from(resource);
  let sum=m.w(total)?.wrapping_add(amount&65535)&65535;m.sw(total,sum)?;
  if sum>9999{m.sw(total,9999)?;}
  let per=m.w(cave+2)?;
  if per==0{return stop("BatimentAjouteMatiere capacity division",0x423501)}
  m.sb(cave+4,(((stock.wrapping_add(amount))&65535)/count)*7/per)?;
  extra&65535
 };
 if excess!=0&&matches!(t,2|3){return stop("TerrainDeposeSac",0x4235b1)}
 Ok(())
}
pub fn lodge(m:&mut MemoriaJogo,s:u16,u:u16)->Result<bool>{
 let a=structure(u32::from(s));let rec=unit(m,u32::from(u))?;let kind=m.b(rec+1)?;
 if kind==10{return stop("BatimentLogeEngin",0x41f7ab)}
 let t=m.b(a+8)?;let b=a+12;
 let occupied=if matches!(t,2|21){
  let troop=bag(m,"BagContientTroupe",b,0,0)?.eax&255!=0;
  troop||(t==2&&bag(m,"BagContient",b,1,9)?.eax&65535!=0)
 }else{bag(m,"BagContient",b,1,9)?.eax&65535!=0};
 if occupied&&m.b(rec)?!=m.b(a+4)?{return Ok(false)}
 if place_free(m,R{eax:u32::from(s),edx:u32::from(u),..Default::default()})?.eax&255==0{return Ok(false)}
 if kind!=9{
  for resource in[2,1]{while bag(m,"BagContient",rec+10,2,resource)?.eax&65535!=0{
   credit(m,resource as u8,1,m.b(rec)?as u8,s)?;
   bag(m,"BagRetire",rec+10,2,resource)?;
  }}
 }
 if m.b(a+4)?==200{
  m.sb(a+4,m.b(rec)?)?;crate::chain_habitation::habitable(m,u32::from(s))?;
  crate::chain_vision::structure_minimap(m,s,1)?;
  crate::chain_habitation::own(m,"InitBatimentPlayer",R{eax:u32::from(s),edx:m.b(rec)?,..Default::default()})?;
  if m.b(a+4)?==m.b(0x508041)?{
   let volume=crate::player_orders::volume(m,m.w(a+2)?)?;
   if m.d(a+0x100)?==u32::MAX{player::sound(m,0x41faeb,true,[0x42,(m.b(a+8)?<<16)|0x2700,a+0x100,0],Some(volume))?;}
  }
 }
 bag(m,"BagPrend",b,1,u32::from(u))?;Ok(true)
}
pub fn calculate(m:&mut MemoriaJogo,u:u16)->Result<()> {
 let rec=unit(m,u32::from(u))?;let t=m.b(rec+1)?;
 if t>10&&t!=25{return stop("CalculEntreBatiment",if t==16{0x449c56}else{0x44a12f})}
 let s=m.w(rec+0xc0)?as u16;if s==65535{return Ok(())}
 let a=structure(u32::from(s));
 if m.b(a+8)?==8&&m.b(a+4)?==m.b(rec)?{
  let c=entry_cell(m,s,u)?;m.sw(rec+0xb2,c)?;m.sw(rec+0x7e,c)?;
  crate::frame_spawn::release(m,u32::from(u))?;m.sb(rec+0x88,0)?;
  if alive(m,u32::from(u))?{m.sb(rec+2,21)?;crate::frame_spawn::release(m,u32::from(u))?;}
  return Ok(())
 }
 let near=m.b(rec+0x86)?==0&&m.b(rec+0x87)?==0&&adjacent(m,s,m.w(rec+8)?as u16)?;
 if !near{
  if m.w(rec+0x7e)?==m.w(rec+8)?{
   let c=crate::frame_core::building_cell(m,u32::from(s))?;m.sw(rec+0x7e,c)?;
   crate::frame_spawn::release(m,u32::from(u))?;m.sb(rec+0x88,0)?;
  }
  crate::frame_movement::displace(m,u32::from(u))?;return Ok(())
 }
 if !lodge(m,s,u)?{
  if alive(m,u32::from(u))?{m.sb(rec+2,7)?;crate::frame_spawn::release(m,u32::from(u))?;}
  return Ok(())
 }
 let c=crate::frame_core::building_cell(m,u32::from(s))?;retire(m,u)?;
 let kind=m.b(rec+1)?;let structure_kind=m.b(a+8)?;
 if kind==10&&structure_kind==16{return stop("iagUnitSendMessage",0x4499ee)}
 if kind==10&&structure_kind==2&&m.b(a+4)?!=m.b(rec)?{return stop("PlayerInitPropositionAlliance",0x449ad7)}
 if kind!=9&&!matches!(structure_kind,19|21){
  crate::frame_ai::call(m,"iagUnitSendMessage",&[u32::from(u),0x47,0])?;reset_type(m,u)?;
 }
 m.sw(rec+0x7c,c)?;m.sw(rec+8,c)?;
 crate::player_orders::call(m,"DeselectionEngin",[u32::from(u),0,0,0],0x449be6)?;
 m.sb(rec+2,14)
}
/// State13 consumes the dispatcher's record pointer, without demanding an
/// unneeded pool pointer on its no-target prefix.
pub fn state13(m:&mut MemoriaJogo,u:u16,rec:u32)->Result<()> {
 let s=m.w(rec+0xc0)?as u16;
 if s==65535{
  if m.w(rec+0xb8)?==65535{return Ok(())}
  return stop("EnginNextEtape state 13",0x4559c6)
 }
 let a=structure(u32::from(s));let mut refused=m.b(a+5)?==3;
 if !refused{
  let(p,q)=(m.b(a+4)?,m.b(rec)?);
  refused=if m.b(rec+1)?==10{p==200||(p==q&&m.b(a+8)?==16)}else{p!=q&&!(p==200&&m.b(rec+1)?==9)};
 }
 if refused{
  crate::frame_spawn::order(m,u32::from(u),m.w(rec+0x7e)?as u16)?;m.sw(rec+0xc0,65535)?;
  Ok(())
 }else{calculate(m,u)}
}
pub fn select_enter(m:&mut MemoriaJogo,p:u8,s:u16)->Result<()> {
 let t=m.b(structure(u32::from(s))+8)?;let base=0x508728+(u32::from(p)<<9);let(mut i,mut spoke)=(0,false);
 while i<m.w(base)?{
  let u=m.w(base+2+2*i)?;i+=1;if !alive(m,u)?{continue}
  let k=m.b(unit(m,u)?+1)?;set_enter(m,u as u16,s)?;
  if spoke{continue}spoke=true;
  if u32::from(p)!=m.b(0x508041)?{continue}
  let mode=match t{1|10|13=>Some(14),2 if k!=10=>Some(10),16 if k==9=>Some(25),16 if k==10=>Some(36),_=>None};
  if let Some(mode)=mode{crate::player_orders::ask(m,u,mode,0,u)?;}
 }Ok(())
}
