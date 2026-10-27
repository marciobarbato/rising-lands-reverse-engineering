/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void OriginaisSBL::SetDeplaceEngin(void)

{
  UnidadeParcial *pUVar1;
  short sVar2;
  uint in_EAX;
  ushort extraout_CX;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 uVar3;
  uint extraout_EDX;
  uint uVar4;
  int extraout_EDX_00;
  longlong lVar5;

  sVar2 = (short)in_EAX;
  ResetOrdre();
  *(undefined1 *)(extraout_EDX + 0x88) = 0;
  if (sVar2 == DAT_00496304) {
    DAT_004e0f36 = 0;
    DAT_004e0f37 = 0;
    DAT_004e0f3c = 0;
    DAT_00496304 = -1;
  }
  uVar3 = extraout_ECX;
  uVar4 = extraout_EDX;
  if (*(char *)(extraout_EDX + 1) == '\x06') {
    lVar5 = TerrainEstCaisse(extraout_ECX,extraout_EDX);
    uVar4 = (uint)((ulonglong)lVar5 >> 0x20);
    uVar3 = extraout_ECX_00;
    if ((char)lVar5 != '\0') {
      ResetOrdre();
      *(undefined1 *)(extraout_EDX_00 + 2) = 5;
      *(undefined1 *)(extraout_EDX_00 + 0x89) = 1;
      pUVar1 = tabela_unidades;
      tabela_unidades[in_EAX & 0xffff].celula_destino = extraout_CX;
      if (sVar2 == DAT_00496304) {
        DAT_004e0f36 = 0;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = -1;
      }
      pUVar1[in_EAX & 0xffff].estado_caminho = 0;
      *(ushort *)(extraout_EDX_00 + 0xb2) = extraout_CX;
      FUN_00445f27();
      return;
    }
  }
  pUVar1 = tabela_unidades;
  tabela_unidades[in_EAX & 0xffff].celula_destino = (ushort)uVar3;
  if (sVar2 == DAT_00496304) {
    DAT_004e0f36 = (byte)in_EAX ^ (byte)DAT_00496304;
    DAT_004e0f3c = 0;
    DAT_004e0f37 = (byte)(in_EAX >> 8) ^ (byte)((ushort)DAT_00496304 >> 8);
    DAT_00496304 = -1;
  }
  pUVar1[in_EAX & 0xffff].estado_caminho = 0;
  *(undefined1 *)(uVar4 + 2) = 2;
  *(undefined2 *)(uVar4 + 0xb8) = 0xffff;
  *(undefined2 *)(uVar4 + 0xb2) = 0xffff;
  *(undefined1 *)(uVar4 + 0xbe) = 0xff;
  *(undefined2 *)(uVar4 + 0xc0) = 0xffff;
  FUN_00445f27();
  return;
}
