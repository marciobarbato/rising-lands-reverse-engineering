/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00443dfc, entrada 00443dfc.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00443dfc(undefined4 param_1,uint param_2)

{
  byte bVar1;
  ushort uVar2;
  bool bVar3;
  UnidadeParcial *pUVar4;
  ushort in_AX;
  ushort uVar5;
  ushort uVar6;
  uint uVar7;
  undefined4 extraout_ECX;
  int extraout_ECX_00;
  int extraout_ECX_01;
  UnidadeParcial *extraout_ECX_02;
  int extraout_ECX_03;
  UnidadeParcial *extraout_ECX_04;
  UnidadeParcial *pUVar8;
  undefined4 extraout_ECX_05;
  int extraout_ECX_06;
  int extraout_ECX_07;
  UnidadeParcial *extraout_ECX_08;
  UnidadeParcial *pUVar9;
  undefined4 extraout_ECX_09;
  undefined4 extraout_ECX_10;
  char local_2c;

  uVar7 = param_2 & 0xffff;
  pUVar9 = tabela_unidades + in_AX;
  bVar1 = (&pUVar9->field_0x4c)[uVar7];
  if (bVar1 == 0) goto LAB_00443e4d;
  if (1 < bVar1) {
    if (bVar1 == 2) {
      local_2c = (char)*(undefined2 *)(&pUVar9->field_0x10 + uVar7 * 2);
      uVar7 = FUN_004757af(uVar7,local_2c + 'B');
      if ((uVar7 & 0xffff) != 0xffff) {
        uVar6 = FUN_004473cf(extraout_ECX_09,(ushort)extraout_ECX_09);
        local_2c = (char)uVar6;
        FUN_0047605d(extraout_ECX_10,local_2c);
      }
    }
    goto LAB_00443e4d;
  }
  uVar6 = FUN_004436ab();
  if (uVar6 != 0xffff) {
    uVar5 = FUN_004473cf(extraout_ECX,(ushort)extraout_ECX);
    pUVar8 = tabela_unidades;
    if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
      bVar3 = false;
    }
    else {
      bVar3 = true;
    }
    if (bVar3) {
      tabela_unidades[uVar5].celula_destino = uVar6;
      pUVar8[uVar5].celula_passo = uVar6;
      pUVar8[uVar5].celula_atual = uVar6;
      pUVar4 = tabela_unidades;
      tabela_unidades[uVar5].celula_destino = uVar6;
      if (uVar5 == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = 0xffff;
      }
      pUVar4[uVar5].estado_caminho = 0;
      if ((tabela_unidades[uVar5].estado == 0) || (tabela_unidades[uVar5].estado == 4)) {
        bVar3 = false;
      }
      else {
        bVar3 = true;
      }
      if ((bVar3) && (tabela_unidades[uVar5].estado = 7, uVar5 == DAT_00496304)) {
        DAT_004e0f36 = (byte)uVar5 ^ (byte)DAT_00496304;
        DAT_004e0f37 = (byte)(uVar5 >> 8) ^ (byte)(DAT_00496304 >> 8);
        DAT_004e0f3c = 0;
        DAT_00496304 = 0xffff;
      }
      *(undefined2 *)&pUVar8[uVar5].field_0xc0 = 0xffff;
      uVar7 = (uint)uVar5;
      *(undefined2 *)&pUVar8[uVar5].field_0xb8 = 0xffff;
      pUVar8[uVar5].deslocamento_y = 0;
      pUVar8[uVar5].deslocamento_x = pUVar8[uVar5].deslocamento_y;
      pUVar8 = tabela_unidades;
      FUN_00442cb4(uVar7);
      pUVar8[uVar7].field_0x72 = 1;
      pUVar8 = tabela_unidades + uVar7;
      if ((pUVar8->proprietario_id != 200) && (pUVar8->proprietario_id != 4)) {
        FUN_00476851(pUVar8,(uint)(ushort)((ushort)(byte)pUVar8->field_0xf5 + pUVar8->raio_visao + 2
                                          ));
        FUN_00476cb3(extraout_ECX_03,
                     (uint)(ushort)((ushort)*(byte *)(extraout_ECX_03 + 0xf5) +
                                   (ushort)*(byte *)(extraout_ECX_03 + 0xbb)));
        pUVar8 = extraout_ECX_04;
      }
LAB_0044431b:
      FUN_0046a388(pUVar8,4);
    }
    else {
      uVar7 = FUN_00467d97((uint)uVar5 * 0x114,2);
      if ((char)uVar7 == '\0') {
        uVar2 = *(ushort *)((int)&tabela_unidades->vida + extraout_ECX_00);
        *(ushort *)((int)&tabela_unidades->vida + extraout_ECX_00) = uVar2 - uVar2 / 2;
        pUVar8 = tabela_unidades;
        *(ushort *)((int)&tabela_unidades->celula_destino + extraout_ECX_00) = uVar6;
        *(ushort *)((int)&pUVar8->celula_passo + extraout_ECX_00) = uVar6;
        *(ushort *)((int)&pUVar8->celula_atual + extraout_ECX_00) = uVar6;
        pUVar4 = tabela_unidades;
        *(ushort *)((int)&tabela_unidades->celula_destino + extraout_ECX_00) = uVar6;
        if (uVar5 == DAT_00496304) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_004e0f3c = 0;
          DAT_00496304 = 0xffff;
        }
        (&pUVar4->estado_caminho)[extraout_ECX_00] = 0;
        if ((tabela_unidades[uVar5].estado == 0) || (tabela_unidades[uVar5].estado == 4)) {
          bVar3 = false;
        }
        else {
          bVar3 = true;
        }
        if ((bVar3) && (tabela_unidades[uVar5].estado = 7, uVar5 == DAT_00496304)) {
          DAT_004e0f37 = (byte)uVar5 ^ (byte)DAT_00496304;
          DAT_004e0f36 = 0;
          DAT_004e0f3c = 0;
          DAT_00496304 = 0xffff;
        }
        *(undefined2 *)(&pUVar8->field_0xc0 + extraout_ECX_00) = 0xffff;
        uVar7 = (uint)uVar5;
        *(undefined2 *)(&pUVar8->field_0xb8 + extraout_ECX_00) = 0xffff;
        (&pUVar8->deslocamento_y)[extraout_ECX_00] = 0;
        (&pUVar8->deslocamento_x)[extraout_ECX_00] = (&pUVar8->deslocamento_y)[extraout_ECX_00];
        pUVar8 = tabela_unidades;
        FUN_00442cb4(uVar7);
        pUVar8[uVar7].field_0x72 = 1;
        pUVar8 = tabela_unidades + uVar7;
        if ((pUVar8->proprietario_id != 200) && (pUVar8->proprietario_id != 4)) {
          FUN_00476851(pUVar8,(uint)(ushort)(pUVar8->raio_visao + 2 +
                                            (ushort)(byte)pUVar8->field_0xf5));
          FUN_00476cb3(extraout_ECX_01,
                       (uint)(ushort)((ushort)*(byte *)(extraout_ECX_01 + 0xf5) +
                                     (ushort)*(byte *)(extraout_ECX_01 + 0xbb)));
          pUVar8 = extraout_ECX_02;
        }
        goto LAB_0044431b;
      }
      if (((&tabela_unidades->estado)[extraout_ECX_00] == 0) ||
         ((&tabela_unidades->estado)[extraout_ECX_00] == 4)) {
        bVar3 = false;
      }
      else {
        bVar3 = true;
      }
      if ((bVar3) && (tabela_unidades[uVar5].estado = 0, uVar5 == DAT_00496304)) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = 0xffff;
      }
    }
    if (tabela_unidades[uVar5].tipo_id == 9) {
      FUN_004829c8((uint)uVar5,0x42);
    }
  }
  switch(tabela_unidades[in_AX].tipo_id) {
  case 0xb:
  case 0xc:
  case 0xd:
  case 0xe:
  case 0xf:
  case 0x10:
  case 0x11:
    bVar3 = true;
    break;
  default:
    bVar3 = false;
  }
  if (bVar3) {
    for (uVar6 = 0; uVar6 < pUVar9->campo_0c; uVar6 = uVar6 + 1) {
      if ((&pUVar9->field_0x4c)[uVar6] == '\x01') {
        bVar1 = tabela_unidades[*(ushort *)(&pUVar9->field_0x10 + (uint)uVar6 * 2)].tipo_id;
        bVar3 = true;
        if (bVar1 < 0xe) {
          if (bVar1 < 6) {
            if ((bVar1 < 3) || (3 < bVar1)) goto LAB_0044440c;
          }
          else if ((bVar1 < 9) || (bVar1 < 0xb)) {
LAB_0044440c:
            bVar3 = true;
            goto LAB_0044440e;
          }
LAB_00444402:
          bVar3 = false;
        }
        else {
          if ((bVar1 < 0xf) || (bVar1 < 0x12)) goto LAB_00444402;
          if ((bVar1 < 0x13) || ((bVar1 < 0x17 || (bVar1 < 0x19)))) goto LAB_0044440c;
          if (bVar1 == 0x19) goto LAB_00444402;
        }
LAB_0044440e:
        if (bVar3) {
          bVar3 = true;
          goto LAB_00444418;
        }
      }
    }
    bVar3 = false;
LAB_00444418:
    if (!bVar3) {
      FUN_0044357c();
      FUN_00472648(extraout_ECX_05);
      FUN_00457058();
      pUVar9->proprietario_id = 200;
      FUN_00442cb4(tabela_unidades);
      *(undefined1 *)(extraout_ECX_06 + 0x72 + (uint)in_AX * 0x114) = 1;
      pUVar9 = tabela_unidades + in_AX;
      if ((pUVar9->proprietario_id != 200) && (pUVar9->proprietario_id != 4)) {
        FUN_00476851(pUVar9,(uint)(ushort)((ushort)(byte)pUVar9->field_0xf5 + pUVar9->raio_visao + 2
                                          ));
        FUN_00476cb3(extraout_ECX_07,
                     (uint)(ushort)((ushort)*(byte *)(extraout_ECX_07 + 0xf5) +
                                   (ushort)*(byte *)(extraout_ECX_07 + 0xbb)));
        pUVar9 = extraout_ECX_08;
      }
      FUN_0046a388(pUVar9,4);
    }
  }
LAB_00443e4d:
  FUN_00445f27();
  return;
}
