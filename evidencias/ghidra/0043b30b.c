/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0043b30b, entrada 0043b30b.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Removing unreachable block (ram,0x0043d305) */
/* WARNING: Removing unreachable block (ram,0x0043b63a) */
/* WARNING: Removing unreachable block (ram,0x0043baf0) */
/* WARNING: Removing unreachable block (ram,0x0043b7cf) */
/* WARNING: Removing unreachable block (ram,0x0043b955) */
/* WARNING: Removing unreachable block (ram,0x0043bc8b) */
/* WARNING: Removing unreachable block (ram,0x0043c1bb) */
/* WARNING: Removing unreachable block (ram,0x0043ca75) */
/* WARNING: Removing unreachable block (ram,0x0043dbad) */

int __fastcall
FUN_0043b30b(byte param_1,ushort param_2,undefined2 *param_3,undefined1 param_4,undefined1 param_5)

{
  ushort uVar1;
  byte bVar2;
  char cVar3;
  uint in_EAX;
  uint uVar4;
  uint3 uVar5;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_ECX_01;
  uint extraout_ECX_02;
  uint extraout_ECX_03;
  uint uVar6;
  uint extraout_ECX_04;
  uint extraout_ECX_05;
  uint extraout_ECX_06;
  uint extraout_ECX_07;
  uint extraout_ECX_08;
  uint extraout_ECX_09;
  uint extraout_ECX_10;
  uint extraout_ECX_11;
  uint extraout_ECX_12;
  uint extraout_ECX_13;
  uint extraout_ECX_14;
  uint extraout_ECX_15;
  uint extraout_ECX_16;
  uint extraout_ECX_17;
  uint extraout_ECX_18;
  uint extraout_ECX_19;
  uint extraout_ECX_20;
  uint extraout_ECX_21;
  uint extraout_ECX_22;
  uint extraout_ECX_23;
  uint extraout_ECX_24;
  uint extraout_ECX_25;
  uint extraout_ECX_26;
  uint extraout_ECX_27;
  uint extraout_ECX_28;
  uint extraout_ECX_29;
  uint extraout_ECX_30;
  uint extraout_ECX_31;
  int iVar7;
  uint uVar8;
  uint uVar9;
  ushort *puVar10;
  uint uVar11;
  ushort unaff_BX;
  ushort uVar12;
  int iVar13;
  uint uVar14;
  uint uVar15;
  ushort uVar16;
  bool bVar17;
  undefined8 uVar18;
  int local_1f8;
  int local_1f4;
  undefined1 local_1ec;
  int local_1e4;
  int local_1e0;
  ushort local_1d8;
  ushort local_1d0;
  uint local_1cc;
  ushort local_1c8;
  ushort local_1c0;
  uint local_1bc;
  uint local_1b8;
  ushort local_1b4;
  ushort local_1b0;
  uint local_1a4;
  ushort local_1a0;
  uint local_198;
  ushort local_194;
  ushort local_18c;
  undefined4 local_188;
  int local_184;
  ushort local_180;
  ushort local_17c;
  uint local_168;
  ushort local_164;
  ushort local_160;
  ushort local_158;
  ushort local_154;
  ushort local_150;
  undefined4 local_140;
  ushort local_138;

  local_1b8 = CONCAT22(local_1b8._2_2_,param_2);
  uVar14 = local_1b8;
  DAT_004e0f34 = param_4;
  DAT_004e0f37 = 0;
  DAT_00496302 = 0;
  DAT_004e0f35 = param_5;
  DAT_004e0f36 = 1;
  DAT_004e0f3c = param_3;
  DAT_004e0f48 = (&DAT_004962c8)[tabela_unidades[unaff_BX].tipo_id];
  DAT_004e0f41 = tabela_unidades[unaff_BX].proprietario_id;
  DAT_00496304 = unaff_BX;
  DAT_004e0f42 = param_1;
  *param_3 = 0;
  DAT_004e0f4a = 0xffff;
  DAT_004e0f4c = 1;
  iVar13 = (uint)(param_2 & 0xff) - (in_EAX & 0xff);
  iVar7 = ((int)(uint)param_2 >> 8) - ((int)(in_EAX & 0xffff) >> 8);
  bVar2 = 0 < iVar13;
  if (0 < iVar7) {
    bVar2 = bVar2 + 2;
  }
  if (iVar13 < 0) {
    iVar13 = -iVar13;
  }
  if (iVar7 < 0) {
    iVar7 = -iVar7;
  }
  if (iVar13 == 0) {
    bVar2 = (&DAT_0049638c)[bVar2];
  }
  else if (iVar7 == 0) {
    bVar2 = (&DAT_00496390)[bVar2];
  }
  else {
    bVar2 = (&DAT_00496388)[bVar2];
  }
  uVar12 = (ushort)bVar2;
  local_1b8._0_1_ = (char)param_2;
  uVar4 = uVar14;
  if (DAT_004e0f48 != 0) {
    if (DAT_004e0f48 < 2) {
      if (*(char *)((uint)param_2 + DAT_00507d74) == -3) {
        bVar2 = DAT_004e0f42 & 1;
      }
      else {
        bVar2 = *(byte *)(DAT_00507da8 + (uint)param_2) & DAT_004e0f42;
      }
      if (bVar2 != 0) {
        uVar1 = tabela_unidades[DAT_00496304].celula_atual;
        if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1)) ||
            ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)))) ||
           (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043b5e0:
          bVar17 = false;
        }
        else if (DAT_004e0f48 == 1) {
          bVar17 = uVar1 == param_2;
        }
        else {
          if (uVar1 != param_2) {
            uVar8 = (uint)uVar1;
            uVar6 = (uint)param_2;
            if (((uVar8 - 1 != uVar6) && (uVar8 - 0x101 != uVar6)) && (uVar8 - 0x100 != uVar6))
            goto LAB_0043b5e0;
          }
          bVar17 = true;
        }
        if (!bVar17) {
          puVar10 = (ushort *)(DAT_004e0f38 + (uint)param_2 * 2);
          if ((*puVar10 >> 8 & 0xc0) == 0x40) {
            iVar7 = (int)(*puVar10 & 0x3ff8) >> 3;
          }
          else {
            iVar7 = 0xffff;
          }
          if (iVar7 == 0xffff) goto LAB_0043b62f;
          uVar18 = FUN_0042ece0(uVar14,(uint)uVar12);
          cVar3 = (char)uVar18;
          uVar4 = extraout_ECX;
joined_r0x0043b650:
          bVar17 = false;
          if (cVar3 == '\0') goto LAB_0043b457;
        }
      }
    }
    else if (DAT_004e0f48 < 4) {
      if (((char)local_1b8 == '\0') || (uVar6 = (uint)param_2, (int)uVar6 >> 8 == 0)) {
LAB_0043b62f:
        bVar17 = false;
        goto LAB_0043b457;
      }
      if (*(char *)(uVar6 + DAT_00507d74) == -3) {
        bVar2 = DAT_004e0f42 & 1;
      }
      else {
        bVar2 = *(byte *)(DAT_00507da8 + uVar6) & DAT_004e0f42;
      }
      if (bVar2 != 0) {
        uVar1 = tabela_unidades[DAT_00496304].celula_atual;
        if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1)) ||
            ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)))) ||
           (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043b77b:
          bVar17 = false;
        }
        else if (DAT_004e0f48 == 1) {
          bVar17 = uVar1 == param_2;
        }
        else {
          if (uVar1 != param_2) {
            uVar8 = (uint)uVar1;
            uVar6 = (uint)param_2;
            if (((uVar8 - 1 != uVar6) && (uVar8 - 0x101 != uVar6)) && (uVar8 - 0x100 != uVar6))
            goto LAB_0043b77b;
          }
          bVar17 = true;
        }
        if (!bVar17) {
          puVar10 = (ushort *)(DAT_004e0f38 + (uint)param_2 * 2);
          if ((*puVar10 >> 8 & 0xc0) == 0x40) {
            iVar7 = (int)(*puVar10 & 0x3ff8) >> 3;
          }
          else {
            iVar7 = 0xffff;
          }
          if (iVar7 == 0xffff) {
            bVar17 = false;
            goto LAB_0043b457;
          }
          uVar18 = FUN_0042ece0(uVar14,(uint)uVar12);
          bVar17 = false;
          uVar4 = extraout_ECX_00;
          if ((char)uVar18 == '\0') goto LAB_0043b457;
        }
      }
      uVar6 = (uint)(ushort)((short)uVar4 - 1);
      if (*(char *)(uVar6 + DAT_00507d74) == -3) {
        bVar2 = DAT_004e0f42 & 1;
      }
      else {
        bVar2 = *(byte *)(DAT_00507da8 + uVar6) & DAT_004e0f42;
      }
      if (bVar2 != 0) {
        uVar1 = tabela_unidades[DAT_00496304].celula_atual;
        if (((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1)) ||
           (((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)) ||
            (tabela_unidades[DAT_00496304].estado == 0xe)))) {
LAB_0043b900:
          bVar17 = false;
        }
        else {
          uVar16 = (ushort)(uVar4 - 1);
          if (DAT_004e0f48 == 1) {
            bVar17 = uVar1 == uVar16;
          }
          else {
            if (uVar1 != uVar16) {
              uVar6 = (uint)uVar1;
              uVar8 = uVar4 - 1 & 0xffff;
              if (((uVar6 - 1 != uVar8) && (uVar6 - 0x101 != uVar8)) && (uVar6 - 0x100 != uVar8))
              goto LAB_0043b900;
            }
            bVar17 = true;
          }
        }
        if (!bVar17) {
          iVar7 = DAT_004e0f38 + (uVar4 & 0xffff) * 2;
          if ((*(ushort *)(iVar7 + -2) >> 8 & 0xc0) == 0x40) {
            iVar7 = (int)(*(ushort *)(iVar7 + -2) & 0x3ff8) >> 3;
          }
          else {
            iVar7 = 0xffff;
          }
          if (iVar7 == 0xffff) goto LAB_0043b62f;
          uVar18 = FUN_0042ece0(uVar4,(uint)uVar12);
          bVar17 = false;
          uVar4 = extraout_ECX_01;
          if ((char)uVar18 == '\0') goto LAB_0043b457;
        }
      }
      uVar6 = (uint)(ushort)((short)uVar4 - 0x101);
      if (*(char *)(uVar6 + DAT_00507d74) == -3) {
        bVar2 = DAT_004e0f42 & 1;
      }
      else {
        bVar2 = *(byte *)(DAT_00507da8 + uVar6) & DAT_004e0f42;
      }
      if (bVar2 != 0) {
        uVar1 = tabela_unidades[DAT_00496304].celula_atual;
        if (((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1)) ||
           (((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)) ||
            (tabela_unidades[DAT_00496304].estado == 0xe)))) {
LAB_0043ba91:
          bVar17 = false;
        }
        else {
          uVar16 = (ushort)(uVar4 - 0x101);
          if (DAT_004e0f48 == 1) {
            bVar17 = uVar1 == uVar16;
          }
          else {
            if (uVar1 != uVar16) {
              uVar8 = (uint)uVar1;
              uVar6 = uVar4 - 0x101 & 0xffff;
              if (((uVar8 - 1 != uVar6) && (uVar8 - 0x101 != uVar6)) && (uVar8 - 0x100 != uVar6))
              goto LAB_0043ba91;
            }
            bVar17 = true;
          }
        }
        if (!bVar17) {
          iVar7 = DAT_004e0f38 + (uVar4 & 0xffff) * 2;
          if ((*(ushort *)(iVar7 + -0x202) >> 8 & 0xc0) == 0x40) {
            iVar7 = (int)(*(ushort *)(iVar7 + -0x202) & 0x3ff8) >> 3;
          }
          else {
            iVar7 = 0xffff;
          }
          if (iVar7 == 0xffff) goto LAB_0043b62f;
          uVar18 = FUN_0042ece0(uVar4,(uint)uVar12);
          bVar17 = false;
          uVar4 = extraout_ECX_02;
          if ((char)uVar18 == '\0') goto LAB_0043b457;
        }
      }
      uVar6 = (uint)(ushort)((short)uVar4 - 0x100);
      if (*(char *)(uVar6 + DAT_00507d74) == -3) {
        bVar2 = DAT_004e0f42 & 1;
      }
      else {
        bVar2 = *(byte *)(DAT_00507da8 + uVar6) & DAT_004e0f42;
      }
      if (bVar2 != 0) {
        uVar1 = tabela_unidades[DAT_00496304].celula_atual;
        if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1)) ||
            ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)))) ||
           (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043bc2c:
          bVar17 = false;
        }
        else {
          uVar16 = (ushort)(uVar4 - 0x100);
          if (DAT_004e0f48 == 1) {
            bVar17 = uVar1 == uVar16;
          }
          else {
            if (uVar1 != uVar16) {
              uVar6 = (uint)uVar1;
              uVar8 = uVar4 - 0x100 & 0xffff;
              if (((uVar6 - 1 != uVar8) && (uVar6 - 0x101 != uVar8)) && (uVar6 - 0x100 != uVar8))
              goto LAB_0043bc2c;
            }
            bVar17 = true;
          }
        }
        if (!bVar17) {
          iVar7 = DAT_004e0f38 + (uVar4 & 0xffff) * 2;
          if ((*(ushort *)(iVar7 + -0x200) >> 8 & 0xc0) == 0x40) {
            iVar7 = (int)(*(ushort *)(iVar7 + -0x200) & 0x3ff8) >> 3;
          }
          else {
            iVar7 = 0xffff;
          }
          if (iVar7 != 0xffff) {
            uVar18 = FUN_0042ece0(uVar4,(uint)uVar12);
            cVar3 = (char)uVar18;
            uVar4 = extraout_ECX_03;
            goto joined_r0x0043b650;
          }
          goto LAB_0043b62f;
        }
      }
    }
  }
  bVar17 = true;
