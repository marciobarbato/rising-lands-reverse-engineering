/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall
FUN_0047d98b(int param_1,uint param_2,int param_3,int param_4,int param_5,int param_6,int param_7)

{
  int in_EAX;
  int iVar1;
  int iVar2;
  uint uVar3;
  uint unaff_EBX;

  iVar2 = *(int *)(&DAT_005148b0 + in_EAX * 0x10);
  while( true ) {
    if (iVar2 == -1) {
      return -1;
    }
    iVar1 = iVar2 * 0x60;
    if ((int *)(&DAT_00512320 + iVar1) == (int *)0x0) break;
    if (*(ushort *)(&DAT_0051237a + iVar1) == param_2) {
      uVar3 = *(ushort *)(&DAT_0051237a + iVar1) ^ param_2;
      if ((0 < (int)unaff_EBX) && (param_1 == *(int *)(&DAT_00512338 + iVar1))) {
        uVar3 = 1;
      }
      if ((1 < (int)unaff_EBX) && (*(int *)(&DAT_0051233c + iVar1) == param_3)) {
        uVar3 = uVar3 + 1;
      }
      if ((2 < (int)unaff_EBX) && (*(int *)(&DAT_00512340 + iVar1) == param_4)) {
        uVar3 = uVar3 + 1;
      }
      if ((3 < (int)unaff_EBX) && (*(int *)(&DAT_00512344 + iVar1) == param_5)) {
        uVar3 = uVar3 + 1;
      }
      if ((4 < (int)unaff_EBX) && (*(int *)(&DAT_00512348 + iVar1) == param_6)) {
        uVar3 = uVar3 + 1;
      }
      if ((5 < (int)unaff_EBX) && (*(int *)(&DAT_0051234c + iVar1) == param_7)) {
        uVar3 = uVar3 + 1;
      }
      if (uVar3 == unaff_EBX) {
        return iVar2;
      }
    }
    iVar2 = *(int *)(&DAT_00512320 + iVar1);
  }
  return -1;
}
