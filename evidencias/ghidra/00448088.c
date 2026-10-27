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
  byte bVar5;
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
  bVar5 = tabela_unidades[uVar6].contador_animacao + 1;
  pUVar2 = tabela_unidades + uVar6;
  tabela_unidades[uVar6].contador_animacao = bVar5;
  if (bVar5 == pUVar2->periodo_animacao) {
    uVar7 = pUVar3[uVar6].quadro_movimento + 1;
    pUVar3[uVar6].contador_animacao = 0;
    pUVar3[uVar6].quadro_movimento =
         (byte)(uVar7 % (uint)pUVar3[uVar6].quantidade_quadros_movimento);
    return CONCAT44(param_2,uVar7 / pUVar3[uVar6].quantidade_quadros_movimento);
  }
  return CONCAT44(param_2,CONCAT22((short)(uVar6 * 0x114 >> 0x10),CONCAT11(bVar5,bVar1)));
}
