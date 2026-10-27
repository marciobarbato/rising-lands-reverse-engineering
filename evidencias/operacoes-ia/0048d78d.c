/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_0048d78d(undefined4 param_1,char *param_2)

{
  char cVar1;
  int iVar2;
  char *pcVar3;
  byte *pbVar4;
  char *pcVar5;
  undefined8 uVar6;
  byte local_110 [256];

  pbVar4 = local_110;
  do {
    cVar1 = *param_2;
    *pbVar4 = cVar1;
    if (cVar1 == '\0') break;
    cVar1 = param_2[1];
    param_2 = param_2 + 2;
    pbVar4[1] = cVar1;
    pbVar4 = pbVar4 + 2;
  } while (cVar1 != '\0');
  pcVar3 = &DAT_004955db;
  iVar2 = -1;
  pbVar4 = local_110;
  do {
    pcVar5 = (char *)pbVar4;
    if (iVar2 == 0) break;
    iVar2 = iVar2 + -1;
    pcVar5 = (char *)(pbVar4 + 1);
    cVar1 = *pbVar4;
    pbVar4 = (byte *)pcVar5;
  } while (cVar1 != '\0');
  pcVar5 = pcVar5 + -1;
  do {
    cVar1 = *pcVar3;
    *pcVar5 = cVar1;
    if (cVar1 == '\0') break;
    cVar1 = pcVar3[1];
    pcVar3 = pcVar3 + 2;
    pcVar5[1] = cVar1;
    pcVar5 = pcVar5 + 2;
  } while (cVar1 != '\0');
  uVar6 = OriginaisSBL::strstr(iVar2,local_110);
  return uVar6;
}
