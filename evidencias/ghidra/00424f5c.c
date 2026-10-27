/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00424f5c, entrada 00424f5c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined1 FUN_00424f5c(void)

{
  byte bVar1;
  ushort in_AX;
  ushort uVar2;
  ushort indice_unidade;
  undefined4 extraout_EDX;
  int3 iVar3;
  int iVar4;

  iVar4 = (uint)in_AX * 0x114;
  uVar2 = FUN_00447107();
  iVar3 = (int3)((uint)extraout_EDX >> 8);
  if ((((int)(uint)uVar2 < (CONCAT31(iVar3,DAT_00495be9) - ((int)iVar3 >> 0x17) >> 1) + 1) &&
      ((&DAT_0049a13c)[iVar4] == '\0')) &&
     ((*(short *)(&DAT_0049a150 + iVar4) == 0 || (*(short *)(&DAT_0049a150 + iVar4) == -1)))) {
    (&DAT_0049a0cd)[iVar4] = 4;
    (&DAT_0049a13c)[iVar4] = 1;
    *(undefined2 *)(&DAT_0049a146 + iVar4) = 0;
    *(undefined2 *)(&DAT_0049a148 + iVar4) = 0;
    *(undefined2 *)(&DAT_0049a14a + iVar4) = 0;
    *(ushort *)(&DAT_0049a150 + iVar4) = indice_unidade;
    bVar1 = unidade_obter_tipo(indice_unidade);
    (&DAT_0049a143)[iVar4] = bVar1;
    return 1;
  }
  return 0;
}
