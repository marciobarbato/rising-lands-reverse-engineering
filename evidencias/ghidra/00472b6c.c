/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00472b6c, entrada 00472b6c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_00472b6c(undefined4 param_1,undefined1 param_2)

{
  char cVar1;
  char cVar2;
  bool bVar3;
  byte bVar4;
  uint in_EAX;
  uint uVar5;
  undefined3 extraout_var;
  undefined3 extraout_var_00;
  uint extraout_ECX;
  uint extraout_ECX_00;
  undefined4 extraout_ECX_01;
  uint extraout_ECX_02;
  uint extraout_ECX_03;
  uint3 uVar7;
  undefined2 uVar8;
  uint extraout_ECX_04;
  uint extraout_ECX_05;
  uint extraout_ECX_06;
  undefined4 extraout_ECX_07;
  uint uVar6;
  uint extraout_ECX_08;
  uint extraout_ECX_09;
  uint extraout_ECX_10;
  undefined4 extraout_ECX_11;
  uint extraout_ECX_12;
  uint extraout_ECX_13;
  uint extraout_ECX_14;
  uint extraout_ECX_15;
  uint extraout_ECX_16;
  uint extraout_ECX_17;
  undefined2 extraout_var_01;
  uint extraout_ECX_18;
  undefined4 extraout_ECX_19;
  undefined4 extraout_ECX_20;
  uint extraout_ECX_21;
  uint extraout_ECX_22;
  ushort indice_unidade;
  ushort indice_unidade_00;
  int iVar9;
  uint uVar10;
  ushort unaff_BX;
  ushort uVar11;
  longlong lVar12;
  undefined8 uVar13;

  cVar1 = (char)in_EAX;
  uVar6 = CONCAT31(CONCAT21((short)((uint)param_1 >> 0x10),param_2),cVar1);
  uVar5 = in_EAX;
  for (uVar11 = 0; iVar9 = (uVar6 & 0xff) * 0x200, uVar11 < *(ushort *)(&DAT_00508728 + iVar9);
      uVar11 = uVar11 + 1) {
    lVar12 = FUN_00443dad(uVar6,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar11 * 2 + iVar9));
    uVar5 = (uint)lVar12;
    uVar6 = extraout_ECX;
    if (((char)lVar12 != '\0') &&
       (uVar5 = FUN_0044fffe(extraout_ECX), uVar6 = extraout_ECX_00, (char)uVar5 != '\0')) {
      uVar5 = CONCAT31((int3)(uVar5 >> 8),1);
      goto LAB_00472bbd;
    }
  }
  uVar5 = uVar5 & 0xffffff00;
