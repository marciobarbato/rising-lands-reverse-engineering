/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::BatimentTailleGet(undefined4 param_1,undefined2 *param_2)

{
  undefined2 *in_EAX;
  uint unaff_EBX;

  *in_EAX = *(undefined2 *)(&DAT_00495d8c + (unaff_EBX & 0xff) * 0x34);
  *param_2 = *(undefined2 *)(&DAT_00495d8e + (unaff_EBX & 0xff) * 0x34);
  return;
}
