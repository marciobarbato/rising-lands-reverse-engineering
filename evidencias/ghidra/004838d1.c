/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004838d1, entrada 004838d1.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined4 __fastcall FUN_004838d1(undefined4 param_1,uint param_2)

{
  byte bVar1;
  UnidadeParcial *pUVar2;
  ushort in_AX;
  int extraout_ECX;
  int iVar3;
  int iVar4;

  pUVar2 = tabela_unidades;
  bVar1 = tabela_unidades[in_AX].proprietario_id;
  iVar3 = -1;
  iVar4 = (&DAT_0051b6b4)[(uint)bVar1 * 0x18];
  while( true ) {
    if (iVar4 == -1) {
      if ((param_2 & 0x7ffffff) != 0x7fd72b1) {
        *(undefined2 *)&tabela_unidades[in_AX].field_0x108 = (&DAT_0051a9f0)[param_2 * 0x10];
        *(uint *)&pUVar2[in_AX].field_0x10c = param_2;
        (&DAT_0051a9f0)[param_2 * 0x10] = in_AX;
        (&DAT_0051a9f2)[param_2 * 0x10] = (&DAT_0051a9f2)[param_2 * 0x10] + 1;
      }
      return 0x1a1a0016;
    }
    if ((&DAT_0051a9fa)[iVar4 * 0x20] == tabela_unidades[in_AX].tipo_id) break;
    iVar3 = iVar4;
    iVar4 = (&DAT_0051a9e4)[iVar4 * 8];
  }
  if (iVar4 * 0x20 != -0x51a9e0) {
    *(undefined2 *)&tabela_unidades[in_AX].field_0x108 = (&DAT_0051a9f0)[iVar4 * 0x10];
    *(int *)&pUVar2[in_AX].field_0x10c = iVar4;
    (&DAT_0051a9f0)[iVar4 * 0x10] = in_AX;
    (&DAT_0051a9f2)[iVar4 * 0x10] = (&DAT_0051a9f2)[iVar4 * 0x10] + 1;
  }
  if ((&DAT_0051a9e8)[iVar4 * 8] != -1) {
    FUN_0047da54(iVar3,1);
    iVar3 = extraout_ECX;
  }
  if (iVar3 == -1) {
    (&DAT_0051b6b4)[(uint)bVar1 * 0x18] = (&DAT_0051a9e4)[iVar4 * 8];
  }
  else {
    (&DAT_0051a9e4)[iVar3 * 8] = (&DAT_0051a9e4)[iVar4 * 8];
  }
  (&DAT_0051a9fa)[iVar4 * 0x20] = 0xff;
  return 0x1a1a0017;
}
