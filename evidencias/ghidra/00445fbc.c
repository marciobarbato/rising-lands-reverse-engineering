/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00445fbc, entrada 00445fbc.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00445fbc(undefined4 param_1,ushort param_2)

{
  bool bVar1;
  UnidadeParcial *pUVar2;
  ushort in_AX;
  int extraout_ECX;
  int extraout_ECX_00;
  UnidadeParcial *extraout_ECX_01;
  UnidadeParcial *pUVar3;

  pUVar3 = tabela_unidades;
  tabela_unidades[in_AX].celula_destino = param_2;
  pUVar3[in_AX].celula_passo = param_2;
  pUVar3[in_AX].celula_atual = param_2;
  pUVar2 = tabela_unidades;
  tabela_unidades[in_AX].celula_destino = param_2;
  if (in_AX == DAT_00496304) {
    DAT_004e0f36 = 0;
    DAT_004e0f37 = 0;
    DAT_00496304 = 0xffff;
    DAT_004e0f3c = 0;
  }
  pUVar2[in_AX].estado_caminho = 0;
  if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  if ((bVar1) && (tabela_unidades[in_AX].estado = 7, in_AX == DAT_00496304)) {
    DAT_004e0f36 = 0;
    DAT_004e0f37 = 0;
    DAT_004e0f3c = 0;
    DAT_00496304 = 0xffff;
  }
  *(undefined2 *)&pUVar3[in_AX].field_0xc0 = 0xffff;
  *(undefined2 *)&pUVar3[in_AX].field_0xb8 = 0xffff;
  pUVar3[in_AX].deslocamento_y = 0;
  pUVar3[in_AX].deslocamento_x = pUVar3[in_AX].deslocamento_y;
  FUN_00442cb4(tabela_unidades);
  *(undefined1 *)(extraout_ECX + 0x72 + (uint)in_AX * 0x114) = 1;
  pUVar3 = tabela_unidades + in_AX;
  if ((pUVar3->proprietario_id != 200) && (pUVar3->proprietario_id != 4)) {
    FUN_00476851(pUVar3,(uint)(ushort)((ushort)(byte)pUVar3->field_0xf5 + pUVar3->raio_visao + 2));
    FUN_00476cb3(extraout_ECX_00,
                 (uint)(ushort)((ushort)*(byte *)(extraout_ECX_00 + 0xf5) +
                               (ushort)*(byte *)(extraout_ECX_00 + 0xbb)));
    pUVar3 = extraout_ECX_01;
  }
  FUN_0046a388(pUVar3,4);
  return;
}
