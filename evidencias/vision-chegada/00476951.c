/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined4 __fastcall OriginaisSBL::TerrainEstIllumine(undefined4 param_1,uint param_2)

{
  uint in_EAX;

  return CONCAT31((int3)((in_EAX & 0xffff) >> 8),
                  (*(byte *)((&DAT_00507d88)[param_2 & 0xff] + (in_EAX & 0xffff)) & 0x1f) == 0);
}
