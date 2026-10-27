/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004737e9, entrada 004737e9.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004737e9(uint param_1,undefined1 param_2)

{
  byte in_AL;
  uint extraout_ECX;
  byte *pbVar1;
  ushort uVar2;
  longlong lVar3;

  uVar2 = 0;
  while( true ) {
    if (*(ushort *)(&DAT_00508728 + (uint)in_AL * 0x200) <= uVar2) {
      return;
    }
    lVar3 = FUN_00443dad(param_1,(uint)(tabela_unidades +
                                       *(ushort *)
                                        (&DAT_0050872a + (uint)uVar2 * 2 + (uint)in_AL * 0x200)));
    pbVar1 = (byte *)((ulonglong)lVar3 >> 0x20);
    if ((((char)lVar3 != '\0') && (*pbVar1 == in_AL)) && (pbVar1[1] == 4)) break;
    uVar2 = uVar2 + 1;
    param_1 = extraout_ECX;
  }
  FUN_004459c4(extraout_ECX & 0xffff,param_2);
  return;
}
