/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00448088, entrada 00448088.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00448088(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  UnidadeParcial *pUVar2;
  UnidadeParcial *pUVar3;
  ushort in_AX;
  char cVar5;
  undefined4 uVar4;
  uint uVar6;
  uint uVar7;

  pUVar3 = tabela_unidades;
  uVar6 = (uint)in_AX;
  bVar1 = tabela_unidades[uVar6].tipo_id;
  uVar4 = CONCAT31((int3)(uVar6 * 0x114 >> 8),bVar1);
  if ((10 < bVar1) && (0xb < bVar1)) {
    if (bVar1 < 0x12) {
      if ((0xd < bVar1) && (0xf < bVar1)) {
        if (bVar1 == 0x11) {
          uVar4 = FUN_00447b2f();
          return CONCAT44(param_2,uVar4);
        }
        return CONCAT44(param_2,uVar4);
      }
    }
    else if ((((0x12 < bVar1) && (0x16 < bVar1)) && (0x18 < bVar1)) && (bVar1 != 0x19)) {
      return CONCAT44(param_2,uVar4);
    }
  }
  cVar5 = tabela_unidades[uVar6].field_0xa9 + '\x01';
  pUVar2 = tabela_unidades + uVar6;
  tabela_unidades[uVar6].field_0xa9 = cVar5;
  if (cVar5 == pUVar2->field_0xa7) {
    uVar7 = (byte)pUVar3[uVar6].field_0xa4 + 1;
    pUVar3[uVar6].field_0xa9 = 0;
    pUVar3[uVar6].field_0xa4 = (char)(uVar7 % (uint)(byte)pUVar3[uVar6].field_0xa5);
    return CONCAT44(param_2,uVar7 / (byte)pUVar3[uVar6].field_0xa5);
  }
  return CONCAT44(param_2,CONCAT22((short)(uVar6 * 0x114 >> 0x10),CONCAT11(cVar5,bVar1)));
}
