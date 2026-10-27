/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00451464, entrada 00451464.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_00451464(undefined4 param_1,undefined4 param_2)

{
  UnidadeParcial *pUVar1;
  UnidadeParcial *pUVar2;
  byte bVar3;
  ushort in_AX;
  ushort uVar4;
  uint uVar5;
  int iVar6;
  uint unaff_EDI;
  bool bVar7;

  pUVar1 = tabela_unidades + in_AX;
  uVar5 = 0xffff;
  uVar4 = 0xffff;
  bVar3 = pUVar1->field_0xb7;
  if (bVar3 < 3) {
    if (bVar3 == 1) {
      uVar4 = tabela_unidades[*(ushort *)&pUVar1->field_0xb8].celula_passo;
    }
  }
  else if (bVar3 < 4) {
    if ((pUVar1->alcance_quadrado_u8 == 0) || (pUVar1->alcance_quadrado_u8 == 1)) {
      uVar5 = FUN_004239a0(pUVar1,(uint)tabela_unidades[in_AX].celula_passo);
    }
    uVar4 = (ushort)uVar5;
    if ((uVar5 & 0xffff) == 0xffff) {
      uVar4 = FUN_0041aee2();
    }
  }
  else if (bVar3 == 5) {
    uVar4 = *(ushort *)&pUVar1->field_0xb8;
  }
  pUVar2 = tabela_unidades;
  if ((pUVar1->tipo_id == 0xf) || (pUVar1->tipo_id == 0xc)) {
    bVar3 = pUVar1->field_0xb7;
    if (bVar3 < 3) {
      if (bVar3 == 1) {
        unaff_EDI = (uint)tabela_unidades[*(ushort *)&pUVar1->field_0xb8].celula_passo;
      }
    }
    else if (bVar3 < 4) {
      unaff_EDI = FUN_0041aee2();
    }
    else if (bVar3 == 5) {
      unaff_EDI = (uint)*(ushort *)&pUVar1->field_0xb8;
    }
    iVar6 = FUN_004796cb((unaff_EDI & 0xffff) >> 8,(int)(uint)pUVar2[in_AX].celula_atual >> 8,0x20);
    bVar7 = (char)iVar6 == pUVar1->field_0x94;
  }
  else {
    iVar6 = FUN_004796cb((uint)(uVar4 >> 8),(int)(uint)pUVar1->celula_atual >> 8,8);
    bVar3 = (char)iVar6 * '\x02' - 1;
    iVar6 = CONCAT31((int3)((uint)iVar6 >> 8),bVar3);
    if (pUVar1->tipo_id == 3) {
      iVar6 = (bVar3 + 0xb) % 0x10 + 1;
    }
    bVar7 = (char)iVar6 == pUVar1->field_0x91;
  }
  return CONCAT44(param_2,CONCAT31((int3)((uint)iVar6 >> 8),bVar7));
}
