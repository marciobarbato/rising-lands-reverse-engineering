/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00441659, entrada 00441659.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00441659(void)

{
  UnidadeParcial *pUVar1;
  UnidadeParcial *pUVar2;
  uint uVar3;
  undefined2 *puVar4;
  uint uVar5;
  ushort uVar6;
  uint uVar7;

  for (uVar6 = 0; uVar6 < 4; uVar6 = uVar6 + 1) {
    for (uVar7 = 0; (uVar7 & 0xffff) < 0x1a; uVar7 = uVar7 + 1) {
      puVar4 = (undefined2 *)(*(int *)(DAT_004e19b8 + (uint)uVar6 * 4) + (uVar7 & 0xffff) * 0x68);
      *puVar4 = 0;
      puVar4[0x33] = 0;
      puVar4[2] = 0;
      puVar4[1] = 0;
      for (uVar5 = 0; uVar3 = uVar5 & 0xffff, uVar3 < 0x1e; uVar5 = uVar5 + 1) {
        puVar4[uVar3 + 3] = 0;
        *(undefined1 *)((int)puVar4 + uVar3 + 0x42) = 0;
      }
    }
  }
  for (uVar6 = 0; uVar6 < 800; uVar6 = uVar6 + 1) {
    if (tabela_unidades[uVar6].estado != 0) {
      tabela_unidades[uVar6].vida = 0;
      tabela_unidades[uVar6].estado = 0;
      tabela_unidades[uVar6].field_0xaf = 0;
      pUVar2 = tabela_unidades;
      pUVar1 = tabela_unidades + uVar6;
      *(undefined2 *)&tabela_unidades[uVar6].field_0x70 = 0;
      *(undefined2 *)&pUVar2[uVar6].field_0xe = 0;
      pUVar2[uVar6].campo_0c = 0;
      pUVar1->campo_0a = 0;
      for (uVar7 = 0; uVar5 = uVar7 & 0xffff, uVar5 < 0x1e; uVar7 = uVar7 + 1) {
        *(undefined2 *)(&pUVar2[uVar6].field_0x10 + uVar5 * 2) = 0;
        (&pUVar2[uVar6].field_0x4c)[uVar5] = 0;
      }
    }
  }
  return;
}
