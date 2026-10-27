/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00428cc0, entrada 00428cc0.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_00428cc0(uint param_1,undefined1 param_2)

{
  uint in_EAX;
  uint uVar1;
  byte unaff_BL;

  uVar1 = in_EAX & 0xff;
  if ((uVar1 == 200) || (uVar1 == 4)) {
    return 0;
  }
  switch(param_2) {
  case 0:
    param_1 = CONCAT22((short)(uVar1 * 0x1d4 >> 0x10),
                       *(undefined2 *)(&DAT_004dfba0 + (uint)unaff_BL * 0x12 + uVar1 * 0x1d4));
    break;
  case 1:
    return CONCAT31((int3)(uVar1 * 0x1d4 >> 8),
                    (&DAT_004dfbab)[(uint)unaff_BL * 0x12 + uVar1 * 0x1d4]) & 0xffff00ff;
  case 2:
    return CONCAT31((int3)(uVar1 * 0x1d4 >> 8),
                    (&DAT_004dfba2)[(uint)unaff_BL * 0x12 + uVar1 * 0x1d4]) & 0xffff00ff;
  case 3:
    return CONCAT22((short)(uVar1 * 0x1d4 >> 0x10),
                    *(undefined2 *)(&DAT_004dfba4 + (uint)unaff_BL * 0x12 + uVar1 * 0x1d4));
  case 4:
    return CONCAT31((int3)(uVar1 * 0x1d4 >> 8),
                    (&DAT_004dfba6)[(uint)unaff_BL * 0x12 + uVar1 * 0x1d4]) & 0xffff00ff;
  case 5:
    return CONCAT22((short)(uVar1 * 0x1d4 >> 0x10),
                    *(undefined2 *)(&DAT_004dfba8 + (uint)unaff_BL * 0x12 + uVar1 * 0x1d4));
  case 6:
    return CONCAT31((int3)(uVar1 * 0x1d4 >> 8),
                    (&DAT_004dfbaa)[(uint)unaff_BL * 0x12 + uVar1 * 0x1d4]) & 0xffff00ff;
  case 7:
    return CONCAT31((int3)(uVar1 * 0x1d4 >> 8),
                    (&DAT_004dfbac)[(uint)unaff_BL * 0x12 + uVar1 * 0x1d4]) & 0xffff00ff;
  case 9:
    return CONCAT31((int3)(uVar1 * 0x1d4 >> 8),
                    (&DAT_004dfbae)[(uint)unaff_BL * 0x12 + uVar1 * 0x1d4]) & 0xffff00ff;
  case 10:
    return CONCAT31((int3)(uVar1 * 0x1d4 >> 8),
                    (&DAT_004dfbb1)[(uint)unaff_BL * 0x12 + uVar1 * 0x1d4]) & 0xffff00ff;
  case 0xb:
    return CONCAT31((int3)(uVar1 * 0x1d4 >> 8),
                    (&DAT_004dfbaf)[(uint)unaff_BL * 0x12 + uVar1 * 0x1d4]) & 0xffff00ff;
  case 0xc:
    return CONCAT31((int3)(uVar1 * 0x1d4 >> 8),
                    (&DAT_004dfbb0)[(uint)unaff_BL * 0x12 + uVar1 * 0x1d4]) & 0xffff00ff;
  }
  return param_1;
}
