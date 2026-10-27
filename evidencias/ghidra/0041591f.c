/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0041591f, entrada 0041591f.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0041591f(undefined4 param_1,undefined4 param_2)

{
  UnidadeParcial *pUVar1;
  byte bVar2;
  undefined4 in_EAX;
  undefined4 extraout_ECX;
  short extraout_DX;
  ushort unaff_BX;

  pUVar1 = tabela_unidades;
  bVar2 = tabela_unidades[unaff_BX].estado;
  if (bVar2 < 0x10) {
    if (4 < bVar2) {
      if (bVar2 < 6) {
        FUN_00414a8a(in_EAX,(int)(short)param_2);
        return;
      }
      if (10 < bVar2) {
        if (0xb < bVar2) {
          if (bVar2 < 0xd) {
            return;
          }
          if (bVar2 < 0xe) goto LAB_00415978;
          if (bVar2 != 0xf) {
            return;
          }
        }
        FUN_00414495(in_EAX,(short)param_2);
        return;
      }
      if (9 < bVar2) {
        return;
      }
      goto LAB_00415978;
    }
    if (1 < bVar2) {
      if (3 < bVar2) {
        FUN_0041559a(in_EAX,(int)(short)param_2);
        return;
      }
      goto LAB_00415978;
    }
    if (bVar2 != 1) {
      return;
    }
LAB_004159a6:
    bVar2 = unidade_obter_tipo(unaff_BX);
    in_EAX = extraout_ECX;
    param_2._0_2_ = extraout_DX;
    if ((bVar2 != 0x10) && (pUVar1[unaff_BX].field_0x8a != 0)) {
      if (3 < (byte)pUVar1[unaff_BX].field_0x8a) {
        return;
      }
LAB_00415981:
      FUN_0041374c(in_EAX,(int)(short)param_2);
      return;
    }
  }
  else {
    if (bVar2 < 0x12) goto LAB_00415978;
    if (bVar2 < 0x15) {
      if ((0x12 < bVar2) && (bVar2 < 0x14)) goto LAB_00415978;
    }
    else {
      if (bVar2 < 0x16) goto LAB_00415978;
      if (0x16 < bVar2) {
        if (bVar2 < 0x18) goto LAB_00415978;
        if (0x18 < bVar2) {
          if (bVar2 != 0x1e) {
            return;
          }
          goto LAB_00415978;
        }
        goto LAB_004159a6;
      }
      if (tabela_unidades[unaff_BX].field_0x8a != '\0') {
        if (tabela_unidades[unaff_BX].field_0x8a != '\x01') {
          return;
        }
        goto LAB_00415981;
      }
    }
  }
LAB_00415978:
  FUN_00412390(in_EAX,(int)(short)param_2);
  return;
}
