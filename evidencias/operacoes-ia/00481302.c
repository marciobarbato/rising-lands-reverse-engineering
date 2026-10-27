/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall OriginaisSBL::I_Divise(undefined4 param_1,undefined4 param_2)

{
  int *in_EAX;
  int iVar1;

  if (in_EAX[1] == 0) {
    iVar1 = -1;
  }
  else {
    iVar1 = *in_EAX / in_EAX[1];
  }
  return CONCAT44(param_2,iVar1);
}
