/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall OriginaisSBL::EnginGetEtat(undefined4 param_1,undefined4 param_2)

{
  ushort in_AX;

  return CONCAT44(param_2,CONCAT31((int3)((uint)tabela_unidades >> 8),tabela_unidades[in_AX].estado)
                 );
}
