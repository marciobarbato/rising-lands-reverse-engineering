/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::SetCollision(undefined4 param_1,byte param_2)

{
  ushort in_AX;

  *(byte *)((uint)in_AX + DAT_00507da8) = *(byte *)((uint)in_AX + DAT_00507da8) | param_2;
  return;
}
