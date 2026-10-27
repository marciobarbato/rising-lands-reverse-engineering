/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044fe42, entrada 0044fe42.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_0044fe42(void)

{
  int iVar1;
  ushort in_AX;
  uint uVar2;
  ushort uVar3;
  UnidadeParcial *pUVar4;

  uVar2 = (uint)in_AX;
  pUVar4 = tabela_unidades + uVar2;
  iVar1 = (uint)pUVar4->proprietario_id * 10;
  if ((*(char *)((int)&DAT_004e19c4 + iVar1 + 1) != '\0') &&
     (*(byte *)(&DAT_004e19c4 + (uint)pUVar4->proprietario_id * 5) == pUVar4->tipo_id)) {
    pUVar4->field_0xaf = *(undefined1 *)((int)&DAT_004e19c4 + iVar1 + 1);
    FUN_0044f9e0(uVar2,(byte)tabela_unidades[uVar2].field_0xaf >> 5);
    for (uVar3 = 0; uVar2 = (uint)uVar3, uVar3 < 4; uVar3 = uVar3 + 1) {
      iVar1 = (uint)pUVar4->proprietario_id * 10 + uVar2 * 2;
      *(undefined1 *)((int)&DAT_004e19c4 + iVar1 + 1) =
           *(undefined1 *)((int)&DAT_004e19c6 + iVar1 + 1);
      *(undefined1 *)(&DAT_004e19c4 + uVar2 + (uint)pUVar4->proprietario_id * 5) =
           *(undefined1 *)(&DAT_004e19c6 + uVar2 + (uint)pUVar4->proprietario_id * 5);
    }
    (&DAT_004e19cd)[(uint)pUVar4->proprietario_id * 10] = 0;
    (&DAT_004e19cc)[(uint)pUVar4->proprietario_id * 10] = 0xff;
  }
  return;
}
