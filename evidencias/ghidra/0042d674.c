/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0042d674, entrada 0042d674.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Removing unreachable block (ram,0x0042daa5) */
/* WARNING: Removing unreachable block (ram,0x0042d900) */
/* WARNING: Removing unreachable block (ram,0x0042e5f8) */
/* WARNING: Removing unreachable block (ram,0x0042e2fe) */
/* WARNING: Removing unreachable block (ram,0x0042e47a) */
/* WARNING: Removing unreachable block (ram,0x0042e170) */

undefined8 __fastcall FUN_0042d674(int *param_1,uint param_2)

{
  ushort uVar1;
  ushort uVar2;
  byte bVar3;
  char cVar4;
  uint in_EAX;
  int iVar5;
  uint uVar6;
  uint uVar7;
  byte *pbVar8;
  ushort *puVar9;
  uint uVar10;
  ushort uVar11;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_ECX_01;
  uint extraout_ECX_02;
  uint extraout_ECX_03;
  uint extraout_ECX_04;
  uint extraout_ECX_05;
  uint extraout_ECX_06;
  uint extraout_ECX_07;
  undefined3 uVar13;
  UnidadeParcial *pUVar12;
  int unaff_EBX;
  int iVar14;
  uint uVar15;
  undefined1 *puVar16;
  ushort uVar17;
  bool bVar18;
  ulonglong uVar19;
  longlong lVar20;
  undefined8 uVar21;
  int local_c0;
  int local_bc;
  int local_b8;
  ushort local_b4;
  ushort local_b0;
  ushort local_ac;
  ushort local_a8;
  char local_7c;
  byte local_74;

  DAT_004e1771 = 0;
  iVar14 = (param_2 & 0xff) - (in_EAX & 0xff);
  iVar5 = ((int)(param_2 & 0xffff) >> 8) - ((int)(in_EAX & 0xffff) >> 8);
  bVar3 = 0 < iVar14;
  if (0 < iVar5) {
    bVar3 = bVar3 + 2;
  }
  if (iVar14 < 0) {
    iVar14 = -iVar14;
  }
  if (iVar5 < 0) {
    iVar5 = -iVar5;
  }
  if (iVar14 == 0) {
    local_74 = (&DAT_0049638c)[bVar3];
  }
  else if (iVar5 == 0) {
    local_74 = (&DAT_00496390)[bVar3];
  }
  else {
    local_74 = (&DAT_00496388)[bVar3];
  }
  iVar14 = (in_EAX & 0xff) + *(int *)(&DAT_00496308 + (uint)local_74 * 8);
  iVar5 = ((int)(in_EAX & 0xffff) >> 8) + *(int *)(&DAT_0049630c + (uint)local_74 * 8);
  if ((((iVar14 < 0) || ((int)(DAT_00497168 - 1) < iVar14)) || (iVar5 < 0)) ||
     ((int)(DAT_0049716a - 1) < iVar5)) {
    uVar6 = 0xffff;
  }
  else {
    uVar6 = iVar5 * 0x100 + iVar14;
  }
  uVar13 = (undefined3)((uint)iVar5 >> 8);
  pUVar12 = (UnidadeParcial *)CONCAT31(uVar13,DAT_004e0f48);
  uVar11 = (ushort)local_74;
  uVar7 = CONCAT22((short)((uint)*(int *)(&DAT_00496308 + (uint)local_74 * 8) >> 0x10),uVar11);
  if (DAT_004e0f48 != 0) {
    uVar17 = (ushort)uVar6;
    if (DAT_004e0f48 < 2) {
      pUVar12 = (UnidadeParcial *)CONCAT31(uVar13,DAT_004e0f42);
      if (*(char *)(DAT_00507d74 + (uVar6 & 0xffff)) == -3) {
        bVar3 = DAT_004e0f42 & 1;
      }
      else {
        pUVar12 = (UnidadeParcial *)(uint)DAT_004e0f42;
        bVar3 = *(byte *)(DAT_00507da8 + (uVar6 & 0xffff)) & DAT_004e0f42;
      }
      if (bVar3 != 0) {
        pUVar12 = tabela_unidades + DAT_00496304;
        uVar1 = pUVar12->celula_atual;
        if ((((pUVar12->field_0xab == '2') && (DAT_004e0f42 == 1)) ||
            ((pUVar12->field_0xab == '\0' && (DAT_004e0f42 == 2)))) || (pUVar12->estado == 0xe)) {
LAB_0042d8a6:
          bVar18 = false;
        }
        else if (DAT_004e0f48 == 1) {
          bVar18 = uVar1 == uVar17;
        }
        else {
          if (uVar1 != uVar17) {
            pUVar12 = (UnidadeParcial *)(uint)uVar1;
            puVar16 = (undefined1 *)(uVar6 & 0xffff);
            if (((&pUVar12[-1].field_0x113 != puVar16) && (&pUVar12[-1].field_0x13 != puVar16)) &&
               (&pUVar12[-1].field_0x14 != puVar16)) goto LAB_0042d8a6;
          }
          bVar18 = true;
        }
        if (!bVar18) {
          puVar9 = (ushort *)(DAT_004e0f38 + (uVar6 & 0xffff) * 2);
          if ((*puVar9 >> 8 & 0xc0) == 0x40) {
            pUVar12 = (UnidadeParcial *)((int)(*puVar9 & 0x3ff8) >> 3);
          }
          else {
            pUVar12 = (UnidadeParcial *)0xffff;
          }
          if (pUVar12 == (UnidadeParcial *)0xffff) goto LAB_0042d8f5;
          uVar19 = FUN_0042ece0(uVar7,(uint)uVar11);
          pUVar12 = (UnidadeParcial *)(uVar19 >> 0x20);
          cVar4 = (char)uVar19;
joined_r0x0042d916:
          if (cVar4 == '\0') goto LAB_0042d784;
        }
      }
    }
    else if (DAT_004e0f48 < 4) {
      if (((char)uVar6 == '\0') ||
         (pUVar12 = (UnidadeParcial *)(uVar6 & 0xffff), (int)pUVar12 >> 8 == 0)) {
LAB_0042d8f5:
        uVar19 = ZEXT48(pUVar12) << 0x20;
        goto LAB_0042d784;
      }
      if ((&pUVar12->proprietario_id)[DAT_00507d74] == 0xfd) {
        bVar3 = DAT_004e0f42 & 1;
      }
      else {
        bVar3 = (&pUVar12->proprietario_id)[DAT_00507da8] & DAT_004e0f42;
      }
      if (bVar3 != 0) {
        uVar1 = tabela_unidades[DAT_00496304].celula_atual;
        if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1)) ||
            ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)))) ||
           (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0042da4c:
          bVar18 = false;
        }
        else if (DAT_004e0f48 == 1) {
          bVar18 = uVar1 == uVar17;
        }
        else {
          if (uVar1 != uVar17) {
            uVar10 = (uint)uVar1;
            uVar15 = uVar6 & 0xffff;
            if (((uVar10 - 1 != uVar15) && (uVar10 - 0x101 != uVar15)) && (uVar10 - 0x100 != uVar15)
               ) goto LAB_0042da4c;
          }
          bVar18 = true;
        }
        if (!bVar18) {
          pUVar12 = (UnidadeParcial *)(DAT_004e0f38 + (uVar6 & 0xffff) * 2);
          uVar1._0_1_ = pUVar12->proprietario_id;
          uVar1._1_1_ = pUVar12->tipo_id;
          if ((uVar1 >> 8 & 0xc0) == 0x40) {
            uVar2._0_1_ = pUVar12->proprietario_id;
            uVar2._1_1_ = pUVar12->tipo_id;
            local_c0 = (int)(uVar2 & 0x3ff8) >> 3;
          }
          else {
            local_c0 = 0xffff;
          }
          if (local_c0 == 0xffff) goto LAB_0042d8f5;
          uVar19 = FUN_0042ece0(uVar7,(uint)uVar11);
          uVar7 = extraout_ECX;
          if ((char)uVar19 == '\0') goto LAB_0042d784;
        }
      }
      if (*(char *)((uint)(ushort)(uVar17 - 1) + DAT_00507d74) == -3) {
        bVar3 = DAT_004e0f42 & 1;
      }
      else {
        bVar3 = *(byte *)(DAT_00507da8 + (uint)(ushort)(uVar17 - 1)) & DAT_004e0f42;
      }
      if (bVar3 != 0) {
        uVar11 = tabela_unidades[DAT_00496304].celula_atual;
        if (((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1)) ||
           (((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)) ||
            (tabela_unidades[DAT_00496304].estado == 0xe)))) {
LAB_0042dbde:
          bVar18 = false;
        }
        else {
          local_a8 = (ushort)(uVar6 - 1);
          if (DAT_004e0f48 == 1) {
            bVar18 = uVar11 == local_a8;
          }
          else {
            if (uVar11 != local_a8) {
              uVar10 = (uint)uVar11;
              uVar15 = uVar6 - 1 & 0xffff;
              if (((uVar10 - 1 != uVar15) && (uVar10 - 0x101 != uVar15)) &&
                 (uVar10 - 0x100 != uVar15)) goto LAB_0042dbde;
            }
            bVar18 = true;
          }
        }
        if (!bVar18) {
          pUVar12 = (UnidadeParcial *)(DAT_004e0f38 + (uVar6 & 0xffff) * 2);
          if ((*(ushort *)&pUVar12[-1].field_0x112 >> 8 & 0xc0) == 0x40) {
            local_bc = (int)(*(ushort *)&pUVar12[-1].field_0x112 & 0x3ff8) >> 3;
          }
          else {
            local_bc = 0xffff;
          }
          if (local_bc == 0xffff) goto LAB_0042d8f5;
          if ((char)(uVar7 >> 8) == '\0') {
            uVar19 = FUN_0042ece0(uVar7,uVar7 & 0xff);
            uVar7 = extraout_ECX_01;
          }
          else {
            uVar19 = FUN_0042eba4(uVar7,uVar7 & 0xff);
            uVar7 = extraout_ECX_00;
          }
          if ((char)uVar19 == '\0') goto LAB_0042d784;
        }
      }
      if (*(char *)((uint)(ushort)(uVar17 - 0x101) + DAT_00507d74) == -3) {
        bVar3 = DAT_004e0f42 & 1;
      }
      else {
        bVar3 = *(byte *)(DAT_00507da8 + (uint)(ushort)(uVar17 - 0x101)) & DAT_004e0f42;
      }
      if (bVar3 != 0) {
        uVar11 = tabela_unidades[DAT_00496304].celula_atual;
        if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1)) ||
            ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)))) ||
           (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0042dd86:
          bVar18 = false;
        }
        else {
          local_b4 = (ushort)(uVar6 - 0x101);
          if (DAT_004e0f48 == 1) {
            bVar18 = uVar11 == local_b4;
          }
          else {
            if (uVar11 != local_b4) {
              uVar10 = (uint)uVar11;
              uVar15 = uVar6 - 0x101 & 0xffff;
              if (((uVar10 - 1 != uVar15) && (uVar10 - 0x101 != uVar15)) &&
                 (uVar10 - 0x100 != uVar15)) goto LAB_0042dd86;
            }
            bVar18 = true;
          }
        }
        if (!bVar18) {
          pUVar12 = (UnidadeParcial *)(DAT_004e0f38 + (uVar6 & 0xffff) * 2);
          if ((*(ushort *)&pUVar12[-2].field_0x26 >> 8 & 0xc0) == 0x40) {
            local_b8 = (int)(*(ushort *)&pUVar12[-2].field_0x26 & 0x3ff8) >> 3;
          }
          else {
            local_b8 = 0xffff;
          }
          if (local_b8 == 0xffff) goto LAB_0042d8f5;
          if ((char)(uVar7 >> 8) == '\0') {
            uVar19 = FUN_0042ece0(uVar7,uVar7 & 0xff);
            uVar7 = extraout_ECX_03;
          }
          else {
            uVar19 = FUN_0042eba4(uVar7,uVar7 & 0xff);
            uVar7 = extraout_ECX_02;
          }
          if ((char)uVar19 == '\0') goto LAB_0042d784;
        }
      }
      pUVar12 = (UnidadeParcial *)(uint)(ushort)(uVar17 - 0x100);
      if ((&pUVar12->proprietario_id)[DAT_00507d74] == 0xfd) {
        bVar3 = DAT_004e0f42 & 1;
      }
      else {
        pbVar8 = &pUVar12->proprietario_id;
        pUVar12 = (UnidadeParcial *)(uint)pbVar8[DAT_00507da8];
        bVar3 = pbVar8[DAT_00507da8] & DAT_004e0f42;
      }
      if (bVar3 != 0) {
        pUVar12 = tabela_unidades + DAT_00496304;
        uVar11 = pUVar12->celula_atual;
        if (((pUVar12->field_0xab == '2') && (DAT_004e0f42 == 1)) ||
           (((pUVar12->field_0xab == '\0' && (DAT_004e0f42 == 2)) || (pUVar12->estado == 0xe)))) {
LAB_0042df2e:
          bVar18 = false;
        }
        else {
          local_b0 = (ushort)(uVar6 - 0x100);
          if (DAT_004e0f48 == 1) {
            bVar18 = uVar11 == local_b0;
          }
          else {
            if (uVar11 != local_b0) {
              pUVar12 = (UnidadeParcial *)(uint)uVar11;
              puVar16 = (undefined1 *)(uVar6 - 0x100 & 0xffff);
              if (((&pUVar12[-1].field_0x113 != puVar16) && (&pUVar12[-1].field_0x13 != puVar16)) &&
                 (&pUVar12[-1].field_0x14 != puVar16)) goto LAB_0042df2e;
            }
            bVar18 = true;
          }
        }
        if (!bVar18) {
          iVar5 = DAT_004e0f38 + (uVar6 & 0xffff) * 2;
          if ((*(ushort *)(iVar5 + -0x200) >> 8 & 0xc0) == 0x40) {
            pUVar12 = (UnidadeParcial *)((int)(*(ushort *)(iVar5 + -0x200) & 0x3ff8) >> 3);
          }
          else {
            pUVar12 = (UnidadeParcial *)0xffff;
          }
          if (pUVar12 != (UnidadeParcial *)0xffff) {
            if ((char)(uVar7 >> 8) == '\0') {
              uVar19 = FUN_0042ece0(uVar7,uVar7 & 0xff);
            }
            else {
              uVar19 = FUN_0042eba4(uVar7,uVar7 & 0xff);
            }
            pUVar12 = (UnidadeParcial *)(uVar19 >> 0x20);
            cVar4 = (char)uVar19;
            goto joined_r0x0042d916;
          }
          goto LAB_0042d8f5;
        }
      }
    }
  }
  uVar19 = CONCAT44(pUVar12,1);
