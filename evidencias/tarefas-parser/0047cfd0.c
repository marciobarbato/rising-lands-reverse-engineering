/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0047cfd0(int param_1,int *param_2,int param_3)

{
  undefined4 *in_EAX;
  int unaff_EBX;
  int iVar1;

  in_EAX[1] = unaff_EBX;
  in_EAX[2] = param_1;
  in_EAX[3] = param_2;
  if (param_3 == 0) {
    *in_EAX = 0xffffffff;
  }
  else {
    *in_EAX = 0;
    iVar1 = 0;
    while (iVar1 < unaff_EBX + -1) {
      iVar1 = iVar1 + 1;
      *param_2 = iVar1;
      param_2 = (int *)((int)param_2 + param_1);
    }
    *param_2 = -1;
  }
  return;
}
