/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00424c2e, entrada 00424c2e.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00424c2e(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  char cVar2;
  ushort uVar3;
  ushort uVar4;
  ushort uVar5;
  undefined2 uVar6;
  uint uVar7;
  undefined3 extraout_var;
  undefined2 extraout_var_00;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  int extraout_ECX;
  int iVar8;
  int extraout_ECX_00;
  int extraout_ECX_01;
  undefined4 extraout_ECX_02;
  int extraout_ECX_03;
  undefined4 extraout_ECX_04;
  int extraout_ECX_05;
  undefined4 extraout_ECX_06;
  int extraout_ECX_07;
  undefined4 extraout_ECX_08;
  int extraout_ECX_09;
  undefined4 extraout_EDX;
  ushort uVar9;
  undefined8 uVar10;

  uVar3 = FUN_00447107();
  uVar7 = (uint)(CONCAT44(extraout_EDX,DAT_00508f7c) / 0x4b);
  if ((int)(CONCAT44(extraout_EDX,DAT_00508f7c) % 0x4b) == 0) {
    iVar8 = extraout_ECX;
    for (uVar9 = 0; uVar9 < uVar3; uVar9 = uVar9 + 1) {
      bVar1 = FUN_004472d3(iVar8,(uint)uVar9);
      uVar7 = (uint)bVar1;
      iVar8 = extraout_ECX_00;
      if (uVar7 == 1) {
        uVar4 = FUN_004472de(extraout_ECX_00,(uint)uVar9);
        unidade_obter_tipo(uVar4);
        cVar2 = FUN_00442347();
        uVar7 = CONCAT31(extraout_var,cVar2);
        iVar8 = extraout_ECX_01;
        if (cVar2 != '\0') {
          uVar5 = unidade_obter_vida(uVar4);
          uVar10 = FUN_00441108(extraout_ECX_02,CONCAT22(extraout_var_00,uVar5));
          uVar7 = (uint)uVar10;
          iVar8 = extraout_ECX_03;
          if ((ushort)((ulonglong)uVar10 >> 0x20) < (ushort)uVar10) {
            FUN_0041b327(extraout_ECX_03);
            uVar4 = unidade_obter_vida(uVar4);
            uVar10 = FUN_00441108(extraout_ECX_04,CONCAT22(extraout_var_01,uVar4));
            if (((short)((ulonglong)uVar10 >> 0x20) == (short)uVar10) ||
               (uVar7 = (uint)*(byte *)(extraout_ECX_05 + 4), iVar8 = extraout_ECX_05,
               (&DAT_004dfb58)[uVar7] != '\0')) {
              uVar4 = FUN_004473cf(extraout_ECX_05,uVar9);
              uVar10 = FUN_0041d1d0(extraout_ECX_06,CONCAT22(extraout_var_02,uVar4));
              *(short *)(extraout_ECX_07 + 0x7c) = (short)uVar10;
              uVar6 = FUN_00420698();
              FUN_00445fbc(extraout_ECX_08,uVar6);
              uVar7 = FUN_004457d3();
              (&DAT_004dfb58)[*(byte *)(extraout_ECX_09 + 4)] = 0;
              iVar8 = extraout_ECX_09;
            }
          }
        }
      }
    }
  }
  return CONCAT44(param_2,uVar7);
}
