/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::Remplit(undefined4 param_1,char param_2)

{
  char cVar1;
  ushort uVar2;
  ushort in_AX;
  int iVar3;
  uint uVar4;
  int iVar5;
  int iVar6;
  int iVar7;
  byte local_24;
  byte local_20;

  if (param_2 != '\0') {
    cVar1 = *(char *)((uint)in_AX + DAT_004e156c);
    iVar7 = 1;
    DAT_004e0734 = in_AX;
    do {
      if (iVar7 == 0) {
        return;
      }
      uVar2 = *(ushort *)(iVar7 * 2 + 0x4e0732);
      iVar7 = iVar7 + -1;
      if (*(char *)((uint)uVar2 + DAT_004e156c) == cVar1) {
        *(char *)((uint)uVar2 + DAT_004e156c) = param_2;
      }
      local_24 = 1;
      iVar5 = iVar7 * 2;
      for (local_20 = 0; local_20 < 4; local_20 = local_20 + 1) {
        iVar6 = (uint)(uVar2 & 0xff) + *(int *)(&DAT_00496308 + (uint)local_24 * 8);
        iVar3 = ((int)(uint)uVar2 >> 8) + *(int *)(&DAT_0049630c + (uint)local_24 * 8);
        if ((((iVar6 < 0) || ((int)(DAT_00497168 - 1) < iVar6)) || (iVar3 < 0)) ||
           ((int)(DAT_0049716a - 1) < iVar3)) {
          uVar4 = 0xffff;
        }
        else {
          uVar4 = iVar3 * 0x100 + iVar6;
        }
        iVar3 = iVar5;
        if ((((uVar4 & 0xffff) != 0xffff) && (*(char *)((uVar4 & 0xffff) + DAT_004e156c) == cVar1))
           && (iVar7 < 0x3ff)) {
          iVar3 = iVar5 + 2;
          iVar7 = iVar7 + 1;
          *(short *)((int)&DAT_004e0734 + iVar5) = (short)uVar4;
        }
        local_24 = local_24 + 4;
        iVar5 = iVar3;
      }
    } while (iVar7 != 0x3ff);
  }
  return;
}
