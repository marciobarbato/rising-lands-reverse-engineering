/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0042436c, entrada 0042436c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_0042436c(uint param_1,byte param_2)

{
  byte bVar1;
  char cVar2;
  ushort in_AX;
  uint uVar3;
  uint uVar4;
  uint extraout_ECX;
  int extraout_ECX_00;
  int extraout_ECX_01;
  int iVar5;
  int extraout_ECX_02;
  ushort indice_unidade;
  short sVar6;
  ushort unaff_BX;
  bool bVar7;
  undefined8 uVar8;
  ushort local_24;
  ushort local_1c;

  uVar3 = (uint)(byte)(&DAT_0049a0d0)[(uint)in_AX * 0x114];
  if ((uVar3 != 0xb) && (uVar3 != 10)) goto LAB_004243b0;
  if (param_2 != 0) {
    if (param_2 < 2) {
      bVar1 = unidade_obter_proprietario(unaff_BX);
      uVar3 = (uint)bVar1;
      if (uVar3 == 200) goto LAB_004243b0;
      unidade_obter_tipo(indice_unidade);
      cVar2 = FUN_004422cf();
      param_1 = extraout_ECX;
      if (cVar2 != '\0') {
        bVar7 = (&DAT_0049a0d0)[(uint)in_AX * 0x114] == '\n';
        goto LAB_0042440f;
      }
    }
    else if (param_2 == 3) {
      bVar7 = (&DAT_0049a0cc)[(uint)unaff_BX * 0x114] == -0x38;
LAB_0042440f:
      uVar3 = 0;
      if (bVar7) goto LAB_004243b0;
    }
  }
  local_1c = *(ushort *)(&DAT_0049a0ca + (uint)in_AX * 0x114) / 0x100;
  switch((&DAT_0049a0d0)[(uint)in_AX * 0x114]) {
  case 0:
    param_1 = 0x14;
    break;
  case 1:
  case 3:
  case 5:
  case 6:
  case 7:
  case 8:
  case 0xd:
  case 0xe:
  case 0xf:
  case 0x10:
  case 0x12:
  case 0x14:
    param_1 = 8;
    break;
  case 2:
    param_1 = 10;
    break;
  case 4:
    param_1 = 5;
    break;
  case 10:
  case 0xb:
    param_1 = 7;
    break;
  case 0x11:
  case 0x13:
  case 0x15:
    param_1 = 4;
  }
  uVar3 = FUN_00428cc0(param_1,4);
  if (param_2 < 3) {
    if (param_2 == 1) {
      FUN_0044113e(extraout_ECX_00,0);
      uVar8 = FUN_0044113e(0x100,0);
      iVar5 = extraout_ECX_01;
      goto LAB_00424550;
    }
  }
  else if (param_2 < 4) {
    FUN_0041aee2();
    uVar8 = FUN_0041aee2();
    iVar5 = extraout_ECX_02;
LAB_00424550:
    sVar6 = (short)((ulonglong)uVar8 >> 0x30);
    local_24 = (ushort)(CONCAT44((int)sVar6 >> 0xf,CONCAT22(sVar6,(short)uVar8)) / (longlong)iVar5);
  }
  else if (param_2 == 5) goto LAB_004243b0;
  uVar4 = extraout_ECX_00 + uVar3 & 0xffff;
  uVar3 = FUN_00479555(local_24,local_1c);
  if (uVar3 <= uVar4 * uVar4) {
    return CONCAT31((int3)(uVar3 >> 8),1);
  }
LAB_004243b0:
  return uVar3 & 0xffffff00;
}
