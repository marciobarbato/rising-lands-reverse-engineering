/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall FUN_0047d07a(undefined4 param_1,int param_2)

{
  int iVar1;
  int *in_EAX;
  int iVar2;
  int iVar3;
  int iVar4;

  if (param_2 == -1) {
    return -1;
  }
  iVar3 = *in_EAX;
  if (iVar3 != -1) {
    iVar4 = in_EAX[2] * iVar3;
    iVar2 = in_EAX[3];
    while (iVar1 = *(int *)(iVar2 + iVar4), iVar1 != -1) {
      iVar4 = in_EAX[3];
      iVar3 = iVar1;
      iVar2 = in_EAX[2] * iVar1;
    }
  }
  if (iVar3 == -1) {
    *in_EAX = param_2;
  }
  else {
    *(int *)(in_EAX[3] + in_EAX[2] * iVar3) = param_2;
  }
  *(undefined4 *)(in_EAX[2] * param_2 + in_EAX[3]) = 0xffffffff;
  in_EAX[1] = in_EAX[1] + 1;
  return param_2;
}
