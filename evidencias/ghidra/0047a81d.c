/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0047a81d, entrada 0047a81d.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0047a81d(undefined4 param_1,byte param_2)

{
  byte bVar1;
  ushort uVar2;
  int iVar3;
  uint uVar4;
  int extraout_ECX;
  int iVar5;
  undefined4 extraout_ECX_00;
  int extraout_ECX_01;
  int extraout_ECX_02;
  int extraout_ECX_03;
  undefined4 extraout_ECX_04;
  int iVar6;
  int local_1c;

  if ((((param_2 != 0xff) && (DAT_0050b178 < 0x32)) && (DAT_0050b134 < 0x10)) &&
     (iVar3 = FUN_00483bd8(param_1,0x10), iVar3 != -1)) {
    local_1c = 0;
    iVar5 = extraout_ECX;
    do {
      bVar1 = (&DAT_0050af84)[(uint)param_2 * 0x1a + local_1c];
      for (iVar6 = 0; iVar6 < (int)(uint)bVar1; iVar6 = iVar6 + 1) {
        uVar4 = FUN_00479f20(iVar5,(ushort)local_1c);
        iVar5 = extraout_ECX_02;
        if ((uVar4 & 0xffff) != 0xffff) {
          uVar2 = FUN_00457e6c(4);
          iVar5 = extraout_ECX_03;
          if (uVar2 != 0xffff) {
            DAT_0050b178 = DAT_0050b178 + 1;
            FUN_00443108(extraout_ECX_03,4);
            FUN_00456fa6();
            FUN_004704dc(extraout_ECX_04,tabela_unidades + uVar2);
            FUN_0046e44c(0,0,0,0,0);
            FUN_00482939(extraout_ECX_00,uVar2);
            iVar5 = extraout_ECX_01;
          }
        }
      }
      iVar5 = local_1c + 1;
      local_1c = iVar5;
    } while (iVar5 < 0x1a);
    uVar4 = (uint)DAT_0050b134;
    DAT_0050b134 = DAT_0050b134 + 1;
    *(int *)(&DAT_0050b138 + uVar4 * 4) = iVar3;
  }
  return;
}
