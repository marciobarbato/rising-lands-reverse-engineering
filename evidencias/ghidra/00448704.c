/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00448704, entrada 00448704.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00448704(undefined4 param_1,char param_2)

{
  byte bVar1;
  short sVar2;
  short *psVar3;
  bool bVar4;
  uint in_EAX;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  int extraout_ECX_02;
  UnidadeParcial *extraout_ECX_03;
  UnidadeParcial *pUVar5;
  undefined4 extraout_ECX_04;
  undefined4 extraout_EDX;
  sbyte sVar6;
  UnidadeParcial *pUVar7;

  pUVar7 = tabela_unidades + (in_EAX & 0xffff);
  bVar1 = pUVar7->direcao_desejada;
  if (bVar1 < 7) {
    if (bVar1 < 3) {
      if (bVar1 != 1) goto LAB_00448889;
      sVar6 = pUVar7->deslocamento_x - (pUVar7->incremento_passo - param_2);
LAB_0044877b:
      pUVar7->deslocamento_x = sVar6;
      goto LAB_00448889;
    }
    if (bVar1 < 4) {
      pUVar7->deslocamento_x = pUVar7->deslocamento_x - (pUVar7->incremento_passo - param_2);
      sVar6 = pUVar7->deslocamento_y - (pUVar7->incremento_passo - param_2);
LAB_004487ac:
      pUVar7->deslocamento_y = sVar6;
      goto LAB_00448889;
    }
    if (bVar1 != 5) goto LAB_00448889;
    sVar6 = pUVar7->deslocamento_y - (pUVar7->incremento_passo - param_2);
  }
  else {
    if (bVar1 < 8) {
      pUVar7->deslocamento_x = pUVar7->deslocamento_x + (pUVar7->incremento_passo - param_2);
      pUVar7->deslocamento_y = pUVar7->deslocamento_y - (pUVar7->incremento_passo - param_2);
      goto LAB_00448889;
    }
    if (bVar1 < 0xb) {
      if (bVar1 != 9) goto LAB_00448889;
      sVar6 = pUVar7->deslocamento_x + (pUVar7->incremento_passo - param_2);
      goto LAB_0044877b;
    }
    if (bVar1 < 0xc) {
      pUVar7->deslocamento_x = pUVar7->deslocamento_x + (pUVar7->incremento_passo - param_2);
      sVar6 = pUVar7->deslocamento_y + (pUVar7->incremento_passo - param_2);
      goto LAB_004487ac;
    }
    if (bVar1 < 0xd) goto LAB_00448889;
    if (0xd < bVar1) {
      if (bVar1 == 0xf) {
        pUVar7->deslocamento_x = pUVar7->deslocamento_x - (pUVar7->incremento_passo - param_2);
        pUVar7->deslocamento_y = pUVar7->deslocamento_y + (pUVar7->incremento_passo - param_2);
      }
      goto LAB_00448889;
    }
    sVar6 = pUVar7->deslocamento_y + (pUVar7->incremento_passo - param_2);
  }
  pUVar7->deslocamento_y = sVar6;
LAB_00448889:
  pUVar7->progresso_passo = pUVar7->progresso_passo + (pUVar7->incremento_passo - param_2);
  if (0x1f < pUVar7->progresso_passo) {
    pUVar7->progresso_passo = 0;
    pUVar7->deslocamento_x = 0;
    pUVar7->deslocamento_y = 0;
    FUN_00442eac();
    FUN_00442cb4(extraout_ECX);
    FUN_0046a388(extraout_ECX_00,5);
    if ((pUVar7->proprietario_id != 200) && (pUVar7->proprietario_id != 4)) {
      FUN_00476e82(extraout_ECX_01,
                   (uint)(ushort)((ushort)pUVar7->raio_visao + (ushort)(byte)pUVar7->field_0xf5));
    }
    pUVar7->celula_atual = pUVar7->celula_passo;
    pUVar5 = tabela_unidades + (in_EAX & 0xffff);
    if ((pUVar5->proprietario_id != 200) && (pUVar5->proprietario_id != 4)) {
      FUN_00476851(pUVar5,(uint)(ushort)((ushort)(byte)pUVar5->field_0xf5 + pUVar5->raio_visao + 2))
      ;
      FUN_00476cb3(extraout_ECX_02,
                   (uint)(ushort)((ushort)*(byte *)(extraout_ECX_02 + 0xf5) +
                                 (ushort)*(byte *)(extraout_ECX_02 + 0xbb)));
      pUVar5 = extraout_ECX_03;
    }
    FUN_0046a388(pUVar5,4);
    if ((*(char *)(DAT_00507d74 + (uint)pUVar7->celula_atual) == 'F') &&
       (pUVar7->proprietario_id != *(byte *)((uint)pUVar7->celula_atual + DAT_00507dac))) {
      if ((tabela_unidades[in_EAX & 0xffff].tipo_id < 0x10) ||
         (0x11 < tabela_unidades[in_EAX & 0xffff].tipo_id)) {
        bVar4 = false;
      }
      else {
        bVar4 = true;
      }
      if (!bVar4) {
        FUN_00450874(0,8,'\0');
        FUN_004704dc(extraout_ECX_04,extraout_EDX);
        FUN_0046e44c(0,0,0,0,0);
        *(undefined1 *)(DAT_00507d74 + (uint)pUVar7->celula_atual) = 0;
        *(undefined1 *)(DAT_00507dac + (uint)pUVar7->celula_atual) = 0;
      }
    }
    psVar3 = *(short **)(DAT_004e1924 + (in_EAX & 0xffff) * 4);
    sVar2 = *psVar3;
    if (sVar2 != 0) {
      *psVar3 = sVar2 + -1;
    }
  }
  if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
     (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
    bVar4 = false;
  }
  else {
    bVar4 = true;
  }
  if (bVar4) {
    switch(tabela_unidades[in_EAX & 0xffff].tipo_id) {
    case 0:
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
    case 7:
    case 8:
    case 9:
    case 10:
    case 0x19:
      bVar4 = true;
      break;
    default:
      bVar4 = false;
    }
    if (bVar4) {
      FUN_00452cc8((in_EAX & 0xffff) * 0x45);
    }
  }
  FUN_00445f27();
  return;
}