LAB_0043b457:
  local_180 = (ushort)in_EAX;
  local_1b8 = uVar14;
  if (!bVar17) {
    iVar13 = (param_2 & 0xff) - (in_EAX & 0xff);
    iVar7 = ((int)(uint)param_2 >> 8) - ((int)(in_EAX & 0xffff) >> 8);
    bVar2 = 0 < iVar13;
    if (0 < iVar7) {
      bVar2 = bVar2 + 2;
    }
    if (iVar13 < 0) {
      iVar13 = -iVar13;
    }
    if (iVar7 < 0) {
      iVar7 = -iVar7;
    }
    if (iVar13 == 0) {
      uVar4 = (uint)(byte)(&DAT_0049638c)[bVar2];
    }
    else if (iVar7 == 0) {
      uVar4 = (uint)(byte)(&DAT_00496390)[bVar2];
    }
    else {
      uVar4 = (uint)(byte)(&DAT_00496388)[bVar2];
    }
    iVar7 = (int)(uint)param_2 >> 8;
    uVar6 = in_EAX;
    if (param_2 != local_180) {
      if (((param_2 & 0xff) < DAT_00497168) && (param_2 >> 8 < DAT_0049716a)) {
        local_188 = CONCAT22(local_188._2_2_,0x100);
        local_140 = 0x200;
        local_184 = 2;
        local_1a4 = uVar14 + 0xffff;
        for (uVar12 = 1; uVar12 < 0x1e; uVar12 = uVar12 + 1) {
          uVar14 = (param_2 & 0xff) - (in_EAX & 0xff);
          uVar8 = iVar7 - ((int)(in_EAX & 0xffff) >> 8);
          if ((int)uVar14 < 0) {
            uVar14 = -uVar14;
          }
          if ((int)uVar8 < 0) {
            uVar8 = -uVar8;
          }
          if ((int)uVar14 < (int)uVar8) {
            uVar14 = uVar8;
          }
          if (uVar14 == uVar12) {
            uVar14 = in_EAX;
            goto LAB_0043e096;
          }
          uVar8 = local_1a4 - local_188;
          local_1ec = (undefined1)uVar4;
          if (-1 < (int)(iVar7 - (uint)uVar12)) {
            local_168 = 0;
            uVar11 = CONCAT31((int3)((uint)local_188 >> 8),local_1ec);
            uVar14 = uVar8;
            while( true ) {
              if ((uint)uVar12 * 2 < (local_168 & 0xffff)) break;
              iVar13 = ((local_168 & 0xffff) + (param_2 & 0xff)) - (uint)uVar12;
              uVar6 = uVar11;
              if ((-1 < iVar13) && (iVar13 <= (int)(uint)DAT_00497168)) {
                uVar6 = CONCAT22((short)(uVar11 >> 0x10),(ushort)(byte)uVar11);
                if (DAT_004e0f48 == 0) goto LAB_0043be80;
                local_160 = (ushort)uVar14;
                if (DAT_004e0f48 < 2) {
                  if (*(char *)((uVar14 & 0xffff) + DAT_00507d74) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + (uVar14 & 0xffff)) & DAT_004e0f42;
                  }
                  if (bVar2 != 0) {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                        || ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ))) || (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043bfa5:
                      bVar17 = false;
                    }
                    else if (DAT_004e0f48 == 1) {
                      bVar17 = uVar1 == local_160;
                    }
                    else {
                      if (uVar1 != local_160) {
                        uVar11 = (uint)uVar1;
                        uVar15 = uVar14 & 0xffff;
                        if (((uVar11 - 1 != uVar15) && (uVar11 - 0x101 != uVar15)) &&
                           (uVar11 - 0x100 != uVar15)) goto LAB_0043bfa5;
                      }
                      bVar17 = true;
                    }
                    if (!bVar17) {
                      puVar10 = (ushort *)(DAT_004e0f38 + (uVar14 & 0xffff) * 2);
                      if ((*puVar10 >> 8 & 0xc0) == 0x40) {
                        iVar13 = (int)(*puVar10 & 0x3ff8) >> 3;
                      }
                      else {
                        iVar13 = 0xffff;
                      }
                      if (iVar13 == 0xffff) goto LAB_0043bff4;
LAB_0043bffb:
                      if ((char)(uVar6 >> 8) == '\0') {
                        uVar18 = FUN_0042ece0(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_05;
                      }
                      else {
                        uVar18 = FUN_0042eba4(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_04;
                      }
                      if (cVar3 == '\0') goto LAB_0043bff4;
                    }
                  }
LAB_0043be80:
                  bVar17 = true;
                }
                else {
                  if (3 < DAT_004e0f48) goto LAB_0043be80;
                  if (((uVar14 & 0xff) == 0) || (uVar15 = uVar14 & 0xffff, (int)uVar15 >> 8 == 0))
                  goto LAB_0043bff4;
                  if (*(char *)(uVar15 + DAT_00507d74) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + uVar15) & DAT_004e0f42;
                  }
                  if (bVar2 != 0) {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                        || ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ))) || (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043c16a:
                      bVar17 = false;
                    }
                    else if (DAT_004e0f48 == 1) {
                      bVar17 = uVar1 == local_160;
                    }
                    else {
                      if (uVar1 != local_160) {
                        uVar15 = (uint)uVar1;
                        uVar9 = uVar14 & 0xffff;
                        if (((uVar9 != uVar15 - 1) && (uVar9 != uVar15 - 0x101)) &&
                           (uVar15 - 0x100 != uVar9)) goto LAB_0043c16a;
                      }
                      bVar17 = true;
                    }
                    if (bVar17) goto LAB_0043c1d7;
                    puVar10 = (ushort *)(DAT_004e0f38 + (uVar14 & 0xffff) * 2);
                    if ((*puVar10 >> 8 & 0xc0) == 0x40) {
                      iVar13 = (int)(*puVar10 & 0x3ff8) >> 3;
                    }
                    else {
                      iVar13 = 0xffff;
                    }
                    if (iVar13 != 0xffff) {
                      uVar18 = FUN_0042ece0(uVar6,uVar11 & 0xff);
                      uVar6 = extraout_ECX_06;
                      if ((char)uVar18 != '\0') goto LAB_0043c1d7;
                    }
                    goto LAB_0043bff4;
                  }
LAB_0043c1d7:
                  uVar11 = uVar14 - 1 & 0xffff;
                  if (*(char *)(uVar11 + DAT_00507d74) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + uVar11) & DAT_004e0f42;
                  }
                  if (bVar2 != 0) {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if (((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                       || (((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ) || (tabela_unidades[DAT_00496304].estado == 0xe)))) {
LAB_0043c30f:
                      bVar17 = false;
                    }
                    else {
                      local_17c = (ushort)(uVar14 - 1);
                      if (DAT_004e0f48 == 1) {
                        bVar17 = uVar1 == local_17c;
                      }
                      else {
                        if (uVar1 != local_17c) {
                          uVar11 = (uint)uVar1;
                          uVar15 = uVar14 - 1 & 0xffff;
                          if (((uVar15 != uVar11 - 1) && (uVar15 != uVar11 - 0x101)) &&
                             (uVar11 - 0x100 != uVar15)) goto LAB_0043c30f;
                        }
                        bVar17 = true;
                      }
                    }
                    if (bVar17) goto LAB_0043c380;
                    iVar13 = DAT_004e0f38 + (uVar14 & 0xffff) * 2;
                    if ((*(ushort *)(iVar13 + -2) >> 8 & 0xc0) == 0x40) {
                      iVar13 = (int)(*(ushort *)(iVar13 + -2) & 0x3ff8) >> 3;
                    }
                    else {
                      iVar13 = 0xffff;
                    }
                    if (iVar13 != 0xffff) {
                      if ((char)(uVar6 >> 8) == '\0') {
                        uVar18 = FUN_0042ece0(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_08;
                      }
                      else {
                        uVar18 = FUN_0042eba4(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_07;
                      }
                      if (cVar3 != '\0') goto LAB_0043c380;
                    }
                    goto LAB_0043bff4;
                  }
LAB_0043c380:
                  uVar11 = uVar14 - 0x101 & 0xffff;
                  if (*(char *)(uVar11 + DAT_00507d74) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + uVar11) & DAT_004e0f42;
                  }
                  if (bVar2 == 0) {
LAB_0043c529:
                    uVar11 = uVar14 - 0x100 & 0xffff;
                    if (*(char *)(uVar11 + DAT_00507d74) == -3) {
                      bVar2 = DAT_004e0f42 & 1;
                    }
                    else {
                      bVar2 = *(byte *)(DAT_00507da8 + uVar11) & DAT_004e0f42;
                    }
                    if (bVar2 == 0) goto LAB_0043be80;
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                        || ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ))) || (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043c656:
                      bVar17 = false;
                    }
                    else {
                      local_164 = (ushort)(uVar14 - 0x100);
                      if (DAT_004e0f48 == 1) {
                        bVar17 = uVar1 == local_164;
                      }
                      else {
                        if (uVar1 != local_164) {
                          uVar15 = (uint)uVar1;
                          uVar11 = uVar14 - 0x100 & 0xffff;
                          if (((uVar15 - 1 != uVar11) && (uVar15 - 0x101 != uVar11)) &&
                             (uVar15 - 0x100 != uVar11)) goto LAB_0043c656;
                        }
                        bVar17 = true;
                      }
                    }
                    if (bVar17) goto LAB_0043be80;
                    iVar13 = DAT_004e0f38 + (uVar14 & 0xffff) * 2;
                    if ((*(ushort *)(iVar13 + -0x200) >> 8 & 0xc0) == 0x40) {
                      iVar13 = (int)(*(ushort *)(iVar13 + -0x200) & 0x3ff8) >> 3;
                    }
                    else {
                      iVar13 = 0xffff;
                    }
                    if (iVar13 != 0xffff) goto LAB_0043bffb;
                  }
                  else {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                        || ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ))) || (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043c4ae:
                      bVar17 = false;
                    }
                    else {
                      local_150 = (ushort)(uVar14 - 0x101);
                      if (DAT_004e0f48 == 1) {
                        bVar17 = uVar1 == local_150;
                      }
                      else {
                        if (uVar1 != local_150) {
                          uVar11 = (uint)uVar1;
                          uVar15 = uVar14 - 0x101 & 0xffff;
                          if (((uVar15 != uVar11 - 1) && (uVar15 != uVar11 - 0x101)) &&
                             (uVar11 - 0x100 != uVar15)) goto LAB_0043c4ae;
                        }
                        bVar17 = true;
                      }
                    }
                    if (bVar17) goto LAB_0043c529;
                    iVar13 = DAT_004e0f38 + (uVar14 & 0xffff) * 2;
                    if ((*(ushort *)(iVar13 + -0x202) >> 8 & 0xc0) == 0x40) {
                      iVar13 = (int)(*(ushort *)(iVar13 + -0x202) & 0x3ff8) >> 3;
                    }
                    else {
                      iVar13 = 0xffff;
                    }
                    if (iVar13 != 0xffff) {
                      if ((char)(uVar6 >> 8) == '\0') {
                        uVar18 = FUN_0042ece0(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_10;
                      }
                      else {
                        uVar18 = FUN_0042eba4(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_09;
                      }
                      if (cVar3 != '\0') goto LAB_0043c529;
                    }
                  }
LAB_0043bff4:
                  bVar17 = false;
                }
                if (bVar17) goto LAB_0043e096;
              }
              local_168 = local_168 + 1;
              uVar14 = uVar14 + 1;
              uVar11 = uVar6;
            }
          }
          if ((uint)uVar12 + iVar7 < (uint)DAT_0049716a) {
            local_198 = 0;
            uVar14 = uVar8 + local_140;
            uVar11 = uVar4;
            while( true ) {
              if ((uint)uVar12 * 2 < (local_198 & 0xffff)) break;
              iVar13 = ((local_198 & 0xffff) + (param_2 & 0xff)) - (uint)uVar12;
              uVar6 = uVar11;
              if ((-1 < iVar13) && (iVar13 <= (int)(uint)DAT_00497168)) {
                uVar6 = CONCAT22((short)(uVar11 >> 0x10),(ushort)(byte)uVar11);
                if (DAT_004e0f48 == 0) goto LAB_0043c748;
                local_138 = (ushort)uVar14;
                if (DAT_004e0f48 < 2) {
                  if (*(char *)((uVar14 & 0xffff) + DAT_00507d74) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + (uVar14 & 0xffff)) & DAT_004e0f42;
                  }
                  if (bVar2 != 0) {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if (((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                       || (((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ) || (tabela_unidades[DAT_00496304].estado == 0xe)))) {
LAB_0043c887:
                      bVar17 = false;
                    }
                    else if (DAT_004e0f48 == 1) {
                      bVar17 = uVar1 == local_138;
                    }
                    else {
                      if (uVar1 != local_138) {
                        uVar11 = (uint)uVar1;
                        uVar15 = uVar14 & 0xffff;
                        if (((uVar11 - 1 != uVar15) && (uVar11 - 0x101 != uVar15)) &&
                           (uVar11 - 0x100 != uVar15)) goto LAB_0043c887;
                      }
                      bVar17 = true;
                    }
                    if (!bVar17) {
                      puVar10 = (ushort *)(DAT_004e0f38 + (uVar14 & 0xffff) * 2);
                      if ((*puVar10 >> 8 & 0xc0) == 0x40) {
                        iVar13 = (int)(*puVar10 & 0x3ff8) >> 3;
                      }
                      else {
                        iVar13 = 0xffff;
                      }
                      if (iVar13 == 0xffff) goto LAB_0043c8d6;
LAB_0043c8dd:
                      if ((char)(uVar6 >> 8) == '\0') {
                        uVar18 = FUN_0042ece0(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_12;
                      }
                      else {
                        uVar18 = FUN_0042eba4(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_11;
                      }
                      if (cVar3 == '\0') goto LAB_0043c8d6;
                    }
                  }
LAB_0043c748:
                  bVar17 = true;
                }
                else {
                  if (3 < DAT_004e0f48) goto LAB_0043c748;
                  if (((uVar14 & 0xff) == 0) || (uVar15 = uVar14 & 0xffff, (int)uVar15 >> 8 == 0))
                  goto LAB_0043c8d6;
                  if (*(char *)(uVar15 + DAT_00507d74) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + uVar15) & DAT_004e0f42;
                  }
                  if (bVar2 != 0) {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                        || ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ))) || (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043ca20:
                      bVar17 = false;
                    }
                    else if (DAT_004e0f48 == 1) {
                      bVar17 = uVar1 == local_138;
                    }
                    else {
                      if (uVar1 != local_138) {
                        uVar15 = (uint)uVar1;
                        uVar9 = uVar14 & 0xffff;
                        if (((uVar9 != uVar15 - 1) && (uVar9 != uVar15 - 0x101)) &&
                           (uVar15 - 0x100 != uVar9)) goto LAB_0043ca20;
                      }
                      bVar17 = true;
                    }
                    if (bVar17) goto LAB_0043ca91;
                    puVar10 = (ushort *)((uVar14 & 0xffff) * 2 + DAT_004e0f38);
                    if ((*puVar10 >> 8 & 0xc0) == 0x40) {
                      local_1f8 = (int)(*puVar10 & 0x3ff8) >> 3;
                    }
                    else {
                      local_1f8 = 0xffff;
                    }
                    if (local_1f8 != 0xffff) {
                      uVar18 = FUN_0042ece0(uVar6,uVar11 & 0xff);
                      uVar6 = extraout_ECX_13;
                      if ((char)uVar18 != '\0') goto LAB_0043ca91;
                    }
                    goto LAB_0043c8d6;
                  }
LAB_0043ca91:
                  uVar11 = uVar14 - 1 & 0xffff;
                  if (*(char *)(uVar11 + DAT_00507d74) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + uVar11) & DAT_004e0f42;
                  }
                  if (bVar2 != 0) {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                        || ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ))) || (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043cba9:
                      bVar17 = false;
                    }
                    else {
                      local_1d0 = (ushort)(uVar14 - 1);
                      if (DAT_004e0f48 == 1) {
                        bVar17 = uVar1 == local_1d0;
                      }
                      else {
                        if (uVar1 != local_1d0) {
                          uVar11 = (uint)uVar1;
                          uVar15 = uVar14 - 1 & 0xffff;
                          if (((uVar15 != uVar11 - 1) && (uVar15 != uVar11 - 0x101)) &&
                             (uVar11 - 0x100 != uVar15)) goto LAB_0043cba9;
                        }
                        bVar17 = true;
                      }
                    }
                    if (bVar17) goto LAB_0043cc1a;
                    iVar13 = DAT_004e0f38 + (uVar14 & 0xffff) * 2;
                    if ((*(ushort *)(iVar13 + -2) >> 8 & 0xc0) == 0x40) {
                      iVar13 = (int)(*(ushort *)(iVar13 + -2) & 0x3ff8) >> 3;
                    }
                    else {
                      iVar13 = 0xffff;
                    }
                    if (iVar13 != 0xffff) {
                      if ((char)(uVar6 >> 8) == '\0') {
                        uVar18 = FUN_0042ece0(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_15;
                      }
                      else {
                        uVar18 = FUN_0042eba4(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_14;
                      }
                      if (cVar3 != '\0') goto LAB_0043cc1a;
                    }
                    goto LAB_0043c8d6;
                  }
LAB_0043cc1a:
                  uVar11 = uVar14 - 0x101 & 0xffff;
                  if (*(char *)(uVar11 + DAT_00507d74) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + uVar11) & DAT_004e0f42;
                  }
                  if (bVar2 == 0) {
LAB_0043cdbb:
                    uVar11 = uVar14 - 0x100 & 0xffff;
                    if (*(char *)(DAT_00507d74 + uVar11) == -3) {
                      bVar2 = DAT_004e0f42 & 1;
                    }
                    else {
                      bVar2 = *(byte *)(DAT_00507da8 + uVar11) & DAT_004e0f42;
                    }
                    if (bVar2 == 0) goto LAB_0043c748;
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if (((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                       || (((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ) || (tabela_unidades[DAT_00496304].estado == 0xe)))) {
LAB_0043ceef:
                      bVar17 = false;
                    }
                    else {
                      local_1b0 = (ushort)(uVar14 - 0x100);
                      if (DAT_004e0f48 == 1) {
                        bVar17 = uVar1 == local_1b0;
                      }
                      else {
                        if (uVar1 != local_1b0) {
                          uVar11 = (uint)uVar1;
                          uVar15 = uVar14 - 0x100 & 0xffff;
                          if (((uVar11 - 1 != uVar15) && (uVar11 - 0x101 != uVar15)) &&
                             (uVar11 - 0x100 != uVar15)) goto LAB_0043ceef;
                        }
                        bVar17 = true;
                      }
                    }
                    if (bVar17) goto LAB_0043c748;
                    iVar13 = DAT_004e0f38 + (uVar14 & 0xffff) * 2;
                    if ((*(ushort *)(iVar13 + -0x200) >> 8 & 0xc0) == 0x40) {
                      iVar13 = (int)(*(ushort *)(iVar13 + -0x200) & 0x3ff8) >> 3;
                    }
                    else {
                      iVar13 = 0xffff;
                    }
                    if (iVar13 != 0xffff) goto LAB_0043c8dd;
                  }
                  else {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                        || ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ))) || (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043cd3a:
                      bVar17 = false;
                    }
                    else {
                      local_1d8 = (ushort)(uVar14 - 0x101);
                      if (DAT_004e0f48 == 1) {
                        bVar17 = uVar1 == local_1d8;
                      }
                      else {
                        if (uVar1 != local_1d8) {
                          uVar15 = (uint)uVar1;
                          uVar11 = uVar14 - 0x101 & 0xffff;
                          if (((uVar15 - 1 != uVar11) && (uVar15 - 0x101 != uVar11)) &&
                             (uVar15 - 0x100 != uVar11)) goto LAB_0043cd3a;
                        }
                        bVar17 = true;
                      }
                    }
                    if (bVar17) goto LAB_0043cdbb;
                    iVar13 = DAT_004e0f38 + (uVar14 & 0xffff) * 2;
                    if ((*(ushort *)(iVar13 + -0x202) >> 8 & 0xc0) == 0x40) {
                      local_1f4 = (int)(*(ushort *)(iVar13 + -0x202) & 0x3ff8) >> 3;
                    }
                    else {
                      local_1f4 = 0xffff;
                    }
                    if (local_1f4 != 0xffff) {
                      if ((char)(uVar6 >> 8) == '\0') {
                        uVar18 = FUN_0042ece0(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_17;
                      }
                      else {
                        uVar18 = FUN_0042eba4(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_16;
                      }
                      if (cVar3 != '\0') goto LAB_0043cdbb;
                    }
                  }
LAB_0043c8d6:
                  bVar17 = false;
                }
                if (bVar17) goto LAB_0043e096;
              }
              local_198 = local_198 + 1;
              uVar14 = uVar14 + 1;
              uVar11 = uVar6;
            }
          }
          if (-1 < (int)((param_2 & 0xff) - (uint)uVar12)) {
            local_1bc = 1;
            uVar11 = uVar4;
            uVar14 = uVar8;
            while( true ) {
              uVar15 = (uint)uVar12;
              uVar9 = local_1bc & 0xffff;
              if (uVar15 * 2 <= uVar9) break;
              uVar6 = uVar11;
              if ((-1 < (int)((iVar7 + uVar9) - uVar15)) &&
                 ((int)((uVar9 + (param_2 & 0xff)) - uVar15) < (int)(uint)DAT_0049716a)) {
                uVar6 = CONCAT22((short)(uVar11 >> 0x10),(ushort)(byte)uVar11);
                if (DAT_004e0f48 == 0) goto LAB_0043cfe1;
                local_194 = (ushort)uVar14;
                if (DAT_004e0f48 < 2) {
                  if (*(char *)((uVar14 & 0xffff) + DAT_00507d74) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + (uVar14 & 0xffff)) & DAT_004e0f42;
                  }
                  if (bVar2 != 0) {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                        || ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ))) || (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043d107:
                      bVar17 = false;
                    }
                    else if (DAT_004e0f48 == 1) {
                      bVar17 = uVar1 == local_194;
                    }
                    else {
                      if (uVar1 != local_194) {
                        uVar11 = (uint)uVar1;
                        uVar15 = uVar14 & 0xffff;
                        if (((uVar11 - 1 != uVar15) && (uVar11 - 0x101 != uVar15)) &&
                           (uVar11 - 0x100 != uVar15)) goto LAB_0043d107;
                      }
                      bVar17 = true;
                    }
                    if (!bVar17) {
                      puVar10 = (ushort *)(DAT_004e0f38 + (uVar14 & 0xffff) * 2);
                      if ((*puVar10 >> 8 & 0xc0) == 0x40) {
                        iVar13 = (int)(*puVar10 & 0x3ff8) >> 3;
                      }
                      else {
                        iVar13 = 0xffff;
                      }
                      if (iVar13 == 0xffff) goto LAB_0043d156;
LAB_0043d15d:
                      if ((char)(uVar6 >> 8) == '\0') {
                        uVar18 = FUN_0042ece0(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_19;
                      }
                      else {
                        uVar18 = FUN_0042eba4(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_18;
                      }
                      if (cVar3 == '\0') goto LAB_0043d156;
                    }
                  }
LAB_0043cfe1:
                  bVar17 = true;
                }
                else {
                  if (3 < DAT_004e0f48) goto LAB_0043cfe1;
                  if (((uVar14 & 0xff) == 0) || (uVar15 = uVar14 & 0xffff, (int)uVar15 >> 8 == 0))
                  goto LAB_0043d156;
                  if (*(char *)(uVar15 + DAT_00507d74) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + uVar15) & DAT_004e0f42;
                  }
                  if (bVar2 != 0) {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                        || ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ))) || (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043d2ac:
                      bVar17 = false;
                    }
                    else if (DAT_004e0f48 == 1) {
                      bVar17 = uVar1 == local_194;
                    }
                    else {
                      if (uVar1 != local_194) {
                        uVar15 = (uint)uVar1;
                        uVar9 = uVar14 & 0xffff;
                        if (((uVar9 != uVar15 - 1) && (uVar9 != uVar15 - 0x101)) &&
                           (uVar15 - 0x100 != uVar9)) goto LAB_0043d2ac;
                      }
                      bVar17 = true;
                    }
                    if (bVar17) goto LAB_0043d321;
                    puVar10 = (ushort *)(DAT_004e0f38 + (uVar14 & 0xffff) * 2);
                    if ((*puVar10 >> 8 & 0xc0) == 0x40) {
                      local_1e0 = (int)(*puVar10 & 0x3ff8) >> 3;
                    }
                    else {
                      local_1e0 = 0xffff;
                    }
                    if (local_1e0 != 0xffff) {
                      uVar18 = FUN_0042ece0(uVar6,uVar11 & 0xff);
                      uVar6 = extraout_ECX_20;
                      if ((char)uVar18 != '\0') goto LAB_0043d321;
                    }
                    goto LAB_0043d156;
                  }
