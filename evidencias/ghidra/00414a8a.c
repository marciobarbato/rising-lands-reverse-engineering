/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00414a8a, entrada 00414a8a.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Removing unreachable block (ram,0x004150aa) */

uint __fastcall FUN_00414a8a(undefined4 param_1,undefined4 param_2)

{
  undefined1 *puVar1;
  byte bVar2;
  char cVar3;
  short sVar4;
  ushort uVar5;
  undefined2 uVar6;
  int in_EAX;
  uint uVar7;
  uint uVar8;
  UnidadeParcial *pUVar9;
  undefined3 extraout_var;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_ECX_01;
  uint extraout_ECX_02;
  uint extraout_ECX_03;
  uint extraout_ECX_04;
  uint extraout_ECX_05;
  uint extraout_ECX_06;
  short extraout_DX;
  uint extraout_EDX;
  short sVar10;
  uint unaff_EBX;
  UnidadeParcial *pUVar11;
  short sVar12;
  int iVar13;
  short local_4c [4];
  undefined4 local_44;
  short local_40 [2];
  int local_3c;
  undefined4 local_38;
  undefined4 local_34;
  ushort local_30;
  short sStack_2c;
  uint local_28;
  uint local_24;
  ushort local_20;
  undefined2 uStack_1e;
  short local_1c;
  undefined2 uStack_1a;
  short local_18;
  char local_14;

  local_34._0_2_ = (short)param_2;
  local_20 = (ushort)unaff_EBX;
  uStack_1e = (undefined2)(unaff_EBX >> 0x10);
  uVar8 = unaff_EBX & 0xffff;
  sStack_2c = 0;
  pUVar11 = tabela_unidades + uVar8;
  local_14 = '\x01';
  local_30 = 0;
  iVar13 = in_EAX + CONCAT22((short)(uVar8 * 0x114 >> 0x10),(short)pUVar11->deslocamento_x);
  local_40[0] = 0;
  local_40[1] = 0;
  local_44 = 0;
  local_1c = (short)local_34 + pUVar11->deslocamento_y;
  local_34 = param_2;
  uVar7 = FUN_00410fcc(uVar8,local_40);
  uVar8 = extraout_ECX;
  if ((pUVar11->selecionada != 0) && (DAT_00508041 == pUVar11->proprietario_id)) {
    local_38 = CONCAT22(uStack_1a,local_1c);
    FUN_0044106c(extraout_ECX,local_4c);
    if (local_4c[0] == 1) {
      sVar4 = local_1c;
    }
    else {
      sVar4 = (short)local_38 + -0x20;
    }
    local_3c = iVar13;
    FUN_0045b247('\x01',sVar4);
    uVar7 = 0;
    uVar8 = extraout_ECX_00;
    if (pUVar11->field_0x82 != '\0') {
      uVar8 = 0;
      local_28 = (uint)*(ushort *)&pUVar11->field_0xb2 % 0x100;
      local_24 = *(ushort *)&pUVar11->field_0xb2 / 0x100;
      if ((DAT_0050871e._2_2_ <= (ushort)local_28) &&
         (local_28 < (uint)DAT_00508724 + (uint)DAT_0050871e._2_2_)) {
        uVar8 = (uint)DAT_00508722;
        if ((DAT_00508722 <= (ushort)local_24) &&
           (local_24 < (uint)DAT_00508726 + (uint)DAT_00508722)) {
          FUN_0045b247('\x01',((ushort)local_24 - DAT_00508722) * 0x20);
          uVar8 = extraout_ECX_01;
        }
      }
      bVar2 = pUVar11->field_0x82;
      if (bVar2 != 0) {
        if (bVar2 < 2) {
          uVar5 = *(ushort *)&pUVar11->field_0x80;
        }
        else {
          if (bVar2 != 2) goto LAB_00414c75;
          uVar5 = FUN_0041aee2();
        }
        uVar8 = 0;
        local_28 = (uint)uVar5 % 0x100;
        local_24 = uVar5 / 0x100;
      }
LAB_00414c75:
      uVar7 = local_28;
      if ((((DAT_0050871e._2_2_ <= (ushort)local_28) &&
           (uVar7 = (uint)DAT_00508724 + (uint)DAT_0050871e._2_2_, (local_28 & 0xffff) < uVar7)) &&
          (uVar7 = local_24, DAT_00508722 <= (ushort)local_24)) &&
         (uVar7 = (uint)DAT_00508722 + (uint)DAT_00508726, (local_24 & 0xffff) < uVar7)) {
        uVar7 = FUN_0045b247('\x01',((ushort)local_24 - DAT_00508722) * 0x20);
        uVar8 = extraout_ECX_02;
      }
    }
  }
  sVar4 = local_1c;
  bVar2 = pUVar11->tipo_id;
  uVar7 = CONCAT31((int3)(uVar7 >> 8),bVar2);
  sVar10 = local_1c + 0x1a;
  sVar12 = (short)iVar13;
  if (bVar2 < 6) {
    if (bVar2 == 5) {
      bVar2 = pUVar11->field_0x89;
      if (bVar2 == 0) {
LAB_00414f92:
        uVar6 = FUN_004470b9();
        if ((char)uVar6 == '\0') {
          FUN_0045b796('\x01',sVar4 + 0x1a);
        }
        else {
          FUN_0045b796('\x01',sVar4 + 0x1a);
        }
      }
      else {
        if (1 < bVar2) {
          if (3 < bVar2) goto LAB_00414f7c;
          goto LAB_00414f92;
        }
        FUN_0045b796('\x01',sVar10);
      }
      local_18 = local_40[0] + sVar12;
      FUN_00411147((uint)local_20,(int)(short)(local_1c + (short)local_44));
      uVar8 = extraout_ECX_04;
      goto LAB_00414f7c;
    }
  }
  else {
    if (bVar2 < 7) {
      bVar2 = pUVar11->field_0x89;
      if (bVar2 < 2) {
        uVar6 = FUN_004470b9();
        if ((char)uVar6 == '\0') goto LAB_0041522b;
        FUN_0045b796('\x01',sVar10);
      }
      else {
        if (2 < bVar2) {
          if (bVar2 == 3) {
            local_14 = '\0';
          }
          goto LAB_00414f7c;
        }
LAB_0041522b:
        FUN_0045b796('\x01',sVar10);
      }
      local_18 = local_40[0] + sVar12;
      FUN_00411147((uint)local_20,(int)(short)(local_1c + (short)local_44));
      uVar8 = extraout_ECX_06;
    }
    else if (bVar2 < 8) {
      bVar2 = pUVar11->field_0x89;
      if (bVar2 < 3) {
        if (bVar2 == 0) goto LAB_004150af;
        local_14 = '\0';
      }
      else {
        if ((bVar2 < 4) || (bVar2 < 6)) {
LAB_004150af:
          uVar6 = FUN_004470b9();
          if ((char)uVar6 == '\0') {
            FUN_0045b796('\x01',extraout_DX + 0x1a);
          }
          else {
            FUN_0045b796('\x01',extraout_DX + 0x1a);
          }
        }
        else {
          if (bVar2 != 0xc) goto LAB_00414f7c;
          FUN_0045b796('\x01',sVar10);
        }
        local_18 = local_40[0] + sVar12;
        FUN_00411147((uint)local_20,(int)(short)(local_1c + (short)local_44));
        uVar8 = extraout_ECX_05;
      }
    }
    else {
      if (bVar2 != 0xd) goto LAB_004152c9;
      bVar2 = pUVar11->field_0x89;
      if (bVar2 == 0) {
LAB_00414d98:
        FUN_0045b796('\x01',local_1c + (short)local_44);
      }
      else {
        if (1 < bVar2) {
          if (4 < bVar2) goto LAB_00414f7c;
          goto LAB_00414d98;
        }
        FUN_0045b796('\x01',local_1c + (short)local_44);
      }
      local_18 = local_40[0] + sVar12;
      FUN_00411147((uint)local_20,(int)(short)(local_1c + (short)local_44));
      uVar8 = extraout_ECX_03;
    }
LAB_00414f7c:
    uVar7 = CONCAT22(uStack_1a,local_1c) - 9;
    local_30 = (ushort)uVar7;
    sStack_2c = sVar12;
  }
LAB_004152c9:
  if (local_14 == '\0') {
    return uVar7;
  }
  if (((DAT_00508041 == pUVar11->proprietario_id) && (pUVar11->selecionada != 0)) ||
     ((local_20 == DAT_00496ac2 || (DAT_00508f8d._2_1_ != '\0')))) {
    uVar8 = FUN_00410be4(CONCAT22((short)(uVar8 >> 0x10),CONCAT11(DAT_00508041,(char)uVar8)),
                         local_30);
    return uVar8;
  }
  pUVar9 = tabela_unidades + local_20;
  if (*(short *)&pUVar9->field_0x4 == *(short *)&pUVar9->field_0x76) {
    puVar1 = &pUVar9->field_0x74;
    pUVar9 = (UnidadeParcial *)(uint)*(ushort *)puVar1;
    if (pUVar9 < (UnidadeParcial *)0x64) {
      uVar8 = CONCAT31((uint3)(byte)(*(ushort *)puVar1 >> 8),1);
      goto LAB_00415356;
    }
  }
  uVar8 = (uint)pUVar9 & 0xffffff00;
LAB_00415356:
  if (((char)uVar8 != '\0') &&
     (uVar7 = *(ushort *)&pUVar11->field_0x74 / 5, uVar8 = uVar7 / 2, uVar7 % 2 == 0)) {
    pUVar9 = tabela_unidades + local_20;
    uVar8 = FUN_00442c34();
    if ((char)uVar8 != '\0') {
      if (pUVar9->proprietario_id == 200) {
        uVar8 = FUN_0045b247('\x01',local_30 - 2);
      }
      else {
        uVar8 = FUN_0045c455('\x01',local_30 - 2,pUVar9->proprietario_id);
      }
    }
  }
  if ((pUVar11->field_0xba != '\0') && (uVar8 = DAT_00508f7c / 5, DAT_00508f7c % 5 == 0)) {
    FUN_0044f9a6(tabela_unidades + local_20,(uint)(local_20 & 0xff));
    cVar3 = FUN_004422b0();
    uVar8 = CONCAT31(extraout_var,cVar3);
    if ((cVar3 != '\0') && (uVar8 = 0, (extraout_EDX & 0xffff) != 0)) {
      uVar8 = FUN_0045b247('\x01',local_30 - 2);
    }
  }
  return uVar8;
}
