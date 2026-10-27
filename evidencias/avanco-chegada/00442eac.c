/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void OriginaisSBL::ResetEnginCollision(void)

{
  UnidadeParcial *pUVar1;
  uint in_EAX;
  ushort extraout_CX;
  ushort *puVar2;
  ushort *extraout_ECX;
  ushort *extraout_ECX_00;
  ushort *extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  uint extraout_ECX_04;
  uint uVar3;
  uint uVar4;
  byte bVar5;

  pUVar1 = tabela_unidades;
  uVar4 = in_EAX & 0xffff;
  switch(tabela_unidades[uVar4].tipo_id) {
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
    puVar2 = (ushort *)&tabela_unidades[uVar4].field_0xfa;
    ResetCollision(in_EAX,1);
    bVar5 = 0;
    uVar3 = (uint)extraout_CX;
    break;
  case 3:
  case 0xb:
  case 0xc:
  case 0xd:
  case 0xe:
  case 0xf:
  case 0x19:
    uVar3 = in_EAX & 0xffff;
    ResetCollision(in_EAX,1);
    Chemin_ModifieZone((ushort *)&pUVar1[uVar4].field_0xfa,uVar3,0);
    ResetCollision(&pUVar1[uVar4].field_0xfc,1);
    Chemin_ModifieZone(extraout_ECX,uVar3,1);
    ResetCollision(&pUVar1[uVar4].field_0xfe,1);
    Chemin_ModifieZone(extraout_ECX_00,uVar3,2);
    ResetCollision(&pUVar1[uVar4].field_0x100,1);
    bVar5 = 3;
    puVar2 = extraout_ECX_01;
    break;
  case 0x10:
    ResetCollision(in_EAX,2);
    ResetCollision(extraout_ECX_02,2);
    ResetCollision(extraout_ECX_03,2);
    in_EAX = extraout_ECX_04;
    goto LAB_00442f25;
  case 0x11:
LAB_00442f25:
    ResetCollision(in_EAX,2);
  default:
    goto switchD_00442ee4_default;
  }
  Chemin_ModifieZone(puVar2,uVar3,bVar5);
switchD_00442ee4_default:
  FUN_00445f27();
  return;
}
