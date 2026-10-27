/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00424de4, entrada 00424de4.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00424de4(void)

{
  byte bVar1;
  ushort in_AX;
  ushort uVar2;
  ushort indice_unidade;
  int iVar3;
  undefined4 uVar4;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  ushort indice_unidade_00;
  ushort uVar5;
  bool bVar6;
  ulonglong uVar7;

  uVar4 = 0;
  if ((&DAT_0049a0d0)[(uint)in_AX * 0x114] == '\x15') {
    uVar7 = FUN_0044724a(0,0x15);
    bVar6 = (char)uVar7 == '\0';
LAB_00424e1f:
    if (bVar6) {
      bVar6 = false;
      goto LAB_00424e4c;
    }
  }
  else {
    if ((&DAT_0049a0d0)[(uint)in_AX * 0x114] != '\x02') {
LAB_00424e33:
      iVar3 = FUN_004471b8(uVar4,'\x01');
      bVar6 = (short)iVar3 == 0;
      goto LAB_00424e1f;
    }
    uVar7 = FUN_0044724a(0,2);
    uVar4 = extraout_ECX;
    if ((char)uVar7 == '\0') goto LAB_00424e33;
  }
  bVar6 = true;
LAB_00424e4c:
  if ((bVar6) && ((&DAT_004e2e7c)[(byte)(&DAT_0049a0cc)[(uint)in_AX * 0x114]] == '\0')) {
    uVar2 = FUN_00447107();
    uVar4 = extraout_ECX_00;
    for (uVar5 = 0; uVar5 < uVar2; uVar5 = uVar5 + 1) {
      indice_unidade = FUN_004472de(uVar4,(uint)uVar5);
      bVar1 = unidade_obter_tipo(indice_unidade);
      uVar4 = extraout_ECX_02;
      if (bVar1 != 9) {
        uVar4 = CONCAT31((int3)((uint)extraout_ECX_02 >> 8),1);
      }
      if ((char)uVar4 != '\0') {
        iVar3 = (uint)in_AX * 0x114;
        if ((*(short *)(&DAT_0049a150 + iVar3) == 0) || (*(short *)(&DAT_0049a150 + iVar3) == -1)) {
          (&DAT_0049a0cd)[iVar3] = 4;
          (&DAT_0049a13c)[iVar3] = 1;
          *(undefined2 *)(&DAT_0049a146 + iVar3) = 0x80;
          *(undefined2 *)(&DAT_0049a148 + iVar3) = 0;
          *(undefined2 *)(&DAT_0049a14a + iVar3) = 0xffab;
          *(ushort *)(&DAT_0049a150 + iVar3) = indice_unidade_00;
          FUN_004570f4(uVar4,0xd);
          bVar1 = unidade_obter_tipo(indice_unidade_00);
          (&DAT_0049a143)[iVar3] = bVar1;
        }
        break;
      }
      bVar1 = unidade_obter_tipo(indice_unidade_00);
      uVar4 = extraout_ECX_01;
      if (bVar1 == 9) {
        uVar4 = CONCAT31((int3)((uint)extraout_ECX_01 >> 8),1);
      }
    }
  }
  FUN_0041db1e();
  return;
}
