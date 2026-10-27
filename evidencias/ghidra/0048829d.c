/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0048829d, entrada 0048829d.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined2 __fastcall FUN_0048829d(undefined4 param_1,int param_2)

{
  ushort uVar1;
  int iVar2;
  byte bVar3;
  char cVar4;
  int in_EAX;
  int iVar5;
  undefined4 uVar6;
  uint uVar7;
  uint uVar8;
  ushort indice_unidade;
  undefined2 uVar9;
  uint uVar10;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  uint extraout_ECX_01;
  uint extraout_ECX_02;
  uint extraout_ECX_03;
  uint extraout_ECX_04;
  uint extraout_ECX_05;
  ushort *puVar11;
  ushort *puVar12;
  ushort *extraout_ECX_06;
  ushort *extraout_ECX_07;
  undefined2 *extraout_ECX_08;
  ushort *extraout_ECX_09;
  undefined2 *extraout_ECX_10;
  undefined2 *puVar13;
  byte bVar14;
  int iVar15;
  int iVar16;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  uint uVar17;
  uint uVar18;
  short *psVar19;
  uint uVar20;
  uint uVar21;
  ulonglong uVar22;
  ulonglong uVar23;
  undefined8 uVar24;
  int local_34;
  int local_28;
  uint local_18;

  bVar14 = tabela_unidades[in_EAX].proprietario_id;
  uVar8 = (uint)bVar14;
  if (in_EAX == 0xffff) {
LAB_004882d1:
    uVar9 = 0xffff;
  }
  else {
    iVar2 = param_2 * 0x110 + uVar8 * 0x1144;
    if (*(short *)((int)&DAT_0051bd24 + iVar2 + 0xe) == 0) {
      iVar15 = (int)(&DAT_0051bd24)[uVar8 * 0x451 + param_2 * 0x44 + 1] % 0x100;
      iVar5 = (&DAT_0051bd24)[uVar8 * 0x451 + param_2 * 0x44 + 1];
      iVar16 = iVar5 >> 0x1f;
      iVar5 = (int)((iVar5 + iVar16 * -0x100) - (uint)(iVar16 << 7 < 0)) >> 8;
      uVar20 = iVar15 - (uint)*(ushort *)(&DAT_0051bd24 + uVar8 * 0x451 + param_2 * 0x44 + 3);
      if ((int)uVar20 < 0) {
        uVar20 = 0;
      }
      local_34 = iVar5 - (uint)*(ushort *)(&DAT_0051bd24 + uVar8 * 0x451 + param_2 * 0x44 + 3);
      if (local_34 < 0) {
        local_34 = 0;
      }
      uVar10 = iVar15 + (uint)*(ushort *)(&DAT_0051bd24 + uVar8 * 0x451 + param_2 * 0x44 + 3);
      if (0xff < (int)uVar10) {
        uVar10 = 0xff;
      }
      iVar5 = (uint)*(ushort *)(&DAT_0051bd24 + uVar8 * 0x451 + param_2 * 0x44 + 3) + iVar5;
      if (0xff < iVar5) {
        iVar5 = 0xff;
      }
      iVar15 = 0;
      local_18 = 0xffff;
      local_34 = local_34 << 8;
      uVar7 = uVar10;
      uVar17 = iVar5 << 8;
      while( true ) {
        uVar22 = CONCAT44(uVar17,local_34);
        if (iVar5 << 8 < local_34) break;
        uVar18 = local_34 + uVar20;
        uVar7 = uVar20;
        for (uVar21 = uVar20; uVar17 = (uint)(uVar22 >> 0x20), (int)uVar21 <= (int)uVar10;
            uVar21 = uVar21 + 1) {
          puVar11 = (ushort *)(DAT_004e0f38 + (uVar18 & 0xffff) * 2);
          if ((*puVar11 >> 8 & 0xc0) == 0x40) {
            iVar16 = (int)(*puVar11 & 0x3ff8) >> 3;
          }
          else {
            iVar16 = 0xffff;
          }
          uVar22 = CONCAT44(uVar17,iVar16);
          if (iVar16 != 0xffff) {
            uVar22 = FUN_00443dad(iVar16,uVar17);
            if ((char)uVar22 != '\0') {
              uVar23 = FUN_0044113e(extraout_ECX,(int)(uVar22 >> 0x20));
              uVar22 = uVar23 & 0xffffffff0000ffff;
              if (((uint)uVar23 & 0xffff) == uVar18) {
                uVar6 = FUN_00446fbf(extraout_ECX_00,bVar14);
                uVar22 = CONCAT44(extraout_EDX,uVar6);
                if ((char)uVar6 != '\0') {
                  bVar3 = unidade_obter_tipo(indice_unidade);
                  iVar16 = *(int *)(&DAT_00498cf4 + (uint)bVar3 * 4);
                  uVar22 = CONCAT44(extraout_EDX_00,iVar16);
                  if (iVar15 < iVar16) {
                    uVar22 = CONCAT44(extraout_ECX_01,iVar16);
                    iVar15 = iVar16;
                    local_18 = extraout_ECX_01;
                  }
                }
              }
            }
          }
          uVar6 = (undefined4)(uVar22 >> 0x20);
          puVar11 = (ushort *)(DAT_004e0f38 + (uVar18 & 0xffff) * 2);
          if ((*puVar11 & 0x8000) == 0) {
            uVar7 = 0xffff;
          }
          else {
            uVar7 = (int)(*puVar11 & 0x7fe0) >> 5;
          }
          uVar22 = CONCAT44(uVar6,uVar7);
          if (uVar7 != 0xffff) {
            uVar22 = FUN_0041a735(uVar7,uVar6);
            uVar7 = extraout_ECX_02;
            if ((char)uVar22 != '\0') {
              uVar22 = FUN_0041a70b(extraout_ECX_02,(int)(uVar22 >> 0x20));
              uVar7 = extraout_ECX_03;
              if ((char)uVar22 == '\0') {
                uVar6 = FUN_0041a61c(extraout_ECX_03,bVar14);
                uVar22 = CONCAT44(extraout_EDX_01,uVar6);
                uVar7 = extraout_ECX_04;
                if ((char)uVar6 != '\0') {
                  uVar24 = FUN_0041a4f4(extraout_ECX_04,extraout_EDX_01);
                  iVar16 = *(int *)(&DAT_00498d5c + ((uint)uVar24 & 0xff) * 4);
                  uVar22 = CONCAT44((int)((ulonglong)uVar24 >> 0x20),iVar16);
                  uVar7 = extraout_ECX_05;
                  if (iVar15 < iVar16) {
                    local_18 = extraout_ECX_05 | 0x8000;
                    uVar22 = CONCAT44(extraout_ECX_05,iVar16) | 0x800000000000;
                    iVar15 = iVar16;
                  }
                }
              }
            }
          }
          uVar18 = uVar18 + 1;
        }
        local_34 = local_34 + 0x100;
      }
      if ((short)local_18 == -1) goto LAB_004882d1;
      FUN_00487b78(uVar7,param_2);
    }
    puVar11 = (ushort *)(&DAT_0051bd24 + uVar8 * 0x451 + param_2 * 0x44 + 4);
    for (local_28 = 1; -1 < local_28; local_28 = local_28 + -1) {
      puVar12 = puVar11;
      for (iVar5 = 0; iVar5 < (int)(uint)*(ushort *)((int)&DAT_0051bd24 + iVar2 + 0xe);
          iVar5 = iVar5 + 1) {
        uVar1 = *puVar12;
        if ((uVar1 & 0x8000) == 0) {
          uVar8 = (uint)tabela_unidades[uVar1].vida;
        }
        else {
          uVar8 = (uint)*(ushort *)(&DAT_0049a0d2 + (uint)(uVar1 & 0x7fff) * 0x114) -
                  (uint)(ushort)(&DAT_0049a0ce)[(uint)(uVar1 & 0x7fff) * 0x8a];
        }
        if ((int)(uint)puVar12[1] < (int)uVar8) {
          if (local_28 != 0) {
            if ((*puVar12 & 0x8000) == 0) {
              cVar4 = '\x01';
            }
            else {
              cVar4 = '\x03';
            }
            cVar4 = FUN_00446cb5(puVar12,cVar4);
            puVar12 = extraout_ECX_06;
            if (cVar4 == '\0') goto LAB_00488554;
          }
          if ((*puVar12 & 0x8000) == 0) {
            bVar14 = tabela_unidades[*puVar12].tipo_id;
          }
          else {
            bVar14 = 0x1a;
          }
          uVar8 = FUN_0044f98a(puVar12,bVar14);
          puVar12 = extraout_ECX_07;
          if ((uVar8 & 0xff) != 0) {
            extraout_ECX_07[1] = extraout_ECX_07[1] + (short)(uVar8 & 0xff);
            if ((*extraout_ECX_07 & 0x8000) == 0) {
              cVar4 = '\x01';
            }
            else {
              cVar4 = '\x03';
            }
            FUN_00445a36(extraout_ECX_07,cVar4);
            puVar13 = extraout_ECX_08;
            goto LAB_00488732;
          }
        }
LAB_00488554:
        puVar12 = puVar12 + 4;
      }
    }
    psVar19 = (short *)((int)&DAT_0051bd24 + iVar2 + 0x12);
    if ((*puVar11 & 0x8000) == 0) {
      bVar14 = tabela_unidades[*puVar11].tipo_id;
    }
    else {
      bVar14 = 0x1a;
    }
    uVar6 = FUN_0044f98a(puVar11,bVar14);
    *psVar19 = *psVar19 + ((ushort)uVar6 & 0xff);
    if ((*extraout_ECX_09 & 0x8000) == 0) {
      cVar4 = '\x01';
    }
    else {
      cVar4 = '\x03';
    }
    FUN_00445a36(extraout_ECX_09,cVar4);
    puVar13 = extraout_ECX_10;
LAB_00488732:
    uVar9 = *puVar13;
  }
  return uVar9;
}
