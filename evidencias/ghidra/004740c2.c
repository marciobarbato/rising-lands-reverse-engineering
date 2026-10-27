/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004740c2, entrada 004740c2.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_004740c2(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  uint in_EAX;
  ushort indice_unidade;
  int iVar2;
  int extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_EDX;
  uint extraout_EDX_00;
  ushort uVar3;
  ushort uVar4;
  longlong lVar5;
  ushort local_18;

  lVar5 = CONCAT44(param_2,in_EAX);
  uVar4 = 0;
  uVar3 = 0;
  while( true ) {
    iVar2 = (in_EAX & 0xff) * 0x200;
    if (*(ushort *)(&DAT_00508728 + iVar2) <= uVar3) break;
    lVar5 = FUN_00443dad((uint)*(ushort *)(&DAT_0050872a + (uint)uVar3 * 2 + iVar2),
                         (uint)((ulonglong)lVar5 >> 0x20));
    if (((char)lVar5 != '\0') &&
       (lVar5 = ZEXT48(tabela_unidades) << 0x20,
       tabela_unidades[extraout_ECX].proprietario_id == (byte)in_EAX)) {
      local_18 = (ushort)param_2;
      FUN_00445f2d(extraout_ECX,local_18);
      bVar1 = unidade_obter_tipo(indice_unidade);
      lVar5 = CONCAT44(extraout_EDX,(uint)bVar1);
      if ((bVar1 != 9) && (lVar5 = CONCAT44(extraout_EDX,(uint)uVar4), uVar4 == 0)) {
        lVar5 = (ulonglong)CONCAT31((int3)((uint)extraout_EDX >> 8),DAT_00508041) << 0x20;
        uVar4 = uVar4 + 1;
        if ((byte)in_EAX == DAT_00508041) {
          FUN_00440d5e(extraout_ECX_00,0xe);
          lVar5 = (ulonglong)extraout_EDX_00 << 0x20;
        }
      }
    }
    uVar3 = uVar3 + 1;
  }
  return;
}
