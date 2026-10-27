/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined4 __fastcall FUN_0047fbea(undefined4 param_1,uint param_2)

{
  int iVar1;

  iVar1 = FUN_0047f927(param_1,param_2 & 0xff);
  return CONCAT31((int3)((uint)iVar1 >> 8),1);
}
