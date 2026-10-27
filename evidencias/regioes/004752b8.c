/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

longlong __fastcall OriginaisSBL::TerrainEstObstacleNaturel(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  uint in_EAX;
  undefined3 uVar2;
  uint uVar3;

  uVar3 = (uint)*(ushort *)(DAT_00507d70 + (in_EAX & 0xffff) * 2);
  if ((0x2bd < uVar3) || (*(char *)(uVar3 + DAT_00507db0) == '\0')) {
    bVar1 = *(byte *)((in_EAX & 0xffff) + DAT_00507d74);
    uVar2 = (undefined3)((uint)DAT_00507d74 >> 8);
    in_EAX = CONCAT31(uVar2,bVar1);
    if ((bVar1 == 0) || (0xb < bVar1)) {
      return (ulonglong)CONCAT43(param_2,uVar2) << 8;
    }
  }
  return CONCAT44(param_2,CONCAT31((int3)(in_EAX >> 8),1));
}
