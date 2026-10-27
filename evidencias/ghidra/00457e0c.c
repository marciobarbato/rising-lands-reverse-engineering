/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00457e0c, entrada 00457e0c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00457e0c(undefined4 param_1,undefined4 param_2)

{
  uint uVar1;

  uVar1 = 0;
  while (((uVar1 & 0xffff) < 800 && (tabela_unidades[uVar1 & 0xffff].estado != 0))) {
    uVar1 = uVar1 + 1;
  }
  return CONCAT44(param_2,CONCAT31((int3)(uVar1 >> 8),(uVar1 & 0xffff) != 800));
}
