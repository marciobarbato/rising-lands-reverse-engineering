/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0041f552, entrada 0041f552.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined4 __fastcall FUN_0041f552(undefined4 param_1,uint param_2)

{
  byte bVar1;
  char cVar2;
  ushort in_AX;
  ushort uVar3;
  undefined2 uVar4;
  ushort uVar5;
  int iVar6;
  undefined2 extraout_var;
  uint uVar7;
  undefined2 extraout_var_00;
  undefined4 extraout_ECX;
  int extraout_ECX_00;
  int extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 uVar8;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  undefined4 extraout_ECX_06;
  undefined4 extraout_ECX_07;
  undefined1 uVar9;
  ushort indice_unidade;
  ushort indice_unidade_00;
  undefined4 extraout_EDX;
  int3 iVar10;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 extraout_EDX_02;
  ushort uVar11;
  uint uVar12;
  undefined8 uVar13;
  ushort local_24;
  uint local_14;

  if ((&DAT_0049a0d0)[(uint)in_AX * 0x114] == '\b') {
    uVar3 = FUN_00447107();
    iVar10 = (int3)((uint)extraout_EDX >> 8);
    iVar6 = (CONCAT31(iVar10,DAT_00495be9) - ((int)iVar10 >> 0x17) >> 1) + 1;
    uVar7 = CONCAT31((int3)((uint)iVar6 >> 8),(int)(uint)uVar3 < iVar6);
    if ((int)(uint)uVar3 >= iVar6) goto LAB_0041f765;
LAB_0041f745:
    uVar9 = 1;
  }
  else {
    if ((&DAT_0049a0d0)[(uint)in_AX * 0x114] == '\x13') {
      local_24 = (ushort)param_2;
      uVar3 = unidade_obter_vida(local_24);
      uVar13 = FUN_00441108(extraout_ECX,extraout_EDX_00);
      iVar6 = extraout_ECX_00;
      if (uVar3 == (ushort)uVar13) {
        bVar1 = unidade_obter_tipo((ushort)((ulonglong)uVar13 >> 0x20));
        uVar7 = (uint)bVar1;
        iVar6 = extraout_ECX_01;
        if (uVar7 != 9) goto LAB_0041f765;
      }
      uVar4 = FUN_004470d2(iVar6 + 0xc,1);
      uVar7 = CONCAT22(extraout_var,uVar4);
      if ((char)uVar4 != '\0') {
        uVar3 = FUN_00447107();
        local_14 = 0;
        uVar8 = extraout_ECX_02;
        uVar12 = 0;
        for (uVar11 = 0; uVar11 < uVar3; uVar11 = uVar11 + 1) {
          cVar2 = FUN_004472d3(uVar8,(uint)uVar11);
          uVar8 = extraout_ECX_03;
          uVar7 = uVar12;
          if (cVar2 == '\x01') {
            uVar5 = FUN_004472de(extraout_ECX_03,(uint)uVar11);
            bVar1 = unidade_obter_tipo(uVar5);
            uVar7 = uVar12 + 1;
            if (bVar1 == 9) {
              uVar5 = unidade_obter_vida(indice_unidade);
              uVar13 = FUN_00441108(extraout_ECX_05,extraout_EDX_01);
              uVar8 = extraout_ECX_06;
              if (uVar5 == (ushort)uVar13) {
                local_14 = local_14 + 1;
                uVar7 = uVar12;
              }
            }
            else {
              uVar8 = extraout_ECX_04;
            }
          }
          uVar12 = uVar7;
        }
        bVar1 = unidade_obter_tipo(local_24);
        if (bVar1 == 9) {
          uVar3 = unidade_obter_vida(indice_unidade_00);
          uVar13 = FUN_00441108(extraout_ECX_07,extraout_EDX_02);
          if (uVar3 != (ushort)uVar13) goto LAB_0041f749;
          bVar1 = (&DAT_0049a0d0)[(uint)in_AX * 0x114];
          if (bVar1 < 0xe) {
LAB_0041f71d:
            uVar7 = (uint)(byte)(&DAT_00495d9e)
                                [(uint)(byte)(&DAT_0049a0d0)[(uint)in_AX * 0x114] * 0x34];
          }
          else if (bVar1 < 0xf) {
            uVar7 = (uint)(byte)((&DAT_00495d9e)[(uint)bVar1 * 0x34] - 1);
          }
          else {
            if (bVar1 != 0x13) goto LAB_0041f71d;
            uVar7 = (uint)(byte)(cRam0049617a - DAT_00495be8);
          }
        }
        else {
LAB_0041f749:
          uVar7 = (uint)DAT_00495be8;
          local_14 = uVar12;
        }
        if ((local_14 & 0xffff) < uVar7) goto LAB_0041f745;
      }
    }
    else {
      uVar4 = FUN_004470d2(&DAT_0049a0c8 + (uint)in_AX * 0x114,1);
      uVar7 = CONCAT22(extraout_var_00,uVar4);
      if ((char)uVar4 != '\0') goto LAB_0041f745;
    }
LAB_0041f765:
    uVar9 = 0;
  }
  return CONCAT31((int3)(uVar7 >> 8),uVar9);
}
