/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00445a36, entrada 00445a36.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00445a36(undefined4 param_1,char param_2)

{
  char cVar1;
  ushort in_AX;
  byte extraout_CL;
  int extraout_EDX;
  ushort unaff_BX;

  if (((tabela_unidades[in_AX].estado != 1) || (param_2 != tabela_unidades[in_AX].field_0xb7)) ||
     (unaff_BX != *(ushort *)&tabela_unidades[in_AX].field_0xb8)) {
    FUN_0044357c();
    cVar1 = *(char *)(extraout_EDX + 1);
    if (((cVar1 != '\a') && (cVar1 != '\x06')) &&
       ((cVar1 != '\x05' && ((cVar1 != '\r' && (cVar1 != '\t')))))) {
      if (cVar1 == '\n') {
        return;
      }
      if (extraout_CL < 3) {
        if (extraout_CL != 1) {
          return;
        }
        if (in_AX == unaff_BX) {
          return;
        }
        *(undefined1 *)(extraout_EDX + 0x8a) = 0;
        *(undefined1 *)(extraout_EDX + 2) = 1;
      }
      else {
        if ((3 < extraout_CL) && (extraout_CL != 5)) {
          return;
        }
        *(undefined1 *)(extraout_EDX + 2) = 1;
        *(undefined1 *)(extraout_EDX + 0x8a) = 0;
      }
      *(byte *)(extraout_EDX + 0xb7) = extraout_CL;
      *(ushort *)(extraout_EDX + 0xb8) = unaff_BX;
      return;
    }
  }
  return;
}
