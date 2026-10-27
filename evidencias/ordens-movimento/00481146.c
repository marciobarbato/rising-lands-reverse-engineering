/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall OriginaisSBL::V_DeplacerUnite(undefined4 param_1,undefined4 param_2)

{
  uint in_EAX;
  longlong lVar1;

  lVar1 = EnginEstVivant(param_1,in_EAX);
  if ((char)lVar1 != '\0') {
    SetDeplaceEngin();
  }
  return CONCAT44(param_2,1);
}
