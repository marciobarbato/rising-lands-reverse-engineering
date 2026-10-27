/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0043eb64, entrada 0043eb64.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_0043eb64(char param_1,ushort param_2)

{
  ushort uVar1;
  ushort in_AX;
  UnidadeParcial *pUVar2;
  char unaff_BL;
  undefined1 *puVar3;

  pUVar2 = tabela_unidades + in_AX;
  uVar1 = pUVar2->celula_atual;
  if ((((pUVar2->field_0xab == '2') && (unaff_BL == '\x01')) ||
      ((pUVar2->field_0xab == '\0' && (unaff_BL == '\x02')))) ||
     (pUVar2 = (UnidadeParcial *)(uint)pUVar2->estado, pUVar2 == (UnidadeParcial *)0xe)) {
LAB_0043ec05:
    return (uint)pUVar2 & 0xffffff00;
  }
  if (param_1 == '\x01') {
    return (uint)(uVar1 == param_2);
  }
  if (uVar1 != param_2) {
    pUVar2 = (UnidadeParcial *)(uint)uVar1;
    puVar3 = (undefined1 *)(uint)param_2;
    if (((&pUVar2[-1].field_0x113 != puVar3) && (&pUVar2[-1].field_0x13 != puVar3)) &&
       (pUVar2 = (UnidadeParcial *)&pUVar2[-1].field_0x14, pUVar2 != (UnidadeParcial *)puVar3))
    goto LAB_0043ec05;
  }
  return CONCAT31((int3)((uint)pUVar2 >> 8),1);
}
