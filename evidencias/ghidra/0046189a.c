/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0046189a, entrada 0046189a.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0046189a(undefined4 param_1,byte param_2)

{
  short *psVar1;
  short sVar2;
  byte in_AL;
  byte bVar3;
  ushort uVar4;
  ushort indice_unidade;
  short sVar5;
  undefined4 uVar6;
  undefined1 extraout_CL;
  undefined1 extraout_CL_00;
  uint extraout_ECX;
  undefined4 extraout_ECX_00;
  uint extraout_ECX_01;
  uint uVar7;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  undefined4 extraout_ECX_06;
  undefined4 extraout_ECX_07;
  undefined4 extraout_ECX_08;
  uint uVar8;
  undefined4 extraout_EDX;
  int iVar9;
  int iVar10;
  ushort uVar11;
  undefined8 uVar12;
  byte local_2c;
  byte local_28;
  byte local_24;
  byte local_20;

  local_20 = 0;
  do {
    if (0x19 < local_20) {
      for (local_2c = 0; local_2c < 3; local_2c = local_2c + 1) {
        iVar9 = (uint)local_2c * 2 + (uint)param_2 * 6;
        if (*(short *)(&DAT_004e2d14 + iVar9) != 0) {
          uVar12 = FUN_0046d817((uint)local_2c,iVar9);
          if (((uint)uVar12 & 0xff) == 1) {
            FUN_004235bd(extraout_ECX_08,
                         *(ushort *)(&DAT_004e2d14 + (int)((ulonglong)uVar12 >> 0x20)));
          }
          iVar9 = (uint)param_2 * 4 + (uint)local_2c;
          iVar10 = (uint)param_2 * 6 + (uint)local_2c * 2;
          sVar5 = *(short *)(&DAT_004e2d14 + iVar10);
          sVar2 = *(short *)(&DAT_004e2ea8 + iVar9 * 8);
          *(short *)(&DAT_004e2eaa + iVar9 * 8) = *(short *)(&DAT_004e2eaa + iVar9 * 8) + sVar5;
          *(undefined2 *)(&DAT_004e2d14 + iVar10) = 0;
          *(short *)(&DAT_004e2ea8 + iVar9 * 8) = sVar2 + sVar5;
        }
      }
      return;
    }
    uVar8 = (uint)*(ushort *)((int)&DAT_004e2a8c + (uint)local_20 * 2 + (uint)param_2 * 0x34);
    if (uVar8 != 0) {
      for (local_24 = 0; local_24 < uVar8; local_24 = local_24 + 1) {
        uVar7 = uVar8;
        for (local_28 = 0; local_28 < 10; local_28 = local_28 + 1) {
          if (*(ushort *)(&DAT_004e296c + (uint)param_2 * 0x14 + (uint)local_28 * 2) != 0xffff) {
            FUN_00418a74(0,&DAT_0049a0c8 +
                           (uint)*(ushort *)
                                  (&DAT_004e296c + (uint)param_2 * 0x14 + (uint)local_28 * 2) *
                           0x114);
            uVar4 = FUN_00447107();
            uVar7 = extraout_ECX;
            for (uVar11 = 0; uVar11 < uVar4; uVar11 = uVar11 + 1) {
              indice_unidade = FUN_004472de(uVar7,(uint)uVar11);
              bVar3 = unidade_obter_proprietario(indice_unidade);
              uVar12 = FUN_0041a08c(extraout_ECX_00,CONCAT31((int3)((uint)extraout_EDX >> 8),bVar3))
              ;
              uVar7 = extraout_ECX_01;
              if ((char)((ulonglong)uVar12 >> 0x20) != (char)uVar12) {
                uVar7 = extraout_ECX_01 + 1;
              }
            }
            uVar7 = uVar7 & 0xffff;
            if (uVar7 < DAT_00495be9 / 2) {
              uVar7 = (uint)local_28;
              sVar5 = *(short *)(&DAT_004e296c + uVar7 * 2 + (uint)param_2 * 0x14);
              goto LAB_004619b9;
            }
          }
        }
        sVar5 = -1;
LAB_004619b9:
        if (sVar5 != -1) {
          uVar12 = FUN_0046d817((uint)in_AL,uVar7);
          if (((uint)uVar12 & 0xff) == 1) {
            uVar7 = FUN_004612fe(extraout_ECX_02,local_20);
            if ((uVar7 & 0xffff) != 0xffff) {
              FUN_0046153a(extraout_ECX_03,(short)uVar7);
              FUN_00447483(extraout_ECX_04,1);
LAB_00461a2e:
              psVar1 = (short *)((int)&DAT_004e2a8c + (uint)local_20 * 2 + (uint)param_2 * 0x34);
              *psVar1 = *psVar1 + -1;
            }
          }
          else {
            uVar12 = FUN_0046d817(extraout_ECX_02,(int)((ulonglong)uVar12 >> 0x20));
            if (((uint)uVar12 & 0xff) == 2) {
              uVar7 = FUN_00442434();
              if ((char)uVar7 == '\0') {
                FUN_0041aee2();
                uVar6 = FUN_00457e6c(extraout_CL_00);
              }
              else {
                FUN_0041aee2();
                uVar4 = FUN_00457e6c(extraout_CL);
                FUN_0041aee2();
                uVar6 = FUN_00457e6c(200);
                FUN_00447694(uVar6,uVar4);
                FUN_0044115f(extraout_ECX_05,0xe);
                uVar6 = extraout_ECX_06;
              }
              FUN_0044115f(uVar6,0xe);
              FUN_00447483(extraout_ECX_07,1);
              goto LAB_00461a2e;
            }
          }
        }
      }
    }
    local_20 = local_20 + 1;
  } while( true );
}
