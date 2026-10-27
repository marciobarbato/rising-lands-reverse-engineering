/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00446693, entrada 00446693.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00446693(undefined4 param_1,undefined4 param_2)

{
  bool bVar1;
  ushort in_AX;
  int iVar2;
  uint uVar3;
  uint extraout_ECX;
  uint uVar4;
  uint uVar5;

  uVar5 = 0xffff;
  uVar3 = 0;
  do {
    if (799 < (uVar3 & 0xffff)) {
      uVar5 = uVar5 & 0xffff;
LAB_00440d55:
      return CONCAT44(param_2,uVar5);
    }
    if ((tabela_unidades[uVar3 & 0xffff].estado == 0) ||
       (tabela_unidades[uVar3 & 0xffff].estado == 4)) {
      bVar1 = false;
    }
    else {
      bVar1 = true;
    }
    if ((bVar1) && (tabela_unidades[uVar3 & 0xffff].field_0x72 != '\0')) {
      uVar4 = uVar3 & 0xffff;
      iVar2 = FUN_0044246e(uVar3,in_AX);
      uVar3 = extraout_ECX;
      if ((((char)iVar2 != '\0') &&
          (((tabela_unidades[uVar4].tipo_id == 0x10 && (tabela_unidades[uVar4].field_0xab == '2'))
           || (tabela_unidades[extraout_ECX & 0xffff].tipo_id != 0x10)))) &&
         (uVar5 = extraout_ECX, tabela_unidades[extraout_ECX & 0xffff].field_0xab != '\0')) {
        goto LAB_00440d55;
      }
    }
    uVar3 = uVar3 + 1;
  } while( true );
}