LAB_0043d321:
                  uVar11 = uVar14 - 1 & 0xffff;
                  if (*(char *)(uVar11 + DAT_00507d74) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + uVar11) & DAT_004e0f42;
                  }
                  if (bVar2 != 0) {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                        || ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ))) || (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043d441:
                      bVar17 = false;
                    }
                    else {
                      local_154 = (ushort)(uVar14 - 1);
                      if (DAT_004e0f48 == 1) {
                        bVar17 = uVar1 == local_154;
                      }
                      else {
                        if (uVar1 != local_154) {
                          uVar11 = (uint)uVar1;
                          uVar15 = uVar14 - 1 & 0xffff;
                          if (((uVar11 - 1 != uVar15) && (uVar11 - 0x101 != uVar15)) &&
                             (uVar11 - 0x100 != uVar15)) goto LAB_0043d441;
                        }
                        bVar17 = true;
                      }
                    }
                    if (bVar17) goto LAB_0043d4bc;
                    iVar13 = DAT_004e0f38 + (uVar14 & 0xffff) * 2;
                    if ((*(ushort *)(iVar13 + -2) >> 8 & 0xc0) == 0x40) {
                      local_1e4 = (int)(*(ushort *)(iVar13 + -2) & 0x3ff8) >> 3;
                    }
                    else {
                      local_1e4 = 0xffff;
                    }
                    if (local_1e4 != 0xffff) {
                      if ((char)(uVar6 >> 8) == '\0') {
                        uVar18 = FUN_0042ece0(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_22;
                      }
                      else {
                        uVar18 = FUN_0042eba4(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_21;
                      }
                      if (cVar3 != '\0') goto LAB_0043d4bc;
                    }
                    goto LAB_0043d156;
                  }
LAB_0043d4bc:
                  uVar11 = uVar14 - 0x101 & 0xffff;
                  if (*(char *)(uVar11 + DAT_00507d74) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + uVar11) & DAT_004e0f42;
                  }
                  if (bVar2 == 0) {
LAB_0043d658:
                    uVar11 = uVar14 - 0x100 & 0xffff;
                    if (*(char *)(DAT_00507d74 + uVar11) == -3) {
                      bVar2 = DAT_004e0f42 & 1;
                    }
                    else {
                      bVar2 = *(byte *)(DAT_00507da8 + uVar11) & DAT_004e0f42;
                    }
                    if (bVar2 == 0) goto LAB_0043cfe1;
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                        || ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ))) || (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043d777:
                      bVar17 = false;
                    }
                    else {
                      local_18c = (ushort)(uVar14 - 0x100);
                      if (DAT_004e0f48 == 1) {
                        bVar17 = uVar1 == local_18c;
                      }
                      else {
                        if (uVar1 != local_18c) {
                          uVar11 = (uint)uVar1;
                          uVar15 = uVar14 - 0x100 & 0xffff;
                          if (((uVar15 != uVar11 - 1) && (uVar15 != uVar11 - 0x101)) &&
                             (uVar11 - 0x100 != uVar15)) goto LAB_0043d777;
                        }
                        bVar17 = true;
                      }
                    }
                    if (bVar17) goto LAB_0043cfe1;
                    iVar13 = DAT_004e0f38 + (uVar14 & 0xffff) * 2;
                    if ((*(ushort *)(iVar13 + -0x200) >> 8 & 0xc0) == 0x40) {
                      iVar13 = (int)(*(ushort *)(iVar13 + -0x200) & 0x3ff8) >> 3;
                    }
                    else {
                      iVar13 = 0xffff;
                    }
                    if (iVar13 != 0xffff) goto LAB_0043d15d;
                  }
                  else {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if (((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                       || (((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ) || (tabela_unidades[DAT_00496304].estado == 0xe)))) {
LAB_0043d5dd:
                      bVar17 = false;
                    }
                    else {
                      local_1b4 = (ushort)(uVar14 - 0x101);
                      if (DAT_004e0f48 == 1) {
                        bVar17 = uVar1 == local_1b4;
                      }
                      else {
                        if (uVar1 != local_1b4) {
                          uVar15 = (uint)uVar1;
                          uVar11 = uVar14 - 0x101 & 0xffff;
                          if (((uVar15 - 1 != uVar11) && (uVar15 - 0x101 != uVar11)) &&
                             (uVar15 - 0x100 != uVar11)) goto LAB_0043d5dd;
                        }
                        bVar17 = true;
                      }
                    }
                    if (bVar17) goto LAB_0043d658;
                    iVar13 = DAT_004e0f38 + (uVar14 & 0xffff) * 2;
                    if ((*(ushort *)(iVar13 + -0x202) >> 8 & 0xc0) == 0x40) {
                      iVar13 = (int)(*(ushort *)(iVar13 + -0x202) & 0x3ff8) >> 3;
                    }
                    else {
                      iVar13 = 0xffff;
                    }
                    if (iVar13 != 0xffff) {
                      if ((char)(uVar6 >> 8) == '\0') {
                        uVar18 = FUN_0042ece0(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_24;
                      }
                      else {
                        uVar18 = FUN_0042eba4(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_23;
                      }
                      if (cVar3 != '\0') goto LAB_0043d658;
                    }
                  }
LAB_0043d156:
                  bVar17 = false;
                }
                if (bVar17) goto LAB_0043e096;
              }
              local_1bc = local_1bc + 1;
              uVar14 = uVar14 + 0x100;
              uVar11 = uVar6;
            }
          }
          if ((uint)uVar12 + (param_2 & 0xff) < (uint)DAT_00497168) {
            local_1cc = 1;
            uVar14 = uVar8 + local_184;
            uVar8 = CONCAT31((int3)((uint)local_184 >> 8),local_1ec);
            while( true ) {
              uVar11 = (uint)uVar12;
              uVar15 = local_1cc & 0xffff;
              if (uVar11 * 2 <= uVar15) break;
              uVar6 = uVar8;
              if ((-1 < (int)((iVar7 + uVar15) - uVar11)) &&
                 ((int)(((param_2 & 0xff) + uVar15) - uVar11) < (int)(uint)DAT_0049716a)) {
                uVar6 = CONCAT22((short)(uVar8 >> 0x10),(ushort)(byte)uVar8);
                if (DAT_004e0f48 == 0) goto LAB_0043d878;
                local_1c0 = (ushort)uVar14;
                if (DAT_004e0f48 < 2) {
                  if (*(char *)((uVar14 & 0xffff) + DAT_00507d74) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + (uVar14 & 0xffff)) & DAT_004e0f42;
                  }
                  if (bVar2 != 0) {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                        || ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ))) || (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043d9a0:
                      bVar17 = false;
                    }
                    else if (DAT_004e0f48 == 1) {
                      bVar17 = uVar1 == local_1c0;
                    }
                    else {
                      if (uVar1 != local_1c0) {
                        uVar8 = (uint)uVar1;
                        uVar11 = uVar14 & 0xffff;
                        if (((uVar11 != uVar8 - 1) && (uVar11 != uVar8 - 0x101)) &&
                           (uVar8 - 0x100 != uVar11)) goto LAB_0043d9a0;
                      }
                      bVar17 = true;
                    }
                    if (!bVar17) {
                      puVar10 = (ushort *)((uVar14 & 0xffff) * 2 + DAT_004e0f38);
                      if ((*puVar10 >> 8 & 0xc0) == 0x40) {
                        iVar13 = (int)(*puVar10 & 0x3ff8) >> 3;
                      }
                      else {
                        iVar13 = 0xffff;
                      }
                      if (iVar13 == 0xffff) goto LAB_0043d9ee;
LAB_0043d9f5:
                      if ((char)(uVar6 >> 8) == '\0') {
                        uVar18 = FUN_0042ece0(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_26;
                      }
                      else {
                        uVar18 = FUN_0042eba4(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_25;
                      }
                      if (cVar3 == '\0') goto LAB_0043d9ee;
                    }
                  }
LAB_0043d878:
                  bVar17 = true;
                }
                else {
                  if (3 < DAT_004e0f48) goto LAB_0043d878;
                  if (((uVar14 & 0xff) == 0) || (uVar11 = uVar14 & 0xffff, (int)uVar11 >> 8 == 0))
                  goto LAB_0043d9ee;
                  if (*(char *)(DAT_00507d74 + uVar11) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(uVar11 + DAT_00507da8) & DAT_004e0f42;
                  }
                  if (bVar2 != 0) {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                        || ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ))) || (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043db5c:
                      bVar17 = false;
                    }
                    else if (DAT_004e0f48 == 1) {
                      bVar17 = uVar1 == local_1c0;
                    }
                    else {
                      if (uVar1 != local_1c0) {
                        uVar11 = (uint)uVar1;
                        uVar15 = uVar14 & 0xffff;
                        if (((uVar15 != uVar11 - 1) && (uVar15 != uVar11 - 0x101)) &&
                           (uVar11 - 0x100 != uVar15)) goto LAB_0043db5c;
                      }
                      bVar17 = true;
                    }
                    if (bVar17) goto LAB_0043dbc9;
                    puVar10 = (ushort *)(DAT_004e0f38 + (uVar14 & 0xffff) * 2);
                    if ((*puVar10 >> 8 & 0xc0) == 0x40) {
                      iVar13 = (int)(*puVar10 & 0x3ff8) >> 3;
                    }
                    else {
                      iVar13 = 0xffff;
                    }
                    if (iVar13 != 0xffff) {
                      uVar18 = FUN_0042ece0(uVar6,uVar8 & 0xff);
                      uVar6 = extraout_ECX_27;
                      if ((char)uVar18 != '\0') goto LAB_0043dbc9;
                    }
                    goto LAB_0043d9ee;
                  }
