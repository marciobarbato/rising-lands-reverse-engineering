/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004408b7, entrada 004408b7.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_004408b7(void)

{
  byte bVar1;
  ushort uVar2;
  char cVar3;
  int iVar4;
  undefined4 uVar5;
  char extraout_CL;
  char extraout_CL_00;
  char extraout_CL_01;
  char extraout_CL_02;
  char extraout_CL_03;
  char extraout_CL_04;
  char extraout_CL_05;
  char extraout_CL_06;
  char extraout_CL_07;
  char extraout_CL_08;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 uVar6;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  undefined4 extraout_ECX_06;
  undefined4 extraout_ECX_07;
  undefined4 extraout_ECX_08;
  uint extraout_ECX_09;
  undefined4 extraout_ECX_10;
  undefined4 extraout_ECX_11;
  uint extraout_ECX_12;
  undefined4 extraout_ECX_13;
  undefined4 extraout_ECX_14;
  undefined4 extraout_ECX_15;
  undefined4 extraout_ECX_16;
  undefined4 extraout_ECX_17;
  undefined4 extraout_ECX_18;
  undefined4 extraout_ECX_19;
  undefined4 extraout_ECX_20;
  undefined4 extraout_ECX_21;
  undefined4 extraout_ECX_22;
  undefined4 extraout_ECX_23;
  undefined4 extraout_ECX_24;
  undefined4 extraout_ECX_25;
  undefined4 extraout_ECX_26;
  undefined4 extraout_ECX_27;
  undefined4 extraout_ECX_28;
  short sVar7;
  short sVar8;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 extraout_EDX_02;
  short sVar9;
  uint uVar10;
  uint uVar11;
  UnidadeParcial *pUVar12;
  char local_88 [52];
  uint local_54;
  uint local_50;
  uint local_4c;
  uint local_48;
  uint local_44;
  uint local_40;
  uint local_3c;
  uint local_38;
  uint local_34;
  uint local_30;
  uint local_2c;
  int local_28;
  ushort local_24;
  undefined2 uStack_22;
  int local_20;
  byte local_1c;

  if (DAT_004e17b8 == 0) {
    return;
  }
  if (1 < DAT_004e17b8) {
    if (DAT_004e17b8 == 3) {
      FUN_00401040();
      return;
    }
    return;
  }
  local_2c = (uint)DAT_004963c0;
  if (local_2c == 0xffff) {
    return;
  }
  pUVar12 = tabela_unidades + local_2c;
  local_24 = (ushort)((int)(DAT_0049a016._2_2_ - 300) / 2);
  iVar4 = (int)(DAT_0049a01a - 300) / 2;
  uVar2 = (ushort)iVar4;
  local_30 = (uint)(short)uVar2;
  local_54 = (uint)(short)local_24;
  FUN_0045c912(uVar2 + 300,uVar2,1,'\x01');
  local_20 = CONCAT22(local_20._2_2_,local_24 + 1);
  FUN_0045cc35((int)(short)(uVar2 + 299),(int)(short)(uVar2 + 1),'\x01');
  FUN_00459454(uVar2 + 0x14,(short)local_30,0x4944a4,1,'\x01','\x01');
  local_24 = local_24 + 0x1e;
  local_54 = iVar4 + 0x1eU & 0xffff;
  local_30 = (uint)local_24;
  FUN_004591c8('\0',(short)(iVar4 + 0x1eU));
  FUN_0048c38b(extraout_ECX,local_88);
  FUN_004591c8('\0',(short)local_54);
  local_34 = iVar4 + 0x28U & 0xffff;
  FUN_004591c8('\0',(short)(iVar4 + 0x28U));
  bVar1 = pUVar12->proprietario_id;
  if ((((bVar1 < 2) || (bVar1 < 3)) || (bVar1 < 4)) || ((bVar1 < 5 || (bVar1 == 200)))) {
    FUN_004591c8('\0',(short)local_34);
  }
  FUN_004591c8('\0',uVar2 + 0x32);
  local_28 = CONCAT22(uStack_22,local_24) + 0x50;
  uVar10 = iVar4 + 0x3c;
  uVar6 = extraout_ECX_00;
  for (local_1c = 0; sVar8 = (short)uVar10, local_1c < 4; local_1c = local_1c + 1) {
    if (local_1c != pUVar12->proprietario_id) {
      uVar5 = FUN_0046d838(uVar6,local_1c);
      uVar6 = extraout_ECX_02;
      if ((char)uVar5 != '\0') {
        if (((local_1c < 2) || (local_1c < 3)) || ((local_1c < 4 || (local_1c < 5)))) {
          uVar10 = uVar10 + 10;
          FUN_004591c8('\0',sVar8);
          uVar6 = extraout_ECX_01;
        }
        else if (local_1c == 200) {
          FUN_004591c8('\0',sVar8);
          uVar10 = uVar10 + 10;
          uVar6 = extraout_ECX_03;
        }
      }
    }
  }
  local_30 = uVar10 & 0xffff;
  local_38 = (uint)local_24;
  FUN_004591c8('\0',sVar8);
  FUN_00441775(0,CONCAT22(uStack_22,local_24) + 0x50);
  FUN_004591c8(extraout_CL,(short)local_30);
  FUN_0048c38b(extraout_ECX_04,local_88);
  local_30 = uVar10 + 10 & 0xffff;
  FUN_004591c8('\0',(short)(uVar10 + 10));
  FUN_004591c8('\0',(short)local_30);
  FUN_0048c38b(extraout_ECX_05,local_88);
  local_30 = uVar10 + 0x14 & 0xffff;
  FUN_004591c8('\0',(short)(uVar10 + 0x14));
  FUN_004591c8('\0',(short)local_30);
  FUN_0048c38b(extraout_ECX_06,local_88);
  local_30 = uVar10 + 0x1e & 0xffff;
  FUN_004591c8('\0',(short)(uVar10 + 0x1e));
  FUN_004591c8('\0',(short)local_30);
  FUN_0048c38b(extraout_ECX_07,local_88);
  local_30 = uVar10 + 0x28 & 0xffff;
  FUN_004591c8('\0',(short)(uVar10 + 0x28));
  FUN_004591c8('\0',(short)local_30);
  FUN_0048c38b(extraout_ECX_08,local_88);
  local_4c = uVar10 + 0x32 & 0xffff;
  FUN_004591c8('\0',(short)(uVar10 + 0x32));
  FUN_004591c8('\0',(short)local_4c);
  FUN_00428cc0(extraout_ECX_09,0);
  FUN_0048c38b(extraout_ECX_10,local_88);
  local_30 = uVar10 + 0x3c & 0xffff;
  FUN_004591c8('\0',(short)(uVar10 + 0x3c));
  FUN_004591c8('\0',(short)local_30);
  FUN_0048c38b(extraout_ECX_11,local_88);
  local_30 = uVar10 + 0x46 & 0xffff;
  FUN_004591c8('\0',(short)(uVar10 + 0x46));
  FUN_004591c8('\0',(short)local_30);
  FUN_00428cc0(extraout_ECX_12,3);
  FUN_0048c38b(extraout_ECX_13,local_88);
  local_50 = uVar10 + 0x50 & 0xffff;
  FUN_004591c8('\0',(short)(uVar10 + 0x50));
  FUN_004591c8('\0',(short)local_50);
  FUN_0048c38b(extraout_ECX_14,local_88);
  local_30 = uVar10 + 0x5a & 0xffff;
  FUN_004591c8('\0',(short)(uVar10 + 0x5a));
  uVar11 = uVar10 + 100;
  FUN_004591c8('\0',(short)local_30);
  sVar9 = (short)uVar11;
  local_3c = uVar11 & 0xffff;
  FUN_004591c8('\0',sVar9);
  sVar7 = (short)local_3c;
  switch(pUVar12->estado) {
  case 0:
    iVar4 = CONCAT22(uStack_22,local_24);
    goto LAB_0043fff5;
  case 1:
    local_20 = CONCAT22(uStack_22,local_24) + 0x50;
    FUN_004591c8('\0',sVar9);
    uVar11 = uVar10 + 0x6e;
    switch(pUVar12->field_0x8a) {
    case 0:
      iVar4 = CONCAT22(uStack_22,local_24);
      break;
    case 1:
      iVar4 = CONCAT22(uStack_22,local_24);
      break;
    case 2:
      iVar4 = CONCAT22(uStack_22,local_24);
      break;
    case 3:
      iVar4 = CONCAT22(uStack_22,local_24);
      break;
    default:
      goto switchD_004400ed_default;
    }
    goto LAB_0043fff5;
  case 2:
    iVar4 = CONCAT22(uStack_22,local_24);
    goto LAB_0043fff5;
  case 3:
    iVar4 = CONCAT22(uStack_22,local_24);
    goto LAB_0043fff5;
  case 4:
    iVar4 = CONCAT22(uStack_22,local_24);
    goto LAB_0043fff5;
  case 5:
    local_20 = CONCAT22(uStack_22,local_24) + 0x50;
    FUN_004591c8('\0',sVar9);
    FUN_004591c8('\0',sVar8 + 0x6e);
    FUN_0048c38b(0,local_88);
    local_20 = CONCAT22(uStack_22,local_24) + 0x50;
    FUN_004591c8('\0',sVar8 + 0x6e);
    uVar11 = uVar10 + 0x78;
    switch(pUVar12->field_0x89) {
    case 0:
      iVar4 = CONCAT22(uStack_22,local_24);
      break;
    case 1:
      iVar4 = CONCAT22(uStack_22,local_24);
      break;
    case 2:
      iVar4 = CONCAT22(uStack_22,local_24);
      break;
    case 3:
      iVar4 = CONCAT22(uStack_22,local_24);
      break;
    default:
      goto switchD_004400ed_default;
    }
    goto LAB_0043fff5;
  default:
    sVar7 = sVar9;
    break;
  case 7:
    iVar4 = CONCAT22(uStack_22,local_24);
    goto LAB_0043fff5;
  case 0xb:
    iVar4 = CONCAT22(uStack_22,local_24);
LAB_0043fff5:
    local_20 = iVar4 + 0x50;
    sVar7 = (short)uVar11;
    break;
  case 0xd:
    break;
  case 0xe:
    break;
  case 0xf:
    break;
  case 0x10:
    break;
  case 0x11:
    break;
  case 0x12:
    FUN_004591c8('\0',sVar7);
    local_30 = uVar10 + 0x6e & 0xffff;
    FUN_004591c8('\0',(short)(uVar10 + 0x6e));
    FUN_0048c38b(0,local_88);
    FUN_004591c8(extraout_CL_00,(short)local_30);
    uVar11 = uVar10 + 0x78;
    switch(pUVar12->field_0x89) {
    case 0:
      break;
    case 1:
      break;
    case 2:
      break;
    case 3:
      break;
    default:
      goto switchD_004400ed_default;
    }
    sVar7 = (short)uVar11;
    break;
  case 0x13:
  }
  FUN_004591c8('\0',sVar7);
switchD_004400ed_default:
  sVar8 = (short)uVar11 + 10;
  FUN_004591c8('\0',sVar8);
  switch(pUVar12->estado_caminho) {
  case 0:
    break;
  case 1:
    break;
  default:
    goto switchD_0044004c_caseD_2;
  case 3:
    break;
  case 4:
    break;
  case 5:
    break;
  case 6:
  }
  FUN_004591c8('\0',sVar8);
switchD_0044004c_caseD_2:
  local_30 = uVar11 + 0x14 & 0xffff;
  FUN_004591c8('\0',(short)(uVar11 + 0x14));
  FUN_0048c38b(extraout_ECX_15,local_88);
  local_40 = local_24 + 0x50 & 0xffff;
  FUN_004591c8('\0',(short)local_30);
  local_54 = uVar11 + 0x1e & 0xffff;
  FUN_004591c8('\0',(short)(uVar11 + 0x1e));
  FUN_0048c38b(0,local_88);
  FUN_004591c8(extraout_CL_01,(short)local_54);
  local_30 = uVar11 + 0x28 & 0xffff;
  FUN_004591c8('\0',(short)(uVar11 + 0x28));
  FUN_0048c38b(0,local_88);
  FUN_004591c8(extraout_CL_02,(short)local_30);
  FUN_0048c38b(extraout_ECX_16,local_88);
  FUN_004591c8('\0',(short)local_30);
  local_48 = uVar11 + 0x32 & 0xffff;
  FUN_004591c8('\0',(short)(uVar11 + 0x32));
  FUN_0048c38b(extraout_ECX_17,local_88);
  FUN_004591c8('\0',(short)local_48);
  local_30 = uVar11 + 0x3c & 0xffff;
  FUN_004591c8('\0',(short)(uVar11 + 0x3c));
  FUN_0048c38b(0,local_88);
  FUN_004591c8(extraout_CL_03,(short)local_30);
  local_30 = uVar11 + 0x46 & 0xffff;
  FUN_004591c8('\0',(short)(uVar11 + 0x46));
  FUN_0048c38b(0,local_88);
  FUN_004591c8(extraout_CL_04,(short)local_30);
  uVar10 = uVar11 + 0x50;
  cVar3 = FUN_004422eb();
  if (cVar3 != '\0') {
    local_30 = uVar10 & 0xffff;
    FUN_004591c8('\0',(short)uVar10);
    FUN_0048c38b(0,local_88);
    uVar10 = uVar11 + 0x5a;
    FUN_004591c8(extraout_CL_05,(short)local_30);
  }
  if (pUVar12->tipo_id == 4) {
    FUN_004591c8('\0',(short)uVar10);
    FUN_0044828b(extraout_ECX_18,extraout_EDX);
    FUN_0048c38b(extraout_ECX_19,local_88);
    FUN_004591c8('\0',(short)uVar10);
    uVar10 = uVar10 + 10;
  }
  FUN_004591c8('\0',(short)uVar10);
  uVar11 = uVar10 + 10;
  cVar3 = FUN_0045002e(extraout_ECX_20,extraout_EDX_00);
  uVar6 = extraout_ECX_21;
  if (cVar3 != '\0') {
    FUN_004591c8('\0',(short)uVar11);
    FUN_0048c38b(extraout_ECX_22,local_88);
    FUN_004591c8('\0',(short)uVar11);
    uVar11 = uVar10 + 0x14;
    uVar6 = extraout_ECX_23;
  }
  cVar3 = FUN_0044fffe(uVar6);
  uVar6 = extraout_ECX_24;
  uVar5 = extraout_EDX_01;
  if (cVar3 != '\0') {
    FUN_004591c8('\0',(short)uVar11);
    FUN_0048c38b(extraout_ECX_25,local_88);
    FUN_004591c8('\0',(short)uVar11);
    uVar11 = uVar11 + 10;
    uVar6 = extraout_ECX_26;
    uVar5 = extraout_EDX_02;
  }
  cVar3 = FUN_00450054(uVar6,uVar5);
  if (cVar3 != '\0') {
    FUN_004591c8('\0',(short)uVar11);
    FUN_0048c38b(extraout_ECX_27,local_88);
    FUN_004591c8('\0',(short)uVar11);
    uVar11 = uVar11 + 10;
  }
  local_30 = uVar11 & 0xffff;
  local_44 = (uint)local_24;
  FUN_004591c8('\0',(short)uVar11);
  FUN_0048c38b(extraout_ECX_28,local_88);
  FUN_004591c8('\0',(short)local_30);
  local_30 = uVar11 + 10 & 0xffff;
  FUN_004591c8('\0',(short)(uVar11 + 10));
  FUN_0048c38b(0,local_88);
  FUN_004591c8(extraout_CL_06,(short)local_30);
  local_30 = uVar11 + 0x14 & 0xffff;
  FUN_004591c8('\0',(short)(uVar11 + 0x14));
  FUN_0048c38b(0,local_88);
  sVar8 = (short)uVar11 + 0x1e;
  FUN_004591c8(extraout_CL_07,(short)local_30);
  FUN_004591c8('\0',sVar8);
  FUN_0048c38b(0,local_88);
  FUN_004591c8(extraout_CL_08,sVar8);
  return;
}
