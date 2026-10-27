/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00425516, entrada 00425516.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined4 __fastcall FUN_00425516(undefined4 param_1,ushort param_2)

{
  byte bVar1;
  ushort in_AX;
  ushort uVar2;
  int iVar3;
  ushort indice_unidade;
  undefined2 extraout_var;
  undefined2 local_14 [2];
  uint local_10;

  iVar3 = (uint)in_AX * 0x114;
  (&DAT_0049a0cd)[iVar3] = 4;
  (&DAT_0049a142)[iVar3] = 1;
  (&DAT_0049a13c)[iVar3] = 1;
  *(undefined2 *)(&DAT_0049a146 + iVar3) = 0;
  *(undefined2 *)(&DAT_0049a148 + iVar3) = 0;
  *(undefined2 *)(&DAT_0049a14a + iVar3) = 0;
  bVar1 = unidade_obter_tipo(param_2);
  (&DAT_0049a143)[iVar3] = bVar1;
  *(ushort *)(&DAT_0049a150 + iVar3) = param_2;
  uVar2 = unidade_obter_vida(indice_unidade);
  *(int *)(&DAT_0049a154 + iVar3) = CONCAT22(extraout_var,uVar2) * 100;
  unidade_obter_tipo(*(ushort *)(&DAT_0049a150 + iVar3));
  FUN_004410d2(local_14,(undefined2 *)&local_10);
  *(short *)(&DAT_004dfb5c + (uint)(byte)(&DAT_0049a0cc)[iVar3] * 2) =
       (short)(((local_10 >> 1 & 0x7fff) * *(int *)(&DAT_0049a154 + iVar3)) / 10000);
  return 1;
}
