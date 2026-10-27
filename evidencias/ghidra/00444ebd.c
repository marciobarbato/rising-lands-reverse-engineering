/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00444ebd, entrada 00444ebd.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00444ebd(undefined4 param_1,ushort param_2)

{
  UnidadeParcial *pUVar1;
  uint in_EAX;
  int extraout_ECX;
  int extraout_EDX;
  int iVar2;
  int iVar3;

  FUN_0044357c();
  pUVar1 = tabela_unidades;
  iVar2 = (in_EAX & 0xffff) * 0x44 + extraout_ECX;
  iVar3 = iVar2 * 4;
  (&tabela_unidades->celula_destino)[iVar2 * 2] = param_2;
  iVar2 = extraout_EDX + iVar3;
  if ((short)in_EAX == DAT_00496304) {
    DAT_004e0f36 = (byte)in_EAX ^ (byte)DAT_00496304;
    DAT_004e0f37 = (byte)(in_EAX >> 8) ^ (byte)((ushort)DAT_00496304 >> 8);
    DAT_00496304 = -1;
    DAT_004e0f3c = 0;
  }
  (&pUVar1->estado_caminho)[iVar3] = 0;
  *(undefined1 *)(iVar2 + 0x89) = 0;
  *(undefined1 *)(iVar2 + 2) = 5;
  *(undefined1 *)(iVar2 + 0x82) = 0;
  *(ushort *)(iVar2 + 0xb2) = param_2;
  return;
}
