/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00487e2a, entrada 00487e2a.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00487e2a(undefined4 param_1,int param_2)

{
  short *psVar1;
  int iVar2;
  byte bVar3;
  undefined4 in_EAX;
  uint uVar4;
  ushort *puVar5;
  undefined4 *puVar6;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint uVar7;
  uint unaff_EBX;
  int iVar8;
  undefined8 uVar9;

  if ((unaff_EBX & 0x8000) == 0) {
    bVar3 = unidade_obter_proprietario((ushort)unaff_EBX);
    uVar4 = (uint)bVar3;
    uVar7 = extraout_ECX_00;
  }
  else {
    uVar9 = FUN_0041a08c(in_EAX,param_2);
    uVar4 = (uint)uVar9;
    uVar7 = extraout_ECX;
  }
  if (((uVar4 & 0xff) != uVar7) && (unaff_EBX != 0xffff)) {
    iVar2 = param_2 * 0x110 + uVar7 * 0x1144;
    puVar5 = (ushort *)(&DAT_0051bd24 + uVar7 * 0x451 + param_2 * 0x44 + 4);
    for (iVar8 = 0; uVar4 = (uint)*(ushort *)((int)&DAT_0051bd24 + iVar2 + 0xe), iVar8 < (int)uVar4;
        iVar8 = iVar8 + 1) {
      if (*puVar5 == unaff_EBX) {
        if (iVar8 < (int)(uVar4 - 1)) {
          puVar6 = &DAT_0051bd24 + uVar7 * 0x451 + param_2 * 0x44 + iVar8 * 2;
          for (; iVar8 < (int)(*(ushort *)((int)&DAT_0051bd24 + iVar2 + 0xe) - 1); iVar8 = iVar8 + 1
              ) {
            puVar6[4] = puVar6[6];
            puVar6[5] = puVar6[7];
            puVar6 = puVar6 + 2;
          }
        }
        psVar1 = (short *)((int)&DAT_0051bd24 + iVar2 + 0xe);
        *psVar1 = *psVar1 + -1;
        return;
      }
      puVar5 = puVar5 + 4;
    }
  }
  return;
}
