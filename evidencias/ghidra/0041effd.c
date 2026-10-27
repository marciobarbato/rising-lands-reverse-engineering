/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0041effd, entrada 0041effd.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_0041effd(undefined4 param_1,undefined4 param_2)

{
  ushort uVar1;
  ushort uVar2;
  byte bVar3;
  ushort in_AX;
  ushort uVar4;
  int iVar5;
  uint uVar6;
  short *psVar7;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 uVar8;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  undefined2 extraout_var;
  undefined4 extraout_ECX_06;
  undefined4 extraout_ECX_07;
  undefined4 extraout_ECX_08;
  uint extraout_ECX_09;
  uint extraout_ECX_10;
  uint extraout_ECX_11;
  uint extraout_ECX_12;
  int extraout_EDX;
  int iVar9;
  uint uVar10;
  bool bVar11;
  ulonglong uVar12;
  undefined8 uVar13;

  iVar5 = (uint)in_AX * 0x114;
  if (((&DAT_0049a0d0)[iVar5] == '\f') || ((&DAT_0049a0d0)[iVar5] == '\t')) {
    *(undefined2 *)(&DAT_0049a14c + iVar5) = 0;
  }
  if ((&DAT_0049a0cc)[iVar5] != 200) {
    DAT_004dfab8 = (&DAT_0049a0cc)[iVar5];
  }
  if ((&DAT_0049a158)[iVar5] != '\0') {
    FUN_0041b888(param_1,'\x01');
    (&DAT_0049a158)[iVar5] = 0;
    param_1 = CONCAT31((int3)((uint)extraout_ECX >> 8),DAT_00508041);
    if (DAT_00508041 == (&DAT_0049a0cc)[(uint)in_AX * 0x114]) {
      uVar6 = FUN_0041a0ab();
      param_1 = extraout_ECX_00;
      if (*(int *)(extraout_EDX + 0x100) == -1) {
        FUN_0048aa79(0,(uint)*(byte *)(extraout_EDX + 8) << 0x10 | 0x500,uVar6);
        param_1 = extraout_ECX_01;
      }
    }
  }
  if ((&DAT_0049a0d0)[(uint)in_AX * 0x114] == '\x15') {
    uVar12 = FUN_0044724a(param_1,&DAT_0049a0c8 + (uint)in_AX * 0x114);
    bVar11 = (char)uVar12 == '\0';
    uVar8 = extraout_ECX_02;
LAB_0041f0f0:
    if (bVar11) {
      bVar11 = false;
      goto LAB_0041f11d;
    }
  }
  else {
    if ((&DAT_0049a0d0)[(uint)in_AX * 0x114] != '\x02') {
LAB_0041f104:
      iVar9 = FUN_004471b8(param_1,'\x01');
      bVar11 = (short)iVar9 == 0;
      uVar8 = extraout_ECX_04;
      goto LAB_0041f0f0;
    }
    uVar12 = FUN_0044724a(param_1,&DAT_0049a0c8 + (uint)in_AX * 0x114);
    uVar8 = extraout_ECX_03;
    param_1 = extraout_ECX_03;
    if ((char)uVar12 == '\0') goto LAB_0041f104;
  }
  bVar11 = true;
LAB_0041f11d:
  if (bVar11) {
    psVar7 = (short *)FUN_0041dde0(uVar8);
    if (((uint)psVar7 & 0xffff) != 0xffff) {
      uVar4 = unidade_obter_vida((ushort)psVar7);
      psVar7 = (short *)FUN_004571ae(extraout_ECX_05,uVar4 - uVar4 / 2);
    }
  }
  else if (*(short *)(&DAT_0049a14c + iVar5) == 0) {
    uVar4 = *(ushort *)(&DAT_00495d8c + (uint)(byte)(&DAT_0049a0d0)[iVar5] * 0x34);
    uVar1 = *(ushort *)(&DAT_00495d8e + (uint)(byte)(&DAT_0049a0d0)[iVar5] * 0x34);
    uVar2 = *(ushort *)(&DAT_0049a0ca + iVar5);
    FUN_0041b888(uVar8,'\0');
    FUN_0041b78f(extraout_ECX_07);
    FUN_00419e97(extraout_ECX_08,'\0');
    (&DAT_0049a0cd)[iVar5] = 0;
    *(undefined2 *)(&DAT_0049a0d2 + iVar5) = 0;
    (&DAT_0049a0c8)[iVar5] = 0xff;
    (&DAT_0049a13c)[iVar5] = 0;
    (&DAT_0049a13d)[iVar5] = 0;
    (&DAT_0049a13e)[iVar5] = 0;
    (&DAT_0049a143)[iVar5] = 0xff;
    *(undefined2 *)(&DAT_0049a140 + iVar5) = 0xffff;
    *(undefined2 *)(&DAT_0049a144 + iVar5) = 0;
    *(undefined2 *)(&DAT_0049a146 + iVar5) = 0;
    *(undefined2 *)(&DAT_0049a148 + iVar5) = 0;
    *(undefined2 *)(&DAT_0049a14a + iVar5) = 0;
    *(undefined4 *)(&DAT_0049a154 + iVar5) = 0;
    bVar3 = DAT_004dfab8;
    if (in_AX == *(ushort *)(&DAT_00495be0 + (uint)DAT_004dfab8 * 2)) {
      *(undefined2 *)(&DAT_00495be0 + (uint)DAT_004dfab8 * 2) = 0xffff;
    }
    psVar7 = (short *)(uint)bVar3;
    for (uVar6 = 0; uVar10 = uVar6 & 0xffff, uVar10 < 4; uVar6 = uVar6 + 1) {
      psVar7 = (short *)(uint)in_AX;
      iVar5 = uVar10 + (int)psVar7 * 0x114;
      if ((&DAT_0049a1d8)[iVar5] != '\0') {
        psVar7 = (short *)FUN_00419233(uVar6,(byte)uVar6);
        (&DAT_0049a1d8)[iVar5] = 0;
        uVar6 = extraout_ECX_09;
      }
    }
    for (uVar10 = uVar10 ^ uVar6; (ushort)uVar10 < uVar1; uVar10 = uVar10 + 1) {
      iVar5 = 0;
      while ((ushort)iVar5 < uVar4) {
        uVar12 = FUN_004704dc(iVar5,0);
        if (((int)(uVar12 % 3) == 0) &&
           (iVar5 = (extraout_ECX_11 & 0xffff) + (uVar10 & 0xffff) * 0x100 + (uint)uVar2,
           *(char *)(iVar5 + (int)DAT_00507d74) == '\0')) {
          uVar12 = FUN_004704dc(extraout_ECX_11,0);
          psVar7 = DAT_00507d74;
          *(char *)(iVar5 + (int)DAT_00507d74) = (char)(uVar12 % 0xb) + '\f';
          uVar6 = extraout_ECX_12;
        }
        else {
          iVar5 = (uint)uVar2 + (uVar10 & 0xffff) * 0x100 + (extraout_ECX_11 & 0xffff);
          psVar7 = (short *)(uint)*(byte *)(iVar5 + (int)DAT_00507d74);
          uVar6 = extraout_ECX_11;
          if (psVar7 == (short *)0x0) {
            uVar13 = FUN_004704dc(extraout_ECX_11,iVar5);
            psVar7 = (short *)((int)((ulonglong)uVar13 >> 0x20) * 2 + DAT_00507d70);
            *psVar7 = ((byte)uVar13 & 0xff07) + 0x19d;
            uVar6 = extraout_ECX_10;
          }
        }
        iVar5 = uVar6 + 1;
      }
    }
  }
  else {
    uVar12 = FUN_004704dc(uVar8,0);
    psVar7 = (short *)(uVar12 / 0x19);
    iVar9 = (int)(uVar12 % 0x19) + 8;
    if ((ushort)iVar9 < *(ushort *)(&DAT_0049a14c + iVar5)) {
      uVar12 = FUN_004704dc(CONCAT22(extraout_var,*(ushort *)(&DAT_0049a14c + iVar5)),iVar9);
      psVar7 = (short *)uVar12;
      if ((uVar12 & 1) == 0) {
        *(short *)(&DAT_0049a14c + iVar5) =
             *(short *)(&DAT_0049a14c + iVar5) - (short)(uVar12 >> 0x20);
        uVar13 = FUN_0041e260(extraout_ECX_06,
                              (uint)(byte)(&DAT_0049a0d0)[(uint)in_AX * 0x114] * 0x34);
        psVar7 = (short *)uVar13;
      }
    }
    else {
      *(undefined2 *)(&DAT_0049a14c + iVar5) = 0;
    }
  }
  return CONCAT44(param_2,psVar7);
}
