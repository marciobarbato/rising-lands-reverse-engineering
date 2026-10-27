/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::EteintTerrain(undefined4 param_1,uint param_2)

{
  ushort in_AX;
  ushort uVar1;
  short sVar2;
  uint uVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  int extraout_ECX;
  int extraout_ECX_00;
  int extraout_ECX_01;
  uint uVar7;
  byte unaff_BL;
  uint uVar8;
  undefined4 local_28;
  char cStack_23;
  undefined2 uStack_22;
  short sStack_20;

  uVar7 = (uint)in_AX % 0x100;
  uVar3 = in_AX / 0x100;
  sVar2 = (short)param_2;
  uVar1 = sVar2 * sVar2;
  if (1 < (param_2 & 0xffff)) {
    uVar1 = uVar1 + 1;
  }
  local_28 = CONCAT22(local_28._2_2_,sVar2 * -0x100 + (short)uVar3 * 0x100);
  for (sStack_20 = -sVar2; (int)sStack_20 <= (int)(param_2 & 0xffff); sStack_20 = sStack_20 + 1) {
    iVar4 = (int)sStack_20 + uVar3;
    if ((-1 < iVar4) && (iVar4 < (int)(uint)DAT_0049716a)) {
      uVar8 = -param_2;
      iVar4 = local_28 + uVar8 + uVar7;
      for (; (int)(short)uVar8 <= (int)(param_2 & 0xffff); uVar8 = uVar8 + 1) {
        iVar5 = Distance(iVar4,uVar8 & 0xffff);
        iVar4 = extraout_ECX;
        if ((((ushort)iVar5 <= uVar1) && (iVar5 = (int)(short)uVar8 + uVar7, -1 < iVar5)) &&
           (iVar5 < (int)(uint)DAT_00497168)) {
          EteintCase(extraout_ECX,unaff_BL);
          iVar4 = extraout_ECX_00;
        }
        iVar4 = iVar4 + 1;
      }
    }
    local_28 = (uint)CONCAT21(local_28._2_2_,local_28._1_1_ + '\x01') << 8;
  }
  iVar4 = -param_2;
  sVar2 = sVar2 * -0x100 + (short)uVar3 * 0x100;
  while( true ) {
    cStack_23 = (char)((ushort)sVar2 >> 8);
    if ((int)(param_2 & 0xffff) < (int)(short)iVar4) break;
    iVar5 = (int)(short)iVar4 + uVar3;
    if ((-1 < iVar5) && (iVar5 < (int)(uint)DAT_0049716a)) {
      uVar8 = -param_2;
      iVar5 = CONCAT22(uStack_22,sVar2) + uVar8 + uVar7;
      for (; (int)(short)uVar8 <= (int)(param_2 & 0xffff); uVar8 = uVar8 + 1) {
        iVar6 = (int)(short)uVar8 + uVar7;
        if ((-1 < iVar6) && (iVar6 < (int)(uint)DAT_00497168)) {
          Distance(iVar5,uVar8 & 0xffff);
          iVar5 = extraout_ECX_01;
        }
        iVar5 = iVar5 + 1;
      }
    }
    sVar2 = (ushort)(byte)(cStack_23 + 1) << 8;
    iVar4 = iVar4 + 1;
  }
  return;
}
