/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

longlong __fastcall OriginaisSBL::AlloueCouleur(undefined4 param_1,uint param_2)

{
  byte bVar1;

  if (DAT_004e1570 == 0) {
    return (ulonglong)param_2 << 0x20;
  }
  bVar1 = (&DAT_004e1570)[DAT_004e1570];
  DAT_004e1570 = DAT_004e1570 - 1;
  (&DAT_004e1670)[bVar1] = 0;
  return CONCAT44(param_2,(uint)bVar1);
}
