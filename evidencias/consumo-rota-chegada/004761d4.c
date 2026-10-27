/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

bool __fastcall OriginaisSBL::TerrainEnCollision(undefined4 param_1,byte param_2)

{
  uint in_EAX;

  return (*(byte *)((in_EAX & 0xffff) + DAT_00507da8) & param_2) != 0;
}
