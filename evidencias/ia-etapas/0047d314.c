/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_0047d314(undefined4 param_1,undefined4 param_2)

{
  undefined2 uVar1;
  int *in_EAX;
  int *piVar2;
  undefined4 uVar3;
  uint uVar4;
  int iVar5;
  undefined4 extraout_ECX;
  int iVar6;
  uint *puVar7;
  undefined2 *puVar8;
  byte bVar9;
  int iVar10;
  int iVar11;
  undefined8 uVar12;
  undefined4 local_54 [6];
  uint local_3c;
  uint local_38;
  int local_34;
  int local_30;
  int local_2c;
  int *local_28;
  int local_24;
  uint local_20;
  int local_1c;

  local_30 = *in_EAX;
  do {
    if (local_30 == -1) {
      if (DAT_00514904 == 0) {
        uVar3 = 0x1a1a000e;
      }
      else {
        uVar3 = 0;
      }
      return CONCAT44(param_2,uVar3);
    }
    iVar11 = local_30 * 0x60;
    iVar6 = *(int *)(&DAT_00512320 + iVar11);
    local_24 = local_30;
    local_1c = local_30;
    if ((&DAT_0051237e)[iVar11] == '\0') {
LAB_0047d37e:
      local_30 = iVar6;
      iVar6 = *(int *)(&DAT_0051232c + iVar11) * 0x14;
      puVar7 = (uint *)(&DAT_00514910 + iVar6);
      if ((&DAT_0051237f)[iVar11] != '\0') {
        if (*(short *)(&DAT_00512378 + iVar11) == 0) {
          if ((*(uint *)(&DAT_00514914 + iVar6) & 0xf) != 0) {
            *(undefined4 *)(&DAT_00512334 + (*(uint *)(&DAT_00514914 + iVar6) & 0xf) * 4 + iVar11) =
                 *(undefined4 *)(&DAT_00512374 + iVar11);
          }
        }
        else {
          *(undefined2 *)(&DAT_00512378 + iVar11) = 0;
        }
        (&DAT_0051237f)[iVar11] = 0;
        uVar12 = CONCAT44(puVar7,*(undefined4 *)(&DAT_00512374 + iVar11));
LAB_0047d52c:
        iVar6 = (int)((ulonglong)uVar12 >> 0x20);
        if ((int)uVar12 == -1) {
          uVar3 = *(undefined4 *)(iVar6 + 0xc);
        }
        else {
          uVar3 = *(undefined4 *)(iVar6 + 8);
        }
        switch(uVar3) {
        case 0:
        case 3:
          goto switchD_0047d540_caseD_0;
        case 1:
          if (*(int *)(&DAT_00512324 + iVar11) != -1) {
            iVar6 = *(int *)(&DAT_00512324 + iVar11) * 0x60;
            *(undefined4 *)(&DAT_00512374 + iVar6) = 1;
LAB_0047d55f:
            (&DAT_0051237e)[iVar6] = 0;
            (&DAT_0051237f)[iVar6] = 1;
          }
          break;
        case 2:
          if (*(int *)(&DAT_00512324 + iVar11) != -1) {
            iVar6 = *(int *)(&DAT_00512324 + iVar11) * 0x60;
            *(undefined4 *)(&DAT_00512374 + iVar6) = 0xffffffff;
            goto LAB_0047d55f;
          }
          break;
        default:
          goto switchD_0047d540_default;
        }
        iVar6 = 0x1a1a000d;
        goto LAB_0047d438;
      }
      if (0x3f < *puVar7) {
        bVar9 = 8;
        local_3c = *(uint *)(&DAT_00514914 + iVar6) >> 4 & 0xf;
        for (iVar10 = 0; iVar10 < (int)local_3c; iVar10 = iVar10 + 1) {
          uVar4 = *(uint *)(&DAT_00514914 + iVar6) >> (bVar9 & 0x1f) & 0xf;
          if (uVar4 == 0) {
            uVar3 = *(undefined4 *)(&DAT_00514920 + iVar6);
          }
          else {
            uVar3 = *(undefined4 *)(&DAT_00512334 + uVar4 * 4 + iVar11);
          }
          local_54[iVar10] = uVar3;
          bVar9 = bVar9 + 4;
        }
        local_38 = (uint)(byte)(&DAT_0051237c)[iVar11];
        local_34 = local_1c;
        uVar12 = (*(code *)*puVar7)();
        iVar6 = local_30;
        if ((&DAT_0051237e)[iVar11] == '\0') {
          uVar4 = *(uint *)((int)((ulonglong)uVar12 >> 0x20) + 4) & 0xf;
          if (uVar4 != 0) {
            *(int *)(&DAT_00512334 + uVar4 * 4 + iVar11) = (int)uVar12;
          }
          goto LAB_0047d52c;
        }
        goto LAB_0047d436;
      }
      uVar12 = FUN_0047d7ec(*puVar7,puVar7);
      puVar8 = (undefined2 *)((ulonglong)uVar12 >> 0x20);
      local_2c = (int)uVar12;
      if (local_2c != -1) {
        iVar6 = local_2c * 0x60;
        local_28 = (int *)(&DAT_00512320 + iVar6);
        local_20 = *(uint *)(puVar8 + 2) >> 4 & 0xf;
        bVar9 = 8;
        piVar2 = local_28;
        for (iVar10 = 0; iVar10 < (int)local_20; iVar10 = iVar10 + 1) {
          uVar4 = *(uint *)(puVar8 + 2) >> (bVar9 & 0x1f) & 0xf;
          if (uVar4 == 0) {
            iVar5 = *(int *)(puVar8 + 8);
          }
          else {
            iVar5 = *(int *)(&DAT_00512334 + uVar4 * 4 + iVar11);
          }
          piVar2[6] = iVar5;
          piVar2 = piVar2 + 1;
          bVar9 = bVar9 + 4;
        }
        (&DAT_0051237c)[iVar6] = (&DAT_0051237c)[iVar11];
        *local_28 = *(int *)(&DAT_00512320 + iVar11);
        *(int *)(&DAT_00512320 + iVar11) = local_2c;
        *(undefined4 *)(&DAT_00512334 + iVar6) = 0;
        *(int *)(&DAT_00512324 + iVar6) = local_1c;
        uVar1 = *puVar8;
        (&DAT_0051237e)[iVar11] = 1;
        *(undefined2 *)(&DAT_00512378 + iVar11) = uVar1;
        iVar6 = local_30;
        goto LAB_0047d436;
      }
switchD_0047d540_caseD_0:
      iVar6 = 0x1a1a000c;
    }
    else {
      if (0 < *(int *)(&DAT_00512334 + iVar11)) {
        iVar10 = *(int *)(&DAT_00512334 + iVar11) + -1;
        *(int *)(&DAT_00512334 + iVar11) = iVar10;
        if (iVar10 < 1) {
          (&DAT_0051237e)[iVar11] = 0;
          (&DAT_0051237f)[iVar11] = 1;
          *(undefined4 *)(&DAT_00512374 + iVar11) = 1;
          *(undefined4 *)(&DAT_00512334 + iVar11) = 0;
          goto LAB_0047d37e;
        }
      }
LAB_0047d436:
      local_30 = iVar6;
      iVar6 = 0;
    }
LAB_0047d438:
    iVar11 = local_24;
    if ((iVar6 == 0x1a1a000c) || (iVar6 == 0x1a1a000d)) {
      if (*(int *)(&DAT_00512324 + local_24 * 0x60) != -1) {
        iVar6 = *(int *)(&DAT_00512324 + local_24 * 0x60) * 0x60;
        (&DAT_0051237e)[iVar6] = 0;
        (&DAT_0051237f)[iVar6] = 1;
      }
      FUN_0047d11a(in_EAX,local_24);
      FUN_0047d03a(extraout_ECX,iVar11);
      DAT_00514904 = DAT_00514904 + -1;
    }
  } while( true );
switchD_0047d540_default:
  *(undefined4 *)(&DAT_0051232c + iVar11) = uVar3;
  iVar6 = local_30;
  goto LAB_0047d37e;
}
