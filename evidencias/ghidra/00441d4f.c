/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00441d4f, entrada 00441d4f.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00441d4f(void)

{
  ushort uVar1;
  bool bVar2;
  uint in_EAX;
  int iVar3;
  short sVar4;
  undefined4 extraout_ECX;

  iVar3 = (in_EAX & 0xff) * 8;
  if ((*(short *)(&DAT_004e1a14 + iVar3) != 0) &&
     (sVar4 = *(short *)(&DAT_004e1a14 + iVar3) + -1, *(short *)(&DAT_004e1a14 + iVar3) = sVar4,
     sVar4 == 0)) {
    uVar1 = *(ushort *)(&DAT_004e1a18 + iVar3);
    if ((tabela_unidades[uVar1].estado == 0) || (tabela_unidades[uVar1].estado == 4)) {
      bVar2 = false;
    }
    else {
      bVar2 = true;
    }
    if ((bVar2) && (tabela_unidades[uVar1].estado = 0x1e, uVar1 == DAT_00496304)) {
      DAT_004e0f36 = 0;
      DAT_004e0f37 = 0;
      DAT_004e0f3c = 0;
      DAT_00496304 = 0xffff;
    }
    FUN_004457d3();
    FUN_004829c8(extraout_ECX,0x44);
  }
  return;
}
