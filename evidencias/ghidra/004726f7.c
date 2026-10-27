/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004726f7, entrada 004726f7.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004726f7(undefined4 param_1,undefined1 param_2)

{
  undefined1 in_AL;
  byte bVar1;
  undefined4 uVar2;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  int extraout_EDX;
  ushort uVar3;
  longlong lVar4;

  uVar2 = CONCAT31(CONCAT21((short)((uint)param_1 >> 0x10),in_AL),param_2);
  for (uVar3 = 0; uVar3 < 800; uVar3 = uVar3 + 1) {
    lVar4 = FUN_00443dad(uVar2,(uint)uVar3);
    uVar2 = extraout_ECX;
    if ((char)lVar4 != '\0') {
      bVar1 = unidade_obter_proprietario((ushort)((ulonglong)lVar4 >> 0x20));
      uVar2 = extraout_ECX_00;
      if (bVar1 == (byte)((uint)extraout_ECX_00 >> 8)) {
        if ((byte)extraout_ECX_00 == tabela_unidades[extraout_EDX].grupo_id) {
          tabela_unidades[extraout_EDX].grupo_id = 0;
        }
        if (tabela_unidades[uVar3].selecionada != 0) {
          tabela_unidades[uVar3].grupo_id = (byte)extraout_ECX_00;
        }
      }
    }
  }
  return;
}
