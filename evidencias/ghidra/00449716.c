/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00449716, entrada 00449716.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00449716(undefined4 param_1,undefined4 param_2)

{
  bool bVar1;
  char cVar2;
  ushort in_AX;
  ushort uVar3;
  int iVar4;
  UnidadeParcial *pUVar5;
  UnidadeParcial *pUVar6;
  UnidadeParcial *pUVar7;
  byte bVar9;
  undefined4 uVar8;
  byte bVar12;
  int extraout_ECX;
  int extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  uint uVar10;
  uint extraout_ECX_04;
  uint extraout_ECX_05;
  undefined4 extraout_ECX_06;
  undefined4 extraout_ECX_07;
  undefined4 extraout_ECX_08;
  uint extraout_ECX_09;
  uint extraout_ECX_10;
  uint extraout_ECX_11;
  undefined2 extraout_var;
  undefined4 extraout_ECX_12;
  undefined4 extraout_ECX_13;
  uint extraout_ECX_14;
  uint uVar11;
  undefined4 extraout_ECX_15;
  undefined4 extraout_ECX_16;
  undefined4 extraout_ECX_17;
  undefined4 extraout_ECX_18;
  undefined4 extraout_ECX_19;
  undefined1 extraout_DL;
  undefined1 extraout_DL_00;
  int extraout_EDX;
  undefined4 extraout_EDX_00;
  uint extraout_EDX_01;
  uint uVar13;
  uint extraout_EDX_02;
  int extraout_EDX_03;
  undefined4 extraout_EDX_04;
  int iVar14;
  int iVar15;
  UnidadeParcial *pUVar16;
  undefined8 uVar17;
  ulonglong uVar18;
  ulonglong uVar19;
  longlong lVar20;
  ushort uStack_2c;

  pUVar16 = tabela_unidades + in_AX;
  bVar12 = pUVar16->tipo_id;
  if ((((bVar12 < 6) || (bVar12 < 7)) || (bVar12 < 9)) || (bVar12 < 0xb)) {
LAB_00449769:
    pUVar5 = (UnidadeParcial *)(uint)*(ushort *)&pUVar16->field_0xc0;
    if ((UnidadeParcial *)(uint)*(ushort *)&pUVar16->field_0xc0 == (UnidadeParcial *)0xffff)
    goto switchD_0044d86e_default;
    uVar17 = FUN_0041a4f4(param_1,param_2);
    iVar4 = extraout_ECX;
    if (((uint)uVar17 & 0xff) == 8) {
      uVar17 = FUN_0041a08c((uint)in_AX,(int)((ulonglong)uVar17 >> 0x20));
      iVar14 = (uint)in_AX * 0x44 + extraout_ECX_00;
      iVar15 = iVar14 * 4;
      iVar4 = extraout_ECX_00;
      if ((byte)uVar17 == (&tabela_unidades->proprietario_id)[iVar15]) {
        iVar4 = FUN_0041d057(extraout_ECX_00);
        *(ushort *)&pUVar16->field_0xb2 = (ushort)iVar4;
        pUVar16 = tabela_unidades;
        (&tabela_unidades->celula_destino)[iVar14 * 2] = (ushort)iVar4;
        if (in_AX == DAT_00496304) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_004e0f3c = 0;
          DAT_00496304 = 0xffff;
        }
        (&pUVar16->estado_caminho)[iVar15] = 0;
        pUVar16 = tabela_unidades;
        if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
          pUVar5 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar5 = (UnidadeParcial *)0x1;
        }
        if (((char)pUVar5 != '\0') &&
           (tabela_unidades[in_AX].estado = 0x15, pUVar5 = pUVar16, in_AX == DAT_00496304)) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_00496304 = 0xffff;
          DAT_004e0f3c = 0;
          pUVar5 = (UnidadeParcial *)0x0;
        }
        goto switchD_0044d86e_default;
      }
    }
    if (((*(int *)&pUVar16->field_0x83 >> 0x18 == 0) && (*(int *)&pUVar16->field_0x84 >> 0x18 == 0))
       && (iVar4 = FUN_0042381f(iVar4,(uint)pUVar16->celula_atual), (char)iVar4 != '\0')) {
      uVar13 = (uint)in_AX;
      cVar2 = FUN_0041f76e(uVar13,uVar13);
      pUVar7 = tabela_unidades;
      if (cVar2 == '\0') {
        if ((tabela_unidades[uVar13].estado == 0) || (tabela_unidades[uVar13].estado == 4)) {
          pUVar5 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar5 = (UnidadeParcial *)0x1;
        }
        if (((char)pUVar5 != '\0') &&
           (tabela_unidades[in_AX].estado = 7, pUVar5 = pUVar7, in_AX == DAT_00496304)) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_00496304 = 0xffff;
          DAT_004e0f3c = 0;
        }
      }
      else {
        uVar3 = FUN_0041aee2();
        FUN_00457058();
        uVar8 = extraout_EDX_00;
        if (tabela_unidades[uVar13].tipo_id == 10) {
          uVar17 = FUN_0041a4f4(extraout_ECX_01,extraout_EDX_00);
          uVar8 = (undefined4)((ulonglong)uVar17 >> 0x20);
          if (((uint)uVar17 & 0xff) == 0x10) {
            uVar3 = (ushort)((ulonglong)uVar17 >> 0x20);
            pUVar16->celula_passo = uVar3;
            pUVar16->celula_atual = uVar3;
            FUN_00472648(extraout_ECX_02);
            FUN_004829c8(extraout_ECX_03,extraout_DL);
            pUVar16 = tabela_unidades;
            if ((tabela_unidades[uVar13].estado == 0) || (tabela_unidades[uVar13].estado == 4)) {
              pUVar5 = (UnidadeParcial *)0x0;
            }
            else {
              pUVar5 = (UnidadeParcial *)0x1;
            }
            if (((char)pUVar5 != '\0') &&
               (tabela_unidades[in_AX].estado = 0, pUVar5 = pUVar16, in_AX == DAT_00496304)) {
              DAT_004e0f36 = 0;
              DAT_004e0f37 = 0;
              DAT_004e0f3c = 0;
              DAT_00496304 = 0xffff;
              pUVar5 = (UnidadeParcial *)((uint)pUVar16 & 0xffffff00);
            }
            goto switchD_0044d86e_default;
          }
        }
        uVar10 = (uint)in_AX;
        uVar19 = CONCAT44(uVar8,(uint)tabela_unidades[uVar10].tipo_id);
        uVar13 = uVar10;
        if (tabela_unidades[uVar10].tipo_id == 10) {
          uVar18 = FUN_0041a4f4(uVar10,uVar8);
          uVar19 = uVar18 & 0xffffffff000000ff;
          uVar13 = extraout_ECX_04;
          if ((((uint)uVar18 & 0xff) == 2) &&
             (uVar19 = FUN_0041a08c(extraout_ECX_04,(int)(uVar18 >> 0x20)), uVar13 = extraout_ECX_05
             , (byte)uVar19 != pUVar16->proprietario_id)) {
            uVar17 = FUN_0041a08c(extraout_ECX_05,0);
            FUN_0046dadb(extraout_ECX_06,(byte)uVar17);
            pUVar16->celula_passo = uVar3;
            pUVar16->celula_atual = uVar3;
            FUN_00472648(extraout_ECX_07);
            FUN_004829c8(extraout_ECX_08,extraout_DL_00);
            pUVar16 = tabela_unidades;
            if ((tabela_unidades[uVar10].estado == 0) || (tabela_unidades[uVar10].estado == 4)) {
              pUVar5 = (UnidadeParcial *)0x0;
            }
            else {
              pUVar5 = (UnidadeParcial *)0x1;
            }
            if (((char)pUVar5 != '\0') &&
               (tabela_unidades[in_AX].estado = 0, pUVar5 = pUVar16, in_AX == DAT_00496304)) {
              DAT_004e0f36 = 0;
              DAT_004e0f37 = 0;
              DAT_004e0f3c = 0;
              DAT_00496304 = 0xffff;
            }
            goto switchD_0044d86e_default;
          }
        }
        if (pUVar16->tipo_id != 9) {
          uVar17 = FUN_0041a4f4(uVar13,(int)(uVar19 >> 0x20));
          uVar13 = extraout_ECX_09;
          if ((((uint)uVar17 & 0xff) != 0x13) &&
             (uVar17 = FUN_0041a4f4(extraout_ECX_09,(int)((ulonglong)uVar17 >> 0x20)),
             uVar13 = extraout_ECX_10, ((uint)uVar17 & 0xff) != 0x15)) {
            FUN_004829c8((uint)in_AX,0x47);
            FUN_004571d4();
            uVar13 = extraout_ECX_11;
          }
        }
        pUVar16->celula_passo = uVar3;
        pUVar16->celula_atual = uVar3;
        pUVar5 = (UnidadeParcial *)FUN_00472648(uVar13);
        pUVar16->estado = 0xe;
      }
      goto switchD_0044d86e_default;
    }
    if (pUVar16->celula_destino == pUVar16->celula_atual) {
      uVar3 = FUN_0041aee2();
      pUVar16 = tabela_unidades;
      iVar4 = (uint)in_AX * 0x44 + extraout_EDX;
      (&tabela_unidades->celula_destino)[iVar4 * 2] = uVar3;
      if (in_AX == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f3c = 0;
        DAT_004e0f37 = 0;
        DAT_00496304 = 0xffff;
      }
      (&pUVar16->estado_caminho)[iVar4 * 4] = 0;
    }
