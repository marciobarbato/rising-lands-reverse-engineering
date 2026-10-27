/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004570f4, entrada 004570f4.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004570f4(undefined4 param_1,byte param_2)

{
  UnidadeParcial *pUVar1;
  ushort in_AX;

  pUVar1 = tabela_unidades;
  tabela_unidades[in_AX].direcao_desejada = param_2;
  pUVar1[in_AX].orientacao_atual = param_2;
  return;
}
