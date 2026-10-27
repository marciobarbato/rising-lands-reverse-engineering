/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00449716, entrada 00449716.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00449716(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  bool bVar2;
  char cVar3;
  ushort in_AX;
  ushort uVar4;
  int iVar5;
  UnidadeParcial *pUVar6;
  UnidadeParcial *pUVar7;
  UnidadeParcial *pUVar8;
  char cVar10;
  undefined4 uVar9;
  int extraout_ECX;
  int extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  uint uVar11;
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
  uint uVar12;
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
  bVar1 = pUVar16->tipo_id;
  if ((((bVar1 < 6) || (bVar1 < 7)) || (bVar1 < 9)) || (bVar1 < 0xb)) {
LAB_00449769:
    pUVar6 = (UnidadeParcial *)(uint)*(ushort *)&pUVar16->field_0xc0;
    if ((UnidadeParcial *)(uint)*(ushort *)&pUVar16->field_0xc0 == (UnidadeParcial *)0xffff)
    goto switchD_0044d86e_default;
    uVar17 = FUN_0041a4f4(param_1,param_2);
    iVar5 = extraout_ECX;
    if (((uint)uVar17 & 0xff) == 8) {
      uVar17 = FUN_0041a08c((uint)in_AX,(int)((ulonglong)uVar17 >> 0x20));
      iVar14 = (uint)in_AX * 0x44 + extraout_ECX_00;
      iVar15 = iVar14 * 4;
      iVar5 = extraout_ECX_00;
      if ((byte)uVar17 == (&tabela_unidades->proprietario_id)[iVar15]) {
        iVar5 = FUN_0041d057(extraout_ECX_00);
        *(ushort *)&pUVar16->field_0xb2 = (ushort)iVar5;
        pUVar16 = tabela_unidades;
        (&tabela_unidades->celula_destino)[iVar14 * 2] = (ushort)iVar5;
        if (in_AX == DAT_00496304) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_004e0f3c = 0;
          DAT_00496304 = 0xffff;
        }
        (&pUVar16->estado_caminho)[iVar15] = 0;
        pUVar16 = tabela_unidades;
        if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
          pUVar6 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar6 = (UnidadeParcial *)0x1;
        }
        if (((char)pUVar6 != '\0') &&
           (tabela_unidades[in_AX].estado = 0x15, pUVar6 = pUVar16, in_AX == DAT_00496304)) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_00496304 = 0xffff;
          DAT_004e0f3c = 0;
          pUVar6 = (UnidadeParcial *)0x0;
        }
        goto switchD_0044d86e_default;
      }
    }
    if (((*(int *)&pUVar16->field_0x83 >> 0x18 == 0) && (*(int *)&pUVar16->field_0x84 >> 0x18 == 0))
       && (iVar5 = FUN_0042381f(iVar5,(uint)pUVar16->celula_atual), (char)iVar5 != '\0')) {
      uVar13 = (uint)in_AX;
      cVar3 = FUN_0041f76e(uVar13,uVar13);
      pUVar8 = tabela_unidades;
      if (cVar3 == '\0') {
        if ((tabela_unidades[uVar13].estado == 0) || (tabela_unidades[uVar13].estado == 4)) {
          pUVar6 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar6 = (UnidadeParcial *)0x1;
        }
        if (((char)pUVar6 != '\0') &&
           (tabela_unidades[in_AX].estado = 7, pUVar6 = pUVar8, in_AX == DAT_00496304)) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_00496304 = 0xffff;
          DAT_004e0f3c = 0;
        }
      }
      else {
        uVar4 = FUN_0041aee2();
        FUN_00457058();
        uVar9 = extraout_EDX_00;
        if (tabela_unidades[uVar13].tipo_id == 10) {
          uVar17 = FUN_0041a4f4(extraout_ECX_01,extraout_EDX_00);
          uVar9 = (undefined4)((ulonglong)uVar17 >> 0x20);
          if (((uint)uVar17 & 0xff) == 0x10) {
            uVar4 = (ushort)((ulonglong)uVar17 >> 0x20);
            pUVar16->celula_passo = uVar4;
            pUVar16->celula_atual = uVar4;
            FUN_00472648(extraout_ECX_02);
            FUN_004829c8(extraout_ECX_03,extraout_DL);
            pUVar16 = tabela_unidades;
            if ((tabela_unidades[uVar13].estado == 0) || (tabela_unidades[uVar13].estado == 4)) {
              pUVar6 = (UnidadeParcial *)0x0;
            }
            else {
              pUVar6 = (UnidadeParcial *)0x1;
            }
            if (((char)pUVar6 != '\0') &&
               (tabela_unidades[in_AX].estado = 0, pUVar6 = pUVar16, in_AX == DAT_00496304)) {
              DAT_004e0f36 = 0;
              DAT_004e0f37 = 0;
              DAT_004e0f3c = 0;
              DAT_00496304 = 0xffff;
              pUVar6 = (UnidadeParcial *)((uint)pUVar16 & 0xffffff00);
            }
            goto switchD_0044d86e_default;
          }
        }
        uVar11 = (uint)in_AX;
        uVar19 = CONCAT44(uVar9,(uint)tabela_unidades[uVar11].tipo_id);
        uVar13 = uVar11;
        if (tabela_unidades[uVar11].tipo_id == 10) {
          uVar18 = FUN_0041a4f4(uVar11,uVar9);
          uVar19 = uVar18 & 0xffffffff000000ff;
          uVar13 = extraout_ECX_04;
          if ((((uint)uVar18 & 0xff) == 2) &&
             (uVar19 = FUN_0041a08c(extraout_ECX_04,(int)(uVar18 >> 0x20)), uVar13 = extraout_ECX_05
             , (byte)uVar19 != pUVar16->proprietario_id)) {
            uVar17 = FUN_0041a08c(extraout_ECX_05,0);
            FUN_0046dadb(extraout_ECX_06,(byte)uVar17);
            pUVar16->celula_passo = uVar4;
            pUVar16->celula_atual = uVar4;
            FUN_00472648(extraout_ECX_07);
            FUN_004829c8(extraout_ECX_08,extraout_DL_00);
            pUVar16 = tabela_unidades;
            if ((tabela_unidades[uVar11].estado == 0) || (tabela_unidades[uVar11].estado == 4)) {
              pUVar6 = (UnidadeParcial *)0x0;
            }
            else {
              pUVar6 = (UnidadeParcial *)0x1;
            }
            if (((char)pUVar6 != '\0') &&
               (tabela_unidades[in_AX].estado = 0, pUVar6 = pUVar16, in_AX == DAT_00496304)) {
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
        pUVar16->celula_passo = uVar4;
        pUVar16->celula_atual = uVar4;
        pUVar6 = (UnidadeParcial *)FUN_00472648(uVar13);
        pUVar16->estado = 0xe;
      }
      goto switchD_0044d86e_default;
    }
    if (pUVar16->celula_destino == pUVar16->celula_atual) {
      uVar4 = FUN_0041aee2();
      pUVar16 = tabela_unidades;
      iVar5 = (uint)in_AX * 0x44 + extraout_EDX;
      (&tabela_unidades->celula_destino)[iVar5 * 2] = uVar4;
      if (in_AX == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f3c = 0;
        DAT_004e0f37 = 0;
        DAT_00496304 = 0xffff;
      }
      (&pUVar16->estado_caminho)[iVar5 * 4] = 0;
    }
LAB_00449950:
    pUVar6 = (UnidadeParcial *)FUN_0044930c();
  }
  else {
    if (bVar1 < 0x10) {
LAB_0044a12f:
      pUVar6 = (UnidadeParcial *)(uint)*(ushort *)&pUVar16->field_0xc0;
      if ((UnidadeParcial *)(uint)*(ushort *)&pUVar16->field_0xc0 == (UnidadeParcial *)0xffff)
      goto switchD_0044d86e_default;
      uVar4 = pUVar16->celula_destino;
      if (pUVar16->celula_atual != uVar4) goto LAB_00449950;
      if (uVar4 == *(ushort *)&pUVar16->field_0xb2) {
        pUVar16->field_0x90 = 5;
        uVar17 = FUN_00448599(param_1,CONCAT22((short)((uint)param_2 >> 0x10),uVar4));
        pUVar6 = (UnidadeParcial *)CONCAT31((int3)((ulonglong)uVar17 >> 8),pUVar16->field_0x90);
        if (pUVar16->field_0x90 == pUVar16->field_0x91) {
          FUN_0041a65c(extraout_ECX_16,1);
          lVar20 = FUN_00420c19(extraout_ECX_17,extraout_EDX_04);
          pUVar6 = (UnidadeParcial *)lVar20;
          if ((char)lVar20 != '\0') {
            uVar9 = FUN_00425516(extraout_ECX_18,in_AX);
            pUVar8 = tabela_unidades;
            if ((char)uVar9 == '\0') {
              if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
                pUVar6 = (UnidadeParcial *)0x0;
              }
              else {
                pUVar6 = (UnidadeParcial *)0x1;
              }
              if (((char)pUVar6 != '\0') &&
                 (tabela_unidades[in_AX].estado = 7, pUVar6 = pUVar8, in_AX == DAT_00496304)) {
                DAT_004e0f36 = 0;
                DAT_004e0f37 = 0;
                DAT_00496304 = 0xffff;
                DAT_004e0f3c = 0;
              }
            }
            else {
              FUN_00457058();
              uVar4 = FUN_0041aee2();
              pUVar16->celula_passo = uVar4;
              pUVar16->celula_atual = uVar4;
              pUVar16->estado = 0xe;
              pUVar6 = (UnidadeParcial *)FUN_00472648(extraout_ECX_19);
            }
          }
        }
        goto switchD_0044d86e_default;
      }
      pUVar6 = (UnidadeParcial *)FUN_00442668(0,*(ushort *)&pUVar16->field_0xb2);
      if ((char)pUVar6 == '\0') goto switchD_0044d86e_default;
      pUVar8 = tabela_unidades + in_AX;
      pUVar6 = (UnidadeParcial *)
               CONCAT22((short)((uint)pUVar6 >> 0x10),*(ushort *)&pUVar16->field_0xb2);
      pUVar8->celula_destino = *(ushort *)&pUVar16->field_0xb2;
      if (in_AX == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_00496304 = 0xffff;
        DAT_004e0f3c = 0;
      }
    }
    else {
      if (0x10 < bVar1) {
        if (bVar1 == 0x19) goto LAB_00449769;
        goto LAB_0044a12f;
      }
      if (*(short *)&pUVar16->field_0xc0 == -1) {
        FUN_00472648(param_1);
        if (pUVar16->field_0xab == '2') {
          if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
            bVar2 = false;
          }
          else {
            bVar2 = true;
          }
          if ((bVar2) && (tabela_unidades[in_AX].estado = 7, in_AX == DAT_00496304)) {
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
        bVar1 = tabela_unidades[in_AX].tipo_id;
        pUVar6 = (UnidadeParcial *)CONCAT31((int3)((uint)tabela_unidades >> 8),bVar1);
        if ((10 < bVar1) && (0xb < bVar1)) {
          if (bVar1 < 0x12) {
            if ((0xd < bVar1) && (0xf < bVar1)) {
joined_r0x0044a124:
              if (bVar1 == 0x11) {
                pUVar6 = (UnidadeParcial *)FUN_00447b2f();
              }
              goto switchD_0044d86e_default;
            }
          }
          else if ((0x12 < bVar1) && (((0x16 < bVar1 && (0x18 < bVar1)) && (bVar1 != 0x19))))
          goto switchD_0044d86e_default;
        }
        cVar3 = tabela_unidades[in_AX].field_0xa9 + '\x01';
        tabela_unidades[in_AX].field_0xa9 = cVar3;
        if (cVar3 == pUVar16[in_AX].field_0xa7) {
          uVar13 = (byte)pUVar16[in_AX].field_0xa4 + 1;
          bVar1 = pUVar16[in_AX].field_0xa5;
          pUVar6 = (UnidadeParcial *)(uVar13 / bVar1);
          pUVar16[in_AX].field_0xa9 = 0;
          pUVar16[in_AX].field_0xa4 = (char)(uVar13 % (uint)bVar1);
        }
        goto switchD_0044d86e_default;
      }
      uVar17 = FUN_0041aee2();
      uVar13 = (uint)((ulonglong)uVar17 >> 0x20);
      pUVar7 = (UnidadeParcial *)((int)uVar17 + 1);
      uVar4 = pUVar16->celula_destino;
      uVar9 = CONCAT22(extraout_var,uVar4);
      if (uVar4 != pUVar16->celula_atual) goto LAB_00449950;
      uStack_2c = (ushort)pUVar7;
      if (uVar4 == uStack_2c) {
        if (((tabela_unidades[in_AX].field_0xda == '\x05') &&
            (uVar13 = (uint)*(ushort *)(&DAT_004965b6 + (uint)tabela_unidades[in_AX].tipo_id * 0x32)
            , tabela_unidades[in_AX].vida ==
              *(ushort *)(&DAT_004965b6 + (uint)tabela_unidades[in_AX].tipo_id * 0x32))) ||
           (uVar17 = FUN_0041a08c(uVar9,uVar13), uVar9 = extraout_ECX_12,
           (byte)uVar17 != pUVar16->proprietario_id)) {
          FUN_00472648(uVar9);
          pUVar6 = tabela_unidades;
          bVar1 = pUVar16->field_0xab;
          if ((UnidadeParcial *)(uint)bVar1 == (UnidadeParcial *)0x32) {
            if ((tabela_unidades[extraout_EDX_03].estado == 0) ||
               (tabela_unidades[extraout_EDX_03].estado == 4)) {
              pUVar8 = (UnidadeParcial *)0x0;
            }
            else {
              pUVar8 = (UnidadeParcial *)0x1;
            }
            if (((char)pUVar8 != '\0') &&
               (tabela_unidades[in_AX].estado = 7, pUVar8 = pUVar6, in_AX == DAT_00496304)) {
              DAT_004e0f36 = 0;
              DAT_004e0f3c = 0;
              pUVar8 = (UnidadeParcial *)0xffff;
              DAT_004e0f37 = 0;
              DAT_00496304 = 0xffff;
            }
          }
          else {
            pUVar8 = (UnidadeParcial *)(uint)bVar1;
            if (((byte)DAT_00508f7c & 1) == 0) {
              pUVar16->field_0xab = bVar1 + 1;
              pUVar8 = (UnidadeParcial *)0x0;
            }
          }
          pUVar16 = tabela_unidades;
          bVar1 = tabela_unidades[in_AX].tipo_id;
          pUVar6 = (UnidadeParcial *)CONCAT31((int3)((uint)pUVar8 >> 8),bVar1);
          if ((10 < bVar1) && (0xb < bVar1)) {
            if (bVar1 < 0x12) {
              if ((0xd < bVar1) && (0xf < bVar1)) goto joined_r0x0044a124;
            }
            else if ((((0x12 < bVar1) && (0x16 < bVar1)) && (0x18 < bVar1)) && (bVar1 != 0x19))
            goto switchD_0044d86e_default;
          }
          cVar10 = tabela_unidades[in_AX].field_0xa9 + '\x01';
          pUVar6 = (UnidadeParcial *)CONCAT22((short)((uint)pUVar8 >> 0x10),CONCAT11(cVar10,bVar1));
          cVar3 = tabela_unidades[in_AX].field_0xa7;
          tabela_unidades[in_AX].field_0xa9 = cVar10;
          if (cVar10 == cVar3) {
            uVar13 = (byte)pUVar16[in_AX].field_0xa4 + 1;
            bVar1 = pUVar16[in_AX].field_0xa5;
            pUVar6 = (UnidadeParcial *)(uVar13 / bVar1);
            pUVar16[in_AX].field_0xa9 = 0;
            pUVar16[in_AX].field_0xa4 = (char)(uVar13 % (uint)bVar1);
          }
          goto switchD_0044d86e_default;
        }
        pUVar16->field_0x90 = 5;
        uVar17 = FUN_00448599(extraout_ECX_12,(uint)in_AX);
        pUVar6 = (UnidadeParcial *)CONCAT31((int3)((ulonglong)uVar17 >> 8),pUVar16->field_0x90);
        if (pUVar16->field_0x90 != pUVar16->field_0x91) goto switchD_0044d86e_default;
        FUN_00472648(extraout_ECX_13);
        if ((((byte)DAT_00508f7c & 1) == 0) && (pUVar16->field_0xab != '\x01')) {
          pUVar16->field_0xab = pUVar16->field_0xab + -1;
        }
        pUVar6 = tabela_unidades;
        uVar11 = (uint)in_AX;
        bVar1 = tabela_unidades[uVar11].tipo_id;
        uVar13 = extraout_EDX_01;
        if ((bVar1 < 0xb) || (bVar1 < 0xc)) {
LAB_00449d94:
          cVar3 = tabela_unidades[uVar11].field_0xa9 + '\x01';
          pUVar8 = tabela_unidades + uVar11;
          tabela_unidades[uVar11].field_0xa9 = cVar3;
          uVar12 = (uint)CONCAT11(cVar3,(char)in_AX);
          if (cVar3 == pUVar8->field_0xa7) {
            uVar13 = ((byte)pUVar6[uVar11].field_0xa4 + 1) % (uint)(byte)pUVar6[uVar11].field_0xa5;
            pUVar6[uVar11].field_0xa9 = 0;
            pUVar6[uVar11].field_0xa4 = (char)uVar13;
            uVar12 = (uint)(byte)pUVar6[uVar11].field_0xa5;
          }
        }
        else {
          uVar12 = uVar11;
          if (bVar1 < 0x12) {
            if ((bVar1 < 0xe) || (bVar1 < 0x10)) goto LAB_00449d94;
            if (bVar1 == 0x11) {
              FUN_00447b2f();
              uVar12 = extraout_ECX_14;
              uVar13 = extraout_EDX_02;
            }
          }
          else if ((((bVar1 < 0x13) || (bVar1 < 0x17)) || (bVar1 < 0x19)) || (bVar1 == 0x19))
          goto LAB_00449d94;
        }
        pUVar6 = (UnidadeParcial *)(uint)(byte)pUVar16->field_0xab;
        if (pUVar6 == (UnidadeParcial *)0x1) {
          uVar17 = FUN_004237c0(uVar12,uVar13);
          pUVar6 = (UnidadeParcial *)uVar17;
          if ((char)uVar17 == '\0') {
            pUVar6 = (UnidadeParcial *)FUN_00425516(extraout_ECX_15,in_AX);
          }
        }
        goto switchD_0044d86e_default;
      }
      pUVar6 = (UnidadeParcial *)FUN_00442668(0,uStack_2c);
      if ((char)pUVar6 == '\0') goto switchD_0044d86e_default;
      pUVar8 = tabela_unidades + in_AX;
      pUVar8->celula_destino = uStack_2c;
      pUVar6 = pUVar7;
      if (in_AX == DAT_00496304) {
        pUVar6 = (UnidadeParcial *)((uint)pUVar7 & 0xffffff00);
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = 0xffff;
      }
    }
    pUVar8->estado_caminho = 0;
  }
switchD_0044d86e_default:
  return CONCAT44(param_2,pUVar6);
}
