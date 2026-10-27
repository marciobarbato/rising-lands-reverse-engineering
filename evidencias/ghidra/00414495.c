/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00414495, entrada 00414495.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

char * __fastcall FUN_00414495(undefined4 param_1,short param_2)

{
  undefined1 *puVar1;
  sbyte sVar2;
  byte bVar3;
  ushort uVar4;
  char cVar5;
  short in_AX;
  undefined2 uVar6;
  char *pcVar7;
  UnidadeParcial *pUVar8;
  undefined3 extraout_var;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 uVar9;
  undefined4 extraout_ECX_03;
  undefined3 uVar10;
  uint uVar11;
  byte *extraout_EDX;
  uint extraout_EDX_00;
  ushort unaff_BX;
  short sVar12;
  UnidadeParcial *pUVar13;
  short sVar14;
  ushort uVar15;
  short local_38 [6];
  undefined4 local_2c;
  ushort uStack_24;
  short sStack_20;
  undefined2 uStack_12;

  sStack_20 = 0;
  pUVar13 = tabela_unidades + unaff_BX;
  sVar2 = pUVar13->deslocamento_x;
  uStack_24 = 0;
  local_38[0] = 0;
  local_38[1] = 0;
  local_38[2] = 0;
  local_38[3] = 0;
  sVar14 = param_2 + pUVar13->deslocamento_y;
  FUN_00410fcc((uint)unaff_BX,local_38);
  uVar11 = extraout_ECX;
  if (pUVar13->selecionada != 0) {
    local_2c = CONCAT22(uStack_12,sVar14);
    FUN_0044106c(extraout_ECX,local_38 + 4);
    if (local_38[4] == 1) {
      sVar12 = sVar14;
    }
    else {
      sVar12 = (short)local_2c + -0x20;
    }
    FUN_0045b247('\x01',sVar12);
    uVar11 = extraout_ECX_00;
    if (((pUVar13->tipo_id == 7) && (pUVar13->field_0xbe == '\t')) &&
       (*(short *)&pUVar13->field_0xd8 != 0)) {
      for (uVar15 = 0; uVar15 < *(ushort *)&pUVar13->field_0xd8; uVar15 = uVar15 + 1) {
        uVar11 = (uint)*(ushort *)(&pUVar13->field_0xc4 + (uint)uVar15 * 2) % 0x100;
        if (((DAT_0050871e._2_2_ <= (ushort)uVar11) &&
            (uVar11 < (uint)DAT_00508724 + (uint)DAT_0050871e._2_2_)) &&
           ((uVar4 = *(ushort *)(&pUVar13->field_0xc4 + (uint)uVar15 * 2) >> 8,
            DAT_00508722 <= uVar4 && ((uint)uVar4 < (uint)DAT_00508726 + (uint)DAT_00508722)))) {
          FUN_0045b247('\x01',(uVar4 - DAT_00508722) * 0x20);
          uVar11 = extraout_ECX_01;
        }
      }
    }
  }
  bVar3 = pUVar13->tipo_id;
  uVar10 = (undefined3)(uVar11 >> 8);
  uVar9 = CONCAT31(uVar10,bVar3);
  if (5 < bVar3) {
    sVar12 = sVar14 + 0x1a;
    if (bVar3 < 7) {
      cVar5 = pUVar13->field_0x89;
      uVar9 = CONCAT31(uVar10,cVar5);
      if (cVar5 == '\0') {
        uVar6 = FUN_004470b9();
        if ((char)uVar6 == '\0') {
          FUN_0045b796('\x01',sVar12);
        }
        else {
          FUN_0045b796('\x01',sVar12);
        }
      }
      else {
        if (cVar5 != '\x01') goto LAB_0041477e;
        FUN_0045b796('\x01',sVar12);
      }
      FUN_00411147((uint)unaff_BX,(int)(short)(sVar14 + local_38[2]));
      uVar9 = extraout_ECX_03;
    }
    else {
      if (bVar3 != 7) goto LAB_004148ba;
      cVar5 = pUVar13->field_0x89;
      uVar9 = CONCAT31(uVar10,cVar5);
      if (cVar5 == '\0') {
        uVar6 = FUN_004470b9();
        if ((char)uVar6 == '\0') {
          FUN_0045b796('\x01',sVar12);
        }
        else {
          FUN_0045b796('\x01',sVar12);
        }
        sVar12 = local_38[2];
      }
      else {
        if (cVar5 != '\x01') goto LAB_0041477e;
        FUN_0045b796('\x01',sVar12);
        sVar12 = local_38[2];
      }
      FUN_00411147((uint)unaff_BX,(int)(short)(sVar14 + sVar12));
      uVar9 = extraout_ECX_02;
    }
LAB_0041477e:
    uStack_24 = sVar14 - 9;
    sStack_20 = in_AX + sVar2;
  }
LAB_004148ba:
  if (((DAT_00508041 == pUVar13->proprietario_id) && (pUVar13->selecionada != 0)) ||
     ((unaff_BX == DAT_00496ac2 || (DAT_00508f8d._2_1_ != '\0')))) {
    pcVar7 = (char *)FUN_00410be4(uVar9,uStack_24);
    return pcVar7;
  }
  pUVar8 = tabela_unidades + unaff_BX;
  if (*(short *)&pUVar8->field_0x4 == *(short *)&pUVar8->field_0x76) {
    puVar1 = &pUVar8->field_0x74;
    pUVar8 = (UnidadeParcial *)(uint)*(ushort *)puVar1;
    if (pUVar8 < (UnidadeParcial *)0x64) {
      pcVar7 = (char *)CONCAT31((uint3)(byte)(*(ushort *)puVar1 >> 8),1);
      goto LAB_00414948;
    }
  }
  pcVar7 = (char *)((uint)pUVar8 & 0xffffff00);
LAB_00414948:
  if ((((char)pcVar7 != '\0') &&
      (uVar11 = *(ushort *)&pUVar13->field_0x74 / 5, pcVar7 = (char *)(uVar11 / 2), uVar11 % 2 == 0)
      ) && (pcVar7 = (char *)FUN_00442c34(), (char)pcVar7 != '\0')) {
    if (*extraout_EDX == 200) {
      pcVar7 = (char *)FUN_0045b247('\x01',uStack_24 - 2);
    }
    else {
      pcVar7 = (char *)FUN_0045c455('\x01',uStack_24 - 2,*extraout_EDX);
    }
  }
  if ((pUVar13->field_0xba != '\0') && (pcVar7 = (char *)(DAT_00508f7c / 5), DAT_00508f7c % 5 == 0))
  {
    FUN_0044f9a6(tabela_unidades + unaff_BX,(uint)(unaff_BX & 0xff));
    cVar5 = FUN_004422b0();
    pcVar7 = (char *)CONCAT31(extraout_var,cVar5);
    if ((cVar5 != '\0') && (pcVar7 = (char *)0x0, (extraout_EDX_00 & 0xffff) != 0)) {
      pcVar7 = (char *)FUN_0045b247('\x01',uStack_24 - 2);
    }
  }
  return pcVar7;
}
