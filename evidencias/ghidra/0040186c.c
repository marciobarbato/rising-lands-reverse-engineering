/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0040186c, entrada 0040186c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0040186c(undefined4 param_1,short param_2)

{
  ushort uVar1;
  byte bVar2;
  ushort uVar3;
  ushort uVar4;
  ushort uVar5;
  undefined2 extraout_var;
  undefined2 extraout_var_00;
  short extraout_CX;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  undefined4 uVar6;
  undefined4 extraout_ECX_06;
  undefined4 extraout_ECX_07;
  undefined4 extraout_ECX_08;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  ushort unaff_BX;
  undefined8 uVar7;
  short local_24;
  uint local_18;

  local_18 = 0;
  FUN_00418a74(param_1,(uint)unaff_BX * 0x114 + 0x49a0d4);
  uVar3 = FUN_00447107();
  uVar6 = extraout_ECX;
  for (uVar1 = 0; uVar1 < uVar3; uVar1 = uVar1 + 1) {
    uVar4 = FUN_004472de(uVar6,(uint)uVar1);
    uVar4 = unidade_obter_vida(uVar4);
    uVar7 = FUN_00441108(extraout_ECX_00,extraout_EDX);
    uVar6 = extraout_ECX_01;
    if ((uVar4 == (ushort)uVar7) &&
       (bVar2 = unidade_obter_tipo((ushort)((ulonglong)uVar7 >> 0x20)), uVar6 = extraout_ECX_02,
       bVar2 == 9)) {
      FUN_0045c455('\x01',param_2,(&DAT_0049a0cc)[(uint)unaff_BX * 0x114]);
      local_18 = local_18 + 1;
      param_2 = param_2 + 8;
      uVar6 = extraout_ECX_03;
    }
  }
  for (; uVar7 = FUN_0041f3ed(uVar6,0),
      (int)(local_18 & 0xffff) < CONCAT31((int3)((ulonglong)uVar7 >> 0x28),(char)uVar7);
      local_18 = local_18 + 1) {
    FUN_0045b247('\x01',param_2);
    param_2 = param_2 + 8;
    uVar6 = extraout_ECX_04;
  }
  uVar3 = 0;
  uVar4 = FUN_00447107();
  uVar1 = 0;
  uVar6 = extraout_ECX_05;
  do {
    if (uVar4 <= uVar1) {
      for (; uVar3 < DAT_00495be8; uVar3 = uVar3 + 1) {
        FUN_0045b247('\x01',param_2 + 0x30);
      }
      return;
    }
    uVar5 = FUN_004472de(uVar6,(uint)uVar1);
    uVar5 = unidade_obter_vida(uVar5);
    uVar7 = FUN_00441108(CONCAT22(extraout_var,uVar5),extraout_EDX_00);
    local_24 = (short)uVar7;
    if (extraout_CX == local_24) {
      uVar5 = unidade_obter_vida((ushort)((ulonglong)uVar7 >> 0x20));
      uVar7 = FUN_00441108(CONCAT22(extraout_var_00,uVar5),extraout_EDX_01);
      uVar6 = extraout_ECX_07;
      if (((short)extraout_ECX_07 != (short)uVar7) &&
         (bVar2 = unidade_obter_tipo((ushort)((ulonglong)uVar7 >> 0x20)), uVar6 = extraout_ECX_08,
         bVar2 != 9)) goto LAB_004019e5;
    }
    else {
LAB_004019e5:
      FUN_0045b247('\x01',param_2 + 0x30);
      uVar6 = extraout_ECX_06;
      uVar3 = uVar3 + 1;
    }
    uVar1 = uVar1 + 1;
  } while( true );
}
