/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00461ce5, entrada 00461ce5.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00461ce5(void)

{
  short *psVar1;
  ushort uVar2;
  bool bVar3;
  byte in_AL;
  byte bVar4;
  ushort uVar5;
  ushort indice_unidade;
  uint extraout_ECX;
  int iVar7;
  uint uVar6;
  undefined4 extraout_ECX_00;
  int extraout_ECX_01;
  int extraout_ECX_02;
  byte extraout_DH;
  undefined4 extraout_EDX;
  short sVar8;
  undefined8 uVar9;
  byte local_28;
  byte local_24;

  local_24 = 0;
  do {
    if (0x19 < local_24) {
      return;
    }
    uVar2 = *(ushort *)((int)&DAT_004e29bc + (uint)local_24 * 2 + (uint)in_AL * 0x34);
    if (uVar2 != 0) {
      for (local_28 = 0; local_28 < uVar2; local_28 = local_28 + 1) {
        for (bVar4 = 0; bVar4 < 10; bVar4 = bVar4 + 1) {
          sVar8 = *(short *)(&DAT_004e296c + (uint)bVar4 * 2 + (uint)in_AL * 0x14);
          if (sVar8 != -1) goto LAB_00461d69;
        }
        sVar8 = -1;
LAB_00461d69:
        if (sVar8 != -1) {
          FUN_00418a74(0,(uint)local_24);
          uVar5 = FUN_00447107();
          uVar6 = extraout_ECX;
          while ((ushort)uVar6 < uVar5) {
            indice_unidade = FUN_004472de(uVar6,uVar6 & 0xffff);
            bVar4 = unidade_obter_proprietario(indice_unidade);
            uVar9 = FUN_0041a08c(extraout_ECX_00,CONCAT31((int3)((uint)extraout_EDX >> 8),bVar4));
            iVar7 = extraout_ECX_01;
            if (((char)((ulonglong)uVar9 >> 0x20) == (char)uVar9) &&
               (bVar4 = unidade_obter_tipo(indice_unidade), iVar7 = extraout_ECX_02,
               bVar4 == extraout_DH)) {
              FUN_00443108(extraout_ECX_02,200);
              bVar3 = true;
              goto LAB_00461df5;
            }
            uVar6 = iVar7 + 1;
          }
          bVar3 = false;
LAB_00461df5:
          if (bVar3) {
            psVar1 = (short *)((int)&DAT_004e29bc + (uint)local_24 * 2 + (uint)in_AL * 0x34);
            *psVar1 = *psVar1 + -1;
          }
        }
      }
    }
    local_24 = local_24 + 1;
  } while( true );
}
