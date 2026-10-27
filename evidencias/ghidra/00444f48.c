/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00444f48, entrada 00444f48.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00444f48(void)

{
  UnidadeParcial *pUVar1;
  ushort in_AX;
  short extraout_CX;
  int extraout_EDX;
  int iVar2;
  uint uVar3;

  uVar3 = (uint)in_AX;
  FUN_0044357c();
  pUVar1 = tabela_unidades;
  tabela_unidades[uVar3].celula_destino = extraout_CX + 0x100;
  iVar2 = extraout_EDX + uVar3 * 0x114;
  if (in_AX == DAT_00496304) {
    DAT_004e0f36 = 0;
    DAT_004e0f37 = 0;
    DAT_00496304 = 0xffff;
    DAT_004e0f3c = 0;
  }
  pUVar1[uVar3].estado_caminho = 0;
  *(undefined1 *)(iVar2 + 0x89) = 0;
  *(undefined1 *)(iVar2 + 2) = 5;
  *(undefined1 *)(iVar2 + 0x82) = 0;
  *(ushort *)(iVar2 + 0xb2) = CONCAT11((char)((ushort)extraout_CX >> 8) + '\x01',(char)extraout_CX);
  return;
}
