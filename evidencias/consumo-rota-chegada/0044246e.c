/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall OriginaisSBL::EnginOccupeCase(undefined4 param_1,ushort param_2)

{
  byte bVar1;
  ushort uVar2;
  ushort uVar3;
  ushort in_AX;
  UnidadeParcial *pUVar4;
  uint3 uVar6;
  uint uVar5;
  uint uVar7;
  char unaff_BL;
  undefined1 uVar8;
  bool bVar9;
  bool bVar10;

  pUVar4 = tabela_unidades + in_AX;
  uVar8 = 1;
  uVar2 = pUVar4->celula_atual;
  uVar3 = pUVar4->celula_passo;
  uVar6 = (uint3)((uint)pUVar4 >> 8);
  if ((((pUVar4->field_0xab != '\0') && (unaff_BL == '\x01')) ||
      ((pUVar4->field_0xab == '\0' && (unaff_BL == '\x02')))) || (pUVar4->estado == 0xe)) {
    return (uint)uVar6 << 8;
  }
  bVar1 = pUVar4->tipo_id;
  uVar5 = CONCAT31(uVar6,bVar1);
  if (bVar1 < 0xe) {
    if (bVar1 < 6) {
      bVar9 = bVar1 < 3;
      bVar10 = bVar1 == 3;
      if (!bVar9) {
LAB_004424fb:
        if (bVar9 || bVar10) goto LAB_00442522;
      }
    }
    else if ((8 < bVar1) && (10 < bVar1)) goto LAB_00442522;
LAB_004424fd:
    if ((uVar2 != param_2) && (uVar3 != param_2)) {
LAB_00442571:
      uVar8 = 0;
      goto LAB_00442573;
    }
  }
  else {
    if (0xe < bVar1) {
      if (bVar1 < 0x12) {
        bVar9 = bVar1 < 0x10;
        bVar10 = bVar1 == 0x10;
        if (!bVar9) goto LAB_004424fb;
      }
      else {
        if ((((bVar1 < 0x13) || (bVar1 < 0x14)) || (bVar1 < 0x17)) || (bVar1 < 0x19))
        goto LAB_004424fd;
        if (bVar1 != 0x19) goto LAB_00442573;
      }
    }
LAB_00442522:
    if (uVar2 != param_2) {
      uVar7 = (uint)uVar2;
      uVar5 = (uint)param_2;
      if ((((uVar7 - 1 != uVar5) && (uVar7 - 0x101 != uVar5)) &&
          ((uVar7 - 0x100 != uVar5 &&
           (((uVar3 != param_2 && (uVar7 = (uint)uVar3, uVar7 - 1 != uVar5)) &&
            (uVar7 - 0x101 != uVar5)))))) && (uVar7 - 0x100 != uVar5)) goto LAB_00442571;
    }
  }
  uVar8 = 1;
LAB_00442573:
  return CONCAT31((int3)(uVar5 >> 8),uVar8);
}