LAB_0042d784:
  uVar6 = (uint)(uVar19 >> 0x20);
  uVar7 = 0;
  if ((uVar19 & 0xff) == 0) {
LAB_0042d78f:
    uVar7 = uVar7 & 0xffffff00;
  }
  else {
    *param_1 = 0;
    uVar7 = CONCAT22((short)(param_2 >> 0x10),(ushort)(byte)param_2);
    local_7c = -1;
    do {
      local_ac = (ushort)param_2;
      uVar11 = (ushort)in_EAX;
      if (uVar11 == local_ac) break;
      uVar7 = in_EAX;
      lVar20 = (ulonglong)uVar6 << 0x20;
      if (DAT_004e0f48 == 0) {
LAB_0042dffa:
        uVar6 = (uint)((ulonglong)lVar20 >> 0x20);
        bVar18 = true;
      }
      else {
        if (DAT_004e0f48 < 2) {
          uVar6 = in_EAX & 0xffff;
          if (*(char *)(uVar6 + DAT_00507d74) == -3) {
            bVar3 = DAT_004e0f42 & 1;
          }
          else {
            pbVar8 = (byte *)(DAT_00507da8 + uVar6);
            uVar6 = (uint)*pbVar8;
            bVar3 = *pbVar8 & DAT_004e0f42;
          }
          lVar20 = (ulonglong)uVar6 << 0x20;
          if (bVar3 != 0) {
            uVar17 = tabela_unidades[DAT_00496304].celula_atual;
            uVar6 = in_EAX;
            if (((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1)) ||
               (((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)) ||
                (tabela_unidades[DAT_00496304].estado == 0xe)))) {
LAB_0042e115:
              uVar10 = 0;
            }
            else if (DAT_004e0f48 == 1) {
              uVar10 = (uint)(uVar17 == uVar11);
            }
            else {
              if (uVar17 != uVar11) {
                uVar10 = (uint)uVar17;
                uVar6 = in_EAX & 0xffff;
                if (((uVar10 - 1 != uVar6) && (uVar10 - 0x101 != uVar6)) &&
                   (uVar10 - 0x100 != uVar6)) goto LAB_0042e115;
              }
              uVar10 = 1;
            }
            lVar20 = CONCAT44(uVar6,uVar10);
            if ((char)uVar10 == '\0') {
              puVar9 = (ushort *)(DAT_004e0f38 + (in_EAX & 0xffff) * 2);
              if ((*puVar9 >> 8 & 0xc0) == 0x40) {
                uVar6 = (int)(*puVar9 & 0x3ff8) >> 3;
              }
              else {
                uVar6 = 0xffff;
              }
              if (uVar6 == 0xffff) goto LAB_0042e15f;
LAB_0042e166:
              lVar20 = FUN_0042ece0(uVar7,(uint)local_74);
              uVar6 = (uint)((ulonglong)lVar20 >> 0x20);
              uVar7 = extraout_ECX_04;
              if ((char)lVar20 == '\0') goto LAB_0042e15f;
            }
          }
          goto LAB_0042dffa;
        }
        lVar20 = (ulonglong)uVar6 << 0x20;
        if (3 < DAT_004e0f48) goto LAB_0042dffa;
        if ((char)in_EAX != '\0') {
          uVar10 = in_EAX & 0xffff;
          uVar6 = 0;
          if ((int)uVar10 >> 8 != 0) {
            if (*(char *)(DAT_00507d74 + uVar10) == -3) {
              bVar3 = DAT_004e0f42 & 1;
            }
            else {
              bVar3 = *(byte *)(uVar10 + DAT_00507da8) & DAT_004e0f42;
            }
            if (bVar3 != 0) {
              uVar17 = tabela_unidades[DAT_00496304].celula_atual;
              if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1)) ||
                  ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)))) ||
                 (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0042e2a5:
                bVar18 = false;
              }
              else if (DAT_004e0f48 == 1) {
                bVar18 = uVar17 == uVar11;
              }
              else {
                if (uVar17 != uVar11) {
                  uVar6 = (uint)uVar17;
                  uVar10 = in_EAX & 0xffff;
                  if (((uVar6 - 1 != uVar10) && (uVar6 - 0x101 != uVar10)) &&
                     (uVar6 - 0x100 != uVar10)) goto LAB_0042e2a5;
                }
                bVar18 = true;
              }
              if (!bVar18) {
                puVar9 = (ushort *)((in_EAX & 0xffff) * 2 + DAT_004e0f38);
                if ((*puVar9 >> 8 & 0xc0) == 0x40) {
                  uVar6 = (int)(*puVar9 & 0x3ff8) >> 3;
                }
                else {
                  uVar6 = 0xffff;
                }
                if (uVar6 != 0xffff) {
                  uVar21 = FUN_0042ece0(in_EAX,(uint)local_74);
                  uVar6 = (uint)((ulonglong)uVar21 >> 0x20);
                  uVar7 = extraout_ECX_05;
                  if ((char)uVar21 != '\0') goto LAB_0042e324;
                }
                goto LAB_0042e15f;
              }
            }
