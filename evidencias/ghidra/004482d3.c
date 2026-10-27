/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004482d3, entrada 004482d3.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004482d3(undefined4 param_1,char param_2)

{
  byte bVar1;
  ushort in_AX;
  uint uVar2;
  uint extraout_ECX;
  int extraout_ECX_00;

  uVar2 = (uint)in_AX;
  tabela_unidades[uVar2].field_0xda = tabela_unidades[uVar2].field_0xda + param_2;
  bVar1 = tabela_unidades[uVar2].field_0xda;
  uVar2 = FUN_00428cc0(uVar2 * 0x114,0xc);
  if ((uVar2 & 0xffff) + 10 <= (uint)bVar1) {
    uVar2 = FUN_00428cc0(extraout_ECX,0xc);
    (&tabela_unidades->field_0xda)[extraout_ECX_00] = (char)uVar2 + '\n';
  }
  return;
}
