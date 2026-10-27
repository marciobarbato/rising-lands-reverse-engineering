/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00429278, entrada 00429278.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 __fastcall FUN_00429278(undefined4 param_1,undefined4 param_2)

{
  byte in_AL;
  char cVar1;
  byte bVar2;
  bool bVar3;
  undefined1 uVar4;
  SHORT SVar5;
  undefined2 uVar6;
  ushort uVar7;
  ushort uVar8;
  ushort uVar9;
  short sVar10;
  undefined2 uVar11;
  undefined4 uVar12;
  undefined2 extraout_var;
  ushort *puVar13;
  undefined4 uVar14;
  undefined4 uVar15;
  uint uVar16;
  undefined2 extraout_var_00;
  undefined *puVar17;
  uint uVar18;
  undefined2 extraout_var_01;
  short extraout_CX;
  short extraout_CX_00;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  uint extraout_ECX_04;
  uint extraout_ECX_05;
  uint extraout_ECX_06;
  undefined4 extraout_ECX_07;
  uint extraout_ECX_08;
  undefined4 extraout_ECX_09;
  uint extraout_ECX_10;
  undefined4 extraout_ECX_11;
  undefined4 extraout_ECX_12;
  undefined4 extraout_ECX_13;
  undefined4 extraout_ECX_14;
  undefined4 extraout_ECX_15;
  undefined4 extraout_ECX_16;
  undefined4 extraout_ECX_17;
  uint extraout_ECX_18;
  undefined4 extraout_ECX_19;
  uint extraout_ECX_20;
  uint extraout_ECX_21;
  undefined4 extraout_ECX_22;
  undefined4 extraout_ECX_23;
  uint extraout_ECX_24;
  undefined4 extraout_ECX_25;
  uint extraout_ECX_26;
  uint extraout_ECX_27;
  uint extraout_ECX_28;
  uint extraout_ECX_29;
  uint extraout_ECX_30;
  uint extraout_ECX_31;
  undefined4 extraout_ECX_32;
  undefined4 extraout_ECX_33;
  uint extraout_ECX_34;
  uint extraout_ECX_35;
  uint extraout_ECX_36;
  uint extraout_ECX_37;
  undefined2 extraout_var_02;
  undefined2 extraout_var_03;
  uint extraout_ECX_38;
  uint extraout_ECX_39;
  uint extraout_ECX_40;
  undefined2 extraout_var_04;
  uint extraout_ECX_41;
  uint extraout_ECX_42;
  undefined4 extraout_ECX_43;
  uint extraout_ECX_44;
  uint extraout_ECX_45;
  uint extraout_ECX_46;
  uint extraout_ECX_47;
  uint extraout_ECX_48;
  uint extraout_ECX_49;
  uint extraout_ECX_50;
  uint extraout_ECX_51;
  uint extraout_ECX_52;
  undefined4 extraout_ECX_53;
  uint extraout_ECX_54;
  uint extraout_ECX_55;
  uint extraout_ECX_56;
  uint extraout_ECX_57;
  uint extraout_ECX_58;
  uint extraout_ECX_59;
  uint extraout_ECX_60;
  undefined4 extraout_ECX_61;
  uint extraout_ECX_62;
  uint extraout_ECX_63;
  uint extraout_ECX_64;
  uint extraout_ECX_65;
  uint extraout_ECX_66;
  uint extraout_ECX_67;
  uint extraout_ECX_68;
  undefined4 extraout_ECX_69;
  undefined4 extraout_ECX_70;
  undefined4 extraout_ECX_71;
  undefined4 extraout_ECX_72;
  undefined4 extraout_ECX_73;
  uint extraout_ECX_74;
  undefined4 extraout_ECX_75;
  uint extraout_ECX_76;
  uint extraout_ECX_77;
  uint extraout_ECX_78;
  uint extraout_ECX_79;
  uint extraout_ECX_80;
  uint extraout_ECX_81;
  undefined4 extraout_ECX_82;
  undefined4 extraout_ECX_83;
  undefined4 extraout_ECX_84;
  uint extraout_ECX_85;
  undefined4 extraout_ECX_86;
  uint extraout_ECX_87;
  uint extraout_ECX_88;
  uint extraout_ECX_89;
  uint extraout_ECX_90;
  uint extraout_ECX_91;
  uint extraout_ECX_92;
  uint extraout_ECX_93;
  undefined4 extraout_ECX_94;
  undefined4 extraout_ECX_95;
  uint extraout_ECX_96;
  uint extraout_ECX_97;
  uint extraout_ECX_98;
  uint extraout_ECX_99;
  uint extraout_ECX_x00100;
  undefined4 extraout_ECX_x00101;
  undefined4 extraout_ECX_x00102;
  undefined4 extraout_ECX_x00103;
  uint extraout_ECX_x00104;
  undefined4 extraout_ECX_x00105;
  undefined4 extraout_ECX_x00106;
  undefined4 extraout_ECX_x00107;
  undefined4 extraout_ECX_x00108;
  undefined4 extraout_ECX_x00109;
  undefined4 extraout_ECX_x00110;
  undefined4 extraout_ECX_x00111;
  uint extraout_ECX_x00112;
  undefined4 extraout_ECX_x00113;
  undefined4 extraout_ECX_x00114;
  undefined4 extraout_ECX_x00115;
  uint extraout_ECX_x00116;
  uint extraout_ECX_x00117;
  undefined4 extraout_ECX_x00118;
  uint extraout_ECX_x00119;
  undefined4 extraout_ECX_x00120;
  undefined4 extraout_ECX_x00121;
  undefined4 extraout_ECX_x00122;
  uint extraout_ECX_x00123;
  uint extraout_ECX_x00124;
  uint extraout_ECX_x00125;
  uint extraout_ECX_x00126;
  uint extraout_ECX_x00127;
  uint extraout_ECX_x00128;
  uint extraout_ECX_x00129;
  uint extraout_ECX_x00130;
  uint extraout_ECX_x00131;
  uint extraout_ECX_x00132;
  uint extraout_ECX_x00133;
  uint extraout_ECX_x00134;
  uint extraout_ECX_x00135;
  uint extraout_ECX_x00136;
  uint extraout_ECX_x00137;
  uint extraout_ECX_x00138;
  uint extraout_ECX_x00139;
  uint extraout_ECX_x00140;
  uint extraout_ECX_x00141;
  uint extraout_ECX_x00142;
  uint extraout_ECX_x00143;
  uint extraout_ECX_x00144;
  uint extraout_ECX_x00145;
  uint extraout_ECX_x00146;
  uint extraout_ECX_x00147;
  uint extraout_ECX_x00148;
  undefined4 extraout_ECX_x00149;
  undefined4 extraout_ECX_x00150;
  uint extraout_ECX_x00151;
  uint extraout_ECX_x00152;
  undefined4 extraout_ECX_x00153;
  uint extraout_ECX_x00154;
  uint extraout_ECX_x00155;
  undefined4 extraout_ECX_x00156;
  uint extraout_ECX_x00157;
  uint extraout_ECX_x00158;
  uint extraout_ECX_x00159;
  uint extraout_ECX_x00160;
  uint extraout_ECX_x00161;
  uint extraout_ECX_x00162;
  uint extraout_ECX_x00163;
  uint extraout_ECX_x00164;
  uint extraout_ECX_x00165;
  uint extraout_ECX_x00166;
  uint extraout_ECX_x00167;
  undefined4 extraout_ECX_x00168;
  uint extraout_ECX_x00169;
  uint extraout_ECX_x00170;
  uint extraout_ECX_x00171;
  uint extraout_ECX_x00172;
  undefined4 extraout_ECX_x00173;
  undefined2 extraout_var_05;
  undefined4 extraout_ECX_x00174;
  undefined4 extraout_ECX_x00175;
  undefined4 extraout_ECX_x00176;
  uint extraout_ECX_x00177;
  uint extraout_ECX_x00178;
  uint extraout_ECX_x00179;
  uint extraout_ECX_x00180;
  undefined4 extraout_ECX_x00181;
  uint extraout_ECX_x00182;
  uint extraout_ECX_x00183;
  undefined4 extraout_ECX_x00184;
  uint extraout_ECX_x00185;
  undefined4 extraout_ECX_x00186;
  undefined2 *extraout_ECX_x00187;
  uint extraout_ECX_x00188;
  uint extraout_ECX_x00189;
  undefined4 extraout_ECX_x00190;
  undefined2 *extraout_ECX_x00191;
  uint extraout_ECX_x00192;
  uint extraout_ECX_x00193;
  undefined4 extraout_ECX_x00194;
  undefined4 extraout_ECX_x00195;
  uint extraout_ECX_x00196;
  byte extraout_DL;
  undefined2 extraout_DX;
  short sVar19;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 extraout_EDX_02;
  undefined4 extraout_EDX_03;
  undefined4 extraout_EDX_04;
  undefined4 extraout_EDX_05;
  undefined4 extraout_EDX_06;
  uint extraout_EDX_07;
  undefined4 extraout_EDX_08;
  uint extraout_EDX_09;
  undefined4 extraout_EDX_10;
  uint extraout_EDX_11;
  uint extraout_EDX_12;
  undefined4 extraout_EDX_13;
  undefined4 extraout_EDX_14;
  undefined4 extraout_EDX_15;
  undefined4 extraout_EDX_16;
  undefined4 extraout_EDX_17;
  undefined4 extraout_EDX_18;
  int extraout_EDX_19;
  undefined4 extraout_EDX_20;
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
  uint uVar20;
  undefined4 extraout_EDX_35;
  undefined4 extraout_EDX_36;
  undefined4 extraout_EDX_37;
  undefined4 extraout_EDX_38;
  undefined4 extraout_EDX_39;
  undefined2 extraout_var_06;
  undefined4 extraout_EDX_40;
  uint extraout_EDX_41;
  int iVar21;
  longlong lVar22;
  ulonglong uVar23;
  undefined8 uVar24;
  int local_4c;
  int local_44 [2];
  undefined4 local_3c;
  ushort local_38;
  undefined2 local_34 [2];
  undefined2 local_30 [2];
  undefined4 local_2c;
  char local_28;
  byte local_24;
  char local_20;
  byte local_1c;

  local_2c = 0xffff;
  local_20 = '\x01';
  DAT_0049a010 = 0x1dd8;
  DAT_004e0612 = 0;
  DAT_004e0614 = 0;
  local_4c = 0;
  _DAT_0049a014 = 0;
  DAT_004e0616 = 0;
  DAT_00508f8d._0_3_ = (uint3)(ushort)DAT_00508f8d;
  DAT_004e17ac = 0;
  DAT_004e0618 = 0;
  DAT_00496d4a = -1;
  DAT_00496ac2 = 0xffff;
  DAT_00496ac4 = 0xffff;
  local_1c = in_AL;
  SVar5 = GetAsyncKeyState(0x1b);
  uVar12 = extraout_ECX;
  uVar14 = extraout_EDX;
  if (SVar5 < 0) {
    cVar1 = FUN_004581b6();
    if (cVar1 == '\0') {
      FUN_0045ecd4(0,0xd,0,0);
      do {
        SVar5 = GetAsyncKeyState(0x1b);
      } while (SVar5 < 0);
      uVar12 = thunk_FUN_0048a4a8();
      goto LAB_0042c312;
    }
    FUN_00458088(extraout_ECX_00,extraout_EDX_00);
    uVar12 = extraout_ECX_01;
    uVar14 = extraout_EDX_01;
  }
  if ((DAT_005099ae == '\0') || (DAT_0049a010 = DAT_0049a010 + 8, DAT_004e19b0 == '\0')) {
    if (DAT_004e05a8 == '\0') {
      if ((DAT_005099b1 == '\0') || ((DAT_004e05a9 == '\0' && (DAT_004e05aa == '\0')))) {
        DAT_004e19b0 = '\0';
        lVar22 = FUN_00479cac(uVar12,CONCAT22((short)((uint)uVar14 >> 0x10),(ushort)(byte)uVar14));
        DAT_005099ac = (ushort)lVar22;
      }
      else {
        DAT_005099ac = 0x1a;
      }
    }
    else if (DAT_005099b1 == '\0') {
      DAT_004e05a8 = DAT_005099b1;
    }
    else {
      DAT_005099ac = 10;
    }
  }
  else {
    DAT_005099ac = 0;
  }
  if (DAT_0049a05a != '\0') {
    SVar5 = GetAsyncKeyState(0x11);
    if (SVar5 < 0) {
      uVar6 = 0xb;
LAB_0042952f:
      FUN_0045ecd4(0,uVar6,0,0);
    }
    else {
      SVar5 = GetAsyncKeyState(0x10);
      if (-1 < SVar5) {
        uVar6 = 0xc;
        goto LAB_0042952f;
      }
      FUN_0045ecd4(0,0xc,0,0);
      FUN_00442139(DAT_0049a05a,(ushort *)((int)&DAT_0050871e + 2));
      if ((uint)DAT_0050871e._2_2_ < DAT_00508724 / 2) {
        DAT_0050871e._2_2_ = 0;
      }
      else {
        DAT_0050871e._2_2_ = DAT_0050871e._2_2_ - (short)(DAT_00508724 / 2);
      }
      if ((uint)DAT_00508722 < DAT_00508726 / 2) {
        DAT_00508722 = 0;
      }
      else {
        DAT_00508722 = DAT_00508722 - (short)(DAT_00508726 / 2);
      }
      if ((uint)DAT_00497168 <= (uint)DAT_00508724 + (uint)DAT_0050871e._2_2_) {
        DAT_0050871e._2_2_ = DAT_00497168 - DAT_00508724;
      }
      if ((uint)DAT_0049716a <= (uint)DAT_00508722 + (uint)DAT_00508726) {
        DAT_00508722 = DAT_0049716a - DAT_00508726;
      }
    }
    DAT_0049a05a = '\0';
  }
  SVar5 = GetAsyncKeyState(0x10);
  if (SVar5 < 0) {
    DAT_004e05ae = 0xc;
  }
  else if (DAT_004e05ae == 0xc) {
    DAT_004e05ae = 0;
  }
  if ((DAT_005099b1 != '\0') && (DAT_004e062c != 0)) {
    DAT_004e062c = 0;
    DAT_004e05ae = 0;
  }
  if ((DAT_005099b1 != '\0') && (DAT_005099ac != 0xb)) {
    FUN_0047268b(0,(uint)local_1c);
    FUN_0041b663();
    DAT_004e05ab = 0;
    DAT_00496207 = -1;
    DAT_004e19b0 = '\0';
    DAT_00496d48 = 1;
    DAT_004e05ae = extraout_CX;
  }
  SVar5 = GetAsyncKeyState(0x11);
  if (SVar5 < 0) {
    if (DAT_004e05ae == 9) {
      uVar6 = FUN_0047253d();
      if (((char)uVar6 == '\0') ||
         (lVar22 = FUN_00472ab2(extraout_ECX_03,extraout_EDX_03), (char)lVar22 == '\0')) {
        DAT_004e05ae = 0;
      }
    }
    else {
      uVar6 = FUN_0047253d();
      if (((char)uVar6 != '\0') &&
         (lVar22 = FUN_00472ab2(extraout_ECX_02,extraout_EDX_02), (char)lVar22 != '\0')) {
        DAT_004e05ae = 8;
      }
    }
  }
  else if ((DAT_004e05ae == 8) || (DAT_004e05ae == 9)) {
    DAT_004e05ae = 0;
  }
  SVar5 = GetAsyncKeyState(0x2e);
  if (SVar5 < 0) {
    DAT_004e05ae = 7;
  }
  else if (DAT_004e05ae == 7) {
    DAT_004e05ae = 0;
  }
  SVar5 = GetAsyncKeyState(0x12);
  if (SVar5 < 0) {
    DAT_004e05ae = 2;
  }
  else if (DAT_004e05ae == 2) {
    DAT_004e05ae = 0;
  }
  SVar5 = GetAsyncKeyState(0x20);
  if (SVar5 < 0) {
    DAT_00508f8d._0_3_ = CONCAT12(1,(ushort)DAT_00508f8d);
  }
  SVar5 = GetAsyncKeyState(0x26);
  if ((SVar5 < 0) || (SVar5 = GetAsyncKeyState(0x28), SVar5 < 0)) {
    FUN_00472068(1,&DAT_00508722);
  }
  SVar5 = GetAsyncKeyState(0x27);
  if ((SVar5 < 0) || (SVar5 = GetAsyncKeyState(0x25), SVar5 < 0)) {
    FUN_00472068(1,&DAT_00508722);
  }
  SVar5 = GetAsyncKeyState(0xd);
  uVar20 = extraout_ECX_04;
  if (SVar5 == 0) {
    SVar5 = GetAsyncKeyState(0x58);
    uVar20 = extraout_ECX_05;
    uVar12 = extraout_EDX_04;
    if (SVar5 != 0) goto LAB_00429786;
  }
  else {
LAB_00429786:
    FUN_00440b63(uVar20,&DAT_00508722);
    uVar20 = extraout_ECX_06;
    uVar12 = extraout_EDX_05;
  }
  if (DAT_004e05ae == 0xd) {
    FUN_0041a4b6();
    FUN_0041a1ac(extraout_ECX_07,2);
    uVar20 = extraout_ECX_08;
    uVar12 = extraout_EDX_06;
  }
  if (DAT_005099ac < 10) {
    if (DAT_005099ac != 0) {
      if (DAT_005099ac < 9) {
        if (DAT_005099ae == '\0') {
          sVar10 = 0;
        }
        else {
          sVar10 = 8;
        }
        DAT_0049a010 = sVar10 + DAT_005099ac + 0x1dd7;
        _DAT_0049a014 = 0;
        if (DAT_005099ae == '\0') {
          uVar8 = 1;
        }
        else {
          uVar8 = 2;
        }
        FUN_00472068(uVar8,&DAT_00508722);
        uVar20 = extraout_ECX_x00158;
      }
      goto LAB_0042c2ae;
    }
    uVar18 = _DAT_005099a8 & 0xffff;
    uVar20 = (((int)(uint)DAT_005099aa >> 5) + (uint)DAT_00508722) * 0x100;
    uVar16 = ((int)uVar18 >> 5) + (uint)DAT_0050871e._2_2_ + uVar20;
    iVar21 = DAT_00508f8d >> 0x18;
    if ((int)uVar18 < (int)((uint)DAT_00508724 * 0x20 + iVar21 * -0x20)) {
      if ((int)((uint)DAT_00508726 * 0x20 + iVar21 * -0x20) <= (int)(uint)DAT_005099aa)
      goto switchD_0042a362_default;
      if ((int)uVar18 < iVar21 * 0x20) goto switchD_0042a362_default;
      if ((int)(uint)DAT_005099aa < iVar21 * 0x20) goto switchD_0042a362_default;
      uVar12 = FUN_004766d6(uVar20,(uint)DAT_00508041);
      if (((((char)uVar12 == '\0') && (DAT_004e05ae != 5)) && (DAT_00496208 != 0)) &&
         (DAT_004e05ae != 0xd)) {
        uVar6 = FUN_0047253d();
        uVar20 = extraout_ECX_10;
        if ((char)uVar6 != '\0') {
          if (DAT_004e05ae == 0) {
            _DAT_0049a014 = _DAT_00508f80 & 7;
            DAT_0049a010 = 0x1df5;
            if (DAT_005099ae != '\0') {
              if (DAT_005099af != '\0') {
                uVar6 = 5;
LAB_00429978:
                uVar7 = 0;
                uVar9 = 0;
                uVar8 = 0;
LAB_0042998c:
LAB_0042aecf:
                FUN_0045ecd4(uVar9,uVar6,uVar8,uVar7);
                uVar20 = extraout_ECX_x00100;
              }
            }
          }
          else {
LAB_004299a2:
            DAT_0049a010 = 0x1e0e;
            _DAT_0049a014 = 0;
          }
        }
        goto switchD_0042a362_default;
      }
      uVar8 = (ushort)uVar16;
      lVar22 = FUN_004766b1(extraout_ECX_09,extraout_EDX_07);
      uVar20 = (uint)((ulonglong)lVar22 >> 0x20);
      if ((char)lVar22 == '\0') {
        lVar22 = FUN_004762b9(extraout_ECX_11,uVar20);
        uVar12 = (undefined4)((ulonglong)lVar22 >> 0x20);
        if ((char)lVar22 == '\0') {
          uVar24 = FUN_00476263(extraout_ECX_14,uVar12);
          if ((char)uVar24 == '\0') {
            iVar21 = FUN_004762de(extraout_ECX_15,local_1c);
            if ((char)iVar21 != '\0') {
              uVar24 = FUN_00478a3b(extraout_ECX_17,extraout_EDX_08);
              local_4c = (int)uVar24;
              lVar22 = 0xffff;
              local_20 = '\0';
              goto LAB_00429a58;
            }
          }
          else {
            uVar24 = FUN_00478a3b(extraout_ECX_15,(int)((ulonglong)uVar24 >> 0x20));
            local_4c = (int)uVar24;
            FUN_0047544c(extraout_ECX_16,(int)((ulonglong)uVar24 >> 0x20));
            uVar6 = FUN_00475541();
            local_2c = CONCAT22(extraout_var,uVar6);
            local_20 = '\0';
          }
        }
        else {
          uVar24 = FUN_00478a3b(extraout_ECX_14,uVar12);
          local_4c = (int)uVar24;
        }
      }
      else {
        uVar24 = FUN_00476038(extraout_ECX_11,uVar20);
        uVar24 = FUN_00478a3b(extraout_ECX_12,(int)((ulonglong)uVar24 >> 0x20));
        local_4c = (int)uVar24;
        lVar22 = FUN_00475736(extraout_ECX_13,(uint)((ulonglong)uVar24 >> 0x20));
LAB_00429a58:
        local_2c = (undefined4)lVar22;
      }
      local_24 = 5;
      uVar12 = FUN_0047693a(uVar16,(uint)local_1c);
      uVar24 = CONCAT44(local_2c,local_4c);
      uVar20 = extraout_ECX_18;
      uVar18 = extraout_EDX_09;
      if ((char)uVar12 != '\0') {
        puVar13 = (ushort *)((uVar16 & 0xffff) * 2 + DAT_004e0f38);
        if ((*puVar13 & 0x8000) == 0) {
          iVar21 = 0xffff;
        }
        else {
          iVar21 = (int)(*puVar13 & 0x7fe0) >> 5;
        }
        DAT_00496ac4 = (ushort)iVar21;
        if (iVar21 != 0xffff) {
          local_24 = 3;
          FUN_0041a4f4(iVar21,(uint)CONCAT11(3,(char)iVar21));
          uVar24 = FUN_00418af7(extraout_ECX_19,0xffff);
          uVar20 = extraout_ECX_20;
        }
        local_2c = (undefined4)((ulonglong)uVar24 >> 0x20);
        local_4c = (int)uVar24;
        uVar24 = FUN_00446693(uVar20,0);
        DAT_00496ac2 = (ushort)uVar24;
        uVar18 = CONCAT22((short)((ulonglong)uVar24 >> 0x30),DAT_00496ac2);
        uVar20 = extraout_ECX_21;
        if (uVar18 != 0xffff) {
          local_24 = 1;
          unidade_obter_tipo(DAT_00496ac2);
          uVar24 = FUN_00441775(extraout_ECX_22,extraout_EDX_10);
          local_4c = (int)uVar24;
          local_2c = 0xffff;
          iVar21 = FUN_00472174(extraout_ECX_23,(uint)DAT_00496ac2);
          uVar20 = extraout_ECX_24;
          uVar18 = extraout_EDX_11;
          if (((char)iVar21 != '\0') && (DAT_005099b0 != '\0')) {
            lVar22 = thunk_FUN_0048a438(extraout_ECX_24,2);
            FUN_00440d5e(extraout_ECX_25,(uint)((ulonglong)lVar22 >> 0x20));
            uVar20 = extraout_ECX_26;
            uVar18 = extraout_EDX_12;
          }
        }
      }
      if (DAT_004e05ae == 9) {
        if (DAT_00496ac4 != 0xffff) {
          lVar22 = FUN_004191c9(uVar20,uVar18);
          uVar20 = extraout_ECX_27;
          if ((char)lVar22 != '\0') {
            uVar16 = FUN_004722a5(extraout_ECX_27,(uint)DAT_00496ac4);
            uVar20 = extraout_ECX_28;
            if ((char)uVar16 != '\0') {
              uVar24 = FUN_0041a08c(extraout_ECX_28,extraout_EDX_13);
              uVar20 = extraout_ECX_29;
              if ((byte)uVar24 == local_1c) goto LAB_00429bf2;
            }
          }
LAB_00429be7:
          DAT_0049a010 = 0x1e0e;
          _DAT_0049a014 = 0;
          goto switchD_0042a362_default;
        }
LAB_00429bf2:
        _DAT_0049a014 = _DAT_00508f84 % 3;
        DAT_0049a010 = 0x1e40;
        if ((DAT_005099ae == '\0') || (DAT_005099af == '\0')) goto switchD_0042a362_default;
        uVar9 = DAT_00496ac4;
        switch(DAT_004e05b0) {
        case 0:
          if (DAT_00496ac4 == 0xffff) {
            uVar6 = 6;
LAB_00429c76:
            uVar11 = 1;
            uVar9 = uVar8;
          }
          else {
            uVar11 = 2;
            uVar6 = 6;
          }
          break;
        case 1:
          if (DAT_00496ac4 == 0xffff) {
            uVar6 = 7;
            goto LAB_00429c76;
          }
          uVar11 = 2;
          uVar6 = 7;
          break;
        case 2:
          if (DAT_00496ac4 == 0xffff) {
            uVar6 = 8;
            goto LAB_00429c76;
          }
          uVar11 = 2;
          uVar6 = 8;
          break;
        case 3:
          if (DAT_00496ac4 == 0xffff) {
            uVar6 = 0x13;
            goto LAB_00429c76;
          }
          uVar11 = 2;
          uVar6 = 0x13;
          break;
        default:
          goto switchD_00429d99_default;
        }
        FUN_0045ecd4(uVar11,uVar6,uVar9,(ushort)DAT_004e05b4);
        uVar20 = extraout_ECX_30;
switchD_00429d99_default:
        DAT_004e05ae = 0;
      }
      else {
        if (DAT_004e05ae == 0xc) {
          if (DAT_00496ac2 != 0xffff) {
            uVar23 = FUN_00474169(uVar20,uVar18);
            uVar20 = extraout_ECX_31;
            if ((char)uVar23 != '\0') {
              _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f80 % 5);
              DAT_0049a010 = 0x1df0;
              if (DAT_005099af != '\0') {
                uVar7 = 0;
                uVar6 = 0x24;
                uVar9 = 0;
                uVar8 = 0;
                goto LAB_0042998c;
              }
            }
          }
          goto switchD_0042a362_default;
        }
        if (DAT_004e05ae == 0xb) {
          uVar24 = FUN_004721a8(uVar20,uVar18);
          DAT_004e0628 = (ushort)uVar24;
          uVar12 = extraout_ECX_32;
          if (DAT_004e0628 != 0xffff) {
            uVar20 = FUN_0047242e(extraout_ECX_32,8);
            uVar12 = extraout_ECX_33;
            if ((char)uVar20 != '\0') {
              DAT_0049a010 = 0x1e0e;
              _DAT_0049a014 = 0;
              uVar24 = FUN_0041a4f4(0,extraout_EDX_14);
              if ((((uint)uVar24 & 0xff) == 3) && (uVar20 = extraout_ECX_34, DAT_00496209 != 3)) {
LAB_00429ee8:
                DAT_0049a010 = 0x1ea9;
                _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f80 % 3);
                if (DAT_005099ae != '\0') {
                  if (DAT_005099af != '\0') {
                    uVar7 = 0;
                    uVar6 = 0x22;
                    uVar9 = DAT_00496ac4;
                    uVar8 = (ushort)DAT_00496209;
                    goto LAB_0042998c;
                  }
                }
              }
              else {
                uVar24 = FUN_0041a4f4(extraout_ECX_34,(int)((ulonglong)uVar24 >> 0x20));
                uVar20 = extraout_ECX_35;
                if (((uint)uVar24 & 0xff) == 7) {
                  if (DAT_00496209 == 3) goto LAB_00429ee8;
                }
              }
              goto switchD_0042a362_default;
            }
          }
          DAT_004e19b0 = '\0';
          uVar20 = CONCAT22((short)((uint)uVar12 >> 0x10),0x1ff);
LAB_00429e7e:
          DAT_004e05ae = 0;
          DAT_00496207 = -1;
          DAT_00496d48 = (undefined1)(uVar20 >> 8);
          goto switchD_0042a362_default;
        }
        if (DAT_004e05ae == 3) {
          uVar24 = FUN_004721a8(uVar20,uVar18);
          DAT_004e0628 = (ushort)uVar24;
          uVar20 = extraout_ECX_36;
          if (DAT_004e0628 != 0xffff) {
            bVar2 = unidade_obter_tipo(DAT_004e0628);
            uVar20 = extraout_ECX_37;
            if (bVar2 == 7) {
              uVar12 = extraout_EDX_15;
              if (DAT_00496207 == '\t') {
                uVar23 = FUN_00473999(extraout_ECX_37,extraout_EDX_15);
                uVar12 = (undefined4)(uVar23 >> 0x20);
                if ((char)uVar23 != '\0') {
                  DAT_004e19b0 = '\0';
                  uVar20 = CONCAT22(extraout_var_02,0x1ff);
                  goto LAB_00429e7e;
                }
              }
              FUN_004721a8(0,uVar12);
              uVar16 = FUN_0041fc40(CONCAT22(extraout_var_03,uVar8),CONCAT22(extraout_var_03,uVar8))
              ;
              uVar20 = extraout_ECX_38;
              if ((char)uVar16 != '\0') {
                if (DAT_005099ae != '\0') {
                  if (DAT_005099af != '\0') {
                    FUN_0045ecd4((short)extraout_ECX_38,4,0,0);
                    uVar20 = extraout_ECX_39;
                    if (DAT_00496207 != '\t') {
                      uVar20 = 0;
                      DAT_004e19b0 = '\0';
                      DAT_004e05ae = 0;
                      DAT_00496d48 = 1;
                      DAT_00496207 = -1;
                    }
                  }
                }
              }
              goto switchD_0042a362_default;
            }
          }
          DAT_004e19b0 = '\0';
          DAT_004e05ae = 0;
          DAT_00496d48 = 1;
          DAT_00496207 = -1;
          goto switchD_0042a362_default;
        }
        if (DAT_004e05ae == 0xd) {
          FUN_0041a4b6();
          _DAT_0049a014 = _DAT_00508f80 & 7;
          DAT_0049a010 = 0x1e99;
          if (((byte)DAT_00508f7c & 0x1f) == 0) {
            DAT_004e062c = DAT_004e062c + -1;
          }
          if (DAT_005099ae == '\0') {
            uVar20 = extraout_ECX_40;
            if (DAT_004e062c != 0) goto switchD_0042a362_default;
          }
          FUN_0045ecd4(0,0x27,0,0);
          uVar20 = CONCAT22(extraout_var_04,0x1ff);
          DAT_004e062c = 0;
          goto LAB_00429e7e;
        }
        if (DAT_004e05ae == 5) {
          uVar24 = FUN_004721a8(uVar20,uVar18);
          DAT_004e0628 = (ushort)uVar24;
          uVar20 = extraout_ECX_41;
          if (DAT_004e0628 != 0xffff) {
            bVar2 = unidade_obter_tipo(DAT_004e0628);
            uVar20 = extraout_ECX_42;
            if (bVar2 == 4) {
              uVar24 = FUN_0044828b(extraout_ECX_42,extraout_EDX_16);
              uVar24 = FUN_004746e4(extraout_ECX_43,
                                    CONCAT31((int3)((ulonglong)uVar24 >> 0x28),(char)uVar24));
              uVar20 = extraout_ECX_44;
              if ((byte)uVar24 <= (byte)((ulonglong)uVar24 >> 0x20)) {
                DAT_0049a010 = (ushort)DAT_00496208 * 8 + 0x1e71;
                _DAT_0049a014 = _DAT_00508f80 & 7;
                switch(DAT_00496208) {
                case 0:
                case 4:
                  if ((DAT_005099ae != '\0') && (DAT_005099af != '\0')) {
                    uVar7 = 0;
                    uVar9 = 5;
                    uVar6 = 0x16;
                    goto LAB_0042998c;
                  }
                  break;
                case 1:
                  if ((DAT_00496ac2 != 0xffff) &&
                     (bVar2 = unidade_obter_tipo(DAT_00496ac2), bVar2 != 4)) {
                    unidade_obter_tipo(DAT_00496ac2);
                    uVar16 = FUN_00442434();
                    if ((char)uVar16 == '\0') {
                      uVar20 = extraout_ECX_48;
                      if ((DAT_005099ae != '\0') && (DAT_005099af != '\0')) {
                        uVar7 = (ushort)uVar16 & 0xff;
                        goto LAB_0042a20b;
                      }
                      break;
                    }
                  }
                  uVar20 = 0x1e0e;
                  goto LAB_004299a2;
                case 2:
                  if (DAT_00496ac2 != 0xffff) {
                    bVar2 = unidade_obter_tipo(DAT_00496ac2);
                    uVar20 = extraout_ECX_45;
                    if (bVar2 != 4) {
                      unidade_obter_tipo(DAT_00496ac2);
                      cVar1 = FUN_0044230c();
                      uVar20 = extraout_ECX_46;
                      if (cVar1 != '\0') {
                        bVar2 = unidade_obter_tipo(DAT_00496ac2);
                        uVar20 = extraout_ECX_47;
                        if (bVar2 != 0x10) goto LAB_0042a1ef;
                      }
                    }
                  }
                  DAT_0049a010 = 0x1e0e;
                  _DAT_0049a014 = 0;
                  break;
                case 3:
                  if (DAT_00496ac2 == 0xffff) {
                    DAT_0049a010 = 0x1e0e;
                    _DAT_0049a014 = 0;
                  }
                  else {
LAB_0042a1ef:
                    if ((DAT_005099ae != '\0') && (DAT_005099af != '\0')) {
                      uVar7 = 0;
LAB_0042a20b:
                      uVar9 = 1;
                      uVar6 = 0x16;
                      uVar8 = DAT_00496ac2;
                      goto LAB_0042998c;
                    }
                  }
                }
                goto switchD_0042a362_default;
              }
            }
          }
          DAT_004e19b0 = '\0';
          DAT_00496207 = -1;
          DAT_004e05ae = 0;
          DAT_00496d48 = 1;
          goto switchD_0042a362_default;
        }
        if (DAT_004e05ae == 10) {
          uVar24 = FUN_004721a8(uVar20,uVar18);
          DAT_004e0628 = (ushort)uVar24;
          uVar20 = extraout_ECX_49;
          if (DAT_004e0628 != 0xffff) {
            bVar2 = unidade_obter_tipo(DAT_004e0628);
            uVar20 = extraout_ECX_50;
            if (bVar2 == 0xe) {
              uVar24 = FUN_004738e0(extraout_ECX_50,extraout_EDX_17);
              uVar20 = extraout_ECX_51;
              if ((char)uVar24 == '\0') {
                _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f84 % 3);
                DAT_0049a010 = 0x1e40;
                if (DAT_005099ae != '\0') {
                  if (DAT_005099af != '\0') {
                    uVar6 = 0x20;
                    goto LAB_00429978;
                  }
                }
                goto switchD_0042a362_default;
              }
            }
          }
          DAT_004e19b0 = '\0';
          DAT_004e05ae = 0;
          uVar20 = CONCAT22((short)(uVar20 >> 0x10),0xff00);
          DAT_00496207 = -1;
          DAT_00496d48 = 1;
          goto switchD_0042a362_default;
        }
        if (DAT_004e05ae == 1) {
          uVar20 = 0x1df5;
          _DAT_0049a014 = _DAT_00508f80 & 7;
          DAT_0049a010 = 0x1df5;
          if (DAT_005099ae != '\0') {
            if (DAT_005099af != '\0') {
              FUN_0045ecd4(0,5,0,0);
              DAT_004e05ae = 0;
              uVar20 = extraout_ECX_52;
            }
          }
          goto switchD_0042a362_default;
        }
        if (DAT_004e05ae == 2) {
          sVar10 = FUN_0041a4b6();
          uVar24 = FUN_004721a8(extraout_ECX_53,extraout_EDX_18);
          DAT_004e0628 = (ushort)uVar24;
          if (sVar10 == -1) {
            uVar20 = extraout_ECX_54;
            if (DAT_004e0628 != 0xffff) {
              cVar1 = FUN_00472355(extraout_ECX_54,(uint)local_24);
              uVar20 = extraout_ECX_57;
              if (cVar1 == '\0') {
                bVar2 = unidade_obter_tipo((ushort)extraout_ECX_54);
                uVar20 = extraout_ECX_58;
                if (bVar2 != 10) goto LAB_00429be7;
              }
              _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f80 % 6);
              DAT_0049a010 = 0x1dfd;
              if (DAT_005099ae != '\0') {
                if (DAT_005099af != '\0') {
                  FUN_0045ecd4((short)uVar20,0xe,0,0);
                  DAT_004e05ae = 0;
                  uVar20 = extraout_ECX_59;
                }
              }
            }
          }
          else {
            uVar12 = FUN_0042436c(extraout_ECX_54 & 0xffff,local_24);
            uVar20 = extraout_ECX_55;
            if ((char)uVar12 == '\0') {
              DAT_0049a010 = 0x1e0e;
              _DAT_0049a014 = 0;
            }
            else {
              DAT_0049a010 = 0x1dfd;
              _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f80 % 6);
              if (DAT_005099ae != '\0') {
                if (DAT_005099af != '\0') {
                  FUN_0045ecd4((short)extraout_ECX_55,0xe,0,0);
                  DAT_004e05ae = 0;
                  uVar20 = extraout_ECX_56;
                }
              }
            }
          }
          goto switchD_0042a362_default;
        }
        if (DAT_004e05ae == 7) {
          uVar24 = FUN_0041b54a(uVar20,uVar18);
          DAT_00496ac4 = (ushort)uVar24;
          DAT_0049a010 = 0x1e0e;
          _DAT_0049a014 = 0;
          uVar20 = extraout_ECX_60;
          if (((uint)uVar24 & 0xffff) != 0xffff) {
            uVar24 = FUN_0041a08c(extraout_ECX_60,(int)((ulonglong)uVar24 >> 0x20));
            if (((byte)uVar24 == local_1c) &&
               (uVar23 = FUN_004233d8(extraout_ECX_61,(int)((ulonglong)uVar24 >> 0x20)),
               (char)uVar23 != '\0')) {
              DAT_0049a010 = 0x1e1c;
              _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f80 % 6);
              uVar20 = extraout_ECX_62;
              if (DAT_005099ae != '\0') {
                if (DAT_005099af != '\0') {
                  FUN_0045ecd4(0,10,0,0);
                  FUN_0041b663();
                  uVar20 = extraout_ECX_63;
                }
              }
            }
            else {
LAB_0042b84e:
              DAT_0049a010 = 0x1e0e;
              uVar20 = 0;
              _DAT_0049a014 = 0;
            }
          }
          goto switchD_0042a362_default;
        }
        uVar6 = FUN_0047253d();
        uVar20 = extraout_ECX_64;
        if ((char)uVar6 == '\0') {
          sVar10 = FUN_0041a4b6();
          uVar20 = extraout_ECX_65;
          if (((sVar10 != -1) || (DAT_004e19b0 != '\0')) || (DAT_005099ae == '\0'))
          goto LAB_0042a744;
          _DAT_0049a024 = DAT_005099a8;
          DAT_0049a026._0_2_ = DAT_005099aa;
          uVar20 = CONCAT22((short)(extraout_ECX_65 >> 0x10),CONCAT11(1,(char)extraout_ECX_65));
          DAT_0049a026._2_2_ = (short)((_DAT_005099a8 & 0xffff) + 1);
          _DAT_0049a02a = DAT_005099aa + 1;
LAB_0042b230:
          DAT_004e19b0 = '\x01';
          DAT_004e19b2 = uVar8;
          DAT_004e19b4 = uVar8;
          goto switchD_0042a362_default;
        }
