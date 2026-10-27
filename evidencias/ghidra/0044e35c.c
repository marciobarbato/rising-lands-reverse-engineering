/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044e35c, entrada 0044e35c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Removing unreachable block (ram,0x0044e3bb) */
/* WARNING: Removing unreachable block (ram,0x0044e4b2) */

void __fastcall FUN_0044e35c(uint param_1)

{
  ushort *puVar1;
  undefined2 uVar2;
  bool bVar3;
  ushort in_AX;
  ushort uVar4;
  UnidadeParcial *pUVar5;
  int iVar6;
  undefined4 uVar7;
  uint uVar8;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  char cVar9;
  int extraout_EDX;
  UnidadeParcial *pUVar10;

  pUVar10 = tabela_unidades + in_AX;
  bVar3 = false;
  switch(pUVar10->field_0x89) {
  case 0:
    uVar7 = 1;
    if ((uint)pUVar10->campo_0c < *(ushort *)&pUVar10->field_0x70 + 1) {
LAB_0044e427:
      pUVar10->field_0x8b = 10;
      pUVar10->field_0x89 = 1;
      return;
    }
    if ((pUVar10->celula_atual != pUVar10->celula_destino) &&
       (iVar6 = FUN_0042381f(1,(uint)pUVar10->celula_atual), uVar7 = extraout_ECX,
       (char)iVar6 == '\0')) goto LAB_0044e405;
    iVar6 = FUN_0042381f(uVar7,(uint)pUVar10->celula_atual);
    if ((char)iVar6 != '\0') goto LAB_0044e427;
    uVar4 = FUN_0041aee2();
    pUVar5 = (UnidadeParcial *)
             (&tabela_unidades->proprietario_id + (extraout_EDX * 4 + (uint)in_AX) * 4);
    pUVar5->celula_destino = uVar4;
joined_r0x0044e8cb:
    if (in_AX == DAT_00496304) {
      DAT_004e0f37 = 0;
      DAT_004e0f36 = 0;
      DAT_004e0f3c = 0;
      DAT_00496304 = 0xffff;
    }
    break;
  case 1:
    if ((uint)pUVar10->campo_0c < *(ushort *)&pUVar10->field_0x70 + 1) {
      bVar3 = true;
    }
    else {
      cVar9 = pUVar10->field_0x8b + -1;
      pUVar10->field_0x8b = cVar9;
      if ((cVar9 == '\0') &&
         (iVar6 = FUN_004676e5(0,(ushort)(*(short *)&pUVar10->field_0x84 == 2),
                               pUVar10->proprietario_id), (char)iVar6 != '\0')) {
        FUN_004235bd(extraout_ECX_00,1);
        puVar1 = &pUVar10->campo_0a;
        uVar2 = *(undefined2 *)&pUVar10->field_0x84;
        uVar4 = *puVar1;
        *(short *)&pUVar10->field_0x70 = *(short *)&pUVar10->field_0x70 + 1;
        *(undefined1 *)(uVar4 + 0x42 + (int)puVar1) = 2;
        *(undefined2 *)(&pUVar10->field_0x10 + (uint)uVar4 * 2) = uVar2;
        *puVar1 = *puVar1 + 1;
        pUVar10->field_0x8b = 10;
        bVar3 = false;
      }
    }
    if (!bVar3) {
      return;
    }
    if (pUVar10->field_0x82 == '\x02') {
      if (*(short *)&pUVar10->field_0x80 == -1) {
        if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
          bVar3 = false;
        }
        else {
          bVar3 = true;
        }
        if (!bVar3) {
          return;
        }
        tabela_unidades[in_AX].estado = 7;
        if (in_AX == DAT_00496304) {
          DAT_00496304 = 0xffff;
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_004e0f3c = 0;
          return;
        }
        return;
      }
      uVar4 = FUN_0041aee2();
      pUVar10->field_0x89 = 2;
      pUVar5 = tabela_unidades + in_AX;
      pUVar5->celula_destino = uVar4;
      if (in_AX == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = 0xffff;
      }
    }
    else {
      if (pUVar10->field_0x82 != '\x01') {
        return;
      }
      pUVar10->field_0x89 = 2;
      pUVar5 = tabela_unidades + in_AX;
      pUVar5->celula_destino = *(ushort *)&pUVar10->field_0x80;
      if (in_AX == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_00496304 = 0xffff;
        DAT_004e0f3c = 0;
      }
    }
    break;
  case 2:
    if (pUVar10->field_0x82 == '\x02') {
      if (((*(int *)&pUVar10->field_0x83 >> 0x18 == 0) &&
          (*(int *)&pUVar10->field_0x84 >> 0x18 == 0)) &&
         (iVar6 = FUN_0042381f(param_1,(uint)pUVar10->celula_atual), (char)iVar6 != '\0')) {
        FUN_00472648(extraout_ECX_01);
LAB_0044e773:
        pUVar10->field_0x89 = 3;
        pUVar10->field_0x8b = 10;
        return;
      }
LAB_0044e405:
      FUN_0044930c();
      return;
    }
    if (pUVar10->field_0x82 != '\x01') {
      return;
    }
    if (pUVar10->celula_atual != pUVar10->celula_destino) goto LAB_0044e405;
    uVar8 = FUN_00479555(*(ushort *)&pUVar10->field_0x80 >> 8,pUVar10->celula_atual >> 8);
    if (0x10 < uVar8) {
      pUVar5 = tabela_unidades + in_AX;
      pUVar5->celula_destino = *(ushort *)&pUVar10->field_0x80;
      goto joined_r0x0044e8cb;
    }
    uVar7 = FUN_00475763(extraout_ECX_02,pUVar10->field_0x84 + 'B');
    if ((char)uVar7 != '\0') goto LAB_0044e773;
    uVar8 = FUN_00475bfe(extraout_ECX_03,pUVar10->field_0x84 + 'B');
    if ((uVar8 & 0xffff) == 0xffff) {
      return;
    }
    pUVar5 = tabela_unidades + in_AX;
    pUVar5->celula_destino = (ushort)uVar8;
    if (in_AX == DAT_00496304) {
      DAT_004e0f36 = 0;
      DAT_004e0f37 = 0;
      DAT_004e0f3c = 0;
      DAT_00496304 = 0xffff;
    }
    break;
  case 3:
    cVar9 = pUVar10->field_0x8b + -1;
    pUVar10->field_0x8b = cVar9;
    if (cVar9 != '\0') {
      return;
    }
    pUVar10->field_0x8b = 10;
    uVar8 = FUN_004471b8(param_1,'\x02');
    if ((uVar8 & 0xffff) != 0) {
      if (pUVar10->field_0x82 == '\x02') {
        FUN_0042340f((uint)*(ushort *)&pUVar10->field_0x80,1);
        FUN_004472ea(extraout_ECX_05,'\x02');
        return;
      }
      if (pUVar10->field_0x82 == '\x01') {
        FUN_004438d8(extraout_ECX_04,2);
        return;
      }
      return;
    }
    if (*(short *)&pUVar10->field_0xb2 == -1) {
      if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
        bVar3 = false;
      }
      else {
        bVar3 = true;
      }
      if (!bVar3) {
        return;
      }
      tabela_unidades[in_AX].estado = 7;
      if (in_AX == DAT_00496304) {
        DAT_00496304 = 0xffff;
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        return;
      }
      return;
    }
    pUVar10->field_0x89 = 0;
    pUVar5 = tabela_unidades + in_AX;
    pUVar5->celula_destino = *(ushort *)&pUVar10->field_0xb2;
    if (in_AX == DAT_00496304) {
      DAT_004e0f36 = 0;
      DAT_004e0f37 = 0;
      DAT_004e0f3c = 0;
      DAT_00496304 = 0xffff;
    }
    break;
  default:
    goto switchD_0044d86e_default;
  }
  pUVar5->estado_caminho = 0;
switchD_0044d86e_default:
  return;
}
