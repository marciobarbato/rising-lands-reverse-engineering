/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00421387, entrada 00421387.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00421387(undefined4 param_1,undefined4 param_2)

{
  ushort uVar1;
  byte bVar2;
  ushort in_AX;
  uint3 uVar5;
  undefined *puVar3;
  int iVar4;
  undefined4 extraout_ECX;
  undefined4 uVar6;
  undefined4 extraout_ECX_00;
  int extraout_EDX;
  int extraout_EDX_00;
  undefined8 uVar7;

  unidade_obter_tipo(*(ushort *)(&DAT_0049a150 + (uint)in_AX * 0x114));
  FUN_00442434();
  bVar2 = unidade_obter_tipo(*(ushort *)(extraout_EDX + 0x88));
  uVar6 = extraout_ECX;
  if (bVar2 == 3) {
    uVar6 = 0xffffffab;
  }
  if (*(short *)(extraout_EDX_00 + 0x88) == -1) {
    return CONCAT44(param_2,0xffff);
  }
  uVar1 = *(ushort *)(extraout_EDX_00 + 0x7e);
  if (uVar1 == 0) {
    iVar4 = (uint)in_AX * 0x114;
    (&DAT_0049a13d)[iVar4] = 1;
    uVar5 = (uint3)((uint)(&DAT_0049a0c8 + iVar4) >> 8);
    if (((&DAT_0049a13e)[iVar4] == '\a') && ((&DAT_0049a13d)[iVar4] != '\0')) {
      puVar3 = (undefined *)CONCAT31(uVar5,1);
    }
    else {
      puVar3 = (undefined *)((uint)uVar5 << 8);
    }
    if ((char)puVar3 != '\0') {
LAB_00421442:
      *(short *)(extraout_EDX_00 + 0x7e) = *(short *)(extraout_EDX_00 + 0x7e) + 1;
      return CONCAT44(param_2,puVar3);
    }
  }
  else if (uVar1 < 2) {
    iVar4 = (uint)in_AX * 0x114;
    uVar5 = (uint3)((uint)(&DAT_0049a0c8 + iVar4) >> 8);
    if (((&DAT_0049a13e)[iVar4] == '\a') && ((&DAT_0049a13d)[iVar4] != '\0')) {
      puVar3 = (undefined *)CONCAT31(uVar5,1);
    }
    else {
      puVar3 = (undefined *)((uint)uVar5 << 8);
    }
    if ((char)puVar3 != '\0') {
      if ((short)uVar6 < *(short *)(extraout_EDX_00 + 0x82)) {
        uVar7 = FUN_00443688(uVar6,extraout_EDX_00);
        iVar4 = (int)((ulonglong)uVar7 >> 0x20);
        *(ushort *)(iVar4 + 0x82) = *(short *)(iVar4 + 0x82) - (ushort)(byte)uVar7;
        uVar7 = FUN_00448088(extraout_ECX_00,iVar4);
        return CONCAT44(param_2,(int)uVar7);
      }
      puVar3 = &DAT_0049a0c8 + (uint)in_AX * 0x114;
      (&DAT_0049a13d)[(uint)in_AX * 0x114] = 0;
      goto LAB_00421442;
    }
  }
  else {
    if (uVar1 != 2) {
      return CONCAT44(param_2,(uint)uVar1);
    }
    iVar4 = (uint)in_AX * 0x114;
    uVar5 = (uint3)((uint)(&DAT_0049a0c8 + iVar4) >> 8);
    if (((&DAT_0049a13e)[iVar4] == '\0') && ((&DAT_0049a13d)[iVar4] == '\0')) {
      puVar3 = (undefined *)CONCAT31(uVar5,1);
    }
    else {
      puVar3 = (undefined *)((uint)uVar5 << 8);
    }
    if ((char)puVar3 != '\0') {
      FUN_0041f76e(uVar6,(uint)*(ushort *)(extraout_EDX_00 + 0x88));
      uVar6 = FUN_004212f5();
      return CONCAT44(param_2,uVar6);
    }
  }
  return CONCAT44(param_2,puVar3);
}
