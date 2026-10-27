/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004500e4, entrada 004500e4.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_004500e4(int param_1,char param_2)

{
  ulonglong uVar1;
  ulonglong uVar2;
  ushort uVar3;
  int iVar4;
  uint uVar5;
  uint uVar6;
  ushort *puVar7;
  int iVar8;
  uint unaff_EBX;
  uint uVar9;
  uint local_30;
  uint local_28;
  short local_24;
  ushort local_20;
  ushort local_1c;
  uint local_14;

  uVar2 = ((ulonglong)unaff_EBX & 0xffffffff0000ffff) % 0x100;
  iVar8 = (int)uVar2;
  uVar1 = ((ulonglong)unaff_EBX & 0xffffffff0000ffff) / 0x100;
  iVar4 = (int)uVar1;
  local_14 = param_1 * 2 + 1;
  local_1c = (ushort)param_1;
  if (local_1c < (ushort)uVar2) {
    uVar5 = iVar8 - param_1;
    local_28 = local_14;
  }
  else {
    local_28 = local_14 - (param_1 - iVar8);
    uVar5 = 0;
  }
  uVar3 = (ushort)uVar1;
  if (local_1c < uVar3) {
    local_30 = iVar4 - param_1;
  }
  else {
    local_14 = local_14 - (param_1 - iVar4);
    local_30 = 0;
  }
  local_1c = local_1c * local_1c;
  uVar9 = local_30 * 0x100 + uVar5;
  local_20 = (ushort)local_30;
  do {
    local_24 = (short)uVar5;
    uVar6 = (uint)(short)local_20;
    if ((int)((local_30 & 0xffff) + (local_14 & 0xffff)) <= (int)uVar6) {
      return uVar6 & 0xffffff00;
    }
    if ((int)uVar6 < 0x100) {
      for (; (int)local_24 < (int)((uVar5 & 0xffff) + (local_28 & 0xffff)); local_24 = local_24 + 1)
      {
        if (local_24 < 0x100) {
          puVar7 = (ushort *)((uVar9 & 0xffff) * 2 + DAT_004e0f38);
          if ((*puVar7 >> 8 & 0xc0) == 0x40) {
            iVar4 = (int)(*puVar7 & 0x3ff8) >> 3;
          }
          else {
            iVar4 = 0xffff;
          }
          if (((iVar4 != 0xffff) && (tabela_unidades[iVar4].proprietario_id == param_2)) &&
             (iVar4 = FUN_00479555(local_20,uVar3), (ushort)iVar4 <= local_1c)) {
            return CONCAT31((int3)((uint)iVar4 >> 8),1);
          }
        }
        uVar9 = uVar9 + 1;
      }
    }
    local_20 = local_20 + 1;
    uVar9 = uVar9 + (0x100 - local_28);
  } while( true );
}