LAB_00449950:
    pUVar5 = (UnidadeParcial *)FUN_0044930c();
  }
  else {
    if (bVar12 < 0x10) {
LAB_0044a12f:
      pUVar5 = (UnidadeParcial *)(uint)*(ushort *)&pUVar16->field_0xc0;
      if ((UnidadeParcial *)(uint)*(ushort *)&pUVar16->field_0xc0 == (UnidadeParcial *)0xffff)
      goto switchD_0044d86e_default;
      uVar3 = pUVar16->celula_destino;
      if (pUVar16->celula_atual != uVar3) goto LAB_00449950;
      if (uVar3 == *(ushort *)&pUVar16->field_0xb2) {
        pUVar16->direcao_desejada = 5;
        uVar17 = FUN_00448599(param_1,CONCAT22((short)((uint)param_2 >> 0x10),uVar3));
        pUVar5 = (UnidadeParcial *)
                 CONCAT31((int3)((ulonglong)uVar17 >> 8),pUVar16->direcao_desejada);
        if (pUVar16->direcao_desejada == pUVar16->orientacao_atual) {
          FUN_0041a65c(extraout_ECX_16,1);
          lVar20 = FUN_00420c19(extraout_ECX_17,extraout_EDX_04);
          pUVar5 = (UnidadeParcial *)lVar20;
          if ((char)lVar20 != '\0') {
            uVar8 = FUN_00425516(extraout_ECX_18,in_AX);
            pUVar7 = tabela_unidades;
            if ((char)uVar8 == '\0') {
              if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
                pUVar5 = (UnidadeParcial *)0x0;
              }
              else {
                pUVar5 = (UnidadeParcial *)0x1;
              }
              if (((char)pUVar5 != '\0') &&
                 (tabela_unidades[in_AX].estado = 7, pUVar5 = pUVar7, in_AX == DAT_00496304)) {
                DAT_004e0f36 = 0;
                DAT_004e0f37 = 0;
                DAT_00496304 = 0xffff;
                DAT_004e0f3c = 0;
              }
            }
            else {
              FUN_00457058();
              uVar3 = FUN_0041aee2();
              pUVar16->celula_passo = uVar3;
              pUVar16->celula_atual = uVar3;
              pUVar16->estado = 0xe;
              pUVar5 = (UnidadeParcial *)FUN_00472648(extraout_ECX_19);
            }
          }
        }
        goto switchD_0044d86e_default;
      }
      pUVar5 = (UnidadeParcial *)FUN_00442668(0,*(ushort *)&pUVar16->field_0xb2);
      if ((char)pUVar5 == '\0') goto switchD_0044d86e_default;
      pUVar7 = tabela_unidades + in_AX;
      pUVar5 = (UnidadeParcial *)
               CONCAT22((short)((uint)pUVar5 >> 0x10),*(ushort *)&pUVar16->field_0xb2);
      pUVar7->celula_destino = *(ushort *)&pUVar16->field_0xb2;
      if (in_AX == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_00496304 = 0xffff;
        DAT_004e0f3c = 0;
      }
    }
    else {
      if (0x10 < bVar12) {
        if (bVar12 == 0x19) goto LAB_00449769;
        goto LAB_0044a12f;
      }
      if (*(short *)&pUVar16->field_0xc0 == -1) {
        FUN_00472648(param_1);
        if (pUVar16->field_0xab == '2') {
          if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
            bVar1 = false;
          }
          else {
            bVar1 = true;
          }
          if ((bVar1) && (tabela_unidades[in_AX].estado = 7, in_AX == DAT_00496304)) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = 0xffff;
          }
        }
        else if (((byte)DAT_00508f7c & 1) == 0) {
          pUVar16->field_0xab = pUVar16->field_0xab + '\x01';
        }
        pUVar16 = tabela_unidades;
        bVar12 = tabela_unidades[in_AX].tipo_id;
        pUVar5 = (UnidadeParcial *)CONCAT31((int3)((uint)tabela_unidades >> 8),bVar12);
        if ((10 < bVar12) && (0xb < bVar12)) {
          if (bVar12 < 0x12) {
            if ((0xd < bVar12) && (0xf < bVar12)) {
joined_r0x0044a124:
              if (bVar12 == 0x11) {
                pUVar5 = (UnidadeParcial *)FUN_00447b2f();
              }
              goto switchD_0044d86e_default;
            }
          }
          else if ((0x12 < bVar12) && (((0x16 < bVar12 && (0x18 < bVar12)) && (bVar12 != 0x19))))
          goto switchD_0044d86e_default;
        }
        bVar12 = tabela_unidades[in_AX].contador_animacao + 1;
        tabela_unidades[in_AX].contador_animacao = bVar12;
        if (bVar12 == pUVar16[in_AX].periodo_animacao) {
          uVar13 = pUVar16[in_AX].quadro_movimento + 1;
          bVar12 = pUVar16[in_AX].quantidade_quadros_movimento;
          pUVar5 = (UnidadeParcial *)(uVar13 / bVar12);
          pUVar16[in_AX].contador_animacao = 0;
          pUVar16[in_AX].quadro_movimento = (byte)(uVar13 % (uint)bVar12);
        }
        goto switchD_0044d86e_default;
      }
      uVar17 = FUN_0041aee2();
      uVar13 = (uint)((ulonglong)uVar17 >> 0x20);
      pUVar6 = (UnidadeParcial *)((int)uVar17 + 1);
      uVar3 = pUVar16->celula_destino;
      uVar8 = CONCAT22(extraout_var,uVar3);
      if (uVar3 != pUVar16->celula_atual) goto LAB_00449950;
      uStack_2c = (ushort)pUVar6;
      if (uVar3 == uStack_2c) {
        if (((tabela_unidades[in_AX].field_0xda == '\x05') &&
            (uVar13 = (uint)*(ushort *)(&DAT_004965b6 + (uint)tabela_unidades[in_AX].tipo_id * 0x32)
            , tabela_unidades[in_AX].vida ==
              *(ushort *)(&DAT_004965b6 + (uint)tabela_unidades[in_AX].tipo_id * 0x32))) ||
           (uVar17 = FUN_0041a08c(uVar8,uVar13), uVar8 = extraout_ECX_12,
           (byte)uVar17 != pUVar16->proprietario_id)) {
          FUN_00472648(uVar8);
          pUVar5 = tabela_unidades;
          bVar12 = pUVar16->field_0xab;
          if ((UnidadeParcial *)(uint)bVar12 == (UnidadeParcial *)0x32) {
            if ((tabela_unidades[extraout_EDX_03].estado == 0) ||
               (tabela_unidades[extraout_EDX_03].estado == 4)) {
              pUVar7 = (UnidadeParcial *)0x0;
            }
            else {
              pUVar7 = (UnidadeParcial *)0x1;
            }
            if (((char)pUVar7 != '\0') &&
               (tabela_unidades[in_AX].estado = 7, pUVar7 = pUVar5, in_AX == DAT_00496304)) {
              DAT_004e0f36 = 0;
              DAT_004e0f3c = 0;
              pUVar7 = (UnidadeParcial *)0xffff;
              DAT_004e0f37 = 0;
              DAT_00496304 = 0xffff;
            }
          }
          else {
            pUVar7 = (UnidadeParcial *)(uint)bVar12;
            if (((byte)DAT_00508f7c & 1) == 0) {
              pUVar16->field_0xab = bVar12 + 1;
              pUVar7 = (UnidadeParcial *)0x0;
            }
          }
          pUVar16 = tabela_unidades;
          bVar12 = tabela_unidades[in_AX].tipo_id;
          pUVar5 = (UnidadeParcial *)CONCAT31((int3)((uint)pUVar7 >> 8),bVar12);
          if ((10 < bVar12) && (0xb < bVar12)) {
            if (bVar12 < 0x12) {
              if ((0xd < bVar12) && (0xf < bVar12)) goto joined_r0x0044a124;
            }
            else if ((((0x12 < bVar12) && (0x16 < bVar12)) && (0x18 < bVar12)) && (bVar12 != 0x19))
            goto switchD_0044d86e_default;
          }
          bVar9 = tabela_unidades[in_AX].contador_animacao + 1;
          pUVar5 = (UnidadeParcial *)CONCAT22((short)((uint)pUVar7 >> 0x10),CONCAT11(bVar9,bVar12));
          bVar12 = tabela_unidades[in_AX].periodo_animacao;
          tabela_unidades[in_AX].contador_animacao = bVar9;
          if (bVar9 == bVar12) {
            uVar13 = pUVar16[in_AX].quadro_movimento + 1;
            bVar12 = pUVar16[in_AX].quantidade_quadros_movimento;
            pUVar5 = (UnidadeParcial *)(uVar13 / bVar12);
            pUVar16[in_AX].contador_animacao = 0;
            pUVar16[in_AX].quadro_movimento = (byte)(uVar13 % (uint)bVar12);
          }
          goto switchD_0044d86e_default;
        }
        pUVar16->direcao_desejada = 5;
        uVar17 = FUN_00448599(extraout_ECX_12,(uint)in_AX);
        pUVar5 = (UnidadeParcial *)
                 CONCAT31((int3)((ulonglong)uVar17 >> 8),pUVar16->direcao_desejada);
        if (pUVar16->direcao_desejada != pUVar16->orientacao_atual) goto switchD_0044d86e_default;
        FUN_00472648(extraout_ECX_13);
        if ((((byte)DAT_00508f7c & 1) == 0) && (pUVar16->field_0xab != '\x01')) {
          pUVar16->field_0xab = pUVar16->field_0xab + -1;
        }
        pUVar5 = tabela_unidades;
        uVar10 = (uint)in_AX;
        bVar12 = tabela_unidades[uVar10].tipo_id;
        uVar13 = extraout_EDX_01;
        if ((bVar12 < 0xb) || (bVar12 < 0xc)) {
LAB_00449d94:
          bVar12 = tabela_unidades[uVar10].contador_animacao + 1;
          pUVar7 = tabela_unidades + uVar10;
          tabela_unidades[uVar10].contador_animacao = bVar12;
          uVar11 = (uint)CONCAT11(bVar12,(char)in_AX);
          if (bVar12 == pUVar7->periodo_animacao) {
            uVar13 = (pUVar5[uVar10].quadro_movimento + 1) %
                     (uint)pUVar5[uVar10].quantidade_quadros_movimento;
            pUVar5[uVar10].contador_animacao = 0;
            pUVar5[uVar10].quadro_movimento = (byte)uVar13;
            uVar11 = (uint)pUVar5[uVar10].quantidade_quadros_movimento;
          }
        }
        else {
          uVar11 = uVar10;
          if (bVar12 < 0x12) {
            if ((bVar12 < 0xe) || (bVar12 < 0x10)) goto LAB_00449d94;
            if (bVar12 == 0x11) {
              FUN_00447b2f();
              uVar11 = extraout_ECX_14;
              uVar13 = extraout_EDX_02;
            }
          }
          else if ((((bVar12 < 0x13) || (bVar12 < 0x17)) || (bVar12 < 0x19)) || (bVar12 == 0x19))
          goto LAB_00449d94;
        }
        pUVar5 = (UnidadeParcial *)(uint)(byte)pUVar16->field_0xab;
        if (pUVar5 == (UnidadeParcial *)0x1) {
          uVar17 = FUN_004237c0(uVar11,uVar13);
          pUVar5 = (UnidadeParcial *)uVar17;
          if ((char)uVar17 == '\0') {
            pUVar5 = (UnidadeParcial *)FUN_00425516(extraout_ECX_15,in_AX);
          }
        }
        goto switchD_0044d86e_default;
      }
      pUVar5 = (UnidadeParcial *)FUN_00442668(0,uStack_2c);
      if ((char)pUVar5 == '\0') goto switchD_0044d86e_default;
      pUVar7 = tabela_unidades + in_AX;
      pUVar7->celula_destino = uStack_2c;
      pUVar5 = pUVar6;
      if (in_AX == DAT_00496304) {
        pUVar5 = (UnidadeParcial *)((uint)pUVar6 & 0xffffff00);
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = 0xffff;
      }
    }
    pUVar7->estado_caminho = 0;
  }
switchD_0044d86e_default:
  return CONCAT44(param_2,pUVar5);
}
