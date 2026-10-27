/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall OriginaisSBL::V_DeplaceGroupe(undefined4 param_1,undefined4 param_2)

{
  undefined4 in_EAX;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 uVar1;
  undefined4 extraout_ECX_02;
  uint uVar2;
  UnidadeParcial *pUVar3;
  UnidadeParcial *extraout_EDX;
  undefined8 uVar4;
  longlong lVar5;

  uVar4 = iagUnitGetFirstUnitInGroup(in_EAX,param_2);
  uVar1 = extraout_ECX;
  while (uVar2 = (uint)uVar4 & 0xffff, uVar2 != 0xffff) {
    lVar5 = EnginEstVivant(uVar1,uVar2);
    pUVar3 = (UnidadeParcial *)((ulonglong)lVar5 >> 0x20);
    uVar1 = extraout_ECX_00;
    if (((char)lVar5 != '\0') &&
       ((pUVar3 = tabela_unidades + (int)pUVar3, pUVar3->estado != 1 ||
        (*(short *)&pUVar3->field_0xb8 == -1)))) {
      SetDeplaceEngin();
      uVar1 = extraout_ECX_01;
      pUVar3 = extraout_EDX;
    }
    uVar4 = iagUnitGetNextUnitInGroup(uVar1,pUVar3);
    uVar1 = extraout_ECX_02;
  }
  return CONCAT44(param_2,1);
}
