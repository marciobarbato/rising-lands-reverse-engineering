/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00461621, entrada 00461621.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00461621(undefined4 param_1,byte param_2)

{
  short *psVar1;
  short sVar2;
  short sVar3;
  byte in_AL;
  byte bVar4;
  ushort uVar5;
  ushort indice_unidade;
  uint uVar6;
  uint extraout_ECX;
  undefined4 extraout_ECX_00;
  uint extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  uint uVar7;
  uint uVar8;
  undefined4 extraout_EDX;
  int iVar9;
  int iVar10;
  ushort uVar11;
  undefined8 uVar12;
  byte local_28;
  byte local_24;
  byte local_20;
  byte local_18;

  local_28 = 0;
  do {
    if (0x19 < local_28) {
      for (local_18 = 0; local_18 < 3; local_18 = local_18 + 1) {
        iVar9 = (uint)local_18 * 2 + (uint)param_2 * 6;
        if (*(short *)(&DAT_004e2cfc + iVar9) != 0) {
          uVar12 = FUN_0046d817((uint)local_18,iVar9);
          if (((uint)uVar12 & 0xff) == 1) {
            FUN_004235bd(extraout_ECX_05,
                         *(ushort *)(&DAT_004e2cfc + (int)((ulonglong)uVar12 >> 0x20)));
          }
          iVar9 = (uint)in_AL * 4 + (uint)local_18;
          iVar10 = (uint)local_18 * 2 + (uint)param_2 * 6;
          sVar2 = *(short *)(&DAT_004e2cfc + iVar10);
          sVar3 = *(short *)(&DAT_004e2ea8 + iVar9 * 8);
          *(short *)(&DAT_004e2eaa + iVar9 * 8) = *(short *)(&DAT_004e2eaa + iVar9 * 8) + sVar2;
          *(undefined2 *)(&DAT_004e2cfc + iVar10) = 0;
          *(short *)(&DAT_004e2ea8 + iVar9 * 8) = sVar3 + sVar2;
        }
      }
      return;
    }
    uVar7 = (uint)*(ushort *)((int)&DAT_004e29bc + (uint)local_28 * 2 + (uint)param_2 * 0x34);
    if (uVar7 != 0) {
      for (local_20 = 0; uVar8 = (uint)local_20, uVar8 < uVar7; local_20 = local_20 + 1) {
        for (local_24 = 0; local_24 < 10; local_24 = local_24 + 1) {
          uVar8 = (uint)in_AL * 0x14;
          if (*(short *)(&DAT_004e296c + uVar8 + (uint)local_24 * 2) != -1) {
            FUN_00418a74(0,uVar8);
            uVar5 = FUN_00447107();
            uVar8 = extraout_ECX;
            for (uVar11 = 0; uVar11 < uVar5; uVar11 = uVar11 + 1) {
              indice_unidade = FUN_004472de(uVar8,(uint)uVar11);
              bVar4 = unidade_obter_proprietario(indice_unidade);
              uVar12 = FUN_0041a08c(extraout_ECX_00,CONCAT31((int3)((uint)extraout_EDX >> 8),bVar4))
              ;
              uVar8 = extraout_ECX_01;
              if ((char)((ulonglong)uVar12 >> 0x20) != (char)uVar12) {
                uVar8 = extraout_ECX_01 + 1;
              }
            }
            uVar8 = uVar8 & 0xffff;
            if (uVar8 < DAT_00495be9 / 2) {
              uVar8 = (uint)in_AL * 0x14;
              uVar6 = (uint)*(ushort *)(&DAT_004e296c + (uint)local_24 * 2 + uVar8);
              goto LAB_00461749;
            }
          }
        }
        uVar6 = 0xffff;
LAB_00461749:
        if (uVar6 != 0xffff) {
          uVar12 = FUN_0046d817(&DAT_0049a0c8 + uVar6 * 0x114,uVar8);
          if (((uint)uVar12 & 0xff) == 1) {
            uVar8 = FUN_004612fe(extraout_ECX_02,local_28);
            if ((uVar8 & 0xffff) != 0xffff) {
              FUN_0046153a(extraout_ECX_03,(short)uVar8);
              FUN_00447483(extraout_ECX_04,1);
              psVar1 = (short *)((int)&DAT_004e29bc + (uint)local_28 * 2 + (uint)param_2 * 0x34);
              *psVar1 = *psVar1 + -1;
            }
          }
        }
      }
    }
    local_28 = local_28 + 1;
  } while( true );
}
