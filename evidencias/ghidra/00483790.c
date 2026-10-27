/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00483790, entrada 00483790.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_00483790(undefined4 param_1,uint param_2)

{
  int iVar1;
  int in_EAX;
  uint uVar2;
  uint uVar3;

  iVar1 = (&DAT_0051b664)[in_EAX * 0x18];
  if (iVar1 != -1) {
    if (&DAT_0051a9e0 + iVar1 * 8 != (undefined4 *)0x0) {
      for (uVar3 = CONCAT22((short)((uint)(&DAT_0051a9e0 + iVar1 * 8) >> 0x10),
                            (&DAT_0051a9f0)[iVar1 * 0x10]); uVar2 = uVar3 & 0xffff, uVar2 != 0xffff;
          uVar3 = CONCAT22((short)(uVar3 >> 0x10),*(undefined2 *)&tabela_unidades[uVar2].field_0x108
                          )) {
        if (tabela_unidades[uVar2].tipo_id == param_2) {
          return uVar3;
        }
      }
    }
  }
  return 0xffff;
}
