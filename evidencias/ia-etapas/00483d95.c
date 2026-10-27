/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN_00483d95(uint param_1)

{
  int iVar1;
  uint uVar2;
  UnidadeParcial *pUVar3;
  int in_EAX;
  uint uVar4;
  uint extraout_ECX;
  uint extraout_ECX_00;
  undefined4 *puVar5;
  int local_34;

  local_34 = 4;
  do {
    while (iVar1 = *(int *)((int)&DAT_0051b664 + local_34 + in_EAX * 0x60), iVar1 == -1) {
      local_34 = local_34 + 4;
      if (local_34 == 0x50) {
        return;
      }
    }
    puVar5 = &DAT_0051a9e0 + iVar1 * 8;
    uVar4 = param_1;
    if (puVar5 != (undefined4 *)0x0) {
      while( true ) {
        uVar4 = param_1;
        if ((&DAT_0051a9f2)[iVar1 * 0x10] == 0) break;
        if (puVar5 == (undefined4 *)0x0) {
LAB_00483e29:
          uVar4 = 0xffff;
        }
        else {
          DAT_0051b848 = (&DAT_0051a9f0)[iVar1 * 0x10];
          uVar4 = (uint)DAT_0051b848;
          if (uVar4 == 0xffff) goto LAB_00483e29;
        }
        _DAT_0051b844 = puVar5;
        if (uVar4 == 0xffff) break;
        FUN_004832b1(uVar4,(ushort)uVar4);
        pUVar3 = tabela_unidades;
        uVar2 = (&DAT_0051b664)[in_EAX * 0x18];
        param_1 = extraout_ECX;
        if ((uVar2 != 0xffffffff) && ((uVar2 & 0x7ffffff) != 0x7fd72b1)) {
          *(undefined2 *)&tabela_unidades[uVar4].field_0x108 = (&DAT_0051a9f0)[uVar2 * 0x10];
          *(uint *)&pUVar3[uVar4].field_0x10c = uVar2;
          (&DAT_0051a9f0)[uVar2 * 0x10] = (short)extraout_ECX;
          (&DAT_0051a9f2)[uVar2 * 0x10] = (&DAT_0051a9f2)[uVar2 * 0x10] + 1;
        }
      }
    }
    FUN_00483ce7(uVar4,iVar1);
    param_1 = extraout_ECX_00;
  } while( true );
}
