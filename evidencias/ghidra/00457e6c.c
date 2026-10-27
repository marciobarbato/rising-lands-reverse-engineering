/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00457e6c, entrada 00457e6c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00457e6c(byte param_1)

{
  bool bVar1;
  undefined2 in_AX;
  ushort uVar2;
  uint uVar3;
  undefined4 extraout_ECX;
  uint extraout_ECX_00;
  byte unaff_BL;
  UnidadeParcial *pUVar4;
  int iVar5;
  ushort uVar6;
  undefined8 uVar7;

  uVar6 = 0;
  while ((uVar6 < 800 && (tabela_unidades[uVar6].estado != 0))) {
    uVar6 = uVar6 + 1;
  }
  if (uVar6 == 800) {
    FUN_004457cd();
    return;
  }
  pUVar4 = tabela_unidades + uVar6;
  switch(unaff_BL) {
  case 0xb:
  case 0xc:
  case 0xd:
  case 0xe:
  case 0xf:
  case 0x10:
  case 0x11:
    bVar1 = true;
    break;
  default:
    bVar1 = false;
  }
  if (((bVar1) && (unaff_BL != 0x11)) && (unaff_BL != 0x10)) {
    pUVar4->proprietario_id = 200;
  }
  else {
    pUVar4->proprietario_id = param_1;
  }
  FUN_00457b87(unaff_BL,in_AX);
  pUVar4->field_0xdc = 0;
  pUVar4->estado = 7;
  pUVar4->vida = 100;
  pUVar4->field_0x72 = 0;
  *(undefined2 *)&pUVar4->field_0x74 = 0;
  *(undefined2 *)&pUVar4->field_0xc0 = 0xffff;
  pUVar4->field_0xbe = 0xff;
  pUVar4->grupo_id = 0xff;
  pUVar4->selecionada = 0;
  pUVar4->field_0xaf = 0;
  *(undefined4 *)&pUVar4->field_0x104 = 0xffffffff;
  *(undefined4 *)&pUVar4->field_0x10c = 0xffffffff;
  pUVar4->field_0xf5 = 0;
  pUVar4->field_0xf6 = 0;
  pUVar4->field_0xf7 = 0;
  pUVar4->field_0xf8 = 0;
  *(undefined4 *)&pUVar4->field_0x110 = 0;
  pUVar4->field_0x94 = 1;
  *(undefined2 *)&pUVar4->field_0x4 = *(undefined2 *)&pUVar4->field_0x76;
  for (uVar2 = 0; uVar2 < pUVar4->campo_0c; uVar2 = uVar2 + 1) {
    (&pUVar4->field_0x4c)[uVar2] = 0;
    *(undefined2 *)(&pUVar4->field_0x10 + (uint)uVar2 * 2) = 0;
  }
  uVar7 = FUN_00448194(extraout_ECX,(uint)uVar6);
  iVar5 = ((uint)uVar6 * 0x44 + (int)((ulonglong)uVar7 >> 0x20)) * 4;
  if ((&tabela_unidades->tipo_id)[iVar5] == 4) {
    uVar3 = FUN_00428cc0(extraout_ECX_00,0xc);
    (&tabela_unidades->field_0xda)[iVar5] = (char)uVar3 + '\n';
  }
  if ((tabela_unidades[uVar6].tipo_id == 0x10) || (tabela_unidades[uVar6].tipo_id == 0xe)) {
    tabela_unidades[uVar6].field_0xda = 0;
  }
  FUN_004457cd();
  return;
}
