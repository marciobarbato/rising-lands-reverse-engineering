/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall OriginaisSBL::iagUnitGetNextUnitInGroup(undefined4 param_1,undefined4 param_2)

{
  uint uVar1;

  uVar1 = (uint)DAT_0051b848;
  DAT_0051b848 = *(ushort *)&tabela_unidades[uVar1].field_0x108;
  uVar1 = (uint)*(ushort *)&tabela_unidades[uVar1].field_0x108;
  if (uVar1 == 0xffff) {
    uVar1 = 0xffff;
  }
  return CONCAT44(param_2,uVar1);
}
