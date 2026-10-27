/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::ResetCollision(undefined4 param_1,byte param_2)

{
  byte *pbVar1;
  uint in_EAX;

  pbVar1 = (byte *)(DAT_00507da8 + (in_EAX & 0xffff));
  *pbVar1 = *pbVar1 & ~param_2;
  return;
}