LAB_00472bbd:
  if (((char)uVar5 != '\0') || (bVar4 = (byte)(uVar6 >> 8), bVar4 == 0)) goto LAB_004730a6;
  if (bVar4 < 2) {
    bVar4 = unidade_obter_tipo(unaff_BX);
    uVar5 = (uint)bVar4;
    if (uVar5 != 0x10) {
      unidade_obter_tipo(indice_unidade);
      uVar5 = FUN_00442434();
      if ((char)uVar5 != '\0') {
        uVar6 = (uint)CONCAT21(extraout_var_01,cVar1) << 8;
        for (uVar11 = 0; iVar9 = (uVar6 >> 8 & 0xff) * 0x200,
            uVar11 < *(ushort *)(&DAT_00508728 + iVar9); uVar11 = uVar11 + 1) {
          lVar12 = FUN_00443dad(uVar6,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar11 * 2 + iVar9));
          uVar5 = (uint)lVar12;
          uVar6 = extraout_ECX_18;
          if ((char)lVar12 != '\0') {
            unidade_obter_tipo((ushort)((ulonglong)lVar12 >> 0x20));
            cVar2 = FUN_00442347();
            uVar5 = CONCAT31(extraout_var_00,cVar2);
            if (cVar2 == '\0') {
              uVar6 = 0;
              break;
            }
            uVar6 = CONCAT31((int3)((uint)extraout_ECX_19 >> 8),1);
          }
        }
        if ((char)uVar6 != '\0') {
          bVar4 = unidade_obter_tipo(unaff_BX);
          uVar5 = (uint)bVar4;
          if (uVar5 != 0x11) goto LAB_00472f1e;
          bVar4 = unidade_obter_tipo(indice_unidade_00);
          uVar5 = (uint)bVar4;
          if (uVar5 != 0x11) goto LAB_004730a6;
          uVar6 = CONCAT31((int3)((uint)extraout_ECX_20 >> 8),cVar1);
          uVar5 = 0;
          for (uVar11 = 0; iVar9 = (uVar6 & 0xff) * 0x200,
              uVar11 < *(ushort *)(&DAT_00508728 + iVar9); uVar11 = uVar11 + 1) {
            lVar12 = FUN_00443dad(uVar6,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar11 * 2 + iVar9))
            ;
            uVar5 = (uint)lVar12;
            uVar6 = extraout_ECX_21;
            if ((char)lVar12 != '\0') {
              bVar4 = unidade_obter_tipo((ushort)((ulonglong)lVar12 >> 0x20));
              uVar5 = (uint)bVar4;
              uVar6 = extraout_ECX_22;
              if (uVar5 == 8) {
                uVar5 = 1;
                goto LAB_0047308b;
              }
            }
          }
          uVar5 = uVar5 & 0xffffff00;
LAB_0047308b:
          bVar3 = (char)uVar5 == '\0';
LAB_00472f18:
          if (bVar3) goto LAB_00472f1e;
        }
      }
    }
LAB_004730a6:
    uVar5 = uVar5 & 0xffffff00;
  }
  else {
    if (bVar4 != 3) goto LAB_004730a6;
    uVar13 = FUN_0041a4f4(uVar6,(uint)unaff_BX);
    bVar4 = (byte)uVar13;
    uVar13 = FUN_0041a08c(extraout_ECX_01,(int)((ulonglong)uVar13 >> 0x20));
    if (((char)uVar13 == cVar1) || (uVar6 = extraout_ECX_02, ((uint)uVar13 & 0xff) == 200)) {
      uVar6 = (uint)CONCAT21((short)(extraout_ECX_02 >> 0x10),cVar1) << 8;
      uVar5 = 0;
      while (iVar9 = (uVar6 >> 8 & 0xff) * 0x200, (ushort)uVar5 < *(ushort *)(&DAT_00508728 + iVar9)
            ) {
        uVar11 = *(ushort *)(&DAT_0050872a + (uVar5 & 0xffff) * 2 + iVar9);
        lVar12 = FUN_00443dad(uVar6,uVar5);
        uVar6 = extraout_ECX_03;
        if ((char)lVar12 != '\0') {
          uVar7 = (uint3)(extraout_ECX_03 >> 8);
          if (tabela_unidades[uVar11].tipo_id != 9) {
            uVar6 = (uint)uVar7 << 8;
            break;
          }
          uVar6 = CONCAT31(uVar7,1);
        }
        uVar5 = (int)((ulonglong)lVar12 >> 0x20) + 1;
      }
      if (((char)uVar6 == '\0') || (uVar5 = (uint)bVar4, uVar5 == 9)) goto LAB_00472c56;
      goto LAB_00472f1e;
    }
LAB_00472c56:
    uVar8 = (undefined2)(uVar6 >> 0x10);
    if ((char)uVar13 != cVar1) {
      uVar5 = (uint)bVar4;
      if (uVar5 == 0x10) {
        uVar6 = (uint)CONCAT21(uVar8,cVar1) << 8;
        for (uVar11 = 0; iVar9 = (uVar6 >> 8 & 0xff) * 0x200,
            uVar11 < *(ushort *)(&DAT_00508728 + iVar9); uVar11 = uVar11 + 1) {
          lVar12 = FUN_00443dad(uVar6,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar11 * 2 + iVar9));
          iVar9 = (int)((ulonglong)lVar12 >> 0x20);
          uVar5 = (uint)lVar12;
          uVar6 = extraout_ECX_17;
          if ((char)lVar12 != '\0') {
            uVar5 = iVar9 * 0x114;
            if (tabela_unidades[iVar9].tipo_id != 10) {
              uVar6 = 0;
              break;
            }
            uVar6 = CONCAT31((int3)(extraout_ECX_17 >> 8),1);
          }
        }
        if ((char)uVar6 != '\0') goto LAB_00472f1e;
      }
      goto LAB_004730a6;
    }
    if (bVar4 == 0x15) {
      uVar6 = CONCAT31(CONCAT21(uVar8,cVar1),cVar1);
      uVar5 = 0;
      for (uVar11 = 0; iVar9 = (uVar6 & 0xff) * 0x200, uVar11 < *(ushort *)(&DAT_00508728 + iVar9);
          uVar11 = uVar11 + 1) {
        lVar12 = FUN_00443dad(uVar6,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar11 * 2 + iVar9));
        uVar5 = (uint)lVar12;
        uVar6 = extraout_ECX_04;
        if ((char)lVar12 != '\0') {
          unidade_obter_tipo((ushort)((ulonglong)lVar12 >> 0x20));
          cVar2 = FUN_004423b0();
          uVar5 = CONCAT31(extraout_var,cVar2);
          uVar6 = extraout_ECX_05;
          if (cVar2 == '\0') goto LAB_00472cbd;
        }
      }
      uVar5 = CONCAT31((int3)(uVar5 >> 8),1);
