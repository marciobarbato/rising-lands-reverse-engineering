/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::DecouvreCase(undefined4 param_1,byte param_2)

{
  byte *pbVar1;
  ushort in_AX;
  uint uVar2;
  uint extraout_ECX;
  uint uVar3;

  uVar2 = CONCAT31((int3)((uint)param_1 >> 8),param_2);
  uVar3 = (uint)in_AX;
  if (uVar3 % 0x100 == 0) {
    *(byte *)(uVar3 + (&DAT_00507d78)[param_2]) = *(byte *)(uVar3 + (&DAT_00507d78)[param_2]) & 0xf7
    ;
  }
  else {
    pbVar1 = (byte *)((uVar3 - 1) + (&DAT_00507d78)[param_2]);
    *pbVar1 = *pbVar1 & 0xfd;
  }
  if ((int)uVar3 >> 8 == 0) {
    *(byte *)((uint)in_AX + (&DAT_00507d78)[param_2]) =
         *(byte *)((uint)in_AX + (&DAT_00507d78)[param_2]) & 0xfb;
  }
  else {
    pbVar1 = (byte *)((in_AX - 0x100) + (&DAT_00507d78)[param_2]);
    *pbVar1 = *pbVar1 & 0xfe;
  }
  if (uVar3 % 0x100 == DAT_00497168 - 1) {
    *(byte *)((uint)in_AX + (&DAT_00507d78)[param_2]) =
         *(byte *)((uint)in_AX + (&DAT_00507d78)[param_2]) & 0xfd;
  }
  else {
    pbVar1 = (byte *)(in_AX + 1 + (&DAT_00507d78)[param_2]);
    *pbVar1 = *pbVar1 & 0xf7;
  }
  if ((int)uVar3 >> 8 == DAT_0049716a - 1) {
    *(byte *)((uint)in_AX + (&DAT_00507d78)[param_2]) =
         *(byte *)((uint)in_AX + (&DAT_00507d78)[param_2]) & 0xfe;
  }
  else {
    pbVar1 = (byte *)(in_AX + 0x100 + (&DAT_00507d78)[param_2]);
    *pbVar1 = *pbVar1 & 0xfb;
  }
  if (*(char *)((&DAT_00507d78)[param_2] + (uint)in_AX) != '\0') {
    SetMiniMap(uVar2,1);
    uVar2 = extraout_ECX;
  }
  *(byte *)((uint)in_AX + (&DAT_00507d78)[uVar2 & 0xff]) =
       *(byte *)((uint)in_AX + (&DAT_00507d78)[uVar2 & 0xff]) & 0xef;
  return;
}
