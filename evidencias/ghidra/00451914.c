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
  short sVar4;
  ushort uVar5;
  uint in_EAX;
  uint3 uVar9;
  uint uVar6;
  undefined4 uVar7;
  int iVar8;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_ECX_01;
  uint extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  int extraout_ECX_05;
  UnidadeParcial *extraout_ECX_06;
  UnidadeParcial *extraout_ECX_07;
  UnidadeParcial *pUVar10;
  undefined4 extraout_ECX_08;
  undefined4 extraout_ECX_09;
  undefined4 extraout_ECX_10;
  uint extraout_ECX_11;
  uint extraout_ECX_12;
  undefined4 extraout_ECX_13;
  undefined4 extraout_ECX_14;
  uint extraout_ECX_15;
  undefined4 extraout_ECX_16;
  char cVar14;
  uint uVar11;
  uint uVar12;
  UnidadeParcial *pUVar13;
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
  undefined1 local_20;
  char local_1c;

  uVar2 = local_36;
  pUVar13 = tabela_unidades;
  sVar4 = (short)in_EAX;
  uVar11 = in_EAX & 0xffff;
  uVar6 = CONCAT31((int3)(uVar11 * 0x44 >> 8),tabela_unidades[uVar11].field_0x8a);
  local_36 = (undefined2)(in_EAX >> 0x10);
  uVar3 = local_36;
  switch(tabela_unidades[uVar11].field_0x8a) {
  case 0:
    local_36 = uVar2;
    if (((*(int *)&tabela_unidades[uVar11].field_0x83 >> 0x18 != 0) ||
        (*(int *)&tabela_unidades[uVar11].field_0x84 >> 0x18 != 0)) ||
       ((cVar14 = FUN_00446cb5(param_1,tabela_unidades[uVar11].field_0xb7), param_1 = extraout_ECX,
        cVar14 == '\0' ||
        (iVar8 = FUN_004517a2(extraout_ECX,pUVar13[uVar11].field_0xb7), pUVar10 = tabela_unidades,
        param_1 = extraout_ECX_00, (char)iVar8 == '\0')))) {
      if ((*(int *)&pUVar13[uVar11].field_0x83 >> 0x18 == 0) &&
         (*(int *)&pUVar13[uVar11].field_0x84 >> 0x18 == 0)) {
        uVar6 = in_EAX & 0xffff;
        cVar14 = FUN_00446cb5(param_1,pUVar13[uVar11].field_0xb7);
        if (cVar14 == '\0') {
          bVar15 = tabela_unidades[uVar6].field_0xb7;
          uVar16 = 0xffff;
          uVar5 = 0xffff;
          local_38 = sVar4;
          local_36 = uVar3;
          if (bVar15 < 3) {
            if (bVar15 == 1) {
              uVar5 = tabela_unidades[*(ushort *)&tabela_unidades[uVar6].field_0xb8].celula_passo;
            }
          }
          else if (bVar15 < 4) {
            if ((tabela_unidades[uVar6].alcance_quadrado_u8 == 0) ||
               (tabela_unidades[uVar6].alcance_quadrado_u8 == 1)) {
              uVar16 = FUN_004239a0(tabela_unidades,
                                    (uint)tabela_unidades[in_EAX & 0xffff].celula_passo);
            }
            uVar5 = (ushort)uVar16;
            if ((uVar16 & 0xffff) == 0xffff) {
              uVar5 = FUN_0041aee2();
            }
          }
          else if (bVar15 == 5) {
            uVar5 = *(ushort *)&tabela_unidades[uVar6].field_0xb8;
          }
          if (uVar5 == pUVar13[uVar11].celula_destino) goto LAB_00452001;
          pUVar13 = tabela_unidades + (in_EAX & 0xffff);
          pUVar13->celula_destino = uVar5;
          if (sVar4 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
          }
        }
        else {
          local_1c = pUVar13[uVar11].field_0xb7;
          if (((local_1c == '\x01') &&
              (tabela_unidades[*(ushort *)&pUVar13[uVar11].field_0xb8].tipo_id == 0x10)) &&
             (uVar6 = FUN_00479555(tabela_unidades[*(ushort *)&pUVar13[uVar11].field_0xb8].
                                   celula_passo >> 8,tabela_unidades[uVar6].celula_atual / 0x100),
             uVar6 < 5)) {
            bVar1 = false;
          }
          else {
            bVar1 = true;
          }
          if (!bVar1) {
            uVar6 = in_EAX & 0xffff;
            bVar15 = tabela_unidades[uVar6].field_0xb7;
            uVar16 = 0xffff;
            uVar5 = 0xffff;
            pUVar10 = tabela_unidades;
            if (bVar15 < 3) {
              if (bVar15 == 1) {
                uVar5 = tabela_unidades[*(ushort *)&tabela_unidades[uVar6].field_0xb8].celula_passo;
              }
            }
            else if (bVar15 < 4) {
              if ((tabela_unidades[uVar6].alcance_quadrado_u8 == 0) ||
                 (tabela_unidades[uVar6].alcance_quadrado_u8 == 1)) {
                uVar16 = FUN_004239a0(tabela_unidades,
                                      (uint)tabela_unidades[in_EAX & 0xffff].celula_passo);
                pUVar10 = extraout_ECX_06;
              }
              uVar5 = (ushort)uVar16;
              if ((uVar16 & 0xffff) == 0xffff) {
                uVar5 = FUN_0041aee2();
                pUVar10 = extraout_ECX_07;
              }
            }
            else if (bVar15 == 5) {
              uVar5 = *(ushort *)&tabela_unidades[uVar6].field_0xb8;
            }
            if (uVar5 != pUVar13[uVar11].celula_atual) {
              iVar8 = FUN_00477042(pUVar10,pUVar13[uVar11].celula_atual);
              FUN_004770ee(extraout_ECX_08,(byte)iVar8);
              iVar8 = FUN_00477042(extraout_ECX_09,pUVar13[uVar11].celula_atual);
              uVar6 = FUN_004770ee(extraout_ECX_10,(byte)iVar8);
              uVar5 = (ushort)uVar6;
            }
            pUVar10 = tabela_unidades;
            if (uVar5 != pUVar13[uVar11].celula_destino) {
              tabela_unidades[in_EAX & 0xffff].celula_destino = uVar5;
              if (sVar4 == DAT_00496304) {
                DAT_004e0f36 = 0;
                DAT_004e0f37 = 0;
                DAT_00496304 = -1;
                DAT_004e0f3c = 0;
              }
              pUVar10[in_EAX & 0xffff].estado_caminho = 0;
            }
            goto LAB_00452001;
          }
          bVar15 = tabela_unidades[in_EAX & 0xffff].tipo_id;
          uVar9 = (uint3)((in_EAX & 0xffff) * 0x45 >> 8);
          if (bVar15 < 8) {
            if (bVar15 == 4) goto LAB_00452265;
LAB_0045229e:
            uVar6 = (uint)uVar9 << 8;
          }
          else {
            if ((8 < bVar15) &&
               ((bVar15 < 0xc || ((0xc < bVar15 && ((bVar15 < 0x16 || (0x17 < bVar15))))))))
            goto LAB_0045229e;
LAB_00452265:
            uVar6 = CONCAT31(uVar9,1);
          }
          if ((char)uVar6 != '\0') break;
          uVar16 = in_EAX & 0xffff;
          bVar15 = tabela_unidades[uVar16].field_0xb7;
          uVar6 = 0xffff;
          uVar5 = 0xffff;
          if (bVar15 < 3) {
            if (bVar15 == 1) {
              uVar5 = tabela_unidades[*(ushort *)&tabela_unidades[uVar16].field_0xb8].celula_passo;
            }
          }
          else if (bVar15 < 4) {
            if ((tabela_unidades[uVar16].alcance_quadrado_u8 == 0) ||
               (tabela_unidades[uVar16].alcance_quadrado_u8 == 1)) {
              uVar6 = FUN_004239a0(tabela_unidades,
                                   (uint)tabela_unidades[in_EAX & 0xffff].celula_passo);
            }
            uVar5 = (ushort)uVar6;
            if ((uVar6 & 0xffff) == 0xffff) {
              uVar5 = FUN_0041aee2();
            }
          }
          else if (bVar15 == 5) {
            uVar5 = *(ushort *)&tabela_unidades[uVar16].field_0xb8;
          }
          if (uVar5 == pUVar13[uVar11].celula_destino) goto LAB_00452001;
          pUVar13 = tabela_unidades + (in_EAX & 0xffff);
          pUVar13->celula_destino = uVar5;
          if (sVar4 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f3c = 0;
            DAT_004e0f37 = 0;
            DAT_00496304 = -1;
          }
        }
        pUVar13->estado_caminho = 0;
      }
LAB_00452001:
      uVar6 = FUN_0044930c();
      break;
    }
    local_28 = CONCAT22((short)((in_EAX & 0xffff) * 0x45 >> 0x10),
                        tabela_unidades[in_EAX & 0xffff].celula_passo);
    tabela_unidades[in_EAX & 0xffff].celula_destino = tabela_unidades[in_EAX & 0xffff].celula_passo;
    if (sVar4 == DAT_00496304) {
      DAT_004e0f36 = 0;
      DAT_004e0f37 = 0;
      DAT_004e0f3c = 0;
      DAT_00496304 = -1;
    }
    uVar12 = in_EAX & 0xffff;
    pUVar10[in_EAX & 0xffff].estado_caminho = 0;
    bVar15 = tabela_unidades[uVar12].field_0xb7;
    uVar16 = 0xffff;
    uVar6 = extraout_ECX_00;
    if (bVar15 < 3) {
      if (bVar15 == 1) {
        uVar16 = (uint)tabela_unidades[*(ushort *)&tabela_unidades[uVar12].field_0xb8].celula_passo;
      }
    }
    else if (bVar15 < 4) {
      if ((tabela_unidades[uVar12].alcance_quadrado_u8 == 0) ||
         (tabela_unidades[uVar12].alcance_quadrado_u8 == 1)) {
        uVar16 = FUN_004239a0(extraout_ECX_00,(uint)tabela_unidades[in_EAX & 0xffff].celula_passo);
        uVar6 = extraout_ECX_01;
      }
      if ((uVar16 & 0xffff) == 0xffff) {
        uVar16 = FUN_0041aee2();
        uVar6 = extraout_ECX_02;
      }
    }
    else if (bVar15 == 5) {
      uVar16 = (uint)*(ushort *)&tabela_unidades[uVar12].field_0xb8;
    }
    pUVar10 = tabela_unidades;
    bVar15 = tabela_unidades[in_EAX & 0xffff].tipo_id;
    if ((bVar15 < 0xc) || ((0xc < bVar15 && (bVar15 != 0xf)))) {
      bVar1 = false;
    }
    else {
      bVar1 = true;
    }
    if (bVar1) {
      local_30 = CONCAT22((short)((in_EAX & 0xffff) * 0x114 >> 0x10),
                          *(ushort *)&pUVar13[uVar11].field_0xb8);
      bVar15 = pUVar13[uVar11].field_0xb7;
      if (bVar15 < 3) {
        if (bVar15 == 1) {
          uVar6 = (uint)tabela_unidades[*(ushort *)&pUVar13[uVar11].field_0xb8].celula_passo;
        }
      }
      else if (bVar15 < 4) {
        uVar6 = FUN_0041aee2();
      }
      else if (bVar15 == 5) {
        uVar6 = local_30;
      }
      iVar8 = FUN_004796cb((uVar6 & 0xffff) >> 8,
                           (int)(uint)pUVar10[in_EAX & 0xffff].celula_atual >> 8,0x20);
      pUVar13[uVar11].field_0xda = (char)iVar8;
      uVar7 = extraout_ECX_04;
    }
    else {
      iVar8 = FUN_004796cb((uVar16 & 0xffff) >> 8,(int)(uint)pUVar13[uVar11].celula_atual >> 8,8);
      pUVar13[uVar11].field_0x90 = (char)iVar8 * '\x02' + -1;
      uVar7 = extraout_ECX_03;
      if (pUVar13[uVar11].tipo_id == 3) {
        pUVar13[uVar11].field_0x90 =
             (char)(((byte)pUVar13[uVar11].field_0x90 + 0xb) % 0x10) + '\x01';
      }
    }
    pUVar10 = tabela_unidades;
    bVar15 = tabela_unidades[in_EAX & 0xffff].tipo_id;
    if ((bVar15 < 0xc) || ((0xc < bVar15 && (bVar15 != 0xf)))) {
      bVar1 = false;
    }
    else {
      bVar1 = true;
    }
    if ((!bVar1) && (pUVar13[uVar11].field_0x91 != pUVar13[uVar11].field_0x90)) {
      uVar17 = FUN_00448599(uVar7,tabela_unidades);
      uVar6 = (uint)uVar17;
      break;
    }
    bVar15 = tabela_unidades[in_EAX & 0xffff].tipo_id;
    if ((bVar15 < 0xc) || ((0xc < bVar15 && (bVar15 != 0xf)))) {
      bVar1 = false;
    }
    else {
      bVar1 = true;
    }
    if ((bVar1) && (pUVar13[uVar11].field_0x94 != pUVar13[uVar11].field_0xda)) {
      uVar6 = FUN_004484a7();
      break;
    }
    uVar6 = FUN_00428cc0((uint)*(ushort *)
                                (&DAT_004965de +
                                (uint)tabela_unidades[in_EAX & 0xffff].tipo_id * 0x32),3);
    bVar1 = (int)(extraout_ECX_05 - (uVar6 & 0xffff)) <=
            (int)(uint)pUVar10[in_EAX & 0xffff].contador_recarga;
    uVar6 = (uint)CONCAT11((char)(pUVar10[in_EAX & 0xffff].contador_recarga >> 8),bVar1);
    if (!bVar1) break;
    pUVar13[uVar11].contador_recarga = 0;
    pUVar13[uVar11].field_0x8a = 1;
    if (pUVar13[uVar11].tipo_id != 0x10) {
      pUVar13[uVar11].field_0xa4 = 0;
      pUVar13[uVar11].field_0xa9 = 0;
    }
    bVar15 = tabela_unidades[in_EAX & 0xffff].tipo_id;
    uVar9 = (uint3)((in_EAX & 0xffff) * 0x45 >> 8);
    if ((bVar15 < 0xe) || ((0xe < bVar15 && (bVar15 != 0x10)))) {
      uVar6 = (uint)uVar9 << 8;
    }
    else {
      uVar6 = CONCAT31(uVar9,1);
    }
    if ((char)uVar6 == '\0') break;
    goto LAB_00451e51;
  case 1:
    FUN_004479c4(param_1,uVar11);
    if ((pUVar13[uVar11].field_0xa9 == '\0') &&
       (pUVar13[uVar11].field_0xa4 == pUVar13[uVar11].field_0x7a)) {
      bVar15 = tabela_unidades[uVar11].field_0xb7;
      local_44 = 0xffff;
      uVar6 = in_EAX;
      if (bVar15 < 3) {
        if (bVar15 == 1) {
          local_44 = CONCAT22((short)((uint)*(ushort *)&tabela_unidades[uVar11].field_0xb8 * 0x45 >>
                                     0x10),
                              tabela_unidades[*(ushort *)&tabela_unidades[uVar11].field_0xb8].
                              celula_passo);
        }
      }
      else if (bVar15 < 4) {
        if ((tabela_unidades[uVar11].alcance_quadrado_u8 == 0) ||
           (tabela_unidades[uVar11].alcance_quadrado_u8 == 1)) {
          local_44 = FUN_004239a0(in_EAX,(uint)tabela_unidades[in_EAX & 0xffff].celula_passo);
          uVar6 = extraout_ECX_11;
        }
        if ((local_44 & 0xffff) == 0xffff) {
          local_44 = FUN_0041aee2();
          uVar6 = extraout_ECX_12;
        }
      }
      else if (bVar15 == 5) {
        local_44 = (uint)*(ushort *)&tabela_unidades[uVar11].field_0xb8;
      }
      pUVar10 = tabela_unidades;
      bVar15 = pUVar13[uVar11].estado;
      if (bVar15 != 0) {
        if (bVar15 < 2) {
          uVar16 = in_EAX & 0xffff;
          uVar7 = FUN_004766f0(uVar6,(uint)DAT_00508041);
          if ((char)uVar7 != '\0') {
            uVar17 = FUN_00440c5d(extraout_ECX_13,extraout_EDX);
            pUVar10[uVar16].field_0xf9 = 0;
            if (*(int *)&pUVar10[uVar16].field_0x104 == -1) {
              FUN_0048aa79(0,(uint)pUVar10[uVar16].tipo_id << 0x10 | 0x2300,(uint)uVar17);
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
          if (pUVar13[uVar11].field_0x78 == '\0') {
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
              uVar6 = in_EAX & 0xffff;
              bVar15 = tabela_unidades[uVar6].field_0xb7;
              local_2c = 0xffff;
              if (bVar15 < 3) {
                if (bVar15 == 1) {
                  local_2c = CONCAT22((short)((uint)*(ushort *)&tabela_unidades[uVar6].field_0xb8 *
                                              0x45 >> 0x10),
                                      tabela_unidades[*(ushort *)&tabela_unidades[uVar6].field_0xb8]
                                      .celula_passo);
                }
              }
              else if (bVar15 < 4) {
                if ((tabela_unidades[uVar6].alcance_quadrado_u8 == 0) ||
                   (tabela_unidades[uVar6].alcance_quadrado_u8 == 1)) {
                  local_2c = FUN_004239a0(tabela_unidades,
                                          (uint)tabela_unidades[in_EAX & 0xffff].celula_passo);
                }
                if ((local_2c & 0xffff) == 0xffff) {
                  local_2c = FUN_0041aee2();
                }
              }
              else if (bVar15 == 5) {
                local_2c = (uint)*(ushort *)&tabela_unidades[uVar6].field_0xb8;
              }
            }
            else {
              local_2c = FUN_004770ee(tabela_unidades,pUVar13[uVar11].field_0x91);
            }
            if (pUVar13[uVar11].tipo_id == 0x10) {
              FUN_0046e44c(in_EAX & 0xffff,0,0,0,0);
            }
            FUN_00450874(0,1,'\0');
          }
          else {
            uVar6 = in_EAX & 0xffff;
            asStack_48[0] = 0;
            asStack_34[0] = 0;
            local_24 = tabela_unidades[uVar6].tipo_id;
            if (((local_24 != 1) && (local_24 != 0x15)) && (local_24 != 0xb)) {
              if ((local_24 < 0xc) || ((0xc < local_24 && (local_24 != 0xf)))) {
                bVar1 = false;
              }
              else {
                bVar1 = true;
              }
              if (bVar1) {
                bVar15 = tabela_unidades[uVar6].field_0x94;
              }
              else {
                bVar15 = tabela_unidades[uVar6].field_0x91;
              }
              FUN_004511a5(asStack_34,bVar15);
              FUN_00410fcc(extraout_ECX_14,asStack_48);
            }
            local_20 = pUVar13[uVar11].field_0x91;
            if (pUVar13[uVar11].tipo_id == 0xb) {
              iVar8 = FUN_004796cb((local_44 & 0xffff) >> 8,pUVar13[uVar11].celula_atual / 0x100,
                                   0x20);
              local_20 = (undefined1)iVar8;
            }
            if ((pUVar13[uVar11].tipo_id != 3) && (pUVar13[uVar11].tipo_id != 0x19)) {
              uVar7 = 0;
              if (pUVar13[uVar11].field_0xb7 == '\x01') {
                if ((tabela_unidades[*(ushort *)&pUVar13[uVar11].field_0xb8].tipo_id < 0x10) ||
                   (0x11 < tabela_unidades[*(ushort *)&pUVar13[uVar11].field_0xb8].tipo_id)) {
                  bVar1 = false;
                }
                else {
                  bVar1 = true;
                }
                if (bVar1) {
                  uVar7 = 1;
                }
              }
              FUN_0046e44c(in_EAX & 0xffff,local_20,(int)asStack_48[0],(int)asStack_34[0],uVar7);
            }
            bVar15 = pUVar13[uVar11].tipo_id;
            if (((bVar15 == 0xb) || (bVar15 == 3)) || (bVar15 == 0x19)) {
              FUN_0046e44c(in_EAX & 0xffff,local_20,0,0,0);
            }
          }
        }
        else if (bVar15 == 0x18) {
          FUN_00473510(uVar6,(uint)(byte)pUVar13[uVar11].field_0xf4);
          FUN_0044357c();
        }
      }
    }
    uVar6 = (uint)(byte)pUVar13[uVar11].field_0xa9;
    if ((uVar6 == 0) && (uVar6 = (uint)(byte)pUVar13[uVar11].field_0xa4, uVar6 == 0)) {
      if (pUVar13[uVar11].field_0x8b == '\0') {
        pUVar13[uVar11].field_0x8a = 0;
        uVar6 = (uint)pUVar13[uVar11].tipo_id;
        if (uVar6 != 0x10) {
          pUVar13[uVar11].field_0xa4 = 0;
        }
        pUVar13[uVar11].contador_recarga = 0;
      }
      else {
        uVar6 = (uint)pUVar13[uVar11].tipo_id;
        pUVar13[uVar11].field_0x8b = pUVar13[uVar11].field_0x8b + -1;
        if (uVar6 == 3) {
          pUVar13[uVar11].field_0xa4 = 5;
        }
        else if (uVar6 == 0xb) {
          pUVar13[uVar11].field_0xa4 = 0;
        }
      }
    }
    break;
  case 2:
    bVar15 = tabela_unidades[uVar11].tipo_id;
    if (0xf < bVar15) {
      if (bVar15 < 0x11) {
        cVar14 = tabela_unidades[uVar11].field_0xa9 + '\x01';
        pUVar10 = tabela_unidades + uVar11;
        tabela_unidades[uVar11].field_0xa9 = cVar14;
        if (cVar14 == pUVar10->field_0xa7) {
          pUVar13[uVar11].field_0xa9 = 0;
          pUVar13[uVar11].field_0xa4 =
               (char)(((byte)pUVar13[uVar11].field_0xa4 + 1) %
                     (uint)(byte)pUVar13[uVar11].field_0xa5);
        }
      }
      else if (bVar15 == 0x11) {
        FUN_00447b2f();
        param_1 = extraout_ECX_15;
      }
    }
    if ((pUVar13[uVar11].field_0x8b == '\x01') && (pUVar13[uVar11].tipo_id != 0x10)) {
      pUVar13[uVar11].field_0xa4 = 0;
      pUVar13[uVar11].field_0xa9 = 0;
    }
    bVar15 = pUVar13[uVar11].field_0x8b - 1;
    uVar6 = (uint)bVar15;
    pUVar13[uVar11].field_0x8b = bVar15;
    if (bVar15 != 0) break;
    pUVar13[uVar11].field_0x8a = 1;
    if (pUVar13[uVar11].tipo_id != 0x10) {
      pUVar13[uVar11].field_0xa4 = 0;
      pUVar13[uVar11].field_0xa9 = 0;
    }
    bVar15 = tabela_unidades[in_EAX & 0xffff].tipo_id;
    if ((bVar15 < 0xe) || ((0xe < bVar15 && (bVar15 != 0x10)))) {
      bVar1 = false;
    }
    else {
      bVar1 = true;
    }
    if (!bVar1) {
      uVar17 = FUN_00446cb5(param_1,pUVar13[uVar11].field_0xb7);
      uVar6 = (uint)uVar17;
      if ((char)uVar17 != '\0') {
        uVar17 = FUN_00451464(extraout_ECX_16,(int)((ulonglong)uVar17 >> 0x20));
        uVar6 = (uint)uVar17;
        if ((char)uVar17 != '\0') break;
      }
      pUVar13[uVar11].field_0x8a = 0;
      break;
    }
LAB_00451e51:
    uVar6 = (uint)(byte)tabela_unidades[in_EAX & 0xffff].field_0xda;
    if (uVar6 == 0) {
      uVar6 = FUN_004457d3();
    }
    break;
  case 3:
    if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
       (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
      uVar6 = 0;
    }
    else {
      uVar6 = 1;
    }
    if ((char)uVar6 != '\0') {
      uVar6 = (in_EAX & 0xffff) * 0x45;
      tabela_unidades[in_EAX & 0xffff].estado = 7;
      if (sVar4 == DAT_00496304) {
        uVar6 = CONCAT22((short)(uVar6 >> 0x10),(ushort)(byte)uVar6);
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = -1;
      }
    }
    *(undefined2 *)&pUVar13[uVar11].field_0xb8 = 0xffff;
    pUVar13[uVar11].field_0xa4 = 0;
    pUVar13[uVar11].field_0xa9 = 0;
  }
  return CONCAT44(param_2,uVar6);
}