LAB_0042a744:
        if (DAT_004e19b0 != '\0') goto switchD_0042a362_default;
        uVar6 = FUN_0047253d();
        uVar20 = extraout_ECX_66;
        if ((char)uVar6 != '\0') {
          SVar5 = GetAsyncKeyState(0x45);
          uVar20 = extraout_ECX_67;
          if (SVar5 < 0) {
            FUN_0045ecd4(0,0x25,0,0);
            uVar20 = extraout_ECX_68;
          }
        }
        bVar2 = local_1c;
        if (DAT_00496ac2 != 0xffff) {
          if (DAT_004e05ae != 8) {
            bVar2 = unidade_obter_proprietario(DAT_00496ac2);
            if (bVar2 == local_1c) {
              DAT_0049a010 = 0x1df0;
              _DAT_0049a014 = _DAT_00508f80 % 5;
            }
            uVar6 = FUN_0047253d();
            if ((((char)uVar6 == '\0') || (cVar1 = FUN_00472355(extraout_ECX_69,1), cVar1 == '\0'))
               || ((bVar2 = unidade_obter_proprietario(DAT_00496ac2), bVar2 == extraout_DL ||
                   (bVar2 = unidade_obter_proprietario(DAT_00496ac2), bVar2 == 200)))) {
              uVar6 = FUN_0047253d();
              if ((((char)uVar6 == '\0') ||
                  (uVar20 = FUN_00472b6c(extraout_ECX_71,1), (char)uVar20 == '\0')) ||
                 (cVar1 = FUN_0044fffe(extraout_ECX_72), cVar1 != '\0')) {
                sVar10 = FUN_0041a4b6();
                uVar20 = extraout_ECX_77;
                uVar12 = extraout_EDX_20;
                if (sVar10 != -1) {
                  FUN_0041a4b6();
                  uVar14 = FUN_0042436c(extraout_ECX_78,1);
                  uVar20 = extraout_ECX_79;
                  uVar12 = extraout_EDX_21;
                  if ((char)uVar14 != '\0') {
                    bVar2 = unidade_obter_proprietario(DAT_00496ac2);
                    uVar20 = extraout_ECX_80;
                    uVar12 = extraout_EDX_22;
                    if (bVar2 != (byte)(extraout_ECX_80 >> 8)) {
                      bVar2 = unidade_obter_proprietario(DAT_00496ac2);
                      uVar20 = extraout_ECX_81;
                      uVar12 = extraout_EDX_23;
                      if (bVar2 != 200) goto LAB_0042a858;
                    }
                  }
                }
                if (((DAT_005099b0 != '\0') &&
                    (uVar24 = FUN_004721a8(uVar20,uVar12), (ushort)uVar24 == DAT_00496ac2)) &&
                   (cVar1 = FUN_0044fffe(extraout_ECX_82), cVar1 == '\0')) {
                  bVar2 = unidade_obter_tipo(DAT_00496ac2);
                  if (bVar2 == 7) {
                    uVar6 = 2;
                    uVar11 = 2;
                  }
                  else {
                    bVar2 = unidade_obter_tipo(DAT_00496ac2);
                    if (bVar2 == 5) {
LAB_0042aaca:
                      uVar6 = 2;
                      uVar11 = 1;
                    }
                    else {
                      bVar2 = unidade_obter_tipo(DAT_00496ac2);
                      if (bVar2 == 6) {
                        uVar6 = 2;
                      }
                      else {
                        bVar2 = unidade_obter_tipo(DAT_00496ac2);
                        if (bVar2 != 0xd) {
                          unidade_obter_tipo(DAT_00496ac2);
                          uVar20 = FUN_00442434();
                          if ((char)uVar20 == '\0') goto LAB_0042ab82;
                          uVar6 = 1;
                          uVar11 = 0;
                          goto LAB_0042ab74;
                        }
                        uVar24 = FUN_004474a6(extraout_ECX_83,2);
                        iVar21 = FUN_004471b8(extraout_ECX_84,(char)((ulonglong)uVar24 >> 0x20));
                        if ((short)iVar21 != 0) goto LAB_0042aaca;
                        uVar6 = 1;
                      }
                      uVar11 = 0;
                    }
                  }
LAB_0042ab74:
                  FUN_0045ecd4(uVar6,9,uVar11,0);
                }
LAB_0042ab82:
                bVar2 = unidade_obter_proprietario(DAT_00496ac2);
                uVar20 = extraout_ECX_85;
                if (bVar2 == local_1c) {
                  DAT_0049a010 = 0x1df0;
                  _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f80 % 5);
                  if (DAT_005099ae != '\0') {
                    _DAT_0049a024 = DAT_005099a8;
                    DAT_0049a026._0_2_ = DAT_005099aa;
                    DAT_0049a026._2_2_ = (short)((_DAT_005099a8 & 0xffff) + 1);
                    _DAT_0049a02a = DAT_005099aa + 1;
                    goto LAB_0042b230;
                  }
                }
              }
              else {
                uVar16 = FUN_0047242e(extraout_ECX_73,6);
                uVar20 = extraout_ECX_74;
                if ((char)uVar16 != '\0') {
                  unidade_obter_tipo(DAT_00496ac2);
                  FUN_00441108(extraout_ECX_75,0);
                  uVar8 = unidade_obter_vida(DAT_00496ac2);
                  uVar20 = extraout_ECX_76;
                  if ((int)(uint)uVar8 <= extraout_EDX_19) {
                    uVar20 = 0x1e6d;
                    _DAT_0049a014 = _DAT_00508f84 & 1;
                    DAT_0049a010 = 0x1e6d;
                    if (DAT_005099ae != '\0') {
                      if (DAT_005099af != '\0') {
                        uVar6 = 0x14;
                        goto LAB_0042a87d;
                      }
                    }
                    goto switchD_0042a362_default;
                  }
                }
                DAT_0049a010 = 0x1e16;
                _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f84 % 3);
                if (DAT_005099ae != '\0') {
                  if (DAT_005099af != '\0') {
                    uVar6 = 0x10;
                    goto LAB_0042a87d;
                  }
                }
              }
            }
            else {
              uVar20 = CONCAT31((int3)((uint)extraout_ECX_70 >> 8),DAT_005099ae);
LAB_0042a858:
              _DAT_0049a014 = _DAT_00508f80 % 6;
              DAT_0049a010 = 0x1dfd;
              if (DAT_005099ae != '\0') {
                if (DAT_005099af != '\0') {
                  uVar6 = 0xe;
LAB_0042a87d:
                  uVar7 = 0;
                  uVar8 = 0;
                  uVar9 = DAT_00496ac2;
                  goto LAB_0042aecf;
                }
              }
            }
          }
          goto switchD_0042a362_default;
        }
        if (DAT_00496ac4 == 0xffff) {
          uVar6 = FUN_0047253d();
          uVar20 = extraout_ECX_x00123;
          if ((char)uVar6 == '\0') goto switchD_0042a362_default;
          lVar22 = FUN_004762b9(extraout_ECX_x00123,uVar16 & 0xffff);
          uVar20 = extraout_ECX_x00124;
          if ((char)lVar22 == '\0') {
            uVar24 = FUN_00476038(extraout_ECX_x00124,(int)((ulonglong)lVar22 >> 0x20));
            uVar20 = extraout_ECX_x00125;
            if (((uint)uVar24 & 0xff) == 1) goto LAB_0042b36a;
            if (DAT_00496ac4 != 0xffff) {
              uVar24 = FUN_0041a4f4(extraout_ECX_x00125,(int)((ulonglong)uVar24 >> 0x20));
              uVar20 = extraout_ECX_x00126;
              if (((uint)uVar24 & 0xff) == 3) goto LAB_0042b36a;
            }
          }
          else {
LAB_0042b36a:
            uVar18 = FUN_0047248f(uVar20,1);
            uVar20 = extraout_ECX_x00127;
            if ((char)uVar18 != '\0') {
              if (DAT_004e05ae == 8) {
                _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f84 % 3);
                DAT_0049a010 = 0x1e3d;
                uVar20 = CONCAT31((int3)(extraout_ECX_x00127 >> 8),DAT_005099ae);
                if (DAT_005099ae != '\0') {
                  if (DAT_005099af != '\0') {
                    DAT_004e05ae = 9;
                    lVar22 = FUN_004762b9(uVar20,_DAT_0049a014);
                    uVar20 = extraout_ECX_x00128;
                    if ((char)lVar22 == '\0') {
                      if (DAT_00496ac4 != 0xffff) {
                        uVar24 = FUN_0041a4f4(extraout_ECX_x00128,(int)((ulonglong)lVar22 >> 0x20));
                        uVar20 = extraout_ECX_x00129;
                        if (((uint)uVar24 & 0xff) == 3) {
                          DAT_004e05b0 = 3;
                          goto LAB_0042b421;
                        }
                      }
                      DAT_004e05b0 = 2;
                    }
                    else {
                      DAT_004e05b0 = 1;
                    }
LAB_0042b421:
                    DAT_004e05b4 = 1;
                    DAT_004e05b2 = uVar8;
                    goto LAB_0042ad40;
                  }
                }
              }
              else {
                DAT_0049a010 = 0x1e10;
                _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f80 % 6);
                if (DAT_005099ae != '\0') {
                  if (DAT_005099af != '\0') {
                    lVar22 = FUN_004762b9(extraout_ECX_x00127,_DAT_0049a014);
                    if ((char)lVar22 == '\0') {
                      uVar6 = 0x12;
                      uVar9 = 0;
                      goto LAB_0042af96;
                    }
                    FUN_0045ecd4(0,7,0,0);
                    DAT_004e05ac = 0x1e03;
                    uVar20 = extraout_ECX_x00130;
                    DAT_00496204 = uVar8;
                  }
                }
              }
              goto switchD_0042a362_default;
            }
          }
          uVar24 = FUN_00476263(uVar20,uVar16 & 0xffff);
          uVar20 = extraout_ECX_x00131;
          if ((char)uVar24 == '\0') {
            uVar24 = FUN_00476038(extraout_ECX_x00131,(int)((ulonglong)uVar24 >> 0x20));
            uVar12 = (undefined4)((ulonglong)uVar24 >> 0x20);
            uVar20 = extraout_ECX_x00132;
            if (((uint)uVar24 & 0xff) == 2) goto LAB_0042b4fc;
            if (DAT_00496ac4 != 0xffff) {
              uVar24 = FUN_0041a4f4(extraout_ECX_x00132,uVar12);
              uVar12 = (undefined4)((ulonglong)uVar24 >> 0x20);
              uVar20 = extraout_ECX_x00133;
              if (((uint)uVar24 & 0xff) == 3) goto LAB_0042b4fc;
            }
          }
          else {
LAB_0042b4fc:
            uVar16 = FUN_0047248f(uVar20,2);
            uVar20 = extraout_ECX_x00134;
            uVar12 = extraout_EDX_30;
            if ((char)uVar16 != '\0') {
              if (DAT_004e05ae == 8) {
                _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f84 % 3);
                DAT_0049a010 = 0x1e3d;
                if (DAT_005099ae != '\0') {
                  if (DAT_005099af != '\0') {
                    DAT_004e05ae = 9;
                    uVar24 = FUN_00476263(extraout_ECX_x00134,_DAT_0049a014);
                    if ((char)uVar24 == '\0') {
                      uVar20 = extraout_ECX_x00135;
                      if (DAT_00496ac4 != 0xffff) {
                        uVar24 = FUN_0041a4f4(extraout_ECX_x00135,(int)((ulonglong)uVar24 >> 0x20));
                        uVar20 = extraout_ECX_x00136;
                        if (((uint)uVar24 & 0xff) == 3) {
                          DAT_004e05b0 = 3;
                          goto LAB_0042b5b0;
                        }
                      }
                      DAT_004e05b0 = 2;
                    }
                    else {
                      uVar20 = 0;
                      DAT_004e05b0 = 0;
                    }
LAB_0042b5b0:
                    DAT_004e05b4 = 2;
                    DAT_004e05b2 = uVar8;
                  }
                }
              }
              else {
                DAT_0049a010 = 0x1e10;
                _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f80 % 6);
                uVar20 = CONCAT22((short)(extraout_ECX_x00134 >> 0x10),
                                  CONCAT11(DAT_005099ae,(char)extraout_ECX_x00134));
                if (DAT_005099ae != '\0') {
                  if (DAT_005099af != '\0') {
                    lVar22 = FUN_004766b1(uVar20,_DAT_0049a014);
                    if ((char)lVar22 == '\0') {
                      uVar6 = 6;
                      goto LAB_0042ad8e;
                    }
                    FUN_0045ecd4(0,0x12,0,0);
                    DAT_004e05ac = 0x1e03;
                    uVar20 = extraout_ECX_x00137;
                    DAT_00496204 = uVar8;
                  }
                }
              }
              goto switchD_0042a362_default;
            }
          }
          uVar23 = FUN_00476038(uVar20,uVar12);
          uVar20 = extraout_ECX_x00138;
          if ((uVar23 & 0xff) == 0) {
LAB_0042b684:
            uVar16 = FUN_0047248f(uVar20,0);
            uVar20 = extraout_ECX_x00140;
            if ((char)uVar16 != '\0') {
              if (DAT_004e05ae == 8) {
                _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f84 % 3);
                DAT_0049a010 = 0x1e3d;
                if (DAT_005099ae != '\0') {
                  if (DAT_005099af != '\0') {
                    uVar20 = extraout_ECX_x00140 & 0xffffff00;
                    DAT_004e05ae = 9;
                    DAT_004e05b0 = 2;
                    DAT_004e05b4 = 0;
                    DAT_004e05b2 = uVar8;
                  }
                }
              }
              else {
                DAT_0049a010 = 0x1e10;
                _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f80 % 6);
                if ((DAT_005099ae != '\0') && (DAT_005099af != '\0')) {
                  lVar22 = FUN_004766b1(extraout_ECX_x00140,_DAT_0049a014);
                  uVar20 = extraout_ECX_x00141;
                  if ((char)lVar22 != '\0') {
                    uVar6 = 0x12;
                    goto LAB_0042ad8e;
                  }
                }
              }
              goto switchD_0042a362_default;
            }
          }
          else if (DAT_00496ac4 != 0xffff) {
            uVar24 = FUN_0041a4f4(extraout_ECX_x00138,(int)(uVar23 >> 0x20));
            uVar20 = extraout_ECX_x00139;
            if (((uint)uVar24 & 0xff) == 3) goto LAB_0042b684;
          }
          if (DAT_004e05ae == 8) goto LAB_0042b84e;
          uVar12 = FUN_0047693a(uVar20,(uint)local_1c);
          uVar20 = extraout_ECX_x00142;
          if ((char)uVar12 != '\0') {
            bVar3 = FUN_004761d4(extraout_ECX_x00142,1);
            uVar20 = extraout_ECX_x00143;
            if (bVar3) {
              uVar24 = FUN_0047295e(extraout_ECX_x00143,extraout_EDX_31);
              uVar20 = extraout_ECX_x00144;
              if ((char)uVar24 != '\0') goto LAB_00429be7;
            }
          }
          uVar12 = FUN_0047693a(uVar20,(uint)local_1c);
          uVar20 = extraout_ECX_x00145;
          if ((char)uVar12 == '\0') {
            lVar22 = FUN_004752b8(extraout_ECX_x00145,extraout_EDX_32);
            uVar20 = extraout_ECX_x00146;
            if ((char)lVar22 != '\0') {
              uVar24 = FUN_0047295e(extraout_ECX_x00146,(int)((ulonglong)lVar22 >> 0x20));
              uVar20 = extraout_ECX_x00147;
              if ((char)uVar24 != '\0') goto LAB_00429be7;
            }
          }
          _DAT_0049a014 = _DAT_00508f80 & 7;
          DAT_0049a010 = 0x1df5;
          if ((DAT_005099ae != '\0') && (DAT_005099af != '\0')) {
            FUN_0045ecd4(0,5,0,0);
            DAT_004e05ac = 0x1e03;
            uVar20 = extraout_ECX_x00148;
            DAT_00496204 = uVar8;
          }
          goto switchD_0042a362_default;
        }
        uVar6 = FUN_0047253d();
        if ((char)uVar6 == '\0') {
          uVar9 = FUN_0041a4b6();
          if ((uVar9 == DAT_00496ac4) && (DAT_005099b0 != '\0')) {
            uVar7 = 0;
            uVar6 = 0x21;
            uVar8 = 0;
            uVar9 = 0;
            goto LAB_0042aecf;
          }
          sVar10 = FUN_0041a4b6();
          uVar12 = extraout_ECX_x00118;
          uVar14 = extraout_EDX_28;
          if (sVar10 != -1) {
            FUN_0041a4b6();
            uVar15 = FUN_0042436c(extraout_ECX_x00119,3);
            uVar12 = extraout_ECX_x00120;
            uVar14 = extraout_EDX_29;
            if ((char)uVar15 != '\0') {
              uVar24 = FUN_0041a08c(extraout_ECX_x00120,
                                    CONCAT31((int3)((uint)extraout_EDX_29 >> 8),local_1c));
              uVar14 = (undefined4)((ulonglong)uVar24 >> 0x20);
              uVar12 = extraout_ECX_x00121;
              if ((char)uVar24 != (char)((ulonglong)uVar24 >> 0x20)) {
                uVar24 = FUN_0041a08c(extraout_ECX_x00121,uVar14);
                uVar14 = (undefined4)((ulonglong)uVar24 >> 0x20);
                uVar12 = extraout_ECX_x00122;
                if (((uint)uVar24 & 0xff) != 200) {
                  uVar20 = CONCAT31((int3)((uint)extraout_ECX_x00122 >> 8),DAT_005099ae);
                  goto LAB_0042aea3;
                }
              }
            }
          }
          goto LAB_0042b1ab;
        }
        if (DAT_004e05ae == 8) {
          uVar24 = FUN_0041a08c(extraout_ECX_86,extraout_EDX_24);
          uVar20 = extraout_ECX_87;
          if ((byte)uVar24 == local_1c) {
            uVar24 = FUN_0041a4f4(extraout_ECX_87,(int)((ulonglong)uVar24 >> 0x20));
            uVar20 = extraout_ECX_88;
            if (((uint)uVar24 & 0xff) != 3) goto LAB_0042ad4a;
            uVar16 = FUN_0047242e(extraout_ECX_88,5);
            uVar20 = extraout_ECX_89;
            if ((char)uVar16 == '\0') {
              uVar16 = FUN_0047242e(extraout_ECX_89,7);
              uVar20 = extraout_ECX_90;
              if ((char)uVar16 == '\0') {
                uVar16 = FUN_0047242e(extraout_ECX_90,6);
                uVar20 = extraout_ECX_91;
                if ((char)uVar16 == '\0') goto LAB_0042ad4a;
              }
            }
            _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f84 % 3);
            DAT_0049a010 = 0x1e3d;
            if (DAT_005099ae == '\0') goto switchD_0042a362_default;
            if (DAT_005099af == '\0') goto switchD_0042a362_default;
            DAT_004e05b0 = 3;
            DAT_004e05b2 = DAT_00496ac4;
            DAT_004e05ae = 9;
            uVar20 = FUN_0047242e(uVar20,7);
            if ((char)uVar20 != '\0') {
              DAT_004e05b4 = 2;
              uVar20 = extraout_ECX_92;
              goto switchD_0042a362_default;
            }
            uVar16 = FUN_0047242e(extraout_ECX_92,5);
            DAT_004e05b4 = 0;
            uVar20 = extraout_ECX_93;
            if ((char)uVar16 != '\0') {
              DAT_004e05b4 = 1;
              goto switchD_0042a362_default;
            }
LAB_0042ad40:
            goto switchD_0042a362_default;
          }
