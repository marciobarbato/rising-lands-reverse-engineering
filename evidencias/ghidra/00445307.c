/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00445307, entrada 00445307.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00445307(undefined4 param_1,ushort param_2)

{
  ushort uVar1;
  UnidadeParcial *pUVar2;
  uint in_EAX;
  uint uVar3;
  short extraout_CX;
  int extraout_EDX;

  pUVar2 = tabela_unidades;
  uVar3 = in_EAX & 0xffff;
  if (tabela_unidades[uVar3].estado == 0x16) {
    uVar1 = *(ushort *)&tabela_unidades[uVar3].field_0xd8;
    if (uVar1 < 10) {
      *(ushort *)&tabela_unidades[uVar3].field_0xd8 = uVar1 + 1;
      *(ushort *)(&pUVar2[uVar3].field_0xc4 + (uint)uVar1 * 2) = param_2;
      return;
    }
  }
  else {
    FUN_0044357c();
    pUVar2 = tabela_unidades;
    tabela_unidades[uVar3].celula_destino = param_2;
    if (extraout_CX == DAT_00496304) {
      DAT_004e0f36 = 0;
      DAT_004e0f37 = 0;
      DAT_00496304 = -1;
      DAT_004e0f3c = 0;
    }
    pUVar2[uVar3].estado_caminho = 0;
    *(undefined1 *)(extraout_EDX + 0x88) = 0;
    *(undefined1 *)(extraout_EDX + 0x89) = 0;
    *(undefined1 *)(extraout_EDX + 2) = 0x16;
    *(undefined2 *)(extraout_EDX + 0xd8) = 0;
    *(ushort *)(extraout_EDX + 0xb2) = param_2;
  }
  return;
}
