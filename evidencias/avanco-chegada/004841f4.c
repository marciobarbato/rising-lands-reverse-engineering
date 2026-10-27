/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::iagMessSetWait(undefined4 param_1,uint param_2)

{
  undefined4 in_EAX;
  undefined4 unaff_EBX;

  if ((param_2 & 0x7ffffff) != 0x7fd72b1) {
    (&DAT_0051a9fc)[param_2 * 8] = unaff_EBX;
    (&DAT_0051a9e8)[param_2 * 8] = in_EAX;
    func_0x0047da39(param_1);
  }
  return;
}
