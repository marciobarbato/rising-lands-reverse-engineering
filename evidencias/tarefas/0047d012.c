/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_0047d012(undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  int *in_EAX;
  int *piVar2;

  iVar1 = *in_EAX;
  if (iVar1 != -1) {
    piVar2 = (int *)(in_EAX[2] * iVar1 + in_EAX[3]);
    *in_EAX = *piVar2;
    *piVar2 = -1;
    in_EAX[1] = in_EAX[1] + -1;
  }
  return CONCAT44(param_2,iVar1);
}
