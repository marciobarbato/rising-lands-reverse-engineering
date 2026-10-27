/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004721f9, entrada 004721f9.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_004721f9(undefined4 param_1,undefined4 param_2)

{
  byte in_AL;
  bool bVar1;
  uint uVar2;
  uint extraout_ECX;
  uint extraout_ECX_00;
  ushort uVar3;
  longlong lVar4;

  uVar2 = 0;
  for (uVar3 = 0; uVar3 < *(ushort *)(&DAT_00508728 + (uint)in_AL * 0x200); uVar3 = uVar3 + 1) {
    lVar4 = FUN_00443dad(uVar2,(uint)*(ushort *)
                                      (&DAT_0050872a + (uint)uVar3 * 2 + (uint)in_AL * 0x200));
    uVar2 = extraout_ECX;
    if ((char)lVar4 != '\0') {
      bVar1 = unidade_vida_diferente_do_maximo((ushort)((ulonglong)lVar4 >> 0x20));
      uVar2 = extraout_ECX_00;
      if (bVar1) {
        uVar2 = extraout_ECX_00 + 1;
      }
    }
  }
  return CONCAT44(param_2,CONCAT31((int3)((uVar2 & 0xffff) >> 8),(uVar2 & 0xffff) != 0));
}
