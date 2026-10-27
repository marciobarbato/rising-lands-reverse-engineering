/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0046b119, entrada 0046b119.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0046b119(undefined4 param_1)

{
  ushort uVar1;
  bool bVar2;
  uint extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 uVar3;

  for (uVar1 = 0; uVar1 < 800; uVar1 = uVar1 + 1) {
    unidade_esta_ativa(uVar1);
  }
  FUN_00458476(0x114,2);
  FUN_00458476(extraout_ECX,2);
  uVar3 = extraout_ECX_00;
  for (uVar1 = 0; uVar1 < 800; uVar1 = uVar1 + 1) {
    bVar2 = unidade_esta_ativa(uVar1);
    uVar3 = extraout_ECX_01;
    if (bVar2) {
      FUN_00458476(extraout_ECX_01,2);
      FUN_00458476(extraout_ECX_02,extraout_ECX & 0xffff);
      uVar3 = extraout_ECX_03;
    }
  }
  for (uVar1 = 0; uVar1 < 800; uVar1 = uVar1 + 1) {
    FUN_00458476(uVar3,0x200);
    uVar3 = extraout_ECX_04;
  }
  return;
}
