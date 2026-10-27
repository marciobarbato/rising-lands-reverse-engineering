/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00457b87, entrada 00457b87.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00457b87(byte param_1,ushort param_2)

{
  byte bVar1;
  bool bVar2;
  UnidadeParcial *pUVar3;
  UnidadeParcial *pUVar4;
  ushort in_AX;
  ushort uVar5;
  uint uVar6;
  undefined4 extraout_ECX;
  uint extraout_ECX_00;
  int extraout_ECX_01;
  uint extraout_EDX;
  undefined1 unaff_BL;
  longlong lVar7;

  pUVar3 = tabela_unidades;
  tabela_unidades[in_AX].celula_atual = param_2;
  pUVar3[in_AX].celula_passo = param_2;
  pUVar4 = tabela_unidades;
  tabela_unidades[in_AX].celula_destino = param_2;
  if (in_AX == DAT_00496304) {
    DAT_004e0f36 = 0;
    DAT_004e0f37 = 0;
    DAT_004e0f3c = 0;
    DAT_00496304 = 0xffff;
  }
  pUVar4[in_AX].estado_caminho = 0;
  *(undefined2 *)&pUVar3[in_AX].field_0xb2 = 0xffff;
  pUVar3[in_AX].field_0xab = 0;
  pUVar3[in_AX].field_0x97 = 0;
  pUVar3[in_AX].field_0x95 = 0;
  pUVar3[in_AX].field_0x96 = 0;
  pUVar3[in_AX].field_0x92 = 0;
  pUVar3[in_AX].deslocamento_x = 0;
  pUVar3[in_AX].deslocamento_y = 0;
  pUVar3[in_AX].field_0xb6 = 0;
  pUVar3[in_AX].field_0xaa = 0;
  pUVar3[in_AX].field_0x9c = 99;
  pUVar3[in_AX].field_0xa4 = 0;
  pUVar3[in_AX].field_0xa9 = 0;
  pUVar3[in_AX].field_0x9e = 0;
  *(undefined2 *)&pUVar3[in_AX].field_0xb8 = 0xffff;
  *(undefined2 *)&pUVar3[in_AX].field_0x8c = 0;
  pUVar3[in_AX].field_0x8e = 0;
  pUVar3[in_AX].field_0x90 = unaff_BL;
  pUVar3[in_AX].field_0x91 = unaff_BL;
  pUVar3[in_AX].field_0x94 = unaff_BL;
  pUVar3[in_AX].tipo_id = param_1;
  pUVar3[in_AX].estado_caminho = 0;
  pUVar3[in_AX].field_0x8b = 0;
  pUVar3[in_AX].grupo_id = 0;
  pUVar3[in_AX].selecionada = 0;
  if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
    bVar2 = false;
  }
  else {
    bVar2 = true;
  }
  if ((bVar2) && (tabela_unidades[in_AX].estado = 7, in_AX == DAT_00496304)) {
    DAT_004e0f36 = 0;
    DAT_004e0f37 = 0;
    DAT_004e0f3c = 0;
    DAT_00496304 = 0xffff;
  }
  *(undefined2 *)&pUVar3[in_AX].field_0x4 = 4;
  *(undefined2 *)&pUVar3[in_AX].field_0x74 = 0;
  pUVar3[in_AX].raio_visao = (&DAT_004965d8)[(uint)param_1 * 0x32];
  bVar1 = (&DAT_004965da)[(uint)param_1 * 0x32];
  *(undefined2 *)&pUVar3[in_AX].field_0x76 = 4;
  pUVar3[in_AX].field_0x6 = 4;
  *(undefined2 *)&pUVar3[in_AX].field_0xc2 = 0;
  pUVar3[in_AX].field_0x78 = 0;
  pUVar3[in_AX].alcance_quadrado_u8 = bVar1;
  FUN_00457350();
  lVar7 = FUN_004475ac(extraout_ECX,extraout_EDX);
  uVar6 = FUN_00428cc0(extraout_ECX_00,1);
  pUVar4 = tabela_unidades;
  pUVar3 = tabela_unidades + extraout_ECX_01;
  *(undefined2 *)&tabela_unidades[extraout_ECX_01].field_0x70 = 0;
  *(undefined2 *)&pUVar4[extraout_ECX_01].field_0xe = 0;
  pUVar4[extraout_ECX_01].campo_0c = 0;
  pUVar3->campo_0a = 0;
  for (uVar5 = 0; uVar5 < 0x1e; uVar5 = uVar5 + 1) {
    *(undefined2 *)(&pUVar4[extraout_ECX_01].field_0x10 + (uint)uVar5 * 2) = 0;
    (&pUVar4[extraout_ECX_01].field_0x4c)[uVar5] = 0;
  }
  pUVar4[extraout_ECX_01].campo_0c = (short)lVar7 + (short)uVar6;
  return;
}
