/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined1 FUN_00442409(void)

{
  byte in_AL;

  if ((in_AL < 0xc) || ((0xc < in_AL && (in_AL != 0xf)))) {
    return 0;
  }
  return 1;
}
