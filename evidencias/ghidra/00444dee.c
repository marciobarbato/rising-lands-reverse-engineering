/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00444dee, entrada 00444dee.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00444dee(undefined4 param_1,undefined2 param_2)

{
  UnidadeParcial *pUVar1;
  ushort in_AX;
  undefined2 uVar2;
  short extraout_CX;
  uint uVar3;
  int extraout_EDX;
  int iVar4;

  pUVar1 = tabela_unidades;
  uVar3 = (uint)in_AX;
  iVar4 = uVar3 * 0x114;
  tabela_unidades[uVar3].estado = 0x14;
  pUVar1[uVar3].field_0x89 = 0;
  uVar2 = FUN_0041aee2();
  *(undefined2 *)(extraout_EDX + 0xb2 + iVar4) = uVar2;
  *(undefined2 *)(extraout_EDX + 0xc0 + iVar4) = param_2;
  pUVar1 = tabela_unidades;
  tabela_unidades[uVar3].celula_destino = *(ushort *)(extraout_EDX + 0xb2 + iVar4);
  if (extraout_CX == DAT_00496304) {
    DAT_004e0f36 = 0;
    DAT_004e0f37 = 0;
    DAT_00496304 = -1;
    DAT_004e0f3c = 0;
  }
  pUVar1[uVar3].estado_caminho = 0;
  return;
}
