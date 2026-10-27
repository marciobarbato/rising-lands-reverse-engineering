/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00440c5d, entrada 00440c5d.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00440c5d(undefined4 param_1,undefined4 param_2)

{
  uint in_EAX;
  int iVar1;
  undefined4 extraout_ECX;
  uint uVar2;

  iVar1 = FUN_00479555(tabela_unidades[in_EAX & 0xffff].celula_atual / 0x100,
                       DAT_00508726 / 2 + DAT_00508722);
  uVar2 = 0;
  if (iVar1 < 0x92) {
    uVar2 = 0x100;
  }
  else if ((iVar1 < 0x92) || (300 < iVar1)) {
    if ((300 < iVar1) && (iVar1 < 600)) {
      uVar2 = 100;
    }
  }
  else {
    uVar2 = 0xb4;
  }
  iVar1 = FUN_00472174(extraout_ECX,in_EAX & 0xffff);
  if ((char)iVar1 == '\0') {
    uVar2 = uVar2 / 2;
  }
  return CONCAT44(param_2,uVar2);
}
