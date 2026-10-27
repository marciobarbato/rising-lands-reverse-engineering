/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004733b8, entrada 004733b8.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004733b8(undefined4 param_1)

{
  bool bVar1;
  byte in_AL;
  byte bVar2;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  uint uVar3;
  uint extraout_EDX;
  uint extraout_EDX_00;
  UnidadeParcial *pUVar4;
  ushort uVar5;
  ulonglong uVar6;

  bVar2 = (byte)param_1;
  uVar3 = 0;
  bVar1 = false;
  for (uVar5 = 0; uVar5 < *(ushort *)(&DAT_00508728 + (uint)in_AL * 0x200); uVar5 = uVar5 + 1) {
    pUVar4 = tabela_unidades + *(ushort *)(&DAT_0050872a + (uint)uVar5 * 2 + (uint)in_AL * 0x200);
    uVar6 = FUN_00443dad(param_1,uVar3);
    param_1 = extraout_ECX_00;
    if (((char)uVar6 != '\0') &&
       (uVar6 = uVar6 & 0xffffffff00000000, pUVar4->proprietario_id == in_AL)) {
      FUN_004456c9(bVar2);
      uVar6 = (ulonglong)extraout_EDX_00 << 0x20;
      param_1 = extraout_ECX_01;
      if ((in_AL == DAT_00508041) && (uVar6 = (ulonglong)extraout_EDX_00 << 0x20, !bVar1)) {
        bVar1 = true;
        if (bVar2 < 3) {
          uVar3 = 0x1c;
        }
        else {
          uVar3 = 0x1b;
        }
        FUN_00440d5e(1,uVar3);
        uVar6 = (ulonglong)extraout_EDX << 0x20;
        param_1 = extraout_ECX;
      }
    }
    uVar3 = (uint)(uVar6 >> 0x20);
  }
  return;
}
