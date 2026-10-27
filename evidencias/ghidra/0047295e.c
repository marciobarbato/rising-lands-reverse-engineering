/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0047295e, entrada 0047295e.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_0047295e(undefined4 param_1,undefined4 param_2)

{
  bool bVar1;
  undefined4 in_EAX;
  undefined3 extraout_var;
  uint uVar2;
  uint extraout_ECX;
  uint extraout_ECX_00;
  int iVar3;
  ushort uVar4;
  longlong lVar5;

  uVar2 = CONCAT31((int3)((uint)param_1 >> 8),(char)in_EAX);
  uVar4 = 0;
  do {
    iVar3 = (uVar2 & 0xff) * 0x200;
    if (*(ushort *)(&DAT_00508728 + iVar3) <= uVar4) {
      return CONCAT44(param_2,CONCAT31((int3)((uint)in_EAX >> 8),1));
    }
    lVar5 = FUN_00443dad(uVar2,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar4 * 2 + iVar3));
    in_EAX = (undefined4)lVar5;
    uVar2 = extraout_ECX;
    if ((char)lVar5 != '\0') {
      unidade_obter_tipo((ushort)((ulonglong)lVar5 >> 0x20));
      bVar1 = FUN_004422fc();
      in_EAX = CONCAT31(extraout_var,bVar1);
      uVar2 = extraout_ECX_00;
      if (!bVar1) {
        return CONCAT44(param_2,in_EAX);
      }
    }
    uVar4 = uVar4 + 1;
  } while( true );
}
