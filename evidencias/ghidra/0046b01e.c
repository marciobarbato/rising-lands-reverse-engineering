/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0046b01e, entrada 0046b01e.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_0046b01e(void)

{
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 uVar1;
  ushort uVar2;
  ushort local_18;
  ushort local_14;
  ushort local_10;

  FUN_00472555();
  for (uVar2 = 0; uVar2 < 4; uVar2 = uVar2 + 1) {
    (&DAT_004e19bc)[uVar2] = 0x32;
  }
  FUN_00458461(extraout_ECX,2);
  FUN_00458461(extraout_ECX_00,2);
  uVar1 = extraout_ECX_01;
  for (uVar2 = 0; uVar2 < local_14; uVar2 = uVar2 + 1) {
    FUN_00458461(uVar1,2);
    FUN_00458461(tabela_unidades,(uint)local_10);
    tabela_unidades[local_18].selecionada = 0;
    *(undefined4 *)&tabela_unidades[local_18].field_0x110 = 0;
    *(undefined4 *)&tabela_unidades[local_18].field_0x104 = 0xffffffff;
    uVar1 = extraout_ECX_02;
  }
  for (uVar2 = 0; uVar2 < 800; uVar2 = uVar2 + 1) {
    FUN_00458461(uVar1,0x200);
    uVar1 = extraout_ECX_03;
  }
  return;
}
