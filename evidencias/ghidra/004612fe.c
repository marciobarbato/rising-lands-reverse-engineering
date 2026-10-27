/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004612fe, entrada 004612fe.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined4 __fastcall FUN_004612fe(undefined4 param_1,char param_2)

{
  byte in_AL;
  byte bVar1;
  ushort uVar2;
  ushort indice_unidade;
  undefined4 extraout_ECX;
  undefined4 uVar3;
  undefined4 extraout_ECX_00;
  int iVar4;
  undefined4 extraout_EDX;
  ushort uVar5;
  undefined2 *unaff_EBX;
  byte local_18;

  local_18 = 0;
  do {
    if (9 < local_18) {
      return 0xffff;
    }
    if (*(ushort *)(&DAT_004e296c + (uint)local_18 * 2 + (uint)in_AL * 0x14) != 0xffff) {
      iVar4 = (uint)*(ushort *)(&DAT_004e296c + (uint)local_18 * 2 + (uint)in_AL * 0x14) * 0x114;
      FUN_00418a74(iVar4 + 0x49a0d4,&DAT_0049a0c8 + iVar4);
      uVar2 = FUN_00447107();
      uVar3 = extraout_ECX;
      for (uVar5 = 0; uVar5 < uVar2; uVar5 = uVar5 + 1) {
        indice_unidade = FUN_004472de(uVar3,(uint)uVar5);
        bVar1 = unidade_obter_tipo(indice_unidade);
        if (bVar1 == param_2) {
          *unaff_EBX = *(undefined2 *)(&DAT_004e296c + (uint)local_18 * 2 + (uint)in_AL * 0x14);
          return extraout_EDX;
        }
        uVar3 = extraout_ECX_00;
      }
    }
    local_18 = local_18 + 1;
  } while( true );
}
