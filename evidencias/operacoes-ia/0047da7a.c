/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall OriginaisSBL::V_Attendre(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  undefined4 *in_EAX;

  iVar1 = in_EAX[8];
  (&DAT_0051237e)[iVar1 * 0x60] = 1;
  *(undefined4 *)(&DAT_00512334 + iVar1 * 0x60) = *in_EAX;
  return CONCAT44(param_2,1);
}