LAB_0042e324:
            uVar6 = in_EAX - 1 & 0xffff;
            if (*(char *)(uVar6 + DAT_00507d74) == -3) {
              bVar3 = DAT_004e0f42 & 1;
            }
            else {
              pbVar8 = (byte *)(uVar6 + DAT_00507da8);
              uVar6 = 0;
              bVar3 = *pbVar8 & DAT_004e0f42;
            }
            if (bVar3 != 0) {
              uVar6 = in_EAX - 1;
              uVar17 = tabela_unidades[DAT_00496304].celula_atual;
              if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1)) ||
                  ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)))) ||
                 (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0042e41f:
                bVar18 = false;
              }
              else if (DAT_004e0f48 == 1) {
                bVar18 = uVar17 == (ushort)uVar6;
              }
              else {
                if (uVar17 != (ushort)uVar6) {
                  uVar10 = (uint)uVar17;
                  uVar15 = uVar6 & 0xffff;
                  uVar6 = uVar10 - 1;
                  if (((uVar6 != uVar15) && (uVar6 = uVar10 - 0x101, uVar6 != uVar15)) &&
                     (uVar10 - 0x100 != uVar15)) goto LAB_0042e41f;
                }
                bVar18 = true;
              }
              if (!bVar18) {
                iVar5 = (in_EAX & 0xffff) * 2 + DAT_004e0f38;
                if ((*(ushort *)(iVar5 + -2) >> 8 & 0xc0) == 0x40) {
                  uVar6 = (int)(*(ushort *)(iVar5 + -2) & 0x3ff8) >> 3;
                }
                else {
                  uVar6 = 0xffff;
                }
                if (uVar6 != 0xffff) {
                  uVar21 = FUN_0042ece0(uVar7,(uint)local_74);
                  uVar6 = (uint)((ulonglong)uVar21 >> 0x20);
                  uVar7 = extraout_ECX_06;
                  if ((char)uVar21 != '\0') goto LAB_0042e4a0;
                }
                goto LAB_0042e15f;
              }
            }
