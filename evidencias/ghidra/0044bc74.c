/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044bc74, entrada 0044bc74.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Removing unreachable block (ram,0x0044bcde) */
/* WARNING: Removing unreachable block (ram,0x0044d88d) */
/* WARNING: Removing unreachable block (ram,0x0044c11f) */
/* WARNING: Removing unreachable block (ram,0x0044d026) */
/* WARNING: Removing unreachable block (ram,0x0044da6a) */

undefined8 __fastcall FUN_0044bc74(undefined4 param_1,uint param_2)

{
  ushort *puVar1;
  ushort uVar2;
  bool bVar3;
  bool bVar4;
  UnidadeParcial *pUVar5;
  byte bVar6;
  char cVar7;
  short sVar8;
  ushort uVar9;
  uint in_EAX;
  undefined3 uVar15;
  UnidadeParcial *pUVar10;
  UnidadeParcial *pUVar11;
  undefined2 extraout_var;
  uint uVar12;
  undefined4 uVar13;
  int iVar14;
  uint uVar16;
  undefined2 uVar18;
  undefined4 extraout_ECX;
  int extraout_ECX_00;
  undefined4 extraout_ECX_01;
  int extraout_ECX_02;
  int extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  int extraout_ECX_06;
  int extraout_ECX_07;
  byte *extraout_ECX_08;
  undefined4 extraout_ECX_09;
  int extraout_ECX_10;
  int extraout_ECX_11;
  UnidadeParcial *extraout_ECX_12;
  undefined4 extraout_ECX_13;
  undefined4 extraout_ECX_14;
  undefined4 extraout_ECX_15;
  undefined2 extraout_var_00;
  undefined4 extraout_ECX_16;
  undefined4 extraout_ECX_17;
  undefined4 extraout_ECX_18;
  ushort *extraout_ECX_19;
  undefined4 extraout_ECX_20;
  undefined4 extraout_ECX_21;
  int extraout_ECX_22;
  undefined4 extraout_ECX_23;
  ushort *extraout_ECX_24;
  undefined4 extraout_ECX_25;
  undefined4 extraout_ECX_26;
  uint extraout_ECX_27;
  undefined4 extraout_ECX_28;
  undefined4 extraout_ECX_29;
  int extraout_ECX_30;
  undefined4 extraout_ECX_31;
  undefined4 extraout_ECX_32;
  int extraout_ECX_33;
  int extraout_ECX_34;
  byte *extraout_ECX_35;
  byte *extraout_ECX_36;
  byte *extraout_ECX_37;
  byte *pbVar17;
  uint extraout_ECX_38;
  ushort *extraout_ECX_39;
  int extraout_ECX_40;
  int extraout_ECX_41;
  uint extraout_ECX_42;
  undefined4 extraout_ECX_43;
  undefined4 extraout_ECX_44;
  undefined4 extraout_ECX_45;
  undefined4 extraout_ECX_46;
  byte bVar19;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 extraout_EDX_02;
  uint extraout_EDX_03;
  uint uVar20;
  undefined4 extraout_EDX_04;
  undefined4 extraout_EDX_05;
  undefined4 extraout_EDX_06;
  uint uVar21;
  short sVar22;
  longlong lVar23;
  undefined8 uVar24;
  ulonglong uVar25;
  UnidadeParcial *local_4c;

  pUVar5 = tabela_unidades;
  uVar21 = in_EAX & 0xffff;
  uVar16 = uVar21 * 0x114;
  bVar6 = (byte)in_EAX;
  pUVar11 = (UnidadeParcial *)CONCAT22((short)(in_EAX >> 0x10),(ushort)bVar6);
  bVar3 = false;
  bVar19 = tabela_unidades[uVar21].tipo_id;
  sVar22 = (short)in_EAX;
  uVar15 = (undefined3)((uint)pUVar11 >> 8);
  if (bVar19 < 6) {
    if (bVar19 != 5) goto switchD_0044d86e_default;
    pUVar11 = (UnidadeParcial *)CONCAT31(uVar15,tabela_unidades[uVar21].field_0x89);
    switch(tabela_unidades[uVar21].field_0x89) {
    case 0:
      if ((uint)tabela_unidades[uVar21].campo_0c <
          *(ushort *)&tabela_unidades[uVar21].field_0x70 + 1) {
        bVar19 = tabela_unidades[uVar21].tipo_id;
        tabela_unidades[uVar21].field_0x89 = 1;
      }
      else {
        if (tabela_unidades[uVar21].celula_destino != tabela_unidades[uVar21].celula_atual)
        goto LAB_0044bd11;
        lVar23 = FUN_004762b9(uVar16,(uint)tabela_unidades[uVar21].celula_atual);
        if ((char)lVar23 == '\0') {
          pUVar11 = (UnidadeParcial *)FUN_00477ead((in_EAX & 0xffff) << 4,5);
          iVar14 = (extraout_ECX_34 * 4 + (in_EAX & 0xffff) * 5) * 4;
          if (((uint)pUVar11 & 0xffff) == 0xffff) {
            pbVar17 = &tabela_unidades->proprietario_id + iVar14;
            if (*pbVar17 == DAT_00508041) {
              uVar13 = FUN_004766f0(pbVar17,(uint)DAT_00508041);
              pbVar17 = extraout_ECX_35;
              if ((char)uVar13 != '\0') {
                FUN_00440c5d(extraout_ECX_35,extraout_EDX_06);
                extraout_ECX_36[0xf9] = '\0';
                pbVar17 = extraout_ECX_36;
                if (*(int *)(extraout_ECX_36 + 0x104) == -1) {
                  FUN_0048aa79(0,(uint)extraout_ECX_36[1] << 0x10 | 0x1000,0x100);
                  pbVar17 = extraout_ECX_37;
                }
              }
            }
            pUVar11 = (UnidadeParcial *)(uint)(byte)pUVar5[uVar21].field_0x82;
            if (pUVar11 == (UnidadeParcial *)0x2) {
              FUN_00423b27(pbVar17,0);
            }
            else if (pUVar11 != (UnidadeParcial *)0x1) goto switchD_0044d86e_default;
            pUVar11 = (UnidadeParcial *)FUN_004457d3();
            goto switchD_0044d86e_default;
          }
          pUVar10 = (UnidadeParcial *)(&tabela_unidades->proprietario_id + iVar14);
          pUVar10->celula_destino = (ushort)pUVar11;
          if (sVar22 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
          }
LAB_0044cebb:
          pUVar10->estado_caminho = 0;
          *(short *)&pUVar5[uVar21].field_0xb2 = (short)pUVar11;
          goto switchD_0044d86e_default;
        }
        bVar19 = pUVar5[uVar21].tipo_id;
        pUVar5[uVar21].field_0x89 = 1;
      }
LAB_0044d8f7:
      uVar16 = FUN_00428cc0((uint)bVar19 * 0x19,3);
      cVar7 = (&DAT_004965de)[extraout_ECX_33 * 2];
      uVar15 = (undefined3)(uVar16 >> 8);
      pUVar5[uVar21].quadro_movimento = 0;
LAB_0044d90c:
      pUVar11 = (UnidadeParcial *)CONCAT31(uVar15,cVar7 - (char)uVar16);
      goto LAB_0044d549;
    case 1:
      bVar4 = *(ushort *)&tabela_unidades[uVar21].field_0x70 + 1 <=
              (uint)tabela_unidades[uVar21].campo_0c;
      pUVar11 = (UnidadeParcial *)
                (uint)CONCAT11((char)(tabela_unidades[uVar21].campo_0c >> 8),bVar4);
      if (bVar4) {
        FUN_00447f58(uVar16,&tabela_unidades[uVar21].campo_0a);
        bVar19 = pUVar5[uVar21].field_0x8b - 1;
        pUVar11 = (UnidadeParcial *)(uint)bVar19;
        pUVar5[uVar21].field_0x8b = bVar19;
        uVar16 = extraout_ECX_38;
        if (bVar19 == 0) {
          FUN_004781e8();
          uVar9 = *extraout_ECX_39;
          extraout_ECX_39[0x33] = extraout_ECX_39[0x33] + 1;
          *(undefined1 *)((int)extraout_ECX_39 + uVar9 + 0x42) = 2;
          extraout_ECX_39[uVar9 + 3] = 1;
          *extraout_ECX_39 = *extraout_ECX_39 + 1;
          if ((extraout_ECX_39[0x33] + 1 <= (uint)extraout_ECX_39[1]) &&
             (uVar16 = FUN_00428cc0((uint)extraout_ECX_39,7), (short)uVar16 != 0)) {
            puVar1 = &pUVar5[uVar21].campo_0a;
            *(short *)&pUVar5[uVar21].field_0x70 = *(short *)&pUVar5[uVar21].field_0x70 + 1;
            uVar9 = *puVar1;
            (&pUVar5[uVar21].field_0x4c)[uVar9] = 2;
            *(undefined2 *)(&pUVar5[uVar21].field_0x10 + (uint)uVar9 * 2) = 1;
            *puVar1 = *puVar1 + 1;
          }
          uVar25 = FUN_004704dc((uint)pUVar5[uVar21].celula_atual,0);
          FUN_004704dc(extraout_ECX_40 + (int)(uVar25 % 5),0);
          uVar9 = FUN_004781cc(extraout_ECX_41 + -2,5);
          pUVar11 = (UnidadeParcial *)(uint)uVar9;
          uVar16 = extraout_ECX_42;
          if ((pUVar11 == (UnidadeParcial *)0xffff) ||
             (uVar12 = *(ushort *)&pUVar5[uVar21].field_0x70 + 1,
             bVar4 = uVar12 <= pUVar5[uVar21].campo_0c,
             pUVar11 = (UnidadeParcial *)CONCAT31((int3)(uVar12 >> 8),bVar4), !bVar4))
          goto LAB_0044dc0c;
          uVar12 = in_EAX & 0xffff;
          pUVar5[uVar21].quadro_movimento = 0;
          pUVar10 = tabela_unidades;
          uVar16 = uVar12 * 0x114;
          tabela_unidades[uVar12].celula_destino = uVar9;
          if (sVar22 == DAT_00496304) {
            pUVar11 = (UnidadeParcial *)0xffff;
            uVar16 = uVar16 & 0xffffff00;
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
          }
          pUVar10[uVar12].estado_caminho = 0;
          pUVar5[uVar21].field_0x89 = 0;
          *(ushort *)&pUVar5[uVar21].field_0xb2 = uVar9;
        }
      }
      else {
LAB_0044dc0c:
        bVar3 = true;
      }
      pUVar10 = tabela_unidades;
      if (!bVar3) goto switchD_0044d86e_default;
      if (pUVar5[uVar21].field_0x82 == '\x02') {
        *(undefined2 *)&pUVar5[uVar21].field_0xc0 = *(undefined2 *)&pUVar5[uVar21].field_0x80;
        pUVar10 = tabela_unidades;
        if (*(short *)&pUVar5[uVar21].field_0xc0 == -1) {
          if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
             (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
            pUVar11 = (UnidadeParcial *)0x0;
          }
          else {
            pUVar11 = (UnidadeParcial *)0x1;
          }
          if ((char)pUVar11 != '\0') {
            tabela_unidades[in_EAX & 0xffff].estado = 7;
            pUVar11 = pUVar10;
            if (sVar22 == DAT_00496304) {
              DAT_004e0f37 = bVar6 ^ (byte)DAT_00496304;
              DAT_004e0f36 = 0;
              DAT_00496304 = -1;
              DAT_004e0f3c = 0;
              pUVar11 = (UnidadeParcial *)
                        CONCAT22((short)((uint)pUVar10 >> 0x10),(ushort)(byte)pUVar10);
            }
          }
          goto switchD_0044d86e_default;
        }
        uVar9 = FUN_0041aee2();
        pUVar5[uVar21].field_0x89 = 2;
        pUVar10 = tabela_unidades + (in_EAX & 0xffff);
        pUVar10->celula_destino = uVar9;
        goto joined_r0x0044dc80;
      }
      if (pUVar5[uVar21].field_0x82 != '\x01') {
        if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
           (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
          pUVar11 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar11 = (UnidadeParcial *)0x1;
        }
        if ((char)pUVar11 != '\0') {
          tabela_unidades[in_EAX & 0xffff].estado = 7;
          pUVar11 = pUVar10;
          if (sVar22 == DAT_00496304) {
            DAT_004e0f37 = bVar6 ^ (byte)DAT_00496304;
            DAT_004e0f36 = 0;
            pUVar11 = (UnidadeParcial *)0x0;
            DAT_00496304 = -1;
            DAT_004e0f3c = 0;
          }
        }
        goto switchD_0044d86e_default;
      }
      uVar9 = *(ushort *)&pUVar5[uVar21].field_0x80;
      uVar13 = FUN_00475763(uVar16,'C');
      if ((char)uVar13 == '\0') {
        uVar9 = FUN_0047790d(0x43,10);
        if (uVar9 == 0xffff) {
          uVar9 = FUN_0047790d(0,10);
        }
        *(ushort *)&pUVar5[uVar21].field_0x80 = uVar9;
      }
      pUVar10 = tabela_unidades;
      local_4c = (UnidadeParcial *)(uint)uVar9;
      if (local_4c == (UnidadeParcial *)0xffff) {
        if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
           (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
          pUVar11 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar11 = (UnidadeParcial *)0x1;
        }
        if ((char)pUVar11 == '\0') goto switchD_0044d86e_default;
        tabela_unidades[in_EAX & 0xffff].estado = 7;
        goto joined_r0x0044de59;
      }
      pUVar5[uVar21].field_0x89 = 2;
      pUVar10 = tabela_unidades + (in_EAX & 0xffff);
      pUVar10->celula_destino = uVar9;
      if (sVar22 == DAT_00496304) goto LAB_0044d224;
      break;
    case 2:
      if (tabela_unidades[uVar21].field_0x82 == '\x02') {
        if (((*(int *)&tabela_unidades[uVar21].field_0x83 >> 0x18 == 0) &&
            (*(int *)&tabela_unidades[uVar21].field_0x84 >> 0x18 == 0)) &&
           (iVar14 = FUN_0042381f(uVar16,(uint)tabela_unidades[uVar21].celula_atual),
           (char)iVar14 != '\0')) {
          pUVar5[uVar21].field_0x89 = 3;
          uVar9 = *(ushort *)(&DAT_004965de + (uint)pUVar5[uVar21].tipo_id * 0x32);
          uVar16 = 5;
LAB_0044d542:
          pUVar11 = (UnidadeParcial *)(uVar9 / uVar16);
          goto LAB_0044d549;
        }
        if (pUVar5[uVar21].celula_atual == pUVar5[uVar21].celula_destino) {
          uVar9 = FUN_0041aee2();
          local_4c = (UnidadeParcial *)(in_EAX & 0xffff);
          pUVar10 = tabela_unidades + (int)local_4c;
          pUVar10->celula_destino = uVar9;
          if (sVar22 != DAT_00496304) break;
          local_4c = (UnidadeParcial *)(in_EAX & 0xff00);
LAB_0044c8ad:
          DAT_004e0f36 = 0;
          DAT_004e0f3c = 0;
          DAT_00496304 = -1;
          DAT_004e0f37 = DAT_004e0f36;
          break;
        }
      }
      else {
        pUVar11 = (UnidadeParcial *)(uint)(byte)tabela_unidades[uVar21].field_0x82;
        if ((UnidadeParcial *)(uint)(byte)tabela_unidades[uVar21].field_0x82 !=
            (UnidadeParcial *)0x1) goto switchD_0044d86e_default;
        if (tabela_unidades[uVar21].celula_atual == tabela_unidades[uVar21].celula_destino) {
          uVar16 = FUN_00479555(*(ushort *)&tabela_unidades[uVar21].field_0x80 >> 8,
                                tabela_unidades[uVar21].celula_atual >> 8);
          if (uVar16 < 0x10) {
            uVar13 = FUN_00475763(extraout_ECX_43,pUVar5[uVar21].field_0x84 + 'B');
            if ((char)uVar13 != '\0') {
              *(ushort *)&pUVar5[uVar21].field_0x80 = pUVar5[uVar21].celula_atual;
              iVar14 = (uint)pUVar5[uVar21].tipo_id * 0x19;
              pUVar5[uVar21].field_0x89 = 3;
              goto LAB_0044d533;
            }
            pUVar11 = (UnidadeParcial *)
                      FUN_004757af(extraout_ECX_44,pUVar5[uVar21].field_0x84 + 'B');
            if (((uint)pUVar11 & 0xffff) == 0xffff) goto switchD_0044d86e_default;
            pUVar10 = tabela_unidades + (in_EAX & 0xffff);
            pUVar10->celula_destino = (ushort)pUVar11;
joined_r0x0044e10a:
            local_4c = (UnidadeParcial *)(in_EAX & 0xffff);
            if (sVar22 == DAT_00496304) {
              DAT_004e0f37 = 0;
              DAT_004e0f36 = 0;
              DAT_00496304 = -1;
              local_4c = (UnidadeParcial *)(in_EAX & 0xffff);
              DAT_004e0f3c = 0;
            }
          }
          else {
            pUVar10 = tabela_unidades + (in_EAX & 0xffff);
            local_4c = (UnidadeParcial *)
                       CONCAT22((short)(uVar16 >> 0x10),*(ushort *)&pUVar5[uVar21].field_0x80);
            pUVar10->celula_destino = *(ushort *)&pUVar5[uVar21].field_0x80;
joined_r0x0044e15f:
            if (sVar22 == DAT_00496304) {
              DAT_004e0f37 = 0;
              DAT_004e0f36 = 0;
              DAT_00496304 = -1;
              DAT_004e0f3c = 0;
            }
          }
          break;
        }
      }
      goto LAB_0044bd11;
    case 3:
      bVar19 = tabela_unidades[uVar21].field_0x8b - 1;
      tabela_unidades[uVar21].field_0x8b = bVar19;
      pUVar11 = (UnidadeParcial *)(uint)bVar19;
      if (bVar19 != 0) goto switchD_0044d86e_default;
      uVar16 = FUN_004471b8(uVar16,'\x02');
      pUVar10 = tabela_unidades;
      if ((uVar16 & 0xffff) != 0) {
        if (pUVar5[uVar21].field_0x82 == '\x02') {
          FUN_0042340f((uint)*(ushort *)&pUVar5[uVar21].field_0x80,1);
          pUVar11 = (UnidadeParcial *)FUN_004472ea(extraout_ECX_46,'\x02');
          goto LAB_0044c175;
        }
        pUVar11 = (UnidadeParcial *)(uint)(byte)pUVar5[uVar21].field_0x82;
        if ((UnidadeParcial *)(uint)(byte)pUVar5[uVar21].field_0x82 != (UnidadeParcial *)0x1)
        goto switchD_0044d86e_default;
        FUN_004438d8(extraout_ECX_45,2);
        iVar14 = (uint)pUVar5[uVar21].tipo_id * 0x19;
LAB_0044d533:
        uVar9 = *(ushort *)(&DAT_004965de + iVar14 * 2);
        uVar16 = 10;
        goto LAB_0044d542;
      }
      if (*(short *)&pUVar5[uVar21].field_0xb2 == -1) {
        if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
           (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
          pUVar11 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar11 = (UnidadeParcial *)0x1;
        }
        if ((char)pUVar11 != '\0') {
          tabela_unidades[in_EAX & 0xffff].estado = 7;
          pUVar11 = pUVar10;
          if (sVar22 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
            pUVar11 = (UnidadeParcial *)0x0;
          }
        }
        goto switchD_0044d86e_default;
      }
      pUVar5[uVar21].field_0x89 = 0;
      pUVar10 = tabela_unidades + (in_EAX & 0xffff);
      uVar9 = *(ushort *)&pUVar5[uVar21].field_0xb2;
      local_4c = (UnidadeParcial *)(uint)uVar9;
      pUVar10->celula_destino = uVar9;
      if (sVar22 == DAT_00496304) {
        local_4c = (UnidadeParcial *)((uint)(byte)(uVar9 >> 8) << 8);
        goto LAB_0044c8ad;
      }
      break;
    default:
      goto switchD_0044d86e_default;
    }
LAB_0044c8b4:
    pUVar10->estado_caminho = 0;
    pUVar11 = local_4c;
    goto switchD_0044d86e_default;
  }
  if (bVar19 < 7) {
    bVar19 = tabela_unidades[uVar21].field_0x89;
    pUVar11 = (UnidadeParcial *)CONCAT31(uVar15,bVar19);
    if (bVar19 == 0) goto switchD_0044d86e_default;
    if (1 < bVar19) {
      if (bVar19 == 2) {
        FUN_0044930c();
        pUVar10 = tabela_unidades;
        pUVar11 = (UnidadeParcial *)CONCAT22(extraout_var,pUVar5[uVar21].celula_destino);
        if (pUVar5[uVar21].celula_destino == pUVar5[uVar21].celula_atual) {
          if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
             (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
            pUVar11 = (UnidadeParcial *)0x0;
          }
          else {
            pUVar11 = (UnidadeParcial *)0x1;
          }
          if ((char)pUVar11 != '\0') {
            tabela_unidades[in_EAX & 0xffff].estado = 7;
            pUVar11 = pUVar10;
            if (sVar22 == DAT_00496304) {
              pUVar11 = (UnidadeParcial *)((uint)pUVar10 & 0xffffff00);
              DAT_004e0f36 = 0;
              DAT_004e0f37 = 0;
              DAT_004e0f3c = 0;
              DAT_00496304 = -1;
            }
          }
          *(undefined2 *)&pUVar5[uVar21].field_0x4 = 0;
          *(undefined2 *)&pUVar5[uVar21].field_0xb2 = 0xffff;
        }
      }
      goto switchD_0044d86e_default;
    }
    FUN_0044930c();
    lVar23 = FUN_0047610f(extraout_ECX_18,extraout_EDX_03);
    pUVar11 = (UnidadeParcial *)lVar23;
    if ((char)lVar23 == '\0') goto switchD_0044d86e_default;
    FUN_00476662(&pUVar5[uVar21].campo_0a,(int)((ulonglong)lVar23 >> 0x20));
    extraout_ECX_19[0x33] = extraout_ECX_19[0x33] + 1;
    uVar9 = *extraout_ECX_19;
    *(undefined1 *)((int)extraout_ECX_19 + uVar9 + 0x42) = 2;
    extraout_ECX_19[uVar9 + 3] = 0;
    *extraout_ECX_19 = *extraout_ECX_19 + 1;
    pUVar10 = tabela_unidades;
    if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
       (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
      pUVar11 = (UnidadeParcial *)0x0;
    }
    else {
      pUVar11 = (UnidadeParcial *)0x1;
    }
    if ((char)pUVar11 == '\0') goto switchD_0044d86e_default;
    tabela_unidades[in_EAX & 0xffff].estado = 7;
    pUVar11 = pUVar10;
    if (sVar22 != DAT_00496304) goto switchD_0044d86e_default;
    DAT_004e0f37 = bVar6 ^ (byte)DAT_00496304;
LAB_0044c0d7:
    DAT_004e0f3c = 0;
    DAT_004e0f36 = 0;
    DAT_00496304 = -1;
    pUVar11 = pUVar10;
    goto switchD_0044d86e_default;
  }
  uVar18 = (undefined2)(uVar16 >> 0x10);
  if (bVar19 < 8) {
    pUVar11 = (UnidadeParcial *)CONCAT31(uVar15,tabela_unidades[uVar21].field_0x89);
    switch(tabela_unidades[uVar21].field_0x89) {
    case 0:
      pUVar11 = tabela_unidades + uVar21;
      if ((uint)tabela_unidades[uVar21].campo_0c <
          *(ushort *)&tabela_unidades[uVar21].field_0x70 + 1) {
        bVar19 = tabela_unidades[uVar21].field_0x82;
        if (bVar19 == 0) {
          pUVar11 = (UnidadeParcial *)0x0;
          goto switchD_0044d86e_default;
        }
        if (bVar19 != 0) {
          if (bVar19 < 2) {
            local_4c = (UnidadeParcial *)(uint)*(ushort *)&tabela_unidades[uVar21].field_0x80;
            uVar13 = FUN_00475763(uVar16,'\x02');
            if ((char)uVar13 == '\0') {
              local_4c = (UnidadeParcial *)FUN_0047790d(0x44,10);
              if (((uint)local_4c & 0xffff) == 0xffff) {
                local_4c = (UnidadeParcial *)FUN_0047790d(0,10);
              }
              *(short *)&pUVar5[uVar21].field_0x80 = (short)local_4c;
            }
          }
          else if (bVar19 == 2) {
            *(undefined2 *)&tabela_unidades[uVar21].field_0xc0 =
                 *(undefined2 *)&tabela_unidades[uVar21].field_0x80;
            uVar24 = FUN_00423b27(uVar16,&pUVar11->campo_0a);
            local_4c = (UnidadeParcial *)uVar24;
          }
        }
        pUVar10 = tabela_unidades;
        if ((ushort)local_4c != 0xffff) {
          pUVar5[uVar21].field_0x89 = 3;
          pUVar10 = tabela_unidades + (in_EAX & 0xffff);
          pUVar10->celula_destino = (ushort)local_4c;
          if (sVar22 == DAT_00496304) {
            local_4c = (UnidadeParcial *)
                       CONCAT22((short)((uint)local_4c >> 0x10),(ushort)(byte)local_4c);
            break;
          }
          goto LAB_0044c8b4;
        }
        if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
           (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
          pUVar11 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar11 = (UnidadeParcial *)0x1;
        }
        if ((char)pUVar11 == '\0') goto switchD_0044d86e_default;
        tabela_unidades[in_EAX & 0xffff].estado = 7;
        pUVar11 = pUVar10;
        if (sVar22 != DAT_00496304) goto switchD_0044d86e_default;
        DAT_004e0f37 = 0;
        goto LAB_0044c0d7;
      }
      uVar9 = tabela_unidades[uVar21].celula_atual;
      if (tabela_unidades[uVar21].celula_destino != uVar9) goto LAB_0044bd11;
      uVar2 = *(ushort *)&tabela_unidades[uVar21].field_0xb2;
      local_4c = (UnidadeParcial *)CONCAT22((short)((uint)&pUVar11->campo_0a >> 0x10),uVar2);
      if (uVar9 != uVar2) {
        pUVar10 = tabela_unidades + (in_EAX & 0xffff);
        pUVar10->celula_destino = uVar2;
        goto joined_r0x0044c6e6;
      }
      lVar23 = FUN_00475402(CONCAT22(uVar18,uVar9),local_4c);
      if ((char)lVar23 == '\0') {
        pUVar11 = (UnidadeParcial *)lVar23;
        if (((byte)DAT_00508f7c & 0x1f) != 0) goto switchD_0044d86e_default;
        bVar19 = tabela_unidades[in_EAX & 0xffff].proprietario_id;
        uVar16 = CONCAT22((short)((uint)tabela_unidades >> 0x10),CONCAT11(DAT_00508041,bVar19));
        if ((bVar19 == DAT_00508041) &&
           (uVar16 = FUN_004766f0(tabela_unidades + (in_EAX & 0xffff),(uint)DAT_00508041),
           (char)uVar16 != '\0')) {
          FUN_00440c5d(extraout_ECX_01,extraout_EDX);
          uVar16 = *(uint *)(extraout_ECX_02 + 0x104);
          *(undefined1 *)(extraout_ECX_02 + 0xf9) = 0;
          if (uVar16 == 0xffffffff) {
            uVar16 = FUN_0048aa79(0,(uint)*(byte *)(extraout_ECX_02 + 1) << 0x10 | 0x1000,0x100);
          }
        }
        bVar19 = pUVar5[uVar21].field_0x82;
        pUVar11 = (UnidadeParcial *)CONCAT31((int3)(uVar16 >> 8),bVar19);
        if (bVar19 == 0) goto switchD_0044d86e_default;
        if (bVar19 < 2) {
          pUVar10 = tabela_unidades + (in_EAX & 0xffff);
          pUVar10->celula_destino = *(ushort *)&pUVar5[uVar21].field_0x80;
          goto joined_r0x0044e10a;
        }
        if (bVar19 != 2) goto switchD_0044d86e_default;
        uVar24 = FUN_0041aee2();
        local_4c = (UnidadeParcial *)uVar24;
        pUVar10 = (UnidadeParcial *)
                  (&tabela_unidades->proprietario_id +
                  (extraout_ECX_03 + (int)((ulonglong)uVar24 >> 0x20)) * 4);
        pUVar10->celula_destino = (ushort)uVar24;
        goto joined_r0x0044e15f;
      }
      FUN_004754a7(extraout_ECX,(int)((ulonglong)lVar23 >> 0x20));
      FUN_00457058();
      pUVar5[uVar21].field_0x89 = 1;
      uVar16 = FUN_00428cc0((uint)pUVar5[uVar21].tipo_id * 0x19,3);
      cVar7 = (&DAT_004965de)[extraout_ECX_00 * 2];
      uVar15 = (undefined3)(uVar16 >> 8);
      goto LAB_0044d90c;
    case 1:
      FUN_00447f58(uVar16,param_2);
      bVar19 = pUVar5[uVar21].field_0x8b - 1;
      pUVar11 = (UnidadeParcial *)(uint)bVar19;
      pUVar5[uVar21].field_0x8b = bVar19;
      if (bVar19 != 0) goto switchD_0044d86e_default;
      bVar3 = *(ushort *)&pUVar5[uVar21].field_0x70 + 1 <= (uint)pUVar5[uVar21].campo_0c;
      if (!bVar3) {
        pUVar5[uVar21].field_0x89 = 2;
        pUVar11 = (UnidadeParcial *)(uint)CONCAT11((char)(pUVar5[uVar21].campo_0c >> 8),bVar3);
        goto switchD_0044d86e_default;
      }
      lVar23 = FUN_004755a7(CONCAT31((int3)((uint)extraout_ECX_04 >> 8),bVar19),
                            (uint)&pUVar5[uVar21].campo_0a);
      if ((short)lVar23 != 0) {
        puVar1 = &pUVar5[uVar21].campo_0a;
        *(short *)&pUVar5[uVar21].field_0x70 = *(short *)&pUVar5[uVar21].field_0x70 + 1;
        pUVar11 = (UnidadeParcial *)(uint)*puVar1;
        (&pUVar5[uVar21].field_0x4c)[(int)pUVar11] = 2;
        *(undefined2 *)(&pUVar5[uVar21].field_0x10 + (int)pUVar11 * 2) = 2;
        *puVar1 = *puVar1 + 1;
        goto LAB_0044c175;
      }
      FUN_004754de(extraout_ECX_05,(int)((ulonglong)lVar23 >> 0x20));
      pUVar11 = tabela_unidades;
      FUN_00442cb4((in_EAX & 0xffff) * 0x114);
      (&pUVar11->field_0x72)[extraout_ECX_06] = 1;
      pbVar17 = &tabela_unidades->proprietario_id + extraout_ECX_06;
      if ((*pbVar17 != 200) && (*pbVar17 != 4)) {
        FUN_00476851(pbVar17,(uint)(ushort)((ushort)pbVar17[0xf5] + pbVar17[0xbb] + 2));
        FUN_00476cb3(extraout_ECX_07,
                     (uint)(ushort)((ushort)*(byte *)(extraout_ECX_07 + 0xf5) +
                                   (ushort)*(byte *)(extraout_ECX_07 + 0xbb)));
        pbVar17 = extraout_ECX_08;
      }
      FUN_0046a388(pbVar17,4);
      pUVar11 = tabela_unidades;
      tabela_unidades[in_EAX & 0xffff].celula_destino = pUVar5[uVar21].celula_atual;
      if (sVar22 == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = -1;
      }
      pUVar11[in_EAX & 0xffff].estado_caminho = 0;
      pUVar10 = tabela_unidades;
      if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
         (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
        pUVar11 = (UnidadeParcial *)0x0;
      }
      else {
        pUVar11 = (UnidadeParcial *)0x1;
      }
      if ((char)pUVar11 == '\0') goto switchD_0044d86e_default;
      tabela_unidades[in_EAX & 0xffff].estado = 7;
joined_r0x0044de59:
      pUVar11 = pUVar10;
      if (sVar22 == DAT_00496304) {
        DAT_004e0f3c = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f36 = 0;
        DAT_00496304 = -1;
      }
      goto switchD_0044d86e_default;
    case 2:
      pUVar11 = (UnidadeParcial *)FUN_00442668(0,tabela_unidades[uVar21].celula_atual);
      if ((char)pUVar11 == '\0') goto switchD_0044d86e_default;
      FUN_004754de(extraout_ECX_09,extraout_EDX_00);
      pUVar11 = tabela_unidades;
      FUN_00442cb4((in_EAX & 0xffff) * 0x45);
      (&pUVar11->field_0x72)[extraout_ECX_10 * 4] = 1;
      pUVar11 = tabela_unidades + (in_EAX & 0xffff);
      if ((pUVar11->proprietario_id != 200) && (pUVar11->proprietario_id != 4)) {
        FUN_00476851(pUVar11,(uint)(ushort)(pUVar11->raio_visao + 2 +
                                           (ushort)(byte)pUVar11->field_0xf5));
        FUN_00476cb3(extraout_ECX_11,
                     (uint)(ushort)((ushort)*(byte *)(extraout_ECX_11 + 0xf5) +
                                   (ushort)*(byte *)(extraout_ECX_11 + 0xbb)));
        pUVar11 = extraout_ECX_12;
      }
      FUN_0046a388(pUVar11,4);
      pUVar10 = tabela_unidades;
      bVar19 = pUVar5[uVar21].field_0x82;
      if (bVar19 == 0) {
        if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
           (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
          pUVar11 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar11 = (UnidadeParcial *)0x1;
        }
        if ((char)pUVar11 != '\0') {
          tabela_unidades[in_EAX & 0xffff].estado = 7;
          pUVar11 = pUVar10;
          if (sVar22 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
            pUVar11 = (UnidadeParcial *)((uint)pUVar10 & 0xffffff00);
          }
        }
        goto switchD_0044d86e_default;
      }
      if (bVar19 != 0) {
        if (bVar19 < 2) {
          local_4c = (UnidadeParcial *)(uint)*(ushort *)&pUVar5[uVar21].field_0x80;
          uVar13 = FUN_00475763(extraout_ECX_13,'\x02');
          if ((char)uVar13 == '\0') {
            local_4c = (UnidadeParcial *)FUN_0047790d(0x44,10);
            if (((uint)local_4c & 0xffff) == 0xffff) {
              local_4c = (UnidadeParcial *)FUN_0047790d(0,10);
            }
            *(short *)&pUVar5[uVar21].field_0x80 = (short)local_4c;
          }
        }
        else if (bVar19 == 2) {
          *(undefined2 *)&pUVar5[uVar21].field_0xc0 = *(undefined2 *)&pUVar5[uVar21].field_0x80;
          uVar24 = FUN_00423b27(extraout_ECX_13,extraout_EDX_01);
          local_4c = (UnidadeParcial *)uVar24;
        }
      }
      pUVar10 = tabela_unidades;
      local_4c = (UnidadeParcial *)((uint)local_4c & 0xffff);
      if (local_4c == (UnidadeParcial *)0xffff) {
        if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
           (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
          pUVar11 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar11 = (UnidadeParcial *)0x1;
        }
        if ((char)pUVar11 == '\0') goto switchD_0044d86e_default;
        tabela_unidades[in_EAX & 0xffff].estado = 7;
        goto joined_r0x0044de59;
      }
      pUVar5[uVar21].field_0x89 = 3;
      pUVar10 = tabela_unidades + (in_EAX & 0xffff);
LAB_0044c554:
      pUVar10->celula_destino = (ushort)local_4c;
      if (sVar22 != DAT_00496304) goto LAB_0044c8b4;
      local_4c = (UnidadeParcial *)0x0;
      break;
    case 3:
      if (tabela_unidades[uVar21].field_0x82 == '\x02') {
        if (((*(int *)&tabela_unidades[uVar21].field_0x83 >> 0x18 == 0) &&
            (*(int *)&tabela_unidades[uVar21].field_0x84 >> 0x18 == 0)) &&
           (pUVar11 = (UnidadeParcial *)
                      FUN_0042381f(uVar16,(uint)tabela_unidades[uVar21].celula_atual),
           (char)pUVar11 != '\0')) {
          pUVar5[uVar21].field_0x89 = 4;
LAB_0044c175:
          pUVar5[uVar21].field_0x8b = 0x32;
          goto switchD_0044d86e_default;
        }
        if (pUVar5[uVar21].celula_atual == pUVar5[uVar21].celula_destino) {
          uVar9 = FUN_0041aee2();
          local_4c = (UnidadeParcial *)(in_EAX & 0xffff);
          pUVar10 = tabela_unidades + (int)local_4c;
          pUVar10->celula_destino = uVar9;
joined_r0x0044c6e6:
          if (sVar22 == DAT_00496304) goto LAB_0044c8ad;
          goto LAB_0044c8b4;
        }
      }
      else {
        pUVar11 = (UnidadeParcial *)(uint)(byte)tabela_unidades[uVar21].field_0x82;
        if ((UnidadeParcial *)(uint)(byte)tabela_unidades[uVar21].field_0x82 !=
            (UnidadeParcial *)0x1) goto switchD_0044d86e_default;
        if (tabela_unidades[uVar21].celula_atual == tabela_unidades[uVar21].celula_destino) {
          uVar16 = FUN_00479555(*(ushort *)&tabela_unidades[uVar21].field_0x80 >> 8,
                                tabela_unidades[uVar21].celula_atual >> 8);
          if (0xf < uVar16) {
            local_4c = (UnidadeParcial *)(in_EAX & 0xffff);
            pUVar10 = tabela_unidades + (int)local_4c;
            pUVar10->celula_destino = *(ushort *)&pUVar5[uVar21].field_0x80;
            goto joined_r0x0044c6e6;
          }
          uVar13 = FUN_00475763(extraout_ECX_14,pUVar5[uVar21].field_0x84 + 'B');
          if ((char)uVar13 != '\0') {
            pUVar5[uVar21].field_0x89 = 4;
            pUVar5[uVar21].field_0x8b = 10;
            *(ushort *)&pUVar5[uVar21].field_0x80 = pUVar5[uVar21].celula_atual;
            pUVar11 = (UnidadeParcial *)
                      CONCAT22((short)((uint)uVar13 >> 0x10),pUVar5[uVar21].celula_atual);
            goto switchD_0044d86e_default;
          }
          pUVar11 = (UnidadeParcial *)FUN_004757af(extraout_ECX_15,pUVar5[uVar21].field_0x84 + 'B');
          if (((uint)pUVar11 & 0xffff) == 0xffff) goto switchD_0044d86e_default;
          local_4c = (UnidadeParcial *)(in_EAX & 0xffff);
          pUVar10 = tabela_unidades + (int)local_4c;
          pUVar10->celula_destino = (ushort)pUVar11;
          if (sVar22 != DAT_00496304) goto LAB_0044c8b4;
          local_4c = (UnidadeParcial *)(in_EAX & 0xff);
          goto LAB_0044c859;
        }
      }
      goto LAB_0044bd11;
    case 4:
      if (tabela_unidades[uVar21].field_0x82 == '\x02') {
        bVar19 = tabela_unidades[uVar21].field_0x8b - 1;
        tabela_unidades[uVar21].field_0x8b = bVar19;
        pUVar11 = (UnidadeParcial *)(uint)bVar19;
        if (bVar19 != 0) goto switchD_0044d86e_default;
        pUVar11 = (UnidadeParcial *)FUN_004471b8(CONCAT31((int3)(uVar16 >> 8),bVar19),'\x02');
        if ((short)pUVar11 != 0) {
          FUN_004472ea(0,'\x02');
          uVar18 = extraout_var_00;
          goto LAB_0044c91c;
        }
      }
      else {
        pUVar11 = (UnidadeParcial *)(uint)(byte)tabela_unidades[uVar21].field_0x82;
        if ((UnidadeParcial *)(uint)(byte)tabela_unidades[uVar21].field_0x82 !=
            (UnidadeParcial *)0x1) goto switchD_0044d86e_default;
        bVar19 = tabela_unidades[uVar21].field_0x8b - 1;
        tabela_unidades[uVar21].field_0x8b = bVar19;
        pUVar11 = (UnidadeParcial *)(uint)bVar19;
        if (bVar19 != 0) goto switchD_0044d86e_default;
        pUVar11 = (UnidadeParcial *)FUN_004471b8(uVar16,'\x02');
        if ((short)pUVar11 != 0) {
          pUVar11 = (UnidadeParcial *)FUN_004438d8(extraout_ECX_16,2);
          pUVar5[uVar21].field_0x8b = 10;
          goto switchD_0044d86e_default;
        }
      }
      pUVar5[uVar21].field_0x89 = 5;
      goto switchD_0044d86e_default;
    case 5:
      if (tabela_unidades[uVar21].field_0x82 == '\x02') {
        pUVar11 = (UnidadeParcial *)FUN_00442668(0,tabela_unidades[uVar21].celula_atual);
        if ((char)pUVar11 == '\0') goto switchD_0044d86e_default;
        *(undefined2 *)&pUVar5[uVar21].field_0xc0 = 0xffff;
        if (*(short *)&pUVar5[uVar21].field_0xb2 != -1) {
          FUN_0047544c(extraout_ECX_17,extraout_EDX_02);
          sVar8 = FUN_00475541();
          if (sVar8 != 0) {
            pUVar5[uVar21].field_0x89 = 0;
            pUVar10 = tabela_unidades + (in_EAX & 0xffff);
            uVar9 = *(ushort *)&pUVar5[uVar21].field_0xb2;
            local_4c = (UnidadeParcial *)(uint)uVar9;
            pUVar10->celula_destino = uVar9;
            if (sVar22 == DAT_00496304) {
              local_4c = (UnidadeParcial *)(uint)(uVar9 & 0xff);
              goto LAB_0044c8ad;
            }
            goto LAB_0044c8b4;
          }
        }
        pUVar10 = tabela_unidades;
        if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
           (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
          pUVar11 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar11 = (UnidadeParcial *)0x1;
        }
        if ((char)pUVar11 != '\0') {
          tabela_unidades[in_EAX & 0xffff].estado = 7;
          pUVar11 = pUVar10;
          if (sVar22 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
            pUVar11 = (UnidadeParcial *)0xffff;
          }
        }
      }
      else {
        if (*(short *)&tabela_unidades[uVar21].field_0xb2 != -1) {
          tabela_unidades[uVar21].field_0x89 = 0;
          pUVar11 = tabela_unidades + (in_EAX & 0xffff);
          pUVar11->celula_destino = *(ushort *)&pUVar5[uVar21].field_0xb2;
          if (sVar22 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
          }
          goto LAB_0044cb71;
        }
        if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
           (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
          pUVar11 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar11 = (UnidadeParcial *)0x1;
        }
        if ((char)pUVar11 != '\0') {
          tabela_unidades[in_EAX & 0xffff].estado = 7;
          pUVar11 = pUVar5;
          if (sVar22 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_00496304 = -1;
            DAT_004e0f3c = 0;
          }
        }
      }
      pUVar5[uVar21].field_0x82 = 0;
    default:
      goto switchD_0044d86e_default;
    }
LAB_0044d224:
    DAT_004e0f3c = 0;
    DAT_004e0f37 = 0;
    DAT_004e0f36 = 0;
    DAT_00496304 = -1;
    goto LAB_0044c8b4;
  }
  if (bVar19 != 0xd) goto switchD_0044d86e_default;
  bVar19 = (byte)(in_EAX >> 8);
  pUVar11 = (UnidadeParcial *)CONCAT31(uVar15,tabela_unidades[uVar21].field_0x89);
  switch(tabela_unidades[uVar21].field_0x89) {
  case 0:
    if (tabela_unidades[uVar21].celula_destino == tabela_unidades[uVar21].celula_atual) {
      lVar23 = FUN_004762b9(CONCAT22(uVar18,tabela_unidades[uVar21].celula_atual),param_2);
      if ((char)lVar23 == '\0') {
        pUVar11 = (UnidadeParcial *)FUN_00477ead(extraout_ECX_20,5);
        if (((uint)pUVar11 & 0xffff) == 0xffff) {
          if ((tabela_unidades[in_EAX & 0xffff].proprietario_id == DAT_00508041) &&
             (uVar13 = FUN_004766f0(tabela_unidades + (in_EAX & 0xffff),(uint)DAT_00508041),
             (char)uVar13 != '\0')) {
            uVar24 = FUN_00440c5d(extraout_ECX_21,0x10);
            uVar16 = (uint)uVar24;
            if ((int)((ulonglong)uVar24 >> 0x20) == 0x10) {
              uVar16 = 0x100;
            }
            *(undefined1 *)(extraout_ECX_22 + 0xf9) = 0;
            if (*(int *)(extraout_ECX_22 + 0x104) == -1) {
              FUN_0048aa79(0,(uint)*(byte *)(extraout_ECX_22 + 1) << 0x10 | 0x1000,uVar16);
            }
          }
          pUVar5 = tabela_unidades;
          if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
             (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
            pUVar11 = (UnidadeParcial *)0x0;
          }
          else {
            pUVar11 = (UnidadeParcial *)0x1;
          }
          if ((char)pUVar11 != '\0') {
            tabela_unidades[in_EAX & 0xffff].estado = 7;
            pUVar11 = pUVar5;
            if (sVar22 == DAT_00496304) {
              DAT_004e0f36 = (byte)((in_EAX & 0xffff) >> 8) ^ bVar19;
              DAT_004e0f3c = 0;
              DAT_00496304 = -1;
              DAT_004e0f37 = 0;
              pUVar11 = (UnidadeParcial *)0x0;
            }
          }
          goto switchD_0044d86e_default;
        }
        pUVar10 = tabela_unidades + (in_EAX & 0xffff);
        pUVar10->celula_destino = (ushort)pUVar11;
        if (sVar22 == DAT_00496304) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_00496304 = -1;
          DAT_004e0f3c = 0;
        }
        goto LAB_0044cebb;
      }
      bVar19 = pUVar5[uVar21].tipo_id;
      pUVar5[uVar21].field_0x89 = 1;
      goto LAB_0044d8f7;
    }
    break;
  case 1:
    bVar4 = *(ushort *)&tabela_unidades[uVar21].field_0x70 + 1 <=
            (uint)tabela_unidades[uVar21].campo_0c;
    pUVar11 = (UnidadeParcial *)(uint)CONCAT11((char)(tabela_unidades[uVar21].campo_0c >> 8),bVar4);
    if (bVar4) {
      FUN_00447f58(uVar16,&tabela_unidades[uVar21].campo_0a);
      bVar19 = pUVar5[uVar21].field_0x8b - 1;
      uVar16 = CONCAT22((short)((uint)extraout_ECX_23 >> 0x10),
                        CONCAT11(bVar19,(char)extraout_ECX_23));
      pUVar11 = (UnidadeParcial *)(uint)bVar19;
      pUVar5[uVar21].field_0x8b = bVar19;
      if (pUVar11 == (UnidadeParcial *)0x0) {
        FUN_004781e8();
        extraout_ECX_24[0x33] = extraout_ECX_24[0x33] + 1;
        uVar9 = *extraout_ECX_24;
        *(undefined1 *)((int)extraout_ECX_24 + uVar9 + 0x42) = 2;
        extraout_ECX_24[uVar9 + 3] = 1;
        *extraout_ECX_24 = *extraout_ECX_24 + 1;
        FUN_004704dc(extraout_ECX_24,0);
        FUN_004704dc(extraout_ECX_25,0);
        uVar12 = FUN_00477ead(extraout_ECX_26,5);
        pUVar11 = (UnidadeParcial *)(uVar12 & 0xffff);
        uVar16 = extraout_ECX_27;
        if ((pUVar11 == (UnidadeParcial *)0xffff) ||
           (bVar4 = *(ushort *)(extraout_ECX_27 + 0x66) + 1 <=
                    (uint)*(ushort *)(extraout_ECX_27 + 2),
           pUVar11 = (UnidadeParcial *)
                     (uint)CONCAT11((char)(*(ushort *)(extraout_ECX_27 + 2) >> 8),bVar4), !bVar4))
        goto LAB_0044d182;
        uVar20 = in_EAX & 0xffff;
        pUVar5[uVar21].quadro_movimento = 0;
        pUVar10 = tabela_unidades;
        uVar16 = uVar20 * 0x114;
        tabela_unidades[uVar20].celula_destino = (ushort)uVar12;
        if (sVar22 == DAT_00496304) {
          uVar16 = 0;
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          pUVar11 = (UnidadeParcial *)0xffff;
          DAT_004e0f3c = 0;
          DAT_00496304 = -1;
        }
        pUVar10[uVar20].estado_caminho = 0;
        pUVar5[uVar21].field_0x89 = 0;
        *(ushort *)&pUVar5[uVar21].field_0xb2 = (ushort)uVar12;
      }
    }
    else {
LAB_0044d182:
      bVar3 = true;
    }
    if (!bVar3) goto switchD_0044d86e_default;
    if (pUVar5[uVar21].field_0x82 != '\x02') {
      if (pUVar5[uVar21].field_0x82 == '\x01') {
        uVar9 = *(ushort *)&pUVar5[uVar21].field_0x80;
        uVar13 = FUN_00475763(uVar16,'\x01');
        if ((char)uVar13 == '\0') {
          uVar9 = FUN_0047790d(0x43,10);
          if (uVar9 == 0xffff) {
            uVar9 = FUN_0047790d(0,10);
          }
          *(ushort *)&pUVar5[uVar21].field_0x80 = uVar9;
        }
        local_4c = (UnidadeParcial *)(uint)uVar9;
        if (local_4c == (UnidadeParcial *)0xffff) {
          if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
             (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
            bVar3 = false;
          }
          else {
            bVar3 = true;
          }
          if ((bVar3) && (tabela_unidades[in_EAX & 0xffff].estado = 7, sVar22 == DAT_00496304)) {
            DAT_004e0f36 = 0;
            DAT_004e0f3c = 0;
            DAT_004e0f37 = 0;
            DAT_00496304 = -1;
          }
          local_4c = (UnidadeParcial *)(in_EAX & 0xffff);
          pUVar10 = tabela_unidades + (int)local_4c;
          pUVar10->celula_destino = pUVar5[uVar21].celula_passo;
          if (sVar22 == DAT_00496304) {
            local_4c = (UnidadeParcial *)(in_EAX & 0xff);
            goto LAB_0044c8ad;
          }
        }
        else {
          pUVar5[uVar21].field_0x89 = 2;
          pUVar10 = tabela_unidades + (in_EAX & 0xffff);
          pUVar10->celula_destino = uVar9;
          if (sVar22 == DAT_00496304) goto LAB_0044c859;
        }
      }
      else {
        if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
           (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
          bVar3 = false;
        }
        else {
          bVar3 = true;
        }
        if ((bVar3) && (tabela_unidades[in_EAX & 0xffff].estado = 7, sVar22 == DAT_00496304)) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_004e0f3c = 0;
          DAT_00496304 = -1;
        }
        local_4c = (UnidadeParcial *)(in_EAX & 0xffff);
        pUVar10 = tabela_unidades + (int)local_4c;
        pUVar10->celula_destino = pUVar5[uVar21].celula_passo;
        if (sVar22 == DAT_00496304) {
          local_4c = (UnidadeParcial *)0x0;
LAB_0044c859:
          DAT_004e0f3c = 0;
          DAT_004e0f37 = 0;
          DAT_004e0f36 = 0;
          DAT_00496304 = -1;
        }
      }
      goto LAB_0044c8b4;
    }
    *(undefined2 *)&pUVar5[uVar21].field_0xc0 = *(undefined2 *)&pUVar5[uVar21].field_0x80;
    FUN_004237df();
    uVar24 = FUN_00423b27(extraout_ECX_28,extraout_EDX_04);
    pUVar5[uVar21].field_0x89 = 2;
    pUVar10 = tabela_unidades + (in_EAX & 0xffff);
    pUVar10->celula_destino = (short)uVar24 - 0xfe;
