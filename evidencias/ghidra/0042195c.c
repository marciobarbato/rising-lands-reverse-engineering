/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0042195c, entrada 0042195c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Removing unreachable block (ram,0x004225e9) */
/* WARNING: Removing unreachable block (ram,0x00421d65) */
/* WARNING: Removing unreachable block (ram,0x0042216f) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 __fastcall FUN_0042195c(uint param_1,undefined4 param_2)

{
  char cVar1;
  ushort uVar2;
  UnidadeParcial *pUVar3;
  byte bVar4;
  uint in_EAX;
  int iVar5;
  uint3 uVar10;
  undefined *puVar6;
  int iVar7;
  UnidadeParcial *pUVar8;
  uint uVar9;
  uint extraout_ECX;
  int extraout_ECX_00;
  undefined4 extraout_ECX_01;
  uint extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 uVar11;
  int extraout_ECX_04;
  undefined4 extraout_ECX_05;
  uint extraout_ECX_06;
  undefined4 extraout_ECX_07;
  uint extraout_ECX_08;
  int *extraout_ECX_09;
  uint extraout_ECX_10;
  uint extraout_ECX_11;
  undefined4 extraout_ECX_12;
  int extraout_ECX_13;
  uint extraout_ECX_14;
  undefined4 extraout_ECX_15;
  undefined4 extraout_ECX_16;
  int *extraout_ECX_17;
  undefined4 extraout_ECX_18;
  int extraout_ECX_19;
  undefined4 extraout_EDX;
  bool bVar12;
  float10 fVar13;
  undefined8 uVar14;
  int local_4c [2];
  int local_44;
  int local_40 [2];
  int local_38;
  undefined2 local_2c [2];
  undefined2 local_28 [6];
  uint local_1c;

  iVar5 = (in_EAX & 0xffff) * 0x114;
  pUVar8 = (UnidadeParcial *)CONCAT31((int3)((uint)iVar5 >> 8),(&DAT_0049a143)[iVar5] + -0xb);
  switch((&DAT_0049a143)[iVar5] + -0xb) {
  case '\0':
    uVar2 = *(ushort *)(&DAT_0049a146 + iVar5);
    pUVar8 = (UnidadeParcial *)(uint)uVar2;
    if (uVar2 != 0) {
      if (1 < uVar2) {
        if (uVar2 != 2) goto switchD_00421997_default;
        uVar9 = FUN_00442668(0,*(short *)(&DAT_0049a0ca + iVar5) + 0x402);
        uVar11 = extraout_ECX_03;
        if ((char)uVar9 != '\0') {
          iVar7 = (in_EAX & 0xffff) * 0x114;
          if (((&DAT_0049a13e)[iVar7] == '\a') && ((&DAT_0049a13d)[iVar7] != '\0')) {
            bVar12 = true;
          }
          else {
            bVar12 = false;
          }
          if (bVar12) {
            pUVar8 = (UnidadeParcial *)(*(int *)(&DAT_0049a148 + iVar5) >> 0x10);
            if ((int)pUVar8 < -10) {
LAB_00421d0f:
              *(short *)(&DAT_0049a14a + iVar5) = *(short *)(&DAT_0049a14a + iVar5) + 4;
              goto switchD_00421997_default;
            }
LAB_004220aa:
            iVar7 = (in_EAX & 0xffff) * 0x114;
            pUVar8 = (UnidadeParcial *)(&DAT_0049a0c8 + iVar7);
            (&DAT_0049a13d)[iVar7] = 0;
            FUN_00445fbc(uVar11,*(short *)(&DAT_0049a0ca + iVar5) + 0x402);
            *(undefined2 *)(&DAT_0049a140 + iVar7) = 0xffff;
            (&DAT_0049a143)[iVar7] = 0xff;
            *(undefined2 *)(&DAT_0049a144 + iVar7) = 0;
            *(undefined2 *)(&DAT_0049a146 + iVar7) = 0;
            *(undefined2 *)(&DAT_0049a14e + iVar7) = 0xffff;
            if ((&DAT_0049a0d0)[iVar7] != '\x14') {
              *(undefined2 *)(&DAT_0049a148 + iVar7) = 0;
              *(undefined2 *)(&DAT_0049a14a + iVar7) = 0;
            }
            goto LAB_00422122;
          }
        }
LAB_00421d1c:
        pUVar8 = (UnidadeParcial *)FUN_00443470(uVar11,(uint)*(ushort *)(&DAT_0049a150 + iVar5));
        goto switchD_00421997_default;
      }
      iVar7 = (in_EAX & 0xffff) * 0x114;
      uVar10 = (uint3)((uint)(&DAT_0049a0c8 + iVar7) >> 8);
      if (((&DAT_0049a13e)[iVar7] == '\0') && ((&DAT_0049a13d)[iVar7] == '\0')) {
        pUVar8 = (UnidadeParcial *)CONCAT31(uVar10,1);
      }
      else {
        pUVar8 = (UnidadeParcial *)((uint)uVar10 << 8);
      }
      if ((char)pUVar8 == '\0') goto switchD_00421997_default;
      if (((&DAT_004dfb54)[(byte)(&DAT_0049a0cc)[iVar5]] != '\0') ||
         (uVar14 = FUN_00441108(param_1,0), param_1 = extraout_ECX,
         (uint)(CONCAT22((short)((ulonglong)uVar14 >> 0x30),(short)uVar14) * 100) <=
         *(uint *)(&DAT_0049a154 + iVar5))) {
        if ((&DAT_004dfb54)[(byte)(&DAT_0049a0cc)[iVar5]] == '\0') {
          uVar14 = FUN_00441108(param_1,0);
          tabela_unidades
          [CONCAT22((short)((ulonglong)uVar14 >> 0x30),*(undefined2 *)(&DAT_0049a150 + iVar5))].vida
               = (ushort)uVar14;
          param_1 = extraout_ECX_02;
        }
        (&DAT_004dfb54)[(byte)(&DAT_0049a0cc)[iVar5]] = 0;
        FUN_004570f4(param_1,0xd);
        iVar7 = (in_EAX & 0xffff) * 0x114;
        pUVar8 = (UnidadeParcial *)(&DAT_0049a0c8 + iVar7);
        (&DAT_0049a13d)[iVar7] = 1;
        *(short *)(&DAT_0049a146 + iVar5) = *(short *)(&DAT_0049a146 + iVar5) + 1;
        *(short *)(&DAT_0049a148 + iVar5) = *(short *)(&DAT_0049a148 + iVar5) + 2;
        goto switchD_00421997_default;
      }
      pUVar8 = (UnidadeParcial *)(DAT_00508f7c / 0x4b);
      if (DAT_00508f7c % 0x4b != 0) goto switchD_00421997_default;
      FUN_004471b8(&DAT_0049a0c8 + (in_EAX & 0xffff) * 0x114,'\x01');
      bVar4 = *(byte *)(extraout_ECX_00 + 8);
      if (bVar4 < 0xe) {
LAB_00421b1e:
        bVar4 = (&DAT_00495d9e)[(uint)*(byte *)(extraout_ECX_00 + 8) * 0x34];
      }
      else if (bVar4 < 0xf) {
        bVar4 = (&DAT_00495d9e)[(uint)bVar4 * 0x34] - 1;
      }
      else {
        if (bVar4 != 0x13) goto LAB_00421b1e;
        bVar4 = cRam0049617a - DAT_00495be8;
      }
      local_1c = (uint)bVar4;
      fVar13 = FUN_0048c43e();
      *(uint *)(&DAT_0049a154 + iVar5) =
           *(int *)(&DAT_0049a154 + iVar5) + ((int)ROUND(fVar13) & 0xffffU) + 300;
      uVar9 = FUN_00423f9d(extraout_ECX_01,(uint)(byte)(&DAT_0049a150)[iVar5]);
      tabela_unidades[*(ushort *)(&DAT_0049a150 + iVar5)].vida = (ushort)uVar9;
      goto LAB_00421bf6;
    }
    iVar7 = (in_EAX & 0xffff) * 0x114;
    uVar10 = (uint3)((uint)(&DAT_0049a0c8 + iVar7) >> 8);
    if (((&DAT_0049a13e)[iVar7] == '\a') && ((&DAT_0049a13d)[iVar7] != '\0')) {
      pUVar8 = (UnidadeParcial *)CONCAT31(uVar10,1);
    }
    else {
      pUVar8 = (UnidadeParcial *)((uint)uVar10 << 8);
    }
    if ((char)pUVar8 == '\0') goto switchD_00421997_default;
    iVar7 = *(int *)(&DAT_0049a148 + iVar5);
joined_r0x00421d90:
    pUVar8 = (UnidadeParcial *)(iVar7 >> 0x10);
    if (-0x50 < (int)pUVar8) {
      *(short *)(&DAT_0049a14a + iVar5) = *(short *)(&DAT_0049a14a + iVar5) + -4;
      goto switchD_00421997_default;
    }
    iVar7 = (in_EAX & 0xffff) * 0x114;
    (&DAT_0049a13d)[iVar7] = 0;
    break;
  case '\x01':
  case '\x03':
  case '\x04':
    uVar2 = *(ushort *)(&DAT_0049a146 + iVar5);
    pUVar8 = (UnidadeParcial *)(uint)uVar2;
    if (uVar2 == 0) {
      iVar7 = (in_EAX & 0xffff) * 0x114;
      puVar6 = &DAT_0049a0c8 + iVar7;
      if ((&DAT_0049a13e)[iVar7] == '\a') {
        cVar1 = (&DAT_0049a13d)[iVar7];
LAB_00421d78:
        if (cVar1 == '\0') goto LAB_00421dbc;
        pUVar8 = (UnidadeParcial *)CONCAT31((int3)((uint)puVar6 >> 8),1);
      }
      else {
LAB_00421dbc:
        pUVar8 = (UnidadeParcial *)((uint)puVar6 & 0xffffff00);
      }
      if ((char)pUVar8 == '\0') goto switchD_00421997_default;
      iVar7 = *(int *)(&DAT_0049a148 + iVar5);
      goto joined_r0x00421d90;
    }
    if (1 < uVar2) {
      if (uVar2 != 2) goto switchD_00421997_default;
      uVar9 = FUN_00442668(0,*(short *)(&DAT_0049a0ca + iVar5) + 0x402);
      uVar11 = extraout_ECX_15;
      if ((char)uVar9 != '\0') {
        iVar7 = (in_EAX & 0xffff) * 0x114;
        if (((&DAT_0049a13e)[iVar7] == '\a') && ((&DAT_0049a13d)[iVar7] != '\0')) {
          bVar12 = true;
        }
        else {
          bVar12 = false;
        }
        if (bVar12) {
          pUVar8 = (UnidadeParcial *)(*(int *)(&DAT_0049a148 + iVar5) >> 0x10);
          bVar12 = false;
          pUVar3 = pUVar8;
LAB_004220a4:
          if (bVar12 != (int)pUVar3 < 0) goto LAB_00421d0f;
          goto LAB_004220aa;
        }
      }
      goto LAB_00421d1c;
    }
    iVar7 = (in_EAX & 0xffff) * 0x114;
    uVar10 = (uint3)((uint)(&DAT_0049a0c8 + iVar7) >> 8);
    if (((&DAT_0049a13e)[iVar7] == '\0') && ((&DAT_0049a13d)[iVar7] == '\0')) {
      pUVar8 = (UnidadeParcial *)CONCAT31(uVar10,1);
    }
    else {
      pUVar8 = (UnidadeParcial *)((uint)uVar10 << 8);
    }
    if ((char)pUVar8 == '\0') goto switchD_00421997_default;
    if (((&DAT_004dfb54)[(byte)(&DAT_0049a0cc)[iVar5]] == '\0') &&
       (uVar14 = FUN_00441108(param_1,0), param_1 = extraout_ECX_08,
       *(uint *)(&DAT_0049a154 + iVar5) <
       (uint)(CONCAT22((short)((ulonglong)uVar14 >> 0x30),(short)uVar14) * 100))) {
      pUVar8 = (UnidadeParcial *)(DAT_00508f7c / 0x4b);
      if (DAT_00508f7c % 0x4b != 0) goto switchD_00421997_default;
      iVar7 = (in_EAX & 0xffff) * 0x114;
      FUN_004471b8(&DAT_0049a154 + iVar5,'\x01');
      bVar4 = (&DAT_0049a0d0)[iVar7];
      if (bVar4 < 0xe) {
LAB_004222d1:
        bVar4 = (&DAT_00495d9e)[(uint)(byte)(&DAT_0049a0d0)[iVar7] * 0x34];
      }
      else if (bVar4 < 0xf) {
        bVar4 = (&DAT_00495d9e)[(uint)bVar4 * 0x34] - 1;
      }
      else {
        if (bVar4 != 0x13) goto LAB_004222d1;
        bVar4 = cRam0049617a - DAT_00495be8;
      }
      local_1c = (uint)bVar4;
      fVar13 = FUN_0048c43e();
      *extraout_ECX_09 = *extraout_ECX_09 + ((int)ROUND(fVar13) & 0xffffU) + 300;
      uVar9 = FUN_00423f9d(extraout_ECX_09,(uint)(byte)(&DAT_0049a150)[iVar5]);
      pUVar8 = (UnidadeParcial *)((uint)*(ushort *)(&DAT_0049a150 + iVar5) * 0x45);
      tabela_unidades[*(ushort *)(&DAT_0049a150 + iVar5)].vida = (ushort)uVar9;
      goto switchD_00421997_default;
    }
    if ((((&DAT_004dfb54)[(byte)(&DAT_0049a0cc)[iVar5]] == '\0') &&
        (bVar4 = unidade_obter_tipo(*(ushort *)(&DAT_0049a150 + iVar5)), param_1 = extraout_ECX_10,
        bVar4 == 0xe)) &&
       (uVar14 = FUN_0044841b(extraout_ECX_10,extraout_EDX), param_1 = extraout_ECX_11,
       (char)uVar14 == '\0')) {
      iVar7 = FUN_004676e5(0,2,(&DAT_0049a0cc)[iVar5]);
      if ((char)iVar7 == '\0') {
        pUVar8 = (UnidadeParcial *)(uint)(byte)(&DAT_0049a0cc)[iVar5];
        pUVar8[0x4854].field_0xc4 = 1;
        goto switchD_00421997_default;
      }
      pUVar8 = (UnidadeParcial *)(DAT_00508f7c / 0x4b);
      if (DAT_00508f7c % 0x4b != 0) goto switchD_00421997_default;
      FUN_004483aa();
      iVar5 = CONCAT31((int3)((uint)extraout_ECX_12 >> 8),(&DAT_0049a0cc)[iVar5]);
      FUN_0046792c(iVar5,2);
      iVar5 = (iVar5 * 4 - extraout_ECX_13) * 2;
      pUVar8 = (UnidadeParcial *)0x0;
      if (*(short *)(&DAT_004dfb2c + iVar5) == 0) goto switchD_00421997_default;
      FUN_0046769d(local_2c,(short *)local_40,(byte)extraout_ECX_13);
      uVar2 = *(ushort *)(&DAT_004dfb2c + iVar5);
      uVar9 = local_38 + local_40[0];
      goto LAB_00422491;
    }
    if ((&DAT_004dfb54)[(byte)(&DAT_0049a0cc)[iVar5]] == '\0') {
      uVar14 = FUN_00441108(param_1,0);
      tabela_unidades
      [CONCAT22((short)((ulonglong)uVar14 >> 0x30),*(undefined2 *)(&DAT_0049a150 + iVar5))].vida =
           (ushort)uVar14;
      param_1 = extraout_ECX_14;
    }
    (&DAT_004dfb54)[(byte)(&DAT_0049a0cc)[iVar5]] = 0;
    FUN_004570f4(param_1,0xd);
    iVar7 = (in_EAX & 0xffff) * 0x114;
    (&DAT_0049a13d)[iVar7] = 1;
    break;
  case '\x02':
    uVar2 = *(ushort *)(&DAT_0049a146 + iVar5);
    pUVar8 = (UnidadeParcial *)(uint)uVar2;
    if (uVar2 == 0) {
      puVar6 = (undefined *)(uint)(byte)(&DAT_0049a13e)[iVar5];
      if (puVar6 == (undefined *)0x7) {
        cVar1 = (&DAT_0049a13d)[iVar5];
        goto LAB_00421d78;
      }
      goto LAB_00421dbc;
    }
    if (1 < uVar2) {
      if (uVar2 != 2) goto switchD_00421997_default;
      uVar9 = FUN_00442668(0,*(short *)(&DAT_0049a0ca + iVar5) + 0x402);
      uVar11 = extraout_ECX_07;
      if ((char)uVar9 != '\0') {
        if (((&DAT_0049a13e)[iVar5] == '\a') && ((&DAT_0049a13d)[iVar5] != '\0')) {
          bVar12 = true;
        }
        else {
          bVar12 = false;
        }
        if (bVar12) {
          pUVar8 = (UnidadeParcial *)(*(int *)(&DAT_0049a148 + iVar5) >> 0x10);
          bVar12 = SBORROW4((int)pUVar8,-0xc);
          pUVar3 = (UnidadeParcial *)&pUVar8->campo_0c;
          goto LAB_004220a4;
        }
      }
      goto LAB_00421d1c;
    }
    if (((&DAT_0049a13e)[iVar5] == '\0') && ((&DAT_0049a13d)[iVar5] == '\0')) {
      pUVar8 = (UnidadeParcial *)0x1;
    }
    else {
      pUVar8 = (UnidadeParcial *)0x0;
    }
    if ((char)pUVar8 == '\0') goto switchD_00421997_default;
    if ((&DAT_004dfb54)[(byte)(&DAT_0049a0cc)[iVar5]] == '\0') {
      uVar14 = FUN_00441108(param_1,0);
      param_1 = *(uint *)(&DAT_0049a154 + iVar5);
      if (param_1 < (uint)(CONCAT22((short)((ulonglong)uVar14 >> 0x30),(short)uVar14) * 100)) {
        pUVar8 = (UnidadeParcial *)(DAT_00508f7c / 0x4b);
        if (DAT_00508f7c % 0x4b != 0) goto switchD_00421997_default;
        FUN_004471b8(&DAT_0049a0c8 + (in_EAX & 0xffff) * 0x114,'\x01');
        bVar4 = *(byte *)(extraout_ECX_04 + 8);
        if (bVar4 < 0xe) {
LAB_00421ed4:
          bVar4 = (&DAT_00495d9e)[(uint)*(byte *)(extraout_ECX_04 + 8) * 0x34];
        }
        else if (bVar4 < 0xf) {
          bVar4 = (&DAT_00495d9e)[(uint)bVar4 * 0x34] - 1;
        }
        else {
          if (bVar4 != 0x13) goto LAB_00421ed4;
          bVar4 = cRam0049617a - DAT_00495be8;
        }
        local_1c = (uint)bVar4;
        fVar13 = FUN_0048c43e();
        *(uint *)(&DAT_0049a154 + iVar5) =
             *(int *)(&DAT_0049a154 + iVar5) + ((int)ROUND(fVar13) & 0xffffU) + 300;
        uVar9 = FUN_00423f9d(extraout_ECX_05,(uint)(byte)(&DAT_0049a150)[iVar5]);
        pUVar8 = tabela_unidades;
        tabela_unidades[*(ushort *)(&DAT_0049a150 + iVar5)].vida = (ushort)uVar9;
        goto switchD_00421997_default;
      }
    }
    if ((&DAT_004dfb54)[(byte)(&DAT_0049a0cc)[iVar5]] == '\0') {
      uVar14 = FUN_00441108(param_1,0);
      tabela_unidades
      [CONCAT22((short)((ulonglong)uVar14 >> 0x30),*(undefined2 *)(&DAT_0049a150 + iVar5))].vida =
           (ushort)uVar14;
      param_1 = extraout_ECX_06;
    }
    (&DAT_004dfb54)[(byte)(&DAT_0049a0cc)[iVar5]] = 0;
    FUN_004570f4(CONCAT22((short)(param_1 >> 0x10),(ushort)(byte)param_1),0xd);
    iVar7 = (in_EAX & 0xffff) * 0x114;
    (&DAT_0049a13d)[iVar7] = 1;
    pUVar8 = (UnidadeParcial *)
             (CONCAT22((short)((uint)(&DAT_0049a0c8 + iVar7) >> 0x10),
                       *(undefined2 *)(&DAT_0049a148 + iVar5)) + -0xc);
    *(short *)(&DAT_0049a146 + iVar5) = *(short *)(&DAT_0049a146 + iVar5) + 1;
    *(short *)(&DAT_0049a148 + iVar5) = (short)pUVar8;
    goto switchD_00421997_default;
  case '\x05':
    uVar14 = FUN_00441108(param_1,0);
    iVar7 = CONCAT22((short)((ulonglong)uVar14 >> 0x30),(short)uVar14);
    if ((uint)(iVar7 * 100) <= *(uint *)(&DAT_0049a154 + iVar5)) {
      uVar14 = FUN_0044841b(extraout_ECX_16,iVar7);
      if ((char)uVar14 == '\0') {
        pUVar8 = (UnidadeParcial *)FUN_004676e5(0,2,(&DAT_0049a0cc)[iVar5]);
        if (((char)pUVar8 == '\0') ||
           (pUVar8 = (UnidadeParcial *)(DAT_00508f7c / 0x19), DAT_00508f7c % 0x19 != 0))
        goto switchD_00421997_default;
        FUN_004483aa();
        iVar5 = CONCAT31((int3)((uint)extraout_ECX_18 >> 8),(&DAT_0049a0cc)[iVar5]);
        FUN_0046792c(iVar5,2);
        iVar5 = (iVar5 * 4 - extraout_ECX_19) * 2;
        pUVar8 = (UnidadeParcial *)0x0;
        if (*(short *)(&DAT_004dfb2c + iVar5) == 0) goto switchD_00421997_default;
        FUN_0046769d(local_28,(short *)local_4c,(byte)extraout_ECX_19);
        uVar2 = *(ushort *)(&DAT_004dfb2c + iVar5);
        uVar9 = local_44 + local_4c[0];
LAB_00422491:
        pUVar8 = (UnidadeParcial *)
                 ((((uVar9 & 0xffff) / (uint)uVar2) * 7) / (uint)*(ushort *)(&DAT_004dfb2e + iVar5))
        ;
        (&DAT_004dfb30)[iVar5] = (char)pUVar8;
        goto switchD_00421997_default;
      }
      *(undefined2 *)(&DAT_0049a140 + iVar5) = 0xffff;
      (&DAT_0049a143)[iVar5] = 0xff;
      *(undefined2 *)(&DAT_0049a144 + iVar5) = 0;
      *(undefined2 *)(&DAT_0049a146 + iVar5) = 0;
      *(undefined2 *)(&DAT_0049a14e + iVar5) = 0xffff;
      pUVar8 = (UnidadeParcial *)(&DAT_0049a0c8 + iVar5);
      if ((&DAT_0049a0d0)[iVar5] != '\x14') {
        *(undefined2 *)(&DAT_0049a148 + iVar5) = 0;
        *(undefined2 *)(&DAT_0049a14a + iVar5) = 0;
      }
LAB_00422122:
      pUVar8->field_0x74 = 0;
      *(undefined4 *)&pUVar8->field_0x8c = 0;
      if (pUVar8->field_0x5 != '\x03') {
        pUVar8->field_0x5 = 5;
      }
      goto switchD_00421997_default;
    }
    pUVar8 = (UnidadeParcial *)(DAT_00508f7c / 0x4b);
    if (DAT_00508f7c % 0x4b != 0) goto switchD_00421997_default;
    FUN_004471b8(&DAT_0049a154 + iVar5,'\x01');
    bVar4 = (&DAT_0049a0d0)[iVar5];
    if (bVar4 < 0xe) {
LAB_004226ac:
      bVar4 = (&DAT_00495d9e)[(uint)(byte)(&DAT_0049a0d0)[iVar5] * 0x34];
    }
    else if (bVar4 < 0xf) {
      bVar4 = (&DAT_00495d9e)[(uint)bVar4 * 0x34] - 1;
    }
    else {
      if (bVar4 != 0x13) goto LAB_004226ac;
      bVar4 = cRam0049617a - DAT_00495be8;
    }
    local_1c = (uint)bVar4;
    fVar13 = FUN_0048c43e();
    *extraout_ECX_17 = *extraout_ECX_17 + ((int)ROUND(fVar13) & 0xffffU) + 300;
    uVar9 = FUN_00423f9d(extraout_ECX_17,(uint)(byte)(&DAT_0049a150)[iVar5]);
    tabela_unidades[*(ushort *)(&DAT_0049a150 + iVar5)].vida = (ushort)uVar9;
LAB_00421bf6:
    pUVar8 = (UnidadeParcial *)FUN_0041b1c6(uVar9);
  default:
    goto switchD_00421997_default;
  }
  pUVar8 = (UnidadeParcial *)(&DAT_0049a0c8 + iVar7);
  *(short *)(&DAT_0049a146 + iVar5) = *(short *)(&DAT_0049a146 + iVar5) + 1;
switchD_00421997_default:
  return CONCAT44(param_2,pUVar8);
}
