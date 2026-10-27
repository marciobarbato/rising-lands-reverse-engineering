/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00453da2, entrada 00453da2.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00453da2(void)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  bool bVar4;
  ushort in_AX;
  undefined4 uVar5;
  uint uVar6;
  undefined4 uVar7;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  ushort uVar8;
  UnidadeParcial *pUVar9;
  ushort local_24;

  pUVar9 = tabela_unidades + in_AX;
  uVar7 = 0x100;
  bVar1 = pUVar9->proprietario_id;
  bVar2 = pUVar9->tipo_id;
  local_24 = pUVar9->celula_atual / 0x100;
  uVar8 = 0;
  do {
    if (799 < (short)uVar8) {
      FUN_0044f29a();
      return;
    }
    if ((tabela_unidades[uVar8].estado == 0) || (tabela_unidades[uVar8].estado == 4)) {
      bVar4 = false;
    }
    else {
      bVar4 = true;
    }
    if ((bVar4) && (tabela_unidades[uVar8].field_0x72 != '\0')) {
      bVar3 = tabela_unidades[uVar8].proprietario_id;
      uVar7 = CONCAT31((int3)((uint)uVar7 >> 8),bVar1);
      if ((bVar3 == bVar1) || ((bVar1 != 4 && (bVar3 != 4)))) {
        if ((bVar1 != 200) && ((bVar3 != 200 && (bVar3 != bVar1)))) {
          uVar5 = FUN_0046d838(uVar7,bVar3);
          uVar7 = extraout_ECX;
          if ((char)uVar5 == '\0') goto LAB_00453e95;
        }
        bVar4 = false;
      }
      else {
LAB_00453e95:
        bVar4 = true;
      }
      if ((bVar4) && (tabela_unidades[uVar8].proprietario_id != 200)) {
        bVar3 = tabela_unidades[uVar8].tipo_id;
        if (((bVar3 == 0x11) || (bVar3 == 10)) ||
           ((bVar3 == 0x10 && ((bVar2 < 2 || ((2 < bVar2 && (bVar2 != 8)))))))) {
          bVar4 = false;
        }
        else {
          bVar4 = true;
        }
        if (bVar4) {
          bVar3 = pUVar9->raio_visao;
          uVar6 = FUN_00479555(tabela_unidades[(short)uVar8].celula_atual / 0x100,local_24);
          uVar7 = extraout_ECX_00;
          if (uVar6 <= (uint)bVar3 * (uint)bVar3) {
            FUN_0044f29a();
            return;
          }
        }
      }
    }
    uVar8 = uVar8 + 1;
  } while( true );
}
