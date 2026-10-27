/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall OriginaisSBL::Chemin_Remap(undefined4 param_1,undefined4 param_2)

{
  ushort uVar1;
  HGLOBAL pvVar2;
  byte *pMem;
  byte *pbVar3;
  ushort *pMem_00;
  ushort *puVar4;
  ushort *puVar5;
  int iVar6;
  byte bVar7;
  undefined4 extraout_ECX;
  undefined4 uVar8;
  undefined4 extraout_ECX_00;
  byte bVar9;
  undefined1 *puVar10;
  uint uVar11;
  int iVar12;
  short *psVar13;
  ulonglong uVar14;
  int local_38;
  int local_34;
  uint local_24;
  uint local_20;

  DAT_004e0f36 = 0;
  DAT_004e0f37 = 0;
  DAT_004e0f3c = 0;
  DAT_00496304 = 0xffff;
  memset(param_1,0);
  memset(extraout_ECX,1);
  DAT_004e1570 = 0xff;
  local_24 = 1;
  do {
    iVar12 = local_24 + 1;
    (&DAT_004e1570)[local_24] = (undefined1)local_24;
    local_24 = iVar12;
  } while (iVar12 < 0x100);
  memset(iVar12,0);
  pvVar2 = GlobalAlloc(0,0x10000);
  pMem = GlobalLock(pvVar2);
  uVar11 = 0;
  if (pMem != (byte *)0x0) {
    local_24 = 0;
    pbVar3 = pMem;
    do {
      *pbVar3 = *(byte *)(DAT_00507da8 + local_24) & 1;
      local_24 = local_24 + 1;
      pbVar3 = pbVar3 + 1;
    } while ((int)local_24 < 0x10000);
    uVar8 = 0;
    local_24 = 0;
    pbVar3 = pMem;
    do {
      uVar14 = TerrainEstObstacleNaturel(uVar8,pbVar3);
      puVar10 = (undefined1 *)(uVar14 >> 0x20);
      if ((uVar14 & 0xff) == 0) {
        *puVar10 = 0;
      }
      local_24 = local_24 + 1;
      pbVar3 = puVar10 + 1;
      uVar8 = extraout_ECX_00;
    } while ((int)local_24 < 0x10000);
    local_20 = 0;
    local_24 = 0;
    local_38 = 0;
    do {
      if (*(short *)(DAT_004e0f38 + local_38) == 0) {
        local_20 = local_20 + 1;
        pvVar2 = GlobalAlloc(0,0x100000);
        pMem_00 = GlobalLock(pvVar2);
        puVar5 = pMem_00;
        uVar11 = local_24;
        do {
          *puVar5 = (ushort)uVar11;
          puVar5 = puVar5 + 1;
          do {
            do {
              do {
                puVar4 = puVar5;
                if (puVar4 == pMem_00) {
                  pvVar2 = GlobalHandle(pMem_00);
                  GlobalUnlock(pvVar2);
                  pvVar2 = GlobalHandle(pMem_00);
                  GlobalFree(pvVar2);
                  goto LAB_0042ef6d;
                }
                puVar5 = puVar4 + -1;
                uVar1 = *puVar5;
              } while ((pMem[uVar1] != pMem[local_24 & 0xffff]) ||
                      (psVar13 = (short *)((uint)uVar1 * 2 + DAT_004e0f38), *psVar13 != 0));
              *psVar13 = (short)local_20;
              bVar9 = (byte)uVar1;
              bVar7 = (byte)(uVar1 >> 8);
              if (bVar9 != 0) {
                *puVar5 = uVar1 - 1;
                puVar5 = puVar4;
              }
              if (bVar9 != 0xff) {
                *puVar5 = uVar1 + 1;
                puVar5 = puVar5 + 1;
              }
              if (bVar7 != 0xff) {
                *puVar5 = CONCAT11(bVar7 + 1,bVar9);
                puVar5 = puVar5 + 1;
              }
              if (bVar7 != 0) {
                *puVar5 = uVar1 - 0x100;
                puVar5 = puVar5 + 1;
              }
            } while (pMem[local_24 & 0xffff] != 0);
            if ((bVar9 != 0) && (bVar7 != 0)) {
              *puVar5 = uVar1 - 0x101;
              puVar5 = puVar5 + 1;
            }
            if ((bVar9 != 0) && (bVar7 != 0xff)) {
              *puVar5 = uVar1 + 0xff;
              puVar5 = puVar5 + 1;
            }
            if ((bVar9 != 0xff) && (bVar7 != 0)) {
              *puVar5 = uVar1 - 0xff;
              puVar5 = puVar5 + 1;
            }
          } while ((0xfe < bVar9) || (0xfe < bVar7));
          uVar11 = uVar1 + 0x101;
        } while( true );
      }
LAB_0042ef6d:
      local_38 = local_38 + 2;
      local_24 = local_24 + 1;
    } while ((int)local_24 < 0x10000);
    iVar12 = 0;
    local_34 = 0;
    do {
      if (iVar12 < (int)(uint)DAT_0049716a) {
        local_24 = (uint)DAT_00497168;
      }
      else {
        local_24 = 0;
      }
      iVar6 = local_24 * 2 + local_34;
      for (; (int)local_24 < 0x100; local_24 = local_24 + 1) {
        *(undefined2 *)(DAT_004e0f38 + iVar6) = 0;
        *(undefined1 *)(local_24 + iVar12 * 0x100 + DAT_00507da8) = 1;
        iVar6 = iVar6 + 2;
      }
      local_34 = local_34 + 0x200;
      iVar12 = iVar12 + 1;
    } while (iVar12 < 0x100);
    pvVar2 = GlobalHandle(pMem);
    GlobalUnlock(pvVar2);
    pvVar2 = GlobalHandle(pMem);
    GlobalFree(pvVar2);
    uVar11 = local_20 & 0xffff;
    if ((ushort)local_20 < 0x4000) {
      uVar11 = CONCAT31((uint3)(byte)(local_20 >> 8),1);
      goto LAB_0042f1d7;
    }
  }
  uVar11 = uVar11 & 0xffffff00;
LAB_0042f1d7:
  return CONCAT44(param_2,uVar11);
}
