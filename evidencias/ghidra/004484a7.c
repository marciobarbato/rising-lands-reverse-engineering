/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004484a7, entrada 004484a7.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_004484a7(void)

{
  bool bVar1;
  UnidadeParcial *pUVar2;
  ushort in_AX;
  byte bVar3;
  char cVar4;

  pUVar2 = tabela_unidades;
  bVar3 = tabela_unidades[in_AX].tipo_id;
  if ((bVar3 < 0xc) || ((0xc < bVar3 && (bVar3 != 0xf)))) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  if (((bVar1) && (tabela_unidades[in_AX].field_0xda != tabela_unidades[in_AX].field_0x94)) &&
     (bVar3 = tabela_unidades[in_AX].field_0x96 + 1, tabela_unidades[in_AX].field_0x96 = bVar3,
     bVar3 == pUVar2[in_AX].periodo_giro)) {
    if ((((byte)pUVar2[in_AX].field_0x94 < (byte)pUVar2[in_AX].field_0xda) &&
        ((int)((uint)(byte)pUVar2[in_AX].field_0xda - (uint)(byte)pUVar2[in_AX].field_0x94) < 0x10))
       || (((byte)pUVar2[in_AX].field_0xda < (byte)pUVar2[in_AX].field_0x94 &&
           (0x10 < (int)((uint)(byte)pUVar2[in_AX].field_0x94 - (uint)(byte)pUVar2[in_AX].field_0xda
                        ))))) {
      cVar4 = (byte)pUVar2[in_AX].field_0x94 % 0x20 + 1;
    }
    else if (pUVar2[in_AX].field_0x94 == '\x01') {
      cVar4 = ' ';
    }
    else {
      cVar4 = pUVar2[in_AX].field_0x94 + -1;
    }
    pUVar2[in_AX].field_0x94 = cVar4;
    pUVar2[in_AX].field_0x96 = 0;
  }
  return;
}
