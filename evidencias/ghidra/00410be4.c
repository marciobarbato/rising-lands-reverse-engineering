/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00410be4, entrada 00410be4.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00410be4(undefined4 param_1,ushort param_2)

{
  bool bVar1;
  UnidadeParcial *pUVar2;
  byte bVar3;
  char cVar4;
  uint uVar5;
  short sVar6;
  int extraout_ECX;
  undefined4 extraout_ECX_00;
  int extraout_ECX_01;
  int iVar7;
  int extraout_ECX_02;
  int extraout_ECX_03;
  int extraout_ECX_04;
  undefined4 extraout_ECX_05;
  undefined4 extraout_EDX;
  byte *extraout_EDX_00;
  byte *extraout_EDX_01;
  uint extraout_EDX_02;
  undefined4 extraout_EDX_03;
  ushort unaff_BX;
  ushort uVar8;
  byte *pbVar9;
  undefined8 uVar10;
  byte bVar11;
  undefined2 local_2e;

  pUVar2 = tabela_unidades;
  bVar3 = unidade_obter_proprietario(unaff_BX);
  pbVar9 = &pUVar2->proprietario_id + extraout_ECX * 4;
  if (bVar3 != DAT_00508041) {
    return;
  }
  bVar3 = pbVar9[1];
  FUN_00441108(extraout_ECX * 4,extraout_EDX);
  FUN_0041087e(extraout_ECX_00,param_2);
  if ((*(short *)(&tabela_unidades->field_0x4 + extraout_ECX_01) ==
       *(short *)(&tabela_unidades->field_0x76 + extraout_ECX_01)) &&
     (*(ushort *)(&tabela_unidades->field_0x74 + extraout_ECX_01) < 100)) {
    bVar1 = true;
  }
  else {
    bVar1 = false;
  }
  if ((!bVar1) || (DAT_00508041 != *pbVar9)) {
    uVar5 = FUN_00442c34();
    if ((char)uVar5 != '\0') {
      bVar11 = *extraout_EDX_01;
      if (bVar11 == 200) goto LAB_00410d2b;
LAB_00410dcf:
      FUN_0045c455('\x01',param_2 - 2,bVar11);
    }
  }
  else if (((*(ushort *)(pbVar9 + 0x74) / 5) % 2 == 0) &&
          (uVar5 = FUN_00442c34(), (char)uVar5 != '\0')) {
    bVar11 = *extraout_EDX_00;
    if (bVar11 != 200) goto LAB_00410dcf;
LAB_00410d2b:
    FUN_0045b247('\x01',param_2 - 2);
  }
  iVar7 = CONCAT22(local_2e,param_2) + -2;
  if (pbVar9[0xba] == '\0') {
    uVar10 = FUN_0044f9a6(iVar7,tabela_unidades + unaff_BX);
    cVar4 = FUN_004422b0();
    iVar7 = extraout_ECX_03;
    if ((cVar4 == '\0') || ((char)uVar10 == '\0')) goto LAB_00410ece;
    sVar6 = (short)extraout_ECX_03;
  }
  else {
    if (DAT_00508f7c % 5 != 0) goto LAB_00410ece;
    FUN_0044f9a6(iVar7,unaff_BX & 0xffff00ff);
    cVar4 = FUN_004422b0();
    iVar7 = extraout_ECX_02;
    if ((cVar4 == '\0') || ((extraout_EDX_02 & 0xffff) == 0)) goto LAB_00410ece;
    sVar6 = (short)extraout_ECX_02;
  }
  FUN_0045b247('\x01',sVar6);
  iVar7 = extraout_ECX_04;
LAB_00410ece:
  FUN_00410a2c(iVar7,(int)(short)(param_2 + 10));
  if ((bVar3 == 0xe) || (bVar3 == 0x10)) {
    FUN_0044828b(extraout_ECX_05,extraout_EDX_03);
    for (uVar8 = 0; uVar8 < 5; uVar8 = uVar8 + 1) {
      FUN_0045b247('\x01',param_2 + 0x1e);
    }
  }
  return;
}
