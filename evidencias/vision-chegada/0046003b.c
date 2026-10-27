/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined1 OriginaisSBL::PlayerGetColor(void)

{
  uint in_EAX;

  if ((in_EAX & 0xff) == 200) {
    return 0x1e;
  }
  return (&DAT_004e24dc)[in_EAX & 0xff];
}
