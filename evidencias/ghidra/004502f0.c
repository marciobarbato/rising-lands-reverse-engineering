/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004502f0, entrada 004502f0.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004502f0(char param_1,byte param_2)

{
  bool bVar1;
  UnidadeParcial *pUVar2;
  UnidadeParcial *pUVar3;
  undefined1 uVar4;
  uint in_EAX;
  uint uVar5;
  undefined4 uVar6;
  uint uVar7;
  undefined4 uVar8;
  short *psVar9;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  short *extraout_ECX_02;
  short *extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  undefined4 extraout_ECX_06;
  undefined4 extraout_ECX_07;
  byte bVar10;
  byte bVar12;
  short *psVar11;
  undefined4 extraout_EDX;
  ushort unaff_BX;
  char cVar13;
  undefined8 uVar14;
  short local_2c;
  short local_20 [2];
  byte local_1c;
  undefined4 local_1b;
  byte local_14;
  byte local_10;

  pUVar2 = tabela_unidades;
  uVar5 = in_EAX & 0xffff;
  psVar9 = (short *)(uint)unaff_BX;
  local_1c = param_2;
  if (param_2 < 4) {
    if (param_2 == 0) goto LAB_0045059c;
    if (1 < param_2) {
      if (param_2 == 3) {
        FUN_0041a4f4(psVar9,uVar5);
        uVar7 = FUN_00418b8a(extraout_ECX,1);
        local_1b = CONCAT13((char)uVar7,(undefined3)local_1b);
        uVar14 = FUN_0041a08c(extraout_ECX_00,0x4c);
        local_10 = (byte)uVar14;
        FUN_004829c8(extraout_ECX_01,(char)((ulonglong)uVar14 >> 0x20));
        psVar9 = extraout_ECX_02;
      }
      goto LAB_0045059c;
    }
    local_14 = tabela_unidades[uVar5].tipo_id;
    local_1b._3_1_ =
         tabela_unidades[(int)psVar9].field_0xf7 +
         *(char *)((uint)local_14 +
                  *(int *)((uint)tabela_unidades[(int)psVar9].tipo_id * 4 + DAT_004e199c));
    uVar7 = FUN_00428cc0((uint)psVar9,5);
    local_1b = CONCAT13(local_1b._3_1_ + (char)uVar7,(undefined3)local_1b);
    uVar6 = FUN_004500e4(10,tabela_unidades[(int)psVar9].proprietario_id);
    if ((char)uVar6 != '\0') {
      local_1b = CONCAT13(local_1b._3_1_ + DAT_004965ac,(undefined3)local_1b);
    }
    FUN_004829c8((uint)unaff_BX,0x48);
    psVar9 = extraout_ECX_03;
    psVar11 = extraout_ECX_03;
  }
  else {
    if (4 < param_2) {
      if (7 < param_2) {
        if (param_2 < 9) {
          local_1b = CONCAT13(*(undefined1 *)
                               ((uint)tabela_unidades[uVar5].tipo_id + *(int *)(DAT_004e199c + 0x68)
                               ),(undefined3)local_1b);
        }
        else if ((param_2 == 9) &&
                (cVar13 = (char)(tabela_unidades[uVar5].vida / 2),
                local_1b = CONCAT13(cVar13,(undefined3)local_1b), cVar13 == '\0')) {
          local_1b = CONCAT13(1,(undefined3)local_1b);
        }
      }
      goto LAB_0045059c;
    }
    if (param_1 == '\x1d') {
      uVar4 = DAT_0049716c;
LAB_004504d4:
      local_1b = CONCAT13(uVar4,(undefined3)local_1b);
    }
    else if (param_1 == '\x1e') {
      uVar4 = DAT_0049716e;
      goto LAB_004504d4;
    }
    psVar9 = local_20;
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
      local_20[0] = 1;
      local_2c = 1;
      break;
    case 3:
    case 0xb:
    case 0xc:
    case 0xd:
    case 0xe:
    case 0xf:
    case 0x10:
    case 0x19:
      local_20[0] = 2;
      local_2c = 2;
    }
    if ((local_20[0] == 2) && (local_2c == 2)) {
      local_1b = CONCAT13((char)((int)(((local_1b >> 0x18) + (local_1b >> 0x1f) * -4) -
                                      (uint)((local_1b >> 0x1f) << 1 < 0)) >> 2),
                          (undefined3)local_1b);
    }
    psVar11 = (short *)(uint)unaff_BX;
  }
  local_10 = tabela_unidades[(int)psVar11].proprietario_id;
LAB_0045059c:
  cVar13 = local_1b._3_1_ - pUVar2[uVar5].field_0xf6;
  local_1b = CONCAT13(cVar13,(undefined3)local_1b);
  uVar7 = FUN_00428cc0(CONCAT31((int3)((uint)psVar9 >> 8),cVar13),6);
  pUVar3 = tabela_unidades;
  cVar13 = (char)extraout_ECX_04 - (char)uVar7;
  local_1b._3_1_ = cVar13;
  if (cVar13 < '\0') {
    local_1b._3_1_ = '\x01';
  }
  uVar7 = in_EAX & 0xffff;
  uVar8 = FUN_004766f0(CONCAT31((int3)((uint)extraout_ECX_04 >> 8),cVar13),(uint)DAT_00508041);
  uVar6 = extraout_ECX_05;
  if ((char)uVar8 != '\0') {
    uVar14 = FUN_00440c5d(extraout_ECX_05,extraout_EDX);
    pUVar3[uVar7].field_0xf9 = 0;
    uVar6 = extraout_ECX_06;
    if (*(int *)&pUVar3[uVar7].field_0x104 == -1) {
      FUN_0048aa79(0,(uint)pUVar3[uVar7].tipo_id << 0x10 | 0x100,(uint)uVar14);
      uVar6 = extraout_ECX_07;
    }
  }
  uVar7 = FUN_00467d97(uVar6,3);
  if ((char)uVar7 != '\0') {
    local_1b._3_1_ = local_1b._3_1_ + -1;
  }
  if ((int)local_1b._3_1_ < (int)(uint)pUVar2[uVar5].vida) {
    pUVar2[uVar5].vida = pUVar2[uVar5].vida - (short)local_1b._3_1_;
  }
  else {
    if (local_1c == 1) {
      bVar10 = tabela_unidades[unaff_BX].tipo_id;
      if ((((bVar10 < 6) || (bVar10 < 8)) || (bVar10 < 9)) || ((bVar10 < 0xb || (bVar10 == 0x19))))
      {
        bVar1 = true;
      }
      else {
        bVar1 = false;
      }
      if (bVar1) {
        bVar10 = tabela_unidades[unaff_BX].field_0xaf & 0x1f;
        bVar12 = (byte)tabela_unidades[unaff_BX].field_0xaf >> 5;
        uVar7 = CONCAT11(bVar12,bVar10 + 10) & 0xff;
        if (uVar7 < 10) {
          tabela_unidades[unaff_BX].field_0xaf = bVar12 * ' ' + (bVar10 + 0x14) * '\x02';
        }
        else {
          tabela_unidades[unaff_BX].field_0xaf = tabela_unidades[unaff_BX].field_0xaf & 0xe0;
          FUN_0044fb20(uVar7,bVar12 + 1);
        }
      }
    }
    pUVar2[uVar5].vida = 0;
    if (tabela_unidades[in_EAX & 0xffff].tipo_id == 1) {
      FUN_0046e44c(0,0,0,0,0);
    }
    FUN_00444938();
    FUN_00475118((uint)local_10,(uint)local_10);
  }
  return;
}
