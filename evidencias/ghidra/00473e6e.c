/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00473e6e, entrada 00473e6e.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00473e6e(undefined4 param_1,undefined4 param_2)

{
  bool bVar1;
  char cVar2;
  uint in_EAX;
  uint uVar3;
  ushort indice_unidade;
  ushort indice_unidade_00;
  int iVar4;
  int extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_EDX;
  uint extraout_EDX_00;
  uint extraout_EDX_01;
  ushort uVar5;
  ulonglong uVar6;

  uVar6 = CONCAT44(param_2,in_EAX);
  bVar1 = false;
  uVar5 = 0;
  while( true ) {
    iVar4 = (in_EAX & 0xff) * 0x200;
    if (*(ushort *)(&DAT_00508728 + iVar4) <= uVar5) break;
    uVar6 = FUN_00443dad((uint)*(ushort *)(&DAT_0050872a + (uint)uVar5 * 2 + iVar4),
                         (uint)(uVar6 >> 0x20));
    if ((char)uVar6 != '\0') {
      uVar6 = uVar6 & 0xffffffff00000000;
      if (tabela_unidades[extraout_ECX].proprietario_id == (byte)in_EAX) {
        FUN_004457d3();
        *(undefined4 *)&tabela_unidades[extraout_ECX].field_0x110 = DAT_00508f7c;
        unidade_obter_tipo(indice_unidade);
        uVar3 = FUN_00442394();
        uVar6 = CONCAT44(extraout_EDX,uVar3);
        if ((char)uVar3 == '\0') {
          unidade_obter_tipo(indice_unidade_00);
          cVar2 = FUN_004422cf();
          uVar6 = (ulonglong)extraout_EDX_00 << 0x20;
          if ((cVar2 == '\0') && (uVar6 = (ulonglong)extraout_EDX_00 << 0x20, !bVar1)) {
            uVar6 = (ulonglong)CONCAT31((int3)(extraout_EDX_00 >> 8),DAT_00508041) << 0x20;
            bVar1 = true;
            if ((byte)in_EAX == DAT_00508041) {
              FUN_00440d5e(extraout_ECX_00,0xb);
              uVar6 = (ulonglong)extraout_EDX_01 << 0x20;
            }
          }
        }
      }
    }
    uVar5 = uVar5 + 1;
  }
  return;
}
