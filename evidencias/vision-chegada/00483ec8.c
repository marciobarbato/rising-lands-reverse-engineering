/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::iagMessDispatchWith(undefined4 param_1,undefined2 param_2)

{
  uint in_EAX;

  if ((in_EAX & 0x7ffffff) != 0x7fd72b1) {
    (&DAT_0051a9f6)[in_EAX * 0x10] = param_2;
  }
  return;
}