LAB_00472cbd:
      uVar8 = (undefined2)(uVar6 >> 0x10);
      if ((char)uVar5 != '\0') goto LAB_00472f1e;
    }
    uVar6 = (uint)CONCAT21(uVar8,cVar1) << 8;
    for (uVar11 = 0; iVar9 = (uVar6 >> 8 & 0xff) * 0x200,
        uVar11 < *(ushort *)(&DAT_00508728 + iVar9); uVar11 = uVar11 + 1) {
      lVar12 = FUN_00443dad(uVar6,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar11 * 2 + iVar9));
      uVar6 = extraout_ECX_06;
      if ((char)lVar12 != '\0') {
        unidade_obter_tipo((ushort)((ulonglong)lVar12 >> 0x20));
        cVar2 = FUN_00442347();
        uVar7 = (uint3)((uint)extraout_ECX_07 >> 8);
        if (cVar2 == '\0') {
          uVar6 = (uint)uVar7 << 8;
          break;
        }
        uVar6 = CONCAT31(uVar7,1);
      }
    }
    if ((char)uVar6 != '\0') {
      uVar5 = (uint)bVar4;
      if (uVar5 == 2) goto LAB_00472f1e;
      if (uVar5 == 0x13) {
        uVar6 = 0;
        for (uVar11 = 0; iVar9 = (in_EAX & 0xff) * 0x200,
            uVar11 < *(ushort *)(&DAT_00508728 + iVar9); uVar11 = uVar11 + 1) {
          lVar12 = FUN_00443dad(uVar6,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar11 * 2 + iVar9));
          uVar6 = extraout_ECX_08;
          if (((char)lVar12 != '\0') &&
             (bVar3 = unidade_vida_diferente_do_maximo((ushort)((ulonglong)lVar12 >> 0x20)),
             uVar6 = extraout_ECX_09, bVar3)) {
            uVar6 = extraout_ECX_09 + 1;
          }
        }
        uVar10 = uVar6 & 0xffff;
        uVar5 = CONCAT31((int3)(uVar10 >> 8),uVar10 != 0);
        if (uVar10 != 0) goto LAB_00472f1e;
      }
    }
    if (bVar4 != 0xe) {
LAB_00472eb2:
      if (bVar4 == 0x12) {
        uVar6 = (uint)CONCAT21((short)(uVar6 >> 0x10),cVar1) << 8;
        uVar5 = 0;
        uVar10 = 0;
        while (iVar9 = (uVar6 >> 8 & 0xff) * 0x200,
              (ushort)uVar10 < *(ushort *)(&DAT_00508728 + iVar9)) {
          uVar11 = *(ushort *)(&DAT_0050872a + (uVar10 & 0xffff) * 2 + iVar9);
          lVar12 = FUN_00443dad(uVar6,uVar10);
          uVar5 = (uint)lVar12;
          uVar6 = extraout_ECX_16;
          if ((char)lVar12 != '\0') {
            uVar5 = (uint)uVar11 * 0x114;
            if (tabela_unidades[uVar11].tipo_id != 0x10) {
              uVar6 = 0;
              break;
            }
            uVar6 = CONCAT31((int3)(extraout_ECX_16 >> 8),1);
          }
          uVar10 = (int)((ulonglong)lVar12 >> 0x20) + 1;
        }
        if ((char)uVar6 != '\0') goto LAB_00472f1e;
      }
      uVar5 = (uint)bVar4;
      bVar3 = uVar5 == 8;
      goto LAB_00472f18;
    }
    uVar6 = (uint)CONCAT21((short)(uVar6 >> 0x10),cVar1) << 8;
    for (uVar11 = 0; iVar9 = (uVar6 >> 8 & 0xff) * 0x200,
        uVar11 < *(ushort *)(&DAT_00508728 + iVar9); uVar11 = uVar11 + 1) {
      lVar12 = FUN_00443dad(uVar6,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar11 * 2 + iVar9));
      uVar6 = extraout_ECX_10;
      if ((char)lVar12 != '\0') {
        unidade_obter_tipo((ushort)((ulonglong)lVar12 >> 0x20));
        uVar5 = FUN_00442434();
        uVar7 = (uint3)((uint)extraout_ECX_11 >> 8);
        if ((char)uVar5 == '\0') {
          uVar6 = (uint)uVar7 << 8;
          break;
        }
        uVar6 = CONCAT31(uVar7,1);
      }
    }
    if ((char)uVar6 == '\0') goto LAB_00472eb2;
    uVar6 = 0;
    for (uVar11 = 0; iVar9 = (in_EAX & 0xff) * 0x200, uVar11 < *(ushort *)(&DAT_00508728 + iVar9);
        uVar11 = uVar11 + 1) {
      lVar12 = FUN_00443dad(uVar6,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar11 * 2 + iVar9));
      uVar6 = extraout_ECX_12;
      if (((char)lVar12 != '\0') &&
         (bVar3 = unidade_vida_diferente_do_maximo((ushort)((ulonglong)lVar12 >> 0x20)),
         uVar6 = extraout_ECX_13, bVar3)) {
        uVar6 = extraout_ECX_13 + 1;
      }
    }
    uVar6 = uVar6 & 0xffff;
    uVar5 = CONCAT31((int3)(uVar6 >> 8),uVar6 != 0);
    if (uVar6 == 0) {
      uVar6 = 0;
      for (uVar11 = 0; iVar9 = (in_EAX & 0xff) * 0x200, uVar11 < *(ushort *)(&DAT_00508728 + iVar9);
          uVar11 = uVar11 + 1) {
        lVar12 = FUN_00443dad(uVar6,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar11 * 2 + iVar9));
        uVar6 = extraout_ECX_14;
        if (((char)lVar12 != '\0') &&
           (uVar13 = FUN_0044841b(extraout_ECX_14,(int)((ulonglong)lVar12 >> 0x20)),
           uVar6 = extraout_ECX_15, (char)uVar13 == '\0')) {
          uVar6 = extraout_ECX_15 + 1;
        }
      }
      uVar10 = uVar6 & 0xffff;
      uVar5 = CONCAT31((int3)(uVar10 >> 8),uVar10 != 0);
      if (uVar10 == 0) goto LAB_00472eb2;
    }
LAB_00472f1e:
    uVar5 = CONCAT31((int3)(uVar5 >> 8),1);
  }
  return uVar5;
}
