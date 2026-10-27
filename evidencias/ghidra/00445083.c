/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00445083, entrada 00445083.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00445083(undefined4 param_1,undefined2 param_2)

{
  ushort uVar1;
  UnidadeParcial *pUVar2;
  uint in_EAX;
  uint uVar3;
  int extraout_ECX;
  int extraout_EDX;
  int iVar4;

  uVar3 = in_EAX & 0xffff;
  FUN_0044357c();
  pUVar2 = tabela_unidades;
  uVar1 = tabela_unidades[extraout_ECX].celula_passo;
  tabela_unidades[uVar3].celula_destino = uVar1;
  iVar4 = extraout_EDX + uVar3 * 0x114;
  if ((short)in_EAX == DAT_00496304) {
    DAT_004e0f36 = (byte)in_EAX ^ (byte)DAT_00496304;
    DAT_004e0f37 = (byte)(in_EAX >> 8) ^ (byte)((ushort)DAT_00496304 >> 8);
    DAT_004e0f3c = 0;
    DAT_00496304 = -1;
  }
  pUVar2[uVar3].estado_caminho = 0;
  *(undefined1 *)(iVar4 + 0x88) = 0;
  *(undefined1 *)(iVar4 + 0x89) = 0;
  *(undefined1 *)(iVar4 + 2) = 0xf;
  *(ushort *)(iVar4 + 0xb2) = uVar1;
  *(undefined2 *)(iVar4 + 0xc0) = param_2;
  FUN_00445f27();
  return;
}
