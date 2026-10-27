/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044115f, entrada 0044115f.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0044115f(undefined4 param_1,byte param_2)

{
  bool bVar1;
  ushort in_AX;

  if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  if ((bVar1) && (tabela_unidades[in_AX].estado = param_2, in_AX == DAT_00496304)) {
    DAT_004e0f36 = 0;
    DAT_004e0f37 = 0;
    DAT_004e0f3c = 0;
    DAT_00496304 = 0xffff;
  }
  return;
}
