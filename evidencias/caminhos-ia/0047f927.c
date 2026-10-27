/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall FUN_0047f927(undefined4 param_1,uint param_2)

{
  int in_EAX;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  int iVar1;
  undefined4 extraout_EDX;
  uint extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined8 uVar2;
  longlong lVar3;

  iVar1 = in_EAX * 0x10;
  if (in_EAX == 4) {
    FUN_0047b283();
    uVar2 = FUN_0047d314(extraout_ECX,extraout_EDX);
    iVar1 = (int)uVar2;
    if (iVar1 == 0) {
      return 0;
    }
    if (iVar1 == 0x1a1a000e) {
      return 0x1a1a000e;
    }
    if (iVar1 == 0) {
      return 0;
    }
    return iVar1;
  }
  if (*(char *)((int)&DAT_0051a98e + iVar1 + 2) != '\0') {
    return 0;
  }
  if ((*(int *)(&DAT_004dfaa8 + in_EAX * 4) == 0) && (*(short *)(&DAT_004e1928 + in_EAX * 2) == 0))
  {
    (&DAT_0051a995)[iVar1] = (&DAT_0051a995)[iVar1] + '\x01';
    if ((&DAT_0051a995)[iVar1] == '\n') {
      FUN_00483d95(param_2);
      iVar1 = 0x1a1a0019;
      goto LAB_0047f9c8;
    }
  }
  else {
    (&DAT_0051a995)[in_EAX * 0x10] = 0;
  }
  iVar1 = 0;
LAB_0047f9c8:
  if (iVar1 == 0x1a1a0019) {
    *(undefined1 *)((int)&DAT_0051a98e + in_EAX * 0x10 + 2) = 1;
    return 0;
  }
  iVar1 = FUN_00482936();
  if (iVar1 != 0) {
    return iVar1;
  }
  lVar3 = FUN_0048453c(extraout_ECX_00,extraout_EDX_00);
  if ((int)lVar3 != 0) {
    return (int)lVar3;
  }
  lVar3 = FUN_00485183(extraout_ECX_01,(uint)((ulonglong)lVar3 >> 0x20));
  if ((int)lVar3 != 0) {
    return (int)lVar3;
  }
  iVar1 = FUN_004866d7();
  if (iVar1 != 0) {
    return iVar1;
  }
  uVar2 = FUN_0047d314(extraout_ECX_02,extraout_EDX_01);
  iVar1 = (int)uVar2;
  if (((iVar1 == 0) || (iVar1 == 0x1a1a000e)) || (iVar1 == 0)) {
    return iVar1;
  }
  return iVar1;
}
