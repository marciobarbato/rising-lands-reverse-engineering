/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044ab60, entrada 0044ab60.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_0044ab60(int param_1,undefined4 param_2)

{
  byte bVar1;
  bool bVar2;
  UnidadeParcial *pUVar3;
  ushort in_AX;
  int iVar4;
  uint uVar5;
  undefined4 uVar6;
  UnidadeParcial *pUVar7;
  undefined4 uVar8;
  char cVar9;
  int extraout_ECX;
  int extraout_ECX_00;
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
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  ushort uVar10;
  UnidadeParcial *pUVar11;
  undefined8 uVar12;
  uint uStack_1c;

  uVar5 = (uint)in_AX;
  pUVar11 = tabela_unidades + uVar5;
  pUVar7 = (UnidadeParcial *)(uint)pUVar11->tipo_id;
  if (pUVar7 != (UnidadeParcial *)0x7) goto switchD_0044d86e_default;
  bVar1 = pUVar11->field_0x89;
  pUVar7 = (UnidadeParcial *)(uint)bVar1;
  if (bVar1 != 0) {
    if (bVar1 == 1) {
      if (pUVar11->direcao_desejada == pUVar11->orientacao_atual) {
        uVar12 = FUN_00447e12(param_1,uVar5);
        uVar12 = FUN_0041c652(extraout_ECX_04,(int)((ulonglong)uVar12 >> 0x20));
        uVar8 = extraout_ECX_05;
        if (((char)uVar12 == '\0') ||
           (uVar12 = FUN_0041a976(extraout_ECX_05,(int)((ulonglong)uVar12 >> 0x20)),
           pUVar7 = tabela_unidades, uVar8 = extraout_ECX_06, (short)uVar12 != 0)) {
          if (pUVar11->field_0x8b != '\0') {
            cVar9 = pUVar11->field_0x8b + -1;
            uVar8 = CONCAT22((short)((uint)uVar8 >> 0x10),CONCAT11(cVar9,(char)uVar8));
            pUVar11->field_0x8b = cVar9;
          }
          pUVar7 = (UnidadeParcial *)(uint)(byte)pUVar11->field_0x8b;
          if ((pUVar7 == (UnidadeParcial *)0x0) &&
             (pUVar7 = (UnidadeParcial *)(uint)pUVar11->quadro_movimento,
             pUVar7 == (UnidadeParcial *)0x2)) {
            uVar5 = FUN_004770ee(uVar8,pUVar11->orientacao_atual);
            FUN_004704dc(extraout_ECX_07,uVar5);
            FUN_0046e44c(0,0,0,0,0);
            uVar12 = FUN_0041a976(extraout_ECX_08,extraout_EDX);
            if ((short)uVar12 == 0) {
              uVar6 = FUN_0041cf59(extraout_ECX_09);
              uVar8 = extraout_ECX_11;
            }
            else {
              uVar6 = FUN_0041cec4();
              uVar8 = extraout_ECX_10;
            }
            pUVar11->field_0x8b = 0x14;
            pUVar3 = tabela_unidades;
            pUVar7 = (UnidadeParcial *)CONCAT31((int3)((uint)uVar6 >> 8),pUVar11->proprietario_id);
            if ((pUVar11->proprietario_id == DAT_00508041) &&
               (pUVar7 = (UnidadeParcial *)FUN_004766f0(uVar8,(uint)DAT_00508041),
               (char)pUVar7 != '\0')) {
              uVar12 = FUN_00440c5d(extraout_ECX_12,extraout_EDX_00);
              pUVar7 = (UnidadeParcial *)uVar12;
              iVar4 = *(int *)&pUVar3[in_AX].field_0x104;
              pUVar3[in_AX].field_0xf9 = 0;
              if (iVar4 == -1) {
                pUVar7 = (UnidadeParcial *)
                         FUN_0048aa79(0,(uint)pUVar3[in_AX].tipo_id << 0x10 | 0x2500,(uint)pUVar7);
              }
            }
          }
        }
        else if ((pUVar11->field_0xbe == '\t') && (*(short *)&pUVar11->field_0xd8 != 0)) {
          pUVar11 = tabela_unidades + uVar5;
          pUVar11->celula_destino = *(ushort *)&pUVar11->field_0xc4;
          if (in_AX == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f3c = 0;
            DAT_004e0f37 = 0;
            DAT_00496304 = 0xffff;
          }
          pUVar11->estado_caminho = 0;
          pUVar11->estado_caminho = 0;
          pUVar11->field_0x89 = 0;
          *(undefined2 *)&pUVar11->field_0xc0 = 0xffff;
          pUVar11->estado = 0xb;
          *(ushort *)&pUVar11->field_0xb2 = *(ushort *)&pUVar11->field_0xc4;
          pUVar7 = pUVar11;
          for (uVar10 = 1; uVar10 < *(ushort *)&pUVar11->field_0xd8; uVar10 = uVar10 + 1) {
            pUVar7 = (UnidadeParcial *)(uint)uVar10;
            *(undefined2 *)(&pUVar11->field_0xc2 + (int)pUVar7 * 2) =
                 *(undefined2 *)(&pUVar11->field_0xc4 + (int)pUVar7 * 2);
          }
          *(ushort *)&pUVar11->field_0xd8 = *(ushort *)&pUVar11->field_0xd8 - 1;
        }
        else {
          if (DAT_00508041 == pUVar11->proprietario_id) {
            uVar5 = (uint)in_AX;
            uVar8 = FUN_004766f0(uVar5,(uint)DAT_00508041);
            if ((char)uVar8 != '\0') {
              uVar12 = FUN_00440c5d(extraout_ECX_13,extraout_EDX_01);
              pUVar7[uVar5].field_0xf9 = 0;
              if (*(int *)&pUVar7[uVar5].field_0x104 == -1) {
                FUN_0048aa79(0,(uint)pUVar7[uVar5].tipo_id << 0x10 | 0x1200,(uint)uVar12);
              }
            }
          }
          pUVar11->field_0xbe = 0xff;
          *(undefined2 *)&pUVar11->field_0xb2 = 0xffff;
          if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
            bVar2 = false;
          }
          else {
            bVar2 = true;
          }
          if ((bVar2) && (tabela_unidades[in_AX].estado = 7, in_AX == DAT_00496304)) {
            DAT_004e0f37 = (byte)in_AX ^ (byte)DAT_00496304;
            DAT_004e0f3c = 0;
            DAT_004e0f36 = 0;
            DAT_00496304 = 0xffff;
          }
          pUVar7 = tabela_unidades + in_AX;
          pUVar7->celula_destino = pUVar7->celula_passo;
          if (in_AX == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = 0xffff;
          }
          pUVar7->estado_caminho = 0;
        }
      }
      else {
        uVar12 = FUN_00448599(param_1,uVar5);
        pUVar7 = (UnidadeParcial *)uVar12;
      }
    }
    goto switchD_0044d86e_default;
  }
  pUVar7 = (UnidadeParcial *)(uint)pUVar11->estado;
  if (pUVar7 == (UnidadeParcial *)0xb) {
    if (((pUVar11->field_0xbe == '\t') || (pUVar11->field_0xbe == '\f')) &&
       ((pUVar11->celula_atual == *(ushort *)&pUVar11->field_0xb2 &&
        ((*(int *)&pUVar11->field_0x83 >> 0x18 == 0 && (*(int *)&pUVar11->field_0x84 >> 0x18 == 0)))
        ))) {
      uVar5 = FUN_0044512e((uint)in_AX,pUVar11->celula_atual);
      pUVar7 = tabela_unidades;
      param_1 = extraout_ECX;
      if ((uVar5 & 0xffff) != 0xffff) {
        tabela_unidades[extraout_ECX].celula_destino = (ushort)uVar5;
        if (in_AX == DAT_00496304) {
          param_1 = 0xffff;
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_004e0f3c = 0;
          DAT_00496304 = 0xffff;
        }
        pUVar7[extraout_ECX].estado_caminho = 0;
      }
    }
    if (((((pUVar11->celula_destino == pUVar11->celula_atual) || (pUVar11->field_0xbe == '\t')) ||
         (pUVar11->field_0xbe == '\f')) &&
        (((pUVar11->field_0xbe != '\t' && (pUVar11->field_0xbe != '\f')) ||
         ((pUVar11->celula_atual != *(ushort *)&pUVar11->field_0xb2 &&
          (uVar8 = FUN_004467a1(param_1,(uint)*(ushort *)&pUVar11->field_0xb2),
          param_1 = extraout_ECX_00, (char)uVar8 != '\0')))))) &&
       ((*(int *)&pUVar11->field_0x83 >> 0x18 == 0 && (*(int *)&pUVar11->field_0x84 >> 0x18 == 0))))
    {
      if ((pUVar11->celula_atual == *(ushort *)&pUVar11->field_0xb2) ||
         (((pUVar11->field_0xbe == '\t' || (pUVar11->field_0xbe == '\f')) &&
          (uVar8 = FUN_004467a1(param_1,(uint)*(ushort *)&pUVar11->field_0xb2), (char)uVar8 != '\0')
          ))) {
        pUVar7 = (UnidadeParcial *)(uint)(byte)pUVar11->field_0xbe;
        if (pUVar7 == (UnidadeParcial *)0xff) goto switchD_0044d86e_default;
        if ((pUVar7 == (UnidadeParcial *)0x9) || (pUVar7 == (UnidadeParcial *)0xc)) {
          uStack_1c = (uint)*(ushort *)&pUVar11->field_0xb2;
        }
        else {
          iVar4 = FUN_0041aea4();
          uStack_1c = (uint)pUVar11->celula_atual + iVar4;
        }
        uVar5 = FUN_0041fb12(uStack_1c & 0xffff,uStack_1c & 0xffff);
        if ((char)uVar5 != '\0') {
          uVar5 = FUN_0041fea2(extraout_ECX_01,pUVar11->field_0xbe);
          *(short *)&pUVar11->field_0xc0 = (short)uVar5;
          if (*(short *)&pUVar11->field_0xc0 == -1) {
            if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
              pUVar7 = (UnidadeParcial *)0x0;
            }
            else {
              pUVar7 = (UnidadeParcial *)0x1;
            }
            if ((char)pUVar7 != '\0') {
              pUVar7 = (UnidadeParcial *)((uint)in_AX * 0x45);
              tabela_unidades[in_AX].estado = 7;
              if (in_AX == DAT_00496304) {
                DAT_004e0f36 = 0;
                DAT_004e0f37 = 0;
                pUVar7 = (UnidadeParcial *)0x0;
                DAT_00496304 = 0xffff;
                DAT_004e0f3c = 0;
              }
            }
            goto switchD_0044d86e_default;
          }
          pUVar11->field_0x89 = 1;
          pUVar11->field_0x8b = 0x14;
          pUVar11->contador_animacao = 0;
          pUVar7 = (UnidadeParcial *)(uint)(byte)pUVar11->field_0xbe;
          pUVar11->quadro_movimento = 0;
          if (pUVar7 == (UnidadeParcial *)0x11) {
            pUVar11->direcao_desejada = 7;
            goto switchD_0044d86e_default;
          }
          if ((pUVar7 != (UnidadeParcial *)0x9) && (pUVar7 != (UnidadeParcial *)0xc)) {
            pUVar11->direcao_desejada = 3;
            goto switchD_0044d86e_default;
          }
          uVar8 = extraout_ECX_02;
          goto LAB_0044adec;
        }
        pUVar7 = (UnidadeParcial *)(uint)(byte)pUVar11->field_0xbe;
        if (pUVar7 != (UnidadeParcial *)0x9) goto switchD_0044d86e_default;
        if (*(short *)&pUVar11->field_0xd8 != 0) {
          pUVar7 = tabela_unidades + in_AX;
          pUVar7->celula_destino = *(ushort *)&pUVar7->field_0xc4;
          if (in_AX == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = 0xffff;
          }
          pUVar7->estado_caminho = 0;
          pUVar7->estado_caminho = 0;
          pUVar7->field_0x89 = 0;
          *(undefined2 *)&pUVar7->field_0xc0 = 0xffff;
          pUVar7->estado = 0xb;
          *(ushort *)&pUVar7->field_0xb2 = *(ushort *)&pUVar7->field_0xc4;
          for (uVar10 = 1; uVar10 < *(ushort *)&pUVar7->field_0xd8; uVar10 = uVar10 + 1) {
            *(undefined2 *)(&pUVar7->field_0xc2 + (uint)uVar10 * 2) =
                 *(undefined2 *)(&pUVar7->field_0xc4 + (uint)uVar10 * 2);
          }
          *(ushort *)&pUVar7->field_0xd8 = *(ushort *)&pUVar7->field_0xd8 - 1;
          goto switchD_0044d86e_default;
        }
        pUVar11->field_0xbe = 0xff;
        *(undefined2 *)&pUVar11->field_0xb2 = 0xffff;
        *(undefined2 *)&pUVar11->field_0xc0 = 0xffff;
        pUVar11->field_0x89 = 0;
        if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
          pUVar7 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar7 = (UnidadeParcial *)0x1;
        }
        if ((char)pUVar7 != '\0') {
          pUVar7 = (UnidadeParcial *)((uint)in_AX * 0x45);
          tabela_unidades[in_AX].estado = 7;
          if (in_AX == DAT_00496304) {
            pUVar7 = (UnidadeParcial *)((uint)pUVar7 & 0xffffff00);
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = 0xffff;
          }
        }
      }
      else {
        if ((pUVar11->field_0xbe == '\t') && (*(short *)&pUVar11->field_0xd8 != 0)) {
          pUVar7 = tabela_unidades + in_AX;
          pUVar7->celula_destino = *(ushort *)&pUVar7->field_0xc4;
          if (in_AX == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_00496304 = 0xffff;
            DAT_004e0f3c = 0;
          }
          pUVar7->estado_caminho = 0;
          pUVar7->estado_caminho = 0;
          pUVar7->field_0x89 = 0;
          *(undefined2 *)&pUVar7->field_0xc0 = 0xffff;
          pUVar7->estado = 0xb;
          *(ushort *)&pUVar7->field_0xb2 = *(ushort *)&pUVar7->field_0xc4;
          for (uVar10 = 1; uVar10 < *(ushort *)&pUVar7->field_0xd8; uVar10 = uVar10 + 1) {
            *(undefined2 *)(&pUVar7->field_0xc2 + (uint)uVar10 * 2) =
                 *(undefined2 *)(&pUVar7->field_0xc4 + (uint)uVar10 * 2);
          }
          *(ushort *)&pUVar7->field_0xd8 = *(ushort *)&pUVar7->field_0xd8 - 1;
          goto switchD_0044d86e_default;
        }
        pUVar11->field_0xbe = 0xff;
        *(undefined2 *)&pUVar11->field_0xb2 = 0xffff;
        *(undefined2 *)&pUVar11->field_0xc0 = 0xffff;
        pUVar11->field_0x89 = 0;
        if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
          pUVar7 = (UnidadeParcial *)0x0;
        }
        else {
          pUVar7 = (UnidadeParcial *)0x1;
        }
        if ((char)pUVar7 != '\0') {
          pUVar7 = (UnidadeParcial *)((uint)in_AX * 0x45);
          tabela_unidades[in_AX].estado = 7;
          if (in_AX == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f3c = 0;
            pUVar7 = (UnidadeParcial *)0xffff;
            DAT_004e0f37 = 0;
            DAT_00496304 = 0xffff;
          }
        }
      }
      pUVar11->estado_caminho = 0;
      goto switchD_0044d86e_default;
    }
  }
  else {
    if (pUVar7 != (UnidadeParcial *)0xf) goto switchD_0044d86e_default;
    if (((*(int *)&pUVar11->field_0x83 >> 0x18 == 0) && (*(int *)&pUVar11->field_0x84 >> 0x18 == 0))
       && (iVar4 = FUN_0042381f(param_1,(uint)pUVar11->celula_atual), (char)iVar4 != '\0')) {
      pUVar11->field_0x89 = 1;
      pUVar11->field_0x8b = 0x32;
      uStack_1c._0_2_ = FUN_0041aee2();
      uVar8 = extraout_ECX_03;
LAB_0044adec:
      pUVar7 = (UnidadeParcial *)FUN_00477042(uVar8,(ushort)uStack_1c);
      pUVar11->direcao_desejada = (byte)pUVar7;
      goto switchD_0044d86e_default;
    }
  }
  pUVar7 = (UnidadeParcial *)FUN_0044930c();
switchD_0044d86e_default:
  return CONCAT44(param_2,pUVar7);
}
