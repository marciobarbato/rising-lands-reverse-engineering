/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00447f58, entrada 00447f58.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00447f58(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  undefined1 uVar2;
  UnidadeParcial *pUVar3;
  UnidadeParcial *pUVar4;
  uint in_EAX;
  undefined3 uVar6;
  undefined4 uVar5;
  undefined2 uVar7;
  char cVar9;
  uint uVar8;
  uint uVar10;
  bool bVar11;

  pUVar4 = tabela_unidades;
  uVar10 = in_EAX & 0xffff;
  bVar1 = tabela_unidades[uVar10].tipo_id;
  uVar6 = (undefined3)(in_EAX >> 8);
  uVar5 = CONCAT31(uVar6,bVar1);
  if (bVar1 < 6) {
    if (bVar1 != 5) goto switchD_00448004_caseD_0;
    uVar5 = CONCAT31(uVar6,tabela_unidades[uVar10].field_0x89);
    switch(tabela_unidades[uVar10].field_0x89) {
    default:
      goto switchD_00448004_caseD_0;
    case 1:
      cVar9 = tabela_unidades[uVar10].field_0xa9 + '\x01';
      tabela_unidades[uVar10].field_0xa9 = cVar9;
      bVar11 = cVar9 == pUVar4[uVar10].field_0xa7;
    }
  }
  else {
    if (bVar1 < 7) goto switchD_00448004_caseD_0;
    uVar7 = (undefined2)(in_EAX >> 0x10);
    if (bVar1 < 8) {
      bVar1 = tabela_unidades[uVar10].field_0x89;
      uVar5 = CONCAT31(uVar6,bVar1);
      if ((((bVar1 < 2) || (bVar1 < 3)) || (bVar1 < 4)) || (bVar1 < 5))
      goto switchD_00448004_caseD_0;
      if (bVar1 != 0xc) {
        return CONCAT44(param_2,uVar5);
      }
      cVar9 = tabela_unidades[uVar10].field_0xa9 + '\x01';
      pUVar3 = tabela_unidades + uVar10;
      uVar5 = CONCAT22(uVar7,CONCAT11(pUVar3->field_0xa7,0xc));
      tabela_unidades[uVar10].field_0xa9 = cVar9;
      if (cVar9 != pUVar3->field_0xa7) goto switchD_00448004_caseD_0;
      bVar1 = pUVar4[uVar10].field_0xa4;
      uVar8 = (uint)(byte)pUVar4[uVar10].field_0xa5;
      goto LAB_00447fc2;
    }
    if (bVar1 != 0xd) {
      return CONCAT44(param_2,uVar5);
    }
    uVar2 = tabela_unidades[uVar10].field_0x89;
    uVar5 = CONCAT31(uVar6,uVar2);
    switch(uVar2) {
    default:
      goto switchD_00448004_caseD_0;
    case 1:
      cVar9 = tabela_unidades[uVar10].field_0xa9 + '\x01';
      pUVar3 = tabela_unidades + uVar10;
      tabela_unidades[uVar10].field_0xa9 = cVar9;
      bVar11 = cVar9 == pUVar3->field_0xa7;
      break;
    case 4:
      cVar9 = tabela_unidades[uVar10].field_0xa9 + '\x01';
      uVar5 = CONCAT22(uVar7,CONCAT11(cVar9,uVar2));
      pUVar3 = tabela_unidades + uVar10;
      tabela_unidades[uVar10].field_0xa9 = cVar9;
      bVar11 = cVar9 == pUVar3->field_0xa7;
    }
  }
  if (bVar11) {
    bVar1 = pUVar4[uVar10].field_0xa4;
    uVar8 = 4;
LAB_00447fc2:
    pUVar4[uVar10].field_0xa9 = 0;
    pUVar4[uVar10].field_0xa4 = (char)((bVar1 + 1) % uVar8);
    return CONCAT44(param_2,(bVar1 + 1) / uVar8);
  }
switchD_00448004_caseD_0:
  return CONCAT44(param_2,uVar5);
}
