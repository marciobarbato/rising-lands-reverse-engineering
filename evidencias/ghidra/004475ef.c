/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004475ef, entrada 004475ef.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004475ef(undefined4 param_1,uint param_2)

{
  bool bVar1;
  byte in_AL;
  UnidadeParcial *pUVar2;
  uint uVar3;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_EDX;
  longlong lVar4;

  for (uVar3 = 0; (uVar3 & 0xffff) < 800; uVar3 = uVar3 + 1) {
    if ((tabela_unidades[uVar3 & 0xffff].estado == 0) ||
       (tabela_unidades[uVar3 & 0xffff].estado == 4)) {
      bVar1 = false;
    }
    else {
      bVar1 = true;
    }
    if (bVar1) {
      pUVar2 = tabela_unidades + (uVar3 & 0xffff);
      param_2 = CONCAT31((int3)(param_2 >> 8),in_AL);
      if (in_AL == pUVar2->proprietario_id) {
        lVar4 = FUN_004475ac(uVar3,param_2);
        uVar3 = FUN_00428cc0(extraout_ECX,1);
        pUVar2->campo_0c = (short)uVar3 + (short)lVar4;
        uVar3 = extraout_ECX_00;
        param_2 = extraout_EDX;
      }
    }
  }
  return;
}
