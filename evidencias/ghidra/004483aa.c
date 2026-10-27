/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004483aa, entrada 004483aa.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_004483aa(void)

{
  ushort in_AX;

  tabela_unidades[in_AX].field_0xda = tabela_unidades[in_AX].field_0xda + '\x01';
  if (4 < (byte)tabela_unidades[in_AX].field_0xda) {
    tabela_unidades[in_AX].field_0xda = 5;
  }
  return;
}
