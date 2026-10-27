/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::iaProbSleep(undefined4 param_1,undefined4 param_2)

{
  int in_EAX;

  (&DAT_0051237e)[in_EAX * 0x60] = 1;
  *(undefined4 *)(&DAT_00512334 + in_EAX * 0x60) = param_2;
  return;
}
