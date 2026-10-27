/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0048270b, entrada 0048270b.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

longlong __fastcall FUN_0048270b(undefined4 param_1,uint param_2)

{
  int iVar1;
  int iVar2;
  uint *puVar3;
  uint extraout_ECX;
  uint uVar4;
  uint extraout_ECX_00;
  uint *puVar5;
  uint *extraout_EDX;
  UnidadeParcial *pUVar6;
  ushort uVar7;
  undefined8 uVar8;
  longlong lVar9;
  uint local_24;
  uint *local_20;
  uint *local_1c;

  iVar2 = 0;
  do {
    iVar1 = iVar2 + 0x20;
    *(undefined4 *)((int)&DAT_0051a9e0 + iVar2) = 0xffffffff;
    *(undefined4 *)((int)&DAT_0051a9e4 + iVar2) = 0xffffffff;
    *(undefined2 *)((int)&DAT_0051a9f2 + iVar2) = 0;
    *(undefined2 *)((int)&DAT_0051a9f4 + iVar2) = 0x7fff;
    *(undefined2 *)((int)&DAT_0051a9f6 + iVar2) = 0xffff;
    *(undefined2 *)((int)&DAT_0051a9f0 + iVar2) = 0xffff;
    puVar3 = (uint *)0x0;
    (&DAT_0051a9fa)[iVar2] = 0xff;
    *(undefined4 *)((int)&DAT_0051a9fc + iVar2) = 0;
    *(undefined4 *)((int)&DAT_0051a9e8 + iVar2) = 0xffffffff;
    (&DAT_0051a9fb)[iVar2] = 0xff;
    *(undefined4 *)((int)&DAT_0051a9ec + iVar2) = 0xffffffff;
    (&DAT_0051a9f8)[iVar2] = 0;
    (&DAT_0051a9f9)[iVar2] = 0;
    iVar2 = iVar1;
  } while (iVar1 != 0xc80);
  puVar5 = &DAT_0051b664;
  DAT_0051b660 = 0;
  local_24 = 0;
  local_1c = &DAT_0051b664;
  local_20 = &DAT_0051b6b4;
  do {
    uVar8 = FUN_0046d817(puVar3,puVar5);
    puVar5 = (uint *)((ulonglong)uVar8 >> 0x20);
    if (((uint)uVar8 & 0xff) == 2) {
      puVar3 = local_1c;
      do {
        *puVar3 = 0xffffffff;
        puVar3 = puVar3 + 1;
      } while (puVar3 != local_20);
      local_1c[0x14] = 0xffffffff;
      puVar5 = local_20;
      if (local_24 != 4) {
        iVar2 = FUN_00483bd8(local_1c,0);
        puVar5 = extraout_EDX;
        if (iVar2 != -1) {
          uVar4 = extraout_ECX;
          for (uVar7 = 0; puVar5 = (uint *)(uint)uVar7, uVar7 < 800; uVar7 = uVar7 + 1) {
            lVar9 = FUN_00443dad(uVar4,(uint)puVar5);
            uVar4 = extraout_ECX_00;
            if (((char)lVar9 != '\0') &&
               (pUVar6 = tabela_unidades + (int)((ulonglong)lVar9 >> 0x20),
               pUVar6->proprietario_id == local_24)) {
              uVar4 = *local_1c;
              if ((uVar4 & 0x7ffffff) != 0x7fd72b1) {
                *(undefined2 *)&pUVar6->field_0x108 = (&DAT_0051a9f0)[uVar4 * 0x10];
                *(uint *)&pUVar6->field_0x10c = uVar4;
                (&DAT_0051a9f0)[uVar4 * 0x10] = uVar7;
                (&DAT_0051a9f2)[uVar4 * 0x10] = (&DAT_0051a9f2)[uVar4 * 0x10] + 1;
              }
            }
          }
        }
      }
    }
    local_20 = local_20 + 0x18;
    puVar3 = local_1c + 0x18;
    local_24 = local_24 + 1;
    local_1c = puVar3;
  } while ((int)local_24 < 5);
  return (ulonglong)param_2 << 0x20;
}
