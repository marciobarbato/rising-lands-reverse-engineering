/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00474169, entrada 00474169.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

ulonglong __fastcall FUN_00474169(undefined4 param_1,undefined4 param_2)

{
  byte *pbVar1;
  uint in_EAX;
  UnidadeParcial *pUVar2;
  undefined8 uVar3;

  pUVar2 = tabela_unidades + (in_EAX & 0xffff);
  if ((pUVar2->estado != 0xe) &&
     (((pbVar1 = &pUVar2->tipo_id, *pbVar1 != 0x10 || (pUVar2->estado != 0xd)) ||
      (pUVar2 = (UnidadeParcial *)(uint)(byte)pUVar2->field_0xab, pUVar2 == (UnidadeParcial *)0x32))
     )) {
    uVar3 = FUN_004465bf((uint)*pbVar1,in_EAX);
    pUVar2 = (UnidadeParcial *)uVar3;
    if ((char)uVar3 != '\0') {
      return CONCAT44(param_2,CONCAT31((int3)((ulonglong)uVar3 >> 8),1));
    }
  }
  return CONCAT44(param_2,pUVar2) & 0xffffffffffffff00;
}
