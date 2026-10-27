/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00448599, entrada 00448599.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00448599(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  bool bVar2;
  UnidadeParcial *pUVar3;
  uint in_EAX;
  undefined3 uVar5;
  uint uVar4;
  char cVar6;
  uint uVar7;

  pUVar3 = tabela_unidades;
  uVar7 = in_EAX & 0xffff;
  bVar1 = tabela_unidades[uVar7].tipo_id;
  uVar5 = (undefined3)(in_EAX >> 8);
  if ((bVar1 < 0xc) || ((0xc < bVar1 && (bVar1 != 0xf)))) {
    bVar2 = false;
  }
  else {
    bVar2 = true;
  }
  if (bVar2) {
    tabela_unidades[uVar7].field_0xda = (tabela_unidades[uVar7].field_0x90 + -1) * '\x02' + '\x01';
  }
  uVar4 = CONCAT31(uVar5,pUVar3[uVar7].field_0x90);
  if ((pUVar3[uVar7].field_0x90 == pUVar3[uVar7].field_0x91) ||
     (cVar6 = pUVar3[uVar7].field_0x92 + '\x01', pUVar3[uVar7].field_0x92 = cVar6,
     cVar6 != pUVar3[uVar7].field_0x93)) goto LAB_00448695;
  if (((byte)pUVar3[uVar7].field_0x91 < (byte)pUVar3[uVar7].field_0x90) &&
     ((int)((uint)(byte)pUVar3[uVar7].field_0x90 - (uint)(byte)pUVar3[uVar7].field_0x91) < 8)) {
LAB_00448655:
    uVar4 = (byte)pUVar3[uVar7].field_0x91 / 0x10;
    cVar6 = (byte)pUVar3[uVar7].field_0x91 % 0x10 + 1;
  }
  else {
    bVar1 = pUVar3[uVar7].field_0x91;
    uVar4 = CONCAT31(uVar5,bVar1);
    if (((byte)pUVar3[uVar7].field_0x90 < bVar1) &&
       (8 < (int)((uint)bVar1 - (uint)(byte)pUVar3[uVar7].field_0x90))) goto LAB_00448655;
    if (pUVar3[uVar7].field_0x91 == '\x01') {
      cVar6 = '\x10';
    }
    else {
      cVar6 = pUVar3[uVar7].field_0x91 + -1;
    }
  }
  pUVar3[uVar7].field_0x91 = cVar6;
  pUVar3[uVar7].field_0x92 = 0;
LAB_00448695:
  return CONCAT44(param_2,uVar4);
}
