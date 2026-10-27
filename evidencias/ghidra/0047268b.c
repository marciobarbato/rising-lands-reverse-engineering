/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0047268b, entrada 0047268b.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0047268b(undefined4 param_1,uint param_2)

{
  byte in_AL;
  byte bVar1;
  UnidadeParcial *pUVar2;
  uint uVar3;
  int iVar4;
  int extraout_ECX;
  undefined4 extraout_ECX_00;
  int extraout_ECX_01;
  undefined4 extraout_EDX;
  UnidadeParcial *extraout_EDX_00;
  longlong lVar5;

  uVar3 = 0;
  while ((uVar3 & 0xffff) < 800) {
    lVar5 = FUN_00443dad(uVar3,param_2);
    iVar4 = extraout_ECX;
    param_2 = (uint)(UnidadeParcial *)((ulonglong)lVar5 >> 0x20);
    if ((char)lVar5 != '\0') {
      pUVar2 = tabela_unidades + (uVar3 & 0xffff);
      param_2 = (uint)tabela_unidades;
      if (((pUVar2->selecionada != 0) &&
          (param_2 = CONCAT31((int3)((uint)tabela_unidades >> 8),pUVar2->proprietario_id),
          pUVar2->proprietario_id == in_AL)) && (pUVar2->selecionada != 0)) {
        pUVar2->selecionada = 0;
        bVar1 = unidade_obter_proprietario((ushort)uVar3);
        FUN_00472576(extraout_ECX_00,CONCAT31((int3)((uint)extraout_EDX >> 8),bVar1));
        iVar4 = extraout_ECX_01;
        param_2 = (uint)extraout_EDX_00;
      }
    }
    uVar3 = iVar4 + 1;
  }
  return;
}
