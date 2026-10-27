/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00442586, entrada 00442586.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall FUN_00442586(undefined4 param_1,ushort param_2)

{
  byte bVar1;
  ushort uVar2;
  ushort in_AX;
  UnidadeParcial *pUVar3;
  uint3 uVar5;
  uint uVar4;
  undefined1 uVar6;
  uint uVar7;
  char unaff_BL;
  bool bVar8;
  bool bVar9;

  pUVar3 = tabela_unidades + in_AX;
  uVar6 = 1;
  uVar2 = pUVar3->celula_atual;
  uVar5 = (uint3)((uint)pUVar3 >> 8);
  if ((((pUVar3->field_0xab == '2') && (unaff_BL == '\x01')) ||
      ((pUVar3->field_0xab == '\0' && (unaff_BL == '\x02')))) || (pUVar3->estado == 0xe)) {
    return (uint)uVar5 << 8;
  }
  bVar1 = pUVar3->tipo_id;
  uVar4 = CONCAT31(uVar5,bVar1);
  if (bVar1 < 0xe) {
    if (bVar1 < 6) {
      bVar8 = bVar1 < 3;
      bVar9 = bVar1 == 3;
      if (!bVar8) {
LAB_00442615:
        if (bVar8 || bVar9) goto LAB_0044262c;
      }
    }
    else if ((8 < bVar1) && (10 < bVar1)) goto LAB_0044262c;
LAB_00442617:
    if (uVar2 != param_2) {
LAB_00442656:
      uVar6 = 0;
      goto LAB_00442660;
    }
  }
  else {
    if (0xe < bVar1) {
      if (bVar1 < 0x12) {
        bVar8 = bVar1 < 0x10;
        bVar9 = bVar1 == 0x10;
        if (!bVar8) goto LAB_00442615;
      }
      else {
        if ((((bVar1 < 0x13) || (bVar1 < 0x14)) || (bVar1 < 0x17)) || (bVar1 < 0x19))
        goto LAB_00442617;
        if (bVar1 != 0x19) goto LAB_00442660;
      }
    }
LAB_0044262c:
    if (uVar2 != param_2) {
      uVar7 = (uint)uVar2;
      uVar4 = (uint)param_2;
      if (((uVar7 - 1 != uVar4) && (uVar7 - 0x101 != uVar4)) && (uVar7 - 0x100 != uVar4))
      goto LAB_00442656;
    }
  }
  uVar6 = 1;
LAB_00442660:
  return CONCAT31((int3)(uVar4 >> 8),uVar6);
}
