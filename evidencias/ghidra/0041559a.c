/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0041559a, entrada 0041559a.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0041559a(undefined4 param_1,int param_2)

{
  byte bVar1;
  UnidadeParcial *pUVar2;
  ushort indice_unidade;
  int in_EAX;
  undefined2 uVar3;
  short extraout_CX;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  int iVar4;
  undefined4 extraout_EDX_01;
  uint unaff_EBX;
  short sVar5;
  uint uVar6;
  bool bVar7;
  undefined8 uVar8;
  short local_48 [6];
  uint local_3c;
  uint local_38;
  int local_34;
  int local_30;
  ushort local_2c;
  undefined2 uStack_2a;
  short local_28;
  ushort local_24;
  undefined2 uStack_22;
  short local_20;
  undefined4 local_1c;
  byte local_18;
  byte local_14;

  pUVar2 = tabela_unidades;
  local_2c = (ushort)unaff_EBX;
  indice_unidade = local_2c;
  uStack_2a = (undefined2)(unaff_EBX >> 0x10);
  uVar6 = unaff_EBX & 0xffff;
  uVar3 = (undefined2)(uVar6 * 0x114 >> 0x10);
  local_30 = param_2 + CONCAT22(uVar3,(short)tabela_unidades[uVar6].deslocamento_y);
  local_48[0] = 0;
  local_48[1] = 0;
  local_48[2] = 0;
  local_48[3] = 0;
  FUN_00410fcc(in_EAX + CONCAT22(uVar3,(short)tabela_unidades[uVar6].deslocamento_x),local_48);
  local_1c = extraout_ECX;
  unidade_obter_tipo(indice_unidade);
  uVar8 = FUN_00415496(extraout_ECX_00,extraout_EDX);
  local_24 = (ushort)uVar8;
  uStack_22 = (undefined2)((ulonglong)uVar8 >> 0x10);
  bVar1 = pUVar2[uVar6].tipo_id;
  if ((4 < bVar1) && (10 < bVar1)) {
    if (bVar1 < 0x13) {
      bVar7 = bVar1 == 0x12;
    }
    else {
      if ((bVar1 < 0x17) || (bVar1 < 0x19)) goto LAB_00415637;
      bVar7 = bVar1 == 0x19;
    }
    if (!bVar7) {
      return;
    }
  }
LAB_00415637:
  if (*(ushort *)&pUVar2[uVar6].field_0xc2 < 0x13c) {
    FUN_00411147((uint)local_2c,(int)(short)((short)local_30 + local_48[2]));
  }
  if ((299 < *(ushort *)&pUVar2[uVar6].field_0xc2) && (*(ushort *)&pUVar2[uVar6].field_0xc2 < 0x13b)
     ) {
    for (local_38 = 0;
        (int)(local_38 & 0xffff) < (int)(*(ushort *)&pUVar2[uVar6].field_0xc2 - 300) / 5;
        local_38 = local_38 + 1) {
      local_48[4] = (short)local_30 + local_48[2];
      local_20 = (short)local_1c + local_48[0];
      local_14 = unidade_obter_proprietario(local_2c);
      sVar5 = local_48[4];
      iVar4 = CONCAT31((int3)((uint)extraout_EDX_00 >> 8),local_14);
      if (((iVar4 == 0) || (iVar4 == 200)) || (iVar4 == 4)) {
        FUN_0045b796('\x01',local_48[4]);
        if (local_14 == 200) {
          FUN_0045bcb0('\x01',sVar5);
        }
      }
      else {
        FUN_0045b796('\x01',extraout_CX);
      }
    }
  }
  if (0x13a < *(ushort *)&pUVar2[uVar6].field_0xc2) {
    for (local_3c = 0;
        (int)(local_3c & 0xffff) < 3 - (int)(*(ushort *)&pUVar2[uVar6].field_0xc2 - 0x13b) / 5;
        local_3c = local_3c + 1) {
      sVar5 = (short)local_30 + local_48[2];
      local_34 = (uint)pUVar2[uVar6].quadro_movimento +
                 (uint)local_24 +
                 (uint)(byte)pUVar2[uVar6].field_0xdb *
                 ((pUVar2[uVar6].orientacao_atual + 1) / 2 - 1);
      local_28 = (short)local_1c + local_48[0];
      local_18 = unidade_obter_proprietario(local_2c);
      iVar4 = CONCAT31((int3)((uint)extraout_EDX_01 >> 8),local_18);
      if (((iVar4 == 0) || (iVar4 == 200)) || (iVar4 == 4)) {
        FUN_0045b796('\x01',sVar5);
        if (local_18 == 200) {
          FUN_0045bcb0('\x01',sVar5);
        }
      }
      else {
        FUN_0045b796('\x01',sVar5);
      }
    }
  }
  return;
}
