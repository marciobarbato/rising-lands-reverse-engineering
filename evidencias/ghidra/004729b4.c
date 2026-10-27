/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004729b4, entrada 004729b4.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_004729b4(undefined4 param_1,undefined4 param_2)

{
  char cVar1;
  undefined4 in_EAX;
  undefined3 extraout_var;
  uint uVar2;
  uint extraout_ECX;
  undefined4 extraout_ECX_00;
  int iVar3;
  ushort uVar4;
  longlong lVar5;

  uVar2 = CONCAT22((short)((uint)param_1 >> 0x10),(ushort)(byte)in_EAX);
  for (uVar4 = 0; iVar3 = (uVar2 & 0xff) * 0x200, uVar4 < *(ushort *)(&DAT_00508728 + iVar3);
      uVar4 = uVar4 + 1) {
    lVar5 = FUN_00443dad(uVar2,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar4 * 2 + iVar3));
    in_EAX = (undefined4)lVar5;
    uVar2 = extraout_ECX;
    if ((char)lVar5 != '\0') {
      unidade_obter_tipo((ushort)((ulonglong)lVar5 >> 0x20));
      cVar1 = FUN_00442347();
      in_EAX = CONCAT31(extraout_var,cVar1);
      if (cVar1 == '\0') goto LAB_00472a08;
      uVar2 = CONCAT22((short)((uint)extraout_ECX_00 >> 0x10),CONCAT11(1,(char)extraout_ECX_00));
    }
  }
  in_EAX = CONCAT31((int3)((uint)in_EAX >> 8),(char)(uVar2 >> 8));
LAB_00472a08:
  return CONCAT44(param_2,in_EAX);
}
