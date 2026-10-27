/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0047f36e, entrada 0047f36e.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_0047f36e(uint param_1,undefined4 param_2)

{
  byte bVar1;
  int iVar2;
  bool bVar3;
  undefined1 uVar4;
  int iVar5;
  undefined3 extraout_var;
  undefined3 extraout_var_00;
  uint extraout_ECX;
  int iVar6;
  undefined1 *puVar7;
  int extraout_ECX_00;
  undefined1 *puVar8;
  undefined1 *extraout_ECX_01;
  uint extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  uint extraout_ECX_05;
  uint extraout_ECX_06;
  undefined4 extraout_ECX_07;
  undefined4 extraout_ECX_08;
  undefined4 extraout_ECX_09;
  undefined *extraout_ECX_10;
  undefined4 extraout_ECX_11;
  uint uVar9;
  uint extraout_EDX;
  uint extraout_EDX_00;
  uint extraout_EDX_01;
  undefined4 extraout_EDX_02;
  ushort uVar10;
  int iVar11;
  uint uVar12;
  undefined1 *puVar13;
  int iVar14;
  longlong lVar15;
  undefined8 uVar16;
  ulonglong uVar17;
  uint local_24;

  uVar9 = 0;
  puVar13 = &DAT_0051a98c;
  local_24 = 0;
  do {
    uVar16 = FUN_0046d817(param_1,uVar9);
    uVar9 = (uint)((ulonglong)uVar16 >> 0x20);
    param_1 = extraout_ECX_06;
    if (((uint)uVar16 & 0xff) == 2) {
      if ((((*(int *)(puVar13 + 2) >> 0x18 == 0) && (*(int *)(puVar13 + 3) >> 0x18 == 0)) &&
          (*(int *)(puVar13 + 4) >> 0x18 == 0)) && (*(int *)(puVar13 + 5) >> 0x18 == 0)) {
        uVar12 = extraout_ECX_06;
        if (local_24 == 3) {
          iVar14 = 0;
        }
        else {
          iVar14 = 1;
          if (local_24 != 1) {
            lVar15 = FUN_00489728(extraout_ECX_06,uVar9);
            iVar14 = (int)lVar15;
            uVar12 = extraout_ECX;
          }
        }
        lVar15 = FUN_00489728(uVar12,100);
        iVar5 = (int)lVar15 + 0x1e;
        iVar11 = 0;
        iVar6 = 0;
        puVar7 = puVar13;
        do {
          if (iVar6 == iVar14) {
            iVar2 = iVar5;
          }
          else {
            iVar2 = ((int)((ulonglong)lVar15 >> 0x20) - iVar5) / 3;
          }
          iVar11 = iVar11 + iVar2;
          iVar6 = iVar6 + 1;
          puVar7[5] = (char)iVar11;
          puVar7 = puVar7 + 1;
        } while (iVar6 < 3);
        puVar13[8] = 100;
      }
      if (((*(int *)(puVar13 + 2) >> 0x18 != -1) || (*(int *)(puVar13 + 3) >> 0x18 != -1)) ||
         ((*(int *)(puVar13 + 4) >> 0x18 != -1 || (*(int *)(puVar13 + 5) >> 0x18 != -1)))) {
        iVar14 = 0;
        puVar7 = puVar13;
        do {
          bVar1 = (&DAT_00498464)[iVar14];
          uVar4 = FUN_004717c2(puVar7,(ushort)iVar14);
          if ((uint)bVar1 <= (CONCAT31(extraout_var,uVar4) & 0xffff)) {
            *(undefined1 *)(extraout_ECX_00 + 5) = 0xff;
          }
          iVar14 = iVar14 + 1;
          puVar7 = (undefined1 *)(extraout_ECX_00 + 1);
          uVar9 = extraout_EDX;
        } while (iVar14 < 4);
        do {
          lVar15 = FUN_00489728(puVar7,uVar9);
          puVar8 = (undefined1 *)lVar15;
          uVar9 = 0;
          for (puVar7 = puVar13; ((int)uVar9 < 4 && (*(int *)(puVar7 + 2) >> 0x18 <= (int)puVar8));
              puVar7 = puVar7 + 1) {
            uVar9 = uVar9 + 1;
          }
          if (*(int *)(puVar13 + uVar9 + 2) >> 0x18 == -1) {
            uVar9 = 0xffffffff;
            uVar12 = 0;
            puVar7 = puVar13;
            while (((int)uVar12 < 4 && (uVar9 == 0xffffffff))) {
              puVar8 = (undefined1 *)(*(int *)(puVar7 + 2) >> 0x18);
              if (puVar8 != (undefined1 *)0xffffffff) {
                uVar9 = uVar12;
              }
              puVar7 = puVar7 + 1;
              uVar12 = uVar12 + 1;
            }
          }
          if (uVar9 != 3) break;
          uVar4 = FUN_0046c11a();
          puVar7 = extraout_ECX_01;
          puVar8 = extraout_ECX_01;
          uVar9 = extraout_EDX_00;
        } while ((CONCAT31(extraout_var_00,uVar4) & 0xffff) < 7);
        FUN_00470b37(puVar8,(char)uVar9);
      }
      param_1 = local_24;
      for (uVar10 = 0; uVar9 = (uint)uVar10, uVar10 < 800; uVar10 = uVar10 + 1) {
        lVar15 = FUN_00443dad(param_1,uVar9);
        iVar14 = (int)((ulonglong)lVar15 >> 0x20);
        param_1 = extraout_ECX_02;
        if (((char)lVar15 != '\0') &&
           (uVar9 = iVar14 * 0x114, tabela_unidades[iVar14].proprietario_id == extraout_ECX_02)) {
          bVar3 = true;
          goto LAB_0047f50d;
        }
      }
      bVar3 = false;
LAB_0047f50d:
      if (bVar3) {
        puVar13[4] = 0;
        *puVar13 = 0;
        FUN_004846a7(param_1,'\0');
        FUN_0048569a(extraout_ECX_03,'\0');
        FUN_00486ca7(extraout_ECX_04,'\0');
        puVar13[1] = 0;
        puVar13[2] = 1;
        puVar13[3] = 0;
        puVar13[9] = 0;
        param_1 = extraout_ECX_05;
        uVar9 = extraout_EDX_01;
      }
      else {
        puVar13[4] = 1;
      }
    }
    local_24 = local_24 + 1;
    puVar13 = puVar13 + 0x10;
    if (3 < (int)local_24) {
      lVar15 = FUN_0047d220(param_1,uVar9);
      iVar14 = (int)lVar15;
      if (iVar14 == 0) {
        lVar15 = FUN_0048270b(extraout_ECX_07,(uint)((ulonglong)lVar15 >> 0x20));
        iVar14 = (int)lVar15;
        if (iVar14 == 0) {
          lVar15 = FUN_00484310(extraout_ECX_08,(uint)((ulonglong)lVar15 >> 0x20));
          iVar14 = (int)lVar15;
          if (iVar14 == 0) {
            FUN_0048134c();
            uVar16 = FUN_00485002(extraout_ECX_09,extraout_EDX_02);
            iVar14 = (int)uVar16;
            if (iVar14 == 0) {
              uVar17 = FUN_004864c1(extraout_ECX_10,(int)((ulonglong)uVar16 >> 0x20));
              iVar14 = (int)uVar17;
              if (iVar14 == 0) {
                FUN_0047af90(extraout_ECX_11);
                iVar14 = 0;
              }
            }
          }
        }
      }
      return CONCAT44(param_2,iVar14);
    }
  } while( true );
}