LAB_0043dbc9:
                  uVar8 = uVar14 - 1 & 0xffff;
                  if (*(char *)(DAT_00507d74 + uVar8) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + uVar8) & DAT_004e0f42;
                  }
                  if (bVar2 != 0) {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if (((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                       || (((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ) || (tabela_unidades[DAT_00496304].estado == 0xe)))) {
LAB_0043dcf4:
                      bVar17 = false;
                    }
                    else {
                      local_1a0 = (ushort)(uVar14 - 1);
                      if (DAT_004e0f48 == 1) {
                        bVar17 = uVar1 == local_1a0;
                      }
                      else {
                        if (uVar1 != local_1a0) {
                          uVar8 = (uint)uVar1;
                          uVar11 = uVar14 - 1 & 0xffff;
                          if (((uVar8 - 1 != uVar11) && (uVar8 - 0x101 != uVar11)) &&
                             (uVar8 - 0x100 != uVar11)) goto LAB_0043dcf4;
                        }
                        bVar17 = true;
                      }
                    }
                    if (bVar17) goto LAB_0043dd65;
                    iVar13 = DAT_004e0f38 + (uVar14 & 0xffff) * 2;
                    if ((*(ushort *)(iVar13 + -2) >> 8 & 0xc0) == 0x40) {
                      iVar13 = (int)(*(ushort *)(iVar13 + -2) & 0x3ff8) >> 3;
                    }
                    else {
                      iVar13 = 0xffff;
                    }
                    if (iVar13 != 0xffff) {
                      if ((char)(uVar6 >> 8) == '\0') {
                        uVar18 = FUN_0042ece0(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_29;
                      }
                      else {
                        uVar18 = FUN_0042eba4(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_28;
                      }
                      if (cVar3 != '\0') goto LAB_0043dd65;
                    }
                    goto LAB_0043d9ee;
                  }
LAB_0043dd65:
                  uVar8 = uVar14 - 0x101 & 0xffff;
                  if (*(char *)(uVar8 + DAT_00507d74) == -3) {
                    bVar2 = DAT_004e0f42 & 1;
                  }
                  else {
                    bVar2 = *(byte *)(DAT_00507da8 + uVar8) & DAT_004e0f42;
                  }
                  if (bVar2 == 0) {
LAB_0043df00:
                    uVar8 = uVar14 - 0x100 & 0xffff;
                    if (*(char *)(uVar8 + DAT_00507d74) == -3) {
                      bVar2 = DAT_004e0f42 & 1;
                    }
                    else {
                      bVar2 = *(byte *)(DAT_00507da8 + uVar8) & DAT_004e0f42;
                    }
                    if (bVar2 == 0) goto LAB_0043d878;
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                        || ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ))) || (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0043e031:
                      bVar17 = false;
                    }
                    else {
                      local_158 = (ushort)(uVar14 - 0x100);
                      if (DAT_004e0f48 == 1) {
                        bVar17 = uVar1 == local_158;
                      }
                      else {
                        if (uVar1 != local_158) {
                          uVar11 = (uint)uVar1;
                          uVar8 = uVar14 - 0x100 & 0xffff;
                          if (((uVar8 != uVar11 - 1) && (uVar8 != uVar11 - 0x101)) &&
                             (uVar11 - 0x100 != uVar8)) goto LAB_0043e031;
                        }
                        bVar17 = true;
                      }
                    }
                    if (bVar17) goto LAB_0043d878;
                    iVar13 = DAT_004e0f38 + (uVar14 & 0xffff) * 2;
                    if ((*(ushort *)(iVar13 + -0x200) >> 8 & 0xc0) == 0x40) {
                      iVar13 = (int)(*(ushort *)(iVar13 + -0x200) & 0x3ff8) >> 3;
                    }
                    else {
                      iVar13 = 0xffff;
                    }
                    if (iVar13 != 0xffff) goto LAB_0043d9f5;
                  }
                  else {
                    uVar1 = tabela_unidades[DAT_00496304].celula_atual;
                    if (((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1))
                       || (((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)
                            ) || (tabela_unidades[DAT_00496304].estado == 0xe)))) {
LAB_0043de86:
                      bVar17 = false;
                    }
                    else {
                      local_1c8 = (ushort)(uVar14 - 0x101);
                      if (DAT_004e0f48 == 1) {
                        bVar17 = uVar1 == local_1c8;
                      }
                      else {
                        if (uVar1 != local_1c8) {
                          uVar11 = (uint)uVar1;
                          uVar8 = uVar14 - 0x101 & 0xffff;
                          if (((uVar11 - 1 != uVar8) && (uVar11 - 0x101 != uVar8)) &&
                             (uVar11 - 0x100 != uVar8)) goto LAB_0043de86;
                        }
                        bVar17 = true;
                      }
                    }
                    if (bVar17) goto LAB_0043df00;
                    iVar13 = (uVar14 & 0xffff) * 2 + DAT_004e0f38;
                    if ((*(ushort *)(iVar13 + -0x202) >> 8 & 0xc0) == 0x40) {
                      iVar13 = (int)(*(ushort *)(iVar13 + -0x202) & 0x3ff8) >> 3;
                    }
                    else {
                      iVar13 = 0xffff;
                    }
                    if (iVar13 != 0xffff) {
                      if ((char)(uVar6 >> 8) == '\0') {
                        uVar18 = FUN_0042ece0(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_31;
                      }
                      else {
                        uVar18 = FUN_0042eba4(uVar6,uVar6 & 0xff);
                        cVar3 = (char)uVar18;
                        uVar6 = extraout_ECX_30;
                      }
                      if (cVar3 != '\0') goto LAB_0043df00;
                    }
                  }
LAB_0043d9ee:
                  bVar17 = false;
                }
                if (bVar17) goto LAB_0043e096;
              }
              local_1cc = local_1cc + 1;
              uVar14 = uVar14 + 0x100;
              uVar8 = uVar6;
            }
          }
          uVar6 = local_1a4 - 1;
          local_184 = local_184 + 2;
          local_188 = (uint)CONCAT21(local_188._2_2_,local_188._1_1_ + '\x01') << 8;
          local_140 = (uint)(byte)(local_140._1_1_ + 2) << 8;
          local_1a4 = uVar6;
        }
      }
      uVar14 = 0xffff;
    }
