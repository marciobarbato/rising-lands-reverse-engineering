/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00482939, entrada 00482939.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined4 __fastcall FUN_00482939(undefined4 param_1,ushort param_2)

{
  UnidadeParcial *pUVar1;
  uint in_EAX;
  undefined4 uVar2;

  pUVar1 = tabela_unidades;
  if ((in_EAX & 0x7ffffff) == 0x7fd72b1) {
    uVar2 = 0x1a1a0010;
  }
  else {
    *(undefined2 *)&tabela_unidades[param_2].field_0x108 = (&DAT_0051a9f0)[in_EAX * 0x10];
    *(uint *)&pUVar1[param_2].field_0x10c = in_EAX;
    (&DAT_0051a9f0)[in_EAX * 0x10] = param_2;
    uVar2 = 0;
    (&DAT_0051a9f2)[in_EAX * 0x10] = (&DAT_0051a9f2)[in_EAX * 0x10] + 1;
  }
  return uVar2;
}
