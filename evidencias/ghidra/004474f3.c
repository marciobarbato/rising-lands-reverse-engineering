/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004474f3, entrada 004474f3.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_004474f3(undefined4 param_1,undefined4 param_2)

{
  ushort uVar1;
  ushort in_AX;

  uVar1._0_1_ = tabela_unidades[in_AX].proprietario_id;
  uVar1._1_1_ = tabela_unidades[in_AX].tipo_id;
  return CONCAT44(param_2,(uint)(byte)uVar1._1_1_ * 0x68 +
                          *(int *)(DAT_004e19b8 + (uVar1 & 0xff) * 4));
}
