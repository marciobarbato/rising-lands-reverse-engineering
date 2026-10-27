/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004454ce, entrada 004454ce.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004454ce(undefined4 param_1,char param_2)

{
  ushort uVar1;
  UnidadeParcial *pUVar2;
  char cVar3;
  ushort in_AX;
  undefined4 uVar4;
  int extraout_ECX;
  int extraout_ECX_00;
  int extraout_ECX_01;
  int iVar5;
  ushort unaff_BX;
  ushort local_1c;
  ushort local_18 [2];
  char local_14;

  local_14 = param_2;
  FUN_0041a996(tabela_unidades + in_AX,local_18);
  cVar3 = local_14;
  pUVar2 = tabela_unidades;
  if ((*(char *)(extraout_ECX + 2) == '\v') && (*(char *)(extraout_ECX + 0xbe) == '\t')) {
    uVar1 = *(ushort *)&tabela_unidades[in_AX].field_0xd8;
    if (uVar1 < 10) {
      *(ushort *)&tabela_unidades[in_AX].field_0xd8 = uVar1 + 1;
      *(ushort *)(&pUVar2[in_AX].field_0xc4 + (uint)uVar1 * 2) = unaff_BX;
    }
  }
  else {
    FUN_0044357c();
    iVar5 = extraout_ECX_00;
    if ((cVar3 != '\t') && (cVar3 != '\f')) {
      uVar4 = FUN_0041aea4();
      unaff_BX = (unaff_BX +
                 (local_18[0] - local_18[0] / 2) * 0x100 + (local_1c - local_1c / 2) + -0x101) -
                 (short)uVar4;
      iVar5 = extraout_ECX_01;
    }
    pUVar2 = tabela_unidades;
    tabela_unidades[in_AX].celula_destino = unaff_BX;
    if (in_AX == DAT_00496304) {
      DAT_004e0f36 = 0;
      DAT_004e0f37 = 0;
      DAT_00496304 = 0xffff;
      DAT_004e0f3c = 0;
    }
    pUVar2[in_AX].estado_caminho = 0;
    *(undefined1 *)(iVar5 + 0x88) = 0;
    *(undefined1 *)(iVar5 + 0x89) = 0;
    *(undefined2 *)(iVar5 + 0xc0) = 0xffff;
    *(char *)(iVar5 + 0xbe) = local_14;
    *(undefined1 *)(iVar5 + 2) = 0xb;
    *(ushort *)(iVar5 + 0xb2) = unaff_BX;
    if (local_14 == '\t') {
      *(undefined2 *)(iVar5 + 0xd8) = 0;
    }
  }
  return;
}
