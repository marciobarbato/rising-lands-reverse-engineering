/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00473d2c, entrada 00473d2c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00473d2c(undefined4 param_1,undefined4 param_2)

{
  bool bVar1;
  uint in_EAX;
  int iVar2;
  int extraout_ECX;
  undefined4 extraout_ECX_00;
  uint extraout_EDX;
  uint extraout_EDX_00;
  ushort uVar3;
  longlong lVar4;
  undefined2 local_18;

  lVar4 = CONCAT44(param_2,in_EAX);
  bVar1 = false;
  uVar3 = 0;
  while( true ) {
    iVar2 = (in_EAX & 0xff) * 0x200;
    if (*(ushort *)(&DAT_00508728 + iVar2) <= uVar3) break;
    lVar4 = FUN_00443dad((uint)*(ushort *)(&DAT_0050872a + (uint)uVar3 * 2 + iVar2),
                         (uint)((ulonglong)lVar4 >> 0x20));
    if (((char)lVar4 != '\0') &&
       (lVar4 = ZEXT48(tabela_unidades) << 0x20,
       tabela_unidades[extraout_ECX].proprietario_id == (byte)in_EAX)) {
      local_18 = (undefined2)param_2;
      FUN_00445947(extraout_ECX,local_18);
      lVar4 = (ulonglong)extraout_EDX << 0x20;
      if (!bVar1) {
        lVar4 = (ulonglong)CONCAT31((int3)(extraout_EDX >> 8),DAT_00508041) << 0x20;
        bVar1 = true;
        if ((byte)in_EAX == DAT_00508041) {
          FUN_00440d5e(extraout_ECX_00,0xf);
          lVar4 = (ulonglong)extraout_EDX_00 << 0x20;
        }
      }
    }
    uVar3 = uVar3 + 1;
  }
  return;
}
