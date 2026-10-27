/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 __fastcall
OriginaisSBL::iagUnitGetFirstUnitInGroup(undefined4 param_1,undefined4 param_2)

{
  int in_EAX;

  _DAT_0051b844 = &DAT_0051a9e0 + in_EAX * 8;
  if (&DAT_0051a9e0 + in_EAX * 8 != (undefined4 *)0x0) {
    DAT_0051b848 = (&DAT_0051a9f0)[in_EAX * 0x10];
    if (DAT_0051b848 != 0xffff) {
      return CONCAT44(param_2,(uint)DAT_0051b848);
    }
  }
  return CONCAT44(param_2,0xffff);
}
