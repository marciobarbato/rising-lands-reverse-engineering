/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00443108, entrada 00443108.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00443108(undefined4 param_1,byte param_2)

{
  ushort uVar1;
  bool bVar2;
  UnidadeParcial *pUVar3;
  ushort uVar4;
  uint in_EAX;
  uint uVar5;

  pUVar3 = tabela_unidades;
  switch(tabela_unidades[in_EAX & 0xffff].tipo_id) {
  case 0xb:
  case 0xc:
  case 0xd:
  case 0xe:
  case 0xf:
  case 0x10:
  case 0x11:
    bVar2 = true;
    break;
  default:
    bVar2 = false;
  }
  if (bVar2) {
    uVar5 = in_EAX & 0xffff;
    uVar1 = tabela_unidades[uVar5].campo_0a;
    for (uVar4 = 0; uVar4 < uVar1; uVar4 = uVar4 + 1) {
      if ((&pUVar3[uVar5].field_0x4c)[uVar4] == '\x01') {
        tabela_unidades[*(ushort *)(&pUVar3[uVar5].field_0x10 + (uint)uVar4 * 2)].proprietario_id =
             param_2;
      }
    }
    tabela_unidades[in_EAX & 0xffff].proprietario_id = param_2;
  }
  else {
    tabela_unidades[in_EAX & 0xffff].proprietario_id = param_2;
  }
  return;
}
