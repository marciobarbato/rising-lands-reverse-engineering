/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004484a7, entrada 004484a7.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_004484a7(void)

{
  byte bVar1;
  bool bVar2;
  UnidadeParcial *pUVar3;
  ushort in_AX;
  char cVar4;

  pUVar3 = tabela_unidades;
  bVar1 = tabela_unidades[in_AX].tipo_id;
  if ((bVar1 < 0xc) || ((0xc < bVar1 && (bVar1 != 0xf)))) {
    bVar2 = false;
  }
  else {
    bVar2 = true;
  }
  if (((bVar2) && (tabela_unidades[in_AX].field_0xda != tabela_unidades[in_AX].field_0x94)) &&
     (cVar4 = tabela_unidades[in_AX].field_0x96 + '\x01', tabela_unidades[in_AX].field_0x96 = cVar4,
     cVar4 == pUVar3[in_AX].field_0x93)) {
    if ((((byte)pUVar3[in_AX].field_0x94 < (byte)pUVar3[in_AX].field_0xda) &&
        ((int)((uint)(byte)pUVar3[in_AX].field_0xda - (uint)(byte)pUVar3[in_AX].field_0x94) < 0x10))
       || (((byte)pUVar3[in_AX].field_0xda < (byte)pUVar3[in_AX].field_0x94 &&
           (0x10 < (int)((uint)(byte)pUVar3[in_AX].field_0x94 - (uint)(byte)pUVar3[in_AX].field_0xda
                        ))))) {
      cVar4 = (byte)pUVar3[in_AX].field_0x94 % 0x20 + 1;
    }
    else if (pUVar3[in_AX].field_0x94 == '\x01') {
      cVar4 = ' ';
    }
    else {
      cVar4 = pUVar3[in_AX].field_0x94 + -1;
    }
    pUVar3[in_AX].field_0x94 = cVar4;
    pUVar3[in_AX].field_0x96 = 0;
  }
  return;
}
