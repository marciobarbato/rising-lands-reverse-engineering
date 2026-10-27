/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044a2ed, entrada 0044a2ed.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_0044a2ed(void)

{
  byte bVar1;
  ushort uVar2;
  UnidadeParcial *pUVar3;
  UnidadeParcial *pUVar4;
  char cVar5;
  uint in_EAX;
  undefined4 uVar6;
  uint extraout_ECX;
  uint extraout_ECX_00;
  undefined4 extraout_ECX_01;
  uint uVar7;
  uint uVar8;
  bool bVar9;

  pUVar3 = tabela_unidades;
  uVar8 = in_EAX & 0xffff;
  bVar1 = tabela_unidades[uVar8].tipo_id;
  if (bVar1 < 5) {
    if (bVar1 != 0) goto LAB_0044a331;
    bVar9 = true;
  }
  else {
    if ((((bVar1 < 6) || (bVar1 < 8)) || (bVar1 < 9)) || (bVar1 < 0xb)) goto LAB_0044a331;
    bVar9 = bVar1 == 0x19;
  }
  if (!bVar9) {
    return;
  }
LAB_0044a331:
  uVar6 = FUN_004468e4(in_EAX);
  pUVar4 = tabela_unidades;
  if ((char)uVar6 == '\0') {
    if (pUVar3[uVar8].celula_destino == pUVar3[uVar8].celula_atual) {
      tabela_unidades[in_EAX & 0xffff].celula_destino =
           tabela_unidades[*(ushort *)&pUVar3[uVar8].field_0xb8].celula_passo;
      if ((ushort)extraout_ECX == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_00496304 = 0xffff;
        DAT_004e0f3c = 0;
      }
      pUVar4[in_EAX & 0xffff].estado_caminho = 0;
    }
    FUN_0044930c();
  }
  else {
    if ((tabela_unidades[*(ushort *)&pUVar3[uVar8].field_0xb8].estado == 0) ||
       (tabela_unidades[*(ushort *)&pUVar3[uVar8].field_0xb8].estado == 4)) {
      bVar9 = false;
    }
    else {
      bVar9 = true;
    }
    uVar7 = extraout_ECX;
    if ((bVar9) &&
       (cVar5 = FUN_00447694(extraout_ECX,(ushort)extraout_ECX), uVar7 = extraout_ECX_00,
       cVar5 != '\0')) {
      FUN_00457058();
      uVar2 = tabela_unidades[*(ushort *)&pUVar3[uVar8].field_0xb8].celula_passo;
      pUVar3[uVar8].celula_passo = uVar2;
      pUVar3[uVar8].celula_destino = uVar2;
      pUVar3[uVar8].celula_atual = uVar2;
      pUVar3[uVar8].estado = 0xe;
      FUN_00472648(extraout_ECX_01);
    }
    else {
      if ((tabela_unidades[uVar7 & 0xffff].estado == 0) ||
         (tabela_unidades[uVar7 & 0xffff].estado == 4)) {
        bVar9 = false;
      }
      else {
        bVar9 = true;
      }
      if ((bVar9) && (tabela_unidades[uVar7 & 0xffff].estado = 7, (ushort)uVar7 == DAT_00496304)) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = 0xffff;
      }
    }
  }
  return;
}
