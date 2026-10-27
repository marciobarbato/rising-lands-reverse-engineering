/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004741cd, entrada 004741cd.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004741cd(undefined4 param_1,undefined1 param_2)

{
  bool bVar1;
  UnidadeParcial *pUVar2;
  byte bVar3;
  ushort in_AX;
  int iVar4;
  ushort uVar5;
  undefined4 extraout_ECX;
  uint extraout_ECX_00;
  uint uVar6;
  int extraout_EDX;
  longlong lVar7;
  undefined8 uVar8;

  lVar7 = FUN_00443dad(CONCAT31((int3)((uint)param_1 >> 8),param_2),(uint)in_AX);
  iVar4 = (int)((ulonglong)lVar7 >> 0x20);
  if ((char)lVar7 != '\0') {
    uVar6 = (uint)tabela_unidades[iVar4].estado;
    if (((uVar6 == 0xe) ||
        (((tabela_unidades[iVar4].tipo_id == 0x10 && (uVar6 == 0xd)) &&
         (tabela_unidades[iVar4].field_0xab != '2')))) ||
       (uVar8 = FUN_004465bf(extraout_ECX,uVar6), (char)uVar8 == '\0')) {
      bVar1 = false;
    }
    else {
      bVar1 = true;
    }
    if (((bVar1) &&
        (bVar3 = unidade_obter_proprietario(in_AX), pUVar2 = tabela_unidades,
        bVar3 == (byte)extraout_ECX_00)) && (tabela_unidades[extraout_EDX].selecionada == 0)) {
      iVar4 = (extraout_ECX_00 & 0xff) * 0x200;
      if (*(ushort *)(&DAT_00508728 + iVar4) < 0xff) {
        uVar5 = *(ushort *)(&DAT_00508728 + iVar4) + 1;
        *(ushort *)(&DAT_00508728 + iVar4) = uVar5;
        *(ushort *)(&DAT_00508728 + (uint)uVar5 * 2 + iVar4) = in_AX;
        pUVar2[extraout_EDX].selecionada = 1;
        tabela_unidades[in_AX].selecionada = 1;
      }
    }
  }
  return;
}
