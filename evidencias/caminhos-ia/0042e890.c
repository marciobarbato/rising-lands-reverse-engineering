/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0042e890(uint param_1)

{
  ushort uVar1;
  undefined3 uVar2;
  ushort *in_EAX;
  ushort *puVar3;
  int iVar4;
  byte bVar5;
  int iVar6;
  char cVar7;
  uint uVar8;
  ushort uVar9;
  int iVar10;
  ushort *puVar11;
  int iVar12;
  undefined8 uVar13;
  undefined4 local_340;
  ushort auStack_33c [254];
  char local_140 [256];
  int local_40;
  uint local_3c;
  int local_38;
  int local_34;
  int local_30;
  int local_2c;
  int local_28;
  uint local_24;
  char local_20;
  byte local_1c;

  local_340 = local_340 & 0xffff0000;
  local_3c = 1;
  do {
    uVar8 = (uint)*in_EAX;
    if ((int)uVar8 < (int)local_3c) {
      iVar4 = 2;
      for (iVar12 = 1; iVar12 < (int)(local_340 & 0xffff); iVar12 = iVar12 + 1) {
        uVar9 = *(ushort *)((int)auStack_33c + iVar4 + -2);
        uVar1 = *(ushort *)((int)auStack_33c + iVar4 + -4);
        local_24 = CONCAT22((short)(param_1 >> 0x10),uVar1) & 0xffff00ff;
        iVar10 = (uint)(uVar9 & 0xff) - (uVar1 & 0xff);
        local_38 = (int)(uint)uVar9 >> 8;
        iVar6 = local_38 - ((int)(uint)uVar1 >> 8);
        bVar5 = 0 < iVar10;
        uVar2 = CONCAT21((short)((uint)iVar6 >> 0x10),bVar5);
        if (0 < iVar6) {
          bVar5 = bVar5 + 2;
        }
        param_1 = CONCAT31(uVar2,bVar5);
        if (iVar10 < 0) {
          iVar10 = -iVar10;
        }
        if (iVar6 < 0) {
          iVar6 = -iVar6;
        }
        if (iVar10 == 0) {
          cVar7 = (&DAT_0049638c)[bVar5];
        }
        else if (iVar6 == 0) {
          cVar7 = (&DAT_00496390)[bVar5];
        }
        else {
          cVar7 = (&DAT_00496388)[bVar5];
        }
        iVar4 = iVar4 + 2;
        local_140[iVar12] = cVar7;
      }
      local_140[0] = local_140[1];
      for (iVar4 = 1; iVar4 < (int)(local_340 & 0xffff); iVar4 = iVar4 + 1) {
        local_140[iVar4] = local_140[iVar4] - local_140[1];
      }
      *in_EAX = 0;
      local_40 = 1;
      do {
        if ((int)(local_340 & 0xffff) < local_40) {
          return;
        }
        iVar12 = (local_340 & 0xffff) - 1;
        local_20 = '\0';
        local_2c = local_40 * 2;
        local_28 = local_40 * 2;
        for (iVar4 = iVar12 * 2; local_28 < iVar4; iVar4 = iVar4 + -2) {
          uVar13 = FUN_0042d674(&local_30,(uint)*(ushort *)((int)auStack_33c + iVar4 + -4));
          if ((char)uVar13 != '\0') {
            local_40 = iVar12;
            local_20 = '\x01';
            *in_EAX = *in_EAX + (short)local_30;
            break;
          }
          iVar12 = iVar12 + -1;
        }
        if (local_20 == '\0') {
          *in_EAX = *in_EAX + 1;
          iVar4 = local_40 + -2;
          local_40 = local_40 + 1;
          in_EAX[*in_EAX] = auStack_33c[iVar4];
        }
      } while( true );
    }
    puVar11 = in_EAX + local_3c;
    local_34 = local_3c + 1;
    puVar3 = in_EAX + uVar8;
    for (; (int)(local_3c + 1) < (int)uVar8; uVar8 = uVar8 - 1) {
      local_1c = ((char)*puVar3 + '\x01') - (char)*puVar11;
      if ((local_1c < 3) &&
         (((((int)(uint)*puVar3 >> 8) + 1) - ((int)(uint)*puVar11 >> 8) & 0xffU) < 3)) {
        uVar9 = (short)local_340 + 1;
        local_340 = CONCAT22(local_340._2_2_,uVar9);
        local_3c = uVar8;
        auStack_33c[uVar9 - 2] = *puVar11;
        break;
      }
      puVar3 = puVar3 + -1;
    }
    param_1 = local_340 + 1;
    local_340 = CONCAT22(local_340._2_2_,(short)param_1);
    puVar3 = in_EAX + local_3c;
    local_3c = local_3c + 1;
    auStack_33c[(param_1 & 0xffff) - 2] = *puVar3;
  } while( true );
}
