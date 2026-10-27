/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004479c4, entrada 004479c4.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_004479c4(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  byte bVar2;
  undefined1 uVar3;
  UnidadeParcial *pUVar4;
  UnidadeParcial *pUVar5;
  char cVar7;
  uint in_EAX;
  undefined3 uVar8;
  undefined4 uVar6;
  uint uVar9;
  bool bVar10;

  pUVar5 = tabela_unidades;
  uVar9 = in_EAX & 0xffff;
  bVar1 = tabela_unidades[uVar9].tipo_id;
  uVar8 = (undefined3)(in_EAX >> 8);
  uVar6 = CONCAT31(uVar8,bVar1);
  if (bVar1 < 0xc) {
    if (bVar1 < 3) {
      if (bVar1 == 0) {
        bVar10 = true;
        goto LAB_00447ac9;
      }
    }
    else if (3 < bVar1) {
      if (bVar1 < 8) {
        bVar10 = bVar1 == 4;
      }
      else {
        if (bVar1 < 9) goto LAB_00447a8f;
        bVar10 = bVar1 == 0xb;
      }
      goto LAB_00447ac9;
    }
    goto LAB_00447a8f;
  }
  if (bVar1 < 0xe) goto switchD_00447a9d_caseD_2;
  if (bVar1 < 0x13) {
    if ((0xe < bVar1) && (0xf < bVar1)) {
      bVar10 = bVar1 == 0x12;
      goto LAB_00447ac9;
    }
  }
  else if (((0x13 < bVar1) && (0x16 < bVar1)) && (0x18 < bVar1)) {
    bVar10 = bVar1 == 0x19;
LAB_00447ac9:
    if (!bVar10) goto switchD_00447a9d_caseD_2;
  }
LAB_00447a8f:
  uVar3 = tabela_unidades[uVar9].field_0x8a;
  uVar6 = CONCAT31(uVar8,uVar3);
  switch(uVar3) {
  case 0:
    cVar7 = tabela_unidades[uVar9].field_0xa9 + '\x01';
    pUVar4 = tabela_unidades + uVar9;
    tabela_unidades[uVar9].field_0xa9 = cVar7;
    if (cVar7 == pUVar4->field_0xa7) {
      bVar1 = pUVar5[uVar9].field_0xa4;
      bVar2 = pUVar5[uVar9].field_0xa5;
LAB_00447a48:
      pUVar5[uVar9].field_0xa9 = 0;
      pUVar5[uVar9].field_0xa4 = (char)((bVar1 + 1) % (uint)bVar2);
      return CONCAT44(param_2,(bVar1 + 1) / (uint)bVar2);
    }
    break;
  case 1:
    cVar7 = tabela_unidades[uVar9].field_0xa9 + '\x01';
    uVar6 = CONCAT22((short)(in_EAX >> 0x10),CONCAT11(cVar7,uVar3));
    pUVar4 = tabela_unidades + uVar9;
    tabela_unidades[uVar9].field_0xa9 = cVar7;
    if (cVar7 == pUVar4->field_0xa8) {
      bVar1 = pUVar5[uVar9].field_0xa4;
      bVar2 = pUVar5[uVar9].field_0xa6;
      goto LAB_00447a48;
    }
  }
switchD_00447a9d_caseD_2:
  return CONCAT44(param_2,uVar6);
}
