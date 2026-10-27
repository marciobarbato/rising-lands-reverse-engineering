/* Pseudocódigo Ghidra, não é fonte original.
 * Função unidade_vida_diferente_do_maximo, entrada 004420a6.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Unknown calling convention */
/* Assinatura recuperada: índice em AX, resultado em AL. Convenção interna por registradores;
   não presumir stdcall/fastcall. */

bool unidade_vida_diferente_do_maximo(ushort indice_unidade)

{
  return *(ushort *)(&DAT_004965b6 + (uint)tabela_unidades[indice_unidade].tipo_id * 0x32) !=
         tabela_unidades[indice_unidade].vida;
}