LAB_0042e4a0:
            uVar6 = CONCAT31((int3)(uVar6 >> 8),DAT_004e0f42);
            if (*(char *)((uint)(ushort)(uVar11 - 0x101) + DAT_00507d74) == -3) {
              bVar3 = DAT_004e0f42 & 1;
            }
            else {
              bVar3 = *(byte *)((uint)(ushort)(uVar11 - 0x101) + DAT_00507da8) & DAT_004e0f42;
            }
            if (bVar3 != 0) {
              uVar11 = tabela_unidades[DAT_00496304].celula_atual;
              uVar6 = CONCAT22((short)((uint)tabela_unidades >> 0x10),uVar11);
              if (((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1)) ||
                 (((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)) ||
                  (tabela_unidades[DAT_00496304].estado == 0xe)))) {
LAB_0042e597:
                bVar18 = false;
              }
              else {
                uVar17 = (ushort)(in_EAX - 0x101);
                if (DAT_004e0f48 == 1) {
                  bVar18 = uVar11 == uVar17;
                }
                else {
                  if (uVar11 != uVar17) {
                    uVar10 = (uint)uVar11;
                    uVar6 = in_EAX - 0x101 & 0xffff;
                    if (((uVar10 - 1 != uVar6) && (uVar10 - 0x101 != uVar6)) &&
                       (uVar10 - 0x100 != uVar6)) goto LAB_0042e597;
                  }
                  bVar18 = true;
                }
              }
              if (!bVar18) {
                iVar5 = DAT_004e0f38 + (in_EAX & 0xffff) * 2;
                if ((*(ushort *)(iVar5 + -0x202) >> 8 & 0xc0) == 0x40) {
                  uVar6 = (int)(*(ushort *)(iVar5 + -0x202) & 0x3ff8) >> 3;
                }
                else {
                  uVar6 = 0xffff;
                }
                if (uVar6 != 0xffff) {
                  uVar21 = FUN_0042ece0(uVar7,(uint)local_74);
                  uVar6 = (uint)((ulonglong)uVar21 >> 0x20);
                  uVar7 = extraout_ECX_07;
                  if ((char)uVar21 != '\0') goto LAB_0042e61e;
                }
                goto LAB_0042e15f;
              }
            }
