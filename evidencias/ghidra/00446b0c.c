/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00446b0c, entrada 00446b0c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_00446b0c(undefined4 param_1,short param_2)

{
  ulonglong uVar1;
  ushort in_AX;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  uint local_24;
  uint local_20;
  uint local_14;

  uVar2 = *(int *)&tabela_unidades[in_AX].field_0x83 >> 0x18;
  if ((uVar2 == 0) && (uVar2 = *(int *)&tabela_unidades[in_AX].field_0x84 >> 0x18, uVar2 == 0)) {
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
      local_20 = CONCAT22(local_20._2_2_,1);
      local_24 = 1;
      break;
    case 3:
    case 0xb:
    case 0xc:
    case 0xd:
    case 0xe:
    case 0xf:
    case 0x10:
    case 0x19:
      local_20 = CONCAT22(local_20._2_2_,2);
      local_24 = 2;
    }
    uVar4 = (uint)tabela_unidades[in_AX].celula_atual - ((local_24 - 1) * 0x100 + local_20 + -1);
    uVar2 = uVar4 & 0xffff;
    if (((ulonglong)uVar4 & 0xffffffff0000ffff) % 0x100 == 0) {
      local_20 = local_20 - 1;
    }
    else {
      uVar4 = uVar4 - 1;
    }
    if ((int)uVar2 >> 8 == 0) {
      local_24 = local_24 - 1;
    }
    else {
      uVar4 = uVar4 - 0x100;
    }
    uVar3 = uVar4 & 0xffff;
    uVar1 = (ulonglong)uVar4;
    local_14 = 0;
    uVar2 = 0xfe - local_20;
    while ((local_14 & 0xffff) < (local_24 & 0xffff) + 2) {
      if ((local_14 & 0xffff) + ((int)uVar3 >> 8) < 0x100) {
        for (uVar2 = 0; (uVar2 & 0xffff) < (local_20 & 0xffff) + 2; uVar2 = uVar2 + 1) {
          if (((uVar2 & 0xffff) + (int)((uVar1 & 0xffffffff0000ffff) % 0x100) < 0x100) &&
             ((short)uVar4 == param_2)) {
            return CONCAT31((int3)(uVar2 >> 8),1);
          }
          uVar4 = uVar4 + 1;
        }
      }
      uVar4 = uVar4 + (0xfe - local_20);
      uVar2 = local_14 + 1;
      local_14 = uVar2;
    }
  }
  return uVar2 & 0xffffff00;
}
