/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004268d4, entrada 004268d4.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_004268d4(uint param_1,undefined4 param_2)

{
  byte bVar1;
  char cVar2;
  short sVar3;
  short sVar4;
  undefined2 uVar5;
  ushort uVar6;
  uint in_EAX;
  int iVar7;
  undefined2 extraout_var;
  int iVar8;
  uint uVar9;
  uint uVar10;
  uint uVar11;
  int iVar12;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_ECX_01;
  uint extraout_ECX_02;
  uint extraout_ECX_03;
  uint extraout_ECX_04;
  uint extraout_ECX_05;
  uint extraout_ECX_06;
  uint extraout_ECX_07;
  undefined4 extraout_ECX_08;
  undefined4 extraout_ECX_09;
  undefined *extraout_ECX_10;
  uint extraout_ECX_11;
  uint extraout_ECX_12;
  uint extraout_ECX_13;
  undefined4 extraout_ECX_14;
  undefined4 extraout_ECX_15;
  undefined4 extraout_ECX_16;
  undefined4 extraout_ECX_17;
  undefined4 extraout_ECX_18;
  undefined *extraout_ECX_19;
  undefined *extraout_ECX_20;
  undefined *extraout_ECX_21;
  undefined4 extraout_ECX_22;
  uint extraout_ECX_23;
  uint extraout_ECX_24;
  uint extraout_ECX_25;
  uint extraout_ECX_26;
  uint extraout_ECX_27;
  uint extraout_ECX_28;
  uint extraout_ECX_29;
  uint extraout_ECX_30;
  undefined2 extraout_var_00;
  undefined4 extraout_ECX_31;
  uint extraout_ECX_32;
  uint extraout_ECX_33;
  uint extraout_ECX_34;
  undefined2 extraout_var_01;
  undefined4 extraout_ECX_35;
  uint extraout_ECX_36;
  uint extraout_ECX_37;
  undefined4 extraout_ECX_38;
  uint extraout_ECX_39;
  uint extraout_ECX_40;
  uint extraout_ECX_41;
  uint extraout_ECX_42;
  uint extraout_ECX_43;
  uint extraout_ECX_44;
  uint extraout_ECX_45;
  uint extraout_ECX_46;
  undefined2 extraout_var_02;
  undefined4 extraout_ECX_47;
  uint extraout_ECX_48;
  uint extraout_ECX_49;
  uint extraout_ECX_50;
  undefined2 extraout_var_03;
  undefined4 extraout_ECX_51;
  uint extraout_ECX_52;
  undefined4 extraout_ECX_53;
  undefined2 extraout_var_04;
  ushort *extraout_ECX_54;
  ushort *puVar13;
  ushort *extraout_ECX_55;
  uint extraout_ECX_56;
  uint extraout_ECX_57;
  uint extraout_ECX_58;
  uint extraout_ECX_59;
  undefined4 extraout_ECX_60;
  undefined4 extraout_ECX_61;
  undefined4 extraout_ECX_62;
  undefined4 extraout_ECX_63;
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
  uint extraout_ECX_75;
  uint extraout_ECX_76;
  undefined *extraout_ECX_77;
  undefined *extraout_ECX_78;
  undefined *extraout_ECX_79;
  undefined4 extraout_EDX;
  undefined4 uVar14;
  undefined4 extraout_EDX_00;
  short sVar16;
  undefined *extraout_EDX_01;
  undefined *extraout_EDX_02;
  undefined *extraout_EDX_03;
  undefined *extraout_EDX_04;
  undefined *puVar15;
  undefined *extraout_EDX_05;
  undefined *extraout_EDX_06;
  undefined4 extraout_EDX_07;
  undefined4 extraout_EDX_08;
  undefined4 extraout_EDX_09;
  undefined4 extraout_EDX_10;
  undefined4 extraout_EDX_11;
  bool bVar17;
  longlong lVar18;
  ulonglong uVar19;
  ulonglong uVar20;
  undefined8 uVar21;
  ushort uVar22;
  uint local_4c;
  short local_40;
  short local_2c;

  uVar10 = in_EAX & 0xffff;
  iVar7 = uVar10 * 0x114;
  cVar2 = (&DAT_0049a0d0)[iVar7];
  uVar11 = CONCAT22((short)((uint)iVar7 >> 0x10),CONCAT11(cVar2 + -1,cVar2));
  switch(cVar2 + -1) {
  case '\0':
  case '\x01':
  case '\f':
  case '\x0f':
    iVar7 = (in_EAX & 0xffff) * 0x114;
    if ((&DAT_0049a0d0)[iVar7] == '\x15') {
      uVar20 = FUN_0044724a(param_1,&DAT_0049a0c8 + iVar7);
      bVar17 = (char)uVar20 == '\0';
      uVar10 = extraout_ECX;
LAB_00426949:
      if (bVar17) goto LAB_00426974;
    }
    else {
      if ((&DAT_0049a0d0)[iVar7] != '\x02') {
LAB_0042695d:
        iVar7 = FUN_004471b8(param_1,'\x01');
        uVar20 = CONCAT44(extraout_EDX,iVar7);
        bVar17 = (short)iVar7 == 0;
        uVar10 = extraout_ECX_01;
        goto LAB_00426949;
      }
      uVar20 = FUN_0044724a(param_1,&DAT_0049a0c8 + iVar7);
      uVar10 = extraout_ECX_00;
      param_1 = extraout_ECX_00;
      if ((char)uVar20 == '\0') goto LAB_0042695d;
    }
    uVar14 = (undefined4)(uVar20 >> 0x20);
    uVar11 = CONCAT31((int3)(uVar20 >> 8),1);
    goto LAB_00426976;
  case '\x02':
    puVar15 = &DAT_0049a0c8 + (in_EAX & 0xffff) * 0x114;
    if ((&DAT_0049a0d0)[(in_EAX & 0xffff) * 0x114] == '\x15') {
      uVar20 = FUN_0044724a(puVar15,&DAT_0049a0c8);
      bVar17 = (char)uVar20 == '\0';
LAB_00426b4a:
      if (!bVar17) goto LAB_00426b4c;
      uVar11 = (uint)(uint3)(uVar20 >> 8) << 8;
    }
    else {
      if ((&DAT_0049a0d0)[(in_EAX & 0xffff) * 0x114] != '\x02') {
LAB_00426b80:
        uVar11 = FUN_004471b8(puVar15,'\x01');
        uVar20 = (ulonglong)uVar11;
        bVar17 = (short)uVar11 == 0;
        goto LAB_00426b4a;
      }
      uVar20 = FUN_0044724a(puVar15,&DAT_0049a0c8);
      puVar15 = extraout_ECX_10;
      if ((char)uVar20 == '\0') goto LAB_00426b80;
LAB_00426b4c:
      uVar11 = CONCAT31((int3)(uVar20 >> 8),1);
    }
    if ((char)uVar11 != '\0') {
      iVar7 = (in_EAX & 0xffff) * 0x114;
      uVar11 = (uint)(byte)(&DAT_0049a0d0)[iVar7];
      if ((uVar11 == 3) && (((byte)DAT_00508f80 & 1) == 0)) {
        if ((&DAT_0049a13d)[iVar7] == '\0') {
          cVar2 = (&DAT_0049a13e)[iVar7];
          uVar11 = 0;
          if (cVar2 != '\0') {
            uVar11 = (uint)CONCAT11(cVar2 + -1,cVar2);
            (&DAT_0049a13e)[iVar7] = cVar2 + -1;
          }
        }
        else {
          bVar1 = (&DAT_0049a13e)[iVar7];
          uVar11 = (uint)bVar1;
          if (bVar1 < 0xf) {
            (&DAT_0049a13e)[iVar7] = bVar1 + 1;
          }
        }
      }
    }
    break;
  case '\x03':
    uVar9 = in_EAX & 0xffff;
    if ((&DAT_0049a0d0)[uVar9 * 0x114] == '\x15') {
      uVar20 = FUN_0044724a(uVar9,uVar10);
      uVar11 = (uint)uVar20;
      bVar17 = (char)uVar20 == '\0';
      uVar10 = extraout_ECX_11;
LAB_00426c67:
      if (!bVar17) goto LAB_00426c69;
      uVar11 = uVar11 & 0xffffff00;
    }
    else {
      if ((&DAT_0049a0d0)[(in_EAX & 0xffff) * 0x114] != '\x02') {
LAB_00426c9e:
        uVar11 = FUN_004471b8(uVar9,'\x01');
        bVar17 = (short)uVar11 == 0;
        uVar10 = extraout_ECX_13;
        goto LAB_00426c67;
      }
      uVar20 = FUN_0044724a(uVar9,&DAT_0049a0c8);
      uVar11 = (uint)uVar20;
      uVar10 = extraout_ECX_12;
      uVar9 = extraout_ECX_12;
      if ((char)uVar20 == '\0') goto LAB_00426c9e;
LAB_00426c69:
      uVar11 = CONCAT31((int3)(uVar11 >> 8),1);
    }
    if ((char)uVar11 != '\0') {
      uVar11 = FUN_00428cc0(uVar10,2);
      uVar11 = 5 - (uVar11 & 0xffff);
      if ((int)uVar11 <= (int)(uint)*(ushort *)(&DAT_0049a140 + iVar7)) {
        uVar21 = FUN_00457e0c(extraout_ECX_14,(uint)*(ushort *)(&DAT_0049a140 + iVar7));
        uVar11 = (uint)uVar21;
        if ((char)uVar21 != '\0') {
          uVar5 = FUN_004470d2(extraout_ECX_15,1);
          uVar11 = CONCAT22(extraout_var,uVar5);
          if ((char)uVar5 != '\0') {
            *(undefined2 *)(&DAT_0049a140 + iVar7) = 0;
            uVar6 = FUN_00457e6c((&DAT_0049a0cc)[iVar7]);
            FUN_0041f76e(extraout_ECX_16,(uint)uVar6);
            FUN_0044115f(extraout_ECX_17,0xe);
            uVar11 = FUN_004829c8(extraout_ECX_18,0x43);
          }
        }
      }
    }
    break;
  case '\x04':
  case '\r':
    iVar7 = (in_EAX & 0xffff) * 0x114;
    if ((&DAT_0049a0d0)[iVar7] == '\x15') {
      uVar20 = FUN_0044724a(param_1,&DAT_0049a0c8 + iVar7);
      bVar17 = (char)uVar20 == '\0';
      uVar11 = extraout_ECX_02;
LAB_004269be:
      uVar14 = (undefined4)(uVar20 >> 0x20);
      if (!bVar17) goto LAB_004269c0;
      bVar17 = false;
    }
    else {
      if ((&DAT_0049a0d0)[iVar7] != '\x02') {
LAB_004269d2:
        iVar7 = FUN_004471b8(param_1,'\x01');
        uVar20 = CONCAT44(extraout_EDX_00,iVar7);
        bVar17 = (short)iVar7 == 0;
        uVar11 = extraout_ECX_04;
        goto LAB_004269be;
      }
      uVar20 = FUN_0044724a(param_1,&DAT_0049a0c8 + iVar7);
      uVar14 = (undefined4)(uVar20 >> 0x20);
      uVar11 = extraout_ECX_03;
      param_1 = extraout_ECX_03;
      if ((char)uVar20 == '\0') goto LAB_004269d2;
LAB_004269c0:
      bVar17 = true;
    }
    if (bVar17) {
      FUN_004259e6(uVar11,uVar14);
    }
    uVar11 = FUN_00420d3a();
    break;
  case '\x05':
    puVar15 = &DAT_0049a0c8 + (in_EAX & 0xffff) * 0x114;
    if ((&DAT_0049a0d0)[(in_EAX & 0xffff) * 0x114] == '\x15') {
      uVar20 = FUN_0044724a(puVar15,&DAT_0049a0c8);
      bVar17 = (char)uVar20 == '\0';
      puVar15 = extraout_ECX_77;
LAB_004280e6:
      uVar14 = (undefined4)(uVar20 >> 0x20);
      if (!bVar17) goto LAB_004280e8;
      uVar11 = (uint)(uint3)(uVar20 >> 8) << 8;
    }
    else {
      iVar12 = (in_EAX & 0xffff) * 0x114;
      if ((&DAT_0049a0d0)[iVar12] != '\x02') {
LAB_0042811f:
        iVar12 = FUN_004471b8(puVar15,'\x01');
        uVar20 = CONCAT44(extraout_EDX_11,iVar12);
        bVar17 = (short)iVar12 == 0;
        puVar15 = extraout_ECX_79;
        goto LAB_004280e6;
      }
      uVar20 = FUN_0044724a(puVar15,iVar12);
      puVar15 = extraout_ECX_78;
      if ((char)uVar20 == '\0') goto LAB_0042811f;
LAB_004280e8:
      uVar14 = (undefined4)(uVar20 >> 0x20);
      uVar11 = CONCAT31((int3)(uVar20 >> 8),1);
    }
    if ((char)uVar11 != '\0') {
      FUN_004259e6(puVar15,uVar14);
      if (*(short *)(&DAT_0049a144 + iVar7) == 500) {
        *(undefined2 *)(&DAT_0049a144 + iVar7) = 0;
      }
      else {
        *(short *)(&DAT_0049a144 + iVar7) = *(short *)(&DAT_0049a144 + iVar7) + 1;
      }
      if (*(int *)(&DAT_0049a146 + iVar7) >> 0x10 == 0xfa) {
        *(undefined2 *)(&DAT_0049a148 + iVar7) = 0;
      }
      else {
        *(short *)(&DAT_0049a148 + iVar7) = *(short *)(&DAT_0049a148 + iVar7) + 1;
      }
      if (*(int *)(&DAT_0049a148 + iVar7) >> 0x10 == 0x168) {
        *(undefined2 *)(&DAT_0049a14a + iVar7) = 0;
      }
      else {
        *(short *)(&DAT_0049a14a + iVar7) = *(short *)(&DAT_0049a14a + iVar7) + 1;
      }
      uVar11 = *(int *)(&DAT_0049a144 + iVar7) >> 0x10;
      if (uVar11 == 0xa0) {
        *(undefined2 *)(&DAT_0049a146 + iVar7) = 0;
      }
      else {
        *(short *)(&DAT_0049a146 + iVar7) = *(short *)(&DAT_0049a146 + iVar7) + 1;
      }
    }
    break;
  case '\x06':
    puVar15 = &DAT_0049a0c8 + (in_EAX & 0xffff) * 0x114;
    if ((&DAT_0049a0d0)[(in_EAX & 0xffff) * 0x114] == '\x15') {
      uVar20 = FUN_0044724a(puVar15,uVar10);
      uVar11 = (uint)uVar20;
      bVar17 = (char)uVar20 == '\0';
      puVar15 = extraout_ECX_19;
LAB_00426daa:
      if (!bVar17) goto LAB_00426dac;
      uVar11 = uVar11 & 0xffffff00;
    }
    else {
      if ((&DAT_0049a0d0)[(in_EAX & 0xffff) * 0x114] != '\x02') {
LAB_00426dde:
        uVar11 = FUN_004471b8(puVar15,'\x01');
        bVar17 = (short)uVar11 == 0;
        puVar15 = extraout_ECX_21;
        goto LAB_00426daa;
      }
      uVar20 = FUN_0044724a(puVar15,&DAT_0049a0c8);
      uVar11 = (uint)uVar20;
      puVar15 = extraout_ECX_20;
      if ((char)uVar20 == '\0') goto LAB_00426dde;
LAB_00426dac:
      uVar11 = CONCAT31((int3)(uVar11 >> 8),1);
    }
    if ((char)uVar11 != '\0') {
      iVar7 = FUN_004471b8(puVar15,'\x01');
      uVar11 = FUN_00470bf7(extraout_ECX_22,(short)iVar7);
    }
    break;
  case '\a':
    if ((&DAT_0049a0d0)[(in_EAX & 0xffff) * 0x114] == '\x15') {
      uVar20 = FUN_0044724a(in_EAX,in_EAX & 0xffff);
      bVar17 = (char)uVar20 == '\0';
      uVar10 = extraout_ECX_05;
LAB_00426a5b:
      if (!bVar17) goto LAB_00426a5d;
      uVar11 = (uint)(uint3)(uVar20 >> 8) << 8;
    }
    else {
      uVar11 = in_EAX;
      if ((&DAT_0049a0d0)[(in_EAX & 0xffff) * 0x114] != '\x02') {
LAB_00426a91:
        uVar11 = FUN_004471b8(uVar11,'\x01');
        uVar20 = (ulonglong)uVar11;
        bVar17 = (short)uVar11 == 0;
        uVar10 = extraout_ECX_07;
        goto LAB_00426a5b;
      }
      uVar20 = FUN_0044724a(in_EAX,&DAT_0049a0c8);
      uVar10 = extraout_ECX_06;
      uVar11 = extraout_ECX_06;
      if ((char)uVar20 == '\0') goto LAB_00426a91;
LAB_00426a5d:
      uVar11 = CONCAT31((int3)(uVar20 >> 8),1);
    }
    if ((char)uVar11 != '\0') {
      FUN_004259e6(uVar10,in_EAX & 0xffff);
      FUN_00420d3a();
      uVar14 = extraout_ECX_08;
      if ((&DAT_0049a13c)[iVar7] == '\0') {
        FUN_00424de4();
        uVar14 = extraout_ECX_09;
      }
      uVar11 = FUN_00461e6e(uVar14,(short)in_EAX);
    }
    break;
  case '\t':
    if ((&DAT_0049a0d0)[(in_EAX & 0xffff) * 0x114] == '\x15') {
      uVar20 = FUN_0044724a(in_EAX,&DAT_0049a0c8);
      bVar17 = (char)uVar20 == '\0';
      uVar11 = extraout_ECX_23;
LAB_00426e92:
      if (!bVar17) goto LAB_00426e94;
      bVar17 = false;
    }
    else {
      uVar11 = in_EAX;
      if ((&DAT_0049a0d0)[(in_EAX & 0xffff) * 0x114] != '\x02') {
LAB_00426ec8:
        iVar12 = FUN_004471b8(uVar11,'\x01');
        bVar17 = (short)iVar12 == 0;
        uVar11 = extraout_ECX_25;
        goto LAB_00426e92;
      }
      uVar20 = FUN_0044724a(in_EAX,&DAT_0049a0c8);
      uVar11 = extraout_ECX_24;
      if ((char)uVar20 == '\0') goto LAB_00426ec8;
LAB_00426e94:
      bVar17 = true;
    }
    if (bVar17) {
      uVar21 = FUN_00424624(uVar11,in_EAX & 0xffff);
      iVar12 = (int)((ulonglong)uVar21 >> 0x20);
      uVar11 = extraout_ECX_26;
      if ((char)uVar21 == '\0') {
        (&DAT_0049a13e)[iVar7] = 0;
        (&DAT_0049a13c)[iVar7] = 0;
        *(undefined2 *)(&DAT_0049a140 + iVar7) = 0;
        iVar8 = iVar12 * 0x114;
        *(undefined2 *)(&DAT_0049a14e + iVar7) = 0xffff;
        if (((in_EAX & 0xffff) + DAT_00508f7c & 0x1f) == 0) {
          uVar21 = FUN_00423fb9(DAT_00508f7c,iVar12);
          sVar3 = (short)uVar21;
          if (((uint)uVar21 & 0xffff) == 0xffff) {
            sVar3 = FUN_00424123();
            uVar11 = extraout_ECX_28;
            if (sVar3 != -1) {
              *(undefined2 *)(&DAT_0049a150 + iVar8) = 0;
              (&DAT_0049a143)[iVar8] = 3;
            }
          }
          else {
            *(undefined2 *)(&DAT_0049a150 + iVar8) = 0;
            (&DAT_0049a143)[iVar8] = 1;
            uVar11 = extraout_ECX_27;
          }
        }
        else {
          sVar3 = -1;
          uVar11 = DAT_00508f7c;
        }
        *(short *)(&DAT_0049a14e + iVar7) = sVar3;
      }
      if (*(short *)(&DAT_0049a14e + iVar7) == -1) {
        cVar2 = (&DAT_0049a13e)[iVar7];
        if ((((cVar2 == '\x01') || (cVar2 == '\x02')) || (cVar2 == '\x03')) &&
           (DAT_00508f7c % 5 == 0)) {
          (&DAT_0049a13e)[iVar7] = (&DAT_0049a13e)[iVar7] + '\x01';
        }
        uVar20 = FUN_004704dc(uVar11,0);
        if (((int)(uVar20 % 100) == 0) && ((&DAT_0049a153)[iVar7] == (&DAT_0049a152)[iVar7])) {
          uVar21 = FUN_004704dc(extraout_ECX_38,0);
          (&DAT_0049a153)[iVar7] = ((byte)uVar21 & 0x1f) + 1;
        }
      }
      else {
        (&DAT_0049a13c)[iVar7] = 1;
        if ((&DAT_0049a143)[iVar7] == '\x01') {
          uVar6 = 0x20;
          uVar21 = FUN_00440df0(uVar11,0);
          sVar16 = (short)((ulonglong)uVar21 >> 0x30);
          iVar12 = (int)sVar16 >> 0xf;
          FUN_00440df0((CONCAT22(sVar16,(short)uVar21) + iVar12 * -0x100) - (uint)(iVar12 << 7 < 0)
                       >> 8 & 0xffff,0);
          iVar12 = (int)(*(ushort *)(&DAT_0049a0ca + iVar7) - 0x100) >> 0x1f;
          iVar12 = ((*(ushort *)(&DAT_0049a0ca + iVar7) - 0x100) + iVar12 * -0x100) -
                   (uint)(iVar12 << 7 < 0);
          uVar11 = extraout_ECX_29;
LAB_00427194:
          local_4c = iVar12 >> 8 & 0xffff;
          iVar12 = FUN_004796cb(uVar11,local_4c,uVar6);
          (&DAT_0049a153)[iVar7] = (char)iVar12;
          uVar11 = extraout_ECX_30;
        }
        else if ((&DAT_0049a143)[iVar7] == '\x03') {
          uVar11 = (uint)((ushort)((*(ushort *)
                                     (&DAT_00495d8e +
                                     (uint)(byte)(&DAT_0049a0d0)
                                                 [(uint)*(ushort *)(&DAT_0049a14e + iVar7) * 0x114]
                                     * 0x34) >> 1) * 0x100 +
                                   (*(ushort *)
                                     (&DAT_00495d8c +
                                     (uint)(byte)(&DAT_0049a0d0)
                                                 [(uint)*(ushort *)(&DAT_0049a14e + iVar7) * 0x114]
                                     * 0x34) >> 1) +
                                  *(short *)(&DAT_0049a0ca +
                                            (uint)*(ushort *)(&DAT_0049a14e + iVar7) * 0x114)) >> 8)
          ;
          iVar12 = (int)(*(ushort *)(&DAT_0049a0ca + iVar7) - 0x100) >> 0x1f;
          iVar12 = ((*(ushort *)(&DAT_0049a0ca + iVar7) - 0x100) + iVar12 * -0x100) -
                   (uint)(iVar12 << 7 < 0);
          uVar6 = 0x20;
          goto LAB_00427194;
        }
        puVar15 = (undefined *)(DAT_00508f7c % (uint)DAT_00495bfc);
        if ((puVar15 == (undefined *)0x0) && ((&DAT_0049a153)[iVar7] == (&DAT_0049a152)[iVar7])) {
          *(undefined2 *)(&DAT_0049a140 + iVar7) = 100;
          if ((&DAT_0049a143)[iVar7] == '\x01') {
            if (((&DAT_0049a13c)[iVar7] != '\0') &&
               ((&DAT_0049a153)[iVar7] == (&DAT_0049a152)[iVar7])) {
              (&DAT_0049a13e)[iVar7] = 1;
              uVar10 = (uint)*(ushort *)(&DAT_0049a14e + iVar7);
              uVar11 = in_EAX & 0xffff;
              uVar21 = FUN_0044113e(0,0);
              FUN_00425100(CONCAT22(extraout_var_00,(short)uVar21),(&DAT_0049a0d0)[iVar7],uVar10,
                           (short)uVar11);
              bVar1 = unidade_obter_proprietario(*(ushort *)(&DAT_0049a14e + iVar7));
              FUN_00419d54(extraout_ECX_31,bVar1);
              iVar12 = (in_EAX & 0xffff) * 0x114;
              uVar11 = extraout_ECX_32;
              puVar15 = extraout_EDX_01;
              if ((&DAT_0049a0cc)[iVar12] == DAT_00508041) {
                uVar10 = FUN_0041a0ab();
                uVar11 = extraout_ECX_33;
                puVar15 = extraout_EDX_02;
                if (*(int *)(&DAT_0049a1c8 + iVar12) == -1) {
                  bVar1 = (&DAT_0049a0d0)[iVar12];
                  goto LAB_004272a0;
                }
              }
            }
          }
          else if ((((&DAT_0049a143)[iVar7] == '\x03') && ((&DAT_0049a13c)[iVar7] != '\0')) &&
                  ((&DAT_0049a153)[iVar7] == (&DAT_0049a152)[iVar7])) {
            (&DAT_0049a13e)[iVar7] = 1;
            uVar10 = (uint)*(ushort *)(&DAT_0049a14e + iVar7);
            uVar11 = in_EAX & 0xffff;
            uVar5 = FUN_0041aee2();
            FUN_00425100(CONCAT22(extraout_var_01,uVar5),(&DAT_0049a0d0)[iVar7],uVar10,(short)uVar11
                        );
            FUN_00419d54(extraout_ECX_35,
                         (&DAT_0049a0cc)[(uint)*(ushort *)(&DAT_0049a14e + iVar7) * 0x114]);
            iVar12 = (in_EAX & 0xffff) * 0x114;
            puVar15 = &DAT_0049a0c8 + iVar12;
            uVar11 = extraout_ECX_36;
            if (DAT_00508041 == (&DAT_0049a0cc)[iVar12]) {
              uVar10 = FUN_0041a0ab();
              uVar11 = extraout_ECX_37;
              puVar15 = extraout_EDX_04;
              if (*(int *)(extraout_EDX_04 + 0x100) == -1) {
                bVar1 = extraout_EDX_04[8];
LAB_004272a0:
                FUN_0048aa79(0,(uint)bVar1 << 0x10 | 0x2300,uVar10);
                uVar11 = extraout_ECX_34;
                puVar15 = extraout_EDX_03;
              }
            }
          }
        }
        else {
          uVar10 = (uint)*(ushort *)(&DAT_0049a140 + iVar7);
          if ((uVar10 != 0) && (uVar10 != 0xffff)) {
            uVar11 = uVar10 - 1;
            *(short *)(&DAT_0049a140 + iVar7) = (short)uVar11;
          }
          cVar2 = (&DAT_0049a13e)[iVar7];
          if ((((cVar2 == '\x01') || (cVar2 == '\x02')) || (cVar2 == '\x03')) &&
             (puVar15 = (undefined *)(DAT_00508f7c % 5), puVar15 == (undefined *)0x0)) {
            (&DAT_0049a13e)[iVar7] = (&DAT_0049a13e)[iVar7] + '\x01';
          }
        }
        bVar1 = (&DAT_0049a143)[iVar7];
        if (bVar1 != 0) {
          if (bVar1 < 2) {
            lVar18 = FUN_00443dad(uVar11,(uint)puVar15);
            cVar2 = (char)lVar18;
          }
          else {
            if (bVar1 != 3) goto LAB_004274a7;
            cVar2 = (&DAT_0049a0cd)[(uint)*(ushort *)(&DAT_0049a14e + iVar7) * 0x114] != '\0';
          }
          if (cVar2 == '\0') {
            *(undefined2 *)(&DAT_0049a14e + iVar7) = 0xffff;
            (&DAT_0049a143)[iVar7] = 0xff;
            (&DAT_0049a13e)[iVar7] = 0;
            (&DAT_0049a13c)[iVar7] = 0;
          }
        }
      }
LAB_004274a7:
      bVar1 = (&DAT_0049a153)[iVar7];
      if ((bVar1 != (&DAT_0049a152)[iVar7]) && ((DAT_00508f7c & 1) == 0)) {
        if (((byte)(&DAT_0049a152)[iVar7] < bVar1) &&
           ((int)((uint)bVar1 - (uint)(byte)(&DAT_0049a152)[iVar7]) < 0x10)) {
LAB_004274fe:
          cVar2 = (byte)(&DAT_0049a152)[iVar7] % 0x20 + 1;
        }
        else {
          if (((byte)(&DAT_0049a153)[iVar7] < (byte)(&DAT_0049a152)[iVar7]) &&
             (0x10 < (int)((uint)(byte)(&DAT_0049a152)[iVar7] - (uint)(byte)(&DAT_0049a153)[iVar7]))
             ) goto LAB_004274fe;
          if ((&DAT_0049a152)[iVar7] == '\x01') {
            cVar2 = ' ';
          }
          else {
            cVar2 = (&DAT_0049a152)[iVar7] + -1;
          }
        }
        (&DAT_0049a152)[iVar7] = cVar2;
      }
    }
    uVar11 = (uint)(byte)(&DAT_0049a13e)[iVar7];
    if (uVar11 == 4) {
      (&DAT_0049a13e)[iVar7] = 0;
    }
    break;
  case '\n':
    if ((&DAT_0049a0d0)[(in_EAX & 0xffff) * 0x114] == '\x15') {
      uVar20 = FUN_0044724a(in_EAX,&DAT_0049a0c8);
      bVar17 = (char)uVar20 == '\0';
      uVar10 = extraout_ECX_39;
LAB_0042759a:
      if (!bVar17) goto LAB_0042759c;
      uVar11 = (uint)(uint3)(uVar20 >> 8) << 8;
    }
    else {
      uVar11 = in_EAX;
      if ((&DAT_0049a0d0)[(in_EAX & 0xffff) * 0x114] != '\x02') {
LAB_004275d0:
        uVar11 = FUN_004471b8(uVar11,'\x01');
        uVar20 = (ulonglong)uVar11;
        bVar17 = (short)uVar11 == 0;
        uVar10 = extraout_ECX_41;
        goto LAB_0042759a;
      }
      uVar20 = FUN_0044724a(in_EAX,&DAT_0049a0c8);
      uVar10 = extraout_ECX_40;
      uVar11 = extraout_ECX_40;
      if ((char)uVar20 == '\0') goto LAB_004275d0;
LAB_0042759c:
      uVar11 = CONCAT31((int3)(uVar20 >> 8),1);
    }
    if ((char)uVar11 == '\0') break;
    uVar21 = FUN_00424624(uVar10,in_EAX & 0xffff);
    iVar12 = (int)((ulonglong)uVar21 >> 0x20);
    uVar11 = extraout_ECX_42;
    if ((char)uVar21 == '\0') {
      (&DAT_0049a13e)[iVar7] = 0;
      (&DAT_0049a13c)[iVar7] = 0;
      *(undefined2 *)(&DAT_0049a140 + iVar7) = 0;
      iVar8 = iVar12 * 0x114;
      *(undefined2 *)(&DAT_0049a14e + iVar7) = 0xffff;
      if (((in_EAX & 0xffff) + DAT_00508f7c & 0x1f) == 0) {
        uVar21 = FUN_00423fb9(DAT_00508f7c,iVar12);
        sVar4 = (short)uVar21;
        if (((uint)uVar21 & 0xffff) == 0xffff) {
          sVar4 = FUN_00424123();
          uVar11 = extraout_ECX_44;
          if (sVar4 != -1) {
            *(undefined2 *)(&DAT_0049a150 + iVar8) = 0;
            (&DAT_0049a143)[iVar8] = 3;
          }
        }
        else {
          *(undefined2 *)(&DAT_0049a150 + iVar8) = 0;
          (&DAT_0049a143)[iVar8] = 1;
          uVar11 = extraout_ECX_43;
        }
      }
      else {
        sVar4 = -1;
        uVar11 = DAT_00508f7c;
      }
      *(short *)(&DAT_0049a14e + iVar7) = sVar4;
    }
    if (*(short *)(&DAT_0049a14e + iVar7) == -1) {
      uVar19 = FUN_004704dc(uVar11,0);
      iVar12 = (int)(uVar19 % 100);
      uVar20 = CONCAT44(iVar12,(int)(uVar19 / 100));
      if ((iVar12 == 0) &&
         (uVar20 = (ulonglong)CONCAT31((int3)(uVar19 / 100 >> 8),(&DAT_0049a153)[iVar7]),
         (&DAT_0049a153)[iVar7] == (&DAT_0049a152)[iVar7])) {
        uVar21 = FUN_004704dc(extraout_ECX_53,0);
        uVar11 = (uint)uVar21 & 0xffffff1f;
        cVar2 = (char)uVar11 + '\x01';
        (&DAT_0049a153)[iVar7] = cVar2;
        uVar20 = (ulonglong)CONCAT31((int3)(uVar11 >> 8),cVar2);
      }
    }
    else {
      (&DAT_0049a13c)[iVar7] = 1;
      if ((&DAT_0049a143)[iVar7] == '\x01') {
        uVar22 = 0x20;
        uVar21 = FUN_00440df0(uVar11,0);
        sVar16 = (short)((ulonglong)uVar21 >> 0x30);
        iVar12 = (int)sVar16 >> 0xf;
        FUN_00440df0((CONCAT22(sVar16,(short)uVar21) + iVar12 * -0x100) - (uint)(iVar12 << 7 < 0) >>
                     8 & 0xffff,0);
        uVar6 = *(ushort *)(&DAT_0049a0ca + iVar7);
        uVar11 = extraout_ECX_45;
LAB_00427893:
        iVar12 = FUN_004796cb(uVar11,(int)(uint)uVar6 >> 8,uVar22);
        (&DAT_0049a153)[iVar7] = (char)iVar12;
        uVar11 = extraout_ECX_46;
      }
      else if ((&DAT_0049a143)[iVar7] == '\x03') {
        uVar11 = (uint)((ushort)((*(ushort *)
                                   (&DAT_00495d8e +
                                   (uint)(byte)(&DAT_0049a0d0)
                                               [(uint)*(ushort *)(&DAT_0049a14e + iVar7) * 0x114] *
                                   0x34) >> 1) * 0x100 +
                                 (*(ushort *)
                                   (&DAT_00495d8c +
                                   (uint)(byte)(&DAT_0049a0d0)
                                               [(uint)*(ushort *)(&DAT_0049a14e + iVar7) * 0x114] *
                                   0x34) >> 1) +
                                *(short *)(&DAT_0049a0ca +
                                          (uint)*(ushort *)(&DAT_0049a14e + iVar7) * 0x114)) >> 8);
        uVar22 = 0x20;
        uVar6 = *(ushort *)(&DAT_0049a0ca + iVar7);
        goto LAB_00427893;
      }
      puVar15 = (undefined *)(DAT_00508f7c % (uint)DAT_00495bfa);
      if ((puVar15 == (undefined *)0x0) && ((&DAT_0049a153)[iVar7] == (&DAT_0049a152)[iVar7])) {
        uVar10 = (uint)(byte)(&DAT_0049a143)[iVar7];
        *(undefined2 *)(&DAT_0049a140 + iVar7) = 100;
        if (uVar10 == 1) {
          if (((&DAT_0049a13c)[iVar7] != '\0') &&
             (uVar10 = 0, (&DAT_0049a153)[iVar7] == (&DAT_0049a152)[iVar7])) {
            (&DAT_0049a13e)[iVar7] = 1;
            uVar10 = (uint)*(ushort *)(&DAT_0049a14e + iVar7);
            uVar11 = in_EAX & 0xffff;
            uVar21 = FUN_0044113e(0,0);
            FUN_00425100(CONCAT22(extraout_var_02,(short)uVar21),(&DAT_0049a0d0)[iVar7],uVar10,
                         (short)uVar11);
            bVar1 = unidade_obter_proprietario(*(ushort *)(&DAT_0049a14e + iVar7));
            FUN_00419d54(extraout_ECX_47,bVar1);
            uVar9 = (in_EAX & 0xffff) * 0x114;
            uVar10 = CONCAT31((int3)(uVar9 >> 8),(&DAT_0049a0cc)[uVar9]);
            bVar17 = (&DAT_0049a0cc)[uVar9] == DAT_00508041;
            uVar11 = extraout_ECX_48;
            goto LAB_00427969;
          }
        }
        else if (((uVar10 == 3) && ((&DAT_0049a13c)[iVar7] != '\0')) &&
                (uVar10 = 0, (&DAT_0049a153)[iVar7] == (&DAT_0049a152)[iVar7])) {
          (&DAT_0049a13e)[iVar7] = 1;
          uVar10 = (uint)*(ushort *)(&DAT_0049a14e + iVar7);
          uVar11 = in_EAX & 0xffff;
          uVar5 = FUN_0041aee2();
          FUN_00425100(CONCAT22(extraout_var_03,uVar5),(&DAT_0049a0d0)[iVar7],uVar10,(short)uVar11);
          FUN_00419d54(extraout_ECX_51,
                       (&DAT_0049a0cc)[(uint)*(ushort *)(&DAT_0049a14e + iVar7) * 0x114]);
          uVar10 = (in_EAX & 0xffff) * 0x114;
          bVar17 = DAT_00508041 == (&DAT_0049a0cc)[uVar10];
          uVar11 = extraout_ECX_52;
          uVar9 = uVar10;
LAB_00427969:
          puVar15 = &DAT_0049a0c8 + uVar9;
          if (bVar17) {
            uVar10 = FUN_0041a0ab();
            uVar11 = extraout_ECX_49;
            puVar15 = extraout_EDX_05;
            if (*(int *)(extraout_EDX_05 + 0x100) == -1) {
              uVar10 = FUN_0048aa79(0,(uint)(byte)extraout_EDX_05[8] << 0x10 | 0x2300,uVar10);
              uVar11 = extraout_ECX_50;
              puVar15 = extraout_EDX_06;
            }
          }
        }
      }
      else {
        uVar10 = (uint)*(ushort *)(&DAT_0049a140 + iVar7);
        if ((uVar10 != 0) && (uVar10 != 0xffff)) {
          (&DAT_0049a13e)[iVar7] = 0;
          uVar11 = CONCAT22((short)(uVar11 >> 0x10),*(undefined2 *)(&DAT_0049a140 + iVar7)) - 1;
          *(short *)(&DAT_0049a140 + iVar7) = (short)uVar11;
        }
      }
      bVar1 = (&DAT_0049a143)[iVar7];
      uVar14 = CONCAT31((int3)(uVar10 >> 8),bVar1);
      uVar20 = CONCAT44(puVar15,uVar14);
      if (bVar1 != 0) {
        if (bVar1 < 2) {
          uVar20 = FUN_00443dad(uVar11,(uint)puVar15);
        }
        else {
          uVar20 = CONCAT44(puVar15,uVar14);
          if (bVar1 != 3) goto LAB_00427b1c;
          uVar20 = (ulonglong)
                   CONCAT24(*(ushort *)(&DAT_0049a14e + iVar7),
                            (uint)((&DAT_0049a0cd)[(uint)*(ushort *)(&DAT_0049a14e + iVar7) * 0x114]
                                  != '\0'));
        }
        if ((char)uVar20 == '\0') {
          *(undefined2 *)(&DAT_0049a14e + iVar7) = 0xffff;
          (&DAT_0049a143)[iVar7] = 0xff;
          (&DAT_0049a13c)[iVar7] = 0;
        }
      }
    }
LAB_00427b1c:
    bVar1 = (&DAT_0049a153)[iVar7];
    uVar11 = CONCAT31((int3)(uVar20 >> 8),bVar1);
    if ((bVar1 != (&DAT_0049a152)[iVar7]) && ((DAT_00508f7c & 1) == 0)) {
      if ((((byte)(&DAT_0049a152)[iVar7] < bVar1) &&
          ((int)((uint)bVar1 - (uint)(byte)(&DAT_0049a152)[iVar7]) < 0x10)) ||
         (((byte)(&DAT_0049a153)[iVar7] < (byte)(&DAT_0049a152)[iVar7] &&
          (0x10 < (int)((uint)(byte)(&DAT_0049a152)[iVar7] - (uint)(byte)(&DAT_0049a153)[iVar7])))))
      {
        uVar11 = (byte)(&DAT_0049a152)[iVar7] / 0x20;
        (&DAT_0049a152)[iVar7] = (byte)(&DAT_0049a152)[iVar7] % 0x20 + 1;
      }
      else {
        if ((byte)(&DAT_0049a152)[iVar7] == 1) {
          uVar11 = 0x20;
        }
        else {
          uVar11 = (byte)(&DAT_0049a152)[iVar7] - 1;
        }
        (&DAT_0049a152)[iVar7] = (char)uVar11;
      }
    }
    break;
  case '\v':
    if ((DAT_005099af != '\0') && (DAT_004dfb50 == '\0')) {
      DAT_004dfb50 = '\x01';
      uVar21 = FUN_00426799(CONCAT31((int3)(param_1 >> 8),1),uVar10);
      uVar6 = (ushort)uVar21;
      if (((uint)uVar21 & 0xffff) != 0xffff) {
        if ((((&DAT_0049a13e)[(uint)uVar6 * 0x114] == '\0') ||
            ((&DAT_0049a13e)[(uint)uVar6 * 0x114] == '\x0f')) ||
           ((&DAT_0049a13e)[(uint)uVar6 * 0x114] == '\x1f')) {
          bVar17 = false;
        }
        else {
          bVar17 = true;
        }
        if (!bVar17) {
          if ((&DAT_0049a13e)[(uint)uVar6 * 0x114] == '\x0f') {
            FUN_004195ca(CONCAT22(extraout_var_04,
                                  *(undefined2 *)(&DAT_0049a0ca + (uint)uVar6 * 0x114)),(uint)uVar6)
            ;
          }
          else {
            FUN_004193d4(CONCAT22(extraout_var_04,
                                  *(undefined2 *)(&DAT_0049a0ca + (uint)uVar6 * 0x114)),uVar6);
          }
        }
      }
    }
    cVar2 = (&DAT_0049a13e)[(in_EAX & 0xffff) * 0x114];
    if (((cVar2 == '\0') || (cVar2 == '\x0f')) || (cVar2 == '\x1f')) {
      uVar11 = 0;
    }
    else {
      uVar11 = 1;
    }
    if ((char)uVar11 != '\0') {
      cVar2 = (&DAT_0049a13e)[iVar7];
      (&DAT_0049a13e)[iVar7] = cVar2 + 1U;
      if (0x1e < (byte)(cVar2 + 1U)) {
        (&DAT_0049a13e)[iVar7] = 0;
      }
      uVar11 = (uint)(byte)(&DAT_0049a13e)[iVar7];
      if (uVar11 == 0xf) {
        FUN_0047623e(&DAT_0049a194 + iVar7,1);
        puVar13 = extraout_ECX_54;
      }
      else {
        if ((uVar11 < 0x1f) && (uVar11 != 0)) break;
        FUN_0047622e(&DAT_0049a194 + iVar7,1);
        puVar13 = extraout_ECX_55;
      }
      uVar11 = FUN_0043e138(puVar13,in_EAX & 0xffff,0);
    }
    break;
  case '\x0e':
    if (cVar2 == '\x15') {
      uVar20 = FUN_0044724a(param_1,0x15);
      bVar17 = (char)uVar20 == '\0';
      uVar10 = extraout_ECX_56;
LAB_00427d72:
      if (!bVar17) goto LAB_00427d78;
LAB_00426974:
      uVar14 = (undefined4)(uVar20 >> 0x20);
      uVar11 = (uint)uVar20 & 0xffffff00;
    }
    else {
      if (cVar2 != '\x02') {
LAB_00427d8d:
        iVar7 = FUN_004471b8(param_1,'\x01');
        uVar20 = CONCAT44(extraout_EDX_07,iVar7);
        bVar17 = (short)iVar7 == 0;
        uVar10 = extraout_ECX_58;
        goto LAB_00427d72;
      }
      uVar20 = FUN_0044724a(param_1,2);
      uVar10 = extraout_ECX_57;
      param_1 = extraout_ECX_57;
      if ((char)uVar20 == '\0') goto LAB_00427d8d;
LAB_00427d78:
      uVar14 = (undefined4)(uVar20 >> 0x20);
      uVar11 = CONCAT31((int3)(uVar20 >> 8),1);
    }
LAB_00426976:
    if ((char)uVar11 != '\0') {
      uVar21 = FUN_004259e6(uVar10,uVar14);
      uVar11 = (uint)uVar21;
    }
    break;
  case '\x10':
    uVar11 = FUN_004249de();
    *(short *)(&DAT_0049a14e + iVar7) = (short)uVar11;
    break;
  case '\x11':
    if (cVar2 == '\x15') {
      uVar20 = FUN_0044724a(param_1,0x15);
      bVar17 = (char)uVar20 == '\0';
      uVar10 = extraout_ECX_64;
LAB_00427f01:
      uVar14 = (undefined4)(uVar20 >> 0x20);
      if (!bVar17) goto LAB_00427f03;
      uVar11 = (uint)(uint3)(uVar20 >> 8) << 8;
    }
    else {
      if (cVar2 != '\x02') {
LAB_00427f15:
        iVar12 = FUN_004471b8(param_1,'\x01');
        uVar20 = CONCAT44(extraout_EDX_09,iVar12);
        bVar17 = (short)iVar12 == 0;
        uVar10 = extraout_ECX_66;
        goto LAB_00427f01;
      }
      uVar20 = FUN_0044724a(param_1,2);
      uVar10 = extraout_ECX_65;
      param_1 = extraout_ECX_65;
      if ((char)uVar20 == '\0') goto LAB_00427f15;
LAB_00427f03:
      uVar14 = (undefined4)(uVar20 >> 0x20);
      uVar11 = CONCAT31((int3)(uVar20 >> 8),1);
    }
    if ((char)uVar11 != '\0') {
      if ((&DAT_0049a13c)[iVar7] != '\0') {
        if ((&DAT_0049a142)[iVar7] == '\0') {
          FUN_004259e6(uVar10,uVar14);
          uVar10 = extraout_ECX_68;
        }
        else {
          FUN_0042195c(uVar10,uVar14);
          uVar10 = extraout_ECX_67;
        }
      }
      bVar1 = (&DAT_004dfb4c)[(byte)(&DAT_0049a0cc)[iVar7]];
      uVar6 = FUN_00456d92(uVar10,0x10);
      if (uVar6 < bVar1) {
        uVar11 = FUN_004471b8(extraout_ECX_69,'\x06');
        if ((short)uVar11 == 0) {
          FUN_00447148(extraout_ECX_70,1);
          uVar11 = FUN_00447483(extraout_ECX_71,6);
        }
      }
      else {
        bVar1 = (&DAT_004dfb4c)[(byte)(&DAT_0049a0cc)[iVar7]];
        uVar6 = FUN_00456d92(extraout_ECX_69,0x10);
        uVar11 = (uint)uVar6;
        if (bVar1 <= uVar11) {
          FUN_00447148(extraout_ECX_72,1);
          uVar11 = FUN_004472ea(extraout_ECX_73,'\x06');
        }
      }
    }
    break;
  case '\x12':
    if (cVar2 == '\x15') {
      uVar20 = FUN_0044724a(param_1,0x15);
      bVar17 = (char)uVar20 == '\0';
      uVar10 = extraout_ECX_74;
LAB_00428051:
      uVar14 = (undefined4)(uVar20 >> 0x20);
      if (!bVar17) goto LAB_00428053;
      uVar11 = (uint)(uint3)(uVar20 >> 8) << 8;
    }
    else {
      if (cVar2 != '\x02') {
LAB_00428065:
        iVar7 = FUN_004471b8(param_1,'\x01');
        uVar20 = CONCAT44(extraout_EDX_10,iVar7);
        bVar17 = (short)iVar7 == 0;
        uVar10 = extraout_ECX_76;
        goto LAB_00428051;
      }
      uVar20 = FUN_0044724a(param_1,2);
      uVar10 = extraout_ECX_75;
      param_1 = extraout_ECX_75;
      if ((char)uVar20 == '\0') goto LAB_00428065;
LAB_00428053:
      uVar14 = (undefined4)(uVar20 >> 0x20);
      uVar11 = CONCAT31((int3)(uVar20 >> 8),1);
    }
    if ((char)uVar11 != '\0') {
      uVar21 = FUN_00424c2e(uVar10,uVar14);
      uVar11 = (uint)uVar21;
    }
    break;
  case '\x13':
    if (cVar2 == '\x15') {
      uVar20 = FUN_0044724a(param_1,0x15);
      uVar11 = (uint)uVar20;
      bVar17 = (char)uVar20 == '\0';
LAB_00427db9:
      if (!bVar17) goto LAB_00427dbb;
      uVar11 = uVar11 & 0xffffff00;
    }
    else {
      if (cVar2 != '\x02') {
LAB_00427dcd:
        uVar11 = FUN_004471b8(param_1,'\x01');
        bVar17 = (short)uVar11 == 0;
        goto LAB_00427db9;
      }
      uVar20 = FUN_0044724a(param_1,2);
      uVar11 = (uint)uVar20;
      param_1 = extraout_ECX_59;
      if ((char)uVar20 == '\0') goto LAB_00427dcd;
LAB_00427dbb:
      uVar11 = CONCAT31((int3)(uVar11 >> 8),1);
    }
    if ((char)uVar11 != '\0') {
      if (((&DAT_0049a13d)[iVar7] != '\0') && ((&DAT_0049a1cc)[iVar7] == '\0')) {
        *(undefined4 *)(&DAT_0049a1d0 + iVar7) = 1;
        (&DAT_0049a1cc)[iVar7] = 1;
      }
      FUN_00426418();
      FUN_004259e6(extraout_ECX_60,extraout_EDX_08);
      uVar11 = *(int *)(&DAT_0049a146 + iVar7) >> 0x10;
      if ((int)uVar11 < 1) {
        uVar11 = (uint)*(ushort *)(&DAT_00495d90 + (uint)(byte)(&DAT_0049a0d0)[iVar7] * 0x34);
        if (*(int *)(&DAT_0049a148 + iVar7) >> 0x10 < (int)uVar11) {
          *(undefined2 *)(&DAT_0049a148 + iVar7) = 0x14;
          *(short *)(&DAT_0049a14a + iVar7) = *(short *)(&DAT_0049a14a + iVar7) + 0x14;
        }
        else {
          FUN_00447148(extraout_ECX_61,2);
          FUN_00447483(extraout_ECX_62,6);
          uVar11 = FUN_00447483(extraout_ECX_63,4);
          (&DAT_0049a13d)[iVar7] = 1;
        }
      }
      else {
        *(short *)(&DAT_0049a148 + iVar7) = *(short *)(&DAT_0049a148 + iVar7) + -1;
      }
    }
  }
  return CONCAT44(param_2,uVar11);
}
