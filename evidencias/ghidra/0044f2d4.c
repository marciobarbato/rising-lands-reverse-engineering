/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044f2d4, entrada 0044f2d4.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_0044f2d4(undefined4 param_1,undefined4 param_2)

{
  ushort *puVar1;
  char cVar2;
  bool bVar3;
  bool bVar4;
  UnidadeParcial *pUVar5;
  ushort in_AX;
  ushort uVar6;
  UnidadeParcial *pUVar7;
  uint uVar8;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined2 uVar9;
  byte bVar10;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  uint uVar11;
  undefined8 uVar12;
  longlong lVar13;

  pUVar5 = tabela_unidades;
  uVar11 = (uint)in_AX;
  uVar8 = uVar11 * 0x114 & 0xffff0000;
  bVar3 = false;
  bVar4 = false;
  switch(tabela_unidades[uVar11].tipo_id) {
  case 0xb:
  case 0xc:
  case 0xd:
  case 0xe:
  case 0xf:
  case 0x10:
  case 0x11:
    uVar8 = 0;
    bVar3 = true;
    break;
  default:
  }
  if ((!bVar3) || (tabela_unidades[uVar11].field_0x82 == '\x01')) {
    pUVar7 = (UnidadeParcial *)FUN_0044ea78(param_1);
    goto switchD_0044d86e_default;
  }
  pUVar7 = (UnidadeParcial *)CONCAT31((int3)(uVar8 >> 8),tabela_unidades[uVar11].field_0x89);
  uVar9 = (undefined2)((uint)param_1 >> 0x10);
  switch(tabela_unidades[uVar11].field_0x89) {
  case 0:
    if (tabela_unidades[uVar11].celula_destino != tabela_unidades[uVar11].celula_atual) {
LAB_0044f351:
      pUVar7 = (UnidadeParcial *)FUN_0044930c();
      goto switchD_0044d86e_default;
    }
    uVar12 = FUN_00476038(CONCAT22(uVar9,tabela_unidades[uVar11].celula_atual),
                          (uint)*(ushort *)&tabela_unidades[uVar11].field_0x84);
    pUVar7 = (UnidadeParcial *)((uint)uVar12 & 0xff);
    if (pUVar7 == (UnidadeParcial *)((ulonglong)uVar12 >> 0x20)) {
      pUVar5[uVar11].field_0x89 = 1;
      pUVar5[uVar11].field_0x8b = 10;
      pUVar5[uVar11].quadro_movimento = 0;
      goto switchD_0044d86e_default;
    }
    uVar6 = FUN_00477b74(pUVar5[uVar11].field_0x84 + 0x42,10);
    pUVar7 = (UnidadeParcial *)(uint)uVar6;
    if (pUVar7 == (UnidadeParcial *)0xffff) goto switchD_0044d86e_default;
    pUVar7 = tabela_unidades + in_AX;
    pUVar7->celula_destino = uVar6;
    if (in_AX != DAT_00496304) break;
LAB_0044f406:
    DAT_004e0f3c = 0;
    DAT_004e0f37 = 0;
    DAT_004e0f36 = 0;
    DAT_00496304 = 0xffff;
    break;
  case 1:
    uVar8 = *(ushort *)&tabela_unidades[uVar11].field_0x70 + 1;
    bVar3 = uVar8 <= tabela_unidades[uVar11].campo_0c;
    pUVar7 = (UnidadeParcial *)(uint)CONCAT11((char)(tabela_unidades[uVar11].campo_0c >> 8),bVar3);
    if (bVar3) {
      tabela_unidades[uVar11].field_0x8b = tabela_unidades[uVar11].field_0x8b + -1;
      pUVar7 = (UnidadeParcial *)(uint)(byte)pUVar5[uVar11].field_0x8b;
      if (pUVar7 == (UnidadeParcial *)0x0) {
        uVar12 = FUN_00476662(CONCAT22(uVar9,(ushort)(byte)param_1),uVar8);
        puVar1 = &pUVar5[uVar11].campo_0a;
        *(short *)&pUVar5[uVar11].field_0x70 = *(short *)&pUVar5[uVar11].field_0x70 + 1;
        uVar6 = *puVar1;
        *(undefined1 *)(uVar6 + 0x42 + (int)puVar1) = 2;
        *(short *)(&pUVar5[uVar11].field_0x10 + (uint)uVar6 * 2) =
             (short)CONCAT31((int3)((uint)extraout_ECX >> 8),(char)uVar12);
        *puVar1 = *puVar1 + 1;
        cVar2 = pUVar5[uVar11].field_0x84;
        FUN_004704dc(5,0);
        FUN_004704dc(extraout_ECX_00,0);
        uVar6 = FUN_00477b74(cVar2 + 0x42,10);
        pUVar7 = (UnidadeParcial *)(uint)uVar6;
        if (pUVar7 == (UnidadeParcial *)0xffff) goto LAB_0044f54d;
        pUVar5[uVar11].quadro_movimento = 0;
        pUVar7 = tabela_unidades + in_AX;
        pUVar7->celula_destino = uVar6;
        if (in_AX == DAT_00496304) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_004e0f3c = 0;
          DAT_00496304 = 0xffff;
        }
        pUVar7->estado_caminho = 0;
        pUVar5[uVar11].field_0x89 = 0;
      }
    }
    else {
LAB_0044f54d:
      bVar4 = true;
    }
    if (!bVar4) goto switchD_0044d86e_default;
    pUVar7 = (UnidadeParcial *)(uint)(byte)pUVar5[uVar11].field_0x82;
    if (pUVar7 == (UnidadeParcial *)0x2) {
      *(undefined2 *)&pUVar5[uVar11].field_0xc0 = *(undefined2 *)&pUVar5[uVar11].field_0x80;
      if (*(short *)&pUVar5[uVar11].field_0xc0 == -1) {
        pUVar7 = tabela_unidades + in_AX;
        pUVar7->celula_destino = pUVar5[uVar11].celula_passo;
        if (in_AX == DAT_00496304) goto LAB_0044f406;
      }
      else {
        FUN_004237df();
        uVar12 = FUN_00423b27(extraout_ECX_01,extraout_EDX);
        pUVar5[uVar11].field_0x89 = 2;
        pUVar7 = tabela_unidades + in_AX;
        pUVar7->celula_destino = (short)uVar12 - 0xfe;
        if (in_AX == DAT_00496304) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_004e0f3c = 0;
          DAT_00496304 = 0xffff;
        }
      }
    }
    else {
      if (pUVar7 != (UnidadeParcial *)0x1) goto switchD_0044d86e_default;
      pUVar5[uVar11].field_0x89 = 2;
      pUVar7 = tabela_unidades + in_AX;
      pUVar7->celula_destino = *(ushort *)&pUVar5[uVar11].field_0x80;
      if (in_AX == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f3c = 0;
        DAT_004e0f37 = 0;
        DAT_00496304 = 0xffff;
      }
    }
    break;
  case 2:
    if (tabela_unidades[uVar11].celula_destino != tabela_unidades[uVar11].celula_atual)
    goto LAB_0044f351;
    pUVar7 = (UnidadeParcial *)(uint)(byte)tabela_unidades[uVar11].field_0x82;
    tabela_unidades[uVar11].field_0x89 = 3;
    if (pUVar7 == (UnidadeParcial *)0x2) {
      pUVar5[uVar11].direcao_desejada = 9;
    }
    goto LAB_0044f6e6;
  case 3:
    pUVar7 = (UnidadeParcial *)(uint)tabela_unidades[uVar11].direcao_desejada;
    if (tabela_unidades[uVar11].direcao_desejada != tabela_unidades[uVar11].orientacao_atual) {
      uVar12 = FUN_00448599(param_1,param_2);
      pUVar7 = (UnidadeParcial *)uVar12;
      goto switchD_0044d86e_default;
    }
    if (tabela_unidades[uVar11].field_0x82 == '\x02') {
      FUN_0041a65c(param_1,1);
      lVar13 = FUN_00420c7c(extraout_ECX_02,extraout_EDX_00);
      pUVar7 = (UnidadeParcial *)lVar13;
      if ((char)lVar13 == '\0') goto switchD_0044d86e_default;
      pUVar5[uVar11].field_0x89 = 4;
LAB_0044f744:
      pUVar5[uVar11].field_0x8b = 0x32;
      goto switchD_0044d86e_default;
    }
    tabela_unidades[uVar11].field_0x89 = 4;
