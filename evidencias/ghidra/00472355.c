/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00472355, entrada 00472355.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined1 __fastcall FUN_00472355(undefined4 param_1,uint param_2)

{
  ushort indice_unidade;
  byte in_AL;
  char cVar1;
  uint uVar2;
  int iVar3;
  int extraout_ECX;
  undefined4 extraout_ECX_00;
  int extraout_ECX_01;
  int extraout_ECX_02;
  byte bVar4;
  uint extraout_EDX;
  uint extraout_EDX_00;
  ushort unaff_BX;
  ulonglong uVar5;
  ulonglong uVar6;
  byte local_18;

  bVar4 = (byte)param_2;
  if (bVar4 != 0) {
    if (bVar4 < 2) {
      local_18 = unidade_obter_tipo(unaff_BX);
      param_2 = extraout_EDX;
      if (local_18 == 0x11) {
        return 0;
      }
    }
    else if (bVar4 == 5) {
      return 1;
    }
  }
  uVar5 = (ulonglong)param_2 << 0x20;
  uVar2 = 0;
  do {
    if (*(ushort *)(&DAT_00508728 + (uint)in_AL * 0x200) <= (ushort)uVar2) {
      return 1;
    }
    indice_unidade = *(ushort *)(&DAT_0050872a + (uVar2 & 0xffff) * 2 + (uint)in_AL * 0x200);
    uVar5 = FUN_00443dad(uVar2,(uint)(uVar5 >> 0x20));
    iVar3 = extraout_ECX;
    if ((char)uVar5 != '\0') {
      unidade_obter_tipo(indice_unidade);
      cVar1 = FUN_0044230c();
      if (cVar1 == '\0') {
        return 0;
      }
      if ((bVar4 == 1) && (cVar1 = FUN_00453d7d(extraout_ECX_00,local_18), cVar1 == '\0')) {
        return 0;
      }
      cVar1 = FUN_004422eb();
      uVar5 = (ulonglong)extraout_EDX_00 << 0x20;
      iVar3 = extraout_ECX_01;
      if (cVar1 != '\0') {
        uVar6 = FUN_0044828b(extraout_ECX_01,extraout_EDX_00);
        uVar5 = uVar6 & 0xffffffff000000ff;
        iVar3 = extraout_ECX_02;
        if ((uVar6 & 0xff) == 0) {
          return 0;
        }
      }
    }
    uVar2 = iVar3 + 1;
  } while( true );
}
