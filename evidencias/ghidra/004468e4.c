/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004468e4, entrada 004468e4.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_004468e4(undefined4 param_1)

{
  ulonglong uVar1;
  ulonglong uVar2;
  ushort in_AX;
  UnidadeParcial *pUVar3;
  int iVar4;
  uint uVar5;
  uint extraout_ECX;
  uint uVar6;
  uint local_28;
  uint local_20;
  uint local_1c;

  pUVar3 = tabela_unidades + in_AX;
  if ((*(int *)&pUVar3->field_0x83 >> 0x18 == 0) && (*(int *)&pUVar3->field_0x84 >> 0x18 == 0)) {
    switch(pUVar3->tipo_id) {
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
      local_1c = CONCAT22(local_1c._2_2_,1);
      local_28 = CONCAT22(local_28._2_2_,1);
      break;
    case 3:
    case 0xb:
    case 0xc:
    case 0xd:
    case 0xe:
    case 0xf:
    case 0x10:
    case 0x19:
      local_1c = CONCAT22(local_1c._2_2_,2);
      local_28 = CONCAT22(local_28._2_2_,2);
    }
    uVar5 = CONCAT22((short)((uint)param_1 >> 0x10),pUVar3->celula_atual) -
            ((local_28 - 1) * 0x100 + local_1c + -1);
    uVar6 = uVar5 & 0xffff;
    if (((ulonglong)uVar5 & 0xffffffff0000ffff) % 0x100 == 0) {
      local_1c = local_1c - 1;
    }
    else {
      uVar5 = uVar5 - 1;
    }
    if ((int)uVar6 >> 8 == 0) {
      local_28 = local_28 - 1;
    }
    else {
      uVar5 = uVar5 - 0x100;
    }
    uVar1 = (ulonglong)uVar5;
    uVar2 = (ulonglong)uVar5;
    for (local_20 = 0; pUVar3 = (UnidadeParcial *)(local_20 & 0xffff),
        pUVar3 < (UnidadeParcial *)((local_28 & 0xffff) + 2); local_20 = local_20 + 1) {
      if (&pUVar3->proprietario_id + (int)((uVar2 & 0xffffffff0000ffff) / 0x100) < (byte *)0x100) {
        for (uVar6 = 0; (uVar6 & 0xffff) < (local_1c & 0xffff) + 2; uVar6 = uVar6 + 1) {
          if (((uVar6 & 0xffff) + (int)((uVar1 & 0xffffffff0000ffff) % 0x100) < 0x100) &&
             (iVar4 = FUN_0044246e(uVar5,(ushort)uVar5), uVar5 = extraout_ECX, (char)iVar4 != '\0'))
          {
            return CONCAT31((int3)((uint)iVar4 >> 8),1);
          }
          uVar5 = uVar5 + 1;
        }
      }
      uVar5 = uVar5 + (0xfe - local_1c);
    }
  }
  return (uint)pUVar3 & 0xffffff00;
}
