/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00472769, entrada 00472769.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00472769(undefined4 param_1,uint param_2)

{
  byte in_AL;
  byte bVar1;
  ushort indice_unidade;
  uint uVar2;
  uint uVar3;
  uint extraout_ECX;
  uint extraout_ECX_00;
  undefined4 extraout_ECX_01;
  uint extraout_ECX_02;
  uint extraout_ECX_03;
  uint extraout_ECX_04;
  uint extraout_ECX_05;
  undefined4 extraout_ECX_06;
  undefined4 extraout_ECX_07;
  undefined4 extraout_ECX_08;
  undefined4 extraout_ECX_09;
  undefined4 uVar4;
  uint extraout_ECX_10;
  byte bVar5;
  uint extraout_EDX;
  undefined4 extraout_EDX_00;
  uint extraout_EDX_01;
  uint extraout_EDX_02;
  undefined4 extraout_EDX_03;
  uint extraout_EDX_04;
  uint uVar6;
  int iVar7;
  ushort uVar8;
  int iVar9;
  longlong lVar10;
  undefined8 uVar11;

  bVar5 = (byte)param_2;
  iVar9 = 0;
  uVar2 = 0;
  do {
    uVar6 = uVar2 & 0xffff;
    if (799 < uVar6) {
      return;
    }
    lVar10 = FUN_00443dad(uVar2,param_2);
    param_2 = (uint)((ulonglong)lVar10 >> 0x20);
    uVar3 = extraout_ECX;
    if ((char)lVar10 != '\0') {
      bVar1 = unidade_obter_proprietario((ushort)uVar2);
      uVar3 = extraout_ECX_00;
      param_2 = extraout_EDX;
      if (bVar1 == in_AL) {
        if (tabela_unidades[uVar6].selecionada != 0) {
          tabela_unidades[uVar6].selecionada = 0;
          bVar1 = unidade_obter_proprietario((ushort)uVar2);
          FUN_00472576(extraout_ECX_01,CONCAT31((int3)((uint)extraout_EDX_00 >> 8),bVar1));
          uVar3 = extraout_ECX_02;
        }
        param_2 = (uVar3 & 0xffff) * 0x114;
        if (tabela_unidades[uVar3 & 0xffff].grupo_id == bVar5) {
          uVar11 = FUN_00440e11(uVar3,param_2);
          param_2 = (uint)((ulonglong)uVar11 >> 0x20);
          uVar3 = extraout_ECX_03;
          if (((uint)uVar11 & 0xff) != 0xe) {
            iVar7 = (uint)in_AL * 0x200;
            indice_unidade = (ushort)extraout_ECX_03;
            if (*(ushort *)(&DAT_00508728 + iVar7) < 0xff) {
              uVar8 = *(ushort *)(&DAT_00508728 + iVar7) + 1;
              *(ushort *)(&DAT_00508728 + iVar7) = uVar8;
              *(ushort *)(&DAT_00508728 + (uint)uVar8 * 2 + iVar7) = indice_unidade;
              (&tabela_unidades->selecionada)[param_2] = 1;
            }
            if (iVar9 < 1) {
              bVar1 = unidade_obter_tipo(indice_unidade);
              uVar3 = extraout_ECX_04;
              param_2 = extraout_EDX_01;
              if ((bVar1 != 10) && (in_AL == DAT_00508041)) {
                unidade_obter_tipo(indice_unidade);
                uVar2 = FUN_00440c44();
                uVar3 = extraout_ECX_05;
                param_2 = extraout_EDX_02;
                if ((char)uVar2 == '\0') {
                  iVar9 = iVar9 + 1;
                  bVar1 = unidade_obter_tipo(indice_unidade);
                  uVar4 = extraout_ECX_06;
                  if (bVar1 == 7) {
                    uVar11 = FUN_00440e11(extraout_ECX_06,extraout_EDX_03);
                    uVar4 = extraout_ECX_07;
                    if (((uint)uVar11 & 0xff) != 0xb) {
                      uVar11 = FUN_00440e11(extraout_ECX_07,(int)((ulonglong)uVar11 >> 0x20));
                      uVar4 = extraout_ECX_08;
                      if (((uint)uVar11 & 0xff) != 0xf) goto LAB_004728f5;
                    }
                    lVar10 = thunk_FUN_0048a438(uVar4,0x16);
                    uVar2 = (uint)((ulonglong)lVar10 >> 0x20);
                    uVar4 = extraout_ECX_09;
                  }
                  else {
LAB_004728f5:
                    uVar2 = 8;
                  }
                  FUN_00440d5e(uVar4,uVar2);
                  uVar3 = extraout_ECX_10;
                  param_2 = extraout_EDX_04;
                }
              }
            }
          }
        }
      }
    }
    uVar2 = uVar3 + 1;
  } while( true );
}
