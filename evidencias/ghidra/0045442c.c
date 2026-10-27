/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0045442c, entrada 0045442c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_0045442c(uint param_1,undefined4 param_2)

{
  byte bVar1;
  byte bVar2;
  undefined3 uVar3;
  UnidadeParcial *pUVar4;
  ushort *puVar5;
  undefined1 uVar6;
  undefined1 uVar7;
  short sVar8;
  ushort uVar9;
  uint in_EAX;
  char cVar13;
  uint uVar10;
  undefined4 uVar11;
  UnidadeParcial *pUVar12;
  uint3 uVar14;
  ushort extraout_var_01;
  undefined2 extraout_var_02;
  ushort extraout_var_03;
  ushort extraout_var_04;
  ushort extraout_var_05;
  ushort extraout_var_06;
  undefined3 extraout_var;
  undefined3 extraout_var_00;
  ushort extraout_var_07;
  undefined4 extraout_ECX;
  uint extraout_ECX_00;
  int extraout_ECX_01;
  int extraout_ECX_02;
  int extraout_ECX_03;
  int extraout_ECX_04;
  int extraout_ECX_05;
  int extraout_ECX_06;
  int iVar15;
  int extraout_ECX_07;
  int extraout_ECX_08;
  int extraout_ECX_09;
  byte *extraout_ECX_10;
  byte *pbVar16;
  byte *extraout_ECX_11;
  int extraout_ECX_12;
  undefined4 extraout_ECX_13;
  byte *extraout_ECX_14;
  byte *extraout_ECX_15;
  byte *extraout_ECX_16;
  uint extraout_ECX_17;
  byte *extraout_ECX_18;
  undefined4 extraout_ECX_19;
  uint extraout_ECX_20;
  uint extraout_ECX_21;
  uint extraout_ECX_22;
  uint extraout_ECX_23;
  uint extraout_ECX_24;
  undefined4 extraout_ECX_25;
  uint extraout_ECX_26;
  int extraout_ECX_27;
  UnidadeParcial *extraout_ECX_28;
  undefined4 extraout_ECX_29;
  uint extraout_ECX_30;
  int extraout_ECX_31;
  UnidadeParcial *extraout_ECX_32;
  undefined4 extraout_ECX_33;
  uint extraout_ECX_34;
  int extraout_ECX_35;
  UnidadeParcial *extraout_ECX_36;
  uint extraout_ECX_37;
  uint extraout_ECX_38;
  int extraout_ECX_39;
  UnidadeParcial *extraout_ECX_40;
  undefined4 extraout_ECX_41;
  undefined4 extraout_ECX_42;
  uint extraout_ECX_43;
  undefined4 extraout_ECX_44;
  uint extraout_ECX_45;
  undefined4 extraout_ECX_46;
  uint extraout_ECX_47;
  uint extraout_ECX_48;
  undefined4 extraout_ECX_49;
  undefined4 extraout_ECX_50;
  uint extraout_ECX_51;
  uint extraout_ECX_52;
  uint extraout_ECX_53;
  uint extraout_ECX_54;
  undefined2 extraout_var_08;
  undefined4 extraout_ECX_55;
  undefined4 extraout_ECX_56;
  undefined2 extraout_var_09;
  undefined4 extraout_ECX_57;
  undefined4 extraout_ECX_58;
  undefined4 extraout_ECX_59;
  undefined4 extraout_ECX_60;
  undefined4 extraout_ECX_61;
  undefined4 extraout_ECX_62;
  undefined4 extraout_ECX_63;
  undefined4 extraout_ECX_64;
  undefined4 extraout_ECX_65;
  undefined4 extraout_ECX_66;
  undefined4 extraout_ECX_67;
  uint extraout_ECX_68;
  int extraout_ECX_69;
  UnidadeParcial *extraout_ECX_70;
  undefined4 extraout_ECX_71;
  uint extraout_ECX_72;
  int extraout_ECX_73;
  UnidadeParcial *extraout_ECX_74;
  undefined4 extraout_ECX_75;
  uint extraout_ECX_76;
  int extraout_ECX_77;
  int extraout_ECX_78;
  UnidadeParcial *extraout_ECX_79;
  undefined4 extraout_ECX_80;
  undefined4 extraout_ECX_81;
  undefined4 extraout_ECX_82;
  undefined4 extraout_ECX_83;
  undefined4 extraout_ECX_84;
  undefined4 extraout_ECX_85;
  undefined4 extraout_ECX_86;
  undefined4 extraout_ECX_87;
  undefined4 extraout_ECX_88;
  undefined4 extraout_ECX_89;
  uint extraout_ECX_90;
  undefined4 extraout_ECX_91;
  undefined4 extraout_ECX_92;
  undefined4 extraout_ECX_93;
  undefined4 extraout_ECX_94;
  undefined4 extraout_ECX_95;
  undefined4 extraout_ECX_96;
  uint extraout_ECX_97;
  uint extraout_ECX_98;
  uint extraout_ECX_99;
  uint extraout_ECX_x00100;
  int extraout_ECX_x00101;
  UnidadeParcial *extraout_ECX_x00102;
  undefined4 extraout_ECX_x00103;
  uint extraout_ECX_x00104;
  undefined4 extraout_ECX_x00105;
  undefined4 extraout_ECX_x00106;
  uint extraout_ECX_x00107;
  undefined4 extraout_ECX_x00108;
  undefined4 extraout_ECX_x00109;
  int extraout_ECX_x00110;
  undefined4 extraout_ECX_x00111;
  undefined4 extraout_ECX_x00112;
  uint extraout_ECX_x00113;
  int extraout_EDX;
  int iVar17;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  uint extraout_EDX_02;
  uint extraout_EDX_03;
  uint extraout_EDX_04;
  undefined4 extraout_EDX_05;
  undefined4 extraout_EDX_06;
  undefined4 extraout_EDX_07;
  undefined4 extraout_EDX_08;
  undefined4 extraout_EDX_09;
  undefined4 uVar18;
  undefined2 extraout_var_10;
  int extraout_EDX_10;
  int extraout_EDX_11;
  uint uVar19;
  int3 iVar20;
  int extraout_EDX_12;
  UnidadeParcial *pUVar21;
  bool bVar22;
  undefined8 uVar23;
  ulonglong uVar24;
  longlong lVar25;
  ulonglong uVar26;
  ushort auStack_7c [4];
  UnidadeParcial *pUStack_74;
  uint uStack_70;
  undefined4 uStack_6c;
  undefined2 auStack_64 [2];
  uint uStack_60;
  uint uStack_5c;
  undefined4 uStack_58;
  undefined4 uStack_50;
  undefined4 uStack_4c;
  undefined4 uStack_48;
  undefined4 uStack_44;
  undefined4 uStack_40;
  undefined4 uStack_3c;
  undefined4 uStack_38;
  uint uStack_34;
  byte local_30;
  char local_2c;
  byte bStack_28;
  byte local_24;
  byte bStack_20;
  byte local_1c;

  sVar8 = (short)in_EAX;
  pUVar21 = tabela_unidades + (in_EAX & 0xffff);
  if (pUVar21->estado != 0) {
    local_24 = pUVar21->proprietario_id;
    local_1c = pUVar21->tipo_id;
    if (*(int *)&pUVar21->field_0x104 == -1) {
      pUVar21->field_0xf9 = 0;
    }
    else {
      uVar23 = FUN_00440c5d(param_1,*(int *)&pUVar21->field_0x104);
      thunk_FUN_0048a14a(extraout_ECX,(int)uVar23);
      param_1 = extraout_ECX_00;
    }
  }
  pUVar12 = tabela_unidades;
  if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
     (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
    uVar11 = 0;
  }
  else {
    uVar11 = 1;
  }
  uVar23 = CONCAT44(tabela_unidades,uVar11);
  if ((char)uVar11 != '\0') {
    if (pUVar21->tipo_id == 0x10) {
      uVar10 = in_EAX & 0xffff;
      cVar13 = tabela_unidades[uVar10].field_0xa9 + '\x01';
      pUVar4 = tabela_unidades + uVar10;
      tabela_unidades[uVar10].field_0xa9 = cVar13;
      if (cVar13 == pUVar4->field_0xa7) {
        pUVar12[uVar10].field_0xa9 = 0;
        pUVar12[uVar10].field_0xa4 =
             (char)(((byte)pUVar12[uVar10].field_0xa4 + 1) % (uint)(byte)pUVar12[uVar10].field_0xa5)
        ;
      }
    }
    uVar9 = *(ushort *)(&DAT_004965de + (uint)tabela_unidades[in_EAX & 0xffff].tipo_id * 0x32);
    uVar10 = FUN_00428cc0((uint)(tabela_unidades + (in_EAX & 0xffff)),3);
    iVar17 = extraout_EDX;
    if ((int)(uint)*(ushort *)(extraout_ECX_01 + 0x102) < (int)((uint)uVar9 - (uVar10 & 0xffff))) {
      iVar17 = *(ushort *)(extraout_ECX_01 + 0x102) + 1;
      *(short *)(extraout_ECX_01 + 0x102) = (short)iVar17;
    }
    if ((local_1c < 0x10) || (0x11 < local_1c)) {
      bVar22 = false;
    }
    else {
      bVar22 = true;
    }
    iVar15 = extraout_ECX_01;
    if (!bVar22) {
      switch(local_1c) {
      case 0xb:
      case 0xc:
      case 0xd:
      case 0xe:
      case 0xf:
      case 0x10:
        bVar22 = true;
        break;
      default:
        bVar22 = false;
      }
      if ((((bVar22) && (*(int *)&pUVar21->field_0x104 != -1)) &&
          (pUVar21->celula_destino == pUVar21->celula_atual)) && (pUVar21->field_0xf9 != '\0')) {
        thunk_FUN_0048a438(extraout_ECX_01,
                           CONCAT22((short)((uint)iVar17 >> 0x10),CONCAT11(local_1c,(char)iVar17)));
        iVar15 = extraout_ECX_02;
      }
    }
    pUVar12 = tabela_unidades;
    if ((local_1c == 0x10) && (*(int *)&pUVar21->field_0x104 == -1)) {
      uVar10 = in_EAX & 0xffff;
      uVar11 = FUN_004766f0(uVar10,(uint)DAT_00508041);
      iVar15 = extraout_ECX_03;
      if ((char)uVar11 != '\0') {
        uVar23 = FUN_00440c5d(extraout_ECX_03,extraout_EDX_00);
        pUVar12[uVar10].field_0xf9 = 1;
        iVar15 = extraout_ECX_04;
        if (*(int *)&pUVar12[uVar10].field_0x104 == -1) {
          FUN_0048aa79(1,(uint)pUVar12[uVar10].tipo_id << 0x10 | 0x800,(uint)uVar23);
          iVar15 = extraout_ECX_05;
        }
      }
      pUVar21->field_0xf9 = 1;
    }
    if (((pUVar21->estado != 0xe) && (((in_EAX & 0xffff) + DAT_00508f7c & 0x1f) == 0)) &&
       (local_24 != 200)) {
      bVar1 = tabela_unidades[in_EAX & 0xffff].tipo_id;
      if (bVar1 < 0xf) {
        if (((2 < bVar1) && (3 < bVar1)) &&
           ((bVar1 < 8 || ((8 < bVar1 && ((bVar1 < 0xb || (0xc < bVar1)))))))) goto LAB_00454711;
LAB_004546f9:
        bVar22 = true;
      }
      else {
        if (bVar1 < 0x10) goto LAB_004546f9;
        if (bVar1 < 0x14) {
          if ((bVar1 < 0x11) || (0x11 < bVar1)) goto LAB_004546f9;
        }
        else if ((bVar1 < 0x17) || ((bVar1 < 0x19 || (bVar1 == 0x19)))) goto LAB_004546f9;
LAB_00454711:
        bVar22 = false;
      }
      if (bVar22) {
        uVar23 = FUN_0046d817(iVar15,(in_EAX & 0xffff) * 0x114);
        local_2c = (char)uVar23;
        iVar15 = extraout_ECX_06;
        if ((pUVar21->estado != 1) && (pUVar21->estado != 0x13)) {
          iVar15 = CONCAT31((int3)((uint)extraout_ECX_06 >> 8),local_1c);
          if ((local_1c < 0xe) || ((0xe < local_1c && (local_1c != 0x10)))) {
            bVar22 = false;
          }
          else {
            bVar22 = true;
          }
          pUVar12 = (UnidadeParcial *)((ulonglong)uVar23 >> 0x20);
          if ((!bVar22) ||
             (pUVar12 = tabela_unidades, tabela_unidades[in_EAX & 0xffff].field_0xda == '\0')) {
            if ((local_1c < 0xe) || ((0xe < local_1c && (local_1c != 0x10)))) {
              bVar22 = false;
            }
            else {
              bVar22 = true;
            }
            if (bVar22) goto LAB_004547e0;
          }
          uVar23 = FUN_00453f74(in_EAX & 0xffff,pUVar12);
          iVar15 = extraout_ECX_07;
          if ((short)uVar23 != -1) {
            if (local_2c == '\x02') {
              FUN_004829c8(extraout_ECX_07,0x49);
              iVar15 = extraout_ECX_08;
            }
            else if (pUVar21->estado == 7) {
              FUN_00445a36(extraout_ECX_07,'\x01');
              iVar15 = extraout_ECX_09;
            }
          }
        }
      }
    }
LAB_004547e0:
    uVar10 = FUN_00467d97(iVar15,2);
    pbVar16 = extraout_ECX_10;
    if ((char)uVar10 != '\0') {
      uVar23 = FUN_0047474f(extraout_ECX_10,extraout_EDX_01);
      pbVar16 = (byte *)(uint)(ushort)uVar23;
      if (DAT_00508f7c % (uint)pbVar16 == 0) {
        pbVar16 = (byte *)(pUVar21->vida - 1);
        pUVar21->vida = (ushort)pbVar16;
        if (((uint)pbVar16 & 0xffff) == 0) {
          pUVar12 = (UnidadeParcial *)FUN_00444938();
          goto switchD_0044d86e_default;
        }
      }
    }
    switch(pUVar21->tipo_id) {
    case 0:
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
    case 7:
    case 8:
    case 9:
    case 10:
    case 0x19:
      bVar22 = true;
      break;
    default:
      bVar22 = false;
    }
    if ((bVar22) &&
       (uVar10 = FUN_00467d97((in_EAX & 0xffff) * 0x114,2), pbVar16 = extraout_ECX_11,
       (char)uVar10 == '\0')) {
      FUN_00452cc8(extraout_ECX_11);
      pbVar16 = &tabela_unidades->proprietario_id + extraout_ECX_12;
      if ((pbVar16[2] == 0) || (pbVar16[2] == 4)) {
        pUVar12 = (UnidadeParcial *)0x0;
      }
      else {
        pUVar12 = (UnidadeParcial *)0x1;
      }
      if ((char)pUVar12 == '\0') goto switchD_0044d86e_default;
      if (*(short *)&pUVar21->field_0x4 != 4) {
        if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
           (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
          bVar22 = false;
        }
        else {
          bVar22 = true;
        }
        if ((((bVar22) &&
             (pbVar16 = (byte *)(in_EAX & 0xffff), tabela_unidades[(int)pbVar16].field_0x72 != '\0')
             ) && (*(short *)&tabela_unidades[(int)pbVar16].field_0x4 == 0)) &&
           ((*(int *)&pUVar21->field_0x83 >> 0x18 == 0 &&
            (*(int *)&pUVar21->field_0x84 >> 0x18 == 0)))) {
          uVar23 = FUN_0046d817(pbVar16,0);
          if (((uint)uVar23 & 0xff) == 2) {
            FUN_004829c8(extraout_ECX_13,0x4b);
            pbVar16 = extraout_ECX_14;
          }
          else {
            FUN_00453b84();
            pbVar16 = extraout_ECX_15;
          }
        }
      }
    }
    pUVar12 = tabela_unidades + (in_EAX & 0xffff);
    if ((pUVar12->tipo_id == 0x11) &&
       (local_30 = pUVar12->proprietario_id, *(short *)(&DAT_004e1a14 + (uint)local_30 * 8) == 0)) {
      if ((pUVar12->estado == 0) || (pUVar12->estado == 4)) {
        bVar22 = false;
      }
      else {
        bVar22 = true;
      }
      if ((bVar22) && (tabela_unidades[in_EAX & 0xffff].estado = 0x1e, sVar8 == DAT_00496304)) {
        DAT_004e0f36 = (byte)in_EAX ^ (byte)DAT_00496304;
        DAT_004e0f37 = (byte)(in_EAX >> 8) ^ (byte)((ushort)DAT_00496304 >> 8);
        DAT_00496304 = -1;
        DAT_004e0f3c = 0;
      }
      uVar10 = (uint)local_30;
      FUN_004457d3();
      if ((tabela_unidades[(int)extraout_ECX_16].celula_passo ==
           *(ushort *)(&DAT_004e1a1a + uVar10 * 8)) ||
         (pbVar16 = extraout_ECX_16,
         (int)(uint)tabela_unidades[(int)extraout_ECX_16].celula_passo >> 8 == 0)) {
        FUN_00457058();
        pbVar16 = (byte *)(extraout_ECX_17 & 0xffffff00);
        if ((tabela_unidades[extraout_EDX_02].estado == 0) ||
           (tabela_unidades[extraout_EDX_02].estado == 4)) {
          bVar22 = false;
        }
        else {
          bVar22 = true;
        }
        if ((bVar22) &&
           (tabela_unidades[extraout_EDX_02 & 0xffff].estado = 0,
           (short)extraout_EDX_02 == DAT_00496304)) {
          DAT_004e0f36 = 0;
          pbVar16 = (byte *)0x0;
          DAT_00496304 = -1;
          DAT_004e0f3c = 0;
          DAT_004e0f37 = DAT_004e0f36;
        }
        *(undefined2 *)(&DAT_004e1a18 + (uint)local_30 * 8) = 0xffff;
      }
    }
    if ((tabela_unidades[in_EAX & 0xffff].field_0x72 != '\0') && (pUVar21->estado != 4)) {
      FUN_00442cb4(pbVar16);
      pbVar16 = extraout_ECX_18;
    }
    uVar19 = in_EAX & 0xffff;
    uVar10 = FUN_00467d97(pbVar16,1);
    if ((char)uVar10 != '\0') {
      *(int *)&tabela_unidades[uVar19].field_0xe4 = *(int *)&tabela_unidades[uVar19].field_0xe4 + -1
      ;
      pUVar12 = (UnidadeParcial *)(uint)*(ushort *)&tabela_unidades[uVar19].field_0xe4;
      if (pUVar12 == (UnidadeParcial *)0x0) {
        pUVar12 = (UnidadeParcial *)FUN_00467d71(extraout_ECX_19,1);
      }
      goto switchD_0044d86e_default;
    }
    uVar10 = FUN_00467d97(extraout_ECX_19,3);
    param_1 = extraout_ECX_20;
    if (((char)uVar10 != '\0') &&
       (*(int *)&tabela_unidades[uVar19].field_0xec =
             *(int *)&tabela_unidades[uVar19].field_0xec + -1,
       *(short *)&tabela_unidades[uVar19].field_0xec == 0)) {
      FUN_00467d71(extraout_ECX_20,3);
      param_1 = extraout_ECX_21;
    }
    bVar1 = tabela_unidades[in_EAX & 0xffff].tipo_id;
    uVar14 = (uint3)((uint)tabela_unidades >> 8);
    if ((bVar1 < 0xc) || ((0xc < bVar1 && (bVar1 != 0xf)))) {
      iVar17 = (uint)uVar14 << 8;
    }
    else {
      iVar17 = CONCAT31(uVar14,1);
    }
    uVar23 = CONCAT44((in_EAX & 0xffff) * 0x114,iVar17);
    if ((char)iVar17 != '\0') {
      uVar23 = FUN_004484a7();
      param_1 = extraout_ECX_22;
    }
  }
  pUVar4 = tabela_unidades;
  uVar10 = (uint)((ulonglong)uVar23 >> 0x20);
  bVar1 = pUVar21->estado;
  pUVar12 = (UnidadeParcial *)CONCAT31((int3)((ulonglong)uVar23 >> 8),bVar1);
  if (0x18 < bVar1) goto switchD_0044d86e_default;
  pUVar12 = (UnidadeParcial *)(uint)bVar1;
  switch(pUVar12) {
  case (UnidadeParcial *)0x1:
  case (UnidadeParcial *)0x18:
    bVar1 = pUVar21->field_0xb7;
    if (bVar1 == 0) {
LAB_0045689e:
      uVar23 = FUN_00451914(param_1,uVar10);
      pUVar12 = (UnidadeParcial *)uVar23;
      break;
    }
    if (bVar1 < 2) {
      if (*(ushort *)&pUVar21->field_0xb8 != 0xffff) {
        if ((tabela_unidades[*(ushort *)&pUVar21->field_0xb8].estado == 0) ||
           (tabela_unidades[*(ushort *)&pUVar21->field_0xb8].estado == 4)) {
          bVar22 = false;
        }
        else {
          bVar22 = true;
        }
        if (bVar22) {
          uVar10 = (uint)tabela_unidades[*(ushort *)&pUVar21->field_0xb8].proprietario_id;
          if ((uVar10 != 200) &&
             (tabela_unidades[*(ushort *)&pUVar21->field_0xb8].field_0x72 != '\0'))
          goto LAB_0045689e;
        }
      }
      uVar23 = FUN_0046d817(in_EAX & 0xffff,tabela_unidades);
      uVar10 = (uint)uVar23;
      uVar11 = extraout_ECX_x00106;
    }
    else {
      if (bVar1 != 3) goto LAB_0045689e;
      if (*(short *)&pUVar21->field_0xb8 != -1) {
        uVar23 = FUN_0041a70b(param_1,uVar10);
        if ((char)uVar23 == '\0') {
          uVar23 = FUN_0041a08c(extraout_ECX_x00103,(int)((ulonglong)uVar23 >> 0x20));
          uVar10 = (uint)((ulonglong)uVar23 >> 0x20);
          param_1 = extraout_ECX_x00104;
          if (((uint)uVar23 & 0xff) != 200) goto LAB_0045689e;
        }
      }
      uVar23 = FUN_0046d817(in_EAX & 0xffff,tabela_unidades);
      uVar10 = (uint)uVar23;
      uVar11 = extraout_ECX_x00105;
    }
    if ((uVar10 & 0xff) == 2) {
      pUVar12 = (UnidadeParcial *)FUN_004829c8(uVar11,0x4a);
      break;
    }
LAB_004567b7:
    pUVar12 = (UnidadeParcial *)FUN_004457d3();
    *(undefined2 *)&pUVar21->field_0xb8 = 0xffff;
    break;
  case (UnidadeParcial *)0x2:
    if (pUVar21->celula_destino != pUVar21->celula_atual) goto LAB_004555a7;
    if (pUVar21->field_0x91 == pUVar21->field_0x90) {
      uVar23 = FUN_00448194(param_1,uVar10);
      if ((char)uVar23 == '\0') {
        uVar10 = in_EAX & 0xffff;
        uVar19 = (byte)tabela_unidades[uVar10].field_0xa4 + 1;
        pUVar12 = (UnidadeParcial *)(uVar19 / (byte)tabela_unidades[uVar10].field_0xa5);
        tabela_unidades[uVar10].field_0xa4 =
             (char)(uVar19 % (uint)(byte)tabela_unidades[uVar10].field_0xa5);
      }
      else {
        if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
           (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
          pUVar12 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar12 = (UnidadeParcial *)0x1;
        }
        if ((char)pUVar12 != '\0') {
          pUVar12 = (UnidadeParcial *)((in_EAX & 0xffff) * 0x45);
          tabela_unidades[in_EAX & 0xffff].estado = 7;
          if (sVar8 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
          }
        }
      }
      break;
    }
    goto LAB_00455a6f;
  case (UnidadeParcial *)0x3:
    if (pUVar21->field_0x90 == pUVar21->field_0x91) {
      if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
         (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
        pUVar12 = (UnidadeParcial *)0x0;
      }
      else {
        pUVar12 = (UnidadeParcial *)0x1;
      }
      if ((char)pUVar12 != '\0') {
        pUVar12 = (UnidadeParcial *)((in_EAX & 0xffff) * 0x45);
        tabela_unidades[in_EAX & 0xffff].estado = 7;
        if (sVar8 == DAT_00496304) {
          pUVar12 = (UnidadeParcial *)((uint)pUVar12 & 0xffffff00);
          DAT_004e0f36 = 0;
          DAT_004e0f3c = 0;
          DAT_004e0f37 = 0;
          DAT_00496304 = -1;
        }
      }
      break;
    }
LAB_00455a6f:
    uVar23 = FUN_00448599(param_1,uVar10);
    pUVar12 = (UnidadeParcial *)uVar23;
    break;
  case (UnidadeParcial *)0x4:
    switch(tabela_unidades[in_EAX & 0xffff].tipo_id) {
    case 0xb:
    case 0xc:
    case 0xd:
    case 0xe:
    case 0xf:
    case 0x10:
    case 0x11:
      bVar22 = true;
      break;
    default:
      bVar22 = false;
    }
    if (bVar22) {
      uVar10 = FUN_00467d97(param_1,2);
      uVar11 = extraout_ECX_x00111;
      if ((char)uVar10 == '\0') {
        iVar17 = (uint)tabela_unidades[in_EAX & 0xffff].tipo_id * 0x32;
        uStack_60 = (uint)*(ushort *)(&DAT_004965b4 + iVar17);
        uStack_5c = (uint)*(ushort *)(&DAT_004965b2 + iVar17);
        for (uVar9 = 0; uVar9 < (ushort)uStack_5c; uVar9 = uVar9 + 1) {
          FUN_0047605d(uVar11,0);
          uVar11 = extraout_ECX_x00112;
        }
      }
      pUStack_74 = tabela_unidades + (in_EAX & 0xffff);
      FUN_00472648(uVar11);
      pUVar12 = tabela_unidades + (in_EAX & 0xffff);
      while (pUVar12->campo_0a != 0) {
        FUN_00443dfc(in_EAX,0);
        in_EAX = extraout_ECX_x00113;
      }
      FUN_00457058();
      pUStack_74->vida = 0;
      pUVar12 = pUStack_74;
    }
    else {
      if (pUVar21->field_0xa4 == '\0') {
        FUN_00472648(param_1);
        FUN_00442eac();
        if (pUVar21->celula_atual != pUVar21->celula_passo) {
          FUN_00442eac();
        }
      }
      uVar10 = in_EAX & 0xffff;
      if ((uint)(byte)tabela_unidades[uVar10].field_0xa4 !=
          (byte)tabela_unidades[uVar10].field_0xdb - 1) {
        tabela_unidades[uVar10].field_0xa4 =
             (char)(((byte)tabela_unidades[uVar10].field_0xa4 + 1) %
                   (uint)(byte)tabela_unidades[uVar10].field_0xdb);
      }
      *(short *)&pUVar21->field_0xc2 = *(short *)&pUVar21->field_0xc2 + 1;
      pUVar12 = (UnidadeParcial *)(uint)*(ushort *)&pUVar21->field_0xc2;
      if (*(ushort *)&pUVar21->field_0xc2 < 0x14a) break;
      FUN_00472648(tabela_unidades + (in_EAX & 0xffff));
      puVar5 = &tabela_unidades->campo_0a;
      uVar11 = extraout_ECX_x00108;
      while (*(short *)((int)puVar5 + extraout_EDX_12) != 0) {
        FUN_00443dfc(uVar11,0);
        uVar11 = extraout_ECX_x00109;
      }
      pUVar12 = (UnidadeParcial *)FUN_00457058();
      *(undefined2 *)(extraout_ECX_x00110 + 0x9a) = 0;
    }
    pUVar21->estado = 0;
    break;
  case (UnidadeParcial *)0x5:
    if (pUVar21->field_0x82 != '\x02') {
LAB_0045672c:
      uVar23 = FUN_0044bc74(param_1,uVar10);
      pUVar12 = (UnidadeParcial *)uVar23;
      break;
    }
    uVar23 = FUN_0041a70b(param_1,uVar10);
    uVar19 = extraout_ECX_99;
    if ((char)uVar23 == '\0') {
      uVar23 = FUN_0041a08c(extraout_ECX_99,(int)((ulonglong)uVar23 >> 0x20));
      uVar10 = (uint)((ulonglong)uVar23 >> 0x20);
      param_1 = extraout_ECX_x00100;
      uVar19 = extraout_ECX_x00100;
      if ((byte)uVar23 == pUVar21->proprietario_id) goto LAB_0045672c;
    }
    if (tabela_unidades[in_EAX & 0xffff].field_0x72 == '\0') {
      if (pUVar21->tipo_id == 7) {
        FUN_004754de(uVar19,tabela_unidades);
      }
      pUVar12 = tabela_unidades;
      uVar10 = in_EAX & 0xffff;
      FUN_00442cb4(uVar10);
      pUVar12[uVar10].field_0x72 = 1;
      pUVar12 = tabela_unidades + uVar10;
      uStack_48 = CONCAT22(extraout_var_07,pUVar12->celula_atual);
      if ((pUVar12->proprietario_id != 200) && (pUVar12->proprietario_id != 4)) {
        uStack_34 = CONCAT31((int3)(((uint)extraout_var_07 << 0x10) >> 8),pUVar12->raio_visao) + 2;
        FUN_00476851(pUVar12,(uint)(ushort)((ushort)(byte)pUVar12->field_0xf5 + (short)uStack_34));
        FUN_00476cb3(extraout_ECX_x00101,
                     (uint)(ushort)((ushort)*(byte *)(extraout_ECX_x00101 + 0xbb) +
                                   (ushort)*(byte *)(extraout_ECX_x00101 + 0xf5)));
        pUVar12 = extraout_ECX_x00102;
      }
LAB_004550a2:
      FUN_0046a388(pUVar12,4);
    }
    goto LAB_004550b4;
  case (UnidadeParcial *)0x6:
    if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
       (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
      pUVar12 = (UnidadeParcial *)0x0;
    }
    else {
      pUVar12 = (UnidadeParcial *)0x1;
    }
    if ((char)pUVar12 != '\0') {
      pUVar12 = (UnidadeParcial *)((in_EAX & 0xffff) * 0x45);
      tabela_unidades[in_EAX & 0xffff].estado = 7;
      if (sVar8 == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = -1;
      }
    }
    break;
  case (UnidadeParcial *)0x7:
    uVar10 = in_EAX & 0xffff;
    bVar1 = tabela_unidades[uVar10].tipo_id;
    pUVar12 = (UnidadeParcial *)CONCAT31((int3)(uVar10 * 0x114 >> 8),bVar1);
    if ((7 < bVar1) && (8 < bVar1)) {
      if (bVar1 < 0x12) {
        if (10 < bVar1) {
          if (bVar1 == 0x11) {
            pUVar12 = (UnidadeParcial *)FUN_00447b2f();
          }
          break;
        }
      }
      else if ((((0x12 < bVar1) && (0x16 < bVar1)) && (0x18 < bVar1)) && (bVar1 != 0x19)) break;
    }
    uVar26 = FUN_004704dc(200,0);
    pUVar12 = (UnidadeParcial *)(uVar26 / extraout_ECX_x00107);
    uVar26 = uVar26 % (ulonglong)extraout_ECX_x00107;
    if ((int)uVar26 == 0) {
      iVar20 = (int3)(uVar26 >> 8);
      lVar25 = CONCAT44((int)iVar20 >> 0x17,CONCAT31(iVar20,pUVar4[uVar10].field_0x91));
      pUVar12 = (UnidadeParcial *)(lVar25 / 0x10);
      cVar13 = (char)(lVar25 % 0x10) + '\x01';
      pUVar4[uVar10].field_0x90 = cVar13;
      pUVar4[uVar10].field_0x91 = cVar13;
    }
    break;
  case (UnidadeParcial *)0xb:
    if (pUVar21->field_0x89 != '\0') {
      uVar23 = FUN_0041a70b(param_1,uVar10);
      uVar10 = (uint)((ulonglong)uVar23 >> 0x20);
      param_1 = extraout_ECX_97;
      if ((char)uVar23 != '\0') goto LAB_00454cbd;
    }
    uVar23 = FUN_0044ab60(param_1,uVar10);
    pUVar12 = (UnidadeParcial *)uVar23;
    break;
  case (UnidadeParcial *)0xd:
    if (*(short *)&pUVar21->field_0xc0 == -1) {
      pUVar12 = (UnidadeParcial *)(uint)*(ushort *)&pUVar21->field_0xb8;
      if (pUVar12 == (UnidadeParcial *)0xffff) break;
      if ((tabela_unidades[*(ushort *)&pUVar21->field_0xb8].estado == 0) ||
         (tabela_unidades[(int)pUVar12].estado == 4)) {
        bVar22 = false;
      }
      else {
        bVar22 = true;
      }
      if ((bVar22) &&
         ((tabela_unidades[*(ushort *)&pUVar21->field_0xb8].proprietario_id ==
           pUVar21->proprietario_id ||
          (tabela_unidades[*(ushort *)&pUVar21->field_0xb8].proprietario_id == 200)))) {
        pUVar12 = (UnidadeParcial *)FUN_0044a2ed();
        break;
      }
      goto LAB_004567b7;
    }
    uVar23 = FUN_0041a70b(param_1,uVar10);
    uVar11 = (undefined4)((ulonglong)uVar23 >> 0x20);
    if ((char)uVar23 == '\0') {
      if (pUVar21->tipo_id == 10) {
        uVar23 = FUN_0041a08c(extraout_ECX_61,uVar11);
        if (((uint)uVar23 & 0xff) == 200) goto LAB_00454d97;
        uVar23 = FUN_0041a08c(extraout_ECX_62,(int)((ulonglong)uVar23 >> 0x20));
        uVar18 = (undefined4)((ulonglong)uVar23 >> 0x20);
        uVar11 = extraout_ECX_63;
        if ((byte)uVar23 == pUVar21->proprietario_id) {
          uVar23 = FUN_0041a4f4(extraout_ECX_63,uVar18);
          uVar18 = (undefined4)((ulonglong)uVar23 >> 0x20);
          uVar11 = extraout_ECX_64;
          if (((uint)uVar23 & 0xff) == 0x10) goto LAB_00454d97;
        }
      }
      else {
        uVar23 = FUN_0041a08c(extraout_ECX_61,uVar11);
        uVar18 = (undefined4)((ulonglong)uVar23 >> 0x20);
        uVar11 = extraout_ECX_65;
        if ((byte)uVar23 != pUVar21->proprietario_id) {
          uVar23 = FUN_0041a08c(extraout_ECX_65,uVar18);
          uVar18 = (undefined4)((ulonglong)uVar23 >> 0x20);
          if ((((uint)uVar23 & 0xff) != 200) || (uVar11 = extraout_ECX_66, pUVar21->tipo_id != 9))
          goto LAB_00454d97;
        }
      }
      uVar23 = FUN_00449716(uVar11,uVar18);
      pUVar12 = (UnidadeParcial *)uVar23;
      break;
    }
    goto LAB_00454d97;
  case (UnidadeParcial *)0xf:
    if (tabela_unidades[in_EAX & 0xffff].tipo_id == 6) {
      if ((tabela_unidades[*(ushort *)&pUVar21->field_0xc0].estado == 0) ||
         (tabela_unidades[*(ushort *)&pUVar21->field_0xc0].estado == 4)) {
        bVar22 = false;
      }
      else {
        bVar22 = true;
      }
      if (!bVar22) goto LAB_00454d97;
    }
    iVar17 = (in_EAX & 0xffff) * 0x114;
    if (tabela_unidades[in_EAX & 0xffff].tipo_id == 7) {
      uVar23 = FUN_0041a70b(param_1,iVar17);
      iVar17 = (int)((ulonglong)uVar23 >> 0x20);
      param_1 = extraout_ECX_98;
      if ((char)uVar23 != '\0') goto LAB_00454d97;
    }
    uVar23 = FUN_0044b5f5(param_1,iVar17);
    pUVar12 = (UnidadeParcial *)uVar23;
    break;
  case (UnidadeParcial *)0x10:
  case (UnidadeParcial *)0x11:
    if (pUVar21->celula_atual == pUVar21->celula_destino) {
      pUVar12 = (UnidadeParcial *)(uint)pUVar21->estado;
      if (pUVar12 == (UnidadeParcial *)0x10) {
        uVar23 = FUN_00476038(param_1,uVar10);
        lVar25 = FUN_004766b1(extraout_ECX_80,
                              CONCAT31(CONCAT21((short)((ulonglong)uVar23 >> 0x30),(char)uVar23),
                                       (char)uVar23));
        if ((((char)lVar25 != '\0') &&
            (*(ushort *)&pUVar21->field_0x70 + 1 <= (uint)pUVar21->campo_0c)) &&
           (((pUVar21->tipo_id == 7 && ((char)((ulonglong)lVar25 >> 0x28) == '\x02')) ||
            (((cVar13 = (char)((ulonglong)lVar25 >> 0x20), pUVar21->tipo_id == 5 &&
              (cVar13 == '\x01')) || ((pUVar21->tipo_id == 6 && (cVar13 == '\0')))))))) {
          uVar23 = FUN_00476662(CONCAT22((short)((uint)extraout_ECX_81 >> 0x10),
                                         (ushort)(byte)extraout_ECX_81),0);
          pUVar21 = tabela_unidades;
          iVar17 = CONCAT22((short)((ulonglong)uVar23 >> 0x30),sVar8);
          pUVar12 = (UnidadeParcial *)&tabela_unidades[iVar17].campo_0a;
          *(short *)&tabela_unidades[iVar17].field_0x70 =
               *(short *)&tabela_unidades[iVar17].field_0x70 + 1;
          uVar9 = *(ushort *)pUVar12;
          *(undefined1 *)((int)pUVar12 + uVar9 + 0x42) = 2;
          *(short *)(&pUVar21[iVar17].field_0x10 + (uint)uVar9 * 2) =
               (short)CONCAT31((int3)((uint)extraout_ECX_82 >> 8),(char)uVar23);
          *(ushort *)pUVar12 = *(ushort *)pUVar12 + 1;
          break;
        }
        if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
           (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
          pUVar12 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar12 = (UnidadeParcial *)0x1;
        }
        if ((char)pUVar12 != '\0') {
          pUVar12 = (UnidadeParcial *)((in_EAX & 0xffff) * 0x45);
          tabela_unidades[in_EAX & 0xffff].estado = 7;
          if (sVar8 == DAT_00496304) {
            pUVar12 = (UnidadeParcial *)0x0;
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
          }
        }
      }
      else {
        if (pUVar12 != (UnidadeParcial *)0x11) break;
        FUN_004438d8(in_EAX & 0xffff,pUVar21->field_0x82);
        pUVar12 = (UnidadeParcial *)FUN_004457d3();
        pUVar21->field_0x82 = 0;
      }
      *(undefined2 *)&pUVar21->field_0xb2 = 0xffff;
      break;
    }
    goto LAB_004555a7;
  case (UnidadeParcial *)0x12:
    if (pUVar21->field_0x82 != '\x02') {
LAB_00455e23:
      uVar23 = FUN_0044f2d4(param_1,uVar10);
      pUVar12 = (UnidadeParcial *)uVar23;
      break;
    }
    uVar23 = FUN_0041a70b(param_1,uVar10);
    if ((char)uVar23 == '\0') {
      uVar23 = FUN_0041a08c(extraout_ECX_75,(int)((ulonglong)uVar23 >> 0x20));
      uVar10 = (uint)((ulonglong)uVar23 >> 0x20);
      param_1 = extraout_ECX_76;
      if ((byte)uVar23 == pUVar21->proprietario_id) goto LAB_00455e23;
    }
    pUVar12 = tabela_unidades;
    uVar10 = in_EAX & 0xffff;
    if (tabela_unidades[uVar10].field_0x72 == '\0') {
      FUN_00442cb4(uVar10 * 0x114);
      pUVar12[uVar10].field_0x72 = 1;
      pUVar12 = (UnidadeParcial *)(&tabela_unidades->proprietario_id + extraout_ECX_77);
      uVar9 = (ushort)((uint)tabela_unidades >> 0x10);
      uStack_44 = CONCAT22(uVar9,pUVar12->celula_atual);
      if ((pUVar12->proprietario_id != 200) && (pUVar12->proprietario_id != 4)) {
        uStack_34 = CONCAT31((int3)(((uint)uVar9 << 0x10) >> 8),pUVar12->raio_visao) + 2;
        uVar11 = FUN_00476851(pUVar12,(uint)(ushort)((ushort)(byte)pUVar12->field_0xf5 +
                                                    (short)uStack_34));
        uVar3 = (undefined3)((uint)uVar11 >> 8);
        uStack_34 = CONCAT31(uVar3,*(undefined1 *)(extraout_ECX_78 + 0xbb)) & 0xffff00ff;
        FUN_00476cb3(extraout_ECX_78,
                     (uint)(ushort)(((ushort)CONCAT31(uVar3,*(undefined1 *)(extraout_ECX_78 + 0xf5))
                                    & 0xff) + (short)uStack_34));
        pUVar12 = extraout_ECX_79;
      }
      goto LAB_004550a2;
    }
    goto LAB_004550b4;
  case (UnidadeParcial *)0x13:
    uVar9 = *(ushort *)&pUVar21->field_0xa0;
    uVar10 = CONCAT22((short)((ulonglong)uVar23 >> 0x30),uVar9);
    if (uVar9 < 0xf) {
      if (uVar9 < 5) {
        bVar22 = uVar9 == 1;
LAB_0045554e:
        uVar26 = CONCAT44(uVar10,uVar10);
        if (bVar22) {
          bVar1 = pUVar21->field_0xb7;
          uVar26 = (ulonglong)uVar10 << 0x20;
          if (bVar1 != 0) {
            if (bVar1 < 2) {
              if (*(ushort *)&pUVar21->field_0xb8 != 0xffff) {
                if ((tabela_unidades[*(ushort *)&pUVar21->field_0xb8].estado == 0) ||
                   (tabela_unidades[*(ushort *)&pUVar21->field_0xb8].estado == 4)) {
                  bVar22 = false;
                }
                else {
                  bVar22 = true;
                }
                if (((bVar22) &&
                    (pUVar12 = tabela_unidades + *(ushort *)&pUVar21->field_0xb8,
                    pUVar12->proprietario_id != 200)) &&
                   (uVar26 = ZEXT48(pUVar12) << 0x20, pUVar12->field_0x72 != '\0'))
                goto LAB_00455554;
              }
              uVar23 = FUN_0046d817(in_EAX & 0xffff,tabela_unidades);
              uVar11 = extraout_ECX_49;
              if (((uint)uVar23 & 0xff) == 2) goto LAB_004552aa;
LAB_004552bd:
              FUN_004457d3();
              *(undefined2 *)&pUVar21->field_0xb8 = 0xffff;
              param_1 = extraout_ECX_48;
              uVar26 = (ulonglong)extraout_EDX_04 << 0x20;
            }
            else {
              uVar26 = (ulonglong)uVar10 << 0x20;
              if (bVar1 == 3) {
                if (*(short *)&pUVar21->field_0xb8 != -1) {
                  uVar23 = FUN_0041a70b(param_1,uVar10);
                  if ((char)uVar23 == '\0') {
                    uVar24 = FUN_0041a08c(extraout_ECX_44,(int)((ulonglong)uVar23 >> 0x20));
                    param_1 = extraout_ECX_45;
                    uVar26 = uVar24 & 0xffffffff000000ff;
                    if (((uint)uVar24 & 0xff) != 200) goto LAB_00455554;
                  }
                }
                uVar23 = FUN_0046d817(in_EAX & 0xffff,tabela_unidades);
                uVar11 = extraout_ECX_46;
                if (((uint)uVar23 & 0xff) != 2) goto LAB_004552bd;
LAB_004552aa:
                FUN_004829c8(uVar11,0x4a);
                param_1 = extraout_ECX_47;
                uVar26 = (ulonglong)extraout_EDX_03 << 0x20;
              }
            }
          }
        }
      }
      else {
        if (5 < uVar9) {
          uVar26 = CONCAT44(uVar10,uVar10);
          if (uVar9 < 0xb) goto LAB_00455554;
          if (uVar9 < 0xc) goto LAB_00454c93;
          uVar26 = CONCAT44(uVar10,uVar10);
          if (uVar9 != 0xd) goto LAB_00455554;
          if (*(short *)&pUVar21->field_0xc0 != -1) {
            uVar23 = FUN_0041a70b(param_1,uVar10);
            uVar11 = (undefined4)((ulonglong)uVar23 >> 0x20);
            if ((char)uVar23 == '\0') {
              uVar18 = extraout_ECX_50;
              if (pUVar21->tipo_id == 10) goto LAB_0045520c;
              uVar26 = FUN_0041a08c(extraout_ECX_50,uVar11);
              param_1 = extraout_ECX_51;
              if ((byte)uVar26 == pUVar21->proprietario_id) goto LAB_00455554;
              uVar23 = FUN_0041a08c(extraout_ECX_51,(int)(uVar26 >> 0x20));
              if (((uint)uVar23 & 0xff) == 200) {
                uVar26 = CONCAT44((int)((ulonglong)uVar23 >> 0x20),(uint)pUVar21->tipo_id);
                bVar22 = pUVar21->tipo_id == 9;
                param_1 = extraout_ECX_52;
                goto LAB_00454d91;
              }
            }
            goto LAB_00454d97;
          }
          uVar19 = (uint)*(ushort *)&pUVar21->field_0xb8;
          uVar26 = CONCAT44(uVar10,uVar19);
          if (uVar19 == 0xffff) goto LAB_00455554;
          if ((tabela_unidades[*(ushort *)&pUVar21->field_0xb8].estado == 0) ||
             (tabela_unidades[uVar19].estado == 4)) {
            bVar22 = false;
          }
          else {
            bVar22 = true;
          }
          if (bVar22) {
            bVar1 = tabela_unidades[*(ushort *)&pUVar21->field_0xb8].proprietario_id;
            uVar26 = ZEXT48(tabela_unidades) << 0x20;
            if ((bVar1 == pUVar21->proprietario_id) ||
               (uVar26 = CONCAT44(tabela_unidades,(uint)bVar1), bVar1 == 200)) goto LAB_00455554;
          }
          goto LAB_004567b7;
        }
        uVar26 = CONCAT44(uVar10,(uint)(byte)pUVar21->field_0x82);
        if ((byte)pUVar21->field_0x82 == 2) {
          uVar23 = FUN_0041a70b(param_1,uVar10);
          uVar10 = extraout_ECX_37;
          if (((char)uVar23 != '\0') ||
             (uVar26 = FUN_0041a08c(extraout_ECX_37,(int)((ulonglong)uVar23 >> 0x20)),
             param_1 = extraout_ECX_38, uVar10 = extraout_ECX_38,
             (byte)uVar26 != pUVar21->proprietario_id)) {
            if (tabela_unidades[in_EAX & 0xffff].field_0x72 == '\0') {
              if (pUVar21->tipo_id == 7) {
                FUN_004754de(uVar10,tabela_unidades);
              }
              pUVar12 = tabela_unidades;
              uVar10 = in_EAX & 0xffff;
              FUN_00442cb4(uVar10);
              pUVar12[uVar10].field_0x72 = 1;
              pUVar12 = tabela_unidades + uVar10;
              uStack_4c = CONCAT22(extraout_var_04,pUVar12->celula_atual);
              if ((pUVar12->proprietario_id != 200) && (pUVar12->proprietario_id != 4)) {
                uStack_34 = CONCAT31((int3)(((uint)extraout_var_04 << 0x10) >> 8),
                                     pUVar12->raio_visao) + 2;
                FUN_00476851(pUVar12,(uint)(ushort)((ushort)(byte)pUVar12->field_0xf5 +
                                                   (short)uStack_34));
                FUN_00476cb3(extraout_ECX_39,
                             (uint)(ushort)((ushort)*(byte *)(extraout_ECX_39 + 0xbb) +
                                           (ushort)*(byte *)(extraout_ECX_39 + 0xf5)));
                pUVar12 = extraout_ECX_40;
              }
              goto LAB_004550a2;
            }
            goto LAB_004550b4;
          }
        }
      }
    }
    else if (uVar9 < 0x10) {
      if (tabela_unidades[in_EAX & 0xffff].tipo_id == 6) {
        if ((tabela_unidades[*(ushort *)&pUVar21->field_0xc0].estado == 0) ||
           (tabela_unidades[*(ushort *)&pUVar21->field_0xc0].estado == 4)) {
          bVar22 = false;
        }
        else {
          bVar22 = true;
        }
        if (!bVar22) goto LAB_00454d97;
      }
      iVar17 = (in_EAX & 0xffff) * 0x114;
      uVar26 = CONCAT44(iVar17,(uint)tabela_unidades[in_EAX & 0xffff].tipo_id);
      if (tabela_unidades[in_EAX & 0xffff].tipo_id == 7) {
        uVar26 = FUN_0041a70b(param_1,iVar17);
        bVar22 = (char)uVar26 == '\0';
        param_1 = extraout_ECX_24;
LAB_00454d91:
        if (!bVar22) goto LAB_00454d97;
      }
    }
    else if (uVar9 < 0x15) {
      uVar26 = CONCAT44(uVar10,uVar10);
      if (0x11 < uVar9) {
        if (uVar9 < 0x13) {
          uVar26 = CONCAT44(uVar10,(uint)(byte)pUVar21->field_0x82);
          if ((byte)pUVar21->field_0x82 == 2) {
            uVar23 = FUN_0041a70b(param_1,uVar10);
            if (((char)uVar23 != '\0') ||
               (uVar26 = FUN_0041a08c(extraout_ECX_33,(int)((ulonglong)uVar23 >> 0x20)),
               param_1 = extraout_ECX_34, (byte)uVar26 != pUVar21->proprietario_id)) {
              pUVar12 = tabela_unidades;
              uVar10 = in_EAX & 0xffff;
              if (tabela_unidades[uVar10].field_0x72 == '\0') {
                FUN_00442cb4(uVar10);
                pUVar12[uVar10].field_0x72 = 1;
                pUVar12 = tabela_unidades + uVar10;
                uStack_3c = CONCAT22(extraout_var_03,pUVar12->celula_atual);
                if ((pUVar12->proprietario_id != 200) && (pUVar12->proprietario_id != 4)) {
                  uStack_34 = CONCAT31((int3)(((uint)extraout_var_03 << 0x10) >> 8),
                                       pUVar12->raio_visao) + 2;
                  FUN_00476851(pUVar12,(uint)(ushort)((ushort)(byte)pUVar12->field_0xf5 +
                                                     (short)uStack_34));
                  FUN_00476cb3(extraout_ECX_35,
                               (uint)(ushort)((ushort)*(byte *)(extraout_ECX_35 + 0xbb) +
                                             (ushort)*(byte *)(extraout_ECX_35 + 0xf5)));
                  pUVar12 = extraout_ECX_36;
                }
                goto LAB_004550a2;
              }
              goto LAB_004550b4;
            }
          }
        }
        else {
          uVar26 = CONCAT44(uVar10,uVar10);
          if (uVar9 == 0x14) {
            uVar23 = FUN_0041a70b(param_1,uVar10);
            if ((char)uVar23 == '\0') {
              uVar23 = FUN_0041a08c(extraout_ECX_25,(int)((ulonglong)uVar23 >> 0x20));
              uVar11 = (undefined4)((ulonglong)uVar23 >> 0x20);
              if ((byte)uVar23 == pUVar21->proprietario_id) {
                param_1 = extraout_ECX_26;
                uVar26 = CONCAT44(uVar11,(uint)(byte)pUVar21->field_0x82);
                if ((byte)pUVar21->field_0x82 == 2) {
                  uVar23 = FUN_0041a70b(extraout_ECX_26,uVar11);
                  if (((char)uVar23 != '\0') ||
                     (uVar26 = FUN_0041a08c(extraout_ECX_29,(int)((ulonglong)uVar23 >> 0x20)),
                     param_1 = extraout_ECX_30, (byte)uVar26 != pUVar21->proprietario_id)) {
                    pUVar12 = tabela_unidades;
                    uVar10 = in_EAX & 0xffff;
                    if (tabela_unidades[uVar10].field_0x72 == '\0') {
                      FUN_00442cb4(uVar10);
                      pUVar12[uVar10].field_0x72 = 1;
                      pUVar12 = tabela_unidades + uVar10;
                      uStack_38 = CONCAT22(extraout_var_02,pUVar12->celula_atual);
                      if ((pUVar12->proprietario_id != 200) && (pUVar12->proprietario_id != 4)) {
                        FUN_00476851(pUVar12,(uint)(ushort)(pUVar12->raio_visao + 2 +
                                                           (ushort)(byte)pUVar12->field_0xf5));
                        FUN_00476cb3(extraout_ECX_31,
                                     (uint)(ushort)((ushort)*(byte *)(extraout_ECX_31 + 0xbb) +
                                                   (ushort)*(byte *)(extraout_ECX_31 + 0xf5)));
                        pUVar12 = extraout_ECX_32;
                      }
                      goto LAB_00454e9f;
                    }
                    goto LAB_00454ea6;
                  }
                }
                goto LAB_00455554;
              }
            }
            pUVar12 = tabela_unidades;
            uVar10 = in_EAX & 0xffff;
            if (tabela_unidades[uVar10].field_0x72 == '\0') {
              FUN_00442cb4(uVar10);
              pUVar12[uVar10].field_0x72 = 1;
              pUVar12 = tabela_unidades + uVar10;
              uStack_58 = CONCAT22(extraout_var_01,pUVar12->celula_atual);
              if ((pUVar12->proprietario_id != 200) && (pUVar12->proprietario_id != 4)) {
                uStack_34 = CONCAT31((int3)(((uint)extraout_var_01 << 0x10) >> 8),
                                     pUVar12->raio_visao) + 2;
                uVar11 = FUN_00476851(pUVar12,(uint)(ushort)((ushort)(byte)pUVar12->field_0xf5 +
                                                            (short)uStack_34));
                uVar3 = (undefined3)((uint)uVar11 >> 8);
                uStack_34 = CONCAT31(uVar3,*(undefined1 *)(extraout_ECX_27 + 0xbb)) & 0xffff00ff;
                FUN_00476cb3(extraout_ECX_27,
                             (uint)(ushort)(((ushort)CONCAT31(uVar3,*(undefined1 *)
                                                                     (extraout_ECX_27 + 0xf5)) &
                                            0xff) + (short)uStack_34));
                pUVar12 = extraout_ECX_28;
              }
              goto LAB_00454e9f;
            }
            goto LAB_00454ea6;
          }
        }
      }
    }
    else if (uVar9 < 0x16) {
LAB_00454c93:
      uVar26 = CONCAT44(uVar10,(uint)*(ushort *)&pUVar21->field_0xc0);
      if ((*(ushort *)&pUVar21->field_0xc0 != 0xffff) &&
         (uVar26 = FUN_0041a70b(param_1,uVar10), param_1 = extraout_ECX_23, (char)uVar26 != '\0'))
      goto LAB_00454cbd;
    }
    else {
      uVar26 = CONCAT44(uVar10,uVar10);
      if (0x16 < uVar9) {
        if (0x17 < uVar9) {
          bVar22 = uVar9 == 0x18;
          goto LAB_0045554e;
        }
        uVar23 = FUN_0041a70b(param_1,uVar10);
        uVar11 = (undefined4)((ulonglong)uVar23 >> 0x20);
        uVar18 = extraout_ECX_41;
        if ((char)uVar23 == '\0') {
LAB_0045520c:
          uVar23 = FUN_0041a08c(uVar18,uVar11);
          if ((((uint)uVar23 & 0xff) != 200) &&
             (uVar26 = FUN_0041a08c(extraout_ECX_42,(int)((ulonglong)uVar23 >> 0x20)),
             param_1 = extraout_ECX_43, (byte)uVar26 != pUVar21->proprietario_id))
          goto LAB_00455554;
        }
        goto LAB_00454d97;
      }
    }
LAB_00455554:
    uVar11 = (undefined4)(uVar26 >> 0x20);
    if ((((*(short *)&pUVar21->field_0xc2 != -1) ||
         (pUVar21->celula_atual == pUVar21->celula_destino)) &&
        (((*(short *)&pUVar21->field_0xc2 == -1 ||
          (iVar17 = FUN_0042381f(param_1,(uint)pUVar21->celula_atual), param_1 = extraout_ECX_53,
          uVar11 = extraout_EDX_05, (char)iVar17 != '\0')) &&
         (*(int *)&pUVar21->field_0x83 >> 0x18 == 0)))) &&
       (*(int *)&pUVar21->field_0x84 >> 0x18 == 0)) {
      if (CONCAT22((short)(*(int *)&pUVar21->field_0x84 >> 0x1f),*(undefined2 *)&pUVar21->field_0xc2
                  ) == 0xffff) {
        uVar23 = FUN_00476038(param_1,uVar11);
        uVar11 = (undefined4)((ulonglong)uVar23 >> 0x20);
        param_1 = extraout_ECX_54;
        if (((uint)uVar23 & 0xff) != 1) goto LAB_00455674;
        FUN_00476662(0,uVar11);
        *(undefined2 *)&pUVar21->field_0x4 = *(undefined2 *)&pUVar21->field_0x76;
        *(undefined2 *)&pUVar21->field_0x74 = 0;
        pUVar21 = tabela_unidades + CONCAT22(extraout_var_08,sVar8);
        uVar11 = FUN_004766f0(CONCAT22(extraout_var_08,sVar8),(uint)DAT_00508041);
        if ((char)uVar11 != '\0') {
          uVar23 = FUN_00440c5d(extraout_ECX_55,extraout_EDX_06);
          iVar17 = *(int *)&pUVar21->field_0x104;
          pUVar21->field_0xf9 = 0;
LAB_00455646:
          uVar19 = (uint)uVar23;
          if (iVar17 == -1) {
            uVar10 = (uint)pUVar21->tipo_id << 0x10;
LAB_00455660:
            FUN_0048aa79(0,uVar10,uVar19);
          }
        }
      }
      else {
LAB_00455674:
        if (*(short *)&pUVar21->field_0xc2 != -1) {
          uVar23 = FUN_0041a4f4(param_1,uVar11);
          if (((((uint)uVar23 & 0xff) == 3) &&
              (uVar23 = FUN_0041a08c(extraout_ECX_56,(int)((ulonglong)uVar23 >> 0x20)),
              (byte)uVar23 == pUVar21->proprietario_id)) &&
             (iVar17 = FUN_004676e5(0,0,pUVar21->proprietario_id), (char)iVar17 != '\0')) {
            FUN_004235bd(0,1);
            *(undefined2 *)&pUVar21->field_0x4 = *(undefined2 *)&pUVar21->field_0x76;
            *(undefined2 *)&pUVar21->field_0x74 = 0;
            pUVar21 = tabela_unidades + CONCAT22(extraout_var_09,sVar8);
            uVar11 = FUN_004766f0(CONCAT22(extraout_var_09,sVar8),(uint)DAT_00508041);
            if ((char)uVar11 != '\0') {
              uVar23 = FUN_00440c5d(extraout_ECX_57,extraout_EDX_07);
              iVar17 = *(int *)&pUVar21->field_0x104;
              pUVar21->field_0xf9 = 0;
              goto LAB_00455646;
            }
            goto LAB_00455665;
          }
        }
        uVar10 = in_EAX & 0xffff;
        uVar9 = FUN_00477b74(0x43,(uint)pUVar21->raio_visao);
        pUVar12 = tabela_unidades;
        if (uVar9 != 0xffff) {
          pUVar21->estado = 0x13;
          pUVar21 = tabela_unidades;
          tabela_unidades[uVar10].celula_destino = uVar9;
          if (sVar8 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
          }
          uVar19 = in_EAX & 0xffff;
          pUVar21[uVar10].estado_caminho = 0;
          pUVar21 = tabela_unidades;
          pUVar12 = (UnidadeParcial *)FUN_004766f0(uVar19,(uint)DAT_00508041);
          if ((char)pUVar12 != '\0') {
            uVar23 = FUN_00440c5d(extraout_ECX_58,extraout_EDX_08);
            pUVar12 = (UnidadeParcial *)uVar23;
            pUVar21[uVar19].field_0xf9 = 0;
            if (*(int *)&pUVar21[uVar19].field_0x104 == -1) {
              pUVar12 = (UnidadeParcial *)
                        FUN_0048aa79(0,(uint)pUVar21[uVar19].tipo_id << 0x10,(uint)pUVar12);
            }
          }
          break;
        }
        if (((pUVar21->proprietario_id == DAT_00508041) && (*(short *)&pUVar21->field_0x74 == 1)) &&
           (uVar11 = FUN_004766f0(0xffff,(uint)DAT_00508041), (char)uVar11 != '\0')) {
          uVar23 = FUN_00440c5d(extraout_ECX_59,extraout_EDX_09);
          uVar19 = (uint)uVar23;
          pUVar12[uVar10].field_0xf9 = 0;
          if (*(int *)&pUVar12[uVar10].field_0x104 == -1) {
            uVar10 = (uint)pUVar12[uVar10].tipo_id << 0x10 | 0xc00;
            goto LAB_00455660;
          }
        }
      }
LAB_00455665:
      pUVar12 = (UnidadeParcial *)FUN_0045315f();
      break;
    }
LAB_004555a7:
    pUVar12 = (UnidadeParcial *)FUN_0044930c();
    break;
  case (UnidadeParcial *)0x14:
    uVar23 = FUN_0041a70b(param_1,uVar10);
    if ((char)uVar23 == '\0') {
      uVar23 = FUN_0041a08c(extraout_ECX_67,(int)((ulonglong)uVar23 >> 0x20));
      if ((byte)uVar23 != pUVar21->proprietario_id) goto LAB_00455b50;
      uVar10 = extraout_ECX_68;
      if (pUVar21->field_0x82 != '\x02') {
LAB_00455d17:
        pUVar12 = (UnidadeParcial *)FUN_0044e35c(uVar10);
        break;
      }
      uVar23 = FUN_0041a70b(extraout_ECX_68,(int)((ulonglong)uVar23 >> 0x20));
      if (((char)uVar23 == '\0') &&
         (uVar23 = FUN_0041a08c(extraout_ECX_71,(int)((ulonglong)uVar23 >> 0x20)),
         uVar10 = extraout_ECX_72, (byte)uVar23 == pUVar21->proprietario_id)) goto LAB_00455d17;
      pUVar12 = tabela_unidades;
      uVar10 = in_EAX & 0xffff;
      if (tabela_unidades[uVar10].field_0x72 == '\0') {
        FUN_00442cb4(uVar10);
        pUVar12[uVar10].field_0x72 = 1;
        pUVar12 = tabela_unidades + uVar10;
        uStack_6c = CONCAT22(extraout_var_06,pUVar12->celula_atual);
        if ((pUVar12->proprietario_id != 200) && (pUVar12->proprietario_id != 4)) {
          uStack_34 = CONCAT31((int3)(((uint)extraout_var_06 << 0x10) >> 8),pUVar12->raio_visao) + 2
          ;
          uVar11 = FUN_00476851(pUVar12,(uint)(ushort)((ushort)(byte)pUVar12->field_0xf5 +
                                                      (short)uStack_34));
          uVar3 = (undefined3)((uint)uVar11 >> 8);
          uStack_34 = CONCAT31(uVar3,*(undefined1 *)(extraout_ECX_73 + 0xbb)) & 0xffff00ff;
          FUN_00476cb3(extraout_ECX_73,
                       (uint)(ushort)(((ushort)CONCAT31(uVar3,*(undefined1 *)
                                                               (extraout_ECX_73 + 0xf5)) & 0xff) +
                                     (short)uStack_34));
          pUVar12 = extraout_ECX_74;
        }
        goto LAB_00454e9f;
      }
    }
    else {
LAB_00455b50:
      pUVar12 = tabela_unidades;
      uVar10 = in_EAX & 0xffff;
      if (tabela_unidades[uVar10].field_0x72 == '\0') {
        FUN_00442cb4(uVar10);
        pUVar12[uVar10].field_0x72 = 1;
        pUVar12 = tabela_unidades + uVar10;
        uStack_40 = CONCAT22(extraout_var_05,pUVar12->celula_atual);
        if ((pUVar12->proprietario_id != 200) && (pUVar12->proprietario_id != 4)) {
          uStack_34 = CONCAT31((int3)(((uint)extraout_var_05 << 0x10) >> 8),pUVar12->raio_visao) + 2
          ;
          uVar11 = FUN_00476851(pUVar12,(uint)(ushort)((ushort)(byte)pUVar12->field_0xf5 +
                                                      (short)uStack_34));
          uVar3 = (undefined3)((uint)uVar11 >> 8);
          uStack_34 = CONCAT31(uVar3,*(undefined1 *)(extraout_ECX_69 + 0xbb)) & 0xffff00ff;
          FUN_00476cb3(extraout_ECX_69,
                       (uint)(ushort)(((ushort)CONCAT31(uVar3,*(undefined1 *)
                                                               (extraout_ECX_69 + 0xf5)) & 0xff) +
                                     (short)uStack_34));
          pUVar12 = extraout_ECX_70;
        }
LAB_00454e9f:
        FUN_0046a388(pUVar12,4);
      }
    }
LAB_00454ea6:
    *(undefined2 *)&pUVar21->field_0xc0 = 0xffff;
LAB_004550b4:
    pUVar12 = (UnidadeParcial *)FUN_004457d3();
    pUVar21->field_0x82 = 0;
    *(undefined2 *)&pUVar21->field_0x80 = 0xffff;
    break;
  case (UnidadeParcial *)0x15:
    pUVar12 = (UnidadeParcial *)(uint)*(ushort *)&pUVar21->field_0xc0;
    if (pUVar12 == (UnidadeParcial *)0xffff) break;
    uVar23 = FUN_0041a70b(param_1,uVar10);
    if ((char)uVar23 == '\0') {
      pUVar12 = (UnidadeParcial *)FUN_00449530(extraout_ECX_60,(int)((ulonglong)uVar23 >> 0x20));
      break;
    }
LAB_00454cbd:
    pUVar12 = (UnidadeParcial *)FUN_004457d3();
    break;
  case (UnidadeParcial *)0x16:
    pUVar12 = (UnidadeParcial *)FUN_0044a706(param_1);
    break;
  case (UnidadeParcial *)0x17:
    uVar23 = FUN_0041a70b(param_1,uVar10);
    if ((char)uVar23 == '\0') {
      uVar23 = FUN_0041a08c(extraout_ECX_83,(int)((ulonglong)uVar23 >> 0x20));
      if ((((uint)uVar23 & 0xff) != 200) &&
         (uVar23 = FUN_0041a08c(extraout_ECX_84,(int)((ulonglong)uVar23 >> 0x20)),
         (byte)uVar23 != pUVar21->proprietario_id)) {
        iVar17 = FUN_0042381f(extraout_ECX_85,(uint)pUVar21->celula_atual);
        if ((char)iVar17 != '\0') {
          uVar23 = FUN_0041a08c(extraout_ECX_86,0);
          bVar1 = tabela_unidades[CONCAT22((short)((ulonglong)uVar23 >> 0x30),sVar8)].
                  proprietario_id;
          uStack_70 = 100;
          bVar2 = (&DAT_004e19bc)[bVar1];
          bStack_28 = bVar1;
          bStack_20 = bVar1;
          uVar26 = FUN_004704dc(CONCAT31((int3)((uint)extraout_ECX_87 >> 8),(char)uVar23),0);
          if ((uint)bVar2 < (uint)(uVar26 % (ulonglong)uStack_70)) {
            if ((byte)(&DAT_004e19bc)[bVar1] < 5) {
              (&DAT_004e19bc)[bVar1] = 0;
            }
            else {
              (&DAT_004e19bc)[bVar1] = (&DAT_004e19bc)[bVar1] - 5;
            }
            FUN_00457058();
            if ((tabela_unidades[extraout_EDX_10].estado == 0) ||
               (tabela_unidades[extraout_EDX_10].estado == 4)) {
              iVar17 = 0;
            }
            else {
              iVar17 = 1;
            }
            uVar11 = extraout_ECX_89;
            if ((char)iVar17 != '\0') {
              iVar17 = (in_EAX & 0xffff) * 0x45;
              tabela_unidades[in_EAX & 0xffff].estado = 0;
              if (sVar8 == DAT_00496304) {
                uVar11 = 0xffff;
                DAT_004e0f36 = 0;
                DAT_004e0f37 = 0;
                DAT_004e0f3c = 0;
                DAT_00496304 = -1;
              }
            }
            pUVar12 = (UnidadeParcial *)CONCAT31((int3)((uint)iVar17 >> 8),bStack_28);
            if (bStack_28 == DAT_00508041) {
              pUVar12 = (UnidadeParcial *)FUN_0046994b(uVar11,0x1f6);
            }
          }
          else {
            uStack_50 = 10;
            if (*(short *)&pUVar21->field_0xc4 == 3) {
              FUN_00475118(extraout_ECX_88,(uint)bStack_20);
              uVar6 = FUN_004717b1();
              uVar11 = CONCAT31((int3)((uint)extraout_ECX_93 >> 8),uVar6);
              uVar6 = FUN_004717c2(uVar11,(ushort)uVar11);
              uVar7 = FUN_004717c2(extraout_ECX_94,(ushort)extraout_ECX_94);
              if ((ushort)CONCAT31(extraout_var,uVar6) < (ushort)CONCAT31(extraout_var_00,uVar7)) {
                if (bStack_20 == DAT_00508041) {
                  FUN_0046994b(extraout_ECX_95,0x1f5);
                }
                FUN_0047149d();
                uStack_50 = extraout_ECX_96;
              }
            }
            else {
              FUN_00475118(extraout_ECX_88,(uint)bStack_20);
              uStack_70 = extraout_ECX_90 & 0xff;
              FUN_0046769d(auStack_64,(short *)(auStack_7c + 2),(byte)extraout_ECX_90);
              uStack_34 = FUN_00461222(extraout_ECX_91,3);
              uVar10 = (uint)(byte)pUVar21->field_0xc4 % 3;
              FUN_004235bd(3,auStack_7c[uVar10] / 2);
              FUN_0042340f(uStack_34 & 0xffff,auStack_7c[uVar10] / 2);
              uStack_50 = 0;
              if (bStack_20 == DAT_00508041) {
                FUN_0046994b(extraout_ECX_92,0x1f5);
              }
            }
            if ((short)uStack_50 != 10) {
              (&DAT_004e19bc)[bStack_28] = (byte)(&DAT_004e19bc)[bStack_28] / 2;
            }
            FUN_00457058();
            if ((tabela_unidades[extraout_EDX_11].estado == 0) ||
               (tabela_unidades[extraout_EDX_11].estado == 4)) {
              pUVar12 = (UnidadeParcial *)0x0;
            }
            else {
              pUVar12 = (UnidadeParcial *)0x1;
            }
            if ((char)pUVar12 != '\0') {
              pUVar12 = (UnidadeParcial *)((in_EAX & 0xffff) * 0x45);
              tabela_unidades[in_EAX & 0xffff].estado = 0;
              if (sVar8 == DAT_00496304) {
                DAT_004e0f36 = 0;
                DAT_004e0f37 = 0;
                DAT_00496304 = -1;
                DAT_004e0f3c = 0;
              }
            }
          }
          break;
        }
        if (pUVar21->celula_destino == pUVar21->celula_atual) {
          uVar9 = FUN_0041aee2();
          pUVar21 = tabela_unidades;
          tabela_unidades[CONCAT22(extraout_var_10,sVar8)].celula_destino = uVar9;
          if (sVar8 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
          }
          pUVar21[CONCAT22(extraout_var_10,sVar8)].estado_caminho = 0;
        }
        goto LAB_004555a7;
      }
    }
LAB_00454d97:
    pUVar12 = (UnidadeParcial *)FUN_004457d3();
    *(undefined2 *)&pUVar21->field_0xc0 = 0xffff;
  }
switchD_0044d86e_default:
  return CONCAT44(param_2,pUVar12);
}
