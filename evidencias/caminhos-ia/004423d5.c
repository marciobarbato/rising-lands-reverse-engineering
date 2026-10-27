/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined1 FUN_004423d5(void)

{
  byte in_AL;
  bool bVar1;

  if (in_AL < 0x10) {
    if (0xb < in_AL) {
      return 0;
    }
    if (in_AL < 3) {
      return 1;
    }
    if (in_AL < 4) {
      return 0;
    }
    bVar1 = in_AL == 0xb;
  }
  else {
    if (in_AL < 0x12) {
      return 0;
    }
    if (in_AL < 0x17) {
      if (in_AL < 0x14) {
        return 1;
      }
      if (in_AL < 0x15) {
        return 0;
      }
      bVar1 = in_AL == 0x15;
    }
    else {
      if (in_AL < 0x18) {
        return 0;
      }
      if (in_AL < 0x19) {
        return 0;
      }
      bVar1 = in_AL == 0x19;
    }
  }
  if (bVar1) {
    return 0;
  }
  return 1;
}
