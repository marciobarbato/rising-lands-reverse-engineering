/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00472648, entrada 00472648.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00472648(undefined4 param_1)

{
  byte bVar1;
  ushort in_AX;
  undefined4 extraout_ECX;
  undefined4 extraout_EDX;

  if (tabela_unidades[in_AX].selecionada != 0) {
    tabela_unidades[in_AX].selecionada = 0;
    bVar1 = unidade_obter_proprietario(in_AX);
    FUN_00472576(extraout_ECX,CONCAT31((int3)((uint)extraout_EDX >> 8),bVar1));
  }
  return;
}
