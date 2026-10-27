/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00445f2d, entrada 00445f2d.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00445f2d(undefined4 param_1,ushort param_2)

{
  UnidadeParcial *pUVar1;
  ushort in_AX;

  pUVar1 = tabela_unidades;
  tabela_unidades[in_AX].celula_destino = tabela_unidades[param_2].celula_atual;
  if (in_AX == DAT_00496304) {
    DAT_004e0f36 = 0;
    DAT_004e0f37 = 0;
    DAT_00496304 = 0xffff;
    DAT_004e0f3c = 0;
  }
  pUVar1[in_AX].estado_caminho = 0;
  *(undefined2 *)&pUVar1[in_AX].field_0xc0 = 0xffff;
  pUVar1[in_AX].estado = 0xd;
  *(ushort *)&pUVar1[in_AX].field_0xb8 = param_2;
  return;
}
