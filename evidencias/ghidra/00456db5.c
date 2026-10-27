/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00456db5, entrada 00456db5.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00456db5(void)

{
  byte bVar1;
  bool bVar2;
  uint uVar3;
  byte bVar4;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint uVar5;
  ushort uVar6;

  _DAT_004e1a38 = 0;
  DAT_004e1a3a = 0;
  for (bVar4 = 0; bVar4 < 4; bVar4 = bVar4 + 1) {
    for (uVar3 = 0; (uVar3 & 0xffff) < 0x1a; uVar3 = uVar3 + 1) {
      *(undefined2 *)(&DAT_004e1a3c + (uVar3 & 0xffff) * 2 + (uint)bVar4 * 0x34) = 0;
    }
    *(undefined2 *)(&DAT_004e1928 + (uint)bVar4 * 2) = 0;
  }
  uVar3 = 0;
  _DAT_004e1930 = 0;
  for (uVar6 = 0; uVar6 < 800; uVar6 = uVar6 + 1) {
    if (tabela_unidades[uVar6].estado != 0) {
      uVar5 = (uint)tabela_unidades[uVar6].estado;
      if ((uVar5 == 0) || (uVar5 == 4)) {
        bVar2 = false;
      }
      else {
        bVar2 = true;
      }
      if (bVar2) {
        bVar4 = tabela_unidades[uVar6].tipo_id;
        bVar1 = tabela_unidades[uVar6].proprietario_id;
        uVar5 = (uint)bVar1;
        if ((uVar5 != 200) && (uVar5 != 4)) {
          *(short *)(&DAT_004e1a3c + (CONCAT11(bVar1,bVar4) & 0xff) * 2 + uVar5 * 0x34) =
               *(short *)(&DAT_004e1a3c + (CONCAT11(bVar1,bVar4) & 0xff) * 2 + uVar5 * 0x34) + 1;
        }
        FUN_0047fbfd(CONCAT22((short)(uVar3 >> 0x10),CONCAT11(bVar1,bVar4)));
        bVar4 = (byte)(extraout_ECX >> 8);
        if ((extraout_ECX & 0xff) != 0x11) {
          if (bVar4 == DAT_00508041) {
            DAT_004e1a3a = DAT_004e1a3a + 1;
          }
          else {
            _DAT_004e1a38 = _DAT_004e1a38 + 1;
          }
        }
        uVar5 = (uint)bVar4;
        uVar3 = extraout_ECX;
        if ((uVar5 != 200) && ((extraout_ECX & 0xff) != 5)) {
          *(short *)(&DAT_004e1928 + uVar5 * 2) = *(short *)(&DAT_004e1928 + uVar5 * 2) + 1;
        }
      }
      FUN_0045442c(uVar3,uVar5);
      uVar3 = extraout_ECX_00;
    }
  }
  return;
}
