/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004722a5, entrada 004722a5.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_004722a5(undefined4 param_1,undefined4 param_2)

{
  ushort uVar1;
  byte in_AL;
  int iVar2;
  byte bVar3;
  undefined2 extraout_var;
  undefined4 uVar4;
  undefined4 extraout_ECX;
  uint uVar5;
  undefined8 uVar6;
  longlong lVar7;

  uVar6 = FUN_0041a4f4(param_1,param_2);
  uVar5 = 0;
  uVar4 = CONCAT22(extraout_var,(ushort)(byte)uVar6);
  do {
    iVar2 = (uint)in_AL * 0x200;
    if (*(ushort *)(&DAT_00508728 + iVar2) <= (ushort)uVar5) {
      return CONCAT31((int3)((uint)iVar2 >> 8),(char)((uint)uVar4 >> 8));
    }
    uVar1 = *(ushort *)(&DAT_0050872a + (uVar5 & 0xffff) * 2 + iVar2);
    lVar7 = FUN_00443dad(uVar4,uVar5);
    uVar5 = (uint)lVar7;
    uVar4 = extraout_ECX;
    if ((char)lVar7 != '\0') {
      bVar3 = (byte)extraout_ECX;
      if (bVar3 < 3) {
LAB_004722d0:
        return uVar5 & 0xffffff00;
      }
      if (bVar3 < 4) {
        uVar5 = (uint)tabela_unidades[uVar1].tipo_id;
        if ((((uVar5 != 7) && (uVar5 != 5)) && (uVar5 != 0xd)) && (uVar5 != 6)) goto LAB_004722d0;
      }
      else if ((bVar3 != 4) || (uVar5 = (uint)tabela_unidades[uVar1].tipo_id, uVar5 != 5))
      goto LAB_004722d0;
      uVar4 = CONCAT22((short)((uint)extraout_ECX >> 0x10),CONCAT11(1,bVar3));
    }
    uVar5 = (int)((ulonglong)lVar7 >> 0x20) + 1;
  } while( true );
}
