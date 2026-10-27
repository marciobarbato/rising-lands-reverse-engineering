/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00447f58, entrada 00447f58.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00447f58(undefined4 param_1,undefined4 param_2)

{
  undefined1 uVar1;
  UnidadeParcial *pUVar2;
  UnidadeParcial *pUVar3;
  uint in_EAX;
  undefined3 uVar5;
  undefined4 uVar4;
  undefined2 uVar6;
  byte bVar8;
  uint uVar7;
  uint uVar9;
  bool bVar10;

  pUVar3 = tabela_unidades;
  uVar9 = in_EAX & 0xffff;
  bVar8 = tabela_unidades[uVar9].tipo_id;
  uVar5 = (undefined3)(in_EAX >> 8);
  uVar4 = CONCAT31(uVar5,bVar8);
  if (bVar8 < 6) {
    if (bVar8 != 5) goto switchD_00448004_caseD_0;
    uVar4 = CONCAT31(uVar5,tabela_unidades[uVar9].field_0x89);
    switch(tabela_unidades[uVar9].field_0x89) {
    default:
      goto switchD_00448004_caseD_0;
    case 1:
      bVar8 = tabela_unidades[uVar9].contador_animacao + 1;
      tabela_unidades[uVar9].contador_animacao = bVar8;
      bVar10 = bVar8 == pUVar3[uVar9].periodo_animacao;
    }
  }
  else {
    if (bVar8 < 7) goto switchD_00448004_caseD_0;
    uVar6 = (undefined2)(in_EAX >> 0x10);
    if (bVar8 < 8) {
      bVar8 = tabela_unidades[uVar9].field_0x89;
      uVar4 = CONCAT31(uVar5,bVar8);
      if ((((bVar8 < 2) || (bVar8 < 3)) || (bVar8 < 4)) || (bVar8 < 5))
      goto switchD_00448004_caseD_0;
      if (bVar8 != 0xc) {
        return CONCAT44(param_2,uVar4);
      }
      bVar8 = tabela_unidades[uVar9].contador_animacao + 1;
      pUVar2 = tabela_unidades + uVar9;
      uVar4 = CONCAT22(uVar6,CONCAT11(pUVar2->periodo_animacao,0xc));
      tabela_unidades[uVar9].contador_animacao = bVar8;
      if (bVar8 != pUVar2->periodo_animacao) goto switchD_00448004_caseD_0;
      bVar8 = pUVar3[uVar9].quadro_movimento;
      uVar7 = (uint)pUVar3[uVar9].quantidade_quadros_movimento;
      goto LAB_00447fc2;
    }
    if (bVar8 != 0xd) {
      return CONCAT44(param_2,uVar4);
    }
    uVar1 = tabela_unidades[uVar9].field_0x89;
    uVar4 = CONCAT31(uVar5,uVar1);
    switch(uVar1) {
    default:
      goto switchD_00448004_caseD_0;
    case 1:
      bVar8 = tabela_unidades[uVar9].contador_animacao + 1;
      pUVar2 = tabela_unidades + uVar9;
      tabela_unidades[uVar9].contador_animacao = bVar8;
      bVar10 = bVar8 == pUVar2->periodo_animacao;
      break;
    case 4:
      bVar8 = tabela_unidades[uVar9].contador_animacao + 1;
      uVar4 = CONCAT22(uVar6,CONCAT11(bVar8,uVar1));
      pUVar2 = tabela_unidades + uVar9;
      tabela_unidades[uVar9].contador_animacao = bVar8;
      bVar10 = bVar8 == pUVar2->periodo_animacao;
    }
  }
  if (bVar10) {
    bVar8 = pUVar3[uVar9].quadro_movimento;
    uVar7 = 4;
LAB_00447fc2:
    pUVar3[uVar9].contador_animacao = 0;
    pUVar3[uVar9].quadro_movimento = (byte)((bVar8 + 1) % uVar7);
    return CONCAT44(param_2,(bVar8 + 1) / uVar7);
  }
switchD_00448004_caseD_0:
  return CONCAT44(param_2,uVar4);
}
