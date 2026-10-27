/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044ea78, entrada 0044ea78.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0044ea78(undefined4 param_1)

{
  ushort *puVar1;
  bool bVar2;
  UnidadeParcial *pUVar3;
  ushort uVar4;
  uint in_EAX;
  int iVar5;
  undefined4 uVar6;
  uint uVar7;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  char cVar8;
  UnidadeParcial *pUVar9;
  uint uVar10;
  short sVar11;
  undefined8 uVar12;

  pUVar3 = tabela_unidades;
  uVar10 = in_EAX & 0xffff;
  bVar2 = false;
  sVar11 = (short)in_EAX;
  switch(tabela_unidades[uVar10].field_0x89) {
  case 0:
    bVar2 = *(ushort *)&tabela_unidades[uVar10].field_0x70 + 1 <=
            (uint)tabela_unidades[uVar10].campo_0c;
    if (!bVar2) {
      tabela_unidades[uVar10].field_0x89 = 1;
      pUVar3[uVar10].field_0x8b = 10;
      pUVar3[uVar10].field_0xa4 = bVar2;
      FUN_0044f29a();
      return;
    }
    if (tabela_unidades[uVar10].celula_destino != tabela_unidades[uVar10].celula_atual) {
LAB_0044eaf3:
      FUN_0044930c();
      FUN_0044f29a();
      return;
    }
    uVar12 = FUN_00476038(param_1,(uint)*(ushort *)&tabela_unidades[uVar10].field_0x84);
    if (((uint)uVar12 & 0xff) == (uint)((ulonglong)uVar12 >> 0x20)) {
      pUVar3[uVar10].field_0x89 = 1;
      pUVar3[uVar10].field_0x8b = 10;
      pUVar3[uVar10].field_0xa4 = 0;
      FUN_0044f29a();
      return;
    }
    uVar4 = FUN_00477b74(pUVar3[uVar10].field_0x84 + 0x42,5);
    if (uVar4 == 0xffff) goto LAB_0044ebbf;
    pUVar9 = tabela_unidades + (in_EAX & 0xffff);
    pUVar9->celula_destino = uVar4;
joined_r0x0044f01b:
    if (sVar11 == DAT_00496304) {
      DAT_004e0f3c = 0;
      DAT_004e0f37 = 0;
      DAT_004e0f36 = 0;
      DAT_00496304 = -1;
    }
    goto LAB_0044ebab;
  case 1:
    uVar7 = *(ushort *)&tabela_unidades[uVar10].field_0x70 + 1;
    if (tabela_unidades[uVar10].campo_0c < uVar7) {
LAB_0044ed45:
      bVar2 = true;
    }
    else {
      tabela_unidades[uVar10].field_0x8b = tabela_unidades[uVar10].field_0x8b + -1;
      if (pUVar3[uVar10].field_0x8b == '\0') {
        uVar12 = FUN_00476662(param_1,uVar7);
        puVar1 = &pUVar3[uVar10].campo_0a;
        uVar4 = *puVar1;
        *(short *)&pUVar3[uVar10].field_0x70 = *(short *)&pUVar3[uVar10].field_0x70 + 1;
        *(undefined1 *)(uVar4 + 0x42 + (int)puVar1) = 2;
        *(ushort *)(&pUVar3[uVar10].field_0x10 + (uint)uVar4 * 2) = (ushort)(byte)uVar12;
        *puVar1 = *puVar1 + 1;
        cVar8 = pUVar3[uVar10].field_0x84;
        FUN_004704dc((uint)pUVar3[uVar10].celula_atual,0);
        FUN_004704dc(5,0);
        uVar4 = FUN_00477b74(cVar8 + 0x42,5);
        if ((uVar4 == 0xffff) ||
           ((uint)pUVar3[uVar10].campo_0c < *(ushort *)&pUVar3[uVar10].field_0x70 + 1))
        goto LAB_0044ed45;
        pUVar3[uVar10].field_0xa4 = 0;
        pUVar9 = tabela_unidades;
        tabela_unidades[in_EAX & 0xffff].celula_destino = uVar4;
        if (sVar11 == DAT_00496304) {
          DAT_004e0f36 = 0;
          DAT_004e0f3c = 0;
          DAT_004e0f37 = 0;
          DAT_00496304 = -1;
        }
        pUVar9[in_EAX & 0xffff].estado_caminho = 0;
        pUVar3[uVar10].field_0x89 = 0;
      }
    }
    if (!bVar2) {
switchD_0044d86e_default:
      return;
    }
    if (pUVar3[uVar10].field_0x82 != '\x02') {
      if (pUVar3[uVar10].field_0x82 != '\x01') {
        return;
      }
      pUVar3[uVar10].field_0x89 = 2;
      pUVar9 = tabela_unidades + (in_EAX & 0xffff);
      pUVar9->celula_destino = *(ushort *)&pUVar3[uVar10].field_0x80;
      if (sVar11 == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = -1;
      }
      goto LAB_0044ebab;
    }
    *(undefined2 *)&pUVar3[uVar10].field_0xc0 = *(undefined2 *)&pUVar3[uVar10].field_0x80;
    if (*(short *)&pUVar3[uVar10].field_0xc0 == -1) {
LAB_0044ebbf:
      FUN_004457d3();
      FUN_0044f29a();
      return;
    }
    uVar4 = FUN_0041aee2();
    pUVar3[uVar10].field_0x89 = 2;
    pUVar9 = tabela_unidades + (in_EAX & 0xffff);
    pUVar9->celula_destino = uVar4;
    break;
  case 2:
    if (tabela_unidades[uVar10].field_0x82 == '\x02') {
      uVar12 = FUN_0041a70b(param_1,uVar10 * 0x114);
      if ((char)uVar12 != '\0') goto LAB_0044ebbf;
      if (((*(int *)&pUVar3[uVar10].field_0x83 >> 0x18 != 0) ||
          (*(int *)&pUVar3[uVar10].field_0x84 >> 0x18 != 0)) ||
         (iVar5 = FUN_0042381f(extraout_ECX,(uint)pUVar3[uVar10].celula_atual), (char)iVar5 == '\0')
         ) goto LAB_0044eaf3;
LAB_0044eec3:
      pUVar3[uVar10].field_0x89 = 3;
LAB_0044eeca:
      pUVar3[uVar10].field_0x8b = 10;
      FUN_0044f29a();
      return;
    }
    if (tabela_unidades[uVar10].field_0x82 != '\x01') {
      return;
    }
    if (tabela_unidades[uVar10].celula_atual != tabela_unidades[uVar10].celula_destino)
    goto LAB_0044eaf3;
    uVar7 = FUN_00479555(*(ushort *)&tabela_unidades[uVar10].field_0x80 >> 8,
                         tabela_unidades[uVar10].celula_atual >> 8);
    if (0x10 < uVar7) {
      pUVar9 = tabela_unidades + uVar10;
      pUVar9->celula_destino = *(ushort *)&pUVar3[uVar10].field_0x80;
      goto joined_r0x0044f01b;
    }
    uVar6 = FUN_00475763(extraout_ECX_00,pUVar3[uVar10].field_0x84 + 'B');
    if ((char)uVar6 != '\0') goto LAB_0044eec3;
    uVar7 = FUN_00475bfe(extraout_ECX_01,pUVar3[uVar10].field_0x84 + 'B');
    if ((uVar7 & 0xffff) == 0xffff) {
      return;
    }
    pUVar9 = tabela_unidades + uVar10;
    pUVar9->celula_destino = (ushort)uVar7;
    break;
  case 3:
    uVar12 = FUN_0041a70b(param_1,uVar10 * 0x114);
    uVar6 = extraout_ECX_02;
    if ((char)uVar12 != '\0') {
      FUN_004457d3();
      uVar6 = extraout_ECX_03;
    }
    cVar8 = pUVar3[uVar10].field_0x8b + -1;
    pUVar3[uVar10].field_0x8b = cVar8;
    if (cVar8 != '\0') {
      return;
    }
    pUVar3[uVar10].field_0x8b = 10;
    uVar7 = FUN_004471b8(uVar6,'\x02');
    if ((uVar7 & 0xffff) != 0) {
      if (pUVar3[uVar10].field_0x82 == '\x02') {
        FUN_0042340f((uint)*(ushort *)&pUVar3[uVar10].field_0x80,1);
        FUN_004472ea(extraout_ECX_05,'\x02');
      }
      else {
        if (pUVar3[uVar10].field_0x82 != '\x01') {
          return;
        }
        FUN_004438d8(extraout_ECX_04,2);
      }
      goto LAB_0044eeca;
    }
    if (*(short *)&pUVar3[uVar10].field_0xb2 == -1) {
      if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
         (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
        bVar2 = false;
      }
      else {
        bVar2 = true;
      }
      if (!bVar2) {
        return;
      }
      tabela_unidades[in_EAX & 0xffff].estado = 7;
      if (sVar11 == DAT_00496304) {
        uVar4 = (ushort)DAT_00496304 >> 8;
        DAT_00496304 = 0xffff;
        DAT_004e0f36 = (byte)(in_EAX >> 8) ^ (byte)uVar4;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        return;
      }
      return;
    }
    uVar4 = FUN_00477b74(pUVar3[uVar10].field_0x84 + 0x42,5);
    if (uVar4 == 0xffff) {
      if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
         (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
        bVar2 = false;
      }
      else {
        bVar2 = true;
      }
      if (!bVar2) {
        return;
      }
      tabela_unidades[in_EAX & 0xffff].estado = 7;
      if (sVar11 == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = 0xffff;
        FUN_0044f29a();
        return;
      }
      return;
    }
    if (uVar4 == *(ushort *)&pUVar3[uVar10].field_0x80) {
      return;
    }
    pUVar3[uVar10].field_0x89 = 0;
    pUVar9 = tabela_unidades + (in_EAX & 0xffff);
    pUVar9->celula_destino = uVar4;
    if (sVar11 == DAT_00496304) {
      DAT_004e0f36 = 0;
      DAT_004e0f37 = 0;
      DAT_00496304 = -1;
      DAT_004e0f3c = 0;
    }
    goto LAB_0044ebab;
  default:
    goto switchD_0044d86e_default;
  }
  if (sVar11 == DAT_00496304) {
    DAT_004e0f3c = 0;
    DAT_004e0f37 = 0;
    DAT_004e0f36 = 0;
    DAT_00496304 = -1;
  }
LAB_0044ebab:
  pUVar9->estado_caminho = 0;
  FUN_0044f29a();
  return;
}
