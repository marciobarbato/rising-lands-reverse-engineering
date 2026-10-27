/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00448f50, entrada 00448f50.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00448f50(uint param_1)

{
  bool bVar1;
  UnidadeParcial *pUVar2;
  UnidadeParcial *pUVar3;
  byte bVar4;
  char cVar6;
  uint in_EAX;
  undefined4 uVar5;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_ECX_01;
  uint extraout_ECX_02;
  uint extraout_ECX_03;
  uint extraout_ECX_04;
  uint extraout_ECX_05;
  int iVar7;
  uint extraout_EDX;
  undefined4 extraout_EDX_00;
  byte bVar8;
  uint uVar9;
  UnidadeParcial *pUVar10;
  uint uVar11;
  undefined8 uVar12;

  pUVar10 = tabela_unidades + (in_EAX & 0xffff);
  if ((*(int *)&pUVar10->field_0x83 >> 0x18 == 0) && (*(int *)&pUVar10->field_0x84 >> 0x18 == 0)) {
    iVar7 = CONCAT31((int3)(*(int *)&pUVar10->field_0x84 >> 0x1f),pUVar10->estado_caminho);
    if (iVar7 == 0) {
      FUN_00448d08(param_1);
      param_1 = extraout_ECX;
    }
    else if (iVar7 == 5) {
      FUN_00448b9f();
      param_1 = extraout_ECX_00;
    }
  }
  pUVar3 = tabela_unidades;
  if (pUVar10->celula_passo == pUVar10->celula_atual) {
    return;
  }
  uVar9 = in_EAX & 0xffff;
  bVar4 = tabela_unidades[uVar9].tipo_id;
  if ((bVar4 < 0xb) || (bVar4 < 0xc)) {
LAB_0044900b:
    cVar6 = tabela_unidades[uVar9].field_0xa9 + '\x01';
    pUVar2 = tabela_unidades + uVar9;
    tabela_unidades[uVar9].field_0xa9 = cVar6;
    uVar11 = CONCAT31((int3)(uVar9 >> 8),pUVar2->field_0xa7);
    if (cVar6 == pUVar2->field_0xa7) {
      param_1 = (uint)(byte)pUVar3[uVar9].field_0xa5;
      uVar11 = ((byte)pUVar3[uVar9].field_0xa4 + 1) % param_1;
      pUVar3[uVar9].field_0xa9 = 0;
      pUVar3[uVar9].field_0xa4 = (char)uVar11;
    }
  }
  else {
    uVar11 = uVar9;
    if (bVar4 < 0x12) {
      if ((bVar4 < 0xe) || (bVar4 < 0x10)) goto LAB_0044900b;
      if (bVar4 == 0x11) {
        FUN_00447b2f();
        param_1 = extraout_ECX_01;
        uVar11 = extraout_EDX;
      }
    }
    else if ((((bVar4 < 0x13) || (bVar4 < 0x17)) || (bVar4 < 0x19)) || (bVar4 == 0x19))
    goto LAB_0044900b;
  }
  if (pUVar10->field_0x91 != pUVar10->field_0x90) {
    FUN_00448599(param_1,uVar11);
    param_1 = extraout_ECX_02;
  }
  pUVar3 = tabela_unidades;
  if (DAT_00508041 == pUVar10->proprietario_id) {
    switch(pUVar10->tipo_id) {
    case 0xb:
    case 0xc:
    case 0xd:
    case 0xe:
    case 0xf:
    case 0x10:
      bVar1 = true;
      break;
    default:
      bVar1 = false;
    }
    if (bVar1) {
      uVar9 = in_EAX & 0xffff;
      uVar5 = FUN_004766f0(uVar9,(uint)DAT_00508041);
      param_1 = extraout_ECX_03;
      if ((char)uVar5 != '\0') {
        uVar12 = FUN_00440c5d(extraout_ECX_03,extraout_EDX_00);
        pUVar3[uVar9].field_0xf9 = 1;
        param_1 = extraout_ECX_04;
        if (*(int *)&pUVar3[uVar9].field_0x104 == -1) {
          FUN_0048aa79(1,(uint)pUVar3[uVar9].tipo_id << 0x10 | 0x800,(uint)uVar12);
          param_1 = extraout_ECX_05;
        }
      }
    }
  }
  bVar4 = pUVar10->field_0x90 - 1;
  bVar8 = pUVar10->field_0x91 - 1;
  if (bVar4 != bVar8) {
    uVar11 = (uint)bVar4;
    param_1 = 0x10;
    uVar9 = (uint)bVar8;
    if ((((uVar11 + 1) % 0x10 != uVar9) && ((uVar11 + 2) % 0x10 != uVar9)) &&
       (((uVar11 + 0xf) % 0x10 != uVar9 && ((uVar11 + 0xe) % 0x10 != uVar9)))) {
      bVar1 = false;
      goto LAB_0044915d;
    }
  }
  bVar1 = true;
LAB_0044915d:
  if (bVar1) {
    FUN_00448704(param_1,'\0');
  }
  return;
}
