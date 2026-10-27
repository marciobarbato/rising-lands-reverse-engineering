/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00445b10, entrada 00445b10.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00445b10(undefined4 param_1,undefined4 param_2)

{
  bool bVar1;
  UnidadeParcial *pUVar2;
  short sVar3;
  ushort uVar4;
  uint in_EAX;
  int iVar5;
  UnidadeParcial *pUVar6;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_ECX_01;
  uint extraout_ECX_02;
  uint uVar7;
  uint extraout_ECX_03;
  uint extraout_ECX_04;
  uint uVar8;
  undefined2 extraout_var;
  uint uVar9;
  undefined2 uVar10;
  undefined8 uVar11;

  uVar9 = in_EAX & 0xffff;
  uVar11 = FUN_0041a4f4(in_EAX,param_2);
  pUVar2 = tabela_unidades;
  uVar8 = (uint)(byte)uVar11;
  uVar10 = (undefined2)param_2;
  if ((uVar8 == 8) && (tabela_unidades[uVar9].tipo_id != 9)) {
    iVar5 = FUN_0041d057(extraout_ECX);
    *(ushort *)&pUVar2[uVar9].field_0xb2 = (ushort)iVar5;
    pUVar6 = tabela_unidades;
    tabela_unidades[uVar9].celula_destino = (ushort)iVar5;
    if ((short)extraout_ECX_00 == DAT_00496304) {
      DAT_004e0f36 = 0;
      DAT_004e0f37 = 0;
      DAT_004e0f3c = 0;
      DAT_00496304 = -1;
    }
    pUVar6[uVar9].estado_caminho = 0;
    *(undefined2 *)&pUVar2[uVar9].field_0xc0 = uVar10;
    if ((tabela_unidades[extraout_ECX_00 & 0xffff].estado == 0) ||
       (tabela_unidades[extraout_ECX_00 & 0xffff].estado == 4)) {
      bVar1 = false;
    }
    else {
      bVar1 = true;
    }
    if ((bVar1) &&
       (tabela_unidades[extraout_ECX_00 & 0xffff].estado = 0x15,
       (short)extraout_ECX_00 == DAT_00496304)) {
      DAT_004e0f36 = 0;
      DAT_004e0f37 = 0;
      DAT_004e0f3c = 0;
      DAT_00496304 = -1;
    }
  }
  else {
    uVar7 = extraout_ECX;
    if (uVar8 == 0xe) {
      switch(tabela_unidades[extraout_ECX & 0xffff].tipo_id) {
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
      if (bVar1) {
        uVar11 = FUN_0041a6ec(extraout_ECX,0xe);
        uVar8 = (uint)((ulonglong)uVar11 >> 0x20);
        uVar7 = extraout_ECX_01;
        if (((uint)uVar11 & 0xff) != 4) {
          iVar5 = FUN_0041d057(extraout_ECX_01);
          *(ushort *)&pUVar2[uVar9].field_0xb2 = (ushort)iVar5;
          pUVar6 = tabela_unidades;
          tabela_unidades[extraout_ECX_01 & 0xffff].celula_destino = (ushort)iVar5;
          if ((short)extraout_ECX_02 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
          }
          pUVar6[extraout_ECX_01 & 0xffff].estado_caminho = 0;
          *(undefined2 *)&pUVar2[uVar9].field_0xc0 = uVar10;
          if ((tabela_unidades[extraout_ECX_02 & 0xffff].estado == 0) ||
             (tabela_unidades[extraout_ECX_02 & 0xffff].estado == 4)) {
            bVar1 = false;
          }
          else {
            bVar1 = true;
          }
          if (!bVar1) {
            return;
          }
          tabela_unidades[extraout_ECX_02 & 0xffff].estado = 0xd;
          if ((short)extraout_ECX_02 == DAT_00496304) {
            DAT_00496304 = 0xffff;
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            return;
          }
          return;
        }
      }
    }
    if ((uVar8 == 0x12) && (tabela_unidades[uVar7 & 0xffff].tipo_id == 0x10)) {
      sVar3 = FUN_0041aee2();
      *(ushort *)&pUVar2[uVar9].field_0xb2 = sVar3 + 1U;
      pUVar6 = tabela_unidades + (uVar7 & 0xffff);
      pUVar6->celula_destino = sVar3 + 1U;
      uVar8 = extraout_ECX_03;
      if ((short)extraout_ECX_03 == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f3c = 0;
        DAT_004e0f37 = 0;
        DAT_00496304 = -1;
      }
    }
    else {
      uVar4 = FUN_0041aee2();
      pUVar6 = tabela_unidades + CONCAT22(extraout_var,(short)extraout_ECX_04);
      pUVar6->celula_destino = uVar4;
      uVar8 = extraout_ECX_04;
      if ((short)extraout_ECX_04 == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_00496304 = -1;
        DAT_004e0f3c = 0;
      }
    }
    pUVar6->estado_caminho = 0;
    *(undefined2 *)&pUVar2[uVar9].field_0xc0 = uVar10;
    if ((tabela_unidades[uVar8 & 0xffff].estado == 0) ||
       (tabela_unidades[uVar8 & 0xffff].estado == 4)) {
      bVar1 = false;
    }
    else {
      bVar1 = true;
    }
    if ((bVar1) && (tabela_unidades[uVar8 & 0xffff].estado = 0xd, (short)uVar8 == DAT_00496304)) {
      DAT_004e0f36 = 0;
      DAT_004e0f37 = 0;
      DAT_004e0f3c = 0;
      DAT_00496304 = -1;
    }
  }
  return;
}
