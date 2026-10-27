/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0045315f, entrada 0045315f.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_0045315f(void)

{
  UnidadeParcial *pUVar1;
  short sVar2;
  undefined2 uVar3;
  undefined2 uVar4;
  UnidadeParcial *pUVar5;
  ushort in_AX;
  ushort uVar6;
  undefined2 uVar7;
  uint uVar8;
  int extraout_ECX;
  int extraout_ECX_00;
  int extraout_ECX_01;
  int extraout_ECX_02;
  int extraout_ECX_03;
  int extraout_ECX_04;
  int extraout_ECX_05;
  byte bVar9;
  undefined2 extraout_DX;
  int extraout_EDX;
  int extraout_EDX_00;
  int extraout_EDX_01;
  int extraout_EDX_02;
  byte *pbVar10;
  int extraout_EDX_03;
  int iVar11;
  int iVar12;
  undefined2 local_38 [4];
  uint local_30;
  undefined1 local_28;
  undefined1 local_24;
  byte local_20;
  byte local_1c;

  pUVar5 = tabela_unidades;
  pUVar1 = tabela_unidades + in_AX;
  uVar6 = *(ushort *)&pUVar1->field_0xa0;
  if (uVar6 < 0xd) {
    if (uVar6 < 5) {
      if (uVar6 != 0) {
        if (uVar6 < 2) {
          FUN_00445a36(pUVar1,pUVar1->field_0xb7);
          return;
        }
        if (uVar6 < 4) goto LAB_00453232;
      }
    }
    else {
      if (uVar6 < 6) {
        local_28 = pUVar1->field_0x82;
        uVar3 = *(undefined2 *)&pUVar1->field_0x80;
        local_20 = pUVar1->field_0x84;
        if (pUVar1->tipo_id == 7) {
          uVar6 = *(ushort *)&pUVar1->field_0xb2;
          FUN_0044357c();
          pUVar1 = tabela_unidades;
          pbVar10 = &pUVar5->proprietario_id + extraout_ECX_03 * 4;
          tabela_unidades[in_AX].celula_destino =
               CONCAT11((char)(uVar6 - 0x100 >> 8) + '\x01',(char)(uVar6 - 0x100));
          if (in_AX == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f3c = 0;
            DAT_004e0f37 = 0;
            DAT_00496304 = 0xffff;
          }
          pUVar1[in_AX].estado_caminho = 0;
          pbVar10[0x89] = 0;
          pbVar10[2] = 5;
        }
        else {
          uVar6 = *(ushort *)&pUVar1->field_0xb2;
          FUN_0044357c();
          pUVar1 = tabela_unidades;
          pbVar10 = &pUVar5->proprietario_id + extraout_ECX_04 * 4;
          tabela_unidades[in_AX].celula_destino = uVar6;
          if (in_AX == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = 0xffff;
          }
          pUVar1[in_AX].estado_caminho = 0;
          pbVar10[0x89] = 0;
          pbVar10[2] = 5;
        }
        pbVar10[0x82] = 0;
        *(ushort *)(pbVar10 + 0xb2) = uVar6;
        pUVar1 = tabela_unidades;
        *(undefined2 *)&tabela_unidades[in_AX].field_0x80 = uVar3;
        pUVar1[in_AX].field_0x82 = local_28;
        *(ushort *)&pUVar1[in_AX].field_0x84 = (ushort)local_20;
        return;
      }
      if (6 < uVar6) {
        if (uVar6 < 8) {
LAB_00453232:
          pUVar1->estado = 2;
          pUVar5 = tabela_unidades;
          tabela_unidades[in_AX].celula_destino = *(ushort *)&pUVar1->field_0xa2;
          if (in_AX == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = 0xffff;
          }
          pUVar5[in_AX].estado_caminho = 0;
          return;
        }
        if (uVar6 == 0xb) goto LAB_00453293;
      }
    }
  }
  else {
    if (uVar6 < 0xe) {
      if (*(ushort *)&pUVar1->field_0xc0 != 0xffff) {
        FUN_00445b10(pUVar1,(uint)*(ushort *)&pUVar1->field_0xc0);
        return;
      }
      uVar6 = *(ushort *)&pUVar1->field_0xb8;
      if (uVar6 == 0xffff) {
        return;
      }
      pUVar1->celula_destino = tabela_unidades[uVar6].celula_atual;
      if (in_AX == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = 0xffff;
      }
      pUVar1->estado_caminho = 0;
      *(undefined2 *)&pUVar1->field_0xc0 = 0xffff;
      pUVar1->estado = 0xd;
      *(ushort *)&pUVar1->field_0xb8 = uVar6;
      return;
    }
    if (uVar6 < 0x11) {
      if (0xe < uVar6) {
        if (0xf < uVar6) {
          uVar3 = *(undefined2 *)&pUVar1->field_0xb2;
          FUN_0044357c();
          pUVar1 = tabela_unidades;
          *(undefined2 *)((int)&tabela_unidades->celula_destino + extraout_EDX_03) = uVar3;
          if (in_AX == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f3c = 0;
            DAT_004e0f37 = 0;
            DAT_00496304 = 0xffff;
          }
          (&pUVar1->estado_caminho)[extraout_EDX_03] = 0;
          *(undefined1 *)(extraout_ECX_05 + 2) = 0x10;
          *(undefined1 *)(extraout_ECX_05 + 0x89) = 0;
          *(undefined2 *)(extraout_ECX_05 + 0xb2) = uVar3;
          return;
        }
LAB_00453293:
        if (pUVar1->tipo_id != 7) {
          if (pUVar1->tipo_id != 6) {
            return;
          }
          local_30 = (uint)*(ushort *)&pUVar1->field_0xc0;
          uVar8 = (uint)in_AX;
          FUN_0044357c();
          pUVar1 = tabela_unidades;
          uVar6 = tabela_unidades[local_30 & 0xffff].celula_passo;
          tabela_unidades[uVar8].celula_destino = uVar6;
          iVar11 = extraout_EDX_01 + uVar8 * 0x114;
          if (in_AX == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = 0xffff;
          }
          pUVar1[uVar8].estado_caminho = 0;
          *(undefined1 *)(iVar11 + 0x88) = 0;
          *(undefined1 *)(iVar11 + 0x89) = 0;
          *(undefined1 *)(iVar11 + 2) = 0xf;
          *(ushort *)(iVar11 + 0xb2) = uVar6;
          *(undefined2 *)(iVar11 + 0xc0) = (undefined2)local_30;
          return;
        }
        sVar2 = *(short *)&pUVar1->field_0xc0;
        if (sVar2 == -1) {
          FUN_0041a996(pUVar1,local_38);
          FUN_0041aea4();
          FUN_004454ce(extraout_ECX_01,*(char *)(extraout_ECX_01 + 0xbe));
          return;
        }
        FUN_0044357c();
        uVar6 = FUN_0041aee2();
        pUVar1 = tabela_unidades;
        iVar11 = ((uint)in_AX * 0x10 + extraout_EDX) * 4 + extraout_EDX_00;
        iVar12 = iVar11 * 4;
        (&tabela_unidades->celula_destino)[iVar11 * 2] = uVar6;
        iVar11 = extraout_ECX_00 + iVar12;
        if (in_AX == DAT_00496304) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_004e0f3c = 0;
          DAT_00496304 = 0xffff;
        }
        (&pUVar1->estado_caminho)[iVar12] = 0;
        *(undefined1 *)(iVar11 + 0x88) = 0;
        *(undefined1 *)(iVar11 + 0x89) = 0;
        *(undefined1 *)(iVar11 + 2) = 0xf;
        *(short *)(iVar11 + 0xc0) = sVar2;
        *(ushort *)(iVar11 + 0xb2) = uVar6;
        return;
      }
    }
    else {
      if (uVar6 < 0x12) {
        pUVar1->field_0x82 = 2;
        uVar3 = *(undefined2 *)&pUVar1->field_0x84;
        *(undefined2 *)&pUVar1->field_0x84 = 0;
        *(undefined2 *)&pUVar1->field_0x80 = uVar3;
        return;
      }
      if (uVar6 < 0x14) {
        if (uVar6 == 0x12) {
          pUVar1->estado = 0x12;
          uVar6 = *(ushort *)&pUVar1->field_0xb2;
          pUVar1->field_0x89 = 0;
          *(ushort *)&pUVar1->field_0xb2 = uVar6;
          pUVar1 = tabela_unidades;
          tabela_unidades[in_AX].celula_destino = uVar6;
          if (in_AX == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = 0xffff;
          }
          pUVar1[in_AX].estado_caminho = 0;
          return;
        }
      }
      else {
        if (uVar6 < 0x15) {
          local_24 = pUVar1->field_0x82;
          uVar3 = *(undefined2 *)&pUVar1->field_0x80;
          local_1c = pUVar1->field_0x84;
          uVar4 = *(undefined2 *)&pUVar1->field_0xc0;
          pUVar1->estado = 0x14;
          pUVar1->field_0x89 = 0;
          uVar7 = FUN_0041aee2();
          *(undefined2 *)(extraout_ECX_02 + 0xb2) = uVar7;
          *(undefined2 *)(extraout_ECX_02 + 0xc0) = uVar4;
          pUVar1 = tabela_unidades;
          *(undefined2 *)((int)&tabela_unidades->celula_destino + extraout_EDX_02) =
               *(undefined2 *)(extraout_ECX_02 + 0xb2);
          if (in_AX == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = 0xffff;
          }
          (&pUVar1->estado_caminho)[extraout_EDX_02] = 0;
          pUVar1 = tabela_unidades;
          tabela_unidades[in_AX].field_0x82 = local_24;
          *(undefined2 *)&pUVar1[in_AX].field_0x80 = uVar3;
          *(ushort *)&pUVar1[in_AX].field_0x84 = (ushort)local_1c;
          return;
        }
        if (uVar6 == 0x18) {
          uVar6 = *(ushort *)&pUVar1->field_0xb8;
          FUN_0044357c();
          if (*(char *)(extraout_ECX + 1) != '\x04') {
            return;
          }
          *(char *)(extraout_ECX + 0xf4) = (char)((ushort)extraout_DX >> 8);
          bVar9 = (byte)extraout_DX;
          if (bVar9 == 0) {
            return;
          }
          if (bVar9 < 2) {
            if (in_AX == uVar6) {
              return;
            }
          }
          else if (bVar9 != 5) {
            return;
          }
          *(undefined1 *)(extraout_ECX + 2) = 0x18;
          *(undefined1 *)(extraout_ECX + 0x8a) = 0;
          *(byte *)(extraout_ECX + 0xb7) = bVar9;
          *(ushort *)(extraout_ECX + 0xb8) = uVar6;
          return;
        }
      }
    }
  }
  FUN_004457d3();
  return;
}