LAB_0042ad4a:
          _DAT_0049a014 = 0;
          DAT_0049a010 = 0x1e0e;
          if (DAT_005099ae == '\0') goto switchD_0042a362_default;
          if (DAT_005099af == '\0') goto switchD_0042a362_default;
          uVar6 = 5;
LAB_0042ad8e:
          FUN_0045ecd4(0,uVar6,0,0);
          uVar20 = 0x1e03;
          DAT_004e05ac = 0x1e03;
          DAT_00496204 = uVar8;
          goto switchD_0042a362_default;
        }
        uVar12 = FUN_0041a61c(extraout_ECX_86,bVar2);
        if ((char)uVar12 != '\0') {
          uVar24 = FUN_0041d02b(extraout_ECX_94,extraout_EDX_25);
          if ((char)uVar24 != '\0') goto LAB_0042aed9;
          uVar24 = FUN_0041a4f4(extraout_ECX_95,(int)((ulonglong)uVar24 >> 0x20));
          uVar20 = extraout_ECX_96;
          if (((uint)uVar24 & 0xff) != 0x10) {
            uVar24 = FUN_0041a4f4(extraout_ECX_96,(int)((ulonglong)uVar24 >> 0x20));
            uVar20 = extraout_ECX_97;
            if (((uint)uVar24 & 0xff) == 2) goto LAB_0042ae05;
LAB_0042ae5b:
            cVar1 = FUN_00472355(uVar20,3);
            uVar20 = extraout_ECX_99;
            if (cVar1 != '\0') {
LAB_0042aea3:
              _DAT_0049a014 = _DAT_00508f80 % 6;
              DAT_0049a010 = 0x1dfd;
              if (DAT_005099ae != '\0') {
                if (DAT_005099af != '\0') {
                  uVar6 = 0xe;
                  goto LAB_0042aec8;
                }
              }
            }
            goto switchD_0042a362_default;
          }
LAB_0042ae05:
          uVar16 = FUN_0047242e(uVar20,10);
          uVar20 = extraout_ECX_98;
          if ((char)uVar16 == '\0') goto LAB_0042ae5b;
          _DAT_0049a014 = _DAT_00508f80 & 1;
          DAT_0049a010 = 0x1e6f;
          if (DAT_005099ae == '\0') goto switchD_0042a362_default;
          if (DAT_005099af == '\0') goto switchD_0042a362_default;
          uVar6 = 0x10;
LAB_0042aec8:
          uVar7 = 0;
          uVar8 = 0;
          uVar9 = DAT_00496ac4;
          goto LAB_0042aecf;
        }
