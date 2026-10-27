/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall
FUN_0047d920(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
            undefined4 param_5,undefined4 param_6)

{
  undefined1 in_AL;
  int iVar1;
  int iVar2;
  undefined4 extraout_ECX;
  undefined4 unaff_EBX;
  undefined8 uVar3;

  uVar3 = FUN_0047d7ec(param_1,param_2);
  iVar2 = (int)uVar3;
  if (iVar2 != -1) {
    iVar1 = iVar2 * 0x60;
    if (iVar1 == -0x512320) {
      iVar2 = -1;
    }
    else {
      *(undefined4 *)(&DAT_00512338 + iVar1) = unaff_EBX;
      *(undefined4 *)(&DAT_0051233c + iVar1) = extraout_ECX;
      *(undefined4 *)(&DAT_00512340 + iVar1) = param_3;
      *(undefined4 *)(&DAT_00512344 + iVar1) = param_4;
      *(undefined4 *)(&DAT_00512348 + iVar1) = param_5;
      *(undefined4 *)(&DAT_0051234c + iVar1) = param_6;
      (&DAT_0051237c)[iVar1] = in_AL;
      FUN_0047d07a(extraout_ECX,iVar2);
    }
  }
  return iVar2;
}
