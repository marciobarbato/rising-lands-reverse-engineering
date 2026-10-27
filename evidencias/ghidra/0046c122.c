/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0046c122, entrada 0046c122.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0046c122(undefined4 param_1)

{
  bool bVar1;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  undefined4 extraout_ECX_06;
  undefined4 uVar2;
  undefined4 extraout_ECX_07;
  uint uVar3;
  undefined4 extraout_EDX;
  uint extraout_EDX_00;
  undefined4 extraout_EDX_01;
  ushort uVar4;
  undefined8 uVar5;
  ulonglong uVar6;

  for (uVar4 = 0; uVar3 = (uint)uVar4, uVar4 < 800; uVar4 = uVar4 + 1) {
    bVar1 = unidade_esta_ativa(uVar4);
    param_1 = extraout_ECX;
    if (bVar1) {
      uVar5 = FUN_004465bf(extraout_ECX,extraout_EDX);
      param_1 = extraout_ECX_00;
      if ((char)uVar5 != '\0') {
        FUN_00456fa6();
        param_1 = extraout_ECX_01;
      }
    }
  }
  for (uVar4 = 0; uVar4 < 4; uVar4 = uVar4 + 1) {
    FUN_004475ef(param_1,uVar3);
    param_1 = extraout_ECX_02;
    uVar3 = extraout_EDX_00;
  }
  for (uVar4 = 0; uVar4 < 1000; uVar4 = uVar4 + 1) {
    uVar5 = FUN_0041a735(param_1,(uint)uVar4);
    param_1 = extraout_ECX_03;
    if ((char)uVar5 != '\0') {
      FUN_0041c4ac(extraout_ECX_03,(uint)((ulonglong)uVar5 >> 0x20));
      uVar6 = FUN_0041a5b8(extraout_ECX_04,extraout_EDX_01);
      uVar2 = extraout_ECX_05;
      if ((char)uVar6 != '\0') {
        FUN_0041cc70(extraout_ECX_05);
        uVar2 = extraout_ECX_06;
      }
      FUN_00419e97(uVar2,'\x01');
      param_1 = extraout_ECX_07;
    }
  }
  return;
}
