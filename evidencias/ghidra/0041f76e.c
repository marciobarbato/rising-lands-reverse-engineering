/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0041f76e, entrada 0041f76e.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0041f76e(undefined4 param_1,uint param_2)

{
  ushort indice_unidade;
  byte bVar1;
  ushort in_AX;
  int iVar2;
  int iVar3;
  undefined4 uVar4;
  uint uVar5;
  ushort indice_unidade_00;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  undefined4 extraout_ECX_06;
  undefined4 extraout_ECX_07;
  undefined4 extraout_ECX_08;
  undefined4 extraout_ECX_09;
  undefined4 extraout_ECX_10;
  undefined *extraout_ECX_11;
  undefined4 extraout_ECX_12;
  undefined4 extraout_ECX_13;
  uint extraout_ECX_14;
  undefined4 extraout_ECX_15;
  undefined4 extraout_ECX_16;
  undefined *extraout_ECX_17;
  uint extraout_ECX_18;
  undefined4 extraout_ECX_19;
  undefined4 extraout_ECX_20;
  undefined4 extraout_ECX_21;
  undefined4 extraout_ECX_22;
  undefined4 extraout_ECX_23;
  undefined *puVar6;
  undefined *extraout_ECX_24;
  undefined *extraout_ECX_25;
  byte extraout_DL;
  byte extraout_DL_00;
  undefined1 extraout_DL_01;
  char extraout_DL_02;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 extraout_EDX_02;
  uint extraout_EDX_03;
  uint extraout_EDX_04;
  bool bVar7;
  undefined8 uVar8;
  ulonglong uVar9;

  iVar2 = (uint)in_AX * 0x114;
  indice_unidade = (ushort)param_2;
  bVar1 = unidade_obter_tipo(indice_unidade);
  uVar4 = extraout_ECX;
  if ((bVar1 == 10) && (((&DAT_0049a0d0)[iVar2] == '\x10' || ((&DAT_0049a0d0)[iVar2] == '\x02')))) {
    iVar3 = (uint)in_AX * 0x114;
    bVar1 = unidade_obter_proprietario(indice_unidade);
    uVar4 = extraout_ECX_00;
    if (extraout_DL != bVar1) {
      if ((((&DAT_0049a0d0)[iVar3] == '\x10') &&
          ((&DAT_004e2e7c)[(byte)(&DAT_0049a0cc)[iVar3]] == '\0')) &&
         ((bVar1 = unidade_obter_proprietario(indice_unidade), (&DAT_004e2e7c)[bVar1] == '\0' &&
          (uVar8 = FUN_004611e6(extraout_ECX_01,extraout_EDX), ((uint)uVar8 & 0xffff) != 0xffff))))
      {
        unidade_obter_proprietario(indice_unidade);
        uVar8 = FUN_004611e6(extraout_ECX_02,extraout_EDX_00);
        if (((uint)uVar8 & 0xffff) != 0xffff) {
          unidade_obter_proprietario(indice_unidade);
          FUN_00463317(extraout_ECX_03,extraout_DL_00);
          unidade_obter_proprietario(indice_unidade);
          uVar8 = FUN_0046d817(extraout_ECX_04,extraout_EDX_01);
          uVar4 = extraout_ECX_05;
          if (((uint)uVar8 & 0xff) != 2) {
            (&DAT_004e2e7c)[(byte)(&DAT_0049a0cc)[iVar3]] = 1;
            bVar1 = unidade_obter_proprietario(indice_unidade);
            (&DAT_004e2e7c)[bVar1] = extraout_DL_01;
            uVar4 = extraout_ECX_06;
          }
          if (DAT_00508041 == (&DAT_0049a0cc)[(uint)in_AX * 0x114]) {
            FUN_0041a1ac(uVar4,0);
          }
        }
      }
      goto LAB_0041fb0a;
    }
  }
  if ((&DAT_0049a0d0)[(uint)in_AX * 0x114] == '\x15') {
    uVar9 = FUN_0044724a(uVar4,0x15);
    bVar7 = (char)uVar9 == '\0';
    uVar4 = extraout_ECX_07;
LAB_0041f93b:
    if (!bVar7) goto LAB_0041f93d;
    bVar7 = false;
  }
  else {
    if (((&DAT_0049a0d0)[(uint)in_AX * 0x114] != '\x02') ||
       (uVar9 = FUN_0044724a(uVar4,2), uVar4 = extraout_ECX_08, (char)uVar9 == '\0')) {
      iVar3 = FUN_004471b8(uVar4,'\x01');
      bVar7 = (short)iVar3 == 0;
      uVar4 = extraout_ECX_09;
      goto LAB_0041f93b;
    }
LAB_0041f93d:
    bVar7 = true;
  }
  if (((!bVar7) ||
      (bVar1 = unidade_obter_proprietario(indice_unidade), uVar4 = extraout_ECX_10,
      bVar1 == (&DAT_0049a0cc)[iVar2])) &&
     (uVar4 = FUN_0041f552(uVar4,param_2 & 0xffff), (char)uVar4 != '\0')) {
    bVar1 = unidade_obter_tipo(indice_unidade);
    puVar6 = extraout_ECX_11;
    if (bVar1 != 9) {
      FUN_004474a6(extraout_ECX_11,extraout_EDX_02);
      uVar4 = extraout_ECX_12;
      while (iVar3 = FUN_004471b8(uVar4,'\x02'), uVar4 = extraout_ECX_13, (short)iVar3 != 0) {
        unidade_obter_proprietario(indice_unidade);
        FUN_0042340f(extraout_ECX_14,extraout_EDX_03);
        FUN_004472ea(extraout_ECX_15,'\x02');
        uVar4 = extraout_ECX_16;
      }
      while (iVar3 = FUN_004471b8(uVar4,'\x02'), puVar6 = extraout_ECX_17, (short)iVar3 != 0) {
        unidade_obter_proprietario(indice_unidade);
        FUN_0042340f(extraout_ECX_18,extraout_EDX_04);
        FUN_004472ea(extraout_ECX_19,'\x02');
        uVar4 = extraout_ECX_20;
      }
    }
    if ((&DAT_0049a0cc)[iVar2] == -0x38) {
      bVar1 = unidade_obter_proprietario(indice_unidade);
      (&DAT_0049a0cc)[iVar2] = bVar1;
      FUN_0041cc70(extraout_ECX_21);
      FUN_00419e97(extraout_ECX_22,extraout_DL_02);
      bVar1 = unidade_obter_proprietario(indice_unidade_00);
      FUN_0041be88(extraout_ECX_23,bVar1);
      puVar6 = &DAT_0049a0c8 + (uint)in_AX * 0x114;
      if (((&DAT_0049a0cc)[(uint)in_AX * 0x114] == DAT_00508041) &&
         (uVar5 = FUN_0041a0ab(), puVar6 = extraout_ECX_24, *(int *)(extraout_ECX_24 + 0x100) == -1)
         ) {
        FUN_0048aa79(0,(uint)(byte)extraout_ECX_24[8] << 0x10 | 0x2700,uVar5);
        puVar6 = extraout_ECX_25;
      }
    }
    FUN_00447483(puVar6,1);
  }
LAB_0041fb0a:
  FUN_0042399a();
  return;
}
