/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::IllumineTerrain(undefined4 param_1,uint param_2)

{
  ushort in_AX;
  ushort uVar1;
  ushort uVar2;
  short sVar3;
  int iVar4;
  int iVar5;
  int extraout_ECX;
  int extraout_ECX_00;
  int extraout_ECX_01;
  uint uVar6;
  byte unaff_BL;
  uint uVar7;
  undefined4 local_24;
  char cStack_1f;
  undefined2 uStack_1e;
  short sStack_1c;
  short local_14;

  uVar6 = (uint)in_AX % 0x100;
  uVar1 = in_AX / 0x100;
  sVar3 = (short)param_2;
  uVar2 = sVar3 * sVar3;
  if (1 < (param_2 & 0xffff)) {
    uVar2 = uVar2 + 1;
  }
  local_14 = -sVar3;
  local_24 = CONCAT22(local_24._2_2_,sVar3 * -0x100 + uVar1 * 0x100);
  while( true ) {
    if ((int)(param_2 & 0xffff) < (int)local_14) break;
    iVar4 = (int)local_14 + (int)(short)uVar1;
    if ((-1 < iVar4) && (iVar4 < (int)(uint)DAT_0049716a)) {
      uVar7 = -param_2;
      iVar4 = local_24 + uVar7 + uVar6;
      for (; (int)(short)uVar7 <= (int)(param_2 & 0xffff); uVar7 = uVar7 + 1) {
        iVar5 = (int)(short)uVar7 + (int)(short)uVar6;
        if (((-1 < iVar5) && (iVar5 < (int)(uint)DAT_00497168)) &&
           (iVar5 = Distance(iVar4,uVar7 & 0xffff), iVar4 = extraout_ECX, (ushort)iVar5 <= uVar2)) {
          IllumineCase(extraout_ECX,unaff_BL);
          iVar4 = extraout_ECX_00;
        }
        iVar4 = iVar4 + 1;
      }
    }
    local_14 = local_14 + 1;
    local_24 = (uint)CONCAT21(local_24._2_2_,local_24._1_1_ + '\x01') << 8;
  }
  sStack_1c = -sVar3;
  sVar3 = sVar3 * -0x100 + uVar1 * 0x100;
  while( true ) {
    cStack_1f = (char)((ushort)sVar3 >> 8);
    if ((int)(param_2 & 0xffff) < (int)sStack_1c) break;
    iVar4 = (int)sStack_1c + (int)(short)uVar1;
    if ((-1 < iVar4) && (iVar4 < (int)(uint)DAT_0049716a)) {
      uVar7 = -param_2;
      iVar4 = CONCAT22(uStack_1e,sVar3) + uVar7 + uVar6;
      for (; (int)(short)uVar7 <= (int)(param_2 & 0xffff); uVar7 = uVar7 + 1) {
        iVar5 = (int)(short)uVar7 + (int)(short)uVar6;
        if ((-1 < iVar5) && (iVar5 < (int)(uint)DAT_00497168)) {
          Distance(iVar4,uVar7 & 0xffff);
          iVar4 = extraout_ECX_01;
        }
        iVar4 = iVar4 + 1;
      }
    }
    sVar3 = (ushort)(byte)(cStack_1f + 1) << 8;
    sStack_1c = sStack_1c + 1;
  }
  return;
}