LAB_0042aed9:
        _DAT_0049a014 = _DAT_00508f80 % 5;
        DAT_0049a010 = 0x1df0;
        uVar24 = FUN_004721a8(0x1df0,_DAT_0049a014);
        bVar2 = unidade_obter_tipo((ushort)uVar24);
        uVar12 = extraout_ECX_x00101;
        if (bVar2 != 7) {
LAB_0042afb3:
          uVar24 = FUN_004721f9(uVar12,(uint)local_1c);
          uVar12 = extraout_ECX_x00105;
          if ((char)uVar24 != '\0') {
            uVar24 = FUN_0041a08c(extraout_ECX_x00105,(int)((ulonglong)uVar24 >> 0x20));
            uVar12 = extraout_ECX_x00106;
            if ((char)uVar24 == (char)((ulonglong)uVar24 >> 0x20)) {
              uVar24 = FUN_004729b4(extraout_ECX_x00106,(int)((ulonglong)uVar24 >> 0x20));
              uVar14 = (undefined4)((ulonglong)uVar24 >> 0x20);
              uVar12 = extraout_ECX_x00107;
              if ((char)uVar24 == '\0') {
LAB_0042affe:
                uVar24 = FUN_00472a0c(uVar12,uVar14);
                uVar12 = extraout_ECX_x00109;
                if ((char)uVar24 != '\0') {
                  uVar24 = FUN_0041a4f4(extraout_ECX_x00109,(int)((ulonglong)uVar24 >> 0x20));
                  uVar14 = (undefined4)((ulonglong)uVar24 >> 0x20);
                  uVar12 = extraout_ECX_x00110;
                  if (((uint)uVar24 & 0xff) == 0xe) goto LAB_0042b027;
                }
              }
              else {
                uVar24 = FUN_0041a4f4(extraout_ECX_x00107,uVar14);
                uVar14 = (undefined4)((ulonglong)uVar24 >> 0x20);
                uVar12 = extraout_ECX_x00108;
                if (((uint)uVar24 & 0xff) != 0x13) goto LAB_0042affe;
LAB_0042b027:
                uVar23 = FUN_00472a64(uVar12,uVar14);
                uVar12 = extraout_ECX_x00111;
                if ((char)uVar23 == '\0') {
                  uVar24 = FUN_0041c652(extraout_ECX_x00111,(int)(uVar23 >> 0x20));
                  uVar20 = extraout_ECX_x00112;
                  if ((char)uVar24 != '\0') {
                    _DAT_0049a014 = _DAT_00508f80 & 1;
                    DAT_0049a010 = 0x1e3b;
                    if (DAT_005099ae != '\0') {
                      if (DAT_005099af != '\0') {
                        uVar7 = 0;
                        uVar6 = 0x15;
                        uVar8 = 0;
                        uVar9 = 0;
                        goto LAB_0042aecf;
                      }
                    }
                  }
                  goto switchD_0042a362_default;
                }
              }
            }
          }
          uVar20 = FUN_00472b6c(uVar12,3);
          uVar12 = extraout_ECX_x00113;
          uVar14 = extraout_EDX_27;
          if ((char)uVar20 != '\0') {
            uVar23 = FUN_00472a64(extraout_ECX_x00113,extraout_EDX_27);
            uVar14 = (undefined4)(uVar23 >> 0x20);
            uVar12 = extraout_ECX_x00114;
            if ((char)uVar23 == '\0') {
              uVar24 = FUN_0041c652(extraout_ECX_x00114,uVar14);
              if ((char)uVar24 == '\0') {
                DAT_0049a010 = 0x1e0e;
                uVar20 = CONCAT22((short)((uint)extraout_ECX_x00115 >> 0x10),
                                  CONCAT11(DAT_005099ae,(char)extraout_ECX_x00115));
                _DAT_0049a014 = 0;
                if (DAT_005099ae != '\0') {
                  if (DAT_005099af != '\0') {
                    uVar6 = 5;
                    uVar9 = 0;
                    goto LAB_0042af96;
                  }
                }
              }
              else {
                DAT_0049a010 = 0x1e16;
                _DAT_0049a014 = _DAT_00508f80 % 6;
                uVar24 = FUN_0041a4f4(extraout_ECX_x00115,_DAT_0049a014);
                if (((uint)uVar24 & 0xff) == 0x15) {
                  _DAT_0049a014 = _DAT_00508f80 % 9;
                  DAT_0049a010 = 0x1eac;
                }
                uVar20 = extraout_ECX_x00116;
                if (DAT_005099ae != '\0') {
                  if (DAT_005099af != '\0') {
                    uVar6 = 0x10;
                    goto LAB_0042aec8;
                  }
                }
              }
              goto switchD_0042a362_default;
            }
          }
LAB_0042b1ab:
          uVar24 = FUN_0041a08c(uVar12,CONCAT22((short)((uint)uVar14 >> 0x10),
                                                CONCAT11(local_1c,(char)uVar14)));
          uVar20 = extraout_ECX_x00117;
          if ((char)uVar24 == (char)((ulonglong)uVar24 >> 0x28)) {
            _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f80 % 5);
            DAT_0049a010 = 0x1df0;
            if (DAT_005099ae != '\0') {
              _DAT_0049a024 = DAT_005099a8;
              DAT_0049a026._0_2_ = DAT_005099aa;
              DAT_0049a026._2_2_ = (short)((_DAT_005099a8 & 0xffff) + 1);
              _DAT_0049a02a = DAT_005099aa + 1;
              goto LAB_0042b230;
            }
          }
          goto switchD_0042a362_default;
        }
        uVar24 = FUN_0041c652(extraout_ECX_x00101,extraout_EDX_26);
        uVar12 = extraout_ECX_x00102;
        if ((char)uVar24 != '\0') {
          uVar24 = FUN_0041a976(extraout_ECX_x00102,(int)((ulonglong)uVar24 >> 0x20));
          uVar12 = extraout_ECX_x00103;
          if ((short)uVar24 == 0) goto LAB_0042afb3;
        }
        DAT_0049a010 = 0x1e10;
        _DAT_0049a014 = (uint)((ulonglong)_DAT_00508f80 % 6);
        uVar20 = CONCAT31((int3)((uint)uVar12 >> 8),DAT_005099ae);
        if (DAT_005099ae == '\0') goto switchD_0042a362_default;
        if (DAT_005099af == '\0') goto switchD_0042a362_default;
        uVar6 = 0x14;
        uVar9 = DAT_00496ac4;
