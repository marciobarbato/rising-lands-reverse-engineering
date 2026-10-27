/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00423fb9, entrada 00423fb9.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00423fb9(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  byte bVar2;
  char cVar3;
  uint in_EAX;
  int iVar4;
  undefined4 uVar5;
  uint uVar6;
  uint uVar7;
  undefined4 uVar8;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  int extraout_ECX_05;
  undefined4 extraout_ECX_06;
  uint uVar9;
  uint extraout_EDX;
  uint extraout_EDX_00;
  uint extraout_EDX_01;
  uint extraout_EDX_02;
  short sVar10;
  uint extraout_EDX_03;
  ushort indice_unidade;
  longlong lVar11;
  undefined8 uVar12;
  ushort local_24;

  iVar4 = (in_EAX & 0xffff) * 0x114;
  bVar1 = (&DAT_0049a0cc)[iVar4];
  uVar8 = 0x100;
  local_24 = *(ushort *)(&DAT_0049a0ca + iVar4) / 0x100;
  uVar9 = (uint)*(ushort *)(&DAT_0049a0ca + iVar4) % 0x100;
  for (iVar4 = 0; indice_unidade = (ushort)iVar4, (short)indice_unidade < 800; iVar4 = iVar4 + 1) {
    lVar11 = FUN_00443dad(uVar8,uVar9);
    uVar9 = (uint)((ulonglong)lVar11 >> 0x20);
    uVar8 = extraout_ECX;
    if ((char)lVar11 != '\0') {
      uVar5 = FUN_00446fbf(extraout_ECX,bVar1);
      uVar8 = extraout_ECX_00;
      uVar9 = extraout_EDX;
      if ((char)uVar5 != '\0') {
        uVar12 = FUN_00440e11(extraout_ECX_00,extraout_EDX);
        uVar9 = (uint)((ulonglong)uVar12 >> 0x20);
        uVar8 = extraout_ECX_01;
        if (((uint)uVar12 & 0xff) != 0xe) {
          bVar2 = unidade_obter_tipo(indice_unidade);
          uVar8 = extraout_ECX_02;
          uVar9 = extraout_EDX_00;
          if (bVar2 != 0x11) {
            bVar2 = unidade_obter_tipo(indice_unidade);
            uVar8 = extraout_ECX_03;
            uVar9 = extraout_EDX_01;
            if (bVar2 != 10) {
              unidade_obter_tipo(indice_unidade);
              cVar3 = FUN_004422cf();
              if (cVar3 != '\0') {
                uVar8 = extraout_ECX_04;
                uVar9 = extraout_EDX_02;
                if ((&DAT_0049a0d0)[(in_EAX & 0xffff) * 0x114] == '\v') goto LAB_00424012;
              }
              FUN_0044113e(extraout_ECX_04,0);
              uVar12 = FUN_0044113e(0x100,0);
              sVar10 = (short)((ulonglong)uVar12 >> 0x30);
              uVar6 = (uint)DAT_00495c00;
              uVar7 = FUN_00479555((ushort)(CONCAT44((int)sVar10 >> 0xf,
                                                     CONCAT22(sVar10,(short)uVar12)) /
                                           (longlong)extraout_ECX_05),local_24);
              uVar8 = extraout_ECX_06;
              uVar9 = extraout_EDX_03;
              if (uVar7 <= uVar6 * uVar6) goto LAB_0041d2f4;
            }
          }
        }
      }
    }
LAB_00424012:
  }
  iVar4 = 0xffff;
LAB_0041d2f4:
  return CONCAT44(param_2,iVar4);
}
