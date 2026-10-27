/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00473999, entrada 00473999.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

ulonglong __fastcall FUN_00473999(undefined4 param_1,undefined4 param_2)

{
  UnidadeParcial *pUVar1;
  uint in_EAX;
  uint uVar2;
  uint extraout_ECX;
  int iVar3;
  byte *pbVar4;
  ushort uVar5;
  longlong lVar6;

  uVar2 = CONCAT31((int3)((uint)param_1 >> 8),(char)in_EAX);
  uVar5 = 0;
  do {
    pUVar1 = tabela_unidades;
    iVar3 = (uVar2 & 0xff) * 0x200;
    if (*(ushort *)(&DAT_00508728 + iVar3) <= uVar5) {
      return CONCAT44(param_2,in_EAX) & 0xffffffffffffff00;
    }
    lVar6 = FUN_00443dad(uVar2,(uint)*(ushort *)(&DAT_0050872a + (uint)uVar5 * 2 + iVar3) * 0x114);
    in_EAX = (uint)lVar6;
    pbVar4 = &pUVar1->proprietario_id + (int)((ulonglong)lVar6 >> 0x20);
    if ((((char)lVar6 != '\0') && ((byte)extraout_ECX == *pbVar4)) &&
       (in_EAX = (uint)pbVar4[1], in_EAX == 7)) {
      in_EAX = (uint)*(ushort *)(pbVar4 + 0xd8);
      if (in_EAX == 10) {
        return CONCAT44(param_2,CONCAT31((uint3)(byte)(*(ushort *)(pbVar4 + 0xd8) >> 8),1));
      }
    }
    uVar5 = uVar5 + 1;
    uVar2 = extraout_ECX;
  } while( true );
}
