/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0041fb12, entrada 0041fb12.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_0041fb12(undefined4 param_1,uint param_2)

{
  ushort uVar1;
  ushort uVar2;
  byte in_AL;
  byte bVar3;
  bool bVar4;
  ushort *puVar5;
  undefined3 extraout_var;
  uint uVar6;
  int iVar7;
  undefined4 extraout_ECX;
  ushort unaff_BX;
  uint uVar8;
  ushort uVar9;
  uint local_1c;

  iVar7 = (uint)in_AL * 0x34;
  uVar1 = *(ushort *)(&DAT_00495d8c + iVar7);
  uVar2 = *(ushort *)(&DAT_00495d8e + iVar7);
  uVar8 = (param_2 - (uVar1 - 1)) + (uVar2 - 1) * -0x100;
  if (in_AL == 0xc) {
    local_1c = param_2 & 0xffff;
    if (*(char *)(DAT_00507d74 + local_1c) == DAT_00495bf8) {
      puVar5 = (ushort *)(DAT_004e0f38 + local_1c * 2);
      if ((*puVar5 & 0x8000) == 0) {
        local_1c = 0xffff;
      }
      else {
        local_1c = (int)(*puVar5 & 0x7fe0) >> 5;
      }
      if (local_1c != 0xffff) {
        iVar7 = local_1c * 0x114;
        bVar3 = unidade_obter_proprietario(unaff_BX);
        local_1c = CONCAT31(extraout_var,bVar3);
        if (bVar3 == (&DAT_0049a0cc)[iVar7]) goto LAB_0041fbd4;
      }
    }
    local_1c = local_1c & 0xffffff00;
  }
  else {
    for (local_1c = 0; (ushort)local_1c < uVar2; local_1c = local_1c + 1) {
      for (uVar9 = 0; uVar9 < uVar1; uVar9 = uVar9 + 1) {
        bVar4 = FUN_004761d4(uVar8 & 0xffff,1);
        if ((bVar4) &&
           (uVar6 = FUN_0044246e(extraout_ECX,(ushort)extraout_ECX), (char)uVar6 == '\0')) {
          return uVar6;
        }
        uVar8 = uVar8 + 1;
      }
      uVar8 = uVar8 + (0x100 - (uint)uVar1);
    }
LAB_0041fbd4:
    local_1c = CONCAT31((int3)(local_1c >> 8),1);
  }
  return local_1c;
}
