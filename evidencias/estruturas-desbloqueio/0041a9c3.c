/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::GetBatimentCaseList(undefined4 param_1,short *param_2)

{
  short sVar1;
  ushort uVar2;
  ushort in_AX;
  ushort uVar3;
  short sVar4;
  short *unaff_EBX;

  *unaff_EBX = 0;
  sVar1 = *(short *)(&DAT_0049a0ca + (uint)in_AX * 0x114);
  uVar2 = *(ushort *)(&DAT_00495d8c + (uint)(byte)(&DAT_0049a0d0)[(uint)in_AX * 0x114] * 0x34);
  sVar4 = *(short *)(&DAT_00495d8e + (uint)(byte)(&DAT_0049a0d0)[(uint)in_AX * 0x114] * 0x34);
  while (sVar4 = sVar4 + -1, sVar4 != -1) {
    for (uVar3 = 0; uVar3 < uVar2; uVar3 = uVar3 + 1) {
      *param_2 = sVar4 * 0x100 + sVar1 + uVar3;
      param_2 = param_2 + 1;
      *unaff_EBX = *unaff_EBX + 1;
    }
  }
  return;
}
