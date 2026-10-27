/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00443470, entrada 00443470.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

uint __fastcall FUN_00443470(undefined4 param_1,uint param_2)

{
  uint in_EAX;
  UnidadeParcial *pUVar1;
  uint uVar2;
  undefined4 extraout_ECX;
  undefined8 uVar3;

  uVar3 = FUN_00446693(in_EAX & 0xffff,param_2 & 0xffff);
  pUVar1 = (UnidadeParcial *)uVar3;
  _DAT_004e1a34 = (ushort)uVar3;
  uVar2 = (uint)_DAT_004e1a34;
  if (((uVar2 == 0xffff) ||
      (pUVar1 = tabela_unidades + uVar2,
      pUVar1->proprietario_id !=
      (&tabela_unidades->proprietario_id)
      [((param_2 & 0xffff) * 0x44 + (int)((ulonglong)uVar3 >> 0x20)) * 4])) ||
     (pUVar1->celula_atual != pUVar1->celula_destino)) {
    return (uint)pUVar1 & 0xffffff00;
  }
  uVar2 = FUN_0044330c(extraout_ECX,uVar2);
  _DAT_004e1a36 = (undefined2)uVar2;
  if ((uVar2 & 0xffff) != 0xffff) {
    uVar2 = FUN_004457d3();
  }
  return CONCAT31((int3)(uVar2 >> 8),1);
}
