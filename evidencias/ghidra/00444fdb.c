/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00444fdb, entrada 00444fdb.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00444fdb(void)

{
  UnidadeParcial *pUVar1;
  ushort in_AX;
  ushort uVar2;
  undefined2 extraout_CX;
  int extraout_EDX;
  int iVar3;
  uint uVar4;

  uVar4 = (uint)in_AX;
  FUN_0044357c();
  uVar2 = FUN_0041aee2();
  pUVar1 = tabela_unidades;
  tabela_unidades[uVar4].celula_destino = uVar2;
  iVar3 = extraout_EDX + uVar4 * 0x114;
  if (in_AX == DAT_00496304) {
    DAT_004e0f36 = 0;
    DAT_004e0f37 = 0;
    DAT_00496304 = 0xffff;
    DAT_004e0f3c = 0;
  }
  pUVar1[uVar4].estado_caminho = 0;
  *(undefined1 *)(iVar3 + 0x88) = 0;
  *(undefined1 *)(iVar3 + 0x89) = 0;
  *(undefined1 *)(iVar3 + 2) = 0xf;
  *(undefined2 *)(iVar3 + 0xc0) = extraout_CX;
  *(ushort *)(iVar3 + 0xb2) = uVar2;
  return;
}
