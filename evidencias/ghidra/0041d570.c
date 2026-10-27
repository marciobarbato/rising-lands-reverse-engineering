/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0041d570, entrada 0041d570.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_0041d570(void)

{
  ushort uVar1;
  ushort uVar2;
  ushort uVar3;
  bool bVar4;
  ushort uVar5;
  uint in_EAX;
  int iVar6;
  int iVar7;
  uint uVar8;
  undefined4 uVar9;
  int extraout_ECX;
  int extraout_ECX_00;
  undefined4 extraout_ECX_01;
  int extraout_ECX_02;
  ushort in_DX;
  int iVar10;
  int iVar11;
  short sVar12;
  undefined4 local_20;

  iVar6 = (in_EAX & 0xffff) * 0x114;
  uVar1 = *(ushort *)(&DAT_00495d8c + (uint)(byte)(&DAT_0049a0d0)[iVar6] * 0x34);
  uVar2 = *(ushort *)(&DAT_00495d8e + (uint)(byte)(&DAT_0049a0d0)[iVar6] * 0x34);
  uVar5 = (*(ushort *)(&DAT_00495d8e + (uint)(byte)(&DAT_0049a0d0)[iVar6] * 0x34) >> 1) * 0x100 +
          (*(ushort *)(&DAT_00495d8c + (uint)(byte)(&DAT_0049a0d0)[iVar6] * 0x34) >> 1) +
          *(short *)(&DAT_0049a0ca + iVar6);
  uVar3 = *(ushort *)(&DAT_0049a0ca + iVar6);
  local_20 = 0xfe00;
  for (sVar12 = -2; sVar12 < 5; sVar12 = sVar12 + 1) {
    iVar6 = (int)sVar12 + (int)(short)(uVar5 / 0x100);
    if ((-1 < iVar6) && (iVar6 < 0x100)) {
      iVar11 = (uint)uVar3 + (uVar2 - 1) * 0x100 + (uVar1 - 2) + 0xfdfc + local_20;
      for (iVar6 = -2; iVar10 = (int)(short)iVar6, iVar10 < 5; iVar6 = iVar6 + 1) {
        iVar7 = (short)(uVar5 % 0x100) + iVar10;
        if ((((-1 < iVar7) && (iVar7 < 0x100)) && ((iVar10 != 0 || (sVar12 != 0)))) &&
           ((bVar4 = FUN_004761d4(iVar6,1), iVar6 = extraout_ECX, !bVar4 &&
            (uVar8 = FUN_0041ab5c(extraout_ECX,
                                  (uint)(ushort)((short)(uVar1 - 2) * sVar12 + (short)extraout_ECX))
            , iVar6 = extraout_ECX_00, (char)uVar8 != '\0')))) {
          unidade_obter_tipo(in_DX);
          uVar8 = FUN_00442394();
          if (((char)uVar8 == '\0') ||
             (uVar9 = FUN_0041d499(extraout_ECX_01,(ushort)iVar11), iVar6 = extraout_ECX_02,
             (char)uVar9 != '\0')) goto LAB_0041d745;
        }
        iVar11 = iVar11 + 1;
      }
    }
    local_20 = (uint)(byte)(local_20._1_1_ + 1) << 8;
  }
LAB_0041d745:
  FUN_0042399a();
  return;
}
