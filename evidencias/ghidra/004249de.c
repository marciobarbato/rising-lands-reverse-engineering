/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004249de, entrada 004249de.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_004249de(void)

{
  byte bVar1;
  ushort in_AX;
  ushort uVar2;
  uint uVar3;
  undefined4 uVar4;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  uint extraout_ECX_03;
  undefined4 extraout_ECX_04;
  int extraout_EDX;
  ushort indice_unidade;
  longlong lVar5;
  ushort local_1c;

  uVar4 = 0x100;
  local_1c = *(ushort *)(&DAT_0049a0ca + (uint)in_AX * 0x114) / 0x100;
  for (indice_unidade = 0; (short)indice_unidade < 800; indice_unidade = indice_unidade + 1) {
    lVar5 = FUN_00443dad(uVar4,(int)(short)indice_unidade);
    uVar4 = extraout_ECX_00;
    if ((((char)lVar5 != '\0') &&
        (bVar1 = unidade_obter_tipo(indice_unidade), uVar4 = extraout_ECX_01, bVar1 == 4)) &&
       (uVar3 = FUN_00479555(tabela_unidades[extraout_EDX].celula_atual / 0x100,local_1c),
       uVar4 = extraout_ECX_02, uVar3 < 0x11)) {
      unidade_obter_proprietario(indice_unidade);
      uVar3 = FUN_00428cc0(extraout_ECX_03,9);
      if ((short)uVar3 == 0) {
        uVar2 = 0x3c;
      }
      else {
        uVar2 = (ushort)(600 / (ulonglong)(longlong)(int)(uVar3 & 0xffff));
      }
      uVar4 = extraout_ECX_04;
      if (DAT_00508f7c % (uint)uVar2 == 0) {
        FUN_004482d3(extraout_ECX_04,'\x01');
        uVar4 = extraout_ECX;
      }
    }
  }
  FUN_0041db1e();
  return;
}
