/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0041209d, entrada 0041209d.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0041209d(undefined4 param_1,int param_2)

{
  UnidadeParcial *pUVar1;
  byte bVar2;
  ushort in_AX;
  short unaff_BX;

  pUVar1 = tabela_unidades;
  bVar2 = tabela_unidades[in_AX].field_0xab;
  if ((((bVar2 < 0x23) || ((0x22 < bVar2 && (bVar2 < 0x28)))) ||
      ((0x27 < (byte)tabela_unidades[in_AX].field_0xab &&
       ((byte)tabela_unidades[in_AX].field_0xab < 0x2d)))) ||
     (0x2c < (byte)tabela_unidades[in_AX].field_0xab)) {
    FUN_0045b796('\x01',unaff_BX + 199);
  }
  if (pUVar1[in_AX].field_0xae == '\0') {
    bVar2 = unidade_obter_proprietario(in_AX);
    FUN_0045c455('\x01',(unaff_BX + 0xb8) - (ushort)(byte)pUVar1[in_AX].field_0xab,bVar2);
    bVar2 = pUVar1[in_AX].field_0xab;
  }
  else {
    bVar2 = unidade_obter_proprietario(in_AX);
    FUN_0045c455('\x01',(unaff_BX + 0xb8) - (ushort)(byte)pUVar1[in_AX].field_0xab,bVar2);
    bVar2 = pUVar1[in_AX].field_0xab;
  }
  FUN_0045b247('\x01',unaff_BX - (ushort)bVar2);
  bVar2 = unidade_obter_proprietario(in_AX);
  FUN_0045c455('\x01',(unaff_BX + 0xf) - (ushort)(byte)pUVar1[in_AX].field_0xab,bVar2);
  return;
}
