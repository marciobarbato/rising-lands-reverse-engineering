/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00446fbf, entrada 00446fbf.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_00446fbf(undefined4 param_1,byte param_2)

{
  byte bVar1;
  ushort in_AX;
  uint uVar2;

  bVar1 = tabela_unidades[in_AX].proprietario_id;
  uVar2 = CONCAT31((int3)((uint)in_AX * 0x45 >> 8),bVar1);
  if ((param_2 != bVar1) && ((param_2 == 4 || (uVar2 = (uint)bVar1, uVar2 == 4)))) {
LAB_0044701d:
    return CONCAT31((int3)(uVar2 >> 8),1);
  }
  uVar2 = CONCAT11(bVar1,param_2) & 0xff;
  if ((uVar2 != 200) && ((bVar1 != 200 && (bVar1 != param_2)))) {
    uVar2 = FUN_0046d838(param_1,bVar1);
    if ((char)uVar2 == '\0') goto LAB_0044701d;
  }
  return uVar2 & 0xffffff00;
}
