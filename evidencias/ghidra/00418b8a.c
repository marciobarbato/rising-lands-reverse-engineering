/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00418b8a, entrada 00418b8a.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_00418b8a(undefined4 param_1,byte param_2)

{
  byte bVar1;
  undefined4 in_EAX;
  ushort uVar2;
  byte unaff_BL;

  bVar1 = (byte)in_EAX;
  if (9 < bVar1) {
    uVar2 = (ushort)((uint)in_EAX >> 0x10);
    if (bVar1 < 0xb) {
      if (param_2 != 0) {
        if (param_2 < 2) {
          return (uint)(byte)(&DAT_004dfb80)[unaff_BL];
        }
        if (param_2 == 3) {
          return CONCAT31((int3)(((uint)uVar2 << 0x10) >> 8),DAT_004dfb9a);
        }
        return 0;
      }
    }
    else if ((bVar1 == 0xb) && (param_2 != 0)) {
      if (param_2 < 2) {
        return (uint)(byte)(&DAT_004dfb64)[unaff_BL];
      }
      if (param_2 == 3) {
        return CONCAT31((int3)(((uint)uVar2 << 0x10) >> 8),DAT_004dfb7e);
      }
      return 0;
    }
  }
  return 0;
}
