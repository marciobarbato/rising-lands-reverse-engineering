/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0046c2cf, entrada 0046c2cf.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 __fastcall FUN_0046c2cf(undefined4 param_1,undefined4 param_2)

{
  char cVar1;
  bool bVar2;
  undefined3 extraout_var;
  uint uVar3;
  undefined4 uVar4;
  int iVar5;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  uint extraout_ECX_06;
  undefined4 extraout_ECX_07;
  uint extraout_ECX_08;
  undefined4 extraout_ECX_09;
  uint extraout_ECX_10;
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
  int extraout_ECX_25;
  undefined4 extraout_ECX_26;
  undefined4 extraout_ECX_27;
  undefined4 extraout_ECX_28;
  undefined4 extraout_ECX_29;
  uint extraout_ECX_30;
  undefined4 extraout_EDX;
  undefined4 uVar6;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 extraout_EDX_02;
  undefined4 extraout_EDX_03;
  ushort uVar7;
  char *pcVar8;
  char *pcVar9;
  char *pcVar10;
  char local_140 [256];
  char local_40 [20];
  ushort uStack_2c;
  undefined2 uStack_28;
  ushort uStack_24;
  undefined1 local_18;

  pcVar9 = local_140;
  local_18 = DAT_00496fe4;
  pcVar8 = (char *)((int)&DAT_00509591 + 3);
  FUN_0046c1b8(param_1,local_40);
  do {
    cVar1 = *pcVar8;
    *pcVar9 = cVar1;
    if (cVar1 == '\0') break;
    cVar1 = pcVar8[1];
    pcVar8 = pcVar8 + 2;
    pcVar9[1] = cVar1;
    pcVar9 = pcVar9 + 2;
  } while (cVar1 != '\0');
  pcVar9 = local_40;
  iVar5 = -1;
  pcVar8 = local_140;
  do {
    pcVar10 = pcVar8;
    if (iVar5 == 0) break;
    iVar5 = iVar5 + -1;
    pcVar10 = pcVar8 + 1;
    cVar1 = *pcVar8;
    pcVar8 = pcVar10;
  } while (cVar1 != '\0');
  pcVar10 = pcVar10 + -1;
  do {
    cVar1 = *pcVar9;
    *pcVar10 = cVar1;
    if (cVar1 == '\0') break;
    cVar1 = pcVar9[1];
    pcVar9 = pcVar9 + 2;
    pcVar10[1] = cVar1;
    pcVar10 = pcVar10 + 2;
  } while (cVar1 != '\0');
  _DAT_004e1a38 = 0xffff;
  DAT_004e1a3a = 0xffff;
  FUN_0045e88f();
  FUN_0046b315(extraout_ECX);
  FUN_00469f00(extraout_ECX_00);
  FUN_0041a75c();
  FUN_00441659();
  FUN_0046e00a();
  FUN_00469908();
  FUN_00441b6c();
  bVar2 = FUN_00458420(extraout_ECX_01,&DAT_00494b3b);
  uVar4 = CONCAT31(extraout_var,bVar2);
  if (bVar2) {
    FUN_0045848b();
    FUN_00458461(extraout_ECX_02,0x10000);
    FUN_00458461(extraout_ECX_03,0x20000);
    FUN_00458461(extraout_ECX_04,0x10000);
    FUN_00458461(extraout_ECX_05,0x10000);
    uVar3 = 0;
    do {
      if (*(char *)(DAT_00507d74 + uVar3) == '6') {
        *(char *)(DAT_00507d74 + uVar3) = 'B';
        *(undefined1 *)(DAT_00507dac + uVar3) = 1;
      }
      uVar3 = uVar3 + 1;
    } while (uVar3 < 0x10000);
    uVar3 = extraout_ECX_06 & 0xffffff00;
    while ((uVar3 & 0xff) < 4) {
      FUN_00458461(uVar3,2);
      FUN_0046799c(CONCAT31((int3)((uint)extraout_ECX_07 >> 8),(char)extraout_ECX_07 + '\x01'),
                   uStack_28);
      uVar3 = extraout_ECX_08;
    }
    uVar3 = uVar3 & 0xffffff00;
    while ((uVar3 & 0xff) < 4) {
      FUN_00458461(uVar3,2);
      FUN_0046799c(CONCAT31((int3)((uint)extraout_ECX_09 >> 8),(char)extraout_ECX_09 + '\x01'),
                   uStack_28);
      uVar3 = extraout_ECX_10;
    }
    uVar3 = uVar3 & 0xffffff00;
    while ((uVar3 & 0xff) < 4) {
      FUN_00458461(uVar3,2);
      FUN_0046799c(CONCAT31((int3)((uint)extraout_ECX_11 >> 8),(char)extraout_ECX_11 + '\x01'),
                   uStack_28);
      uVar3 = extraout_ECX_12;
    }
    FUN_00458461(uVar3,2);
    FUN_00458461(extraout_ECX_13,2);
    uVar4 = extraout_ECX_14;
    uVar6 = extraout_EDX;
    for (uVar7 = 0; uVar7 < 4; uVar7 = uVar7 + 1) {
      if (uVar7 == DAT_00508041) {
        FUN_00458461(uVar4,2);
        uVar4 = extraout_ECX_15;
      }
      else {
        FUN_00458461(uVar4,2);
        uVar4 = extraout_ECX_17;
      }
      FUN_00458461(uVar4,2);
      uVar4 = extraout_ECX_16;
      uVar6 = extraout_EDX_00;
    }
    FUN_0042ee1c(uVar4,uVar6);
    FUN_00458461(extraout_ECX_18,2);
    uVar3 = 2;
    uVar7 = 0;
    uVar4 = extraout_ECX_19;
    while( true ) {
      FUN_00458461(uVar4,uVar3);
      if (uStack_24 <= uVar7) break;
      FUN_00458461(extraout_ECX_21,2);
      uVar3 = (uint)uStack_2c;
      uVar7 = uVar7 + 1;
      uVar4 = extraout_ECX_20;
    }
    carregar_unidades_eta();
    FUN_0047534a(extraout_ECX_22);
    FUN_0047c24d();
    FUN_0047bcc7(extraout_ECX_23,extraout_EDX_01);
    FUN_0047c04a(extraout_ECX_24);
    FUN_00458b05(extraout_ECX_25);
    FUN_0047c30f(extraout_ECX_26);
    FUN_0047c404();
    FUN_0047ac30(extraout_ECX_27);
    FUN_0045844c(extraout_ECX_28,extraout_EDX_02);
    FUN_0046c122(extraout_ECX_29);
    FUN_00441459();
    FUN_00419112();
    FUN_00441623();
    FUN_0046df41();
    FUN_0047f36e(extraout_ECX_30,extraout_EDX_03);
    uVar4 = FUN_0046027c();
    uVar4 = CONCAT31((int3)((uint)uVar4 >> 8),1);
  }
  return CONCAT44(param_2,uVar4);
}
