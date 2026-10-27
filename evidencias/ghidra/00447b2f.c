/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00447b2f, entrada 00447b2f.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00447b2f(void)

{
  UnidadeParcial *pUVar1;
  uint in_EAX;
  uint uVar2;
  undefined4 uVar3;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_ECX_01;
  uint extraout_ECX_02;
  uint extraout_ECX_03;
  uint uVar4;
  undefined4 extraout_ECX_04;
  undefined4 extraout_EDX;
  ulonglong uVar5;
  undefined8 uVar6;

  pUVar1 = tabela_unidades;
  uVar2 = in_EAX & 0xffff;
  if (tabela_unidades[uVar2].field_0xae == '\0') {
    uVar5 = FUN_004704dc(in_EAX,0);
    in_EAX = extraout_ECX;
    if ((int)(uVar5 % 0x28) == 0) {
      if ((byte)pUVar1[uVar2].field_0xab < 0x29) {
        if (pUVar1[uVar2].field_0x94 != '\0') {
          pUVar1[uVar2].field_0x94 = pUVar1[uVar2].field_0x94 + -1;
        }
      }
      else if (pUVar1[uVar2].field_0x94 == '\0') {
        pUVar1[uVar2].field_0x94 = pUVar1[uVar2].field_0x94 + '\x01';
      }
      else if (pUVar1[uVar2].field_0x94 == '\x02') {
        pUVar1[uVar2].field_0x94 = 1;
      }
      else {
        uVar5 = FUN_004704dc(extraout_ECX,0);
        pUVar1[uVar2].field_0x94 = pUVar1[uVar2].field_0x94 + (char)(uVar5 % 3) + -1;
        in_EAX = extraout_ECX_00;
      }
    }
  }
  if (pUVar1[uVar2].field_0xae == '\0') {
    uVar5 = FUN_004704dc(in_EAX,0);
    in_EAX = extraout_ECX_01;
    if ((int)(uVar5 % 10) == 0) {
      if ((byte)pUVar1[uVar2].field_0xab < 0x29) {
        pUVar1[uVar2].field_0x95 = 0;
      }
      if ((pUVar1[uVar2].field_0x95 == '\0') && (pUVar1[uVar2].field_0x96 != '\0')) {
        pUVar1[uVar2].field_0x96 = pUVar1[uVar2].field_0x96 + -1;
      }
      else if ((byte)pUVar1[uVar2].field_0x96 < 0x10) {
        pUVar1[uVar2].field_0x96 = pUVar1[uVar2].field_0x96 + 1;
      }
      if (pUVar1[uVar2].field_0x96 == '\0') {
        pUVar1[uVar2].field_0x95 = 1;
      }
      if (pUVar1[uVar2].field_0x96 == '\x0f') {
        pUVar1[uVar2].field_0x95 = 0;
      }
    }
  }
  if (pUVar1[uVar2].field_0xae == '\0') {
    uVar5 = FUN_004704dc(in_EAX,0);
    uVar4 = extraout_ECX_03;
    if ((int)(uVar5 % 10) == 0) {
      pUVar1[uVar2].field_0xab = pUVar1[uVar2].field_0xab + -1;
    }
  }
  else {
    uVar5 = FUN_004704dc(in_EAX,0);
    if ((int)(uVar5 % 5) == 0) {
      pUVar1[uVar2].field_0xab = pUVar1[uVar2].field_0xab + '\x01';
    }
    pUVar1[uVar2].quadro_movimento = pUVar1[uVar2].quadro_movimento + 1;
    uVar4 = extraout_ECX_02;
  }
  if ((((pUVar1[uVar2].field_0xae == '\0') && ((byte)pUVar1[uVar2].field_0xab < 0x28)) &&
      (pUVar1[uVar2].field_0x96 == '\0')) && (pUVar1[uVar2].field_0x94 == '\0')) {
    pUVar1[uVar2].field_0xae = 1;
    pUVar1[uVar2].quadro_movimento = 0;
    pUVar1 = tabela_unidades;
    uVar4 = uVar4 & 0xffff;
    uVar3 = FUN_004766f0(uVar4,(uint)DAT_00508041);
    if ((char)uVar3 != '\0') {
      uVar6 = FUN_00440c5d(extraout_ECX_04,extraout_EDX);
      pUVar1[uVar4].field_0xf9 = 0;
      if (*(int *)&pUVar1[uVar4].field_0x104 == -1) {
        FUN_0048aa79(0,(uint)pUVar1[uVar4].tipo_id << 0x10 | 0x800,(uint)uVar6);
        return;
      }
    }
  }
  else if (pUVar1[uVar2].field_0xab == '2') {
    pUVar1[uVar2].field_0xae = 0;
  }
  return;
}
