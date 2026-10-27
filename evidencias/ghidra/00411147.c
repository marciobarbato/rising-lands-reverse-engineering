/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00411147, entrada 00411147.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00411147(uint param_1,undefined4 param_2)

{
  char cVar1;
  byte bVar2;
  byte bVar3;
  ushort indice_unidade;
  short sVar4;
  ushort extraout_CX;
  undefined4 extraout_ECX;
  undefined4 uVar5;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
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
  undefined4 extraout_ECX_17;
  undefined4 extraout_ECX_18;
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
  undefined4 extraout_ECX_33;
  undefined4 extraout_ECX_34;
  undefined4 extraout_ECX_35;
  undefined4 extraout_ECX_36;
  undefined4 extraout_ECX_37;
  undefined4 extraout_ECX_38;
  undefined4 extraout_ECX_39;
  undefined4 extraout_ECX_40;
  undefined4 extraout_ECX_41;
  undefined4 extraout_ECX_42;
  undefined4 extraout_ECX_43;
  undefined4 extraout_ECX_44;
  undefined4 extraout_ECX_45;
  undefined4 extraout_ECX_46;
  undefined4 extraout_ECX_47;
  undefined4 extraout_ECX_48;
  undefined4 extraout_ECX_49;
  undefined4 extraout_ECX_50;
  undefined4 extraout_ECX_51;
  undefined4 extraout_ECX_52;
  undefined4 extraout_ECX_53;
  undefined4 extraout_ECX_54;
  undefined4 extraout_ECX_55;
  undefined4 extraout_ECX_56;
  undefined4 extraout_ECX_57;
  undefined4 extraout_ECX_58;
  undefined4 extraout_ECX_59;
  undefined4 extraout_ECX_60;
  undefined4 extraout_ECX_61;
  undefined4 extraout_ECX_62;
  undefined4 extraout_ECX_63;
  undefined4 extraout_ECX_64;
  undefined4 extraout_ECX_65;
  uint extraout_ECX_66;
  undefined4 extraout_EDX;
  uint extraout_EDX_00;
  uint uVar6;
  undefined4 extraout_EDX_01;
  undefined4 extraout_EDX_02;
  undefined4 uVar7;
  undefined4 extraout_EDX_03;
  uint extraout_EDX_04;
  undefined4 extraout_EDX_05;
  undefined4 extraout_EDX_06;
  undefined4 extraout_EDX_07;
  undefined4 extraout_EDX_08;
  undefined4 extraout_EDX_09;
  undefined4 extraout_EDX_10;
  undefined4 extraout_EDX_11;
  undefined4 extraout_EDX_12;
  undefined4 extraout_EDX_13;
  undefined4 extraout_EDX_14;
  undefined4 extraout_EDX_15;
  undefined4 extraout_EDX_16;
  undefined4 extraout_EDX_17;
  undefined4 extraout_EDX_18;
  undefined4 extraout_EDX_19;
  uint extraout_EDX_20;
  undefined4 extraout_EDX_21;
  undefined4 extraout_EDX_22;
  undefined4 extraout_EDX_23;
  undefined4 extraout_EDX_24;
  undefined4 extraout_EDX_25;
  undefined4 extraout_EDX_26;
  undefined4 extraout_EDX_27;
  undefined4 extraout_EDX_28;
  undefined4 extraout_EDX_29;
  undefined4 extraout_EDX_30;
  undefined4 extraout_EDX_31;
  undefined4 extraout_EDX_32;
  undefined4 extraout_EDX_33;
  undefined4 extraout_EDX_34;
  undefined4 extraout_EDX_35;
  undefined4 extraout_EDX_36;
  uint extraout_EDX_37;
  undefined4 extraout_EDX_38;
  undefined4 extraout_EDX_39;
  undefined4 extraout_EDX_40;
  undefined4 extraout_EDX_41;
  undefined4 extraout_EDX_42;
  undefined4 extraout_EDX_43;
  undefined4 extraout_EDX_44;
  undefined4 extraout_EDX_45;
  undefined4 extraout_EDX_46;
  undefined4 extraout_EDX_47;
  undefined4 extraout_EDX_48;
  int3 iVar8;
  undefined4 unaff_EBX;
  undefined8 uVar9;
  undefined8 uVar10;
  short local_28;
  undefined4 local_24;
  int local_20;
  short local_1c [2];
  undefined2 local_18;
  undefined2 uStack_16;
  short local_14;
  byte local_10;

  local_18 = (undefined2)unaff_EBX;
  uStack_16 = (undefined2)((uint)unaff_EBX >> 0x10);
  indice_unidade = (ushort)param_1;
  local_14 = (short)param_2;
  local_10 = unidade_obter_proprietario(indice_unidade);
  sVar4 = local_14;
  uVar5 = extraout_ECX;
  if (local_10 < 4) {
    if (local_10 != 0) goto LAB_0041118a;
    cVar1 = FUN_0044fffe(extraout_ECX);
    uVar5 = extraout_ECX_06;
    if (cVar1 == '\0') {
      cVar1 = FUN_0045002e(extraout_ECX_06,extraout_EDX_03);
      uVar5 = extraout_ECX_07;
      if (cVar1 != '\0') goto LAB_0041133a;
LAB_0041137e:
      sVar4 = local_14;
      FUN_0045b247('\x01',local_14);
      bVar2 = unidade_obter_tipo(indice_unidade);
      if (bVar2 == 0xf) {
        FUN_00440e31(extraout_ECX_09,extraout_EDX_05);
      }
      else {
        bVar2 = unidade_obter_tipo((ushort)extraout_EDX_05);
        uVar5 = extraout_ECX_11;
        uVar7 = extraout_EDX_07;
        if (bVar2 != 0xc) goto LAB_00411265;
        FUN_00440e31(extraout_ECX_11,extraout_EDX_07);
      }
      FUN_0045b247('\x01',sVar4);
      uVar5 = extraout_ECX_10;
      uVar7 = extraout_EDX_06;
      goto LAB_00411265;
    }
LAB_0041133a:
    cVar1 = FUN_0044fffe(uVar5);
    uVar6 = extraout_EDX_04;
    if (cVar1 != '\0') {
      uVar6 = (uint)(byte)(&DAT_004e1c18)[DAT_004e1d18] % 2;
      DAT_004e1d18 = DAT_004e1d18 + 1;
      if (uVar6 == 0) goto LAB_0041137e;
    }
    cVar1 = FUN_0045002e(extraout_ECX_08,uVar6);
    sVar4 = local_14;
    if (cVar1 != '\0') {
      FUN_0045b247('\x01',local_14);
      bVar2 = unidade_obter_tipo(indice_unidade);
      if (bVar2 == 0xf) {
        FUN_00440e31(extraout_ECX_13,extraout_EDX_08);
LAB_004114a8:
        FUN_0045b247('\x01',sVar4);
      }
      else {
        bVar2 = unidade_obter_tipo(indice_unidade);
        if (bVar2 == 0xc) {
          FUN_00440e31(extraout_ECX_14,extraout_EDX_09);
          goto LAB_004114a8;
        }
      }
      sVar4 = local_14;
      FUN_0045bcb0('\x01',local_14);
      bVar2 = unidade_obter_tipo(indice_unidade);
      if (bVar2 == 0xf) {
        FUN_00440e31(extraout_ECX_15,extraout_EDX_10);
      }
      else {
        bVar2 = unidade_obter_tipo((ushort)extraout_EDX_10);
        uVar5 = extraout_ECX_16;
        uVar7 = extraout_EDX_11;
        if (bVar2 != 0xc) goto LAB_00411265;
        FUN_00440e31(extraout_ECX_16,extraout_EDX_11);
      }
      goto LAB_00411e42;
    }
    cVar1 = FUN_0044fffe(extraout_ECX_12);
    sVar4 = local_14;
    uVar5 = extraout_ECX_17;
    uVar7 = extraout_EDX_12;
    if (cVar1 == '\0') goto LAB_00411265;
    FUN_0045ba23('\x01',local_14);
    bVar2 = unidade_obter_tipo(indice_unidade);
    if (bVar2 == 0xf) {
      FUN_00440e31(extraout_ECX_18,extraout_EDX_13);
    }
    else {
      bVar2 = unidade_obter_tipo(indice_unidade);
      uVar5 = extraout_ECX_19;
      uVar7 = extraout_EDX_14;
      if (bVar2 != 0xc) goto LAB_00411265;
      FUN_00440e31(extraout_ECX_19,extraout_EDX_14);
    }
LAB_00411eeb:
    FUN_0045ba23('\x01',sVar4);
    uVar5 = extraout_ECX_63;
    uVar7 = extraout_EDX_46;
    goto LAB_00411265;
  }
  if (local_10 < 5) {
    bVar2 = unidade_obter_tipo(indice_unidade);
    if ((bVar2 < 0x14) || ((0x16 < bVar2 && (0x18 < bVar2)))) {
      cVar1 = FUN_0044fffe(extraout_ECX_48);
      uVar5 = extraout_ECX_49;
      if (cVar1 == '\0') {
        cVar1 = FUN_0045002e(extraout_ECX_49,extraout_EDX_36);
        uVar5 = extraout_ECX_50;
        if (cVar1 != '\0') goto LAB_00411c29;
LAB_00411c6d:
        bVar2 = local_10;
        sVar4 = local_14;
        FUN_0045c455('\x01',local_14,local_10);
        bVar3 = unidade_obter_tipo(indice_unidade);
        if (bVar3 == 0xf) {
          FUN_00440e31(extraout_ECX_52,extraout_EDX_38);
        }
        else {
          bVar3 = unidade_obter_tipo((ushort)extraout_EDX_38);
          uVar5 = extraout_ECX_38;
          if (bVar3 != 0xc) goto LAB_0041118a;
          FUN_00440e31(extraout_ECX_38,extraout_EDX_29);
        }
        FUN_0045c455('\x01',sVar4,bVar2);
        uVar5 = extraout_ECX_53;
        goto LAB_0041118a;
      }
LAB_00411c29:
      cVar1 = FUN_0044fffe(uVar5);
      uVar6 = extraout_EDX_37;
      if (cVar1 != '\0') {
        uVar6 = (uint)(byte)(&DAT_004e1c18)[DAT_004e1d18] % 2;
        DAT_004e1d18 = DAT_004e1d18 + 1;
        if (uVar6 == 0) goto LAB_00411c6d;
      }
      cVar1 = FUN_0045002e(extraout_ECX_51,uVar6);
      sVar4 = local_14;
      if (cVar1 == '\0') {
        cVar1 = FUN_0044fffe(extraout_ECX_39);
        sVar4 = local_14;
        uVar5 = extraout_ECX_44;
        if (cVar1 == '\0') goto LAB_0041118a;
        FUN_0045ba23('\x01',local_14);
        bVar2 = unidade_obter_tipo(indice_unidade);
        if (bVar2 == 0xf) {
          FUN_00440e31(extraout_ECX_45,extraout_EDX_34);
        }
        else {
          bVar2 = unidade_obter_tipo(indice_unidade);
          uVar5 = extraout_ECX_47;
          if (bVar2 != 0xc) goto LAB_0041118a;
          FUN_00440e31(extraout_ECX_47,extraout_EDX_35);
        }
        goto LAB_00411bba;
      }
      uVar6 = (uint)local_10;
      FUN_0045c455('\x01',local_14,local_10);
      bVar2 = unidade_obter_tipo(indice_unidade);
      if (bVar2 == 0xf) {
        FUN_00440e31(uVar6,extraout_EDX_30);
        bVar2 = (byte)uVar6;
LAB_00411aa5:
        FUN_0045c455('\x01',sVar4,bVar2);
      }
      else {
        bVar2 = unidade_obter_tipo(indice_unidade);
        if (bVar2 == 0xc) {
          FUN_00440e31(extraout_ECX_40,extraout_EDX_31);
          bVar2 = (byte)uVar6;
          goto LAB_00411aa5;
        }
      }
      sVar4 = local_14;
      FUN_0045bcb0('\x01',local_14);
      bVar2 = unidade_obter_tipo(indice_unidade);
      if (bVar2 == 0xf) {
        FUN_00440e31(extraout_ECX_41,extraout_EDX_32);
      }
      else {
        bVar2 = unidade_obter_tipo((ushort)extraout_EDX_32);
        uVar5 = extraout_ECX_43;
        if (bVar2 != 0xc) goto LAB_0041118a;
        FUN_00440e31(extraout_ECX_43,extraout_EDX_33);
      }
      goto LAB_00411b11;
    }
    cVar1 = FUN_0044fffe(extraout_ECX_48);
    uVar5 = extraout_ECX_24;
    if (cVar1 == '\0') {
      cVar1 = FUN_0045002e(extraout_ECX_24,extraout_EDX_19);
      uVar5 = extraout_ECX_25;
      if (cVar1 != '\0') goto LAB_00411707;
LAB_0041174b:
      sVar4 = local_14;
      FUN_0045b247('\x01',local_14);
      bVar2 = unidade_obter_tipo(indice_unidade);
      if (bVar2 == 0xf) {
        FUN_00440e31(extraout_ECX_27,extraout_EDX_21);
      }
      else {
        bVar2 = unidade_obter_tipo((ushort)extraout_EDX_21);
        uVar5 = extraout_ECX_29;
        if (bVar2 != 0xc) goto LAB_0041118a;
        FUN_00440e31(extraout_ECX_29,extraout_EDX_22);
      }
      FUN_0045b247('\x01',sVar4);
      uVar5 = extraout_ECX_28;
    }
    else {
LAB_00411707:
      cVar1 = FUN_0044fffe(uVar5);
      uVar6 = extraout_EDX_20;
      if (cVar1 != '\0') {
        uVar6 = (uint)(byte)(&DAT_004e1c18)[DAT_004e1d18] % 2;
        DAT_004e1d18 = DAT_004e1d18 + 1;
        if (uVar6 == 0) goto LAB_0041174b;
      }
      cVar1 = FUN_0045002e(extraout_ECX_26,uVar6);
      sVar4 = local_14;
      if (cVar1 == '\0') {
        cVar1 = FUN_0044fffe(extraout_ECX_30);
        sVar4 = local_14;
        uVar5 = extraout_ECX_35;
        if (cVar1 != '\0') {
          FUN_0045ba23('\x01',local_14);
          bVar2 = unidade_obter_tipo(indice_unidade);
          if (bVar2 == 0xf) {
            FUN_00440e31(extraout_ECX_36,extraout_EDX_27);
          }
          else {
            bVar2 = unidade_obter_tipo(indice_unidade);
            uVar5 = extraout_ECX_37;
            if (bVar2 != 0xc) goto LAB_0041118a;
            FUN_00440e31(extraout_ECX_37,extraout_EDX_28);
          }
LAB_00411bba:
          FUN_0045ba23('\x01',sVar4);
          uVar5 = extraout_ECX_46;
        }
      }
      else {
        FUN_0045b247('\x01',local_14);
        bVar2 = unidade_obter_tipo(indice_unidade);
        if (bVar2 == 0xf) {
          FUN_00440e31(extraout_ECX_31,extraout_EDX_23);
LAB_00411875:
          FUN_0045b247('\x01',sVar4);
        }
        else {
          bVar2 = unidade_obter_tipo(indice_unidade);
          if (bVar2 == 0xc) {
            FUN_00440e31(extraout_ECX_32,extraout_EDX_24);
            goto LAB_00411875;
          }
        }
        sVar4 = local_14;
        FUN_0045bcb0('\x01',local_14);
        bVar2 = unidade_obter_tipo(indice_unidade);
        if (bVar2 == 0xf) {
          FUN_00440e31(extraout_ECX_33,extraout_EDX_25);
        }
        else {
          bVar2 = unidade_obter_tipo((ushort)extraout_EDX_25);
          uVar5 = extraout_ECX_34;
          if (bVar2 != 0xc) goto LAB_0041118a;
          FUN_00440e31(extraout_ECX_34,extraout_EDX_26);
        }
LAB_00411b11:
        FUN_0045bcb0('\x01',sVar4);
        uVar5 = extraout_ECX_42;
      }
    }
LAB_0041118a:
    cVar1 = FUN_0044fffe(uVar5);
    uVar5 = extraout_ECX_00;
    if (cVar1 == '\0') {
      cVar1 = FUN_0045002e(extraout_ECX_00,extraout_EDX);
      uVar5 = extraout_ECX_01;
      if (cVar1 != '\0') goto LAB_004111a5;
LAB_004111e9:
      sVar4 = local_14;
      uVar6 = (uint)local_10;
      FUN_0045c455('\x01',local_14,local_10);
      bVar2 = unidade_obter_tipo(indice_unidade);
      if (bVar2 == 0xf) {
        FUN_00440e31(extraout_ECX_03,extraout_EDX_01);
        bVar2 = (byte)uVar6;
      }
      else {
        bVar2 = unidade_obter_tipo((ushort)extraout_EDX_01);
        uVar5 = extraout_ECX_54;
        uVar7 = extraout_EDX_39;
        if (bVar2 != 0xc) goto LAB_00411265;
        FUN_00440e31(uVar6,extraout_EDX_39);
        bVar2 = (byte)uVar6;
      }
      FUN_0045c455('\x01',sVar4,bVar2);
      uVar5 = extraout_ECX_04;
      uVar7 = extraout_EDX_02;
      goto LAB_00411265;
    }
LAB_004111a5:
    cVar1 = FUN_0044fffe(uVar5);
    uVar6 = extraout_EDX_00;
    if (cVar1 != '\0') {
      uVar6 = (uint)(byte)(&DAT_004e1c18)[DAT_004e1d18] % 2;
      DAT_004e1d18 = DAT_004e1d18 + 1;
      if (uVar6 == 0) goto LAB_004111e9;
    }
    cVar1 = FUN_0045002e(extraout_ECX_02,uVar6);
    sVar4 = local_14;
    if (cVar1 == '\0') {
      cVar1 = FUN_0044fffe(extraout_ECX_55);
      sVar4 = local_14;
      uVar5 = extraout_ECX_61;
      uVar7 = extraout_EDX_44;
      if (cVar1 == '\0') goto LAB_00411265;
      FUN_0045ba23('\x01',local_14);
      bVar2 = unidade_obter_tipo(indice_unidade);
      if (bVar2 == 0xf) {
        FUN_00440e31(extraout_ECX_62,extraout_EDX_45);
      }
      else {
        bVar2 = unidade_obter_tipo(indice_unidade);
        uVar5 = extraout_ECX_64;
        uVar7 = extraout_EDX_47;
        if (bVar2 != 0xc) goto LAB_00411265;
        FUN_00440e31(extraout_ECX_64,extraout_EDX_47);
      }
      goto LAB_00411eeb;
    }
    uVar6 = (uint)local_10;
    FUN_0045c455('\x01',local_14,local_10);
    bVar2 = unidade_obter_tipo(indice_unidade);
    if (bVar2 == 0xf) {
      FUN_00440e31(extraout_ECX_56,uVar6);
      bVar2 = (byte)uVar6;
LAB_00411dd2:
      FUN_0045c455('\x01',sVar4,bVar2);
    }
    else {
      bVar2 = unidade_obter_tipo(indice_unidade);
      if (bVar2 == 0xc) {
        FUN_00440e31(extraout_ECX_57,extraout_EDX_40);
        bVar2 = (byte)uVar6;
        goto LAB_00411dd2;
      }
    }
    sVar4 = local_14;
    FUN_0045bcb0('\x01',local_14);
    bVar2 = unidade_obter_tipo(indice_unidade);
    if (bVar2 == 0xf) {
      FUN_00440e31(extraout_ECX_58,extraout_EDX_41);
    }
    else {
      bVar2 = unidade_obter_tipo((ushort)extraout_EDX_41);
      uVar5 = extraout_ECX_60;
      uVar7 = extraout_EDX_43;
      if (bVar2 != 0xc) goto LAB_00411265;
      FUN_00440e31(extraout_ECX_60,extraout_EDX_43);
    }
  }
  else {
    if (local_10 != 200) goto LAB_0041118a;
    FUN_0045b247('\x01',local_14);
    FUN_0045bcb0('\x01',sVar4);
    bVar2 = unidade_obter_tipo(indice_unidade);
    if (bVar2 == 0xf) {
      FUN_00440e31(extraout_ECX_20,extraout_EDX_15);
      FUN_0045b247('\x01',sVar4);
      FUN_00440e31(extraout_ECX_21,extraout_EDX_16);
    }
    else {
      bVar2 = unidade_obter_tipo(indice_unidade);
      uVar5 = extraout_ECX_22;
      uVar7 = extraout_EDX_17;
      if (bVar2 != 0xc) goto LAB_00411265;
      FUN_00440e31(extraout_ECX_22,extraout_EDX_17);
      FUN_0045b247('\x01',sVar4);
      FUN_00440e31(extraout_ECX_23,extraout_EDX_18);
    }
  }
LAB_00411e42:
  FUN_0045bcb0('\x01',sVar4);
  uVar5 = extraout_ECX_59;
  uVar7 = extraout_EDX_42;
LAB_00411265:
  cVar1 = FUN_00450054(uVar5,uVar7);
  if (cVar1 != '\0') {
    local_24 = 0;
    unidade_obter_tipo(indice_unidade);
    FUN_00410fcc(extraout_ECX_05,(short *)&local_24);
    FUN_0044106c(local_24,local_1c);
    if ((local_1c[0] == 2) && (local_28 == 2)) {
      sVar4 = local_14 + -0x2a;
    }
    else {
      sVar4 = local_14 + -0xe;
    }
    FUN_0045ba23('\x01',sVar4);
  }
  bVar2 = unidade_obter_tipo(indice_unidade);
  if (bVar2 == 4) {
    uVar9 = FUN_0044828b(extraout_ECX_65,extraout_EDX_48);
    unidade_obter_proprietario((ushort)((ulonglong)uVar9 >> 0x20));
    uVar10 = FUN_00448270(extraout_ECX_66,0);
    iVar8 = (int3)((ulonglong)uVar10 >> 0x28);
    if ((char)uVar9 != '\0') {
      local_20 = ((int)(extraout_CX - 1) /
                 (int)((uint)(CONCAT44((int)iVar8 >> 0x17,CONCAT31(iVar8,(char)uVar10)) / 5) &
                      0xffff)) * 0x80 + 0x2c7d;
      sVar4 = local_14 + 8;
      FUN_0045ba23('\x01',sVar4);
      FUN_0045ba23('\x01',sVar4);
      FUN_0045ba23('\x01',sVar4);
      FUN_0045ba23('\x01',sVar4);
    }
  }
  return;
}
