/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0046c5e3, entrada 0046c5e3.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 __fastcall FUN_0046c5e3(undefined4 param_1,undefined4 param_2)

{
  char cVar1;
  bool bVar2;
  char *in_EAX;
  uint uVar3;
  int iVar4;
  undefined3 extraout_var;
  byte bVar5;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  uint extraout_ECX_01;
  uint uVar6;
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
  undefined4 uVar7;
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
  int extraout_ECX_24;
  undefined4 extraout_ECX_25;
  undefined4 extraout_ECX_26;
  undefined4 extraout_ECX_27;
  undefined4 extraout_ECX_28;
  uint extraout_ECX_29;
  undefined4 extraout_EDX;
  undefined4 uVar8;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 extraout_EDX_02;
  undefined4 extraout_EDX_03;
  ushort uVar9;
  char *pcVar10;
  char *pcVar11;
  char *pcVar12;
  char acStack_12c [260];
  ushort uStack_28;
  undefined2 uStack_24;
  ushort uStack_1c;

  _DAT_004e1a38 = 0xffff;
  DAT_004e1a3a = 0xffff;
  FUN_0045e88f();
  FUN_0046b315(extraout_ECX);
  FUN_00469f00(extraout_ECX_00);
  FUN_0041a75c();
  FUN_00441659();
  FUN_0046e00a();
  FUN_00469908();
  for (uVar6 = extraout_ECX_01; (uVar6 & 0xffff) < 4; uVar6 = uVar6 + 1) {
    for (uVar3 = uVar6 & 0xffff ^ uVar6; (uVar3 & 0xffff) < 0x1a; uVar3 = uVar3 + 1) {
      (&DAT_004e1934)[(uVar6 & 0xffff) * 0x1a + (uVar3 & 0xffff)] = 0;
    }
  }
  for (bVar5 = 0; bVar5 < 4; bVar5 = bVar5 + 1) {
    uVar6 = 0;
    while( true ) {
      uVar3 = uVar6 & 0xffff;
      if (0x15 < uVar3) break;
      uVar6 = uVar6 + 1;
      (&DAT_004dfad4)[(uint)bVar5 * 0x16 + uVar3] = 0;
    }
  }
  FUN_004749f2();
  FUN_00470b46();
  FUN_00441470();
  DAT_00496fe4 = 0x32;
  cVar1 = FUN_0042c3b0();
  if (cVar1 != '\0') {
    FUN_004716fe();
    FUN_004714f0();
  }
  FUN_00441b6c();
  uVar6 = 0xffffffff;
  pcVar10 = in_EAX;
  do {
    if (uVar6 == 0) break;
    uVar6 = uVar6 - 1;
    cVar1 = *pcVar10;
    pcVar10 = pcVar10 + 1;
  } while (cVar1 != '\0');
  iVar4 = FUN_0048d561(~uVar6 - 1,&DAT_00494b3e);
  if (iVar4 == 0) {
    pcVar10 = &DAT_00509494;
  }
  else {
    pcVar10 = (char *)((int)&DAT_00509591 + 3);
  }
  pcVar11 = acStack_12c;
  do {
    cVar1 = *pcVar10;
    *pcVar11 = cVar1;
    if (cVar1 == '\0') break;
    cVar1 = pcVar10[1];
    pcVar10 = pcVar10 + 2;
    pcVar11[1] = cVar1;
    pcVar11 = pcVar11 + 2;
  } while (cVar1 != '\0');
  pcVar11 = &DAT_00494b43;
  iVar4 = -1;
  pcVar10 = acStack_12c;
  do {
    pcVar12 = pcVar10;
    if (iVar4 == 0) break;
    iVar4 = iVar4 + -1;
    pcVar12 = pcVar10 + 1;
    cVar1 = *pcVar10;
    pcVar10 = pcVar12;
  } while (cVar1 != '\0');
  pcVar12 = pcVar12 + -1;
  do {
    cVar1 = *pcVar11;
    *pcVar12 = cVar1;
    if (cVar1 == '\0') break;
    cVar1 = pcVar11[1];
    pcVar11 = pcVar11 + 2;
    pcVar12[1] = cVar1;
    pcVar12 = pcVar12 + 2;
  } while (cVar1 != '\0');
  iVar4 = -1;
  pcVar10 = acStack_12c;
  do {
    pcVar11 = pcVar10;
    if (iVar4 == 0) break;
    iVar4 = iVar4 + -1;
    pcVar11 = pcVar10 + 1;
    cVar1 = *pcVar10;
    pcVar10 = pcVar11;
  } while (cVar1 != '\0');
  pcVar11 = pcVar11 + -1;
  do {
    cVar1 = *in_EAX;
    *pcVar11 = cVar1;
    if (cVar1 == '\0') break;
    cVar1 = in_EAX[1];
    in_EAX = in_EAX + 2;
    pcVar11[1] = cVar1;
    pcVar11 = pcVar11 + 2;
  } while (cVar1 != '\0');
  bVar2 = FUN_00458420(iVar4,&DAT_00494b4b);
  uVar7 = CONCAT31(extraout_var,bVar2);
  if (bVar2) {
    FUN_0045848b();
    FUN_00458461(extraout_ECX_02,0x10000);
    FUN_00458461(extraout_ECX_03,0x20000);
    FUN_00458461(extraout_ECX_04,0x10000);
    FUN_00458461(extraout_ECX_05,0x10000);
    for (uVar6 = 0; uVar6 < 0x10000; uVar6 = uVar6 + 1) {
      if (*(char *)(DAT_00507d74 + uVar6) == '6') {
        *(char *)(DAT_00507d74 + uVar6) = 'B';
        *(undefined1 *)(DAT_00507dac + uVar6) = 1;
      }
    }
    uVar6 = extraout_ECX_06 & 0xffffff00;
    while ((uVar6 & 0xff) < 4) {
      FUN_00458461(uVar6,2);
      FUN_0046799c(CONCAT31((int3)((uint)extraout_ECX_07 >> 8),(char)extraout_ECX_07 + '\x01'),
                   uStack_24);
      uVar6 = extraout_ECX_08;
    }
    uVar6 = uVar6 & 0xffffff00;
    while ((uVar6 & 0xff) < 4) {
      FUN_00458461(uVar6,2);
      FUN_0046799c(CONCAT31((int3)((uint)extraout_ECX_09 >> 8),(char)extraout_ECX_09 + '\x01'),
                   uStack_24);
      uVar6 = extraout_ECX_10;
    }
    uVar6 = uVar6 & 0xffffff00;
    while ((uVar6 & 0xff) < 4) {
      FUN_00458461(uVar6,2);
      FUN_0046799c(CONCAT31((int3)((uint)extraout_ECX_11 >> 8),(char)extraout_ECX_11 + '\x01'),
                   uStack_24);
      uVar6 = extraout_ECX_12;
    }
    FUN_00458461(uVar6,2);
    FUN_00458461(extraout_ECX_13,2);
    uVar7 = 2;
    uVar8 = extraout_EDX;
    for (uVar9 = 0; uVar9 < 4; uVar9 = uVar9 + 1) {
      if (uVar9 == DAT_00508041) {
        FUN_00458461(uVar7,uVar7);
        uVar7 = extraout_ECX_14;
      }
      else {
        FUN_00458461(uVar7,uVar7);
        uVar7 = extraout_ECX_16;
      }
      FUN_00458461(uVar7,uVar7);
      uVar7 = extraout_ECX_15;
      uVar8 = extraout_EDX_00;
    }
    FUN_0042ee1c(uVar7,uVar8);
    FUN_00458461(extraout_ECX_17,2);
    uVar6 = 2;
    uVar9 = 0;
    uVar7 = extraout_ECX_18;
    while( true ) {
      FUN_00458461(uVar7,uVar6);
      if (uStack_28 <= uVar9) break;
      FUN_00458461(extraout_ECX_20,2);
      uVar6 = (uint)uStack_1c;
      uVar9 = uVar9 + 1;
      uVar7 = extraout_ECX_19;
    }
    carregar_unidades_eta();
    FUN_0047534a(extraout_ECX_21);
    FUN_0047c24d();
    FUN_0047bcc7(extraout_ECX_22,extraout_EDX_01);
    FUN_0047c04a(extraout_ECX_23);
    FUN_00458b05(extraout_ECX_24);
    FUN_0047c30f(extraout_ECX_25);
    FUN_0047c404();
    FUN_0047ac30(extraout_ECX_26);
    FUN_0045844c(extraout_ECX_27,extraout_EDX_02);
    FUN_0046c122(extraout_ECX_28);
    FUN_00441459();
    FUN_00419112();
    FUN_0047150f();
    FUN_0047f36e(extraout_ECX_29,extraout_EDX_03);
    uVar7 = FUN_0046027c();
    uVar7 = CONCAT31((int3)((uint)uVar7 >> 8),1);
  }
  return CONCAT44(param_2,uVar7);
}
