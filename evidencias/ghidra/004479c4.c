/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004479c4, entrada 004479c4.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_004479c4(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  undefined1 uVar2;
  UnidadeParcial *pUVar3;
  UnidadeParcial *pUVar4;
  byte bVar6;
  uint in_EAX;
  undefined3 uVar7;
  undefined4 uVar5;
  uint uVar8;
  bool bVar9;

  pUVar4 = tabela_unidades;
  uVar8 = in_EAX & 0xffff;
  bVar6 = tabela_unidades[uVar8].tipo_id;
  uVar7 = (undefined3)(in_EAX >> 8);
  uVar5 = CONCAT31(uVar7,bVar6);
  if (bVar6 < 0xc) {
    if (bVar6 < 3) {
      if (bVar6 == 0) {
        bVar9 = true;
        goto LAB_00447ac9;
      }
    }
    else if (3 < bVar6) {
      if (bVar6 < 8) {
        bVar9 = bVar6 == 4;
      }
      else {
        if (bVar6 < 9) goto LAB_00447a8f;
        bVar9 = bVar6 == 0xb;
      }
      goto LAB_00447ac9;
    }
    goto LAB_00447a8f;
  }
  if (bVar6 < 0xe) goto switchD_00447a9d_caseD_2;
  if (bVar6 < 0x13) {
    if ((0xe < bVar6) && (0xf < bVar6)) {
      bVar9 = bVar6 == 0x12;
      goto LAB_00447ac9;
    }
  }
  else if (((0x13 < bVar6) && (0x16 < bVar6)) && (0x18 < bVar6)) {
    bVar9 = bVar6 == 0x19;
LAB_00447ac9:
    if (!bVar9) goto switchD_00447a9d_caseD_2;
  }
LAB_00447a8f:
  uVar2 = tabela_unidades[uVar8].field_0x8a;
  uVar5 = CONCAT31(uVar7,uVar2);
  switch(uVar2) {
  case 0:
    bVar6 = tabela_unidades[uVar8].contador_animacao + 1;
    pUVar3 = tabela_unidades + uVar8;
    tabela_unidades[uVar8].contador_animacao = bVar6;
    if (bVar6 == pUVar3->periodo_animacao) {
      bVar6 = pUVar4[uVar8].quadro_movimento;
      bVar1 = pUVar4[uVar8].quantidade_quadros_movimento;
LAB_00447a48:
      pUVar4[uVar8].contador_animacao = 0;
      pUVar4[uVar8].quadro_movimento = (byte)((bVar6 + 1) % (uint)bVar1);
      return CONCAT44(param_2,(bVar6 + 1) / (uint)bVar1);
    }
    break;
  case 1:
    bVar6 = tabela_unidades[uVar8].contador_animacao + 1;
    uVar5 = CONCAT22((short)(in_EAX >> 0x10),CONCAT11(bVar6,uVar2));
    pUVar3 = tabela_unidades + uVar8;
    tabela_unidades[uVar8].contador_animacao = bVar6;
    if (bVar6 == pUVar3->field_0xa8) {
      bVar6 = pUVar4[uVar8].quadro_movimento;
      bVar1 = pUVar4[uVar8].field_0xa6;
      goto LAB_00447a48;
    }
  }
switchD_00447a9d_caseD_2:
  return CONCAT44(param_2,uVar5);
}
