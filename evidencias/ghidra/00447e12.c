/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00447e12, entrada 00447e12.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00447e12(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  UnidadeParcial *pUVar2;
  UnidadeParcial *pUVar3;
  char cVar4;
  uint in_EAX;
  undefined2 uVar5;
  uint uVar6;
  uint uVar7;
  uint uVar8;

  pUVar3 = tabela_unidades;
  uVar7 = in_EAX & 0xffff;
  bVar1 = tabela_unidades[uVar7].tipo_id;
  uVar5 = (undefined2)(in_EAX >> 0x10);
  if (bVar1 < 7) {
    if ((bVar1 == 6) && (tabela_unidades[uVar7].field_0x89 != '\0')) {
      if (tabela_unidades[uVar7].field_0x89 != '\x01') {
        return CONCAT44(param_2,in_EAX);
      }
      cVar4 = tabela_unidades[uVar7].field_0xa9 + '\x01';
      pUVar2 = tabela_unidades + uVar7;
      in_EAX = CONCAT22(uVar5,CONCAT11(pUVar2->field_0xa7,(char)in_EAX));
      tabela_unidades[uVar7].field_0xa9 = cVar4;
      if (cVar4 == pUVar2->field_0xa7) {
        uVar8 = (byte)pUVar3[uVar7].field_0xa4 + 1;
        uVar6 = 4;
        goto LAB_00447e79;
      }
    }
  }
  else if (bVar1 < 8) {
    if (tabela_unidades[uVar7].field_0x89 != '\0') {
      if (tabela_unidades[uVar7].field_0x89 != '\x01') {
        return CONCAT44(param_2,in_EAX);
      }
      cVar4 = tabela_unidades[uVar7].field_0xa9 + '\x01';
      pUVar2 = tabela_unidades + uVar7;
      tabela_unidades[uVar7].field_0xa9 = cVar4;
      if (cVar4 == pUVar2->field_0xa7) {
        uVar8 = (byte)pUVar3[uVar7].field_0xa4 + 1;
        uVar6 = (uint)(byte)pUVar3[uVar7].field_0xa5;
        goto LAB_00447e79;
      }
    }
  }
  else {
    if (bVar1 != 0xe) {
      return CONCAT44(param_2,in_EAX);
    }
    if (tabela_unidades[uVar7].field_0x89 != '\0') {
      if (tabela_unidades[uVar7].field_0x89 != '\x01') {
        return CONCAT44(param_2,in_EAX);
      }
      cVar4 = tabela_unidades[uVar7].field_0xa9 + '\x01';
      in_EAX = CONCAT22(uVar5,CONCAT11(cVar4,(char)in_EAX));
      pUVar2 = tabela_unidades + uVar7;
      tabela_unidades[uVar7].field_0xa9 = cVar4;
      if (cVar4 == pUVar2->field_0xa8) {
        uVar8 = (byte)pUVar3[uVar7].field_0xa4 + 1;
        uVar6 = (uint)(byte)pUVar3[uVar7].field_0xa6;
LAB_00447e79:
        pUVar3[uVar7].field_0xa9 = 0;
        pUVar3[uVar7].field_0xa4 = (char)(uVar8 % uVar6);
        return CONCAT44(param_2,uVar8 / uVar6);
      }
    }
  }
  return CONCAT44(param_2,in_EAX);
}
