/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044b5f5, entrada 0044b5f5.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_0044b5f5(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  char cVar2;
  ushort uVar3;
  ushort uVar4;
  bool bVar5;
  ushort in_AX;
  int iVar6;
  uint uVar7;
  UnidadeParcial *pUVar8;
  undefined4 uVar9;
  UnidadeParcial *pUVar10;
  UnidadeParcial *pUVar11;
  UnidadeParcial *extraout_ECX;
  UnidadeParcial *extraout_ECX_00;
  UnidadeParcial *extraout_ECX_01;
  UnidadeParcial *extraout_ECX_02;
  UnidadeParcial *extraout_ECX_03;
  UnidadeParcial *extraout_ECX_04;
  UnidadeParcial *extraout_ECX_05;
  undefined4 extraout_ECX_06;
  undefined4 extraout_ECX_07;
  undefined4 extraout_ECX_08;
  undefined4 extraout_ECX_09;
  int extraout_ECX_10;
  undefined4 extraout_ECX_11;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined8 uVar12;
  ulonglong uVar13;
  longlong lVar14;
  ushort uStack_1c;

  pUVar11 = tabela_unidades;
  uVar7 = (uint)in_AX;
  pUVar10 = tabela_unidades + uVar7;
  bVar1 = pUVar10->tipo_id;
  cVar2 = pUVar10->field_0x89;
  pUVar8 = (UnidadeParcial *)CONCAT31(CONCAT21((short)(uVar7 * 0x114 >> 0x10),bVar1),cVar2);
  if (cVar2 == '\0') {
    if (pUVar10->estado != 0xf) goto switchD_0044d86e_default;
    if ((bVar1 == 6) &&
       (tabela_unidades[*(ushort *)&pUVar10->field_0xc0].celula_atual != pUVar10->celula_destino)) {
      pUVar10->celula_destino = tabela_unidades[*(ushort *)&pUVar10->field_0xc0].celula_atual;
      if (in_AX == DAT_00496304) {
        pUVar11 = (UnidadeParcial *)0xffff;
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = 0xffff;
      }
      pUVar10->estado_caminho = 0;
    }
    if ((*(int *)&pUVar10->field_0x83 >> 0x18 == 0) && (*(int *)&pUVar10->field_0x84 >> 0x18 == 0))
    {
      if (CONCAT31((int3)(*(int *)&pUVar10->field_0x84 >> 0x1f),bVar1) == 7) {
        iVar6 = FUN_0042381f(pUVar11,(uint)pUVar10->celula_atual);
        pUVar11 = extraout_ECX;
        if ((char)iVar6 == '\0') goto LAB_0044b70b;
      }
      if (bVar1 == 6) {
        uVar9 = FUN_004468e4(pUVar11);
        pUVar11 = extraout_ECX_00;
        if ((char)uVar9 == '\0') goto LAB_0044b70b;
      }
      pUVar10->field_0x89 = 1;
      pUVar10->field_0x8b = 0x32;
      if (5 < bVar1) {
        if (bVar1 < 7) {
          uStack_1c = tabela_unidades[*(ushort *)&pUVar10->field_0xc0].celula_passo;
        }
        else if (bVar1 == 7) {
          uStack_1c = FUN_0041aee2();
          pUVar11 = extraout_ECX_01;
        }
      }
      pUVar8 = (UnidadeParcial *)FUN_00477042(pUVar11,uStack_1c);
      pUVar10->field_0x90 = (char)pUVar8;
    }
    else {
LAB_0044b70b:
      pUVar8 = (UnidadeParcial *)FUN_0044930c();
    }
    goto switchD_0044d86e_default;
  }
  if (cVar2 != '\x01') goto switchD_0044d86e_default;
  if (pUVar10->field_0x90 != pUVar10->field_0x91) {
    uVar12 = FUN_00448599(tabela_unidades,uVar7);
    pUVar8 = (UnidadeParcial *)uVar12;
    goto switchD_0044d86e_default;
  }
  if (bVar1 == 6) {
    uVar3 = tabela_unidades[*(ushort *)&pUVar10->field_0xc0].celula_atual;
    uVar7 = (uint)uVar3;
    if (uVar3 != pUVar10->celula_destino) {
      pUVar10->celula_destino = uVar3;
      if (in_AX == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = 0xffff;
      }
      pUVar10->estado_caminho = 0;
      pUVar10->field_0x89 = 0;
      pUVar8 = pUVar10;
      goto switchD_0044d86e_default;
    }
  }
  if (pUVar10->field_0xa4 == '\x02') {
    uVar13 = FUN_004704dc(5,0);
    lVar14 = uVar13 % ZEXT48(extraout_ECX_02) << 0x20;
    uVar7 = 0;
    pUVar11 = extraout_ECX_02;
    if ((int)(uVar13 % ZEXT48(extraout_ECX_02)) == 0) goto LAB_0044b83f;
  }
  else {
LAB_0044b83f:
    lVar14 = FUN_00447e12(pUVar11,uVar7);
    pUVar11 = extraout_ECX_03;
  }
  uVar9 = (undefined4)((ulonglong)lVar14 >> 0x20);
  uVar12 = CONCAT44(uVar9,(uint)bVar1);
  if (bVar1 == 7) {
    uVar12 = FUN_0041c652(pUVar11,uVar9);
    pUVar11 = extraout_ECX_04;
    if ((char)uVar12 != '\0') {
      uVar12 = FUN_0041a976(extraout_ECX_04,(int)((ulonglong)uVar12 >> 0x20));
      pUVar11 = extraout_ECX_05;
      if ((short)uVar12 == 0) goto LAB_0044b87b;
    }
  }
  else {
LAB_0044b87b:
    uVar7 = (uint)((ulonglong)uVar12 >> 0x20);
    if ((bVar1 != 6) ||
       (uVar7 = (uint)tabela_unidades[*(ushort *)&pUVar10->field_0xc0].vida,
       *(ushort *)
        (&DAT_004965b6 + (uint)tabela_unidades[*(ushort *)&pUVar10->field_0xc0].tipo_id * 0x32) / 2
       <= uVar7)) {
      if (DAT_00508041 == pUVar10->proprietario_id) {
        thunk_FUN_0048a438((uint)in_AX,uVar7);
        pUVar11 = tabela_unidades;
        uVar9 = FUN_004766f0(extraout_ECX_10,(uint)DAT_00508041);
        if ((char)uVar9 != '\0') {
          uVar12 = FUN_00440c5d(extraout_ECX_11,extraout_EDX_00);
          pUVar11[extraout_ECX_10].field_0xf9 = 0;
          if (*(int *)&pUVar11[extraout_ECX_10].field_0x104 == -1) {
            FUN_0048aa79(0,(uint)pUVar11[extraout_ECX_10].tipo_id << 0x10 | 0x1500,(uint)uVar12);
          }
        }
      }
      pUVar10->field_0xbe = 0xff;
      *(undefined2 *)&pUVar10->field_0xb2 = 0xffff;
      if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
        bVar5 = false;
      }
      else {
        bVar5 = true;
      }
      if ((bVar5) && (tabela_unidades[in_AX].estado = 7, in_AX == DAT_00496304)) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = 0xffff;
      }
      pUVar10 = tabela_unidades + in_AX;
      pUVar10->celula_destino = pUVar10->celula_passo;
      pUVar8 = pUVar10;
      if (in_AX == DAT_00496304) {
        pUVar8 = (UnidadeParcial *)CONCAT22((short)((uint)pUVar10 >> 0x10),(ushort)(byte)pUVar10);
        DAT_004e0f36 = 0;
        DAT_004e0f3c = 0;
        DAT_004e0f37 = 0;
        DAT_00496304 = 0xffff;
      }
      pUVar10->estado_caminho = 0;
      goto switchD_0044d86e_default;
    }
  }
  if (pUVar10->field_0x8b != '\0') {
    pUVar10->field_0x8b = pUVar10->field_0x8b + -1;
  }
  pUVar8 = (UnidadeParcial *)(uint)(byte)pUVar10->field_0x8b;
  if ((pUVar8 == (UnidadeParcial *)0x0) &&
     (pUVar8 = (UnidadeParcial *)(uint)(byte)pUVar10->field_0xa4, pUVar8 == (UnidadeParcial *)0x2))
  {
    uVar7 = FUN_004770ee(pUVar11,pUVar10->field_0x91);
    FUN_004704dc(extraout_ECX_06,uVar7);
    FUN_0046e44c(0,0,0,0,0);
    pUVar11 = tabela_unidades;
    uVar7 = (uint)in_AX;
    bVar1 = tabela_unidades[uVar7].tipo_id;
    pUVar8 = (UnidadeParcial *)CONCAT31((int3)(uVar7 * 0x45 >> 8),bVar1);
    if (5 < bVar1) {
      if (bVar1 < 7) {
        uVar3 = *(ushort *)&pUVar10->field_0xc0;
        tabela_unidades[uVar3].vida = tabela_unidades[uVar3].vida + 2;
        uVar4 = *(ushort *)(&DAT_004965b6 + (uint)tabela_unidades[uVar3].tipo_id * 0x32);
        pUVar8 = (UnidadeParcial *)(uint)uVar4;
        if (uVar4 < pUVar11[uVar3].vida) {
          pUVar11[uVar3].vida = uVar4;
        }
      }
      else if (bVar1 == 7) {
        uVar12 = FUN_0041a976(extraout_ECX_07,uVar7);
        if ((short)uVar12 == 0) {
          pUVar8 = (UnidadeParcial *)FUN_0041cf59(extraout_ECX_08);
        }
        else {
          pUVar8 = (UnidadeParcial *)FUN_0041cec4();
        }
      }
    }
    pUVar10->field_0x8b = 0x14;
  }
  pUVar11 = tabela_unidades;
  if (DAT_00508041 == pUVar10->proprietario_id) {
    uVar7 = (uint)in_AX;
    pUVar8 = (UnidadeParcial *)FUN_004766f0(uVar7,(uint)DAT_00508041);
    if ((char)pUVar8 != '\0') {
      uVar12 = FUN_00440c5d(extraout_ECX_09,extraout_EDX);
      pUVar8 = (UnidadeParcial *)uVar12;
      pUVar11[uVar7].field_0xf9 = 0;
      if (*(int *)&pUVar11[uVar7].field_0x104 == -1) {
        pUVar8 = (UnidadeParcial *)
                 FUN_0048aa79(0,(uint)pUVar11[uVar7].tipo_id << 0x10 | 0x2500,(uint)pUVar8);
      }
    }
  }
switchD_0044d86e_default:
  return CONCAT44(param_2,pUVar8);
}
