/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_0043ec0c(undefined4 param_1,byte param_2)

{
  uint in_EAX;
  uint uVar1;

  uVar1 = in_EAX & 0xffff;
  if (*(char *)(DAT_00507d74 + uVar1) == -3) {
    return CONCAT31((int3)(uVar1 >> 8),(param_2 & 1) != 0);
  }
  return (uint)((*(byte *)(uVar1 + DAT_00507da8) & param_2) != 0);
}
