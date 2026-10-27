/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00483825, entrada 00483825.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00483825(undefined4 param_1,undefined4 param_2)

{
  uint uVar1;

  uVar1 = (uint)DAT_0051b848;
  DAT_0051b848 = *(ushort *)&tabela_unidades[uVar1].field_0x108;
  uVar1 = (uint)*(ushort *)&tabela_unidades[uVar1].field_0x108;
  if (uVar1 == 0xffff) {
    uVar1 = 0xffff;
  }
  return CONCAT44(param_2,uVar1);
}
