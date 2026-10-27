/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_0046d838(undefined4 param_1,byte param_2)

{
  int iVar1;
  uint in_EAX;

  if (((byte)in_EAX == param_2) ||
     (((in_EAX = in_EAX & 0xff, in_EAX < 5 && (param_2 < 5)) &&
      (iVar1 = in_EAX * 0x14, in_EAX = (uint)(char)('\x01' << (param_2 & 0x1f)),
      (*(int *)(DAT_005080a8 + 3 + iVar1) >> 0x18 & in_EAX) != 0)))) {
    return CONCAT31((int3)(in_EAX >> 8),1);
  }
  return in_EAX & 0xffffff00;
}
