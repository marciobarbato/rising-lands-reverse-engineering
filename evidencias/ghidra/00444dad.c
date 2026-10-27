/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00444dad, entrada 00444dad.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00444dad(byte param_1,undefined1 param_2)

{
  UnidadeParcial *pUVar1;
  ushort in_AX;
  undefined2 unaff_BX;

  pUVar1 = tabela_unidades;
  tabela_unidades[in_AX].field_0x82 = param_2;
  *(undefined2 *)&pUVar1[in_AX].field_0x80 = unaff_BX;
  *(ushort *)&pUVar1[in_AX].field_0x84 = (ushort)param_1;
  return;
}
