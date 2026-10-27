/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00440e31, entrada 00440e31.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00440e31(undefined4 param_1,undefined4 param_2)

{
  ushort in_AX;

  return CONCAT44(param_2,CONCAT31((int3)((uint)tabela_unidades >> 8),
                                   tabela_unidades[in_AX].field_0x94));
}
