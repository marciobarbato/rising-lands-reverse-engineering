/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00441a1b, entrada 00441a1b.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00441a1b(void)

{
  int extraout_ECX;
  uint uVar1;
  undefined8 uVar2;

  tabela_unidades = (UnidadeParcial *)FUN_00467ea6();
  DAT_004e199c = FUN_00467ea6();
  for (uVar2 = FUN_00467ea6(); DAT_004e1924 = (int)uVar2,
      uVar1 = (uint)((ulonglong)uVar2 >> 0x20) & 0xffff, uVar1 < 800;
      uVar2 = CONCAT44((int)((ulonglong)uVar2 >> 0x20) + 1,DAT_004e1924)) {
    uVar2 = FUN_00467ea6();
    *(int *)(DAT_004e1924 + uVar1 * 4) = (int)uVar2;
  }
  uVar1 = 0;
  while ((uVar1 & 0xffff) < 0x1b) {
    uVar2 = FUN_00467ea6();
    *(int *)((uVar1 & 0xffff) * 4 + DAT_004e199c) = (int)uVar2;
    uVar1 = (int)((ulonglong)uVar2 >> 0x20) + 1;
  }
  DAT_004e19b8 = FUN_00467ea6();
  uVar1 = 0;
  while ((uVar1 & 0xffff) < 4) {
    uVar2 = FUN_00467ea6();
    *(int *)(DAT_004e19b8 + extraout_ECX * 4) = (int)uVar2;
    uVar1 = (int)((ulonglong)uVar2 >> 0x20) + 1;
  }
  carregar_atributos_tipos();
  FUN_00441659();
  return;
}
