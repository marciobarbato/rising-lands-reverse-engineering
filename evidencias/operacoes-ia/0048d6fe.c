/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

longlong __fastcall OriginaisSBL::debugSymAdr(undefined4 param_1,uint param_2)

{
  undefined4 in_EAX;
  undefined4 extraout_ECX;
  int *piVar1;
  undefined8 uVar2;

  if ((DAT_00522234 != (int *)0x0) && (DAT_00522238 != 0)) {
    for (piVar1 = DAT_00522234; *piVar1 != -1; piVar1 = piVar1 + 2) {
      uVar2 = FUN_0048d78d(in_EAX,(char *)in_EAX);
      if ((int)uVar2 != 0) {
        return CONCAT44(param_2,DAT_00522238 + *piVar1);
      }
      in_EAX = extraout_ECX;
    }
  }
  return (ulonglong)param_2 << 0x20;
}
