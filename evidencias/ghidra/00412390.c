/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00412390, entrada 00412390.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_00412390(undefined4 param_1,int param_2)

{
  undefined1 *puVar1;
  byte bVar2;
  short sVar3;
  char cVar4;
  undefined2 uVar5;
  undefined2 uVar6;
  int in_EAX;
  int iVar7;
  UnidadeParcial *pUVar8;
  uint uVar9;
  uint uVar10;
  undefined3 extraout_var;
  short sVar11;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint uVar12;
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
  short extraout_var_00;
  short extraout_var_01;
  byte *extraout_EDX;
  ushort unaff_BX;
  UnidadeParcial *pUVar13;
  ushort uVar14;
  int iVar15;
  undefined8 uVar16;
  short local_30 [4];
  ushort uStack_28;
  uint local_24;
  undefined4 local_20;
  short local_1c [2];
  undefined4 local_18;
  short local_14;
  undefined2 uStack_12;

  local_30[2] = 0;
  pUVar13 = tabela_unidades + unaff_BX;
  uVar5 = (undefined2)((uint)unaff_BX * 0x114 >> 0x10);
  uStack_28 = 0;
  local_30[0] = 0;
  local_30[1] = 0;
  iVar15 = param_2 + CONCAT22(uVar5,(short)pUVar13->deslocamento_y);
  FUN_00410fcc(in_EAX + CONCAT22(uVar5,(short)pUVar13->deslocamento_x),local_30);
  local_20 = CONCAT22(local_20._2_2_,(short)extraout_ECX);
  if ((((pUVar13->celula_atual != pUVar13->celula_destino) && (pUVar13->field_0x99 != '\0')) &&
      (*(int *)&pUVar13->field_0x83 >> 0x18 != 0)) && (*(int *)&pUVar13->field_0x84 >> 0x18 != 0)) {
    if ((pUVar13->orientacao_atual == 5) || (pUVar13->orientacao_atual == 0xd)) {
      uVar12 = (uint)DAT_004e1d18;
      DAT_004e1d18 = DAT_004e1d18 + 1;
      local_20 = CONCAT22(local_20._2_2_,
                          (short)extraout_ECX +
                          (ushort)(byte)(&DAT_004e1c18)[uVar12] % (ushort)(byte)pUVar13->field_0x99)
      ;
    }
    else {
      uVar12 = (uint)DAT_004e1d18;
      DAT_004e1d18 = DAT_004e1d18 + 1;
      iVar15 = iVar15 + (uint)(byte)(&DAT_004e1c18)[uVar12] % (uint)(byte)pUVar13->field_0x99;
    }
  }
  sVar3 = (short)iVar15;
  uVar12 = extraout_ECX;
  if ((pUVar13->selecionada != 0) && (DAT_00508041 == pUVar13->proprietario_id)) {
    local_18 = local_20;
    FUN_0044106c(extraout_ECX,local_1c);
    if (local_1c[0] == 1) {
      sVar11 = sVar3;
    }
    else {
      sVar11 = sVar3 + -0x20;
    }
    FUN_0045b247('\x01',sVar11);
    uVar12 = extraout_ECX_00;
    if ((pUVar13->tipo_id == 0xe) && (*(short *)&pUVar13->field_0xd8 != 0)) {
      uVar12 = 0;
      for (local_24 = 0; (ushort)local_24 < *(ushort *)&pUVar13->field_0xd8; local_24 = local_24 + 1
          ) {
        uVar12 = (uint)*(ushort *)(&pUVar13->field_0xc4 + (local_24 & 0xffff) * 2) % 0x100;
        if ((((DAT_0050871e._2_2_ <= (ushort)uVar12) &&
             (uVar12 < (uint)DAT_00508724 + (uint)DAT_0050871e._2_2_)) &&
            (uVar14 = *(ushort *)(&pUVar13->field_0xc4 + (local_24 & 0xffff) * 2) >> 8,
            DAT_00508722 <= uVar14)) && ((uint)uVar14 < (uint)DAT_00508726 + (uint)DAT_00508722)) {
          FUN_0045b247('\x01',(uVar14 - DAT_00508722) * 0x20);
          uVar12 = extraout_ECX_01;
        }
      }
    }
    if ((pUVar13->estado != 0x11) && (bVar2 = pUVar13->field_0x82, bVar2 != 0)) {
      uVar12 = 5;
      if (bVar2 < 2) {
        uVar12 = (uint)*(ushort *)&pUVar13->field_0xb2 % 0x100;
        if (((DAT_0050871e._2_2_ <= (ushort)uVar12) &&
            (uVar12 < (uint)DAT_00508724 + (uint)DAT_0050871e._2_2_)) &&
           ((uVar14 = *(ushort *)&pUVar13->field_0xb2 >> 8, DAT_00508722 <= uVar14 &&
            ((uint)uVar14 < (uint)DAT_00508726 + (uint)DAT_00508722)))) {
          FUN_0045b247('\x01',(uVar14 - DAT_00508722) * 0x20);
        }
        uVar12 = (uint)*(ushort *)&pUVar13->field_0x80 % 0x100;
        if ((((DAT_0050871e._2_2_ <= (ushort)uVar12) &&
             (uVar12 < (uint)DAT_00508724 + (uint)DAT_0050871e._2_2_)) &&
            (uVar14 = *(ushort *)&pUVar13->field_0x80 >> 8, DAT_00508722 <= uVar14)) &&
           ((uint)uVar14 < (uint)DAT_00508726 + (uint)DAT_00508722)) {
          sVar11 = uVar14 - DAT_00508722;
LAB_004127b2:
          FUN_0045b247('\x01',sVar11 * 0x20);
          uVar12 = extraout_ECX_02;
        }
      }
      else if (bVar2 == 2) {
        uVar12 = (uint)*(ushort *)&pUVar13->field_0xb2 % 0x100;
        if (((DAT_0050871e._2_2_ <= (ushort)uVar12) &&
            (uVar12 < (uint)DAT_00508724 + (uint)DAT_0050871e._2_2_)) &&
           ((uVar14 = *(ushort *)&pUVar13->field_0xb2 >> 8, DAT_00508722 <= uVar14 &&
            ((uint)uVar14 < (uint)DAT_00508726 + (uint)DAT_00508722)))) {
          FUN_0045b247('\x01',(uVar14 - DAT_00508722) * 0x20);
        }
        uVar5 = FUN_0041aee2();
        uVar6 = FUN_0041aee2();
        iVar7 = (CONCAT22(extraout_var_01,uVar6) + ((int)extraout_var_01 >> 0xf) * -0x100) -
                (uint)(((int)extraout_var_01 >> 0xf) << 7 < 0);
        uVar12 = iVar7 >> 8;
        uVar14 = (ushort)(CONCAT44((int)extraout_var_00 >> 0xf,CONCAT22(extraout_var_00,uVar5)) %
                         0x100);
        if (((DAT_0050871e._2_2_ <= uVar14) &&
            ((uint)uVar14 < (uint)DAT_00508724 + (uint)DAT_0050871e._2_2_)) &&
           ((uVar14 = (ushort)((uint)iVar7 >> 8), DAT_00508722 <= uVar14 &&
            ((uint)uVar14 < (uint)DAT_00508726 + (uint)DAT_00508722)))) {
          sVar11 = uVar14 - DAT_00508722;
          goto LAB_004127b2;
        }
      }
    }
  }
  switch(pUVar13->tipo_id) {
  case 0:
    FUN_0045b796('\x01',sVar3 + 0x1a);
    break;
  case 1:
    FUN_0045b796('\x01',sVar3 + 0x1a);
    break;
  case 2:
    FUN_0045b796('\x01',sVar3 + 0x1a);
    break;
  case 3:
    FUN_0045b796('\x01',sVar3);
    goto LAB_00412e0f;
  case 4:
    FUN_0045b796('\x01',sVar3 + 0x1a);
    break;
  case 5:
    uVar5 = FUN_004470b9();
    if ((char)uVar5 == '\0') {
      FUN_0045b796('\x01',sVar3 + 0x1a);
    }
    else {
      FUN_0045b796('\x01',sVar3 + 0x1a);
    }
    goto LAB_00412a12;
  case 6:
    uVar5 = FUN_004470b9();
    if ((char)uVar5 == '\0') {
      FUN_0045b796('\x01',sVar3 + 0x1a);
    }
    else {
      FUN_0045b796('\x01',sVar3 + 0x1a);
    }
    goto LAB_00412a12;
  case 7:
    uVar5 = FUN_004470b9();
    if ((char)uVar5 == '\0') {
      FUN_0045b796('\x01',sVar3 + 0x1a);
    }
    else {
      FUN_0045b796('\x01',sVar3 + 0x1a);
    }
LAB_00412a12:
    _local_14 = CONCAT22(uStack_12,(short)local_20 + local_30[0]);
    FUN_00411147((uint)unaff_BX,(int)sVar3);
    uStack_28 = sVar3 - 9;
    local_30[2] = (short)local_20;
    uVar12 = extraout_ECX_03;
    goto switchD_0041262f_caseD_12;
  case 8:
    FUN_0045b796('\x01',sVar3 + 0x1a);
    break;
  case 9:
    FUN_0045b796('\x01',sVar3 + 0x1a);
    break;
  case 10:
    FUN_0045b796('\x01',sVar3 + 0x1a);
    break;
  case 0xb:
    FUN_0045b796('\x01',sVar3);
    break;
  case 0xc:
    FUN_0045b796('\x01',sVar3);
    break;
  case 0xd:
    FUN_0045b796('\x01',sVar3);
    break;
  case 0xe:
    FUN_0045b796('\x01',sVar3);
    break;
  case 0xf:
    FUN_0045b796('\x01',sVar3);
    break;
  case 0x10:
    FUN_0045b796('\x01',sVar3);
    uStack_12 = (undefined2)((uint)(iVar15 + -0x14) >> 0x10);
    _local_14 = CONCAT22(uStack_12,(short)local_20 + local_30[0]);
    FUN_00411147((uint)unaff_BX,
                 (int)(short)((short)(iVar15 + -0x14) - (ushort)(byte)pUVar13->field_0xab));
    local_30[2] = (short)local_20;
    uVar14 = sVar3 - 0x29;
    uVar12 = extraout_ECX_06;
    goto LAB_004130b7;
  case 0x11:
    FUN_0041209d(uVar12,(int)(short)((short)local_20 + local_30[0]));
    local_30[2] = (short)local_20;
    uVar14 = sVar3 - 9;
    uVar12 = extraout_ECX_07;
LAB_004130b7:
    local_30[2] = local_30[2] + -0x20;
    goto LAB_00412cef;
  default:
    goto switchD_0041262f_caseD_12;
  case 0x14:
    FUN_0045b796('\x01',sVar3);
    break;
  case 0x15:
    FUN_0045b796('\x01',sVar3);
    break;
  case 0x16:
    FUN_0045b796('\x01',sVar3);
    break;
  case 0x17:
    FUN_0045b796('\x01',sVar3);
    break;
  case 0x18:
    FUN_0045b796('\x01',sVar3);
    break;
  case 0x19:
    FUN_0045b796('\x01',sVar3);
LAB_00412e0f:
    _local_14 = CONCAT22(uStack_12,(short)local_20 + local_30[0]);
    FUN_00411147((uint)unaff_BX,(int)sVar3);
    uVar14 = sVar3 - 0x18;
    local_30[2] = (short)local_20 + -0xf;
    uVar12 = extraout_ECX_05;
    goto LAB_00412cef;
  }
  _local_14 = CONCAT22(uStack_12,(short)local_20 + local_30[0]);
  uVar14 = sVar3 - 9;
  FUN_00411147((uint)unaff_BX,(int)sVar3);
  local_30[2] = (short)local_20;
  uVar12 = extraout_ECX_04;
LAB_00412cef:
  uStack_28 = uVar14;
switchD_0041262f_caseD_12:
  if ((((DAT_00508041 == pUVar13->proprietario_id) && (pUVar13->selecionada != 0)) ||
      (unaff_BX == DAT_00496ac2)) || (DAT_00508f8d._2_1_ != '\0')) {
    uVar12 = FUN_00410be4(uVar12,uStack_28);
    return uVar12;
  }
  pUVar8 = tabela_unidades + unaff_BX;
  if (*(short *)&pUVar8->field_0x4 == *(short *)&pUVar8->field_0x76) {
    puVar1 = &pUVar8->field_0x74;
    pUVar8 = (UnidadeParcial *)(uint)*(ushort *)puVar1;
    if (pUVar8 < (UnidadeParcial *)0x64) {
      uVar10 = CONCAT31((uint3)(byte)(*(ushort *)puVar1 >> 8),1);
      goto LAB_004135a2;
    }
  }
  uVar10 = (uint)pUVar8 & 0xffffff00;
LAB_004135a2:
  if (((char)uVar10 != '\0') &&
     (uVar9 = *(ushort *)&pUVar13->field_0x74 / 5, uVar10 = uVar9 / 2, uVar9 % 2 == 0)) {
    uVar10 = FUN_00442c34();
    uVar12 = extraout_ECX_08;
    if ((char)uVar10 != '\0') {
      if (*extraout_EDX == 200) {
        uVar10 = FUN_0045b247('\x01',uStack_28 - 2);
        uVar12 = extraout_ECX_09;
      }
      else {
        uVar10 = FUN_0045c455('\x01',uStack_28 - 2,*extraout_EDX);
        uVar12 = extraout_ECX_10;
      }
    }
  }
  if ((pUVar13->field_0xba != '\0') && (uVar10 = DAT_00508f7c / 5, DAT_00508f7c % 5 == 0)) {
    uVar16 = FUN_0044f9a6(uVar12,tabela_unidades + unaff_BX);
    cVar4 = FUN_004422b0();
    uVar10 = CONCAT31(extraout_var,cVar4);
    if ((cVar4 != '\0') && (uVar10 = 0, (char)uVar16 != '\0')) {
      uVar10 = FUN_0045b247('\x01',uStack_28 - 2);
    }
  }
  return uVar10;
}
