/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004571d4, entrada 004571d4.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_004571d4(void)

{
  UnidadeParcial *pUVar1;
  ushort in_AX;
  uint uVar2;
  uint uVar3;

  pUVar1 = tabela_unidades;
  tabela_unidades[in_AX].tipo_id = 9;
  pUVar1[in_AX].field_0x93 = 1;
  pUVar1[in_AX].field_0x98 = 2;
  pUVar1[in_AX].field_0xa7 = 2;
  pUVar1[in_AX].field_0xa8 = 4;
  pUVar1[in_AX].field_0xa5 = 8;
  pUVar1[in_AX].field_0x9d = 0xff;
  pUVar1[in_AX].field_0xac = 3;
  pUVar1[in_AX].field_0xad = 3;
  pUVar1[in_AX].field_0x99 = 0;
  pUVar1[in_AX].raio_visao = 5;
  pUVar1[in_AX].campo_0a = 0;
  *(undefined2 *)&pUVar1[in_AX].field_0x70 = 0;
  *(undefined2 *)&pUVar1[in_AX].field_0xe = 0;
  pUVar1[in_AX].campo_0c = 0;
  for (uVar3 = 0; uVar2 = uVar3 & 0xffff, uVar2 < 0x1e; uVar3 = uVar3 + 1) {
    *(undefined2 *)(&pUVar1[in_AX].field_0x10 + uVar2 * 2) = 0;
    (&pUVar1[in_AX].field_0x4c)[uVar2] = 0;
  }
  pUVar1[in_AX].campo_0c = 0;
  if (*(ushort *)(&DAT_004965b6 + (uint)tabela_unidades[in_AX].tipo_id * 0x32) < pUVar1[in_AX].vida)
  {
    pUVar1[in_AX].vida = *(ushort *)(&DAT_004965b6 + (uint)tabela_unidades[in_AX].tipo_id * 0x32);
  }
  return;
}
