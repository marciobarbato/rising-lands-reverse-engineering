/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall OriginaisSBL::Chemin_ModifieZone(ushort *param_1,uint param_2,byte param_3)

{
  uint in_EAX;
  int iVar1;
  undefined1 uVar2;
  ushort uVar3;
  undefined1 unaff_BL;
  char cVar4;

  switch(unaff_BL) {
  case 0:
    iVar1 = (uint)param_3 + param_2 * 8;
    uVar2 = (undefined1)iVar1;
    cVar4 = (char)((uint)iVar1 >> 8) + '@';
    uVar3 = CONCAT11(cVar4,uVar2);
    if ((&DAT_004962c8)[tabela_unidades[param_2 & 0xffff].tipo_id] != '\x01') {
      uVar3 = CONCAT11(cVar4,uVar2) | 4;
    }
    param_2 = (uint)(DAT_004e0f38 + (in_EAX & 0xffff));
    if (uVar3 == *(ushort *)param_2) {
      *(ushort *)param_2 = *param_1;
LAB_0043e1ad:
      return CONCAT31((int3)(param_2 >> 8),1);
    }
    break;
  case 1:
    iVar1 = (uint)param_3 + param_2 * 0x20;
    param_2 = (uint)(DAT_004e0f38 + (in_EAX & 0xffff));
    if (CONCAT11((char)((uint)iVar1 >> 8) + -0x80,(char)iVar1) == *(ushort *)param_2) {
      *(ushort *)param_2 = *param_1;
      param_2 = MurRetire();
      goto LAB_0043e1ad;
    }
    break;
  case 2:
    iVar1 = param_2 * 8 + (uint)param_3;
    uVar2 = (undefined1)iVar1;
    cVar4 = (char)((uint)iVar1 >> 8) + '@';
    uVar3 = CONCAT11(cVar4,uVar2);
    if ((&DAT_004962c8)[tabela_unidades[param_2 & 0xffff].tipo_id] != '\x01') {
      uVar3 = CONCAT11(cVar4,uVar2) | 4;
    }
    param_2 = (uint)(DAT_004e0f38 + (in_EAX & 0xffff));
    if (*(ushort *)param_2 < 0x4000) {
      *param_1 = *(ushort *)param_2;
      param_2 = (uint)DAT_004e0f38;
      DAT_004e0f38[in_EAX & 0xffff] = uVar3;
      goto LAB_0043e1ad;
    }
    break;
  case 3:
    iVar1 = (uint)param_3 + param_2 * 0x20;
    param_2 = (uint)(DAT_004e0f38 + (in_EAX & 0xffff));
    if (*(ushort *)param_2 < 0x4000) {
      *param_1 = *(ushort *)param_2;
      DAT_004e0f38[in_EAX & 0xffff] = CONCAT11((char)((uint)iVar1 >> 8) + -0x80,(char)iVar1);
      param_2 = MurAjoute();
      goto LAB_0043e1ad;
    }
  }
  return param_2 & 0xffffff00;
}