LAB_0042af96:
        FUN_0045ecd4(uVar9,uVar6,0,0);
        uVar20 = extraout_ECX_x00104;
      }
      DAT_004e05ac = 0x1e03;
      DAT_00496204 = uVar8;
    }
switchD_0042a362_default:
    if ((DAT_004e19b0 != '\0') && (DAT_005099ae != '\0')) {
      if ((_DAT_005099a8 & 0xffff) < (uint)DAT_00508724 * 0x20) {
        DAT_0049a026._2_2_ = DAT_005099a8;
      }
      else {
        DAT_0049a026._2_2_ = DAT_00508724 * 0x20 + -1;
      }
      if ((uint)DAT_005099aa < (uint)DAT_00508726 * 0x20) {
        _DAT_0049a02a = DAT_005099aa;
      }
      else {
        _DAT_0049a02a = DAT_00508726 * 0x20 - 1;
      }
      DAT_004e19b4 = DAT_0050871e._2_2_ +
                     ((short)((int)(((int)(short)_DAT_0049a02a +
                                    ((int)(short)_DAT_0049a02a >> 0xf) * -0x20) -
                                   (uint)(((int)(short)_DAT_0049a02a >> 0xf) << 4 < 0)) >> 5) +
                     DAT_00508722) * 0x100 +
                     (short)((int)(((int)DAT_0049a026._2_2_ +
                                   ((int)DAT_0049a026._2_2_ >> 0xf) * -0x20) -
                                  (uint)(((int)DAT_0049a026._2_2_ >> 0xf) << 4 < 0)) >> 5);
      uVar20 = CONCAT31((int3)(uVar20 >> 8),DAT_005099af);
      if (DAT_005099af != '\0') {
        FUN_0047268b(uVar20,0);
        FUN_004742dc(extraout_ECX_x00149,DAT_004e19b2);
        uVar6 = FUN_0047253d();
        if ((char)uVar6 == '\0') {
          FUN_0043f92a(extraout_ECX_x00150,DAT_00496ac4);
          uVar20 = extraout_ECX_x00151;
          if (DAT_00496ac4 != 0xffff) {
            uVar24 = FUN_0041a08c(CONCAT22((short)(extraout_ECX_x00151 >> 0x10),
                                           CONCAT11(local_1c,(char)extraout_ECX_x00151)),
                                  extraout_EDX_33);
            uVar20 = extraout_ECX_x00152;
            if ((char)uVar24 == (char)(extraout_ECX_x00152 >> 8)) {
              FUN_0045ecd4(0,2,0,0);
              FUN_0041b673();
              _DAT_004e244c = (undefined2)extraout_ECX_x00153;
              _DAT_004e244e = _DAT_004e244c;
              uVar24 = FUN_0041a4f4(extraout_ECX_x00153,extraout_EDX_34);
              uVar20 = extraout_ECX_x00154;
              if (((uint)uVar24 & 0xff) == 0x10) {
                DAT_00496fd8 = 1;
                FUN_00471830();
                uVar20 = extraout_ECX_x00155;
              }
            }
          }
        }
        else {
          FUN_0041b663();
          FUN_0045ecd4(DAT_004e19b4,extraout_DX,0,0);
          FUN_0043f92a(extraout_ECX_x00156,DAT_00496ac2);
          _DAT_004e2454 = 0;
          uVar20 = extraout_ECX_x00157;
        }
        DAT_004e19b0 = '\0';
      }
      DAT_0049a010 = 0x1e0c;
      _DAT_0049a014 = 0;
      _DAT_005099a8 = CONCAT22(DAT_005099aa + -7,DAT_005099a8 + -7);
    }
  }
  else if (DAT_005099ac < 0xb) {
    uVar6 = FUN_0047253d();
    if ((char)uVar6 != '\0') {
      _DAT_0049a014 = _DAT_00508f80 & 7;
      DAT_0049a010 = 0x1df5;
    }
    if (DAT_005099b1 == '\0') {
      DAT_004e05a8 = DAT_005099b1;
      uVar20 = extraout_ECX_x00159;
    }
    else {
      DAT_0049a010 = 0x1e0b;
      if (DAT_004e05a8 == '\0') {
        DAT_004e05a8 = '\x01';
        FUN_0046a1d7(CONCAT22((short)(extraout_ECX_x00159 >> 0x10),0x100),DAT_005099aa);
        uVar20 = extraout_ECX_x00160;
      }
      else {
        FUN_0046a19e(1,DAT_005099aa);
        FUN_00471830();
        uVar20 = extraout_ECX_x00161;
      }
    }
    if (DAT_005099ae != '\0') {
      FUN_0046a1f8(uVar20,(undefined2 *)local_44);
      uVar6 = FUN_0047253d();
      uVar20 = (_DAT_005099a8 >> 0x10) - local_44[0];
      if ((char)uVar6 == '\0') {
        FUN_0046a273((short *)&DAT_00508722,(ushort)uVar20);
        uVar20 = extraout_ECX_x00163;
      }
      else {
        FUN_0046a224(0,uVar20 & 0xffff);
        uVar6 = 5;
        sVar10 = extraout_CX_00;
LAB_0042bbd6:
        FUN_0045ecd4(sVar10,uVar6,0,0);
        uVar20 = extraout_ECX_x00162;
      }
    }
  }
  else if (DAT_005099ac < 0x1a) {
    if (DAT_005099ac == 0xb) {
      uVar16 = FUN_0045da4e(uVar20,DAT_005099aa);
      iVar21 = 0;
      sVar10 = FUN_0041a4b6();
      if (sVar10 == -1) {
        uVar18 = FUN_004721ce();
        uVar20 = extraout_ECX_x00170;
        if ((uVar18 & 0xffff) == 1) {
          uVar24 = FUN_004721a8(extraout_ECX_x00170,extraout_EDX_38);
          uVar23 = FUN_004474f3((int)uVar24,(int)((ulonglong)uVar24 >> 0x20));
          uVar20 = extraout_ECX_x00171;
          goto LAB_0042bd42;
        }
      }
      else {
        uVar24 = FUN_0041a4f4(CONCAT22(extraout_var_00,sVar10),extraout_EDX_37);
        puVar17 = FUN_0041c734(extraout_ECX_x00168,(uint)((ulonglong)uVar24 >> 0x20));
        uVar23 = ZEXT48(puVar17);
        uVar20 = extraout_ECX_x00169;
LAB_0042bd42:
        iVar21 = (int)uVar23;
      }
      if (iVar21 != 0) {
        sVar10 = (short)uVar16;
        uVar18 = uVar16 & 0xffff;
        if (uVar18 == 8) {
          DAT_004e05a2 = 1;
          if ((DAT_005099ae != '\0') && (DAT_005099af != '\0')) {
            sVar19 = -1;
LAB_0042bd7c:
            DAT_004e05a2 = 1;
            FUN_0045da13(uVar20,sVar19);
            uVar20 = extraout_ECX_x00172;
          }
        }
        else if (uVar18 == 9) {
          DAT_004e05a2 = 1;
          if ((DAT_005099ae != '\0') && (DAT_005099af != '\0')) {
            sVar19 = 1;
            goto LAB_0042bd7c;
          }
        }
        else if (uVar18 < 4) {
          uVar4 = FUN_004472d3(uVar20,(uint)(ushort)(*(short *)(iVar21 + 4) + sVar10));
          uVar20 = extraout_ECX_x00196;
          switch(uVar4) {
          case 2:
            uVar6 = FUN_004472de(extraout_ECX_x00196,(uint)(ushort)(*(short *)(iVar21 + 4) + sVar10)
                                );
            uVar24 = FUN_00478a3b(extraout_ECX_x00173,
                                  CONCAT31((int3)((uint)extraout_EDX_39 >> 8),(char)uVar6));
            local_4c = (int)uVar24;
            local_2c = 0xffff;
            local_20 = '\0';
            DAT_004e0614 = 0;
            DAT_004e0616 = 0;
            DAT_004e0612 = 0;
            uVar20 = (uint)CONCAT21(extraout_var_05,DAT_005099ae) << 8;
            DAT_004e0618 = 0;
            if ((DAT_005099ae != '\0') && (DAT_005099af != '\0')) {
              uVar20 = 0xb;
              DAT_00496209 = (byte)((ulonglong)uVar24 >> 0x20);
LAB_0042be6c:
              DAT_004e05ae = (short)uVar20;
            }
            break;
          case 3:
            local_2c = 0xffff;
            uVar6 = FUN_004472de(local_34,(uint)(ushort)(*(short *)(iVar21 + 4) + sVar10));
            local_28 = (char)uVar6;
            uVar24 = FUN_00418af7(extraout_ECX_x00190,local_30);
            local_4c = (int)uVar24;
            FUN_0041aace(extraout_ECX_x00191,(undefined2 *)((ulonglong)uVar24 >> 0x20));
            DAT_004e0612 = local_30[0];
            DAT_004e0614 = local_38;
            DAT_004e0616 = local_34[0];
            local_20 = '\0';
            DAT_004e0618 = 0;
            uVar20 = extraout_ECX_x00192;
            if ((DAT_005099ae != '\0') && (DAT_005099af != '\0')) {
              iVar21 = FUN_004676e5(0,local_38,local_1c);
              uVar20 = extraout_ECX_x00193;
              if ((char)iVar21 != '\0') {
                if ((char)uVar6 == '\x14') {
                  uVar6 = 0xf;
                  goto LAB_0042bf88;
                }
                DAT_004e05ae = 3;
                DAT_00496207 = local_28;
              }
            }
            break;
          case 4:
            uVar6 = FUN_004472de(extraout_ECX_x00196,(uint)(ushort)(*(short *)(iVar21 + 4) + sVar10)
                                );
            uVar24 = FUN_004746ac(extraout_ECX_x00174,0xffff);
            local_2c = (undefined4)((ulonglong)uVar24 >> 0x20);
            local_4c = (int)uVar24;
            local_20 = '\0';
            DAT_004e0614 = 0;
            DAT_004e0612 = 0;
            DAT_004e0616 = 0;
            DAT_004e0618 = 0;
            uVar11 = FUN_0041a4b6();
            if (CONCAT22(extraout_var_06,uVar11) == 0xffff) {
              uVar24 = FUN_004746e4(extraout_ECX_x00175,0xffff);
              DAT_004e0618 = (ushort)(byte)uVar24;
              local_3c = CONCAT22((short)((ulonglong)uVar24 >> 0x10),DAT_004e0618);
              DAT_004e0612 = local_30[0];
              DAT_004e0614 = local_38;
              DAT_004e0616 = local_34[0];
              uVar20 = extraout_ECX_x00183;
              if ((DAT_005099ae != '\0') && (DAT_005099af != '\0')) {
                uVar24 = FUN_0044828b(extraout_ECX_x00183,(int)((ulonglong)uVar24 >> 0x20));
                uVar24 = FUN_004746e4(extraout_ECX_x00184,
                                      CONCAT31((int3)((ulonglong)uVar24 >> 0x28),(char)uVar24));
                uVar20 = extraout_ECX_x00185;
                if ((byte)uVar24 <= (byte)((ulonglong)uVar24 >> 0x20)) {
                  uVar20 = 5;
                  DAT_00496208 = (byte)uVar6;
                  goto LAB_0042be6c;
                }
              }
            }
            else {
              uVar24 = FUN_0041a4f4(extraout_ECX_x00175,CONCAT22(extraout_var_06,uVar11));
              if (((uint)uVar24 & 0xff) == 0x14) {
                uVar24 = FUN_004266bc(extraout_ECX_x00176,(int)((ulonglong)uVar24 >> 0x20));
                uVar20 = extraout_ECX_x00180;
                if ((((char)uVar24 != '\0') && (DAT_005099ae != '\0')) && (DAT_005099af != '\0')) {
                  DAT_004e062c = 8;
                  DAT_004e05ae = 0xd;
                  DAT_00496208 = (byte)uVar6;
                  FUN_0041aee2();
                  FUN_004265fd(extraout_ECX_x00181,extraout_EDX_40);
                  uVar20 = extraout_ECX_x00182;
                }
              }
              else {
                local_2c = 0xffff;
                local_20 = '\0';
                FUN_004746fe(local_34,local_30);
                DAT_004e0612 = local_30[0];
                DAT_004e0614 = local_38;
                DAT_004e0616 = local_34[0];
                DAT_004e0618 = 0;
                uVar20 = extraout_ECX_x00177;
                if ((DAT_005099ae != '\0') && (DAT_005099af != '\0')) {
                  iVar21 = FUN_004676e5(0,local_38,local_1c);
                  uVar20 = extraout_ECX_x00178;
                  if ((char)iVar21 != '\0') {
                    uVar6 = 0x23;
                    goto LAB_0042bf88;
                  }
                }
              }
            }
            break;
          case 6:
            local_2c = 0xffff;
            FUN_004472de(local_34,(uint)(ushort)(*(short *)(iVar21 + 4) + sVar10));
            uVar24 = FUN_00441775(extraout_ECX_x00186,extraout_EDX_41 & 0xffffff00);
            local_4c = (int)uVar24;
            local_20 = (char)((ulonglong)uVar24 >> 0x20);
            FUN_004410d2(extraout_ECX_x00187,local_30);
            DAT_004e0612 = local_30[0];
            DAT_004e0614 = local_38;
            DAT_004e0616 = local_34[0];
            DAT_004e0618 = 0;
            uVar20 = extraout_ECX_x00188;
            if ((DAT_005099ae != '\0') && (DAT_005099af != '\0')) {
              iVar21 = FUN_004676e5(0,local_38,local_1c);
              uVar20 = extraout_ECX_x00189;
              if ((char)iVar21 != '\0') {
                uVar6 = 0x11;
LAB_0042bf88:
                FUN_0045ecd4(0,uVar6,0,0);
                uVar20 = extraout_ECX_x00179;
              }
            }
            break;
          case 7:
            uVar6 = FUN_004472de(extraout_ECX_x00196,(uint)(ushort)(*(short *)(iVar21 + 4) + sVar10)
                                );
            uVar24 = FUN_00478a3b(extraout_ECX_x00194,CONCAT22(extraout_var_01,uVar6));
            local_4c = (int)uVar24;
            uVar20 = CONCAT22((short)((uint)extraout_ECX_x00195 >> 0x10),
                              (ushort)(byte)extraout_ECX_x00195);
            local_2c = 0xffff;
            local_20 = '\0';
            if ((DAT_005099ae != '\0') && (DAT_005099af != '\0')) {
              DAT_00496207 = (char)((ulonglong)uVar24 >> 0x20);
              DAT_004e05ae = 10;
            }
          }
        }
        if (((uVar16 & 0xffff) != 0xff) && (DAT_005099ae != '\0')) {
          DAT_004e05a2 = 1;
          DAT_00496d4a = sVar10;
        }
      }
    }
  }
  else if (DAT_005099ac < 0x1b) {
    uVar12 = CONCAT31((int3)((uint)uVar12 >> 8),DAT_005099b1);
    if (DAT_005099b1 == '\0') {
      DAT_004e05a9 = DAT_005099b1;
    }
    else {
      DAT_0049a010 = 0x1e0b;
      if (DAT_004e05a9 == '\0') {
        DAT_004e05a9 = '\x01';
        FUN_004620bb(CONCAT31((int3)(uVar20 >> 8),1),DAT_005099aa);
        uVar20 = extraout_ECX_x00164;
        uVar12 = extraout_EDX_35;
      }
      else {
        FUN_00462082(1,DAT_005099aa);
        FUN_00471830();
        uVar20 = extraout_ECX_x00165;
        uVar12 = extraout_EDX_36;
      }
    }
    FUN_00467557(uVar20,uVar12);
    uVar20 = extraout_ECX_x00166;
  }
  else if (DAT_005099ac < 0x1c) {
    if ((DAT_005099ae != '\0') && (DAT_005099af != '\0')) {
      FUN_00469baf();
      uVar20 = extraout_ECX_x00167;
    }
  }
  else if (((DAT_005099ac < 0x20) && (DAT_005099ae != '\0')) && (DAT_005099af != '\0')) {
    sVar10 = DAT_005099ac - 0x1c;
    uVar6 = 0x26;
    goto LAB_0042bbd6;
  }
LAB_0042c2ae:
  if (DAT_004e060c == local_4c) {
    if (DAT_004e0610 < DAT_0049620a) {
      DAT_004e0610 = DAT_004e0610 + 1;
    }
  }
  else if (local_20 == '\0') {
    DAT_004e0610 = DAT_0049620a;
  }
  else {
    DAT_004e0610 = 1;
  }
  DAT_004e060c = local_4c;
  DAT_0049620c = (undefined2)local_2c;
  uVar12 = 0;
  if (DAT_00496d2c != '\0') {
    uVar24 = FUN_0045ac31(uVar20,local_4c);
    uVar12 = (undefined4)uVar24;
  }
LAB_0042c312:
  return CONCAT44(param_2,uVar12);
}
