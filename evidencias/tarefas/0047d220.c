/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

longlong __fastcall FUN_0047d220(undefined4 param_1,uint param_2)

{
  undefined4 *puVar1;

  puVar1 = (undefined4 *)&DAT_005148b0;
  FUN_0047cfd0(0x60,(int *)&DAT_00512320,1);
  do {
    puVar1 = puVar1 + 4;
    FUN_0047cfd0(0x60,(int *)&DAT_00512320,0);
  } while (puVar1 != &DAT_00514900);
  return (ulonglong)param_2 << 0x20;
}
