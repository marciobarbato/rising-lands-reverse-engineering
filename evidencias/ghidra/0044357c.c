/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044357c, entrada 0044357c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_0044357c(void)

{
  UnidadeParcial *pUVar1;
  UnidadeParcial *pUVar2;
  uint in_EAX;
  uint uVar3;
  undefined4 extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_ECX_01;
  undefined4 extraout_EDX;
  longlong lVar4;

  pUVar1 = tabela_unidades;
  uVar3 = in_EAX & 0xffff;
  if (((*(int *)&tabela_unidades[uVar3].field_0x83 >> 0x18 == 0) &&
      (*(int *)&tabela_unidades[uVar3].field_0x84 >> 0x18 == 0)) &&
     (tabela_unidades[uVar3].tipo_id != 0x10)) {
    tabela_unidades[uVar3].contador_animacao = 0;
    pUVar1[uVar3].quadro_movimento = 0;
  }
  if ((pUVar1[uVar3].tipo_id == 0xd) && (*(short *)&pUVar1[uVar3].field_0xc0 != -1)) {
    FUN_004237ff();
    lVar4 = FUN_00420c7c(extraout_ECX,extraout_EDX);
    in_EAX = extraout_ECX_00;
    if ((char)lVar4 != '\0') {
      FUN_0041a65c(extraout_ECX_00,0);
      in_EAX = extraout_ECX_01;
    }
  }
  pUVar2 = tabela_unidades;
  tabela_unidades[in_EAX & 0xffff].celula_destino = pUVar1[uVar3].celula_passo;
  if ((short)in_EAX == DAT_00496304) {
    DAT_004e0f36 = 0;
    DAT_004e0f37 = 0;
    DAT_00496304 = -1;
    DAT_004e0f3c = 0;
  }
  pUVar2[in_EAX & 0xffff].estado_caminho = 0;
  pUVar1[uVar3].field_0x82 = 0;
  *(undefined2 *)&pUVar1[uVar3].field_0xb2 = 0xffff;
  pUVar1[uVar3].estado = 2;
  return;
}
