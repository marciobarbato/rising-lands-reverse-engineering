/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004649a7, entrada 004649a7.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall FUN_004649a7(uint param_1,uint param_2)

{
  char cVar1;
  byte bVar2;
  ushort uVar3;
  ushort indice_unidade;
  uint in_EAX;
  uint extraout_ECX;
  int iVar4;
  int extraout_ECX_00;
  int extraout_ECX_01;
  uint extraout_EDX;
  uint uVar5;
  uint extraout_EDX_00;
  uint extraout_EDX_01;
  undefined4 unaff_EBX;
  short sVar6;
  uint local_14;

  sVar6 = 0;
  local_14 = 0;
  uVar5 = param_2;
  do {
    if (9 < (ushort)local_14) {
      return (local_14 >> 8 & 0xff) << 8;
    }
    if (*(short *)(&DAT_004e296c + (local_14 & 0xffff) * 2 + (in_EAX & 0xffff) * 0x14) != -1) {
      FUN_00418a74(param_1,uVar5);
      uVar3 = FUN_00447107();
      param_1 = extraout_ECX;
      uVar5 = extraout_EDX;
      while ((ushort)param_1 < uVar3) {
        cVar1 = FUN_004472d3(param_1,param_1 & 0xffff);
        iVar4 = extraout_ECX_00;
        uVar5 = extraout_EDX_00;
        if (cVar1 == '\x01') {
          indice_unidade = FUN_004472de(extraout_ECX_00,param_1 & 0xffff);
          bVar2 = unidade_obter_tipo(indice_unidade);
          iVar4 = extraout_ECX_01;
          uVar5 = extraout_EDX_01;
          if (((param_2 & 0xffff) == (uint)bVar2) && (sVar6 = sVar6 + 1, sVar6 == (short)unaff_EBX))
          {
            return CONCAT31((int3)((uint)unaff_EBX >> 8),1);
          }
        }
        param_1 = iVar4 + 1;
      }
    }
    local_14 = local_14 + 1;
  } while( true );
}
