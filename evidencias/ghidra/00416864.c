/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00416864, entrada 00416864.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00416864(undefined4 param_1,uint param_2)

{
  int iVar1;
  bool bVar2;
  ushort uVar3;
  ushort uVar4;
  uint in_EAX;
  undefined4 uVar5;
  uint uVar6;
  int iVar7;
  int extraout_ECX;
  int extraout_ECX_00;
  int extraout_ECX_01;
  int extraout_ECX_02;
  int extraout_ECX_03;
  int extraout_ECX_04;
  int extraout_ECX_05;
  int extraout_ECX_06;
  int extraout_ECX_07;
  int extraout_ECX_08;
  int extraout_EDX;
  uint uVar8;
  ushort uVar9;
  ushort uVar10;
  short sVar11;
  uint uVar12;
  undefined8 uVar13;
  short local_75c;
  ushort auStack_754 [900];
  int local_4c;
  int local_48;
  UnidadeParcial *local_44;
  uint uStack_40;
  undefined4 local_3c;
  short sStack_38;
  short sStack_34;
  undefined2 local_30;
  undefined2 local_2e;
  ushort uStack_2c;
  uint local_28;
  short sStack_24;
  short sStack_20;
  uint uStack_1c;
  int iStack_18;

  uVar9 = 0;
  iVar7 = 0;
  while( true ) {
    if (799 < (short)(ushort)iVar7) break;
    bVar2 = unidade_esta_ativa((ushort)iVar7);
    iVar7 = extraout_ECX;
    if (bVar2) {
      uVar3 = tabela_unidades[extraout_EDX].celula_atual;
      uVar5 = FUN_004766f0(extraout_ECX,(uint)DAT_00508041);
      iVar7 = extraout_ECX_00;
      if (((char)uVar5 != '\0') &&
         (uVar5 = FUN_0047693a(extraout_ECX_00,(uint)DAT_00508041), iVar7 = extraout_ECX_01,
         (char)uVar5 != '\0')) {
        uVar10 = uVar3 % 0x100;
        uVar3 = uVar3 / 0x100;
        if (((short)in_EAX <= (short)uVar10) &&
           (((local_75c = (short)param_2, local_75c <= (short)uVar3 &&
             ((uint)(int)(short)uVar10 < (in_EAX & 0xffff) + (uint)DAT_00508724 + 2)) &&
            ((uint)(int)(short)uVar3 < (uint)DAT_00508726 + (param_2 & 0xffff) + 10)))) {
          uVar8 = (uint)uVar9;
          uVar9 = uVar9 + 1;
          auStack_754[uVar8] = (ushort)extraout_ECX_01;
        }
      }
    }
    iVar7 = iVar7 + 1;
  }
  for (uStack_2c = 0; (int)(short)uStack_2c < (int)(uint)uVar9; uStack_2c = uStack_2c + 1) {
    uVar3 = tabela_unidades[auStack_754[(short)uStack_2c]].celula_atual;
    uVar10 = uStack_2c;
    uVar4 = uStack_2c;
    while (uVar4 = uVar4 + 1, uVar4 < uVar9) {
      if ((tabela_unidades[auStack_754[uVar4]].celula_atual < uVar3) ||
         ((tabela_unidades[auStack_754[uVar4]].celula_atual < uVar3 &&
          (tabela_unidades[auStack_754[uVar4]].estado == 4)))) {
        uVar3 = tabela_unidades[auStack_754[uVar4]].celula_atual;
        uVar10 = uVar4;
      }
      else {
        local_44 = tabela_unidades;
        if ((uVar3 == tabela_unidades[auStack_754[uVar4]].celula_atual) &&
           ((byte)tabela_unidades[auStack_754[uVar4]].field_0xab <
            (byte)tabela_unidades[auStack_754[uVar10]].field_0xab)) {
          uVar10 = uVar4;
        }
      }
    }
    uVar3 = auStack_754[(short)uStack_2c];
    auStack_754[(short)uStack_2c] = auStack_754[uVar10];
    auStack_754[uVar10] = uVar3;
  }
  local_28 = FUN_0046fc8b();
  uVar8 = CONCAT22(local_3c._2_2_,(undefined2)local_3c);
  iVar7 = 0;
  sStack_20 = 0;
  uVar12 = param_2 * 0x100 + in_EAX;
  uVar6 = param_2;
  while( true ) {
    local_30 = (undefined2)uVar6;
    local_2e = (undefined2)(uVar6 >> 0x10);
    if ((uint)DAT_00508726 + (param_2 & 0xffff) + 5 <= (uVar6 & 0xffff)) break;
    sStack_34 = 0;
    local_3c._2_2_ = (undefined2)(in_EAX >> 0x10);
    uVar8 = in_EAX;
    while ((uVar8 & 0xffff) < (uint)DAT_00508724 + (in_EAX & 0xffff) + 8) {
      local_3c = uVar8;
      if (*(char *)((uVar12 & 0xffff) + DAT_00507d74) != '\0') {
        uVar5 = FUN_004766f0(iVar7,(uint)DAT_00508041);
        iVar7 = extraout_ECX_02;
        if ((char)uVar5 != '\0') {
          FUN_00415acf(extraout_ECX_02);
          iVar7 = extraout_ECX_03;
        }
      }
      local_4c = (int)sStack_20;
      local_48 = (int)sStack_34;
      FUN_00407dd3(iVar7,local_4c);
      FUN_0040f49b();
      iVar7 = extraout_ECX_04;
      while (((int)(short)iVar7 < (int)(uint)uVar9 &&
             (tabela_unidades[auStack_754[(short)iVar7]].field_0xab != '\0'))) {
        iVar7 = iVar7 + 1;
      }
      while ((((int)(short)iVar7 < (int)(uint)uVar9 &&
              ((ushort)uVar12 == tabela_unidades[auStack_754[(short)iVar7]].celula_atual)) &&
             (tabela_unidades[auStack_754[(short)iVar7]].field_0xab == '\0'))) {
        FUN_0041591f(iVar7 + 1,(int)sStack_20);
        iVar7 = extraout_ECX_05;
      }
      uVar12 = uVar12 + 1;
      uVar8 = local_3c + 1;
      sStack_34 = sStack_34 + 0x20;
      local_3c._0_2_ = (undefined2)uVar8;
      local_3c._2_2_ = (undefined2)(uVar8 >> 0x10);
    }
    sStack_20 = sStack_20 + 0x20;
    uVar6 = CONCAT22(local_2e,local_30) + 1;
    uVar12 = uVar12 + (0x100 - (DAT_00508724 + 8));
  }
  iVar7 = 0;
  sVar11 = 0;
  sStack_38 = 0;
  iStack_18 = in_EAX + param_2 * 0x100;
  uStack_40 = param_2;
  do {
    if ((param_2 & 0xffff) + (uint)DAT_00508726 + 10 <= (uStack_40 & 0xffff)) {
      return;
    }
    sStack_24 = 0;
    for (uStack_1c = in_EAX; iVar1 = iStack_18, uVar6 = (in_EAX & 0xffff) + (uint)DAT_00508724 + 8,
        (uStack_1c & 0xffff) < uVar6; uStack_1c = uStack_1c + 1) {
      for (; local_3c = uVar8, (int)sVar11 < (int)(local_28 & 0xffff); sVar11 = sVar11 + 1) {
        uVar13 = FUN_0046fe9a(iVar7,sVar11 * 2);
        iVar7 = extraout_ECX_06;
        if ((short)uVar13 != (short)iVar1) break;
        FUN_0046ff70();
        iVar7 = extraout_ECX_07;
        uVar8 = local_3c;
      }
      while ((uVar8 = local_3c, (int)(short)iVar7 < (int)(uint)uVar9 &&
             (tabela_unidades[auStack_754[(short)iVar7]].field_0xab == '\0'))) {
        iVar7 = iVar7 + 1;
      }
      while ((int)(short)iVar7 < (int)(uint)uVar9) {
        if ((tabela_unidades[auStack_754[(short)iVar7]].celula_atual != (ushort)iStack_18) ||
           (tabela_unidades[auStack_754[(short)iVar7]].field_0xab == '\0')) break;
        local_3c = uVar8;
        FUN_0041591f(iVar7 + 1,(int)sStack_38);
        iVar7 = extraout_ECX_08;
        uVar8 = local_3c;
      }
      sStack_24 = sStack_24 + 0x20;
      iStack_18 = iStack_18 + 1;
    }
    sStack_38 = sStack_38 + 0x20;
    uStack_40 = uStack_40 + 1;
    iStack_18 = iStack_18 + (0x100 - (CONCAT22((short)(uVar6 >> 0x10),DAT_00508724) + 8));
  } while( true );
}
