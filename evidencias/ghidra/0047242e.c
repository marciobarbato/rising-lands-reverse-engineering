/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0047242e, entrada 0047242e.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_0047242e(undefined4 param_1,undefined1 param_2)

{
  ushort uVar1;
  uint in_EAX;
  uint uVar2;
  int iVar3;
  int extraout_ECX;
  uint uVar4;
  int iVar5;
  longlong lVar6;

  iVar3 = (uint)CONCAT21((short)((uint)param_1 >> 0x10),param_2) << 8;
  uVar4 = 0;
  uVar2 = in_EAX;
  do {
    iVar5 = (in_EAX & 0xff) * 0x200;
    if (*(ushort *)(&DAT_00508728 + iVar5) <= (ushort)uVar4) {
      return CONCAT31((int3)(uVar2 >> 8),(char)iVar3);
    }
    uVar1 = *(ushort *)(&DAT_0050872a + (uVar4 & 0xffff) * 2 + iVar5);
    lVar6 = FUN_00443dad(iVar3,uVar4);
    uVar2 = (uint)lVar6;
    iVar3 = extraout_ECX;
    if ((char)lVar6 != '\0') {
      uVar2 = (uint)uVar1 * 0x114;
      if ((byte)((uint)extraout_ECX >> 8) != tabela_unidades[uVar1].tipo_id) {
        return uVar2 & 0xffffff00;
      }
      iVar3 = CONCAT31((int3)((uint)extraout_ECX >> 8),1);
    }
    uVar4 = (int)((ulonglong)lVar6 >> 0x20) + 1;
  } while( true );
}
