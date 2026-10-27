/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00450874, entrada 00450874.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN_00450874(uint param_1,uint param_2,char param_3)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  byte bVar4;
  short sVar5;
  uint uVar6;
  undefined4 uVar7;
  uint extraout_ECX;
  uint uVar8;
  int extraout_ECX_00;
  uint extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  uint extraout_ECX_04;
  undefined4 extraout_ECX_05;
  undefined4 extraout_ECX_06;
  undefined4 extraout_ECX_07;
  undefined4 extraout_ECX_08;
  undefined4 extraout_ECX_09;
  undefined4 extraout_ECX_10;
  undefined4 extraout_ECX_11;
  undefined4 extraout_ECX_12;
  undefined4 extraout_ECX_13;
  undefined4 extraout_ECX_14;
  undefined4 extraout_ECX_15;
  undefined4 extraout_ECX_16;
  UnidadeParcial *pUVar9;
  UnidadeParcial *extraout_ECX_17;
  UnidadeParcial *pUVar10;
  undefined4 extraout_ECX_18;
  undefined4 uVar11;
  undefined4 extraout_ECX_19;
  undefined4 extraout_ECX_20;
  undefined4 extraout_ECX_21;
  undefined4 extraout_ECX_22;
  undefined4 extraout_ECX_23;
  undefined4 extraout_ECX_24;
  undefined4 extraout_ECX_25;
  undefined4 extraout_ECX_26;
  undefined4 extraout_ECX_27;
  undefined4 extraout_ECX_28;
  undefined4 extraout_ECX_29;
  undefined4 extraout_ECX_30;
  undefined4 extraout_ECX_31;
  undefined4 extraout_ECX_32;
  ushort uVar12;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 extraout_EDX_02;
  undefined4 extraout_EDX_03;
  uint extraout_EDX_04;
  uint unaff_EBX;
  int iVar13;
  bool bVar14;
  longlong lVar15;
  undefined8 uVar16;
  ulonglong uVar17;
  uint uVar18;
  byte local_20;

  lVar15 = (ulonglong)param_2 << 0x20;
  bVar4 = (byte)param_2;
  if (param_3 == '\0') {
    lVar15 = FUN_0041b54a(param_1,param_2);
    uVar18 = (uint)lVar15;
    uVar8 = extraout_ECX;
  }
  else {
    uVar18 = 0xffff;
    uVar8 = param_1;
  }
  if ((uVar18 & 0xffff) == 0xffff) {
    uVar8 = FUN_004465df(uVar8,(short)uVar18);
    uVar18 = uVar8 & 0xffff;
    if (uVar18 == 0xffff) {
      return;
    }
    pUVar9 = tabela_unidades + uVar18;
    bVar1 = pUVar9->tipo_id;
    bVar2 = pUVar9->proprietario_id;
    pUVar10 = pUVar9;
    if (((bVar2 == 200) ||
        (uVar16 = FUN_0046d817(pUVar9,uVar18), pUVar10 = extraout_ECX_17, ((uint)uVar16 & 0xff) != 1
        )) || ((extraout_ECX_17->estado != 5 && (extraout_ECX_17->estado != 0x12)))) {
      if (bVar2 == 200) goto LAB_00450d8a;
      if (bVar1 < 0xf) {
        if (((2 < bVar1) && (3 < bVar1)) &&
           ((bVar1 < 8 || ((8 < bVar1 && ((bVar1 < 0xb || (0xc < bVar1)))))))) goto LAB_00450ba0;
LAB_00450b84:
        bVar14 = true;
      }
      else {
        if (bVar1 < 0x10) goto LAB_00450b84;
        if (bVar1 < 0x14) {
          if ((bVar1 < 0x11) || (0x11 < bVar1)) goto LAB_00450b84;
        }
        else if ((bVar1 < 0x17) || ((bVar1 < 0x19 || (bVar1 == 0x19)))) goto LAB_00450b84;
LAB_00450ba0:
        bVar14 = false;
      }
      if (((bVar14) && (uVar18 = FUN_00467d97(pUVar10,1), (char)uVar18 == '\0')) && (bVar4 == 1)) {
        bVar3 = tabela_unidades[unaff_EBX & 0xffff].tipo_id;
        if (((bVar3 == 0x11) || (bVar3 == 10)) ||
           ((bVar3 == 0x10 && ((bVar1 < 2 || ((2 < bVar1 && (bVar1 != 8)))))))) {
          bVar14 = false;
        }
        else {
          bVar14 = true;
        }
        if ((!bVar14) || (tabela_unidades[unaff_EBX & 0xffff].proprietario_id == bVar2))
        goto LAB_00450ce4;
        uVar16 = FUN_0046d817(unaff_EBX & 0xffff,(uint)bVar2);
        if (((uint)uVar16 & 0xff) == 1) {
          uVar11 = extraout_ECX_18;
          if ((pUVar9->estado == 7) || (0xfa < DAT_00508f7c - *(int *)&pUVar9->field_0x110)) {
LAB_00450ca8:
            FUN_00445a36(uVar11,'\x01');
          }
        }
        else {
          uVar16 = FUN_0046d817(extraout_ECX_18,(int)((ulonglong)uVar16 >> 0x20));
          if ((((uint)uVar16 & 0xff) == 2) && (uVar11 = extraout_ECX_19, pUVar9->estado == 7))
          goto LAB_00450ca8;
        }
      }
      else {
LAB_00450ce4:
        if ((param_2 & 0xff) == 3) {
          FUN_0041aee2();
        }
        iVar13 = FUN_00477042((uVar8 & 0xffff) * 0x114,tabela_unidades[uVar8 & 0xffff].celula_passo)
        ;
        uVar18 = FUN_004770ee(extraout_ECX_20,(byte)iVar13);
        if ((uVar18 & 0xffff) != 0xffff) goto LAB_00450b3d;
      }
    }
    else {
      sVar5 = FUN_004539f3(extraout_ECX_17,pUVar9->proprietario_id);
      if (sVar5 == -1) goto LAB_00450d8a;
      FUN_0041aee2();
LAB_00450b3d:
      FUN_004457d3();
    }
LAB_00450d8a:
    FUN_004502f0((char)param_1,bVar4);
    bVar14 = true;
    if (bVar1 < 0xe) {
      if (bVar1 < 6) {
        if ((bVar1 < 3) || (3 < bVar1)) goto LAB_00450de4;
      }
      else if ((bVar1 < 9) || (bVar1 < 0xb)) {
LAB_00450de4:
        bVar14 = true;
        goto LAB_00450de6;
      }
LAB_00450dd9:
      bVar14 = false;
    }
    else {
      if ((bVar1 < 0xf) || (bVar1 < 0x12)) goto LAB_00450dd9;
      if ((bVar1 < 0x13) || ((bVar1 < 0x17 || (bVar1 < 0x19)))) goto LAB_00450de4;
      if (bVar1 == 0x19) goto LAB_00450dd9;
    }
LAB_00450de6:
    if (bVar14) {
      uVar18 = 0;
LAB_00450e02:
      FUN_0046e44c(0,0,0,0,uVar18);
    }
    else {
      switch(bVar1) {
      case 0xb:
      case 0xc:
      case 0xd:
      case 0xe:
      case 0xf:
      case 0x10:
      case 0x11:
        bVar14 = true;
        break;
      default:
        bVar14 = false;
      }
      if (bVar14) {
        uVar18 = extraout_EDX_04 & 0xffffff00;
        if (bVar1 == 0x10) {
          uVar18 = CONCAT31((int3)(extraout_EDX_04 >> 8),1);
        }
        uVar17 = FUN_004704dc(extraout_ECX_21,uVar18);
        uVar18 = (uint)(uVar17 >> 0x20);
        if ((uVar17 & 1) == 0) {
          uVar18 = uVar18 & 0xff;
        }
        else {
          uVar18 = uVar18 & 0xff;
        }
        goto LAB_00450e02;
      }
    }
    if (bVar4 < 3) {
      bVar14 = bVar4 == 1;
    }
    else {
      if (bVar4 < 4) {
        uVar16 = FUN_0041a08c(0,uVar8 & 0xffff);
        iVar13 = (int)((ulonglong)uVar16 >> 0x20);
        bVar4 = (byte)uVar16;
        iVar13 = (((uVar8 & 0xffff) * 0x10 + iVar13) * 4 + iVar13) * 4;
        uVar7 = FUN_0046d838(CONCAT31((int3)((uint)extraout_ECX_22 >> 8),bVar4),
                             (&tabela_unidades->proprietario_id)[iVar13]);
        uVar11 = extraout_ECX_23;
        if ((char)uVar7 != '\0') {
          FUN_00475118(extraout_ECX_23,(uint)bVar4);
          FUN_00475118(extraout_ECX_24,(uint)bVar4);
          FUN_0046d8cb(extraout_ECX_25,(&tabela_unidades->proprietario_id)[iVar13]);
          FUN_0046d8cb(extraout_ECX_26,(byte)extraout_ECX_26);
          uVar11 = extraout_ECX_27;
        }
        bVar4 = tabela_unidades[uVar8 & 0xffff].proprietario_id;
        goto LAB_00450a93;
      }
      bVar14 = bVar4 == 4;
    }
    if (bVar14) {
      bVar4 = tabela_unidades[unaff_EBX & 0xffff].proprietario_id;
      uVar7 = FUN_0046d838((uint)bVar4,tabela_unidades[uVar8 & 0xffff].proprietario_id);
      uVar11 = extraout_ECX_28;
      if ((char)uVar7 != '\0') {
        FUN_00475118(extraout_ECX_28,(uint)bVar4);
        FUN_00475118(extraout_ECX_29,(uint)bVar4);
        FUN_0046d8cb(extraout_ECX_30,tabela_unidades[uVar8 & 0xffff].proprietario_id);
        FUN_0046d8cb(extraout_ECX_31,(byte)extraout_ECX_31);
        uVar11 = extraout_ECX_32;
      }
      FUN_0046d600(uVar11,tabela_unidades[uVar8 & 0xffff].proprietario_id);
      bVar1 = tabela_unidades[uVar8 & 0xffff].proprietario_id;
      if (((bVar1 != bVar4) && (bVar1 == DAT_00508041)) &&
         ((DAT_00508f7c < DAT_004e19c0 || (199 < DAT_00508f7c - DAT_004e19c0)))) {
        DAT_004e19c0 = DAT_00508f7c;
        DAT_00496acc = tabela_unidades[uVar8 & 0xffff].celula_passo;
        FUN_0048aa79(0,(uint)tabela_unidades[uVar8 & 0xffff].tipo_id << 0x10 | 0x700,0x100);
      }
    }
  }
  else {
    uVar6 = param_2 & 0xff;
    uVar8 = 2;
    if (uVar6 == 1) {
      pUVar10 = tabela_unidades + (unaff_EBX & 0xffff);
      uVar8 = FUN_00428cc0((uint)*(byte *)(*(int *)(DAT_004e199c + (uint)pUVar10->tipo_id * 4) +
                                          0x1a),5);
      local_20 = pUVar10->proprietario_id;
      FUN_00484808(extraout_ECX_00 + uVar8,4);
      uVar8 = extraout_ECX_01;
    }
    else if (uVar6 == 3) {
      uVar16 = FUN_0041a4f4(2,(int)((ulonglong)lVar15 >> 0x20));
      FUN_0041a4f4(extraout_ECX_02,(int)((ulonglong)uVar16 >> 0x20));
      uVar8 = FUN_00418b8a(extraout_ECX_03,3);
      uVar16 = FUN_0041a08c(uVar8,extraout_EDX);
      local_20 = (byte)uVar16;
      uVar8 = extraout_ECX_04;
    }
    else if (uVar6 == 4) {
      local_20 = tabela_unidades[unaff_EBX & 0xffff].proprietario_id;
      if ((param_1 & 0xff) == 0x1d) {
        uVar12 = _DAT_0049716c;
      }
      else {
        if ((param_1 & 0xff) != 0x1e) goto LAB_004509b2;
        uVar12 = _DAT_0049716e;
      }
      uVar8 = uVar12 / 2;
    }
LAB_004509b2:
    FUN_0041a2c1(uVar8,(short)uVar8);
    FUN_004704dc(extraout_ECX_05,extraout_EDX_00);
    FUN_0046e44c(0,0,0,0,0);
    uVar16 = FUN_0041a08c(uVar18 & 0xffff,0);
    uVar7 = FUN_0046d838(extraout_ECX_06,(byte)uVar16);
    uVar11 = extraout_ECX_07;
    if ((char)uVar7 != '\0') {
      FUN_0041a08c(extraout_ECX_07,extraout_EDX_01);
      FUN_00475118(extraout_ECX_08,(uint)local_20);
      FUN_0041a08c(extraout_ECX_09,extraout_EDX_02);
      FUN_00475118(extraout_ECX_10,(uint)local_20);
      uVar16 = FUN_0041a08c(extraout_ECX_11,0);
      FUN_0046d8cb(extraout_ECX_12,(byte)uVar16);
      FUN_0041a08c(extraout_ECX_13,extraout_EDX_03);
      FUN_0046d8cb(extraout_ECX_14,local_20);
      uVar11 = extraout_ECX_15;
    }
    uVar16 = FUN_0041a08c(uVar11,0);
    bVar4 = (byte)uVar16;
    uVar11 = extraout_ECX_16;
LAB_00450a93:
    FUN_0046d600(uVar11,bVar4);
  }
  return;
}
