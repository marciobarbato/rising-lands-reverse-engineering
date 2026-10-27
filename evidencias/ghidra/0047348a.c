/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0047348a, entrada 0047348a.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0047348a(undefined4 param_1,undefined2 param_2)

{
  byte in_AL;
  uint uVar1;
  int iVar2;
  int extraout_ECX;
  int extraout_ECX_00;
  byte *pbVar3;
  longlong lVar4;

  uVar1 = 0;
  while ((ushort)uVar1 < *(ushort *)(&DAT_00508728 + (uint)in_AL * 0x200)) {
    lVar4 = FUN_00443dad(uVar1,(uint)(tabela_unidades +
                                     *(ushort *)
                                      (&DAT_0050872a + (uVar1 & 0xffff) * 2 + (uint)in_AL * 0x200)))
    ;
    pbVar3 = (byte *)((ulonglong)lVar4 >> 0x20);
    iVar2 = extraout_ECX;
    if ((((char)lVar4 != '\0') && (*pbVar3 == in_AL)) && (pbVar3[1] == 0xe)) {
      FUN_00445307(extraout_ECX,param_2);
      iVar2 = extraout_ECX_00;
    }
    uVar1 = iVar2 + 1;
  }
  return;
}
