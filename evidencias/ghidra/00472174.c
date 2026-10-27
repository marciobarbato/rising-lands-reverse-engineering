/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00472174, entrada 00472174.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall FUN_00472174(undefined4 param_1,uint param_2)

{
  byte in_AL;
  UnidadeParcial *pUVar1;
  uint3 uVar2;

  pUVar1 = tabela_unidades + (param_2 & 0xffff);
  uVar2 = (uint3)((uint)pUVar1 >> 8);
  if ((pUVar1->selecionada == 0) || (in_AL != pUVar1->proprietario_id)) {
    return (uint)uVar2 << 8;
  }
  return CONCAT31(uVar2,1);
}
