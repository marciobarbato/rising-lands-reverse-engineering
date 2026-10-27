/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004829c8, entrada 004829c8.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004829c8(undefined4 param_1,undefined1 param_2)

{
  byte bVar1;
  ushort in_AX;
  uint uVar2;
  undefined4 *puVar3;
  undefined4 extraout_ECX;
  int extraout_ECX_00;
  undefined4 *extraout_ECX_01;
  int extraout_ECX_02;
  undefined4 *extraout_ECX_03;
  undefined4 *extraout_ECX_04;
  UnidadeParcial *pUVar4;
  int iVar5;
  undefined4 uVar6;
  undefined4 unaff_EBX;
  undefined8 uVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  undefined4 uVar10;
  undefined4 uVar11;

  uVar2 = (uint)tabela_unidades[in_AX].proprietario_id;
  uVar7 = FUN_0046d817(param_1,unaff_EBX);
  if (((uint)uVar7 & 0xff) != 2) {
    return;
  }
  if (*(int *)&tabela_unidades[in_AX].field_0x10c == -1) {
    puVar3 = (undefined4 *)0x0;
  }
  else {
    puVar3 = &DAT_0051a9e0 + *(int *)&tabela_unidades[in_AX].field_0x10c * 8;
  }
  switch(param_2) {
  case 0x41:
    if (puVar3 != (undefined4 *)0x0) {
      FUN_004832b1(puVar3,in_AX);
      pUVar4 = tabela_unidades;
      uVar2 = *(uint *)(&DAT_0051b68c + (uint)tabela_unidades[in_AX].proprietario_id * 0x60);
      if ((uVar2 & 0x7ffffff) != 0x7fd72b1) {
        *(undefined2 *)&tabela_unidades[in_AX].field_0x108 = (&DAT_0051a9f0)[uVar2 * 0x10];
        *(uint *)&pUVar4[in_AX].field_0x10c = uVar2;
        (&DAT_0051a9f0)[uVar2 * 0x10] = in_AX;
        (&DAT_0051a9f2)[uVar2 * 0x10] = (&DAT_0051a9f2)[uVar2 * 0x10] + 1;
      }
    }
    break;
  case 0x42:
    FUN_004832b1(puVar3,in_AX);
    FUN_004838d1(extraout_ECX,
                 *(uint *)(&DAT_0051b690 + (uint)tabela_unidades[in_AX].proprietario_id * 0x60));
    break;
  case 0x43:
    pUVar4 = tabela_unidades + in_AX;
    uVar2 = *(uint *)(&DAT_0051b68c + (uint)pUVar4->proprietario_id * 0x60);
    if ((uVar2 & 0x7ffffff) != 0x7fd72b1) {
      *(undefined2 *)&pUVar4->field_0x108 = (&DAT_0051a9f0)[uVar2 * 0x10];
      *(uint *)&pUVar4->field_0x10c = uVar2;
      (&DAT_0051a9f0)[uVar2 * 0x10] = in_AX;
      (&DAT_0051a9f2)[uVar2 * 0x10] = (&DAT_0051a9f2)[uVar2 * 0x10] + 1;
    }
    for (iVar5 = (&DAT_0051b6b4)[(uint)tabela_unidades[in_AX].proprietario_id * 0x18];
        (iVar5 != -1 && ((&DAT_0051a9fa)[iVar5 * 0x20] != tabela_unidades[in_AX].tipo_id));
        iVar5 = (&DAT_0051a9e4)[iVar5 * 8]) {
    }
    if (iVar5 == -1) {
      uVar11 = 0;
      uVar10 = 0;
      uVar9 = 0;
      uVar8 = 0;
      unidade_obter_proprietario(in_AX);
      uVar6 = 9;
    }
    else {
      uVar11 = 0;
      uVar10 = 0;
      uVar9 = 0;
      uVar8 = 0;
      unidade_obter_proprietario(in_AX);
      uVar6 = 0x17;
    }
    goto LAB_00482d20;
  case 0x44:
    if (puVar3 != (undefined4 *)0x0) {
      if (puVar3[3] != -1) {
        FUN_0048873f(puVar3,puVar3[3]);
        FUN_00488cea(extraout_ECX_00,*(int *)(extraout_ECX_00 + 0xc));
        puVar3 = extraout_ECX_01;
      }
      FUN_004832b1(puVar3,in_AX);
      if ((*(int *)(extraout_ECX_02 + 0x1c) != 0) && (*(int *)(extraout_ECX_02 + 8) != -1)) {
        if ((*(byte *)(extraout_ECX_02 + 0x1c) & 1) == 0) {
          uVar6 = 0xffffffff;
        }
        else {
          uVar6 = 1;
        }
        FUN_0047da54(extraout_ECX_02,uVar6);
      }
    }
    break;
  case 0x45:
    bVar1 = tabela_unidades[in_AX].proprietario_id;
    goto LAB_00482cdb;
  case 0x46:
    FUN_004832b1((uint)in_AX * 0x114,in_AX);
    bVar1 = (&tabela_unidades->proprietario_id)[(int)extraout_ECX_03];
    puVar3 = extraout_ECX_03;
LAB_00482cdb:
    FUN_004838d1(puVar3,(&DAT_0051b664)[(uint)bVar1 * 0x18]);
    bVar1 = unidade_obter_tipo(in_AX);
    if (((&DAT_004989f9)[(uint)bVar1 * 4] & 2) != 0) {
      uVar11 = 0;
      uVar10 = 0;
      uVar9 = 0;
      uVar8 = 0;
      unidade_obter_proprietario(in_AX);
      uVar6 = 0x10;
LAB_00482d20:
      FUN_0047d920(0,uVar6,uVar8,uVar9,uVar10,uVar11);
    }
    break;
  case 0x48:
    if (((puVar3 != (undefined4 *)0x0) && (*(byte *)((int)puVar3 + 0x1b) != 0xff)) &&
       (*(code **)(&PTR_DAT_00498e94)[*(byte *)((int)puVar3 + 0x1b)] != (code *)0x0)) {
      (**(code **)(&PTR_DAT_00498e94)[*(byte *)((int)puVar3 + 0x1b)])();
    }
    break;
  case 0x49:
    if (((puVar3 != (undefined4 *)0x0) && (*(byte *)((int)puVar3 + 0x1b) != 0xff)) &&
       (*(code **)((&PTR_DAT_00498e94)[*(byte *)((int)puVar3 + 0x1b)] + 8) != (code *)0x0)) {
      (**(code **)((&PTR_DAT_00498e94)[*(byte *)((int)puVar3 + 0x1b)] + 8))();
    }
    break;
  case 0x4a:
    if (puVar3 != (undefined4 *)0x0) {
      if ((*(byte *)((int)puVar3 + 0x1b) != 0xff) &&
         (*(code **)((&PTR_DAT_00498e94)[*(byte *)((int)puVar3 + 0x1b)] + 4) != (code *)0x0)) {
        (**(code **)((&PTR_DAT_00498e94)[*(byte *)((int)puVar3 + 0x1b)] + 4))();
        puVar3 = extraout_ECX_04;
      }
      if (puVar3[3] != -1) {
        FUN_00488cea(puVar3,puVar3[3]);
      }
    }
    break;
  case 0x4b:
    if (puVar3 != (undefined4 *)0x0) {
      if (*(byte *)((int)puVar3 + 0x1b) == 0xff) {
        FUN_00453b84();
      }
      else if (*(code **)((&PTR_DAT_00498e94)[*(byte *)((int)puVar3 + 0x1b)] + 0x10) != (code *)0x0)
      {
        (**(code **)((&PTR_DAT_00498e94)[*(byte *)((int)puVar3 + 0x1b)] + 0x10))();
      }
    }
    break;
  case 0x4c:
    if (((puVar3 != (undefined4 *)0x0) && (*(byte *)((int)puVar3 + 0x1b) != 0xff)) &&
       (*(code **)((&PTR_DAT_00498e94)[*(byte *)((int)puVar3 + 0x1b)] + 0xc) != (code *)0x0)) {
      (**(code **)((&PTR_DAT_00498e94)[*(byte *)((int)puVar3 + 0x1b)] + 0xc))(uVar2);
    }
  }
  return;
}
