/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0047b283, entrada 0047b283.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0047b283(void)

{
  int iVar1;
  undefined1 uVar2;
  sbyte sVar3;
  byte bVar4;
  char cVar10;
  short sVar5;
  ushort uVar6;
  undefined3 extraout_var;
  int iVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  ushort extraout_CX;
  uint extraout_ECX;
  uint uVar11;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  uint uVar12;
  undefined4 extraout_ECX_02;
  uint extraout_ECX_03;
  uint extraout_ECX_04;
  uint extraout_ECX_05;
  undefined4 extraout_ECX_06;
  undefined4 extraout_ECX_07;
  uint extraout_ECX_08;
  int extraout_ECX_09;
  int extraout_ECX_10;
  int extraout_ECX_11;
  int extraout_ECX_12;
  int extraout_ECX_13;
  int extraout_ECX_14;
  int extraout_ECX_15;
  int extraout_ECX_16;
  int extraout_ECX_17;
  int iVar13;
  uint extraout_EDX;
  uint uVar14;
  uint extraout_EDX_00;
  uint extraout_EDX_01;
  undefined4 extraout_EDX_02;
  undefined4 extraout_EDX_03;
  undefined4 extraout_EDX_04;
  undefined4 extraout_EDX_05;
  uint extraout_EDX_06;
  uint extraout_EDX_07;
  uint extraout_EDX_08;
  uint extraout_EDX_09;
  uint extraout_EDX_10;
  uint extraout_EDX_11;
  uint extraout_EDX_12;
  undefined2 *puVar15;
  longlong lVar16;
  undefined8 uVar17;
  undefined8 uVar18;
  ulonglong uVar19;
  int local_30;
  int local_28;
  int local_24;
  int local_20;

  if (DAT_0050a9cc == '\0') {
    DAT_0050a9cc = '\x01';
    iVar7 = 0;
    for (iVar13 = 0; iVar13 < (int)(uint)DAT_0050a9ce; iVar13 = iVar13 + 1) {
      *(int *)((int)&DAT_0050a9d8 + iVar7) = DAT_00508f7c;
      iVar7 = iVar7 + 0xc;
    }
  }
  uVar2 = FUN_0046c11a();
  iVar7 = DAT_00508f7c;
  if ((CONCAT31(extraout_var,uVar2) & 0xffff) == 0x17) {
    if (DAT_0050b134 == 0) {
      return;
    }
    iVar7 = FUN_0047d920(0,0x12,0,0,0,0);
    if (iVar7 == -1) {
      return;
    }
    goto LAB_0047b30e;
  }
  puVar15 = &DAT_0050a9d0;
  uVar11 = (uint)DAT_0050a9ce;
  uVar12 = extraout_ECX;
  uVar14 = extraout_EDX;
  while (uVar11 != 0) {
    if (((ushort)puVar15[2] != 0) &&
       (uVar14 = iVar7 - *(int *)(puVar15 + 4), (int)(uint)(ushort)puVar15[2] <= (int)uVar14)) {
      sVar3 = *(sbyte *)(puVar15 + 3);
      cVar10 = '\x10';
      do {
        uVar14 = CONCAT11(cVar10,sVar3 + 1) & 0xffffff0f;
        sVar3 = (sbyte)uVar14;
        uVar12 = CONCAT31((int3)(uVar12 >> 8),sVar3);
        if ((1 << sVar3 & 0xffffU & (uint)(ushort)puVar15[1]) != 0) goto LAB_0047b373;
        cVar10 = (char)(uVar14 >> 8) + -1;
      } while (cVar10 != '\0');
      uVar14 = 0xff;
LAB_0047b373:
      *(char *)(puVar15 + 3) = (char)uVar14;
      *(int *)(puVar15 + 4) = iVar7;
      FUN_0047a81d(uVar12,*(byte *)(puVar15 + 3));
      uVar14 = extraout_EDX_00;
    }
    puVar15 = puVar15 + 6;
    uVar11 = uVar11 - 1;
    uVar12 = uVar11;
  }
  lVar16 = (ulonglong)uVar14 << 0x20;
  for (iVar7 = 0; uVar9 = (undefined4)((ulonglong)lVar16 >> 0x20), iVar7 < DAT_0050ae80;
      iVar7 = iVar7 + 1) {
    iVar13 = iVar7 * 0x10;
    uVar11 = (uint)*(ushort *)((int)&DAT_0050ae90 + iVar13 + 2);
    lVar16 = CONCAT44(iVar13,uVar11);
    if ((uVar11 == 0x31) &&
       (iVar1 = (&DAT_0050ae8c)[iVar7 * 4], (&DAT_0050ae8c)[iVar7 * 4] = iVar1 + -1,
       lVar16 = CONCAT44(iVar13,uVar11), iVar1 + -1 < 1)) {
      (&DAT_0050ae8c)[iVar7 * 4] = 0x1c2;
      lVar16 = FUN_004837f0(uVar12,iVar13);
      iVar13 = (int)((ulonglong)lVar16 >> 0x20);
      sVar5 = (short)lVar16;
      if (sVar5 == -1) {
        iVar1 = *(int *)((int)&DAT_0050ae88 + iVar13);
        FUN_0047b6db(extraout_ECX_00,iVar13);
        iVar7 = iVar7 + -1;
        FUN_00483ce7(extraout_ECX_01,iVar1);
        lVar16 = (ulonglong)extraout_EDX_01 << 0x20;
      }
      uVar12 = iVar7 << 4;
      while (sVar5 != -1) {
        FUN_004457d3();
        lVar16 = FUN_00483825(extraout_ECX_02,extraout_EDX_02);
        uVar12 = extraout_ECX_03;
        sVar5 = (short)lVar16;
      }
    }
  }
  if (DAT_0050b134 == 0) {
    return;
  }
  do {
    uVar17 = FUN_004704dc(uVar12,uVar9);
    uVar9 = (undefined4)((ulonglong)uVar17 >> 0x20);
    uVar11 = extraout_ECX_04;
    if (DAT_0050a9bc == '\0') break;
    uVar17 = FUN_0046d817(extraout_ECX_04,uVar9);
    uVar9 = (undefined4)((ulonglong)uVar17 >> 0x20);
    uVar12 = extraout_ECX_05;
    uVar11 = extraout_ECX_05;
  } while (((uint)uVar17 & 0xff) == 2);
  iVar7 = *(int *)(&DAT_0050b134 + (uint)DAT_0050b134 * 4);
  uVar17 = FUN_004837f0(uVar11,uVar9);
  if ((ushort)uVar17 == 0xffff) {
    FUN_00483ce7(extraout_ECX_06,iVar7);
    goto LAB_0047b30e;
  }
  uVar18 = FUN_0044113e(100,(int)((ulonglong)uVar17 >> 0x20));
  uVar12 = (uint)uVar18;
  uVar19 = FUN_004704dc(extraout_ECX_07,0);
  uVar11 = (uint)(uVar19 % (ulonglong)extraout_ECX_08);
  bVar4 = unidade_obter_tipo((ushort)uVar17);
  iVar13 = extraout_ECX_09;
  if (bVar4 == 0x18) {
    iVar13 = 0;
    uVar9 = extraout_EDX_03;
    for (local_28 = 0; local_28 < 0x14; local_28 = local_28 + 1) {
      uVar17 = FUN_00489147(iVar13,uVar9);
      iVar13 = extraout_ECX_10;
      if ((ushort)uVar17 == 0xffff) break;
      uVar14 = FUN_0042d4f8(uVar12 & 0xffff,(uint)(ushort)uVar17);
      iVar13 = extraout_ECX_11;
      uVar9 = extraout_EDX_04;
      if (((char)uVar14 != '\0') &&
         (uVar8 = FUN_0047a99a((ushort)extraout_ECX_11,iVar7), iVar13 = extraout_ECX_12,
         uVar9 = extraout_EDX_05, (char)uVar8 != '\0')) goto LAB_0047b30e;
    }
  }
  if ((int)uVar11 < DAT_0050a9c0) {
    uVar11 = (uint)DAT_00508041;
    uVar14 = 0;
  }
  else {
    iVar13 = DAT_0050a9c4;
    if ((int)uVar11 < DAT_0050a9c0 + DAT_0050a9c4) {
      uVar14 = 1;
    }
    else if ((int)uVar11 < DAT_0050a9c0 + DAT_0050a9c4 + _DAT_0050a9c8) {
      uVar14 = 2;
    }
    else {
      uVar14 = 3;
    }
  }
  if (uVar14 < 2) {
LAB_0047b63a:
    iVar13 = 0;
    for (local_30 = 0; local_30 < 0x14; local_30 = local_30 + 1) {
      uVar14 = FUN_00489300(iVar13,'\x03');
      iVar13 = extraout_ECX_13;
      uVar11 = extraout_EDX_08;
      if ((uVar14 & 0xffff) == 0xffff) break;
      uVar14 = FUN_0042d4f8(uVar12 & 0xffff,uVar14 & 0xffff);
      iVar13 = extraout_ECX_14;
      uVar11 = extraout_EDX_09;
      if (((char)uVar14 != '\0') &&
         (uVar9 = FUN_0047a99a((ushort)extraout_ECX_14,iVar7), iVar13 = extraout_ECX_15,
         uVar11 = extraout_EDX_10, (char)uVar9 != '\0')) goto LAB_0047b30e;
    }
  }
  else if (uVar14 == 2) {
    for (local_20 = 0; local_20 < 0x14; local_20 = local_20 + 1) {
      for (iVar13 = 0; iVar13 < (int)(uint)DAT_0050a9ce; iVar13 = iVar13 + 1) {
        DAT_005223d4 = DAT_005223d4 + 1;
        if ((int)(uint)DAT_0050a9ce <= DAT_005223d4) {
          DAT_005223d4 = 0;
        }
        uVar11 = (uint)(ushort)(&DAT_0050a9d4)[DAT_005223d4 * 6];
        if (uVar11 == 0) {
          uVar6 = (&DAT_0050a9d0)[DAT_005223d4 * 6];
          uVar11 = (uint)uVar6;
          if (uVar11 != 0xffff) goto LAB_0047b5fe;
        }
      }
      uVar6 = 0xffff;
LAB_0047b5fe:
      if (uVar6 == 0xffff) break;
      uVar14 = FUN_0042d4f8(uVar12 & 0xffff,(uint)uVar6);
      uVar11 = extraout_EDX_06;
      if (((char)uVar14 != '\0') &&
         (uVar9 = FUN_0047a99a(extraout_CX,iVar7), uVar11 = extraout_EDX_07, (char)uVar9 != '\0'))
      goto LAB_0047b30e;
    }
    goto LAB_0047b63a;
  }
  local_24 = 0;
  while( true ) {
    if (0x13 < local_24) {
      return;
    }
    uVar17 = FUN_00489147(iVar13,uVar11);
    if ((ushort)uVar17 == 0xffff) {
      return;
    }
    uVar14 = FUN_0042d4f8(uVar12 & 0xffff,(uint)(ushort)uVar17);
    iVar13 = extraout_ECX_16;
    uVar11 = extraout_EDX_11;
    if (((char)uVar14 != '\0') &&
       (uVar9 = FUN_0047a99a((ushort)extraout_ECX_16,iVar7), iVar13 = extraout_ECX_17,
       uVar11 = extraout_EDX_12, (char)uVar9 != '\0')) break;
    local_24 = local_24 + 1;
  }
LAB_0047b30e:
  DAT_0050b134 = DAT_0050b134 - 1;
  return;
}
