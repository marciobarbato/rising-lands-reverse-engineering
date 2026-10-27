/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00448d08, entrada 00448d08.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00448d08(undefined4 param_1)

{
  byte bVar1;
  bool bVar2;
  UnidadeParcial *pUVar3;
  UnidadeParcial *pUVar4;
  char cVar5;
  ushort in_AX;
  int iVar6;
  uint uVar7;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 uVar8;
  int extraout_EDX;
  short local_28 [4];
  uint local_20;
  byte local_1c;
  byte local_18;

  pUVar3 = tabela_unidades;
  iVar6 = FUN_00477042(param_1,tabela_unidades[in_AX].celula_destino);
  local_18 = (byte)iVar6;
  local_1c = 0;
  uVar8 = extraout_ECX;
  do {
    if (2 < local_1c) {
      pUVar3[in_AX].estado_caminho = 3;
      pUVar3[in_AX].field_0x8b = 0;
      return;
    }
    for (uVar7 = 0; (uVar7 & 0xffff) < 4; uVar7 = uVar7 + 1) {
      local_28[uVar7 & 0xffff] = -1;
    }
    local_20 = FUN_004770ee(uVar8,local_18);
    uVar8 = extraout_ECX_00;
    if ((local_20 & 0xffff) != 0xffff) {
      uVar7 = FUN_00442668((int)local_28,(ushort)local_20);
      pUVar4 = tabela_unidades;
      if ((char)uVar7 != '\0') {
        bVar1 = tabela_unidades[in_AX].tipo_id;
        if ((bVar1 < 0xc) || ((0xc < bVar1 && (bVar1 != 0xf)))) {
          bVar2 = false;
        }
        else {
          bVar2 = true;
        }
        if (bVar2) {
          uVar7 = 0;
          while (((uVar7 & 0xffff) < 4 && (local_28[uVar7 & 0xffff] != -1))) {
            FUN_00444938();
            uVar7 = extraout_EDX + 1;
          }
        }
        FUN_00442eac();
        FUN_00442cb4(extraout_ECX_02);
        FUN_00442cb4(extraout_ECX_03);
        pUVar3[in_AX].field_0x8b = 0;
        pUVar3[in_AX].celula_passo = (ushort)local_20;
        pUVar3[in_AX].field_0x90 = local_18;
        return;
      }
      uVar8 = extraout_ECX_01;
      if ((ushort)local_20 == pUVar3[in_AX].celula_destino) {
        tabela_unidades[in_AX].celula_destino = tabela_unidades[in_AX].celula_passo;
        if (in_AX == DAT_00496304) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_004e0f3c = 0;
          DAT_00496304 = 0xffff;
        }
        pUVar4[in_AX].estado_caminho = 0;
        return;
      }
    }
    if (local_1c == 0) {
      if (local_18 == 1) {
        cVar5 = '\x10';
      }
      else {
        cVar5 = local_18 - 1;
      }
      if (cVar5 == '\x01') {
        local_18 = 0x10;
      }
      else {
        local_18 = cVar5 - 1;
      }
    }
    else if (local_1c == 1) {
      local_18 = (byte)(local_18 % 0x10 + 1) % 0x10 + 1;
    }
    local_1c = local_1c + 1;
  } while( true );
}
