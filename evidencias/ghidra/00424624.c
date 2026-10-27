/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00424624, entrada 00424624.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00424624(undefined4 param_1,undefined4 param_2)

{
  ushort uVar1;
  byte bVar2;
  ushort in_AX;
  undefined2 uVar3;
  int iVar4;
  uint uVar5;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  uint extraout_ECX_02;
  int extraout_ECX_03;
  undefined4 extraout_EDX;
  short sVar6;
  short extraout_var;
  uint uVar7;
  bool bVar8;
  bool bVar9;
  longlong lVar10;
  undefined8 uVar11;

  iVar4 = (uint)in_AX * 0x114;
  if (*(short *)(&DAT_0049a14e + iVar4) == -1) {
    uVar5 = 0xffff;
  }
  else {
    uVar1 = *(ushort *)(&DAT_0049a0ca + iVar4) / 0x100;
    switch((&DAT_0049a0d0)[iVar4]) {
    case 0:
      param_1 = 0x14;
      break;
    case 1:
    case 3:
    case 5:
    case 6:
    case 7:
    case 8:
    case 0xd:
    case 0xe:
    case 0xf:
    case 0x10:
    case 0x12:
    case 0x14:
      param_1 = 8;
      break;
    case 2:
      param_1 = 10;
      break;
    case 4:
      param_1 = 5;
      break;
    case 10:
    case 0xb:
      param_1 = 7;
      break;
    case 0x11:
    case 0x13:
    case 0x15:
      param_1 = 4;
    }
    bVar2 = (&DAT_0049a143)[iVar4];
    uVar5 = 0;
    if (bVar2 != 0) {
      if (bVar2 < 2) {
        lVar10 = FUN_00443dad(param_1,(uint)*(ushort *)(&DAT_0049a0ca + iVar4) % 0x100);
        uVar5 = (uint)lVar10;
        if ((char)lVar10 != '\0') {
          bVar2 = unidade_obter_proprietario(*(ushort *)(&DAT_0049a14e + iVar4));
          uVar5 = (uint)bVar2;
          if (uVar5 != 200) {
            uVar11 = FUN_00440e11(extraout_ECX,extraout_EDX);
            uVar5 = (uint)uVar11 & 0xff;
            if (uVar5 != 0xe) {
              FUN_0044113e(extraout_ECX_00,0);
              uVar11 = FUN_0044113e(extraout_ECX_01,0);
              sVar6 = (short)((ulonglong)uVar11 >> 0x30);
              uVar7 = (extraout_ECX_02 & 0xffff) * (extraout_ECX_02 & 0xffff);
              uVar5 = FUN_00479555((ushort)(CONCAT44((int)sVar6 >> 0xf,CONCAT22(sVar6,(short)uVar11)
                                                    ) / 0x100),uVar1);
              bVar8 = uVar5 < uVar7;
              bVar9 = uVar5 == uVar7;
              goto LAB_00424786;
            }
          }
        }
      }
      else if (((bVar2 == 3) &&
               (uVar5 = 0, (&DAT_0049a0cd)[(uint)*(ushort *)(&DAT_0049a14e + iVar4) * 0x114] != '\0'
               )) && (uVar5 = (uint)(byte)(&DAT_0049a0cc)[iVar4], uVar5 != 200)) {
        FUN_0041aee2();
        uVar3 = FUN_0041aee2();
        uVar5 = FUN_00479555((ushort)(CONCAT44((int)extraout_var >> 0xf,CONCAT22(extraout_var,uVar3)
                                              ) / (longlong)extraout_ECX_03),uVar1);
        bVar8 = uVar5 < 100;
        bVar9 = uVar5 == 100;
LAB_00424786:
        if (bVar8 || bVar9) {
          uVar5 = CONCAT31((int3)(uVar5 >> 8),1);
          goto LAB_00424843;
        }
      }
    }
  }
  uVar5 = uVar5 & 0xffffff00;
LAB_00424843:
  return CONCAT44(param_2,uVar5);
}
