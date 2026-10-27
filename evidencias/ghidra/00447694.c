/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00447694, entrada 00447694.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00447694(undefined4 param_1,ushort param_2)

{
  UnidadeParcial *pUVar1;
  ushort uVar2;
  bool bVar3;
  ushort in_AX;
  UnidadeParcial *pUVar4;
  undefined4 uVar5;
  uint uVar6;
  short extraout_CX;
  int extraout_ECX;
  UnidadeParcial *extraout_ECX_00;
  UnidadeParcial *pUVar7;
  int extraout_ECX_01;
  int extraout_ECX_02;
  int extraout_ECX_03;
  int extraout_ECX_04;
  int iVar8;
  undefined4 extraout_EDX;
  ushort *puVar9;
  undefined8 uVar10;
  longlong lVar11;

  pUVar1 = tabela_unidades + in_AX;
  pUVar4 = tabela_unidades + param_2;
  switch(pUVar1->tipo_id) {
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
  if ((bVar3) && (pUVar1->campo_0a < pUVar1->campo_0c)) {
    bVar3 = true;
  }
  else {
    bVar3 = false;
  }
  if ((bVar3) &&
     ((pUVar1->proprietario_id == 200 || (pUVar1->proprietario_id == pUVar4->proprietario_id)))) {
    if (pUVar1->proprietario_id == 200) {
      pUVar1->proprietario_id = tabela_unidades[param_2].proprietario_id;
      pUVar7 = tabela_unidades + in_AX;
      if ((pUVar7->proprietario_id != 200) && (pUVar7->proprietario_id != 4)) {
        FUN_00476851(pUVar7,(uint)(ushort)((ushort)(byte)pUVar7->field_0xf5 + pUVar7->raio_visao + 2
                                          ));
        FUN_00476cb3(extraout_ECX,
                     (uint)(ushort)((ushort)*(byte *)(extraout_ECX + 0xf5) +
                                   (ushort)*(byte *)(extraout_ECX + 0xbb)));
        pUVar7 = extraout_ECX_00;
      }
      FUN_0046a388(pUVar7,4);
      iVar8 = extraout_ECX_01;
      if ((DAT_00508041 == pUVar1->proprietario_id) &&
         (uVar5 = FUN_004766f0(tabela_unidades + in_AX,(uint)DAT_00508041), iVar8 = extraout_ECX_02,
         (char)uVar5 != '\0')) {
        uVar10 = FUN_00440c5d(extraout_ECX_02,extraout_EDX);
        *(undefined1 *)(extraout_ECX_03 + 0xf9) = 0;
        iVar8 = extraout_ECX_03;
        if (*(int *)(extraout_ECX_03 + 0x104) == -1) {
          FUN_0048aa79(0,(uint)*(byte *)(extraout_ECX_03 + 1) << 0x10 | 0x2700,(uint)uVar10);
          iVar8 = extraout_ECX_04;
        }
      }
      lVar11 = FUN_004475ac(iVar8,1);
      uVar6 = FUN_00428cc0((uint)lVar11,(char)((ulonglong)lVar11 >> 0x20));
      tabela_unidades[in_AX].campo_0c = extraout_CX + (short)uVar6;
    }
    puVar9 = &pUVar1->campo_0a;
    uVar2 = *puVar9;
    *(short *)&pUVar1->field_0x70 = *(short *)&pUVar1->field_0x70 + 1;
    (&pUVar1->field_0x4c)[uVar2] = 1;
    puVar9[uVar2 + 3] = param_2;
    *puVar9 = *puVar9 + 1;
    pUVar4->estado = 0xe;
  }
  FUN_00445f27();
  return;
}
