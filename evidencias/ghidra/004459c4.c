/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004459c4, entrada 004459c4.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004459c4(undefined4 param_1,undefined1 param_2)

{
  short in_AX;
  short extraout_CX;
  int extraout_EDX;
  byte unaff_BL;

  FUN_0044357c();
  if ((*(char *)(extraout_EDX + 1) == '\x04') &&
     (*(undefined1 *)(extraout_EDX + 0xf4) = param_2, unaff_BL != 0)) {
    if (unaff_BL < 2) {
      if (in_AX == extraout_CX) {
        return;
      }
    }
    else if (unaff_BL != 5) {
      return;
    }
    *(undefined1 *)(extraout_EDX + 2) = 0x18;
    *(undefined1 *)(extraout_EDX + 0x8a) = 0;
    *(byte *)(extraout_EDX + 0xb7) = unaff_BL;
    *(short *)(extraout_EDX + 0xb8) = extraout_CX;
  }
  return;
}
