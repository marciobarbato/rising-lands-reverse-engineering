/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

longlong __fastcall OriginaisSBL::TuyauEstSortie(undefined4 param_1,undefined4 param_2)

{
  ushort in_AX;
  int iVar1;
  undefined3 uVar2;

  iVar1 = (uint)in_AX * 0x114;
  uVar2 = (undefined3)((uint)(&DAT_0049a0c8 + iVar1) >> 8);
  if (((&DAT_0049a13e)[iVar1] == '\x0f') && ((&DAT_0049a13d)[iVar1] != '\0')) {
    return CONCAT44(param_2,CONCAT31(uVar2,1));
  }
  return (ulonglong)CONCAT43(param_2,uVar2) << 8;
}
