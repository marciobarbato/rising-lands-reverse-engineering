/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall OriginaisSBL::TerrainGetColor(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  ushort uVar2;
  bool bVar3;
  uint in_EAX;

  bVar1 = *(byte *)(DAT_00507d74 + (in_EAX & 0xffff));
  if ((bVar1 < 0x1d) || (0x34 < bVar1)) {
    bVar3 = false;
  }
  else {
    bVar3 = true;
  }
  if (!bVar3) {
    uVar2 = *(ushort *)(DAT_00507d70 + (in_EAX & 0xffff) * 2);
    in_EAX = (uint)uVar2;
    if (in_EAX < 0x2be) {
      return CONCAT44(param_2,(uint)CONCAT11((char)(uVar2 >> 8),(&DAT_00509694)[in_EAX]));
    }
  }
  return CONCAT44(param_2,CONCAT31((int3)(in_EAX >> 8),0x1e));
}
