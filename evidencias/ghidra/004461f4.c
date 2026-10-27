/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004461f4, entrada 004461f4.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined4 __fastcall FUN_004461f4(ushort param_1,ushort param_2,ushort param_3)

{
  ushort in_AX;
  ushort uVar1;
  int iVar2;
  undefined1 uVar3;
  undefined1 uVar4;
  ushort uVar5;
  ushort unaff_BX;
  int iVar6;
  uint uVar7;

  iVar6 = CONCAT31((int3)((uint)in_AX * 0x45 >> 8),tabela_unidades[in_AX].tipo_id);
  uVar4 = 0;
  uVar3 = 0;
  switch(tabela_unidades[in_AX].tipo_id) {
  case 0:
  case 1:
  case 2:
  case 4:
  case 5:
  case 6:
  case 7:
  case 8:
  case 9:
  case 10:
  case 0x11:
  case 0x12:
  case 0x13:
  case 0x14:
  case 0x15:
  case 0x16:
  case 0x17:
  case 0x18:
    uVar7 = (uint)tabela_unidades[in_AX].celula_atual;
    uVar3 = uVar4;
    break;
  case 3:
  case 0xb:
  case 0xc:
  case 0xd:
  case 0xe:
  case 0xf:
  case 0x10:
  case 0x19:
    uVar5 = tabela_unidades[in_AX].celula_atual % 0x100;
    uVar1 = tabela_unidades[in_AX].celula_atual / 0x100;
    if ((((param_2 <= uVar5) && (uVar5 <= param_1)) && (unaff_BX <= uVar1)) && (uVar1 <= param_3)) {
      uVar4 = 1;
    }
    iVar6 = tabela_unidades[in_AX].celula_atual - 1;
    uVar1 = (ushort)(iVar6 % 0x100);
    if (((param_2 <= uVar1) && (uVar1 <= param_1)) &&
       ((uVar1 = (ushort)(iVar6 / 0x100), unaff_BX <= uVar1 && (uVar1 <= param_3)))) {
      uVar4 = 1;
    }
    iVar6 = tabela_unidades[in_AX].celula_atual - 0x101;
    uVar1 = (ushort)(iVar6 % 0x100);
    if (((param_2 <= uVar1) && (uVar1 <= param_1)) &&
       ((uVar1 = (ushort)(iVar6 / 0x100), unaff_BX <= uVar1 && (uVar1 <= param_3)))) {
      uVar4 = 1;
    }
    uVar7 = tabela_unidades[in_AX].celula_atual - 0x100;
    uVar3 = uVar4;
    break;
  default:
    goto switchD_00446230_default;
  }
  iVar2 = (uVar7 + ((int)uVar7 >> 0x1f) * -0x100) - (uint)(((int)uVar7 >> 0x1f) << 7 < 0);
  iVar6 = iVar2 >> 8;
  uVar1 = (ushort)((int)uVar7 % 0x100);
  if ((((param_2 <= uVar1) && (uVar1 <= param_1)) &&
      (uVar1 = (ushort)((uint)iVar2 >> 8), unaff_BX <= uVar1)) && (uVar1 <= param_3)) {
    uVar3 = 1;
  }
switchD_00446230_default:
  return CONCAT31((int3)((uint)iVar6 >> 8),uVar3);
}
