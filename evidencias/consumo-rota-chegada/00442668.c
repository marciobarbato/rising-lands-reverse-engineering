/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall OriginaisSBL::EnginPeutPasser(int param_1,ushort param_2)

{
  bool bVar1;
  uint in_EAX;
  undefined3 extraout_var;
  int iVar2;
  uint uVar3;
  UnidadeParcial *pUVar4;
  undefined3 extraout_var_00;
  uint3 uVar5;
  byte bVar7;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_ECX_01;
  uint uVar6;
  uint extraout_ECX_02;
  uint extraout_ECX_03;
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
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 extraout_EDX_02;
  undefined4 extraout_EDX_03;
  byte unaff_BL;
  bool bVar8;
  undefined8 uVar9;

  bVar7 = tabela_unidades[in_EAX & 0xffff].tipo_id;
  pUVar4 = (UnidadeParcial *)CONCAT31((int3)((uint)tabela_unidades >> 8),bVar7);
  uVar6 = CONCAT22((short)((uint)param_1 >> 0x10),1);
  if (bVar7 < 0xc) {
    if (bVar7 < 4) {
      bVar1 = bVar7 < 2;
      bVar8 = bVar7 == 2;
    }
    else {
      if ((bVar7 < 6) || (bVar7 < 9)) goto LAB_004426c7;
      bVar1 = bVar7 < 10;
      bVar8 = bVar7 == 10;
    }
    if (bVar1 || bVar8) goto LAB_004426c7;
LAB_00442b94:
    if (((uint)param_2 % 0x100 == 0) || (param_2 / 0x100 == 0)) {
      return 0;
    }
    iVar2 = EnginOccupeCase(uVar6,param_2);
    uVar6 = extraout_ECX_02;
    if (((char)iVar2 == '\0') &&
       (bVar1 = TerrainEnCollision(extraout_ECX_02,unaff_BL), uVar6 = extraout_ECX_03, bVar1)) {
      uVar9 = ChercheIndiceEngin(extraout_ECX_03,extraout_EDX_00);
      uVar6 = extraout_ECX_04;
      if (param_1 != 0) {
        bVar7 = (byte)(extraout_ECX_04 >> 8);
        uVar6 = CONCAT22((short)(extraout_ECX_04 >> 0x10),CONCAT11(bVar7 + 1,(char)extraout_ECX_04))
        ;
        *(short *)(param_1 + (uint)bVar7 * 2) = (short)uVar9;
      }
      bVar7 = tabela_unidades[in_EAX & 0xffff].tipo_id;
      if ((bVar7 < 0xc) || ((0xc < bVar7 && (bVar7 != 0xf)))) {
        bVar1 = false;
      }
      else {
        bVar1 = true;
      }
      if (((bVar1) && (uVar3 = (uint)uVar9 & 0xffff, uVar3 != 0xffff)) &&
         (tabela_unidades[in_EAX & 0xffff].proprietario_id != tabela_unidades[uVar3].proprietario_id
         )) {
        bVar7 = tabela_unidades[uVar3].tipo_id;
        if (bVar7 < 0x10) {
          if (0xb < bVar7) goto LAB_00442807;
          if (2 < bVar7) {
            if (3 < bVar7) {
              bVar1 = bVar7 == 0xb;
              goto LAB_00442801;
            }
            goto LAB_00442807;
          }
LAB_00442803:
          bVar1 = true;
        }
        else {
          if (0x11 < bVar7) {
            if (bVar7 < 0x17) {
              if (bVar7 < 0x14) goto LAB_00442803;
              if (0x14 < bVar7) {
                bVar1 = bVar7 == 0x15;
                goto LAB_00442801;
              }
            }
            else if ((0x17 < bVar7) && (0x18 < bVar7)) {
              bVar1 = bVar7 == 0x19;
LAB_00442801:
              if (!bVar1) goto LAB_00442803;
            }
          }
LAB_00442807:
          bVar1 = false;
        }
        if (bVar1) goto LAB_00442829;
      }
      uVar6 = uVar6 & 0xffffff00;
    }
LAB_00442829:
    iVar2 = EnginOccupeCase(uVar6,param_2 - 1);
    uVar6 = extraout_ECX_05;
    if (((char)iVar2 == '\0') &&
       (bVar1 = TerrainEnCollision(extraout_ECX_05,unaff_BL), uVar6 = extraout_ECX_06, bVar1)) {
      uVar9 = ChercheIndiceEngin(extraout_ECX_06,extraout_EDX_01);
      uVar6 = extraout_ECX_07;
      if (param_1 != 0) {
        bVar7 = (byte)(extraout_ECX_07 >> 8);
        uVar6 = CONCAT22((short)(extraout_ECX_07 >> 0x10),CONCAT11(bVar7 + 1,(char)extraout_ECX_07))
        ;
        *(short *)(param_1 + (uint)bVar7 * 2) = (short)uVar9;
      }
      bVar7 = tabela_unidades[in_EAX & 0xffff].tipo_id;
      if ((bVar7 < 0xc) || ((0xc < bVar7 && (bVar7 != 0xf)))) {
        bVar1 = false;
      }
      else {
        bVar1 = true;
      }
      if (((bVar1) && (uVar3 = (uint)uVar9 & 0xffff, uVar3 != 0xffff)) &&
         (tabela_unidades[in_EAX & 0xffff].proprietario_id != tabela_unidades[uVar3].proprietario_id
         )) {
        bVar7 = tabela_unidades[uVar3].tipo_id;
        if (bVar7 < 0x10) {
          if (0xb < bVar7) goto LAB_0044291b;
          if (2 < bVar7) {
            if (3 < bVar7) {
              bVar1 = bVar7 == 0xb;
              goto LAB_00442915;
            }
            goto LAB_0044291b;
          }
LAB_00442917:
          bVar1 = true;
        }
        else {
          if (0x11 < bVar7) {
            if (bVar7 < 0x17) {
              if (bVar7 < 0x14) goto LAB_00442917;
              if (0x14 < bVar7) {
                bVar1 = bVar7 == 0x15;
                goto LAB_00442915;
              }
            }
            else if ((0x17 < bVar7) && (0x18 < bVar7)) {
              bVar1 = bVar7 == 0x19;
LAB_00442915:
              if (!bVar1) goto LAB_00442917;
            }
          }
LAB_0044291b:
          bVar1 = false;
        }
        if (bVar1) goto LAB_0044293d;
      }
      uVar6 = uVar6 & 0xffffff00;
    }
LAB_0044293d:
    iVar2 = EnginOccupeCase(uVar6,param_2 - 0x101);
    uVar6 = extraout_ECX_08;
    if (((char)iVar2 == '\0') &&
       (bVar1 = TerrainEnCollision(extraout_ECX_08,unaff_BL), uVar6 = extraout_ECX_09, bVar1)) {
      uVar9 = ChercheIndiceEngin(extraout_ECX_09,extraout_EDX_02);
      uVar6 = extraout_ECX_10;
      if (param_1 != 0) {
        bVar7 = (byte)(extraout_ECX_10 >> 8);
        uVar6 = CONCAT22((short)(extraout_ECX_10 >> 0x10),CONCAT11(bVar7 + 1,(char)extraout_ECX_10))
        ;
        *(short *)(param_1 + (uint)bVar7 * 2) = (short)uVar9;
      }
      bVar7 = tabela_unidades[in_EAX & 0xffff].tipo_id;
      if ((bVar7 < 0xc) || ((0xc < bVar7 && (bVar7 != 0xf)))) {
        bVar1 = false;
      }
      else {
        bVar1 = true;
      }
      if (((bVar1) && (uVar3 = (uint)uVar9 & 0xffff, uVar3 != 0xffff)) &&
         (tabela_unidades[in_EAX & 0xffff].proprietario_id != tabela_unidades[uVar3].proprietario_id
         )) {
        bVar7 = tabela_unidades[uVar3].tipo_id;
        if (bVar7 < 0x10) {
          if (0xb < bVar7) goto LAB_00442a34;
          if (2 < bVar7) {
            if (3 < bVar7) {
              bVar1 = bVar7 == 0xb;
              goto LAB_00442a2e;
            }
            goto LAB_00442a34;
          }
LAB_00442a30:
          bVar1 = true;
        }
        else {
          if (0x11 < bVar7) {
            if (bVar7 < 0x17) {
              if (bVar7 < 0x14) goto LAB_00442a30;
              if (0x14 < bVar7) {
                bVar1 = bVar7 == 0x15;
                goto LAB_00442a2e;
              }
            }
            else if ((0x17 < bVar7) && (0x18 < bVar7)) {
              bVar1 = bVar7 == 0x19;
LAB_00442a2e:
              if (!bVar1) goto LAB_00442a30;
            }
          }
LAB_00442a34:
          bVar1 = false;
        }
        if (bVar1) goto LAB_00442a56;
      }
      uVar6 = uVar6 & 0xffffff00;
    }
LAB_00442a56:
    pUVar4 = (UnidadeParcial *)EnginOccupeCase(uVar6,param_2 - 0x100);
    uVar6 = extraout_ECX_11;
    if ((char)pUVar4 != '\0') goto LAB_00442719;
    bVar1 = TerrainEnCollision(extraout_ECX_11,unaff_BL);
    pUVar4 = (UnidadeParcial *)CONCAT31(extraout_var_00,bVar1);
    uVar6 = extraout_ECX_12;
    if (!bVar1) goto LAB_00442719;
    uVar9 = ChercheIndiceEngin(extraout_ECX_12,extraout_EDX_03);
    if (param_1 != 0) {
      *(short *)(param_1 + (extraout_ECX_13 >> 8 & 0xff) * 2) = (short)uVar9;
    }
    bVar7 = tabela_unidades[in_EAX & 0xffff].tipo_id;
    uVar5 = (uint3)((uint)tabela_unidades >> 8);
    if ((bVar7 < 0xc) || ((0xc < bVar7 && (bVar7 != 0xf)))) {
      pUVar4 = (UnidadeParcial *)((uint)uVar5 << 8);
    }
    else {
      pUVar4 = (UnidadeParcial *)CONCAT31(uVar5,1);
    }
    if ((((char)pUVar4 == '\0') ||
        (pUVar4 = (UnidadeParcial *)((uint)uVar9 & 0xffff), pUVar4 == (UnidadeParcial *)0xffff)) ||
       (pUVar4 = tabela_unidades + (int)pUVar4,
       pUVar4->proprietario_id == tabela_unidades[in_EAX & 0xffff].proprietario_id))
    goto LAB_00442717;
    bVar7 = pUVar4->tipo_id;
    uVar5 = (uint3)((uint)pUVar4 >> 8);
    if (bVar7 < 0x10) {
      if (0xb < bVar7) goto LAB_00442b46;
      if (2 < bVar7) {
        if (3 < bVar7) {
          bVar1 = bVar7 == 0xb;
          goto LAB_00442b40;
        }
        goto LAB_00442b46;
      }
LAB_00442b42:
      pUVar4 = (UnidadeParcial *)CONCAT31(uVar5,1);
    }
    else {
      if (0x11 < bVar7) {
        if (bVar7 < 0x17) {
          if (bVar7 < 0x14) goto LAB_00442b42;
          if (0x14 < bVar7) {
            bVar1 = bVar7 == 0x15;
            goto LAB_00442b40;
          }
        }
        else if ((0x17 < bVar7) && (0x18 < bVar7)) {
          bVar1 = bVar7 == 0x19;
LAB_00442b40:
          if (!bVar1) goto LAB_00442b42;
        }
      }
LAB_00442b46:
      pUVar4 = (UnidadeParcial *)((uint)uVar5 << 8);
    }
    uVar6 = extraout_ECX_13;
    if ((char)pUVar4 != '\0') goto LAB_00442719;
  }
  else {
    if (bVar7 < 0x10) goto LAB_00442b94;
    if (bVar7 < 0x13) {
      if (0x10 < bVar7) goto LAB_004426c7;
      goto LAB_00442b94;
    }
    if (((0x13 < bVar7) && (0x16 < bVar7)) && (0x18 < bVar7)) {
      if (bVar7 != 0x19) goto LAB_00442719;
      goto LAB_00442b94;
    }
LAB_004426c7:
    pUVar4 = (UnidadeParcial *)EnginOccupeCase(uVar6,param_2);
    uVar6 = extraout_ECX;
    if ((char)pUVar4 != '\0') goto LAB_00442719;
    bVar1 = TerrainEnCollision(extraout_ECX,unaff_BL);
    pUVar4 = (UnidadeParcial *)CONCAT31(extraout_var,bVar1);
    uVar6 = extraout_ECX_00;
    if (!bVar1) goto LAB_00442719;
    uVar9 = ChercheIndiceEngin(extraout_ECX_00,extraout_EDX);
    pUVar4 = (UnidadeParcial *)uVar9;
    if (param_1 != 0) {
      *(short *)(param_1 + (extraout_ECX_01 >> 8 & 0xff) * 2) = (short)uVar9;
    }
  }
LAB_00442717:
  uVar6 = 0;
LAB_00442719:
  return CONCAT31((int3)((uint)pUVar4 >> 8),(char)uVar6);
}
