/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00473290, entrada 00473290.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00473290(undefined4 param_1,undefined2 param_2)

{
  bool bVar1;
  byte in_AL;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  ushort uVar2;
  longlong lVar3;

  bVar1 = false;
  for (uVar2 = 0; uVar2 < *(ushort *)(&DAT_00508728 + (uint)in_AL * 0x200); uVar2 = uVar2 + 1) {
    lVar3 = FUN_00443dad((uint)*(ushort *)(&DAT_0050872a + (uint)uVar2 * 2 + (uint)in_AL * 0x200),
                         (uint)(tabela_unidades +
                               *(ushort *)(&DAT_0050872a + (uint)uVar2 * 2 + (uint)in_AL * 0x200)));
    if (((char)lVar3 != '\0') && (*(byte *)((ulonglong)lVar3 >> 0x20) == in_AL)) {
      FUN_00444ebd(extraout_ECX,param_2);
      if (!bVar1) {
        bVar1 = true;
        if (in_AL == DAT_00508041) {
          FUN_00440d5e(extraout_ECX_00,0xf);
        }
      }
    }
  }
  return;
}
