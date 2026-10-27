/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004215fb, entrada 004215fb.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_004215fb(undefined4 param_1,undefined4 param_2)

{
  ushort uVar1;
  ushort uVar2;
  ushort uVar3;
  uint in_EAX;
  int iVar4;
  uint uVar5;
  int iVar6;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 uVar7;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  undefined4 extraout_ECX_06;
  undefined4 extraout_ECX_07;
  undefined2 extraout_var_01;
  undefined4 extraout_EDX;
  ushort uVar8;
  undefined8 uVar9;

  iVar4 = (in_EAX & 0xffff) * 0x114;
  unidade_obter_tipo(*(ushort *)(&DAT_0049a150 + iVar4));
  uVar5 = FUN_00442434();
  if (CONCAT22(extraout_var_01,*(undefined2 *)(&DAT_0049a150 + iVar4)) != 0xffff) {
    uVar1 = *(ushort *)(&DAT_0049a146 + iVar4);
    uVar5 = CONCAT22((short)(uVar5 >> 0x10),uVar1);
    if (uVar1 < 0x81) {
      if (uVar1 == 0x80) {
        (&DAT_0049a13d)[iVar4] = 1;
        if (((&DAT_0049a13e)[iVar4] == '\a') && ((&DAT_0049a13d)[iVar4] != '\0')) {
          uVar5 = 1;
        }
        else {
          uVar5 = 0;
        }
        if ((char)uVar5 != '\0') {
          *(short *)(&DAT_0049a146 + iVar4) = *(short *)(&DAT_0049a146 + iVar4) + 1;
        }
      }
    }
    else if (uVar1 < 0x82) {
      iVar6 = FUN_0041d057(extraout_ECX);
      uVar5 = FUN_00442668(0,(ushort)iVar6);
      if ((char)uVar5 == '\0') {
        uVar1 = *(ushort *)(&DAT_0049a150 + iVar4);
        FUN_0041d057(extraout_ECX_00);
        uVar5 = FUN_00443470(extraout_ECX_07,(uint)uVar1);
      }
      else {
        if (((&DAT_0049a13e)[iVar4] == '\a') && ((&DAT_0049a13d)[iVar4] != '\0')) {
          uVar5 = 1;
        }
        else {
          uVar5 = 0;
        }
        if ((char)uVar5 != '\0') {
          if (*(int *)(&DAT_0049a148 + iVar4) >> 0x10 < 0) {
            uVar9 = FUN_00443688(extraout_ECX_00,extraout_EDX);
            *(ushort *)(&DAT_0049a14a + iVar4) =
                 *(short *)(&DAT_0049a14a + iVar4) + (ushort)(byte)uVar9;
            uVar9 = FUN_00448088(extraout_ECX_01,(int)((ulonglong)uVar9 >> 0x20));
            uVar5 = (uint)uVar9;
          }
          else {
            (&DAT_0049a13d)[(in_EAX & 0xffff) * 0x114] = 0;
            uVar1 = *(ushort *)(&DAT_0049a150 + iVar4);
            *(short *)(&DAT_0049a146 + iVar4) = *(short *)(&DAT_0049a146 + iVar4) + 1;
            uVar2 = FUN_00447107();
            uVar5 = CONCAT22(extraout_var,uVar2);
            uVar7 = extraout_ECX_02;
            for (uVar8 = 0; uVar8 < uVar2; uVar8 = uVar8 + 1) {
              uVar3 = FUN_004472de(uVar7,(uint)uVar8);
              uVar5 = CONCAT22(extraout_var_00,uVar3);
              uVar7 = extraout_ECX_03;
              if (uVar3 == uVar1) {
                FUN_004473cf(extraout_ECX_03,uVar8);
                iVar4 = FUN_0041d057((uint)uVar1);
                FUN_00445fbc(extraout_ECX_04,(short)iVar4);
                uVar5 = FUN_004829c8(extraout_ECX_05,0x45);
                uVar7 = extraout_ECX_06;
              }
            }
          }
        }
      }
    }
    else if (uVar1 == 0x82) {
      if (((&DAT_0049a13e)[iVar4] == '\0') && ((&DAT_0049a13d)[iVar4] == '\0')) {
        uVar5 = 1;
      }
      else {
        uVar5 = 0;
      }
      if ((char)uVar5 != '\0') {
        uVar5 = FUN_004212f5();
      }
    }
  }
  return CONCAT44(param_2,uVar5);
}
