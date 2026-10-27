/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00401729, entrada 00401729.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00401729(undefined4 param_1,undefined2 param_2)

{
  ushort uVar1;
  bool bVar2;
  byte bVar3;
  ushort uVar4;
  ushort indice_unidade;
  int iVar5;
  char extraout_CL;
  short sVar6;
  int extraout_ECX;
  int iVar7;
  undefined4 extraout_ECX_00;
  int extraout_ECX_01;
  int extraout_ECX_02;
  int extraout_ECX_03;
  ushort indice_unidade_00;
  undefined4 extraout_EDX;
  uint unaff_EBX;
  uint uVar8;
  undefined8 uVar9;
  undefined2 uStack_1a;

  uStack_1a = (undefined2)(unaff_EBX >> 0x10);
  iVar5 = (unaff_EBX & 0xffff) * 0x114;
  bVar2 = false;
  uVar8 = 0;
  uVar9 = FUN_00418a74(1,CONCAT22(param_2,uStack_1a));
  FUN_0045c455(extraout_CL,(short)((ulonglong)uVar9 >> 0x30),(&DAT_0049a0cc)[iVar5]);
  uVar4 = FUN_00447107();
  iVar7 = extraout_ECX + 0x30;
  sVar6 = (short)iVar7;
  for (uVar1 = 0; uVar1 < uVar4; uVar1 = uVar1 + 1) {
    indice_unidade = FUN_004472de(iVar7,(uint)uVar1);
    bVar3 = unidade_obter_tipo(indice_unidade);
    if ((bVar3 != 9) || (bVar2)) {
      bVar3 = unidade_obter_proprietario(indice_unidade_00);
      uVar9 = FUN_0041a08c(extraout_ECX_00,CONCAT31((int3)((uint)extraout_EDX >> 8),bVar3));
      iVar7 = extraout_ECX_01;
      if ((char)((ulonglong)uVar9 >> 0x20) == (char)uVar9) {
        uVar8 = uVar8 + 1;
        FUN_0045c455('\x01',sVar6,(&DAT_0049a0cc)[iVar5]);
        iVar7 = extraout_ECX_02;
      }
    }
    else {
      bVar2 = true;
      iVar7 = extraout_ECX_03;
    }
  }
  for (; (uVar8 & 0xffff) < DAT_00495be9 / 2; uVar8 = uVar8 + 1) {
    FUN_0045b247('\x01',sVar6);
  }
  return;
}
