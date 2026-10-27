/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall OriginaisSBL::B_TestUniteFaitRien(undefined4 param_1,undefined4 param_2)

{
  undefined8 uVar1;

  uVar1 = EnginGetEtat(param_1,param_2);
  if (((uint)uVar1 & 0xff) == 7) {
    return 1;
  }
  return 0xffffffff;
}
