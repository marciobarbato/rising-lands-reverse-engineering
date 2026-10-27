/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00473510, entrada 00473510.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00473510(undefined4 param_1,uint param_2)

{
  char cVar1;
  byte bVar2;
  ushort in_AX;
  short sVar3;
  ushort uVar4;
  uint uVar5;
  undefined1 uVar6;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
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
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 extraout_EDX_02;
  ushort unaff_BX;
  undefined8 uVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  undefined4 uVar10;
  undefined4 uVar11;
  undefined4 uVar12;

  switch(param_2 & 0xff) {
  case 0:
    bVar2 = unidade_obter_proprietario(in_AX);
    if (bVar2 == DAT_00508041) {
      FUN_00440d5e(extraout_ECX_20,0x1e);
    }
    FUN_0046e44c(0,0,0,0,0);
    uVar8 = extraout_ECX_21;
    break;
  case 1:
    bVar2 = unidade_obter_proprietario(in_AX);
    uVar8 = extraout_ECX_12;
    if (bVar2 == DAT_00508041) {
      FUN_00440d5e(extraout_ECX_12,0x1f);
      uVar8 = extraout_ECX_13;
    }
    FUN_0044ff7f(uVar8,1);
    uVar12 = 0;
    uVar11 = 0;
    uVar10 = 0;
    uVar9 = 0;
    uVar8 = 0;
    FUN_0044113e(0,extraout_EDX_00);
    FUN_0044113e(extraout_ECX_14,0);
    FUN_0046e44c(uVar8,uVar9,uVar10,uVar11,uVar12);
    uVar8 = extraout_ECX_15;
    break;
  case 2:
    bVar2 = unidade_obter_proprietario(unaff_BX);
    uVar7 = FUN_0044113e(CONCAT22((short)((uint)extraout_ECX >> 0x10),
                                  CONCAT11(bVar2,(char)extraout_ECX)),extraout_EDX);
    unidade_obter_tipo((ushort)((ulonglong)uVar7 >> 0x20));
    sVar3 = FUN_004436ab();
    bVar2 = unidade_obter_proprietario(in_AX);
    uVar8 = extraout_ECX_00;
    if (bVar2 == DAT_00508041) {
      FUN_00440d5e(extraout_ECX_00,0x20);
      uVar8 = extraout_ECX_01;
    }
    if (sVar3 == -1) {
      return;
    }
    uVar6 = (undefined1)((uint)uVar8 >> 8);
    FUN_00457e6c(uVar6);
    FUN_00456fa6();
    uVar5 = FUN_00442394();
    uVar8 = extraout_ECX_02;
    if (((char)uVar5 != '\0') && (cVar1 = FUN_0044230c(), uVar8 = extraout_ECX_03, cVar1 != '\0')) {
      uVar4 = FUN_00457e6c(uVar6);
      FUN_0044ff7f(extraout_ECX_04,2);
      FUN_00447694(extraout_ECX_05,uVar4);
      uVar4 = unidade_obter_vida(unaff_BX);
      FUN_004571ae(extraout_ECX_06,uVar4);
      FUN_0044115f(extraout_ECX_07,0xe);
      uVar8 = extraout_ECX_08;
    }
    FUN_0044ff7f(uVar8,2);
    FUN_0046e44c(0,0,0,0,0);
    uVar7 = FUN_004746e4(extraout_ECX_09,0);
    FUN_004482ae(extraout_ECX_10,(char)uVar7);
    uVar4 = unidade_obter_vida(unaff_BX);
    FUN_004571ae(extraout_ECX_11,uVar4);
    return;
  case 3:
    bVar2 = unidade_obter_proprietario(in_AX);
    uVar8 = extraout_ECX_17;
    if (bVar2 == DAT_00508041) {
      FUN_00440d5e(extraout_ECX_17,0x21);
      uVar8 = extraout_ECX_18;
    }
    FUN_0044ff7f(uVar8,3);
    uVar8 = extraout_ECX_19;
    break;
  case 4:
    bVar2 = unidade_obter_proprietario(in_AX);
    uVar8 = extraout_ECX_22;
    uVar9 = extraout_EDX_01;
    if (bVar2 == DAT_00508041) {
      FUN_00440d5e(extraout_ECX_22,0x22);
      uVar8 = extraout_ECX_23;
      uVar9 = extraout_EDX_02;
    }
    FUN_0044113e(uVar8,uVar9);
    FUN_0046e44c(in_AX,0,0,0,0);
    uVar7 = FUN_004746e4(extraout_ECX_24,0);
    cVar1 = (char)uVar7;
    uVar8 = extraout_ECX_25;
    goto LAB_00473704;
  default:
    goto switchD_00473528_default;
  }
  uVar7 = FUN_004746e4(uVar8,0);
  cVar1 = (char)uVar7;
  uVar8 = extraout_ECX_16;
LAB_00473704:
  FUN_004482ae(uVar8,cVar1);
switchD_00473528_default:
  return;
}
