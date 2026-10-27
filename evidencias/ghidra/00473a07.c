/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00473a07, entrada 00473a07.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00473a07(undefined4 param_1,char param_2)

{
  bool bVar1;
  UnidadeParcial *pUVar2;
  byte in_AL;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  ushort uVar3;
  longlong lVar4;

  bVar1 = false;
  for (uVar3 = 0; pUVar2 = tabela_unidades, uVar3 < *(ushort *)(&DAT_00508728 + (uint)in_AL * 0x200)
      ; uVar3 = uVar3 + 1) {
    lVar4 = FUN_00443dad((uint)*(ushort *)(&DAT_0050872a + (uint)uVar3 * 2 + (uint)in_AL * 0x200),
                         (uint)*(ushort *)(&DAT_0050872a + (uint)uVar3 * 2 + (uint)in_AL * 0x200) *
                         0x114);
    if ((((char)lVar4 != '\0') &&
        ((&pUVar2->proprietario_id)[(int)((ulonglong)lVar4 >> 0x20)] == in_AL)) &&
       ((&pUVar2->proprietario_id + (int)((ulonglong)lVar4 >> 0x20))[1] == 7)) {
      FUN_004454ce(extraout_ECX,param_2);
      if (!bVar1) {
        bVar1 = true;
        if (in_AL == DAT_00508041) {
          FUN_00440d5e(extraout_ECX_00,0x11);
        }
      }
    }
  }
  return;
}
