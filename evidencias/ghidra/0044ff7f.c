/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044ff7f, entrada 0044ff7f.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0044ff7f(undefined4 param_1,byte param_2)

{
  UnidadeParcial *pUVar1;
  ushort in_AX;
  undefined4 extraout_ECX;
  int extraout_ECX_00;
  undefined8 uVar2;

  pUVar1 = tabela_unidades;
  FUN_00467d71((uint)param_2,param_2);
  uVar2 = FUN_0047474f(extraout_ECX,0);
  *(uint *)(&pUVar1[in_AX].field_0xe0 + extraout_ECX_00 * 4) =
       CONCAT22((short)((ulonglong)uVar2 >> 0x30),(short)uVar2);
  return;
}
