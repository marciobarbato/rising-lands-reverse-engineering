/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

longlong __fastcall FUN_00485183(undefined4 param_1,uint param_2)

{
  int iVar1;
  undefined2 uVar2;
  int in_EAX;
  undefined4 uVar3;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  int iVar4;
  undefined2 extraout_var_01;
  int *piVar5;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  int *extraout_ECX_06;
  int *piVar6;
  int iVar7;
  ushort local_4c;
  ushort local_4a;
  ushort local_48;
  undefined2 local_46;
  int local_44;
  undefined1 *local_40;
  int local_38;
  int local_30;
  int *local_2c;
  undefined2 local_24 [2];
  ushort local_20;
  ushort local_1c [2];

  local_44 = in_EAX * 0xa8;
  local_2c = (int *)(&DAT_0051ba3c + local_44);
  if (DAT_00508f7c % *(uint *)(&DAT_0051ba7c + local_44) != 0) goto LAB_0048568f;
  *(int *)(&DAT_0051ba4c + local_44) = *local_2c;
  *(undefined4 *)(&DAT_0051ba50 + local_44) = *(undefined4 *)(&DAT_0051ba40 + local_44);
  *(undefined4 *)(&DAT_0051ba54 + local_44) = *(undefined4 *)(&DAT_0051ba44 + local_44);
  *(undefined4 *)(&DAT_0051ba58 + local_44) = *(undefined4 *)(&DAT_0051ba48 + local_44);
  FUN_00467670(&local_46,&local_4a,(byte)in_EAX);
  *(uint *)(&DAT_0051ba3c + local_44) = (uint)local_4c;
  *(uint *)(&DAT_0051ba40 + local_44) = (uint)local_4a;
  *(uint *)(&DAT_0051ba44 + local_44) = (uint)local_48;
  uVar3 = FUN_0047f8e7();
  piVar6 = local_2c;
  if ((char)uVar3 == '\0') {
    uVar2 = FUN_00484b76(extraout_ECX,3);
    uVar3 = extraout_ECX_00;
    if ((0 < CONCAT22(extraout_var,uVar2)) && ((char)local_2c[0x27] == '\0')) {
      *(undefined1 *)(local_2c + 0x27) = 1;
      FUN_0047d920(0,0xb,0,0,0,0);
      FUN_0047d920(0,0xc,0,0,0,0);
      uVar3 = extraout_ECX_01;
    }
    uVar2 = FUN_00484b76(uVar3,4);
    uVar3 = extraout_ECX_02;
    if ((0 < CONCAT22(extraout_var_00,uVar2)) && (*(char *)((int)local_2c + 0x9d) == '\0')) {
      *(undefined1 *)((int)local_2c + 0x9d) = 1;
      FUN_0047d920(0,0x15,0,0,0,0);
      uVar3 = extraout_ECX_03;
    }
    if (((char)local_2c[0x27] != '\0') && (*(char *)((int)local_2c + 0x9d) != '\0')) {
      *(undefined1 *)((int)&DAT_0051a98e + in_EAX * 0x10 + 1) = 1;
      FUN_0047f8f1(uVar3);
    }
  }
  else {
    local_40 = &DAT_0051a98c + in_EAX * 0x10;
    if (local_2c[0x22] != 0) {
      while (local_2c[local_2c[0x21] * 2 + 0x16] == -1) {
        iVar4 = local_2c[0x21];
        local_2c[0x21] = iVar4 + 1;
        if (DAT_0051bcf0 <= iVar4 + 1) {
          local_2c[0x21] = 0;
        }
      }
      FUN_0047d920(0,0xd,0,0,0,0);
      iVar4 = piVar6[0x21];
      piVar6[0x21] = iVar4 + 1;
      if (DAT_0051bcf0 <= iVar4 + 1) {
        piVar6[0x21] = 0;
      }
    }
    if (piVar6[0x12] < *piVar6 - piVar6[4]) {
      if (piVar6[0xc] < *piVar6) {
        iVar4 = FUN_0047d98b(0,0x15,0,0,0,0,0);
        if (iVar4 == -1) {
          FUN_0047d920(0,0x15,0,0,0,0);
        }
        local_40[2] = 1;
        local_40[3] = 1;
        piVar6[0x13] = 0;
      }
      else {
        piVar6[0x13] = 1;
      }
    }
    else if (piVar6[0xc] < *piVar6) {
      iVar4 = FUN_0047d98b(0,0xb,0,0,0,0,0);
      if (iVar4 == -1) {
        FUN_0047d920(0,0xb,0,0,0,0);
      }
      piVar6[0x13] = 2;
    }
    else {
      if (local_40[1] == '\x01') {
        iVar4 = FUN_0047d98b(0,10,0,0,0,0,0);
        if (iVar4 == -1) {
          iVar4 = FUN_0047d98b(5,3,0,0,0,0,0);
          if (iVar4 == -1) {
            iVar4 = FUN_0047d98b(0,8,0,0,0,0,0);
            if (iVar4 == -1) {
              FUN_0047d920(0,8,0,0,0,0);
            }
            goto LAB_004854f7;
          }
        }
      }
      if (local_40[2] == '\x01') {
        local_40[2] = 0;
      }
      else if (local_40[3] == '\x01') {
        local_40[3] = 0;
      }
      else {
        piVar6[0x13] = 3;
      }
    }
LAB_004854f7:
    iVar4 = FUN_0047d98b(0,4,0,0,0,0,0);
    uVar3 = extraout_ECX_04;
    if (iVar4 == -1) {
      FUN_0047d920(0,4,0,0,0,0);
      uVar3 = extraout_ECX_05;
    }
    uVar2 = FUN_00484b76(uVar3,5);
    if (0 < CONCAT22(extraout_var_01,uVar2)) {
      iVar4 = FUN_0047d98b(0,6,0,0,0,0,0);
      if (iVar4 == -1) {
        FUN_0047d920(0,6,0,0,0,0);
      }
    }
    FUN_0046769d(local_24,(short *)local_1c,(byte)in_EAX);
    if ((int)((uint)*(ushort *)(&DAT_004dfb2e + in_EAX * 6) *
              (uint)*(ushort *)(&DAT_004dfb2c + in_EAX * 6) + -0xf) <
        (int)((uint)local_20 + (uint)local_1c[0])) {
      iVar4 = FUN_0047d98b(3,1,0,0,0,0,0);
      if (iVar4 == -1) {
        FUN_0047d920(0,1,0,0,0,0);
      }
    }
  }
  local_30 = -1;
  piVar6 = local_2c;
  local_38 = local_2c[0x11];
  while (iVar4 = local_38, iVar4 != -1) {
    iVar7 = iVar4 * 0x60;
    local_38 = *(int *)(&DAT_00512328 + iVar7);
    piVar5 = piVar6 + (byte)(&DAT_0051237d)[iVar7];
    iVar1 = *(int *)(&DAT_00512330 + iVar7);
    if (iVar1 <= *piVar5) {
      *piVar5 = *piVar5 - iVar1;
      piVar5[8] = piVar5[8] - iVar1;
      FUN_0047da54(piVar6,1);
      if (iVar4 == extraout_ECX_06[0x11]) {
        extraout_ECX_06[0x11] = *(int *)(&DAT_00512328 + iVar7);
      }
      else {
        *(undefined4 *)(&DAT_00512328 + local_30 * 0x60) = *(undefined4 *)(&DAT_00512328 + iVar7);
      }
      (&DAT_0051237d)[iVar4 * 0x60] = 0xff;
      piVar6 = extraout_ECX_06;
    }
    local_30 = iVar4;
  }
LAB_0048568f:
  return (ulonglong)param_2 << 0x20;
}
