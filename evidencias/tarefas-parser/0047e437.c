/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined4 __fastcall FUN_0047e437(undefined4 param_1,int param_2)

{
  int *piVar1;
  uint uVar2;
  uint uVar3;
  HGLOBAL pvVar4;
  LPVOID pMem;
  int iVar5;
  undefined4 extraout_ECX;
  uint extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 uVar6;
  undefined4 extraout_ECX_04;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 extraout_EDX_02;
  undefined4 extraout_EDX_03;
  uint extraout_EDX_04;
  undefined **ppuVar7;
  int iVar8;
  uint *puVar9;
  longlong lVar10;
  int local_2c;
  SIZE_T local_24;
  ushort local_20;
  ushort local_1e;

  piVar1 = (int *)FUN_0048c71f(param_1,&DAT_00494f63);
  if (piVar1 != (int *)0x0) {
    uVar2 = FUN_0048c97b(piVar1,1);
    if ((uVar2 == 0x10) && (local_2c == 0x454c5552)) {
      if (0x4b0 < local_20) {
        FUN_0048c80b(extraout_ECX,extraout_EDX);
        return 0x1a1a0008;
      }
      uVar3 = FUN_0048c97b(piVar1,1);
      uVar2 = (uint)local_20;
      uVar6 = extraout_EDX_00;
      if (((uVar3 == uVar2 * 0x14) && (local_1e < 0x41)) &&
         (uVar3 = FUN_0048c97b(piVar1,1), uVar2 = extraout_ECX_00, uVar6 = extraout_EDX_01,
         uVar3 == (uint)local_1e * 2)) {
        pvVar4 = GlobalAlloc(0,local_24);
        pMem = GlobalLock(pvVar4);
        if (pMem == (LPVOID)0x0) {
          FUN_0048c80b(extraout_ECX_01,extraout_EDX_02);
          return 0x1a1a0003;
        }
        uVar2 = FUN_0048c97b(piVar1,1);
        if (uVar2 == local_24) {
          FUN_0048c80b(extraout_ECX_02,extraout_EDX_03);
          iVar8 = 0;
          DAT_00514900 = local_20 - 4;
          puVar9 = &DAT_00514960;
          do {
            if (DAT_00514900 <= iVar8) {
              pvVar4 = GlobalHandle(pMem);
              GlobalUnlock(pvVar4);
              pvVar4 = GlobalHandle(pMem);
              GlobalFree(pvVar4);
              return 0;
            }
            if ((*puVar9 & 0x80000000) != 0) {
              ppuVar7 = &PTR_s_B_Bidon_00498454;
              uVar2 = FUN_0048d4c0((*puVar9 & 0x7fffffff) + (int)pMem,(uint *)&DAT_00494f4b);
              if (uVar2 == 0) {
                *puVar9 = 0;
                iVar5 = 0;
              }
              else {
                uVar6 = extraout_ECX_03;
                if (param_2 == 1) {
                  lVar10 = FUN_0048d6fe(extraout_ECX_03,extraout_EDX_04);
                  *puVar9 = (uint)lVar10;
                  if ((uint)lVar10 == 0) {
                    iVar5 = 0x1a1a0002;
                  }
                  else {
LAB_0047e608:
                    iVar5 = 0;
                  }
                }
                else {
                  for (; *ppuVar7 != (undefined *)0x0; ppuVar7 = ppuVar7 + 2) {
                    uVar2 = FUN_0048d4c0(uVar6,(uint *)uVar6);
                    if (uVar2 == 0) {
                      *puVar9 = (uint)ppuVar7[1];
                      goto LAB_0047e608;
                    }
                    uVar6 = extraout_ECX_04;
                  }
                  iVar5 = 0x1a1a0002;
                }
              }
              if (iVar5 != 0) {
                pvVar4 = GlobalHandle(pMem);
                GlobalUnlock(pvVar4);
                pvVar4 = GlobalHandle(pMem);
                GlobalFree(pvVar4);
                return 0x1a1a0002;
              }
            }
            puVar9 = puVar9 + 5;
            iVar8 = iVar8 + 1;
          } while( true );
        }
        FUN_0048c80b(extraout_ECX_02,extraout_EDX_03);
        pvVar4 = GlobalHandle(pMem);
        GlobalUnlock(pvVar4);
        pvVar4 = GlobalHandle(pMem);
        GlobalFree(pvVar4);
      }
      else {
        FUN_0048c80b(uVar2,uVar6);
      }
      return 0x1a1a0001;
    }
    FUN_0048c80b(extraout_ECX,extraout_EDX);
  }
  return 0x1a1a0004;
}
