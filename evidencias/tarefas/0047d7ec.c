/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_0047d7ec(undefined4 param_1,undefined4 param_2)

{
  ushort uVar1;
  int in_EAX;
  int iVar2;
  int iVar3;
  undefined8 uVar4;

  if (((in_EAX == 0) || (0x3f < in_EAX)) || (*(short *)(&DAT_0051a720 + in_EAX * 2) == 0)) {
    return CONCAT44(param_2,0xffffffff);
  }
  uVar4 = FUN_0047d012(param_1,in_EAX);
  iVar2 = (int)uVar4;
  if (iVar2 != -1) {
    iVar3 = iVar2 * 0x60;
    DAT_00514904 = DAT_00514904 + 1;
    *(undefined4 *)(&DAT_00512324 + iVar3) = 0xffffffff;
    *(undefined4 *)(&DAT_00512328 + iVar3) = 0xffffffff;
    *(short *)(&DAT_0051237a + iVar3) = (short)((ulonglong)uVar4 >> 0x20);
    uVar1 = *(ushort *)(&DAT_0051a720 + in_EAX * 2);
    *(undefined2 *)(&DAT_00512378 + iVar3) = 0;
    (&DAT_0051237e)[iVar3] = 0;
    (&DAT_0051237f)[iVar3] = 0;
    *(undefined4 *)(&DAT_00512330 + iVar3) = 0;
    (&DAT_0051237d)[iVar3] = 0xff;
    *(undefined4 *)(&DAT_00512334 + iVar3) = 0;
    *(uint *)(&DAT_0051232c + iVar3) = (uint)uVar1;
  }
  return CONCAT44(param_2,iVar2);
}
