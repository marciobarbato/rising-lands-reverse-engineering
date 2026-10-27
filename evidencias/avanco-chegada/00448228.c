/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

ulonglong __fastcall OriginaisSBL::EnginEstArrive(undefined4 param_1,undefined4 param_2)

{
  undefined1 *puVar1;
  ushort in_AX;
  UnidadeParcial *pUVar2;

  pUVar2 = tabela_unidades + in_AX;
  if ((pUVar2->celula_destino == pUVar2->celula_atual) && (*(int *)&pUVar2->field_0x83 >> 0x18 == 0)
     ) {
    puVar1 = &pUVar2->field_0x84;
    pUVar2 = (UnidadeParcial *)(*(int *)puVar1 >> 0x18);
    if (pUVar2 == (UnidadeParcial *)0x0) {
      return CONCAT44(param_2,CONCAT31((int3)(*(int *)puVar1 >> 0x1f),1));
    }
  }
  return CONCAT44(param_2,pUVar2) & 0xffffffffffffff00;
}
