/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

longlong __fastcall FUN_0047d1b8(undefined4 param_1,uint param_2)

{
  int iVar2;
  int iVar1;
  undefined4 extraout_ECX;

  FUN_00458461(param_1,0x70);
  FUN_00458461(extraout_ECX,0x2580);
  _DAT_005148ac = &DAT_00512320;
  iVar2 = 0;
  do {
    iVar1 = iVar2 + 0x10;
    *(undefined **)((int)&DAT_005148bc + iVar2) = &DAT_00512320;
    iVar2 = iVar1;
  } while (iVar1 != 0x50);
  return (ulonglong)param_2 << 0x20;
}
