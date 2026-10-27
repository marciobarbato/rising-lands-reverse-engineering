/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00472ab2, entrada 00472ab2.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

longlong __fastcall FUN_00472ab2(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  uint in_EAX;
  uint uVar2;
  undefined4 extraout_ECX;
  uint extraout_ECX_00;
  int iVar3;
  uint extraout_EDX;
  ushort uVar4;
  longlong lVar5;

  uVar2 = (in_EAX & 0xff) << 8;
  uVar4 = 0;
  while( true ) {
    iVar3 = (uVar2 >> 8 & 0xff) * 0x200;
    if (*(ushort *)(&DAT_00508728 + iVar3) <= uVar4) {
      return CONCAT44(param_2,CONCAT31((int3)(in_EAX >> 8),1));
    }
    bVar1 = unidade_obter_tipo(*(ushort *)(&DAT_0050872a + (uint)uVar4 * 2 + iVar3));
    lVar5 = FUN_00443dad(CONCAT31((int3)((uint)extraout_ECX >> 8),bVar1),extraout_EDX);
    in_EAX = (uint)lVar5;
    if (((((char)lVar5 != '\0') && (uVar2 = extraout_ECX_00 & 0xff, uVar2 != 5)) && (uVar2 != 7)) &&
       ((uVar2 != 6 && (uVar2 != 0xd)))) break;
    uVar4 = uVar4 + 1;
    uVar2 = extraout_ECX_00;
  }
  return (ulonglong)CONCAT43(param_2,(int3)((ulonglong)lVar5 >> 8)) << 8;
}
