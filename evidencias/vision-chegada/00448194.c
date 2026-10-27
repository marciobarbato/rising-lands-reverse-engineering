/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall OriginaisSBL::EnginEnArret(undefined4 param_1,undefined4 param_2)

{
  ushort in_AX;
  UnidadeParcial *pUVar1;
  undefined3 uVar2;
  undefined1 uVar3;

  pUVar1 = tabela_unidades + in_AX;
  uVar3 = 0;
  uVar2 = (undefined3)((uint)pUVar1 >> 8);
  switch(pUVar1->tipo_id) {
  case 0:
  case 6:
    pUVar1->quadro_movimento = 2;
    return CONCAT44(param_2,CONCAT31(uVar2,1));
  case 1:
  case 4:
  case 7:
  case 0x12:
  case 0x13:
  case 0x17:
  case 0x18:
    pUVar1->quadro_movimento = 3;
    return CONCAT44(param_2,CONCAT31(uVar2,1));
  case 2:
  case 3:
  case 0x19:
    pUVar1->quadro_movimento = 7;
    return CONCAT44(param_2,CONCAT31(uVar2,1));
  case 5:
  case 9:
    pUVar1->quadro_movimento = 5;
    return CONCAT44(param_2,CONCAT31(uVar2,1));
  case 8:
  case 0x15:
  case 0x16:
    pUVar1->quadro_movimento = 0;
  case 0xb:
  case 0xc:
  case 0xd:
  case 0xe:
  case 0xf:
  case 0x11:
    return CONCAT44(param_2,CONCAT31(uVar2,1));
  case 10:
  case 0x10:
    pUVar1->quadro_movimento = 6;
    return CONCAT44(param_2,CONCAT31(uVar2,1));
  case 0x14:
    uVar3 = 1;
    pUVar1->quadro_movimento = 1;
  default:
    return CONCAT44(param_2,CONCAT31(uVar2,uVar3));
  }
}
