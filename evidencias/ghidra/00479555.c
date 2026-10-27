/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00479555, entrada 00479555.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall FUN_00479555(ushort param_1,ushort param_2)

{
  ushort in_AX;
  int iVar1;
  ushort unaff_BX;

  if (unaff_BX < in_AX) {
    iVar1 = ((uint)in_AX - (uint)unaff_BX) * ((uint)in_AX - (uint)unaff_BX);
  }
  else {
    iVar1 = ((uint)unaff_BX - (uint)in_AX) * ((uint)unaff_BX - (uint)in_AX);
  }
  if (param_1 < param_2) {
    return iVar1 + ((uint)param_2 - (uint)param_1) * ((uint)param_2 - (uint)param_1);
  }
  return iVar1 + ((uint)param_1 - (uint)param_2) * ((uint)param_1 - (uint)param_2);
}
