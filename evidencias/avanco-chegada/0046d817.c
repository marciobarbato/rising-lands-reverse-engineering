/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall OriginaisSBL::PlayerGetType(undefined4 param_1,undefined4 param_2)

{
  uint in_EAX;
  uint uVar1;

  uVar1 = in_EAX & 0xff;
  if (uVar1 < 4) {
    return CONCAT44(param_2,CONCAT31((int3)(uVar1 * 5 >> 8),
                                     *(undefined1 *)(DAT_005080a8 + 1 + uVar1 * 0x14)));
  }
  return CONCAT44(param_2,CONCAT31((int3)(in_EAX >> 8),2));
}
