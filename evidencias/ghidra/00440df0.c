/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00440df0, entrada 00440df0.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00440df0(undefined4 param_1,undefined4 param_2)

{
  ushort in_AX;

  return CONCAT44(param_2,CONCAT22((short)((uint)tabela_unidades >> 0x10),
                                   tabela_unidades[in_AX].celula_atual));
}
