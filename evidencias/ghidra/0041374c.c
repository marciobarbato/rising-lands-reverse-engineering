/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0041374c, entrada 0041374c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_0041374c(undefined4 param_1,int param_2)

{
  undefined1 *puVar1;
  ushort uVar2;
  char cVar3;
  short sVar4;
  short sVar5;
  int in_EAX;
  UnidadeParcial *pUVar6;
  uint uVar7;
  uint uVar8;
  undefined3 extraout_var;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint uVar9;
  uint extraout_ECX_01;
  uint extraout_ECX_02;
  uint extraout_ECX_03;
  uint extraout_ECX_04;
  uint extraout_ECX_05;
  uint extraout_ECX_06;
  uint extraout_ECX_07;
  uint extraout_ECX_08;
  uint extraout_ECX_09;
  uint extraout_ECX_10;
  undefined4 extraout_EDX;
  byte *extraout_EDX_00;
  uint extraout_EDX_01;
  ushort unaff_BX;
  UnidadeParcial *pUVar10;
  short sVar11;
  ushort uVar12;
  int iVar13;
  undefined8 uVar14;
  short local_40 [2];
  int local_3c;
  undefined4 local_38;
  int local_34;
  int local_30;
  short local_2c [2];
  ushort uStack_28;
  short sStack_24;
  undefined4 local_18;

  uVar9 = (uint)unaff_BX;
  sStack_24 = 0;
  pUVar10 = tabela_unidades + uVar9;
  uStack_28 = 0;
  iVar13 = in_EAX + CONCAT22((short)(uVar9 * 0x114 >> 0x10),(short)pUVar10->deslocamento_x);
  sVar5 = (short)iVar13;
  local_18 = CONCAT22(local_18._2_2_,sVar5);
  local_40[0] = 0;
  local_40[1] = 0;
  iVar13 = CONCAT22((short)((uint)iVar13 >> 0x10),(short)pUVar10->deslocamento_y) + param_2;
  local_34 = param_2;
  FUN_00410fcc(uVar9,local_40);
  sVar11 = (short)iVar13;
  uVar9 = extraout_ECX;
  if ((pUVar10->selecionada != 0) && (DAT_00508041 == pUVar10->proprietario_id)) {
    local_38 = local_18;
    FUN_0044106c(extraout_ECX,local_2c);
    if (local_2c[0] == 1) {
      sVar4 = sVar11;
    }
    else {
      sVar4 = sVar11 + -0x20;
    }
    local_3c = iVar13;
    FUN_0045b247('\x01',sVar4);
    uVar9 = extraout_ECX_00;
    if ((pUVar10->tipo_id == 0xe) && (*(short *)&pUVar10->field_0xd8 != 0)) {
      uVar9 = 0;
      for (uVar12 = 0; uVar12 < *(ushort *)&pUVar10->field_0xd8; uVar12 = uVar12 + 1) {
        uVar9 = (uint)*(ushort *)(&pUVar10->field_0xc4 + (uint)uVar12 * 2) % 0x100;
        if ((((DAT_0050871e._2_2_ <= (ushort)uVar9) &&
             (uVar9 < (uint)DAT_00508724 + (uint)DAT_0050871e._2_2_)) &&
            (uVar2 = *(ushort *)(&pUVar10->field_0xc4 + (uint)uVar12 * 2) >> 8,
            DAT_00508722 <= uVar2)) && ((uint)uVar2 < (uint)DAT_00508726 + (uint)DAT_00508722)) {
          FUN_0045b247('\x01',(uVar2 - DAT_00508722) * 0x20);
          uVar9 = extraout_ECX_01;
        }
      }
    }
  }
  switch(pUVar10->tipo_id) {
  case 0:
    FUN_0045b796('\x01',sVar11 + 0x1a);
    break;
  case 1:
    FUN_0045b796('\x01',sVar11 + 0x1a);
    break;
  case 2:
    FUN_0045b796('\x01',sVar11 + 0x1a);
    break;
  case 3:
    FUN_0045b796('\x01',sVar11);
    goto LAB_00413b11;
  case 4:
    FUN_0045b796('\x01',sVar11 + 0x1a);
    uVar14 = FUN_00440e11((uint)unaff_BX,extraout_EDX);
    uVar9 = extraout_ECX_04;
    if ((((uint)uVar14 & 0xff) == 1) ||
       (uVar14 = FUN_00440e11(extraout_ECX_04,(int)((ulonglong)uVar14 >> 0x20)),
       uVar9 = extraout_ECX_05, ((uint)uVar14 & 0xff) == 0x18)) {
      FUN_00411147(uVar9,(int)sVar11);
      uVar9 = extraout_ECX_06;
    }
    uStack_28 = sVar11 - 9;
    sStack_24 = sVar5;
  default:
    goto switchD_00414318_caseD_5;
  case 8:
    FUN_0045b796('\x01',sVar11 + 0x1a);
    break;
  case 0xb:
    FUN_0045b796('\x01',sVar11);
    break;
  case 0xc:
    uVar9 = (uint)pUVar10->orientacao_atual;
    local_30 = (uint)pUVar10->quadro_movimento * (uVar9 % 2) +
               (uVar9 / 2) * (uint)pUVar10->quantidade_quadros_movimento + (int)(uVar9 - 1) / 2;
    FUN_0045b796('\x01',sVar11);
    break;
  case 0xe:
    FUN_0045b796('\x01',sVar11);
    break;
  case 0xf:
    FUN_0045b796('\x01',sVar11);
    break;
  case 0x10:
    uVar9 = (uint)pUVar10->orientacao_atual;
    local_30 = (uint)pUVar10->quadro_movimento * (uVar9 % 2) +
               (uint)pUVar10->quantidade_quadros_movimento * (uVar9 / 2) + (int)(uVar9 - 1) / 2;
    FUN_0045b796('\x01',sVar11);
    FUN_00411147((uint)unaff_BX,(int)(short)((sVar11 + -0x14) - (ushort)(byte)pUVar10->field_0xab));
    uVar9 = (uint)pUVar10->orientacao_atual;
    local_30 = (uVar9 % 2) * (uint)pUVar10->quadro_movimento +
               (uVar9 / 2) * (uint)pUVar10->quantidade_quadros_movimento + (int)(uVar9 - 1) / 2;
    FUN_0045b796('\x01',sVar11);
    FUN_00411147((uint)unaff_BX,(int)(short)(sVar11 - (ushort)(byte)pUVar10->field_0xab));
    uVar12 = sVar11 - 0x29;
    uVar9 = extraout_ECX_07;
    goto LAB_00413f6b;
  case 0x11:
    uVar12 = sVar11 - 9;
LAB_00413f6b:
    sVar5 = sVar5 + -0x20;
    goto LAB_004139ae;
  case 0x14:
    FUN_0045b796('\x01',sVar11);
    break;
  case 0x15:
    FUN_0045b796('\x01',sVar11);
    break;
  case 0x16:
    local_30 = (uint)pUVar10->quadro_movimento +
               (uint)(byte)pUVar10->field_0xa6 * ((pUVar10->orientacao_atual + 1) / 2 - 1);
    FUN_0045b796('\x01',sVar11);
    break;
  case 0x17:
    FUN_0045b796('\x01',sVar11);
    break;
  case 0x18:
    FUN_0045b796('\x01',sVar11);
    break;
  case 0x19:
    FUN_0045b796('\x01',sVar11);
LAB_00413b11:
    FUN_00411147((uint)unaff_BX,(int)sVar11);
    uVar12 = sVar11 - 0x18;
    sVar5 = sVar5 + -0xf;
    uVar9 = extraout_ECX_03;
    goto LAB_004139ae;
  }
  uVar12 = sVar11 - 9;
  FUN_00411147((uint)unaff_BX,(int)sVar11);
  uVar9 = extraout_ECX_02;
LAB_004139ae:
  uStack_28 = uVar12;
  sStack_24 = sVar5;
switchD_00414318_caseD_5:
  if (((DAT_00508041 == pUVar10->proprietario_id) && (pUVar10->selecionada != 0)) ||
     ((unaff_BX == DAT_00496ac2 || (DAT_00508f8d._2_1_ != '\0')))) {
    uVar9 = FUN_00410be4(uVar9,uStack_28);
    return uVar9;
  }
  pUVar6 = tabela_unidades + unaff_BX;
  if (*(short *)&pUVar6->field_0x4 == *(short *)&pUVar6->field_0x76) {
    puVar1 = &pUVar6->field_0x74;
    pUVar6 = (UnidadeParcial *)(uint)*(ushort *)puVar1;
    if (pUVar6 < (UnidadeParcial *)0x64) {
      uVar8 = CONCAT31((uint3)(byte)(*(ushort *)puVar1 >> 8),1);
      goto LAB_0041435a;
    }
  }
  uVar8 = (uint)pUVar6 & 0xffffff00;
LAB_0041435a:
  if ((((char)uVar8 != '\0') &&
      (uVar7 = *(ushort *)&pUVar10->field_0x74 / 5, uVar8 = uVar7 / 2, uVar7 % 2 == 0)) &&
     (uVar8 = FUN_00442c34(), uVar9 = extraout_ECX_08, (char)uVar8 != '\0')) {
    if (*extraout_EDX_00 == 200) {
      uVar8 = FUN_0045b247('\x01',uStack_28 - 2);
      uVar9 = extraout_ECX_09;
    }
    else {
      uVar8 = FUN_0045c455('\x01',uStack_28 - 2,*extraout_EDX_00);
      uVar9 = extraout_ECX_10;
    }
  }
  if ((pUVar10->field_0xba != '\0') && (uVar8 = DAT_00508f7c / 5, DAT_00508f7c % 5 == 0)) {
    FUN_0044f9a6(uVar9,unaff_BX & 0xffff00ff);
    cVar3 = FUN_004422b0();
    uVar8 = CONCAT31(extraout_var,cVar3);
    if ((cVar3 != '\0') && (uVar8 = 0, (extraout_EDX_01 & 0xffff) != 0)) {
      uVar8 = FUN_0045b247('\x01',uStack_28 - 2);
    }
  }
  return uVar8;
}
