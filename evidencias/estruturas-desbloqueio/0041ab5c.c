/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall OriginaisSBL::BatimentCollision(undefined4 param_1,uint param_2)

{
  undefined1 in_AL;

  switch(in_AL) {
  case 0:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495c04)[param_2 & 0xffff]);
  case 1:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495c10)[param_2 & 0xffff]);
  case 2:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495c30)[param_2 & 0xffff]);
  case 3:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495c50)[param_2 & 0xffff]);
  case 4:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495cec)[param_2 & 0xffff]);
  case 5:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495c80)[param_2 & 0xffff]);
  case 6:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495d6c)[param_2 & 0xffff]);
  case 7:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495d30)[param_2 & 0xffff]);
  case 8:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495cf8)[param_2 & 0xffff]);
  case 9:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495d8a)[param_2 & 0xffff]);
  case 10:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495d64)[param_2 & 0xffff]);
  case 0xb:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495d5c)[param_2 & 0xffff]);
  case 0xc:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495d8b)[param_2 & 0xffff]);
  case 0xd:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495c6c)[param_2 & 0xffff]);
  case 0xe:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495ca4)[param_2 & 0xffff]);
  case 0xf:
  case 0x14:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495d1c)[param_2 & 0xffff]);
  case 0x10:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495cd4)[param_2 & 0xffff]);
  case 0x11:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495ce8)[param_2 & 0xffff]);
  case 0x12:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495d48)[param_2 & 0xffff]);
  case 0x13:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495cbc)[param_2 & 0xffff]);
  case 0x15:
    return CONCAT31((int3)((param_2 & 0xffff) >> 8),(&DAT_00495cc8)[param_2 & 0xffff]);
  default:
    return param_2 & 0xffffff00;
  }
}
