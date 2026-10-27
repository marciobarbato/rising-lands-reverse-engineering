/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00457058, entrada 00457058.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00457058(void)

{
  ushort in_AX;
  int extraout_ECX;
  int extraout_ECX_00;
  int iVar1;
  char *extraout_ECX_01;

  FUN_00472648(tabela_unidades + in_AX);
  FUN_00442eac();
  iVar1 = extraout_ECX;
  if (*(short *)(extraout_ECX + 8) != *(short *)(extraout_ECX + 0x7c)) {
    FUN_00442eac();
    iVar1 = extraout_ECX_00;
  }
  *(undefined1 *)(iVar1 + 0x72) = 0;
  FUN_0046a388(iVar1,5);
  if ((*extraout_ECX_01 != -0x38) && (*extraout_ECX_01 != '\x04')) {
    FUN_00476e82(extraout_ECX_01,
                 (uint)(ushort)((ushort)(byte)extraout_ECX_01[0xbb] +
                               (ushort)(byte)extraout_ECX_01[0xf5]));
  }
  return;
}