LAB_0043e096:
    uVar4 = CONCAT31((int3)(uVar6 >> 8),2);
    DAT_004e0f4a = (undefined2)uVar14;
    local_1b8 = CONCAT22(local_1b8._2_2_,DAT_004e0f4a);
    DAT_004e0f4c = 2;
  }
  uVar14 = FUN_0042d4f8(uVar4,local_1b8 & 0xffff);
  uVar5 = (uint3)(uVar14 >> 8);
  if ((char)uVar14 == '\0') {
    DAT_004e0f4c = 7;
    DAT_00496302 = 1;
    iVar7 = (uint)uVar5 << 8;
  }
  else if ((local_1b8 & 0xffff) == 0xffff) {
    iVar7 = (uint)uVar5 << 8;
    DAT_004e0f4c = 6;
    DAT_00496302 = 1;
  }
  else if (local_180 == (ushort)local_1b8) {
    DAT_00496302 = 1;
    DAT_004e0f37 = 1;
    iVar7 = CONCAT31((int3)(CONCAT22((short)(in_EAX >> 0x10),0x100) >> 8),1);
  }
  else {
    DAT_004e0f44 = local_180;
    DAT_004e0f46 = (ushort)local_1b8;
    iVar7 = CONCAT31((int3)(in_EAX >> 8),1);
  }
  return iVar7;
}
