/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004832b1, entrada 004832b1.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined4 __fastcall FUN_004832b1(undefined4 param_1,ushort param_2)

{
  ushort uVar1;
  ushort uVar2;
  uint in_EAX;
  uint uVar3;
  ushort uVar4;

  if ((in_EAX & 0x7ffffff) == 0x7fd72b1) {
    return 0x1a1a0010;
  }
  uVar1 = (&DAT_0051a9f0)[in_EAX * 0x10];
  uVar4 = 0xffff;
  while( true ) {
    uVar2 = uVar1;
    uVar3 = (uint)uVar2;
    if (uVar3 == 0xffff) {
      return 0x1a1a0012;
    }
    if (uVar2 == param_2) break;
    uVar1 = *(ushort *)&tabela_unidades[uVar3].field_0x108;
    uVar4 = uVar2;
  }
  if (uVar4 == 0xffff) {
    (&DAT_0051a9f0)[in_EAX * 0x10] = *(undefined2 *)&tabela_unidades[uVar3].field_0x108;
  }
  else {
    *(undefined2 *)&tabela_unidades[uVar4].field_0x108 =
         *(undefined2 *)&tabela_unidades[uVar3].field_0x108;
  }
  (&DAT_0051a9f2)[in_EAX * 0x10] = (&DAT_0051a9f2)[in_EAX * 0x10] + -1;
  return 0;
}
