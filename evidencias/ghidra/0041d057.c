/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0041d057, entrada 0041d057.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall FUN_0041d057(undefined4 param_1)

{
  byte bVar1;
  ushort in_AX;
  int iVar2;
  uint uVar3;
  ushort in_DX;
  int extraout_EDX;
  int extraout_EDX_00;

  iVar2 = (uint)in_AX * 0x114;
  bVar1 = (&DAT_0049a0d0)[iVar2];
  if (7 < bVar1) {
    if (bVar1 < 9) {
      bVar1 = unidade_obter_tipo(in_DX);
      uVar3 = (uint)bVar1;
      iVar2 = extraout_EDX;
      if (uVar3 != 3) {
        unidade_obter_tipo(in_DX);
        uVar3 = FUN_00442434();
        iVar2 = extraout_EDX_00;
        if ((char)uVar3 == '\0') {
          return CONCAT22((short)(uVar3 >> 0x10),*(undefined2 *)(extraout_EDX_00 + 2)) + 0x303;
        }
      }
      return CONCAT22((short)(uVar3 >> 0x10),*(undefined2 *)(iVar2 + 2)) + 0x403;
    }
    if (bVar1 == 0xe) {
      return CONCAT22((short)((uint)iVar2 >> 0x10),*(undefined2 *)(&DAT_0049a0ca + iVar2)) + 0x402;
    }
  }
  return 0;
}
