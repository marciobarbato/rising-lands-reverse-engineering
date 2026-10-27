/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void OriginaisSBL::LibereCouleur(void)

{
  byte in_AL;

  if (((DAT_004e1570 != 0xff) && ((&DAT_004e1670)[in_AL] == '\0')) && (in_AL != 0)) {
    DAT_004e1570 = DAT_004e1570 + 1;
    (&DAT_004e1570)[DAT_004e1570] = in_AL;
    (&DAT_004e1670)[in_AL] = 1;
  }
  return;
}
