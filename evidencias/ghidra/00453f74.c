/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00453f74, entrada 00453f74.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00453f74(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  byte bVar2;
  bool bVar3;
  ushort in_AX;
  uint uVar4;
  undefined4 uVar5;
  int iVar6;
  ushort *puVar7;
  uint uVar8;
  undefined2 extraout_var;
  int iVar9;
  uint uVar10;
  UnidadeParcial *pUVar11;
  uint uVar12;
  bool bVar13;
  ushort local_4c;
  ushort local_48;
  int local_44;
  uint local_3c;
  uint local_38;
  uint local_30;
  int local_2c;
  uint local_24;

  pUVar11 = tabela_unidades + in_AX;
  bVar1 = pUVar11->tipo_id;
  if ((bVar1 < 2) || ((2 < bVar1 && (bVar1 != 8)))) {
    bVar3 = false;
  }
  else {
    bVar3 = true;
  }
  if ((!bVar3) || (local_44 = FUN_00453da2(), CONCAT22(extraout_var,(short)local_44) == 0xffff)) {
    uVar8 = 0x100;
    local_3c = (uint)pUVar11->celula_atual % 0x100;
    uVar4 = pUVar11->celula_atual / 0x100;
    uVar10 = (uint)pUVar11->raio_visao;
    local_30 = uVar10 * 2 + 1;
    if (pUVar11->raio_visao < local_3c) {
      local_3c = local_3c - uVar10;
      uVar10 = local_30;
    }
    else {
      uVar8 = 0;
      uVar10 = local_30 - (uVar10 - local_3c);
      local_3c = 0;
    }
    bVar2 = pUVar11->raio_visao;
    if (bVar2 < uVar4) {
      uVar8 = uVar4 - bVar2;
      local_24 = uVar8;
    }
    else {
      local_30 = local_30 - (bVar2 - uVar4);
      local_24 = 0;
    }
    bVar3 = false;
    local_38 = local_3c + local_24 * 0x100;
    local_4c = (ushort)local_24;
    local_2c = 0xffff;
    for (; (int)(short)local_4c < (int)((local_30 & 0xffff) + (local_24 & 0xffff));
        local_4c = local_4c + 1) {
      if ((short)local_4c < 0x100) {
        for (uVar12 = local_3c; (int)(short)uVar12 < (int)((local_3c & 0xffff) + (uVar10 & 0xffff));
            uVar12 = uVar12 + 1) {
          if ((short)uVar12 < 0x100) {
            puVar7 = (ushort *)((local_38 & 0xffff) * 2 + DAT_004e0f38);
            if ((*puVar7 >> 8 & 0xc0) == 0x40) {
              iVar9 = (int)(uint)(*puVar7 & 0x3ff8) >> 3;
            }
            else {
              iVar9 = 0xffff;
            }
            if (iVar9 != 0xffff) {
              if (tabela_unidades[iVar9].proprietario_id != 200) {
                uVar5 = FUN_0046d838(uVar8,pUVar11->proprietario_id);
                if ((char)uVar5 == '\0') {
                  bVar2 = tabela_unidades[iVar9].tipo_id;
                  if (((bVar2 == 0x11) || (bVar2 == 10)) ||
                     ((bVar2 == 0x10 && ((bVar1 < 2 || ((2 < bVar1 && (bVar1 != 8)))))))) {
                    bVar13 = false;
                  }
                  else {
                    bVar13 = true;
                  }
                  if (bVar13) {
                    local_48 = (ushort)uVar4;
                    iVar6 = FUN_00479555(local_4c,local_48);
                    if ((ushort)iVar6 <=
                        (ushort)((ushort)pUVar11->raio_visao * (ushort)pUVar11->raio_visao)) {
                      bVar13 = (ushort)iVar6 < (ushort)local_2c;
                      if (bVar13) {
                        bVar3 = true;
                        local_44 = iVar9;
                        local_2c = iVar6;
                      }
                    }
                  }
                }
              }
            }
          }
          uVar8 = local_38 + 1;
          local_38 = uVar8;
        }
      }
      local_38 = local_38 + (0x100 - uVar10);
    }
    if (!bVar3) {
      local_44 = 0xffff;
    }
  }
  return CONCAT44(param_2,local_44);
}
