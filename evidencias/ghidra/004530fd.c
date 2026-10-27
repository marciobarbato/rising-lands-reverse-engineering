/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004530fd, entrada 004530fd.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_004530fd(void)

{
  UnidadeParcial *pUVar1;
  ushort in_AX;

  pUVar1 = tabela_unidades;
  *(undefined2 *)&tabela_unidades[in_AX].field_0x74 = 0;
  *(undefined2 *)&pUVar1[in_AX].field_0x4 = *(undefined2 *)&pUVar1[in_AX].field_0x76;
  return;
}
