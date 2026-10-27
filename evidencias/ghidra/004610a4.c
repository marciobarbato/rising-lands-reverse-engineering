/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004610a4, entrada 004610a4.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004610a4(undefined4 param_1,undefined4 param_2)

{
  ushort uVar1;
  bool bVar2;
  char cVar3;
  byte bVar4;
  ushort uVar5;
  ushort indice_unidade;
  int in_EAX;
  int extraout_ECX;
  int extraout_ECX_00;
  undefined4 extraout_ECX_01;
  int extraout_ECX_02;
  int iVar6;
  int extraout_ECX_03;
  int extraout_ECX_04;
  undefined4 uVar7;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  undefined4 extraout_EDX_02;
  undefined8 uVar8;

  uVar8 = FUN_0046d817(param_1,param_2);
  if (((uint)uVar8 & 0xff) == 2) {
    uVar7 = 0;
    bVar2 = false;
    iVar6 = extraout_ECX;
    for (uVar1 = 0; uVar1 < 10; uVar1 = uVar1 + 1) {
      if (*(short *)(&DAT_004e296c + (uint)uVar1 * 2 + in_EAX * 0x14) != -1) {
        FUN_00418a74(iVar6,uVar7);
        uVar5 = FUN_00447107();
        uVar7 = extraout_EDX;
        for (iVar6 = extraout_ECX_00; (ushort)iVar6 < uVar5; iVar6 = iVar6 + 1) {
          cVar3 = FUN_004472d3(iVar6,0);
          iVar6 = extraout_ECX_03;
          uVar7 = extraout_EDX_01;
          if (cVar3 == '\x01') {
            indice_unidade = FUN_004472de(extraout_ECX_03,0);
            bVar4 = unidade_obter_tipo(indice_unidade);
            if ((bVar4 != 9) || (bVar2)) {
              FUN_004473cf(extraout_ECX_04,1);
              FUN_0044115f(extraout_ECX_01,0);
              iVar6 = extraout_ECX_02;
              uVar7 = extraout_EDX_00;
            }
            else {
              bVar2 = true;
              iVar6 = extraout_ECX_04;
              uVar7 = extraout_EDX_02;
            }
          }
        }
      }
    }
  }
  return;
}
