/* Pseudocódigo Ghidra, não é fonte original.
 * Função unidade_obter_campo_0a, entrada 00442085.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Unknown calling convention */
/* Assinatura recuperada: índice em AX, resultado em AX. Convenção interna por registradores;
   não presumir stdcall/fastcall. */

ushort unidade_obter_campo_0a(ushort indice_unidade)

{
  return tabela_unidades[indice_unidade].campo_0a;
}
