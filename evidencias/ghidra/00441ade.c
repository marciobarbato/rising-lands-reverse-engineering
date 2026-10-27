/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00441ade, entrada 00441ade.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00441ade(void)

{
  uint uVar1;
  uint extraout_EDX;
  uint extraout_EDX_00;
  uint extraout_EDX_01;

  uVar1 = 0;
  while ((uVar1 & 0xffff) < 4) {
    FUN_00467ecb();
    uVar1 = extraout_EDX;
  }
  FUN_00467ecb();
  uVar1 = 0;
  while ((uVar1 & 0xffff) < 0x1b) {
    FUN_00467ecb();
    uVar1 = extraout_EDX_00;
  }
  uVar1 = 0;
  while ((uVar1 & 0xffff) < 800) {
    FUN_00467ecb();
    uVar1 = extraout_EDX_01;
  }
  FUN_00467ecb();
  FUN_00467ecb();
  FUN_00467ecb();
  return;
}
