/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0047af90, entrada 0047af90.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN_0047af90(undefined4 param_1)

{
  byte bVar1;
  ushort indice_unidade;
  char cVar2;
  undefined1 uVar3;
  int iVar4;
  undefined3 extraout_var;
  uint uVar5;
  int extraout_ECX;
  int extraout_ECX_00;
  undefined4 extraout_ECX_01;
  int extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  undefined4 extraout_ECX_06;
  undefined4 uVar6;
  undefined4 extraout_ECX_07;
  undefined4 extraout_ECX_08;
  undefined4 extraout_ECX_09;
  undefined4 extraout_ECX_10;
  uint extraout_EDX;
  uint extraout_EDX_00;
  uint extraout_EDX_01;
  int extraout_EDX_02;
  int extraout_EDX_03;
  int extraout_EDX_04;
  int extraout_EDX_05;
  int iVar7;
  int iVar8;
  int iVar9;
  longlong lVar10;
  undefined8 uVar11;
  byte abStack_48 [16];
  byte abStack_38 [16];
  int local_28;
  uint local_24;
  int local_20;
  char local_1c;

  DAT_0050a9cc = 0;
  DAT_0050ae80 = 0;
  DAT_0050b134 = 0;
  DAT_0050b178 = 0;
  iVar4 = FUN_00483bd8(param_1,0x10);
  if (iVar4 != -1) {
    local_28 = 0;
    uVar5 = extraout_EDX;
    do {
      indice_unidade = (ushort)local_28;
      lVar10 = FUN_00443dad(iVar4,uVar5);
      uVar5 = (uint)((ulonglong)lVar10 >> 0x20);
      iVar4 = extraout_ECX;
      if ((char)lVar10 != '\0') {
        unidade_obter_tipo(indice_unidade);
        cVar2 = FUN_004422dd();
        iVar4 = extraout_ECX_00;
        uVar5 = extraout_EDX_00;
        if (cVar2 != '\0') {
          FUN_00482939(extraout_ECX_00,indice_unidade);
          FUN_00443108(extraout_ECX_01,4);
          DAT_0050b178 = DAT_0050b178 + 1;
          iVar4 = extraout_ECX_02;
          uVar5 = extraout_EDX_01;
        }
      }
      local_28 = local_28 + 1;
    } while (local_28 < 800);
    uVar3 = FUN_0046c11a();
    if ((CONCAT31(extraout_var,uVar3) & 0xffff) == 0x17) {
      uVar5 = (uint)DAT_0050b134;
      DAT_0050b134 = DAT_0050b134 + 1;
      *(undefined4 *)(&DAT_0050b138 + uVar5 * 4) = extraout_ECX_03;
    }
    else {
      local_20 = 0;
      local_28 = 0;
      do {
        if ((&DAT_0050b124)[local_28] != '\0') {
          abStack_38[local_20] = (byte)local_28;
          abStack_48[local_20] = (&DAT_0050b124)[local_28];
          local_20 = local_20 + 1;
        }
        local_28 = local_28 + 1;
      } while (local_28 < 0x10);
      iVar4 = local_20 + -1;
      for (local_28 = 0; iVar7 = local_28, local_28 < iVar4; local_28 = local_28 + 1) {
        while (iVar9 = iVar7, iVar8 = local_28, iVar7 = iVar9 + 1, iVar7 < local_20) {
          if (abStack_48[local_28] < abStack_48[iVar9 + 1]) {
            bVar1 = abStack_48[local_28];
            abStack_48[local_28] = abStack_48[iVar9 + 1];
            abStack_48[iVar9 + 1] = bVar1;
            bVar1 = abStack_38[iVar8];
            abStack_38[iVar8] = abStack_38[iVar9 + 1];
            abStack_38[iVar9 + 1] = bVar1;
          }
        }
      }
      local_28 = 0;
      uVar6 = extraout_ECX_03;
      while (((local_28 < local_20 && (DAT_0050b178 < 0x32)) && (DAT_0050b134 < 0x10))) {
        local_1c = '\x01';
        while (((local_1c != '\0' && (DAT_0050b178 < 0x32)) &&
               ((DAT_0050b134 < 0x10 &&
                (iVar4 = FUN_00483bd8(uVar6,0x10), uVar6 = extraout_ECX_04, iVar7 = extraout_EDX_02,
                iVar4 != -1))))) {
          iVar9 = 0;
          while ((iVar9 < 0x1a && (DAT_0050b178 < 0x32))) {
            local_24 = (uint)(byte)(&DAT_0050af84)[(uint)abStack_38[local_28] * 0x1a + iVar9];
            for (iVar8 = 0; iVar8 < (int)local_24; iVar8 = iVar8 + 1) {
              uVar5 = FUN_00483747(uVar6,uVar6);
              if ((uVar5 & 0xffff) == 0xffff) {
                local_1c = '\0';
                uVar6 = extraout_ECX_07;
                iVar7 = extraout_EDX_04;
                break;
              }
              FUN_004832b1(extraout_ECX_07,(ushort)uVar5);
              FUN_00482939(extraout_ECX_05,(ushort)uVar5);
              uVar6 = extraout_ECX_06;
              iVar7 = extraout_EDX_03;
            }
            iVar9 = iVar9 + 1;
          }
          uVar11 = FUN_004837f0(uVar6,iVar7);
          iVar7 = (int)((ulonglong)uVar11 >> 0x20);
          if (((uint)uVar11 & 0xffff) == 0xffff) {
            FUN_00483ce7(extraout_ECX_08,iVar4);
            uVar6 = extraout_ECX_09;
            iVar7 = extraout_EDX_05;
          }
          else {
            uVar6 = extraout_ECX_08;
            if (0xf < DAT_0050b134) break;
            uVar5 = (uint)DAT_0050b134;
            DAT_0050b134 = DAT_0050b134 + 1;
            *(int *)(&DAT_0050b138 + uVar5 * 4) = iVar4;
          }
        }
        local_28 = local_28 + 1;
      }
      uVar11 = FUN_004837f0(uVar6,iVar7);
      if (((uint)uVar11 & 0xffff) == 0xffff) {
        FUN_00483ce7(extraout_ECX_10,extraout_ECX_10);
      }
      else if (DAT_0050b134 < 0x10) {
        uVar5 = (uint)DAT_0050b134;
        DAT_0050b134 = DAT_0050b134 + 1;
        *(undefined4 *)(&DAT_0050b138 + uVar5 * 4) = extraout_ECX_10;
      }
      _DAT_0050b180 = 0xffff;
      _DAT_0050b17c = 3;
    }
  }
  return;
}
