/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00472a0c, entrada 00472a0c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00472a0c(undefined4 param_1,undefined4 param_2)

{
  uint in_EAX;
  uint uVar1;
  uint extraout_ECX;
  undefined4 extraout_ECX_00;
  int iVar2;
  ushort uVar3;
  longlong lVar4;

  uVar1 = CONCAT22((short)((uint)param_1 >> 0x10),(ushort)(byte)in_EAX);
  for (uVar3 = 0; iVar2 = (uVar1 & 0xff) * 0x200, uVar3 < *(ushort *)(&DAT_00508728 + iVar2);
      uVar3 = uVar3 + 1) {
    lVar4 = FUN_00443dad(uVar1,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar3 * 2 + iVar2));
    in_EAX = (uint)lVar4;
    uVar1 = extraout_ECX;
    if ((char)lVar4 != '\0') {
      unidade_obter_tipo((ushort)((ulonglong)lVar4 >> 0x20));
      in_EAX = FUN_00442434();
      if ((char)in_EAX == '\0') goto LAB_00472a60;
      uVar1 = CONCAT22((short)((uint)extraout_ECX_00 >> 0x10),CONCAT11(1,(char)extraout_ECX_00));
    }
  }
  in_EAX = CONCAT31((int3)(in_EAX >> 8),(char)(uVar1 >> 8));
LAB_00472a60:
  return CONCAT44(param_2,in_EAX);
}
