/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void OriginaisSBL::EnginNextCaseChemin(void)

{
  byte bVar1;
  ushort uVar2;
  bool bVar3;
  UnidadeParcial *pUVar4;
  ushort in_AX;
  ushort uVar5;
  int iVar6;
  uint uVar7;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  int extraout_EDX;
  uint uVar8;
  short asStack_28 [4];
  undefined4 local_20;
  byte local_1c;

  pUVar4 = tabela_unidades;
  uVar8 = (uint)in_AX;
  uVar2 = **(ushort **)(DAT_004e1924 + uVar8 * 4);
  if (uVar2 == 0) {
    tabela_unidades[uVar8].estado_caminho = 0;
    pUVar4[uVar8].field_0x8b = 0;
  }
  else {
    for (uVar5 = 0; uVar5 < 4; uVar5 = uVar5 + 1) {
      asStack_28[uVar5] = -1;
    }
    iVar6 = *(int *)(DAT_004e1924 + (uint)in_AX * 4);
    uVar2 = *(ushort *)(iVar6 + (uint)uVar2 * 2);
    local_20 = CONCAT22((short)((uint)iVar6 >> 0x10),uVar2);
    iVar6 = CalculDirection(0xffff,uVar2);
    local_1c = (byte)iVar6;
    uVar7 = EnginPeutPasser((int)asStack_28,(ushort)local_20);
    if ((char)uVar7 == '\0') {
      pUVar4[uVar8].estado_caminho = 0;
      pUVar4[uVar8].field_0x8b = 0;
    }
    else {
      bVar1 = tabela_unidades[in_AX].tipo_id;
      if ((bVar1 < 0xc) || ((0xc < bVar1 && (bVar1 != 0xf)))) {
        bVar3 = false;
      }
      else {
        bVar3 = true;
      }
      if (bVar3) {
        uVar7 = 0;
        while (((uVar7 & 0xffff) < 4 && (asStack_28[uVar7 & 0xffff] != -1))) {
          SetDyingEngin();
          uVar7 = extraout_EDX + 1;
        }
      }
      ResetEnginCollision();
      SetEnginCollision(extraout_ECX);
      SetEnginCollision(extraout_ECX_00);
      pUVar4[uVar8].celula_passo = (ushort)local_20;
      pUVar4[uVar8].direcao_desejada = local_1c;
    }
  }
  return;
}
