/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00442139, entrada 00442139.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00442139(char param_1,ushort *param_2)

{
  bool bVar1;
  byte in_AL;
  uint uVar2;
  uint uVar3;
  ushort uVar4;
  ushort *unaff_EBX;
  uint uVar5;
  uint local_24;
  uint local_1c;
  uint local_18;

  uVar4 = 0;
  local_18 = 0xffff;
  uVar5 = 0xffff;
  local_24 = 0;
  local_1c = 0;
  do {
    uVar2 = (uint)uVar4;
    if (799 < uVar2) {
LAB_00442212:
      if (uVar4 == 800) {
        local_18 = (uint)*unaff_EBX;
        uVar5 = (uint)*param_2;
        local_1c = (DAT_00508724 + uVar5) - 1;
        local_24 = (local_18 + DAT_00508726) - 1;
      }
      *param_2 = (short)((int)((local_1c & 0xffff) - uVar5) / 2) + (short)uVar5;
      *unaff_EBX = (short)((int)((local_24 & 0xffff) - local_18) / 2) + (short)local_18;
      return;
    }
    if ((tabela_unidades[uVar2].estado == 0) || (tabela_unidades[uVar2].estado == 4)) {
      bVar1 = false;
    }
    else {
      bVar1 = true;
    }
    if (((bVar1) && (tabela_unidades[uVar2].grupo_id == param_1)) &&
       (tabela_unidades[uVar4].proprietario_id == in_AL)) {
      uVar3 = (uint)tabela_unidades[uVar2].celula_atual % 0x100;
      uVar2 = tabela_unidades[uVar2].celula_atual / 0x100;
      if ((short)uVar3 != -1) {
        uVar5 = uVar3;
      }
      if ((short)uVar2 != -1) {
        local_18 = uVar2;
      }
      if ((short)uVar3 != 0) {
        local_1c = uVar3;
      }
      if ((short)uVar2 != 0) {
        local_24 = uVar2;
      }
      goto LAB_00442212;
    }
    uVar4 = uVar4 + 1;
  } while( true );
}