joined_r0x0044dc80:
    local_4c = (UnidadeParcial *)(in_EAX & 0xffff);
    if (sVar22 != DAT_00496304) goto LAB_0044c8b4;
    local_4c = (UnidadeParcial *)(in_EAX & 0xffff);
    goto LAB_0044d224;
  case 2:
    uVar9 = tabela_unidades[uVar21].celula_atual;
    if (tabela_unidades[uVar21].celula_destino == uVar9) {
      pUVar11 = (UnidadeParcial *)(uint)(byte)tabela_unidades[uVar21].field_0x82;
      if (pUVar11 != (UnidadeParcial *)0x2) {
        if (pUVar11 != (UnidadeParcial *)0x1) goto switchD_0044d86e_default;
        if (*(ushort *)&tabela_unidades[uVar21].field_0x80 == uVar9) {
          iVar14 = (uint)tabela_unidades[uVar21].tipo_id * 0x19;
          tabela_unidades[uVar21].field_0x89 = 4;
        }
        else {
          uVar16 = FUN_00442668(0,*(ushort *)&tabela_unidades[uVar21].field_0x80);
          if ((char)uVar16 != '\0') {
            local_4c = (UnidadeParcial *)
                       CONCAT22((short)(uVar16 >> 0x10),*(ushort *)&pUVar5[uVar21].field_0x80);
            pUVar10 = tabela_unidades + uVar21;
            pUVar10->celula_destino = *(ushort *)&pUVar5[uVar21].field_0x80;
            if (sVar22 == DAT_00496304) {
              local_4c = (UnidadeParcial *)((uint)local_4c & 0xffffff00);
              DAT_004e0f36 = 0;
              DAT_004e0f37 = 0;
              DAT_004e0f3c = 0;
              DAT_00496304 = -1;
            }
            goto LAB_0044c8b4;
          }
          pUVar11 = (UnidadeParcial *)
                    FUN_00479555(*(ushort *)&pUVar5[uVar21].field_0x80 >> 8,
                                 pUVar5[uVar21].celula_atual >> 8);
          if ((UnidadeParcial *)0xf < pUVar11) goto switchD_0044d86e_default;
          pUVar5[uVar21].field_0x89 = 4;
          iVar14 = (uint)pUVar5[uVar21].tipo_id * 0x19;
          *(ushort *)&pUVar5[uVar21].field_0x80 = pUVar5[uVar21].celula_atual;
        }
        goto LAB_0044d533;
      }
      uVar24 = FUN_00423b27(uVar16,CONCAT22((short)(param_2 >> 0x10),uVar9));
      if ((uint)pUVar5[uVar21].celula_atual != ((uint)uVar24 & 0xffff) - 0xfe) {
        uVar24 = FUN_00423b27(extraout_ECX_29,(uint)pUVar5[uVar21].celula_atual);
        pUVar10 = (UnidadeParcial *)(&tabela_unidades->proprietario_id + extraout_ECX_30);
        local_4c = (UnidadeParcial *)((int)uVar24 - 0xfe);
        goto LAB_0044c554;
      }
      pUVar5[uVar21].field_0x89 = 3;
      iVar14 = (uint)pUVar5[uVar21].tipo_id * 0x19;
      pUVar5[uVar21].direcao_desejada = 9;
      goto LAB_0044c93b;
    }
    break;
  case 3:
    if (tabela_unidades[uVar21].direcao_desejada != tabela_unidades[uVar21].orientacao_atual) {
      uVar24 = FUN_00448599(uVar16,param_2);
      pUVar11 = (UnidadeParcial *)uVar24;
      goto switchD_0044d86e_default;
    }
    FUN_0041a65c(uVar16,1);
    lVar23 = FUN_00420c7c(extraout_ECX_31,extraout_EDX_05);
    pUVar11 = (UnidadeParcial *)lVar23;
    if ((char)lVar23 == '\0') goto switchD_0044d86e_default;
    iVar14 = (uint)pUVar5[uVar21].tipo_id * 0x19;
    pUVar5[uVar21].field_0x89 = 4;
    goto LAB_0044c93b;
  case 4:
    uVar16 = FUN_004471b8(&tabela_unidades[uVar21].campo_0a,'\x02');
    if ((uVar16 & 0xffff) == 0) {
      if (pUVar5[uVar21].field_0x82 == '\x02') {
        FUN_0041a65c(extraout_ECX_32,0);
        FUN_004237ff();
        *(undefined2 *)&pUVar5[uVar21].field_0xc0 = 0xffff;
      }
      pUVar10 = tabela_unidades;
      if (*(short *)&pUVar5[uVar21].field_0xb2 == -1) {
        if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
           (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
          pUVar11 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar11 = (UnidadeParcial *)0x1;
        }
        if ((char)pUVar11 != '\0') {
          tabela_unidades[in_EAX & 0xffff].estado = 7;
          pUVar11 = pUVar10;
          if (sVar22 == DAT_00496304) {
            DAT_004e0f36 = bVar19 ^ (byte)((ushort)DAT_00496304 >> 8);
            DAT_004e0f37 = 0;
            DAT_00496304 = -1;
            DAT_004e0f3c = 0;
          }
        }
        goto switchD_0044d86e_default;
      }
      pUVar5[uVar21].field_0x89 = 0;
      pUVar11 = tabela_unidades + (in_EAX & 0xffff);
      pUVar11->celula_destino = *(ushort *)&pUVar5[uVar21].field_0xb2;
      if (sVar22 == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = -1;
      }
LAB_0044cb71:
      pUVar11->estado_caminho = 0;
      goto switchD_0044d86e_default;
    }
    bVar19 = pUVar5[uVar21].field_0x8b - 1;
    pUVar5[uVar21].field_0x8b = bVar19;
    pUVar11 = (UnidadeParcial *)(uint)bVar19;
    if ((UnidadeParcial *)(uint)bVar19 != (UnidadeParcial *)0x0) goto switchD_0044d86e_default;
    pUVar11 = (UnidadeParcial *)(uint)(byte)pUVar5[uVar21].field_0x82;
    if (pUVar11 != (UnidadeParcial *)0x2) {
      if (pUVar11 == (UnidadeParcial *)0x1) {
        pUVar11 = (UnidadeParcial *)FUN_004438d8(extraout_ECX_32,2);
      }
      goto switchD_0044d86e_default;
    }
    FUN_004472ea(extraout_ECX_32,pUVar5[uVar21].field_0x82);
    uVar18 = 0;
LAB_0044c91c:
    FUN_0042340f(CONCAT22(uVar18,*(undefined2 *)&pUVar5[uVar21].field_0x80),1);
    iVar14 = (uint)pUVar5[uVar21].tipo_id * 0x19;
LAB_0044c93b:
    pUVar11 = (UnidadeParcial *)(*(ushort *)(&DAT_004965de + iVar14 * 2) / 2);
LAB_0044d549:
    pUVar5[uVar21].field_0x8b = (char)pUVar11;
  default:
    goto switchD_0044d86e_default;
  }
LAB_0044bd11:
  pUVar11 = (UnidadeParcial *)FUN_0044930c();
switchD_0044d86e_default:
  return CONCAT44(param_2,pUVar11);
}
