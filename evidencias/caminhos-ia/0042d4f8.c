/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_0042d4f8(undefined4 param_1,uint param_2)

{
  UnidadeParcial *in_EAX;
  int iVar1;
  uint uVar2;
  ushort uVar3;
  ushort uVar4;

  if ((((uint)in_EAX & 0xff) < (uint)DAT_00497168) && ((param_2 & 0xff) < (uint)DAT_00497168)) {
    uVar2 = (uint)in_EAX & 0xffff;
    in_EAX = (UnidadeParcial *)((int)uVar2 >> 8);
    if ((in_EAX < (UnidadeParcial *)(uint)DAT_0049716a) &&
       (in_EAX = (UnidadeParcial *)(param_2 & 0xffff),
       (UnidadeParcial *)((int)in_EAX >> 8) < (UnidadeParcial *)(uint)DAT_0049716a)) {
      uVar4 = *(ushort *)(DAT_004e0f38 + uVar2 * 2);
      uVar3 = *(ushort *)(DAT_004e0f38 + (int)in_EAX * 2);
      if ((uVar4 & 0x8000) == 0) {
        if ((uVar4 & 0x4000) != 0) {
          in_EAX = tabela_unidades + ((int)(uVar4 & 0x3ff8) >> 3);
          uVar4 = *(ushort *)(&in_EAX->field_0xfa + ((byte)uVar4 & 0xffffff03) * 2);
        }
      }
      else {
        iVar1 = (int)(uVar4 & 0x7fe0) >> 5;
        in_EAX = (UnidadeParcial *)(iVar1 * 0x45);
        uVar4 = *(ushort *)(&DAT_0049a194 + iVar1 * 0x114 + ((byte)uVar4 & 0xffffff1f) * 2);
      }
      if ((uVar3 & 0x8000) == 0) {
        if ((uVar3 & 0x4000) != 0) {
          in_EAX = tabela_unidades + ((int)(uVar3 & 0x3ff8) >> 3);
          uVar3 = *(ushort *)(&in_EAX->field_0xfa + ((byte)uVar3 & 0xffffff03) * 2);
        }
      }
      else {
        iVar1 = (int)(uVar3 & 0x7fe0) >> 5;
        in_EAX = (UnidadeParcial *)(iVar1 * 0x45);
        uVar3 = *(ushort *)(&DAT_0049a194 + iVar1 * 0x114 + ((byte)uVar3 & 0xffffff1f) * 2);
      }
      return CONCAT31((int3)((uint)in_EAX >> 8),uVar4 == uVar3);
    }
  }
  return (uint)in_EAX & 0xffffff00;
}