LAB_0042e61e:
            uVar10 = in_EAX - 0x100 & 0xffff;
            if (*(char *)(DAT_00507d74 + uVar10) == -3) {
              bVar3 = DAT_004e0f42 & 1;
            }
            else {
              bVar3 = *(byte *)(DAT_00507da8 + uVar10) & DAT_004e0f42;
            }
            lVar20 = (ulonglong)CONCAT31((int3)(uVar6 >> 8),DAT_004e0f42) << 0x20;
            if (bVar3 != 0) {
              uVar11 = tabela_unidades[DAT_00496304].celula_atual;
              uVar6 = CONCAT22((short)((uint)tabela_unidades >> 0x10),uVar11);
              if ((((tabela_unidades[DAT_00496304].field_0xab == '2') && (DAT_004e0f42 == 1)) ||
                  ((tabela_unidades[DAT_00496304].field_0xab == '\0' && (DAT_004e0f42 == 2)))) ||
                 (tabela_unidades[DAT_00496304].estado == 0xe)) {
LAB_0042e725:
                uVar10 = 0;
              }
              else {
                uVar17 = (ushort)(in_EAX - 0x100);
                if (DAT_004e0f48 == 1) {
                  uVar10 = (uint)(uVar11 == uVar17);
                }
                else {
                  if (uVar11 != uVar17) {
                    uVar6 = (uint)uVar11;
                    uVar10 = in_EAX - 0x100 & 0xffff;
                    if (((uVar6 - 1 != uVar10) && (uVar6 - 0x101 != uVar10)) &&
                       (uVar6 = uVar6 - 0x100, uVar6 != uVar10)) goto LAB_0042e725;
                  }
                  uVar10 = 1;
                }
              }
              lVar20 = CONCAT44(uVar6,uVar10);
              if ((char)uVar10 == '\0') {
                iVar5 = (in_EAX & 0xffff) * 2 + DAT_004e0f38;
                if ((*(ushort *)(iVar5 + -0x200) >> 8 & 0xc0) == 0x40) {
                  uVar6 = (int)(*(ushort *)(iVar5 + -0x200) & 0x3ff8) >> 3;
                }
                else {
                  uVar6 = 0xffff;
                }
                if (uVar6 != 0xffff) goto LAB_0042e166;
                goto LAB_0042e15f;
              }
            }
            goto LAB_0042dffa;
          }
        }
