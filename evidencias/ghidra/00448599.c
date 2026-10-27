/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00448599, entrada 00448599.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00448599(undefined4 param_1,undefined4 param_2)

{
  bool bVar1;
  UnidadeParcial *pUVar2;
  uint in_EAX;
  undefined3 uVar4;
  uint uVar3;
  byte bVar5;
  uint uVar6;

  pUVar2 = tabela_unidades;
  uVar6 = in_EAX & 0xffff;
  bVar5 = tabela_unidades[uVar6].tipo_id;
  uVar4 = (undefined3)(in_EAX >> 8);
  if ((bVar5 < 0xc) || ((0xc < bVar5 && (bVar5 != 0xf)))) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  if (bVar1) {
    tabela_unidades[uVar6].field_0xda =
         (tabela_unidades[uVar6].direcao_desejada - 1) * '\x02' + '\x01';
  }
  uVar3 = CONCAT31(uVar4,pUVar2[uVar6].direcao_desejada);
  if ((pUVar2[uVar6].direcao_desejada == pUVar2[uVar6].orientacao_atual) ||
     (bVar5 = pUVar2[uVar6].contador_giro + 1, pUVar2[uVar6].contador_giro = bVar5,
     bVar5 != pUVar2[uVar6].periodo_giro)) goto LAB_00448695;
  if ((pUVar2[uVar6].orientacao_atual < pUVar2[uVar6].direcao_desejada) &&
     ((int)((uint)pUVar2[uVar6].direcao_desejada - (uint)pUVar2[uVar6].orientacao_atual) < 8)) {
LAB_00448655:
    uVar3 = pUVar2[uVar6].orientacao_atual / 0x10;
    bVar5 = pUVar2[uVar6].orientacao_atual % 0x10 + 1;
  }
  else {
    bVar5 = pUVar2[uVar6].orientacao_atual;
    uVar3 = CONCAT31(uVar4,bVar5);
    if ((pUVar2[uVar6].direcao_desejada < bVar5) &&
       (8 < (int)((uint)bVar5 - (uint)pUVar2[uVar6].direcao_desejada))) goto LAB_00448655;
    if (pUVar2[uVar6].orientacao_atual == 1) {
      bVar5 = 0x10;
    }
    else {
      bVar5 = pUVar2[uVar6].orientacao_atual - 1;
    }
  }
  pUVar2[uVar6].orientacao_atual = bVar5;
  pUVar2[uVar6].contador_giro = 0;
LAB_00448695:
  return CONCAT44(param_2,uVar3);
}
