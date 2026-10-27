/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

longlong __fastcall OriginaisSBL::EnginEstVivant(undefined4 param_1,uint param_2)

{
  ushort in_AX;

  if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
    return (ulonglong)param_2 << 0x20;
  }
  return CONCAT44(param_2,1);
}
