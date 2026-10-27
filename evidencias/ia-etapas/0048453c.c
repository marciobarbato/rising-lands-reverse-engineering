/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

longlong __fastcall FUN_0048453c(undefined4 param_1,uint param_2)

{
  char cVar1;
  uint in_EAX;
  int iVar2;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  int extraout_ECX_02;
  uint uVar3;
  uint extraout_EDX;
  uint extraout_EDX_00;
  byte *pbVar4;
  int iVar5;
  undefined *puVar6;
  undefined8 uVar7;

  if (DAT_00508f7c % *(uint *)(&DAT_0051b8a4 + in_EAX * 0x7c) == 0) {
    puVar6 = &DAT_0049a0c8;
    iVar5 = 0;
    uVar3 = 0;
    do {
      uVar7 = FUN_0041a735(param_1,uVar3);
      param_1 = extraout_ECX;
      uVar3 = (uint)((ulonglong)uVar7 >> 0x20);
      if ((((char)uVar7 != '\0') && (uVar3 = in_EAX, (byte)puVar6[4] == in_EAX)) &&
         (CONCAT22((short)(in_EAX >> 0x10),*(undefined2 *)(puVar6 + 6)) != 0 && -1 < (int)in_EAX)) {
        iVar2 = FUN_0047d98b(iVar5,2,0,0,0,0,0);
        param_1 = extraout_ECX_00;
        uVar3 = extraout_EDX;
        if (iVar2 == -1) {
          FUN_0047d920(0,2,0,0,0,0);
          param_1 = extraout_ECX_01;
          uVar3 = extraout_EDX_00;
        }
      }
      iVar5 = iVar5 + 1;
      puVar6 = puVar6 + 0x114;
    } while (iVar5 < 1000);
    if (*(char *)(&DAT_0051a98e + in_EAX * 4) != '\0') {
      for (iVar5 = 1; iVar5 < 0xb; iVar5 = iVar5 + 1) {
        pbVar4 = (&PTR_DAT_00498c24)[*(int *)(&DAT_0051b8b0 + in_EAX * 0x7c)];
        for (iVar2 = 0; iVar2 < 0x16; iVar2 = iVar2 + 1) {
          if (iVar5 <= (int)(uint)pbVar4[1]) {
            if ((int)((uint)(ushort)(&DAT_0051b84c)[in_EAX * 0x3e + (uint)*pbVar4] +
                     (uint)(ushort)(&DAT_0051b84c + in_EAX * 0x3e + (uint)*pbVar4)[0x16]) < iVar5) {
              cVar1 = FUN_00418a93(iVar2,*pbVar4);
              iVar2 = extraout_ECX_02;
              if (cVar1 == '\x01') {
                FUN_0047d920(0,1,0,0,0,0);
                goto LAB_0048469c;
              }
            }
          }
          pbVar4 = pbVar4 + 2;
        }
      }
    }
  }
LAB_0048469c:
  return (ulonglong)param_2 << 0x20;
}
