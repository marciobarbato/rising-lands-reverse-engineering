/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00451914, entrada 00451914.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Removing unreachable block (ram,0x00452b8b) */
/* WARNING: Removing unreachable block (ram,0x00452ba5) */
/* WARNING: Removing unreachable block (ram,0x00452ba9) */
/* WARNING: Removing unreachable block (ram,0x00452bad) */
/* WARNING: Removing unreachable block (ram,0x00452bb1) */
/* WARNING: Removing unreachable block (ram,0x00452ba3) */
/* WARNING: Removing unreachable block (ram,0x00452bbd) */
/* WARNING: Removing unreachable block (ram,0x00452bbf) */
/* WARNING: Removing unreachable block (ram,0x00452bd6) */

undefined8 __fastcall FUN_00451914(uint param_1,undefined4 param_2)

{
  bool bVar1;
  undefined2 uVar2;
  undefined2 uVar3;
  char cVar4;
  short sVar5;
  ushort uVar6;
  uint in_EAX;
  uint3 uVar10;
  uint uVar7;
  undefined4 uVar8;
  int iVar9;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_ECX_01;
  uint extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  int extraout_ECX_05;
  UnidadeParcial *extraout_ECX_06;
  UnidadeParcial *extraout_ECX_07;
  UnidadeParcial *pUVar11;
  undefined4 extraout_ECX_08;
  undefined4 extraout_ECX_09;
  undefined4 extraout_ECX_10;
  uint extraout_ECX_11;
  uint extraout_ECX_12;
  undefined4 extraout_ECX_13;
  undefined4 extraout_ECX_14;
  uint extraout_ECX_15;
  undefined4 extraout_ECX_16;
  uint uVar12;
  uint uVar13;
  UnidadeParcial *pUVar14;
  undefined4 extraout_EDX;
  byte bVar15;
  uint uVar16;
  undefined8 uVar17;
  short local_5c;
  short asStack_48 [2];
  uint local_44;
  short local_40;
  short local_38;
  undefined2 local_36;
  short asStack_34 [2];
  uint local_30;
  uint local_2c;
  undefined4 local_28;
  byte local_24;
  byte local_20;
  char local_1c;

  uVar2 = local_36;
  pUVar14 = tabela_unidades;
  sVar5 = (short)in_EAX;
  uVar12 = in_EAX & 0xffff;
  uVar7 = CONCAT31((int3)(uVar12 * 0x44 >> 8),tabela_unidades[uVar12].field_0x8a);
  local_36 = (undefined2)(in_EAX >> 0x10);
  uVar3 = local_36;
  switch(tabela_unidades[uVar12].field_0x8a) {
  case 0:
    local_36 = uVar2;
    if (((*(int *)&tabela_unidades[uVar12].field_0x83 >> 0x18 != 0) ||
        (*(int *)&tabela_unidades[uVar12].field_0x84 >> 0x18 != 0)) ||
       ((cVar4 = FUN_00446cb5(param_1,tabela_unidades[uVar12].field_0xb7), param_1 = extraout_ECX,
        cVar4 == '\0' ||
        (iVar9 = FUN_004517a2(extraout_ECX,pUVar14[uVar12].field_0xb7), pUVar11 = tabela_unidades,
        param_1 = extraout_ECX_00, (char)iVar9 == '\0')))) {
      if ((*(int *)&pUVar14[uVar12].field_0x83 >> 0x18 == 0) &&
         (*(int *)&pUVar14[uVar12].field_0x84 >> 0x18 == 0)) {
        uVar7 = in_EAX & 0xffff;
        cVar4 = FUN_00446cb5(param_1,pUVar14[uVar12].field_0xb7);
        if (cVar4 == '\0') {
          bVar15 = tabela_unidades[uVar7].field_0xb7;
          uVar16 = 0xffff;
          uVar6 = 0xffff;
          local_38 = sVar5;
          local_36 = uVar3;
          if (bVar15 < 3) {
            if (bVar15 == 1) {
              uVar6 = tabela_unidades[*(ushort *)&tabela_unidades[uVar7].field_0xb8].celula_passo;
            }
          }
          else if (bVar15 < 4) {
            if ((tabela_unidades[uVar7].alcance_quadrado_u8 == 0) ||
               (tabela_unidades[uVar7].alcance_quadrado_u8 == 1)) {
              uVar16 = FUN_004239a0(tabela_unidades,
                                    (uint)tabela_unidades[in_EAX & 0xffff].celula_passo);
            }
            uVar6 = (ushort)uVar16;
            if ((uVar16 & 0xffff) == 0xffff) {
              uVar6 = FUN_0041aee2();
            }
          }
          else if (bVar15 == 5) {
            uVar6 = *(ushort *)&tabela_unidades[uVar7].field_0xb8;
          }
          if (uVar6 == pUVar14[uVar12].celula_destino) goto LAB_00452001;
          pUVar14 = tabela_unidades + (in_EAX & 0xffff);
          pUVar14->celula_destino = uVar6;
          if (sVar5 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
          }
        }
        else {
          local_1c = pUVar14[uVar12].field_0xb7;
          if (((local_1c == '\x01') &&
              (tabela_unidades[*(ushort *)&pUVar14[uVar12].field_0xb8].tipo_id == 0x10)) &&
             (uVar7 = FUN_00479555(tabela_unidades[*(ushort *)&pUVar14[uVar12].field_0xb8].
                                   celula_passo >> 8,tabela_unidades[uVar7].celula_atual / 0x100),
             uVar7 < 5)) {
            bVar1 = false;
          }
          else {
            bVar1 = true;
          }
          if (!bVar1) {
            uVar7 = in_EAX & 0xffff;
            bVar15 = tabela_unidades[uVar7].field_0xb7;
            uVar16 = 0xffff;
            uVar6 = 0xffff;
            pUVar11 = tabela_unidades;
            if (bVar15 < 3) {
              if (bVar15 == 1) {
                uVar6 = tabela_unidades[*(ushort *)&tabela_unidades[uVar7].field_0xb8].celula_passo;
              }
            }
            else if (bVar15 < 4) {
              if ((tabela_unidades[uVar7].alcance_quadrado_u8 == 0) ||
                 (tabela_unidades[uVar7].alcance_quadrado_u8 == 1)) {
                uVar16 = FUN_004239a0(tabela_unidades,
                                      (uint)tabela_unidades[in_EAX & 0xffff].celula_passo);
                pUVar11 = extraout_ECX_06;
              }
              uVar6 = (ushort)uVar16;
              if ((uVar16 & 0xffff) == 0xffff) {
                uVar6 = FUN_0041aee2();
                pUVar11 = extraout_ECX_07;
              }
            }
            else if (bVar15 == 5) {
              uVar6 = *(ushort *)&tabela_unidades[uVar7].field_0xb8;
            }
            if (uVar6 != pUVar14[uVar12].celula_atual) {
              iVar9 = FUN_00477042(pUVar11,pUVar14[uVar12].celula_atual);
              FUN_004770ee(extraout_ECX_08,(byte)iVar9);
              iVar9 = FUN_00477042(extraout_ECX_09,pUVar14[uVar12].celula_atual);
              uVar7 = FUN_004770ee(extraout_ECX_10,(byte)iVar9);
              uVar6 = (ushort)uVar7;
            }
            pUVar11 = tabela_unidades;
            if (uVar6 != pUVar14[uVar12].celula_destino) {
              tabela_unidades[in_EAX & 0xffff].celula_destino = uVar6;
              if (sVar5 == DAT_00496304) {
                DAT_004e0f36 = 0;
                DAT_004e0f37 = 0;
                DAT_00496304 = -1;
                DAT_004e0f3c = 0;
              }
              pUVar11[in_EAX & 0xffff].estado_caminho = 0;
            }
            goto LAB_00452001;
          }
          bVar15 = tabela_unidades[in_EAX & 0xffff].tipo_id;
          uVar10 = (uint3)((in_EAX & 0xffff) * 0x45 >> 8);
          if (bVar15 < 8) {
            if (bVar15 == 4) goto LAB_00452265;
LAB_0045229e:
            uVar7 = (uint)uVar10 << 8;
          }
          else {
            if ((8 < bVar15) &&
               ((bVar15 < 0xc || ((0xc < bVar15 && ((bVar15 < 0x16 || (0x17 < bVar15))))))))
            goto LAB_0045229e;
LAB_00452265:
            uVar7 = CONCAT31(uVar10,1);
          }
          if ((char)uVar7 != '\0') break;
          uVar16 = in_EAX & 0xffff;
          bVar15 = tabela_unidades[uVar16].field_0xb7;
          uVar7 = 0xffff;
          uVar6 = 0xffff;
          if (bVar15 < 3) {
            if (bVar15 == 1) {
              uVar6 = tabela_unidades[*(ushort *)&tabela_unidades[uVar16].field_0xb8].celula_passo;
            }
          }
          else if (bVar15 < 4) {
            if ((tabela_unidades[uVar16].alcance_quadrado_u8 == 0) ||
               (tabela_unidades[uVar16].alcance_quadrado_u8 == 1)) {
              uVar7 = FUN_004239a0(tabela_unidades,
                                   (uint)tabela_unidades[in_EAX & 0xffff].celula_passo);
            }
            uVar6 = (ushort)uVar7;
            if ((uVar7 & 0xffff) == 0xffff) {
              uVar6 = FUN_0041aee2();
            }
          }
          else if (bVar15 == 5) {
            uVar6 = *(ushort *)&tabela_unidades[uVar16].field_0xb8;
          }
          if (uVar6 == pUVar14[uVar12].celula_destino) goto LAB_00452001;
          pUVar14 = tabela_unidades + (in_EAX & 0xffff);
          pUVar14->celula_destino = uVar6;
          if (sVar5 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f3c = 0;
            DAT_004e0f37 = 0;
            DAT_00496304 = -1;
          }
        }
        pUVar14->estado_caminho = 0;
      }
LAB_00452001:
      uVar7 = FUN_0044930c();
      break;
    }
    local_28 = CONCAT22((short)((in_EAX & 0xffff) * 0x45 >> 0x10),
                        tabela_unidades[in_EAX & 0xffff].celula_passo);
    tabela_unidades[in_EAX & 0xffff].celula_destino = tabela_unidades[in_EAX & 0xffff].celula_passo;
    if (sVar5 == DAT_00496304) {
      DAT_004e0f36 = 0;
      DAT_004e0f37 = 0;
      DAT_004e0f3c = 0;
      DAT_00496304 = -1;
    }
    uVar13 = in_EAX & 0xffff;
    pUVar11[in_EAX & 0xffff].estado_caminho = 0;
    bVar15 = tabela_unidades[uVar13].field_0xb7;
    uVar16 = 0xffff;
    uVar7 = extraout_ECX_00;
    if (bVar15 < 3) {
      if (bVar15 == 1) {
        uVar16 = (uint)tabela_unidades[*(ushort *)&tabela_unidades[uVar13].field_0xb8].celula_passo;
      }
    }
    else if (bVar15 < 4) {
      if ((tabela_unidades[uVar13].alcance_quadrado_u8 == 0) ||
         (tabela_unidades[uVar13].alcance_quadrado_u8 == 1)) {
        uVar16 = FUN_004239a0(extraout_ECX_00,(uint)tabela_unidades[in_EAX & 0xffff].celula_passo);
        uVar7 = extraout_ECX_01;
      }
      if ((uVar16 & 0xffff) == 0xffff) {
        uVar16 = FUN_0041aee2();
        uVar7 = extraout_ECX_02;
      }
    }
    else if (bVar15 == 5) {
      uVar16 = (uint)*(ushort *)&tabela_unidades[uVar13].field_0xb8;
    }
    pUVar11 = tabela_unidades;
    bVar15 = tabela_unidades[in_EAX & 0xffff].tipo_id;
    if ((bVar15 < 0xc) || ((0xc < bVar15 && (bVar15 != 0xf)))) {
      bVar1 = false;
    }
    else {
      bVar1 = true;
    }
    if (bVar1) {
      local_30 = CONCAT22((short)((in_EAX & 0xffff) * 0x114 >> 0x10),
                          *(ushort *)&pUVar14[uVar12].field_0xb8);
      bVar15 = pUVar14[uVar12].field_0xb7;
      if (bVar15 < 3) {
        if (bVar15 == 1) {
          uVar7 = (uint)tabela_unidades[*(ushort *)&pUVar14[uVar12].field_0xb8].celula_passo;
        }
      }
      else if (bVar15 < 4) {
        uVar7 = FUN_0041aee2();
      }
      else if (bVar15 == 5) {
        uVar7 = local_30;
      }
      iVar9 = FUN_004796cb((uVar7 & 0xffff) >> 8,
                           (int)(uint)pUVar11[in_EAX & 0xffff].celula_atual >> 8,0x20);
      pUVar14[uVar12].field_0xda = (char)iVar9;
      uVar8 = extraout_ECX_04;
    }
    else {
      iVar9 = FUN_004796cb((uVar16 & 0xffff) >> 8,(int)(uint)pUVar14[uVar12].celula_atual >> 8,8);
      pUVar14[uVar12].direcao_desejada = (char)iVar9 * '\x02' - 1;
      uVar8 = extraout_ECX_03;
      if (pUVar14[uVar12].tipo_id == 3) {
        pUVar14[uVar12].direcao_desejada =
             (char)((pUVar14[uVar12].direcao_desejada + 0xb) % 0x10) + 1;
      }
    }
    pUVar11 = tabela_unidades;
    bVar15 = tabela_unidades[in_EAX & 0xffff].tipo_id;
    if ((bVar15 < 0xc) || ((0xc < bVar15 && (bVar15 != 0xf)))) {
      bVar1 = false;
    }
    else {
      bVar1 = true;
    }
    if ((!bVar1) && (pUVar14[uVar12].orientacao_atual != pUVar14[uVar12].direcao_desejada)) {
      uVar17 = FUN_00448599(uVar8,tabela_unidades);
      uVar7 = (uint)uVar17;
      break;
    }
    bVar15 = tabela_unidades[in_EAX & 0xffff].tipo_id;
    if ((bVar15 < 0xc) || ((0xc < bVar15 && (bVar15 != 0xf)))) {
      bVar1 = false;
    }
    else {
      bVar1 = true;
    }
    if ((bVar1) && (pUVar14[uVar12].field_0x94 != pUVar14[uVar12].field_0xda)) {
      uVar7 = FUN_004484a7();
      break;
    }
    uVar7 = FUN_00428cc0((uint)*(ushort *)
                                (&DAT_004965de +
                                (uint)tabela_unidades[in_EAX & 0xffff].tipo_id * 0x32),3);
    bVar1 = (int)(extraout_ECX_05 - (uVar7 & 0xffff)) <=
            (int)(uint)pUVar11[in_EAX & 0xffff].contador_recarga;
    uVar7 = (uint)CONCAT11((char)(pUVar11[in_EAX & 0xffff].contador_recarga >> 8),bVar1);
    if (!bVar1) break;
    pUVar14[uVar12].contador_recarga = 0;
    pUVar14[uVar12].field_0x8a = 1;
    if (pUVar14[uVar12].tipo_id != 0x10) {
      pUVar14[uVar12].quadro_movimento = 0;
      pUVar14[uVar12].contador_animacao = 0;
    }
    bVar15 = tabela_unidades[in_EAX & 0xffff].tipo_id;
    uVar10 = (uint3)((in_EAX & 0xffff) * 0x45 >> 8);
    if ((bVar15 < 0xe) || ((0xe < bVar15 && (bVar15 != 0x10)))) {
      uVar7 = (uint)uVar10 << 8;
    }
    else {
      uVar7 = CONCAT31(uVar10,1);
    }
    if ((char)uVar7 == '\0') break;
    goto LAB_00451e51;
  case 1:
    FUN_004479c4(param_1,uVar12);
    if ((pUVar14[uVar12].contador_animacao == 0) &&
       (pUVar14[uVar12].quadro_movimento == pUVar14[uVar12].field_0x7a)) {
      bVar15 = tabela_unidades[uVar12].field_0xb7;
      local_44 = 0xffff;
      uVar7 = in_EAX;
      if (bVar15 < 3) {
        if (bVar15 == 1) {
          local_44 = CONCAT22((short)((uint)*(ushort *)&tabela_unidades[uVar12].field_0xb8 * 0x45 >>
                                     0x10),
                              tabela_unidades[*(ushort *)&tabela_unidades[uVar12].field_0xb8].
                              celula_passo);
        }
      }
      else if (bVar15 < 4) {
        if ((tabela_unidades[uVar12].alcance_quadrado_u8 == 0) ||
           (tabela_unidades[uVar12].alcance_quadrado_u8 == 1)) {
          local_44 = FUN_004239a0(in_EAX,(uint)tabela_unidades[in_EAX & 0xffff].celula_passo);
          uVar7 = extraout_ECX_11;
        }
        if ((local_44 & 0xffff) == 0xffff) {
          local_44 = FUN_0041aee2();
          uVar7 = extraout_ECX_12;
        }
      }
      else if (bVar15 == 5) {
        local_44 = (uint)*(ushort *)&tabela_unidades[uVar12].field_0xb8;
      }
      pUVar11 = tabela_unidades;
      bVar15 = pUVar14[uVar12].estado;
      if (bVar15 != 0) {
        if (bVar15 < 2) {
          uVar16 = in_EAX & 0xffff;
          uVar8 = FUN_004766f0(uVar7,(uint)DAT_00508041);
          if ((char)uVar8 != '\0') {
            uVar17 = FUN_00440c5d(extraout_ECX_13,extraout_EDX);
            pUVar11[uVar16].field_0xf9 = 0;
            if (*(int *)&pUVar11[uVar16].field_0x104 == -1) {
              FUN_0048aa79(0,(uint)pUVar11[uVar16].tipo_id << 0x10 | 0x2300,(uint)uVar17);
            }
          }
          bVar15 = tabela_unidades[in_EAX & 0xffff].tipo_id;
          if ((bVar15 < 0xe) || ((0xe < bVar15 && (bVar15 != 0x10)))) {
            bVar1 = false;
          }
          else {
            bVar1 = true;
          }
          if (bVar1) {
            if (tabela_unidades[in_EAX & 0xffff].field_0xda != '\0') {
              tabela_unidades[in_EAX & 0xffff].field_0xda =
                   tabela_unidades[in_EAX & 0xffff].field_0xda + -1;
            }
          }
          if (pUVar14[uVar12].field_0x78 == '\0') {
            switch(tabela_unidades[in_EAX & 0xffff].tipo_id) {
            case 0:
            case 1:
            case 2:
            case 4:
            case 5:
            case 6:
            case 7:
            case 8:
            case 9:
            case 10:
            case 0x11:
            case 0x12:
            case 0x13:
            case 0x14:
            case 0x15:
            case 0x16:
            case 0x17:
            case 0x18:
              local_5c = 1;
              local_40 = 1;
              break;
            case 3:
            case 0xb:
            case 0xc:
            case 0xd:
            case 0xe:
            case 0xf:
            case 0x10:
            case 0x19:
              local_5c = 2;
              local_40 = 2;
            }
            if ((local_5c == 2) && (local_40 == 2)) {
              uVar7 = in_EAX & 0xffff;
              bVar15 = tabela_unidades[uVar7].field_0xb7;
              local_2c = 0xffff;
              if (bVar15 < 3) {
                if (bVar15 == 1) {
                  local_2c = CONCAT22((short)((uint)*(ushort *)&tabela_unidades[uVar7].field_0xb8 *
                                              0x45 >> 0x10),
                                      tabela_unidades[*(ushort *)&tabela_unidades[uVar7].field_0xb8]
                                      .celula_passo);
                }
              }
              else if (bVar15 < 4) {
                if ((tabela_unidades[uVar7].alcance_quadrado_u8 == 0) ||
                   (tabela_unidades[uVar7].alcance_quadrado_u8 == 1)) {
                  local_2c = FUN_004239a0(tabela_unidades,
                                          (uint)tabela_unidades[in_EAX & 0xffff].celula_passo);
                }
                if ((local_2c & 0xffff) == 0xffff) {
                  local_2c = FUN_0041aee2();
                }
              }
              else if (bVar15 == 5) {
                local_2c = (uint)*(ushort *)&tabela_unidades[uVar7].field_0xb8;
              }
            }
            else {
              local_2c = FUN_004770ee(tabela_unidades,pUVar14[uVar12].orientacao_atual);
            }
            if (pUVar14[uVar12].tipo_id == 0x10) {
              FUN_0046e44c(in_EAX & 0xffff,0,0,0,0);
            }
            FUN_00450874(0,1,'\0');
          }
          else {
            uVar7 = in_EAX & 0xffff;
            asStack_48[0] = 0;
            asStack_34[0] = 0;
            local_24 = tabela_unidades[uVar7].tipo_id;
            if (((local_24 != 1) && (local_24 != 0x15)) && (local_24 != 0xb)) {
              if ((local_24 < 0xc) || ((0xc < local_24 && (local_24 != 0xf)))) {
                bVar1 = false;
              }
              else {
                bVar1 = true;
              }
              if (bVar1) {
                bVar15 = tabela_unidades[uVar7].field_0x94;
              }
              else {
                bVar15 = tabela_unidades[uVar7].orientacao_atual;
              }
              FUN_004511a5(asStack_34,bVar15);
              FUN_00410fcc(extraout_ECX_14,asStack_48);
            }
            local_20 = pUVar14[uVar12].orientacao_atual;
            if (pUVar14[uVar12].tipo_id == 0xb) {
              iVar9 = FUN_004796cb((local_44 & 0xffff) >> 8,pUVar14[uVar12].celula_atual / 0x100,
                                   0x20);
              local_20 = (byte)iVar9;
            }
            if ((pUVar14[uVar12].tipo_id != 3) && (pUVar14[uVar12].tipo_id != 0x19)) {
              uVar8 = 0;
              if (pUVar14[uVar12].field_0xb7 == '\x01') {
                if ((tabela_unidades[*(ushort *)&pUVar14[uVar12].field_0xb8].tipo_id < 0x10) ||
                   (0x11 < tabela_unidades[*(ushort *)&pUVar14[uVar12].field_0xb8].tipo_id)) {
                  bVar1 = false;
                }
                else {
                  bVar1 = true;
                }
                if (bVar1) {
                  uVar8 = 1;
                }
              }
              FUN_0046e44c(in_EAX & 0xffff,local_20,(int)asStack_48[0],(int)asStack_34[0],uVar8);
            }
            bVar15 = pUVar14[uVar12].tipo_id;
            if (((bVar15 == 0xb) || (bVar15 == 3)) || (bVar15 == 0x19)) {
              FUN_0046e44c(in_EAX & 0xffff,local_20,0,0,0);
            }
          }
        }
        else if (bVar15 == 0x18) {
          FUN_00473510(uVar7,(uint)(byte)pUVar14[uVar12].field_0xf4);
          FUN_0044357c();
        }
      }
    }
    uVar7 = (uint)pUVar14[uVar12].contador_animacao;
    if ((uVar7 == 0) && (uVar7 = (uint)pUVar14[uVar12].quadro_movimento, uVar7 == 0)) {
      if (pUVar14[uVar12].field_0x8b == '\0') {
        pUVar14[uVar12].field_0x8a = 0;
        uVar7 = (uint)pUVar14[uVar12].tipo_id;
        if (uVar7 != 0x10) {
          pUVar14[uVar12].quadro_movimento = 0;
        }
        pUVar14[uVar12].contador_recarga = 0;
      }
      else {
        uVar7 = (uint)pUVar14[uVar12].tipo_id;
        pUVar14[uVar12].field_0x8b = pUVar14[uVar12].field_0x8b + -1;
        if (uVar7 == 3) {
          pUVar14[uVar12].quadro_movimento = 5;
        }
        else if (uVar7 == 0xb) {
          pUVar14[uVar12].quadro_movimento = 0;
        }
      }
    }
    break;
  case 2:
    bVar15 = tabela_unidades[uVar12].tipo_id;
    if (0xf < bVar15) {
      if (bVar15 < 0x11) {
        bVar15 = tabela_unidades[uVar12].contador_animacao + 1;
        pUVar11 = tabela_unidades + uVar12;
        tabela_unidades[uVar12].contador_animacao = bVar15;
        if (bVar15 == pUVar11->periodo_animacao) {
          pUVar14[uVar12].contador_animacao = 0;
          pUVar14[uVar12].quadro_movimento =
               (byte)((pUVar14[uVar12].quadro_movimento + 1) %
                     (uint)pUVar14[uVar12].quantidade_quadros_movimento);
        }
      }
      else if (bVar15 == 0x11) {
        FUN_00447b2f();
        param_1 = extraout_ECX_15;
      }
    }
    if ((pUVar14[uVar12].field_0x8b == '\x01') && (pUVar14[uVar12].tipo_id != 0x10)) {
      pUVar14[uVar12].quadro_movimento = 0;
      pUVar14[uVar12].contador_animacao = 0;
    }
    bVar15 = pUVar14[uVar12].field_0x8b - 1;
    uVar7 = (uint)bVar15;
    pUVar14[uVar12].field_0x8b = bVar15;
    if (bVar15 != 0) break;
    pUVar14[uVar12].field_0x8a = 1;
    if (pUVar14[uVar12].tipo_id != 0x10) {
      pUVar14[uVar12].quadro_movimento = 0;
      pUVar14[uVar12].contador_animacao = 0;
    }
    bVar15 = tabela_unidades[in_EAX & 0xffff].tipo_id;
    if ((bVar15 < 0xe) || ((0xe < bVar15 && (bVar15 != 0x10)))) {
      bVar1 = false;
    }
    else {
      bVar1 = true;
    }
    if (!bVar1) {
      uVar17 = FUN_00446cb5(param_1,pUVar14[uVar12].field_0xb7);
      uVar7 = (uint)uVar17;
      if ((char)uVar17 != '\0') {
        uVar17 = FUN_00451464(extraout_ECX_16,(int)((ulonglong)uVar17 >> 0x20));
        uVar7 = (uint)uVar17;
        if ((char)uVar17 != '\0') break;
      }
      pUVar14[uVar12].field_0x8a = 0;
      break;
    }
LAB_00451e51:
    uVar7 = (uint)(byte)tabela_unidades[in_EAX & 0xffff].field_0xda;
    if (uVar7 == 0) {
      uVar7 = FUN_004457d3();
    }
    break;
  case 3:
    if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
       (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
      uVar7 = 0;
    }
    else {
      uVar7 = 1;
    }
    if ((char)uVar7 != '\0') {
      uVar7 = (in_EAX & 0xffff) * 0x45;
      tabela_unidades[in_EAX & 0xffff].estado = 7;
      if (sVar5 == DAT_00496304) {
        uVar7 = CONCAT22((short)(uVar7 >> 0x10),(ushort)(byte)uVar7);
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = -1;
      }
    }
    *(undefined2 *)&pUVar14[uVar12].field_0xb8 = 0xffff;
    pUVar14[uVar12].quadro_movimento = 0;
    pUVar14[uVar12].contador_animacao = 0;
  }
  return CONCAT44(param_2,uVar7);
}