LAB_0042e15f:
        bVar18 = false;
      }
      if (!bVar18) {
        uVar7 = 0;
        goto LAB_0042e886;
      }
      iVar5 = *param_1;
      *param_1 = iVar5 + 1;
      *(short *)(unaff_EBX + iVar5 * 2) = (short)uVar7;
      iVar5 = (uint)(ushort)(byte)param_2 - (uVar7 & 0xff);
      iVar14 = ((int)(param_2 & 0xffff) >> 8) - ((int)(uVar7 & 0xffff) >> 8);
      bVar3 = 0 < iVar5;
      if (0 < iVar14) {
        bVar3 = bVar3 + 2;
      }
      if (iVar5 < 0) {
        iVar5 = -iVar5;
      }
      if (iVar14 < 0) {
        iVar14 = -iVar14;
      }
      if (iVar5 == 0) {
        local_74 = (&DAT_0049638c)[bVar3];
      }
      else if (iVar14 == 0) {
        local_74 = (&DAT_00496390)[bVar3];
      }
      else {
        local_74 = (&DAT_00496388)[bVar3];
      }
      iVar5 = (uVar7 & 0xff) + *(int *)(&DAT_00496308 + (uint)local_74 * 8);
      uVar6 = ((int)(uVar7 & 0xffff) >> 8) + *(int *)(&DAT_0049630c + (uint)local_74 * 8);
      if (((iVar5 < 0) || ((int)(DAT_00497168 - 1) < iVar5)) ||
         (((int)uVar6 < 0 || ((int)(DAT_0049716a - 1) < (int)uVar6)))) {
        in_EAX = 0xffff;
      }
      else {
        uVar6 = uVar6 * 0x100;
        in_EAX = iVar5 + uVar6;
      }
      uVar7 = in_EAX & 0xffff;
      if (uVar7 == 0xffff) goto LAB_0042d78f;
      local_7c = local_7c + -1;
      uVar6 = CONCAT22((short)(uVar6 >> 0x10),CONCAT11(local_7c,(char)uVar6));
    } while (local_7c != '\0');
    uVar7 = CONCAT31((int3)(uVar7 >> 8),1);
  }
LAB_0042e886:
  return CONCAT44(uVar6,uVar7);
}
