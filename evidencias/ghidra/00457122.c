/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00457122, entrada 00457122.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall FUN_00457122(undefined4 param_1,short param_2)

{
  ushort uVar1;
  UnidadeParcial *pUVar2;
  ushort in_AX;
  uint3 uVar3;
  ushort uVar4;

  pUVar2 = tabela_unidades;
  uVar4 = tabela_unidades[in_AX].vida + param_2;
  tabela_unidades[in_AX].vida = uVar4;
  uVar1 = *(ushort *)(&DAT_004965b6 + (uint)tabela_unidades[in_AX].tipo_id * 0x32);
  uVar3 = (uint3)(byte)(uVar1 >> 8);
  if (uVar1 < uVar4) {
    pUVar2[in_AX].vida = uVar1;
    return CONCAT31(uVar3,1);
  }
  return (uint)uVar3 << 8;
}
