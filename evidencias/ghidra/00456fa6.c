/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00456fa6, entrada 00456fa6.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00456fa6(void)

{
  uint in_EAX;
  int extraout_ECX;
  int extraout_ECX_00;
  UnidadeParcial *extraout_ECX_01;
  UnidadeParcial *pUVar1;

  FUN_00442cb4(tabela_unidades);
  *(undefined1 *)(extraout_ECX + 0x72 + (in_EAX & 0xffff) * 0x114) = 1;
  pUVar1 = tabela_unidades + (in_EAX & 0xffff);
  if ((pUVar1->proprietario_id != 200) && (pUVar1->proprietario_id != 4)) {
    FUN_00476851(pUVar1,(uint)(ushort)((ushort)(byte)pUVar1->field_0xf5 + pUVar1->raio_visao + 2));
    FUN_00476cb3(extraout_ECX_00,
                 (uint)(ushort)((ushort)*(byte *)(extraout_ECX_00 + 0xbb) +
                               (ushort)*(byte *)(extraout_ECX_00 + 0xf5)));
    pUVar1 = extraout_ECX_01;
  }
  FUN_0046a388(pUVar1,4);
  return;
}
