/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00473cc5, entrada 00473cc5.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00473cc5(undefined4 param_1)

{
  undefined1 in_AL;
  int iVar1;
  uint uVar2;
  uint uVar3;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_ECX_01;
  ushort uVar4;
  longlong lVar5;

  uVar3 = CONCAT31((int3)((uint)param_1 >> 8),in_AL);
  for (uVar4 = 0; iVar1 = (uVar3 & 0xff) * 0x200, uVar4 < *(ushort *)(&DAT_00508728 + iVar1);
      uVar4 = uVar4 + 1) {
    lVar5 = FUN_00443dad(uVar3,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar4 * 2 + iVar1));
    uVar3 = extraout_ECX;
    if (((char)lVar5 != '\0') &&
       ((byte)extraout_ECX == tabela_unidades[(int)((ulonglong)lVar5 >> 0x20)].proprietario_id)) {
      uVar2 = FUN_00442c34();
      uVar3 = extraout_ECX_00;
      if ((char)uVar2 != '\0') {
        FUN_00453b84();
        uVar3 = extraout_ECX_01;
      }
    }
  }
  return;
}
