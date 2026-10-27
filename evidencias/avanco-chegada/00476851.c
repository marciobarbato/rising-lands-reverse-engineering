/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::DecouvreTerrain(undefined4 param_1,int param_2)

{
  ushort in_AX;
  ushort uVar1;
  int iVar2;
  int iVar3;
  int extraout_ECX;
  int extraout_ECX_00;
  byte unaff_BL;
  uint uVar4;
  uint uVar5;
  int iVar6;
  uint uVar7;

  uVar7 = param_2 + 1;
  uVar1 = (short)uVar7 * (short)uVar7;
  if (1 < (uVar7 & 0xffff)) {
    uVar1 = uVar1 + 1;
  }
  iVar6 = -uVar7;
  uVar4 = in_AX / 0x100 + iVar6;
  for (; (int)(short)iVar6 <= (int)(uVar7 & 0xffff); iVar6 = iVar6 + 1) {
    if ((-1 < (short)uVar4) && ((int)(short)uVar4 < (int)(uint)DAT_0049716a)) {
      uVar5 = -uVar7;
      iVar3 = (uint)in_AX % 0x100 + uVar5;
      for (; (int)(short)uVar5 <= (int)(uVar7 & 0xffff); uVar5 = uVar5 + 1) {
        if ((-1 < (short)iVar3) && ((int)(short)iVar3 < (int)(uint)DAT_00497168)) {
          iVar2 = Distance(iVar3,uVar5 & 0xffff);
          iVar3 = extraout_ECX;
          if ((ushort)iVar2 <= uVar1) {
            DecouvreCase(extraout_ECX,unaff_BL);
            iVar3 = extraout_ECX_00;
          }
        }
        iVar3 = iVar3 + 1;
      }
    }
    uVar4 = (uVar4 & 0xffff) + 1;
  }
  return;
}
