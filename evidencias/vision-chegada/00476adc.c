/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::EteintCase(undefined4 param_1,byte param_2)

{
  byte *pbVar1;
  char cVar2;
  ulonglong uVar3;
  uint in_EAX;
  char *pcVar4;
  uint extraout_ECX;
  uint uVar5;

  uVar5 = in_EAX & 0xffff;
  uVar3 = ((ulonglong)in_EAX & 0xffffffff0000ffff) % 0x100;
  if (*(char *)((&DAT_00507d98)[param_2] + uVar5) == '\x01') {
    if (uVar3 == 0) {
      *(byte *)(uVar5 + (&DAT_00507d88)[param_2]) = *(byte *)(uVar5 + (&DAT_00507d88)[param_2]) | 8;
    }
    else {
      pbVar1 = (byte *)((uVar5 - 1) + (&DAT_00507d88)[param_2]);
      *pbVar1 = *pbVar1 | 2;
    }
    if ((int)uVar5 >> 8 == 0) {
      pbVar1 = (byte *)((in_EAX & 0xffff) + (&DAT_00507d88)[param_2]);
      *pbVar1 = *pbVar1 | 4;
    }
    else {
      pbVar1 = (byte *)(((in_EAX & 0xffff) - 0x100) + (&DAT_00507d88)[param_2]);
      *pbVar1 = *pbVar1 | 1;
    }
    if ((uint)(ushort)uVar3 == DAT_00497168 - 1) {
      pbVar1 = (byte *)((in_EAX & 0xffff) + (&DAT_00507d88)[param_2]);
      *pbVar1 = *pbVar1 | 2;
    }
    else {
      pbVar1 = (byte *)((in_EAX & 0xffff) + 1 + (&DAT_00507d88)[param_2]);
      *pbVar1 = *pbVar1 | 8;
    }
    if (uVar5 >> 8 == DAT_0049716a - 1) {
      pbVar1 = (byte *)((in_EAX & 0xffff) +
                       (&DAT_00507d88)[CONCAT31((int3)(DAT_0049716a - 1 >> 8),param_2)]);
      *pbVar1 = *pbVar1 | 1;
    }
    else {
      pbVar1 = (byte *)((in_EAX & 0xffff) + 0x100 + (&DAT_00507d88)[param_2]);
      *pbVar1 = *pbVar1 | 4;
    }
    pbVar1 = (byte *)((in_EAX & 0xffff) + (&DAT_00507d88)[param_2]);
    *pbVar1 = *pbVar1 | 0x10;
    SetMiniMap(in_EAX,3);
    in_EAX = extraout_ECX;
  }
  uVar5 = (uint)param_2;
  if (uVar5 != 200) {
    pcVar4 = (char *)((&DAT_00507d98)[uVar5] + (in_EAX & 0xffff));
    cVar2 = *pcVar4;
    if ((cVar2 != '\0') && (uVar5 != 4)) {
      *pcVar4 = cVar2 + -1;
    }
  }
  return;
}
