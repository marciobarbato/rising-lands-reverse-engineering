/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00452cc8, entrada 00452cc8.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00452cc8(undefined4 param_1)

{
  byte bVar1;
  UnidadeParcial *pUVar2;
  ushort in_AX;
  uint uVar3;
  undefined4 uVar4;
  int iVar5;
  short extraout_CX;
  ushort uVar6;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  ushort uVar7;
  undefined4 extraout_EDX;
  UnidadeParcial *pUVar8;
  bool bVar9;
  undefined8 uVar10;

  pUVar8 = tabela_unidades + in_AX;
  if (pUVar8->field_0x72 == '\0') {
    return;
  }
  switch(pUVar8->tipo_id) {
  case 0xb:
  case 0xc:
  case 0xd:
  case 0xe:
  case 0xf:
  case 0x10:
  case 0x11:
    bVar9 = true;
    break;
  default:
    bVar9 = false;
  }
  if (bVar9) {
    return;
  }
  uVar3 = FUN_00428cc0(CONCAT22((short)((uint)param_1 >> 0x10),
                                *(undefined2 *)(&DAT_004965dc + (uint)pUVar8->tipo_id * 0x32)) +
                       (uint)(byte)pUVar8->field_0xf8,0);
  uVar7 = *(short *)&pUVar8->field_0x74 + 1;
  uVar6 = extraout_CX + (short)uVar3;
  *(ushort *)&pUVar8->field_0x74 = uVar7;
  pUVar2 = tabela_unidades;
  if (uVar7 < uVar6) {
    return;
  }
  if (*(short *)&pUVar8->field_0x4 != 0) {
    *(undefined2 *)&pUVar8->field_0x74 = 0;
    *(short *)&pUVar8->field_0x4 = *(short *)&pUVar8->field_0x4 + -1;
    return;
  }
  if (pUVar8->proprietario_id != DAT_00508041) goto LAB_00452e2f;
  bVar1 = tabela_unidades[in_AX].tipo_id;
  if (bVar1 < 3) {
    bVar9 = bVar1 == 0;
LAB_00452daf:
    if (bVar9) goto LAB_00452d7e;
LAB_00452db1:
    bVar9 = true;
  }
  else {
    if (3 < bVar1) {
      if (bVar1 < 10) goto LAB_00452db1;
      if (10 < bVar1) {
        bVar9 = bVar1 == 0x19;
        goto LAB_00452daf;
      }
    }
LAB_00452d7e:
    bVar9 = false;
  }
  if ((bVar9) && (uVar6 == *(ushort *)&pUVar8->field_0x74)) {
    uVar3 = (uint)in_AX;
    uVar4 = FUN_004766f0(uVar3,(uint)DAT_00508041);
    if ((char)uVar4 != '\0') {
      uVar10 = FUN_00440c5d(extraout_ECX,extraout_EDX);
      pUVar2[uVar3].field_0xf9 = 0;
      if (*(int *)&pUVar2[uVar3].field_0x104 == -1) {
        FUN_0048aa79(0,(uint)pUVar2[uVar3].tipo_id << 0x10 | 0xc00,(uint)uVar10);
      }
    }
  }
LAB_00452e2f:
  iVar5 = FUN_004471b8(&tabela_unidades[in_AX].campo_0a,'\x02');
  if ((short)iVar5 == 0) {
    if (pUVar8->vida < 0x15) {
      pUVar8->vida = 0;
      FUN_00444938();
    }
    else {
      pUVar8->vida = pUVar8->vida - 0x14;
      *(ushort *)&pUVar8->field_0x74 = *(ushort *)(&DAT_004965dc + (uint)pUVar8->tipo_id * 0x32) / 2
      ;
    }
  }
  else {
    FUN_004472ea(extraout_ECX_00,'\x02');
    *(undefined2 *)&pUVar8->field_0x74 = 0;
    *(undefined2 *)&pUVar8->field_0x4 = *(undefined2 *)&pUVar8->field_0x76;
  }
  return;
}
