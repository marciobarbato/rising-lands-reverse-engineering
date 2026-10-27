/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00447e12, entrada 00447e12.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00447e12(undefined4 param_1,undefined4 param_2)

{
  UnidadeParcial *pUVar1;
  UnidadeParcial *pUVar2;
  byte bVar3;
  uint in_EAX;
  undefined2 uVar4;
  uint uVar5;
  uint uVar6;
  uint uVar7;

  pUVar2 = tabela_unidades;
  uVar6 = in_EAX & 0xffff;
  bVar3 = tabela_unidades[uVar6].tipo_id;
  uVar4 = (undefined2)(in_EAX >> 0x10);
  if (bVar3 < 7) {
    if ((bVar3 == 6) && (tabela_unidades[uVar6].field_0x89 != '\0')) {
      if (tabela_unidades[uVar6].field_0x89 != '\x01') {
        return CONCAT44(param_2,in_EAX);
      }
      bVar3 = tabela_unidades[uVar6].contador_animacao + 1;
      pUVar1 = tabela_unidades + uVar6;
      in_EAX = CONCAT22(uVar4,CONCAT11(pUVar1->periodo_animacao,(char)in_EAX));
      tabela_unidades[uVar6].contador_animacao = bVar3;
      if (bVar3 == pUVar1->periodo_animacao) {
        uVar7 = pUVar2[uVar6].quadro_movimento + 1;
        uVar5 = 4;
        goto LAB_00447e79;
      }
    }
  }
  else if (bVar3 < 8) {
    if (tabela_unidades[uVar6].field_0x89 != '\0') {
      if (tabela_unidades[uVar6].field_0x89 != '\x01') {
        return CONCAT44(param_2,in_EAX);
      }
      bVar3 = tabela_unidades[uVar6].contador_animacao + 1;
      pUVar1 = tabela_unidades + uVar6;
      tabela_unidades[uVar6].contador_animacao = bVar3;
      if (bVar3 == pUVar1->periodo_animacao) {
        uVar7 = pUVar2[uVar6].quadro_movimento + 1;
        uVar5 = (uint)pUVar2[uVar6].quantidade_quadros_movimento;
        goto LAB_00447e79;
      }
    }
  }
  else {
    if (bVar3 != 0xe) {
      return CONCAT44(param_2,in_EAX);
    }
    if (tabela_unidades[uVar6].field_0x89 != '\0') {
      if (tabela_unidades[uVar6].field_0x89 != '\x01') {
        return CONCAT44(param_2,in_EAX);
      }
      bVar3 = tabela_unidades[uVar6].contador_animacao + 1;
      in_EAX = CONCAT22(uVar4,CONCAT11(bVar3,(char)in_EAX));
      pUVar1 = tabela_unidades + uVar6;
      tabela_unidades[uVar6].contador_animacao = bVar3;
      if (bVar3 == pUVar1->field_0xa8) {
        uVar7 = pUVar2[uVar6].quadro_movimento + 1;
        uVar5 = (uint)(byte)pUVar2[uVar6].field_0xa6;
LAB_00447e79:
        pUVar2[uVar6].contador_animacao = 0;
        pUVar2[uVar6].quadro_movimento = (byte)(uVar7 % uVar5);
        return CONCAT44(param_2,uVar7 / uVar5);
      }
    }
  }
  return CONCAT44(param_2,in_EAX);
}
