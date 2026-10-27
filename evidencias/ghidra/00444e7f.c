/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00444e7f, entrada 00444e7f.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00444e7f(undefined4 param_1,undefined2 param_2)

{
  UnidadeParcial *pUVar1;
  ushort in_AX;
  uint uVar2;

  pUVar1 = tabela_unidades;
  uVar2 = (uint)in_AX;
  tabela_unidades[uVar2].estado = 0x12;
  pUVar1[uVar2].field_0x89 = 0;
  *(undefined2 *)&pUVar1[uVar2].field_0xb2 = param_2;
  FUN_00443222(param_2,uVar2 * 0x114);
  return;
}
