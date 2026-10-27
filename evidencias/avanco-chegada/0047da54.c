/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::iaProbReturnTo(undefined4 param_1,undefined4 param_2)

{
  int in_EAX;
  int iVar1;

  iVar1 = in_EAX * 0x60;
  (&DAT_0051237e)[iVar1] = 0;
  (&DAT_0051237f)[iVar1] = 1;
  *(undefined4 *)(&DAT_00512334 + iVar1) = 0;
  *(undefined4 *)(&DAT_00512374 + iVar1) = param_2;
  return;
}
