/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004864c1, entrada 004864c1.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

ulonglong __fastcall FUN_004864c1(undefined *param_1,undefined4 param_2)

{
  int iVar1;
  uint uVar2;
  undefined *puVar3;
  undefined *puVar4;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 uVar5;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined8 uVar6;
  undefined *local_24;
  int local_1c;

  uVar5 = 0;
  local_1c = 0;
  local_24 = &DAT_0051bcfc;
  do {
    uVar6 = FUN_0046d817(param_1,uVar5);
    uVar5 = (undefined4)((ulonglong)uVar6 >> 0x20);
    if (((uint)uVar6 & 0xff) == 2) {
      *(undefined4 *)(local_24 + 0xc) = 0xff;
      *(undefined4 *)(local_24 + 0x14) = 0xff;
      *(undefined4 *)(local_24 + 0x10) = 0xff;
      iVar1 = FUN_00483bd8(local_1c,9);
      *(int *)(local_24 + 4) = iVar1;
      uVar5 = extraout_EDX;
      if (iVar1 != 0) {
        iVar1 = 0;
        uVar5 = extraout_ECX;
        while( true ) {
          uVar2 = FUN_00483685(uVar5,9);
          uVar5 = extraout_EDX_00;
          if ((uVar2 & 0xffff) == 0xffff) break;
          uVar6 = FUN_00484b96(extraout_ECX_00,extraout_EDX_00);
          uVar5 = (undefined4)((ulonglong)uVar6 >> 0x20);
          if ((int)uVar6 * *(int *)(&DAT_0051bd04 + local_1c * 0x1144) <= iVar1) break;
          FUN_00483286(extraout_ECX_01,(ushort)uVar2);
          FUN_00482939(extraout_ECX_02,(ushort)uVar2);
          iVar1 = iVar1 + *(int *)(&DAT_00498cf4 + (uint)tabela_unidades[uVar2 & 0xffff].tipo_id * 4
                                  );
          uVar5 = extraout_ECX_03;
        }
      }
      puVar4 = local_24;
      do {
        puVar3 = puVar4 + 0x110;
        *(undefined4 *)(puVar4 + 0x28) = 0xffffffff;
        *(undefined4 *)(puVar4 + 0x2c) = 0xffffffff;
        *(undefined4 *)(puVar4 + 0x30) = 0xffffffff;
        *(undefined2 *)(puVar4 + 0x34) = 0;
        *(undefined2 *)(puVar4 + 0x36) = 0;
        puVar4 = puVar3;
      } while (puVar3 != local_24 + 0x1100);
    }
    param_1 = local_24 + 0x1144;
    local_1c = local_1c + 1;
    local_24 = param_1;
    if (3 < local_1c) {
      puVar4 = &DAT_0052020c;
      do {
        puVar3 = puVar4 + 0x110;
        *(undefined4 *)(puVar4 + 0x28) = 0xffffffff;
        *(undefined4 *)(puVar4 + 0x2c) = 0xffffffff;
        *(undefined2 *)(puVar4 + 0x34) = 0;
        *(undefined2 *)(puVar4 + 0x36) = 0;
        puVar4 = puVar3;
      } while (puVar3 != &DAT_0052130c);
      return CONCAT44(param_2,&DAT_0052130c) ^ 0x52130c;
    }
  } while( true );
}
