/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::SetEnginCollision(undefined4 param_1)

{
  UnidadeParcial *pUVar1;
  ushort in_AX;
  ushort *extraout_ECX;
  ushort *puVar2;
  ushort *extraout_ECX_00;
  ushort *extraout_ECX_01;
  ushort *extraout_ECX_02;
  ushort *extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  undefined4 extraout_ECX_06;
  uint uVar3;
  byte bVar4;

  pUVar1 = tabela_unidades;
  switch(tabela_unidades[in_AX].tipo_id) {
  case 0:
  case 1:
  case 2:
  case 4:
  case 5:
  case 6:
  case 7:
  case 8:
  case 9:
  case 10:
  case 0x12:
  case 0x13:
  case 0x14:
  case 0x15:
  case 0x16:
  case 0x17:
  case 0x18:
    SetCollision(&tabela_unidades[in_AX].field_0xfa,1);
    bVar4 = 0;
    puVar2 = extraout_ECX;
    break;
  case 3:
  case 0xb:
  case 0xc:
  case 0xd:
  case 0xe:
  case 0xf:
  case 0x19:
    uVar3 = (uint)in_AX;
    SetCollision(&tabela_unidades[in_AX].field_0xfa,1);
    Chemin_ModifieZone(extraout_ECX_00,uVar3,0);
    SetCollision(&pUVar1[in_AX].field_0xfc,1);
    Chemin_ModifieZone(extraout_ECX_01,uVar3,1);
    SetCollision(&pUVar1[in_AX].field_0xfe,1);
    Chemin_ModifieZone(extraout_ECX_02,uVar3,2);
    SetCollision(&pUVar1[in_AX].field_0x100,1);
    bVar4 = 3;
    puVar2 = extraout_ECX_03;
    break;
  case 0x10:
    SetCollision(param_1,2);
    SetCollision(extraout_ECX_04,2);
    SetCollision(extraout_ECX_05,2);
    param_1 = extraout_ECX_06;
    goto LAB_00442d31;
  case 0x11:
LAB_00442d31:
    SetCollision(param_1,2);
  default:
    goto switchD_00442ee4_default;
  }
  Chemin_ModifieZone(puVar2,(uint)in_AX,bVar4);
switchD_00442ee4_default:
  FUN_00445f27();
  return;
}
