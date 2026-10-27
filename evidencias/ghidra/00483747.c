/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00483747, entrada 00483747.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_00483747(undefined4 param_1,int param_2)

{
  uint in_EAX;
  uint uVar1;
  uint uVar2;

  if (&DAT_0051a9e0 + param_2 * 8 != (undefined4 *)0x0) {
    for (uVar2 = CONCAT22((short)((uint)(&DAT_0051a9e0 + param_2 * 8) >> 0x10),
                          (&DAT_0051a9f0)[param_2 * 0x10]); uVar1 = uVar2 & 0xffff, uVar1 != 0xffff;
        uVar2 = CONCAT22((short)(uVar2 >> 0x10),*(undefined2 *)&tabela_unidades[uVar1].field_0x108))
    {
      if (tabela_unidades[uVar1].tipo_id == in_EAX) {
        return uVar2;
      }
    }
  }
  return 0xffff;
}
