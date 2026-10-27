/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004438d8, entrada 004438d8.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004438d8(undefined4 param_1,byte param_2)

{
  byte bVar1;
  bool bVar2;
  UnidadeParcial *pUVar3;
  ushort in_AX;
  ushort uVar4;
  uint uVar5;
  undefined4 uVar6;
  int iVar7;
  undefined4 extraout_ECX;
  int extraout_ECX_00;
  int extraout_ECX_01;
  UnidadeParcial *extraout_ECX_02;
  UnidadeParcial *pUVar8;
  undefined4 extraout_ECX_03;
  int extraout_ECX_04;
  int extraout_ECX_05;
  int extraout_ECX_06;
  int extraout_ECX_07;
  int extraout_ECX_08;
  byte *extraout_ECX_09;
  byte *pbVar9;
  undefined4 extraout_ECX_10;
  undefined4 extraout_ECX_11;
  undefined4 extraout_EDX;
  undefined1 unaff_BL;
  uint uVar10;
  UnidadeParcial *pUVar11;
  undefined8 uVar12;

  pUVar11 = tabela_unidades + in_AX;
  if (param_2 != 0) {
    if (param_2 < 2) {
      uVar4 = FUN_004436ab();
      if (uVar4 != 0xffff) {
        uVar5 = FUN_004472ea(extraout_ECX,param_2);
        pUVar8 = tabela_unidades;
        uVar10 = uVar5 & 0xffff;
        tabela_unidades[uVar10].celula_destino = uVar4;
        pUVar8[uVar10].celula_passo = uVar4;
        pUVar8[uVar10].celula_atual = uVar4;
        pUVar3 = tabela_unidades;
        tabela_unidades[uVar10].celula_destino = uVar4;
        if ((short)uVar5 == DAT_00496304) {
          DAT_004e0f36 = 0;
          DAT_004e0f3c = 0;
          DAT_004e0f37 = 0;
          DAT_00496304 = -1;
        }
        pUVar3[uVar10].estado_caminho = 0;
        if ((tabela_unidades[uVar5 & 0xffff].estado == 0) ||
           (tabela_unidades[uVar5 & 0xffff].estado == 4)) {
          bVar2 = false;
        }
        else {
          bVar2 = true;
        }
        if ((bVar2) && (tabela_unidades[uVar5 & 0xffff].estado = 7, (short)uVar5 == DAT_00496304)) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_004e0f3c = 0;
          DAT_00496304 = -1;
        }
        *(undefined2 *)&pUVar8[uVar10].field_0xc0 = 0xffff;
        *(undefined2 *)&pUVar8[uVar10].field_0xb8 = 0xffff;
        pUVar8[uVar10].deslocamento_y = 0;
        pUVar8[uVar10].deslocamento_x = pUVar8[uVar10].deslocamento_y;
        FUN_00442cb4(tabela_unidades);
        *(undefined1 *)(extraout_ECX_00 + 0x72 + (uVar5 & 0xffff) * 0x114) = 1;
        pUVar8 = tabela_unidades + (uVar5 & 0xffff);
        if ((pUVar8->proprietario_id != 200) && (pUVar8->proprietario_id != 4)) {
          FUN_00476851(pUVar8,(uint)(ushort)((ushort)(byte)pUVar8->field_0xf5 +
                                            pUVar8->raio_visao + 2));
          FUN_00476cb3(extraout_ECX_01,
                       (uint)(ushort)((ushort)*(byte *)(extraout_ECX_01 + 0xbb) +
                                     (ushort)*(byte *)(extraout_ECX_01 + 0xf5)));
          pUVar8 = extraout_ECX_02;
        }
        FUN_0046a388(pUVar8,4);
      }
      switch(tabela_unidades[in_AX].tipo_id) {
      case 0xb:
      case 0xc:
      case 0xd:
      case 0xe:
      case 0xf:
      case 0x10:
      case 0x11:
        bVar2 = true;
        break;
      default:
        bVar2 = false;
      }
      if (bVar2) {
        for (uVar4 = 0; uVar4 < pUVar11->campo_0c; uVar4 = uVar4 + 1) {
          if ((&pUVar11->field_0x4c)[uVar4] == '\x01') {
            bVar1 = tabela_unidades[*(ushort *)(&pUVar11->field_0x10 + (uint)uVar4 * 2)].tipo_id;
            bVar2 = true;
            if (bVar1 < 0xe) {
              if (bVar1 < 6) {
                if ((bVar1 < 3) || (3 < bVar1)) goto LAB_00443bf1;
              }
              else if ((bVar1 < 9) || (bVar1 < 0xb)) {
LAB_00443bf1:
                bVar2 = true;
                goto LAB_00443bf3;
              }
LAB_00443be7:
              bVar2 = false;
            }
            else {
              if ((bVar1 < 0xf) || (bVar1 < 0x12)) goto LAB_00443be7;
              if ((bVar1 < 0x13) || ((bVar1 < 0x17 || (bVar1 < 0x19)))) goto LAB_00443bf1;
              if (bVar1 == 0x19) goto LAB_00443be7;
            }
LAB_00443bf3:
            if (bVar2) {
              bVar2 = true;
              goto LAB_00443bfd;
            }
          }
        }
        bVar2 = false;
LAB_00443bfd:
        if ((!bVar2) && (tabela_unidades[in_AX].tipo_id != 0x11)) {
          if ((pUVar11->proprietario_id == DAT_00508041) &&
             (uVar6 = FUN_004766f0(tabela_unidades + in_AX,(uint)DAT_00508041), (char)uVar6 != '\0')
             ) {
            uVar12 = FUN_00440c5d(extraout_ECX_03,extraout_EDX);
            *(undefined1 *)(extraout_ECX_04 + 0xf9) = 0;
            if (*(int *)(extraout_ECX_04 + 0x104) == -1) {
              FUN_0048aa79(0,(uint)*(byte *)(extraout_ECX_04 + 1) << 0x10 | 0x2600,(uint)uVar12);
            }
          }
          FUN_0044357c();
          FUN_00472648(extraout_ECX_05);
          FUN_00457058();
          pUVar11->proprietario_id = 200;
          pUVar11 = tabela_unidades;
          iVar7 = ((extraout_ECX_05 * 0x10 + extraout_ECX_06) * 4 + extraout_ECX_07) * 4;
          FUN_00442cb4(extraout_ECX_07);
          (&pUVar11->field_0x72)[iVar7] = 1;
          pbVar9 = &tabela_unidades->proprietario_id + iVar7;
          if ((*pbVar9 != 200) && (*pbVar9 != 4)) {
            FUN_00476851(pbVar9,(uint)(ushort)(pbVar9[0xbb] + 2 + (ushort)pbVar9[0xf5]));
            FUN_00476cb3(extraout_ECX_08,
                         (uint)(ushort)((ushort)*(byte *)(extraout_ECX_08 + 0xf5) +
                                       (ushort)*(byte *)(extraout_ECX_08 + 0xbb)));
            pbVar9 = extraout_ECX_09;
          }
          FUN_0046a388(pbVar9,4);
        }
      }
    }
    else if (param_2 == 2) {
      while (iVar7 = FUN_004471b8(2,'\x02'), (short)iVar7 != 0) {
        FUN_004472ea(extraout_ECX_10,(char)extraout_ECX_10);
        FUN_0047605d(extraout_ECX_11,unaff_BL);
      }
    }
  }
  return;
}
