/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044f9e0, entrada 0044f9e0.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0044f9e0(undefined4 param_1,undefined1 param_2)

{
  byte bVar1;
  bool bVar2;
  ushort in_AX;
  uint uVar3;

  switch(param_2) {
  default:
    return;
  case 1:
    bVar1 = tabela_unidades[in_AX].tipo_id;
    if (bVar1 < 0xf) {
      if (((2 < bVar1) && (3 < bVar1)) &&
         ((bVar1 < 8 || ((8 < bVar1 && ((bVar1 < 0xb || (0xc < bVar1)))))))) goto LAB_0044fa4e;
LAB_0044fa36:
      bVar2 = true;
    }
    else {
      if (bVar1 < 0x10) goto LAB_0044fa36;
      if (bVar1 < 0x14) {
        if ((bVar1 < 0x11) || (0x11 < bVar1)) goto LAB_0044fa36;
      }
      else if ((bVar1 < 0x17) || ((bVar1 < 0x19 || (bVar1 == 0x19)))) goto LAB_0044fa36;
LAB_0044fa4e:
      bVar2 = false;
    }
    if (bVar2) {
      tabela_unidades[in_AX].field_0xf7 = 1;
      return;
    }
    break;
  case 2:
    tabela_unidades[in_AX].field_0xf6 = 1;
    return;
  case 3:
    tabela_unidades[in_AX].field_0xf5 = 1;
    return;
  case 4:
    bVar1 = tabela_unidades[in_AX].tipo_id;
    if (bVar1 < 0xf) {
      if (((2 < bVar1) && (3 < bVar1)) &&
         ((bVar1 < 8 || ((8 < bVar1 && ((bVar1 < 0xb || (0xc < bVar1)))))))) goto LAB_0044fadd;
LAB_0044fac5:
      bVar2 = true;
    }
    else {
      if (bVar1 < 0x10) goto LAB_0044fac5;
      if (bVar1 < 0x14) {
        if ((bVar1 < 0x11) || (0x11 < bVar1)) goto LAB_0044fac5;
      }
      else if ((bVar1 < 0x17) || ((bVar1 < 0x19 || (bVar1 == 0x19)))) goto LAB_0044fac5;
LAB_0044fadd:
      bVar2 = false;
    }
    if (!bVar2) {
      uVar3 = (uint)*(ushort *)(&DAT_004965dc + (uint)tabela_unidades[in_AX].tipo_id * 0x32) * 2;
      goto LAB_0044fa79;
    }
  }
  uVar3 = (uint)*(ushort *)(&DAT_004965dc + (uint)tabela_unidades[in_AX].tipo_id * 0x32);
LAB_0044fa79:
  tabela_unidades[in_AX].field_0xf8 = (char)(uVar3 / 100);
  return;
}
