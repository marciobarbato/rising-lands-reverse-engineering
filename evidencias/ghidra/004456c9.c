/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004456c9, entrada 004456c9.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004456c9(byte param_1)

{
  bool bVar1;
  UnidadeParcial *pUVar2;
  ushort in_AX;
  ushort uVar3;
  undefined2 extraout_var;
  undefined2 unaff_BX;

  pUVar2 = tabela_unidades;
  if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  if ((bVar1) && (tabela_unidades[in_AX].estado = 0x17, in_AX == DAT_00496304)) {
    DAT_004e0f36 = 0;
    DAT_004e0f37 = 0;
    DAT_00496304 = 0xffff;
    DAT_004e0f3c = 0;
  }
  *(ushort *)&pUVar2[in_AX].field_0xc4 = (ushort)param_1;
  *(undefined2 *)&pUVar2[in_AX].field_0xc0 = unaff_BX;
  uVar3 = FUN_0041aee2();
  pUVar2 = tabela_unidades;
  tabela_unidades[CONCAT22(extraout_var,in_AX)].celula_destino = uVar3;
  if (in_AX == DAT_00496304) {
    DAT_004e0f36 = 0;
    DAT_004e0f37 = 0;
    DAT_004e0f3c = 0;
    DAT_00496304 = 0xffff;
  }
  pUVar2[CONCAT22(extraout_var,in_AX)].estado_caminho = 0;
  return;
}
