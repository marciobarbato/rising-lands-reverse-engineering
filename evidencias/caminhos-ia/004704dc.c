/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_004704dc(undefined4 param_1,undefined4 param_2)

{
  DAT_00497164 = (DAT_00497164 % 0x1f31d) * 0x41a7 + (DAT_00497164 / 0x1f31d) * -0xb14;
  if ((int)DAT_00497164 < 1) {
    DAT_00497164 = DAT_00497164 + 0x7fffffff;
  }
  return CONCAT44(param_2,DAT_00497164);
}
