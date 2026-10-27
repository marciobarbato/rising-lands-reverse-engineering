/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00440d5e, entrada 00440d5e.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00440d5e(undefined4 param_1,uint param_2)

{
  int iVar1;
  UnidadeParcial *pUVar2;
  ushort in_AX;
  undefined4 uVar3;
  uint uVar4;
  undefined4 extraout_ECX;
  uint extraout_ECX_00;
  undefined1 unaff_BL;
  undefined8 uVar5;

  pUVar2 = tabela_unidades;
  uVar3 = FUN_004766f0(CONCAT31((int3)((uint)param_1 >> 8),unaff_BL),(uint)DAT_00508041);
  if ((char)uVar3 != '\0') {
    uVar5 = FUN_00440c5d(extraout_ECX,param_2 & 0xffff);
    uVar4 = (uint)uVar5;
    if ((int)((ulonglong)uVar5 >> 0x20) == 0x10) {
      uVar4 = 0x100;
    }
    iVar1 = *(int *)&pUVar2[in_AX].field_0x104;
    pUVar2[in_AX].field_0xf9 = (char)extraout_ECX_00;
    if (iVar1 == -1) {
      FUN_0048aa79(extraout_ECX_00 & 0xff,
                   (param_2 & 0xffff) << 8 | (uint)pUVar2[in_AX].tipo_id << 0x10,uVar4);
    }
  }
  return;
}
