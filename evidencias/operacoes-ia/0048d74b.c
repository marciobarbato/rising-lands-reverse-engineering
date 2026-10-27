/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_0048d74b(void)

{
  uint uVar1;
  int *piVar2;

  piVar2 = DAT_00522234;
  while( true ) {
    if (*piVar2 == -1) {
      DAT_00522238 = 0;
      return;
    }
    uVar1 = OriginaisSBL::strcmp(piVar2[1],(uint *)s__debugGetPC_004955ce);
    if (uVar1 == 0) break;
    piVar2 = piVar2 + 2;
  }
  DAT_00522238 = 0x48ff7f - *piVar2;
  return;
}