LAB_0044f6e6:
    pUVar5[uVar11].field_0x8b = 10;
    goto switchD_0044d86e_default;
  case 4:
    uVar8 = FUN_004471b8(&tabela_unidades[uVar11].campo_0a,'\x02');
    if ((uVar8 & 0xffff) != 0) {
      bVar10 = pUVar5[uVar11].field_0x8b - 1;
      pUVar7 = (UnidadeParcial *)(uint)bVar10;
      pUVar5[uVar11].field_0x8b = bVar10;
      if (pUVar7 != (UnidadeParcial *)0x0) goto switchD_0044d86e_default;
      FUN_004472ea(extraout_ECX_03,'\x02');
      if (pUVar5[uVar11].field_0x82 == '\x02') {
        pUVar7 = (UnidadeParcial *)FUN_0042340f((uint)*(ushort *)&pUVar5[uVar11].field_0x80,1);
        goto LAB_0044f744;
      }
      pUVar7 = (UnidadeParcial *)FUN_004438d8(extraout_ECX_04,2);
      goto LAB_0044f6e6;
    }
    if (pUVar5[uVar11].field_0x82 == '\x02') {
      FUN_0041a65c(extraout_ECX_03,0);
      FUN_004237ff();
    }
    *(undefined2 *)&pUVar5[uVar11].field_0xc0 = 0xffff;
    pUVar5[uVar11].field_0x89 = 0;
    pUVar7 = tabela_unidades + in_AX;
    pUVar7->celula_destino = *(ushort *)&pUVar5[uVar11].field_0xb2;
    if (in_AX == DAT_00496304) {
      DAT_004e0f36 = 0;
      DAT_004e0f37 = 0;
      DAT_00496304 = 0xffff;
      DAT_004e0f3c = 0;
    }
    break;
  default:
    goto switchD_0044d86e_default;
  }
  pUVar7->estado_caminho = 0;
switchD_0044d86e_default:
  return CONCAT44(param_2,pUVar7);
}
