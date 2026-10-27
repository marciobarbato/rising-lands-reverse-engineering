/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0041fc40, entrada 0041fc40.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_0041fc40(undefined4 param_1,uint param_2)

{
  ushort uVar1;
  ushort uVar2;
  byte bVar3;
  bool bVar4;
  uint in_EAX;
  uint uVar5;
  uint uVar6;
  uint uVar7;
  uint uVar8;
  undefined4 uVar9;
  int iVar10;
  int extraout_ECX;
  uint uVar11;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  uint extraout_ECX_03;
  uint uVar12;
  int iVar13;
  undefined4 extraout_EDX;
  int extraout_EDX_00;
  int extraout_EDX_01;
  ushort unaff_BX;
  ushort uVar14;
  uint uVar15;
  undefined8 uVar16;
  longlong lVar17;
  uint local_18;

  uVar5 = in_EAX & 0xff;
  uVar1 = *(ushort *)(&DAT_00495d8c + uVar5 * 0x34);
  uVar6 = (uint)uVar1;
  uVar2 = *(ushort *)(&DAT_00495d8e + uVar5 * 0x34);
  uVar11 = (uint)uVar2;
  uVar12 = (uint)(((ulonglong)param_2 & 0xffffffff0000ffff) % 0x100);
  uVar7 = (uint)(((ulonglong)param_2 & 0xffffffff0000ffff) / 0x100);
  DAT_004e05b8 = 1;
  FUN_0048c3b0(param_2 & 0xffff,1);
  uVar8 = uVar6 / 2;
  local_18 = uVar11 / 2;
  uVar15 = (extraout_ECX - uVar8) + local_18 * -0x100;
  if (((uVar8 <= uVar12) && (local_18 <= uVar7)) && ((int)((uVar6 - 1) + (uVar12 - uVar8)) < 0x101))
  {
    uVar7 = uVar7 - local_18;
    uVar11 = (uVar11 + uVar7) - 1;
    if ((int)uVar11 < 0x101) {
      if (uVar5 == 0xc) {
        for (uVar14 = 0; uVar14 < uVar2; uVar14 = uVar14 + 1) {
          iVar13 = 0;
          while ((ushort)iVar13 < uVar1) {
            lVar17 = FUN_0041ac8b(iVar13,uVar7);
            if ((*(char *)(DAT_00507d74 + (uVar15 & 0xffff)) != DAT_00495bf8) ||
               (uVar7 = (uint)(byte)lVar17, uVar7 == 0xff)) {
              uVar7 = uVar6 * uVar14;
              (&DAT_004e05b9)[(extraout_ECX_03 & 0xffff) + uVar7] = 0;
              DAT_004e05b8 = 0;
            }
            uVar15 = uVar15 + 1;
            iVar13 = extraout_ECX_03 + 1;
          }
          local_18 = 0x100 - uVar6;
          uVar15 = uVar15 + local_18;
        }
      }
      else {
        iVar13 = 0;
        for (local_18 = 0; (ushort)local_18 < uVar2; local_18 = local_18 + 1) {
          for (uVar14 = 0; uVar14 < uVar1; uVar14 = uVar14 + 1) {
            uVar16 = FUN_0047636a(uVar15 & 0xffff,iVar13);
            if ((char)uVar16 == '\0') {
LAB_0041fdfb:
              iVar13 = (local_18 & 0xffff) * uVar6;
              (&DAT_004e05b9)[iVar13 + (uint)uVar14] = 0;
              DAT_004e05b8 = 0;
            }
            else {
              bVar3 = unidade_obter_proprietario(unaff_BX);
              uVar9 = FUN_004766f0(extraout_ECX_00,CONCAT31((int3)((uint)extraout_EDX >> 8),bVar3));
              if (((char)uVar9 == '\0') ||
                 ((bVar4 = FUN_004761d4(extraout_ECX_01,1), iVar13 = extraout_EDX_00, bVar4 &&
                  (iVar10 = FUN_0044246e(extraout_ECX_02,(ushort)extraout_ECX_02),
                  iVar13 = extraout_EDX_01, (char)iVar10 == '\0')))) goto LAB_0041fdfb;
            }
            uVar15 = uVar15 + 1;
          }
          uVar15 = uVar15 + (0x100 - uVar6);
        }
      }
      return CONCAT31((int3)(local_18 >> 8),DAT_004e05b8);
    }
  }
  uVar5 = FUN_0048c3b0(uVar11,0);
  DAT_004e05b8 = 0;
  return uVar5 & 0xffffff00;
}
