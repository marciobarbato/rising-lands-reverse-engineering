/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined4 __fastcall OriginaisSBL::BatimentOccupeCase(undefined4 param_1,uint param_2)

{
  ushort uVar1;
  ushort uVar2;
  ushort uVar3;
  uint in_EAX;
  int iVar4;
  uint uVar5;
  uint uVar6;
  uint extraout_ECX;
  ushort uVar7;

  iVar4 = (in_EAX & 0xffff) * 0x114;
  uVar1 = *(ushort *)(&DAT_0049a0ca + iVar4);
  uVar2 = *(ushort *)(&DAT_00495d8c + (uint)(byte)(&DAT_0049a0d0)[iVar4] * 0x34);
  uVar3 = *(ushort *)(&DAT_00495d8e + (uint)(byte)(&DAT_0049a0d0)[iVar4] * 0x34);
  uVar6 = 0;
  do {
    if (uVar3 <= (ushort)uVar6) {
      return 0;
    }
    for (uVar7 = 0; uVar7 < uVar2; uVar7 = uVar7 + 1) {
      if (((uint)uVar7 + (uVar6 & 0xffff) * 0x100 + (uint)uVar1 == (param_2 & 0xffff)) &&
         (uVar5 = BatimentCollision(uVar6,(uint)(ushort)(uVar2 * (short)uVar6 + uVar7)),
         uVar6 = extraout_ECX, (char)uVar5 != '\0')) {
        return 1;
      }
    }
    uVar6 = uVar6 + 1;
  } while( true );
}
