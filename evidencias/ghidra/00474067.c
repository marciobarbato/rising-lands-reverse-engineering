/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00474067, entrada 00474067.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00474067(undefined4 param_1,uint param_2)

{
  ushort indice_unidade;
  byte in_AL;
  bool bVar1;
  uint uVar2;
  int iVar3;
  int extraout_ECX;
  int extraout_ECX_00;
  int extraout_ECX_01;
  longlong lVar4;

  uVar2 = 0;
  while ((ushort)uVar2 < *(ushort *)(&DAT_00508728 + (uint)in_AL * 0x200)) {
    indice_unidade = *(ushort *)(&DAT_0050872a + (uVar2 & 0xffff) * 2 + (uint)in_AL * 0x200);
    lVar4 = FUN_00443dad(uVar2,(uint)indice_unidade);
    iVar3 = extraout_ECX;
    if ((char)lVar4 != '\0') {
      bVar1 = unidade_vida_diferente_do_maximo(indice_unidade);
      iVar3 = extraout_ECX_00;
      if (bVar1) {
        FUN_00445b10(extraout_ECX_00,param_2 & 0xffff);
        iVar3 = extraout_ECX_01;
      }
    }
    uVar2 = iVar3 + 1;
  }
  return;
}
