/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0048d890(uint param_1,uint param_2)

{
  undefined1 *in_EAX;
  undefined1 *puVar1;
  uint uVar2;
  undefined1 uVar3;
  undefined6 uVar4;

  if (param_1 != 0) {
    do {
      if (((uint)in_EAX & 3) == 0) break;
      *in_EAX = (char)param_2;
      in_EAX = in_EAX + 1;
      param_2 = param_2 >> 8 | param_2 << 0x18;
      param_1 = param_1 - 1;
    } while (param_1 != 0);
    uVar4 = FUN_0048d8c7(param_1 >> 2,param_2);
    puVar1 = (undefined1 *)uVar4;
    uVar2 = param_1 & 3;
    if (uVar2 != 0) {
      uVar3 = (undefined1)((uint6)uVar4 >> 0x20);
      *puVar1 = uVar3;
      if ((uVar2 != 1) && (puVar1[1] = (char)((uint6)uVar4 >> 0x28), uVar2 != 2)) {
        puVar1[2] = uVar3;
      }
    }
  }
  return;
}
