/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004742dc, entrada 004742dc.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004742dc(undefined4 param_1,ushort param_2)

{
  ulonglong uVar1;
  bool bVar2;
  byte in_AL;
  byte bVar3;
  undefined4 uVar4;
  uint uVar5;
  uint extraout_ECX;
  uint uVar6;
  uint extraout_ECX_00;
  undefined4 extraout_ECX_01;
  uint extraout_ECX_02;
  uint extraout_ECX_03;
  uint extraout_ECX_04;
  uint extraout_ECX_05;
  uint extraout_ECX_06;
  uint extraout_ECX_07;
  undefined4 extraout_ECX_08;
  undefined4 extraout_ECX_09;
  undefined4 extraout_ECX_10;
  undefined4 extraout_ECX_11;
  uint extraout_ECX_12;
  uint extraout_ECX_13;
  uint extraout_ECX_14;
  ushort indice_unidade;
  ushort indice_unidade_00;
  undefined4 extraout_EDX;
  uint extraout_EDX_00;
  UnidadeParcial *pUVar7;
  int extraout_EDX_01;
  int iVar8;
  undefined4 extraout_EDX_02;
  uint unaff_EBX;
  ushort indice_unidade_01;
  uint uVar9;
  ushort uVar10;
  longlong lVar11;
  undefined8 uVar12;
  undefined4 local_24;
  uint local_20;
  int local_1c;
  undefined4 local_18;
  byte local_14;
  byte local_10;

  local_20 = (uint)param_2 % 0x100;
  uVar1 = ((ulonglong)unaff_EBX & 0xffffffff0000ffff) % 0x100;
  local_18 = (undefined4)uVar1;
  local_24 = (undefined4)(((ulonglong)unaff_EBX & 0xffffffff0000ffff) / 0x100);
  local_10 = in_AL;
  if ((ushort)uVar1 < (ushort)local_20) {
    FUN_00467cc0(unaff_EBX,(undefined2 *)&local_18);
    unaff_EBX = extraout_ECX;
  }
  if ((ushort)local_24 < param_2 / 0x100) {
    FUN_00467cc0(unaff_EBX,(undefined2 *)&local_24);
  }
  uVar6 = 0;
  uVar9 = 0;
  local_1c = 0;
  do {
    indice_unidade_01 = (ushort)uVar9;
    if (799 < (uVar9 & 0xffff)) {
      return;
    }
    lVar11 = FUN_00443dad(uVar6,uVar9 & 0xffff);
    uVar6 = extraout_ECX_13;
    if ((char)lVar11 != '\0') {
      pUVar7 = tabela_unidades + (int)((ulonglong)lVar11 >> 0x20);
      uVar6 = uVar9;
      if (((pUVar7->estado == 0xe) ||
          (((pUVar7->tipo_id == 0x10 && (pUVar7->estado == 0xd)) && (pUVar7->field_0xab != '2'))))
         || (uVar12 = FUN_004465bf(uVar9,pUVar7), uVar6 = extraout_ECX_14, (char)uVar12 == '\0')) {
        bVar2 = false;
      }
      else {
        bVar2 = true;
      }
      if (bVar2) {
        bVar3 = unidade_obter_proprietario(indice_unidade_01);
        uVar6 = extraout_ECX_00;
        if (bVar3 == local_10) {
          if (tabela_unidades[uVar9 & 0xffff].selecionada != 0) {
            tabela_unidades[uVar9 & 0xffff].selecionada = 0;
            bVar3 = unidade_obter_proprietario(indice_unidade_01);
            FUN_00472576(extraout_ECX_01,CONCAT31((int3)((uint)extraout_EDX >> 8),bVar3));
          }
          uVar4 = FUN_004461f4((ushort)local_18,(ushort)local_20,(ushort)local_24);
          uVar6 = extraout_ECX_02;
          if ((char)uVar4 != '\0') {
            local_14 = local_10;
            lVar11 = FUN_00443dad(uVar9,extraout_EDX_00);
            uVar6 = extraout_ECX_03;
            if ((char)lVar11 != '\0') {
              pUVar7 = tabela_unidades + (uVar9 & 0xffff);
              if (((pUVar7->estado == 0xe) ||
                  (((pUVar7->tipo_id == 0x10 && (pUVar7->estado == 0xd)) &&
                   (pUVar7->field_0xab != '2')))) ||
                 (uVar12 = FUN_004465bf(extraout_ECX_03,pUVar7), uVar6 = extraout_ECX_04,
                 (char)uVar12 == '\0')) {
                bVar2 = false;
              }
              else {
                bVar2 = true;
              }
              if (((bVar2) &&
                  (bVar3 = unidade_obter_proprietario((ushort)uVar6), pUVar7 = tabela_unidades,
                  uVar6 = extraout_ECX_05, bVar3 == local_14)) &&
                 (tabela_unidades[extraout_EDX_01].selecionada == 0)) {
                iVar8 = (uint)local_14 * 0x200;
                if (*(ushort *)(&DAT_00508728 + iVar8) < 0xff) {
                  uVar10 = *(ushort *)(&DAT_00508728 + iVar8) + 1;
                  *(ushort *)(&DAT_00508728 + iVar8) = uVar10;
                  *(short *)(&DAT_00508728 + (uint)uVar10 * 2 + iVar8) = (short)extraout_ECX_05;
                  pUVar7[extraout_EDX_01].selecionada = 1;
                  tabela_unidades[extraout_ECX_05 & 0xffff].selecionada = 1;
                }
              }
            }
            if ((((short)local_1c == 0) &&
                (bVar3 = unidade_obter_tipo(indice_unidade_01), uVar6 = extraout_ECX_06, bVar3 != 10
                )) && (local_10 == DAT_00508041)) {
              unidade_obter_tipo(indice_unidade);
              uVar5 = FUN_00440c44();
              uVar6 = extraout_ECX_07;
              if ((char)uVar5 == '\0') {
                local_1c = local_1c + 1;
                bVar3 = unidade_obter_tipo(indice_unidade_00);
                uVar4 = extraout_ECX_08;
                if (bVar3 == 7) {
                  uVar12 = FUN_00440e11(extraout_ECX_08,extraout_EDX_02);
                  uVar4 = extraout_ECX_09;
                  if ((((uint)uVar12 & 0xff) != 0xb) &&
                     (uVar12 = FUN_00440e11(extraout_ECX_09,(int)((ulonglong)uVar12 >> 0x20)),
                     uVar4 = extraout_ECX_10, ((uint)uVar12 & 0xff) != 0xf)) goto LAB_004745fa;
                  lVar11 = thunk_FUN_0048a438(uVar4,0x16);
                  uVar6 = (uint)((ulonglong)lVar11 >> 0x20);
                  uVar4 = extraout_ECX_11;
                }
                else {
LAB_004745fa:
                  uVar6 = 8;
                }
                FUN_00440d5e(uVar4,uVar6);
                uVar6 = extraout_ECX_12;
              }
            }
          }
        }
      }
    }
    uVar9 = uVar9 + 1;
  } while( true );
}
