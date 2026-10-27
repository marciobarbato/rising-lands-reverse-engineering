/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0048d8c7(uint param_1,undefined4 param_2)

{
  undefined4 *in_EAX;
  undefined4 *puVar1;
  int iVar2;
  uint uVar3;

  if (param_1 != 0) {
    do {
      if (((uint)in_EAX & 0x1f) == 0) break;
      *in_EAX = param_2;
      in_EAX = in_EAX + 1;
      param_1 = param_1 - 1;
    } while (param_1 != 0);
    if (param_1 >> 2 != 0) {
      iVar2 = (param_1 >> 2) - 1;
      if (iVar2 != 0) {
        do {
          puVar1 = in_EAX;
          *puVar1 = param_2;
          puVar1[1] = param_2;
          puVar1[2] = param_2;
          puVar1[3] = param_2;
          if (iVar2 == 1) goto LAB_0048d906;
          puVar1[4] = param_2;
          puVar1[5] = param_2;
          iVar2 = iVar2 + -2;
          puVar1[6] = param_2;
          puVar1[7] = param_2;
          in_EAX = puVar1 + 8;
        } while (iVar2 != 0);
        puVar1 = puVar1 + 4;
LAB_0048d906:
        in_EAX = puVar1 + 4;
      }
      *in_EAX = param_2;
      in_EAX[1] = param_2;
      in_EAX[2] = param_2;
      in_EAX[3] = param_2;
      in_EAX = in_EAX + 4;
    }
    uVar3 = param_1 & 3;
    if (uVar3 != 0) {
      *in_EAX = param_2;
      if (uVar3 != 1) {
        in_EAX[1] = param_2;
        if (uVar3 != 2) {
          in_EAX[2] = param_2;
        }
      }
    }
  }
  return;
}
