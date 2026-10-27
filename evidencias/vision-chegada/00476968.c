/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::IllumineCase(undefined4 param_1,byte param_2)

{
  byte *pbVar1;
  char cVar2;
  ushort in_AX;
  uint uVar3;
  uint extraout_ECX;
  uint uVar4;
  short local_14;

  uVar3 = CONCAT31((int3)((uint)param_1 >> 8),param_2);
  uVar4 = (uint)in_AX;
  if (*(char *)((&DAT_00507d98)[param_2] + uVar4) == '\0') {
    local_14 = (short)(uVar4 % 0x100);
    if (local_14 == 0) {
      *(byte *)(uVar4 + (&DAT_00507d88)[param_2]) =
           *(byte *)(uVar4 + (&DAT_00507d88)[param_2]) & 0xf7;
    }
    else {
      pbVar1 = (byte *)((uVar4 - 1) + (&DAT_00507d88)[param_2]);
      *pbVar1 = *pbVar1 & 0xfd;
    }
    if (uVar4 / 0x100 == 0) {
      *(byte *)((uint)in_AX + (&DAT_00507d88)[param_2]) =
           *(byte *)((uint)in_AX + (&DAT_00507d88)[param_2]) & 0xfb;
    }
    else {
      pbVar1 = (byte *)((in_AX - 0x100) + (&DAT_00507d88)[param_2]);
      *pbVar1 = *pbVar1 & 0xfe;
    }
    if (uVar4 % 0x100 == DAT_00497168 - 1) {
      *(byte *)((uint)in_AX + (&DAT_00507d88)[CONCAT31((int3)(DAT_00497168 - 1 >> 8),param_2)]) =
           *(byte *)((uint)in_AX + (&DAT_00507d88)[CONCAT31((int3)(DAT_00497168 - 1 >> 8),param_2)])
           & 0xfd;
    }
    else {
      pbVar1 = (byte *)(in_AX + 1 + (&DAT_00507d88)[param_2]);
      *pbVar1 = *pbVar1 & 0xf7;
    }
    if (uVar4 / 0x100 == DAT_0049716a - 1) {
      *(byte *)((uint)in_AX + (&DAT_00507d88)[param_2]) =
           *(byte *)((uint)in_AX + (&DAT_00507d88)[param_2]) & 0xfe;
    }
    else {
      pbVar1 = (byte *)(in_AX + 0x100 + (&DAT_00507d88)[param_2]);
      *pbVar1 = *pbVar1 & 0xfb;
    }
    *(byte *)((uint)in_AX + (&DAT_00507d88)[param_2]) =
         *(byte *)((uint)in_AX + (&DAT_00507d88)[param_2]) & 0xef;
    SetMiniMap(uVar3,2);
    uVar3 = extraout_ECX;
  }
  uVar3 = uVar3 & 0xff;
  if (uVar3 != 200) {
    cVar2 = *(char *)((&DAT_00507d98)[uVar3] + (uint)in_AX);
    if ((cVar2 != -1) && (uVar3 != 4)) {
      *(char *)((&DAT_00507d98)[uVar3] + (uint)in_AX) = cVar2 + '\x01';
    }
  }
  return;
}
