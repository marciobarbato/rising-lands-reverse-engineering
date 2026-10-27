/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044106c, entrada 0044106c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0044106c(undefined4 param_1,undefined2 *param_2)

{
  ushort in_AX;
  undefined2 *unaff_EBX;

  switch(tabela_unidades[in_AX].tipo_id) {
  case 0:
  case 1:
  case 2:
  case 4:
  case 5:
  case 6:
  case 7:
  case 8:
  case 9:
  case 10:
  case 0x11:
  case 0x12:
  case 0x13:
  case 0x14:
  case 0x15:
  case 0x16:
  case 0x17:
  case 0x18:
    *param_2 = 1;
    *unaff_EBX = 1;
    return;
  case 3:
  case 0xb:
  case 0xc:
  case 0xd:
  case 0xe:
  case 0xf:
  case 0x10:
  case 0x19:
    *param_2 = 2;
    *unaff_EBX = 2;
    return;
  default:
    return;
  }
}
