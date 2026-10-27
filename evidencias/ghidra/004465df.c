/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004465df, entrada 004465df.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_004465df(undefined4 param_1,short param_2)

{
  bool bVar1;
  ushort in_AX;
  uint uVar2;
  int iVar3;
  uint uVar4;
  uint extraout_ECX;
  uint uVar5;

  uVar5 = 0xffff;
  uVar4 = 0;
  do {
    if (799 < (uVar4 & 0xffff)) {
      return uVar5 & 0xffff;
    }
    if ((short)uVar4 != param_2) {
      if ((tabela_unidades[uVar4 & 0xffff].estado == 0) ||
         (tabela_unidades[uVar4 & 0xffff].estado == 4)) {
        bVar1 = false;
      }
      else {
        bVar1 = true;
      }
      if ((((bVar1) && (uVar2 = uVar4 & 0xffff, tabela_unidades[uVar2].field_0x72 != '\0')) &&
          (iVar3 = FUN_0044246e(uVar4,in_AX), uVar4 = extraout_ECX, (char)iVar3 != '\0')) &&
         (uVar5 = extraout_ECX, tabela_unidades[uVar2].field_0xab != '\0')) {
        return extraout_ECX;
      }
    }
    uVar4 = uVar4 + 1;
  } while( true );
}
