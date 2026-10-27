/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall FUN_0047d11a(undefined4 param_1,int param_2)

{
  int iVar1;
  int *in_EAX;
  int iVar2;
  int iVar3;
  int *piVar4;

  piVar4 = (int *)(in_EAX[3] + in_EAX[2] * param_2);
  iVar1 = *in_EAX;
  iVar3 = -1;
  while( true ) {
    iVar2 = iVar1;
    if (iVar2 == -1) {
      return -1;
    }
    if (iVar2 == param_2) break;
    iVar1 = *(int *)(in_EAX[3] + in_EAX[2] * iVar2);
    iVar3 = iVar2;
  }
  if (iVar3 == -1) {
    *in_EAX = *piVar4;
  }
  else {
    *(int *)(in_EAX[3] + in_EAX[2] * iVar3) = *piVar4;
  }
  in_EAX[1] = in_EAX[1] + -1;
  return iVar2;
}
