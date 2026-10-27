/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004660bb, entrada 004660bb.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_004660bb(void)

{
  ushort uVar1;
  bool bVar2;
  byte in_AL;
  char cVar3;
  byte bVar4;
  ushort uVar5;
  ushort uVar6;
  uint uVar7;
  uint extraout_ECX;
  uint extraout_ECX_00;
  uint extraout_ECX_01;
  uint extraout_ECX_02;
  uint extraout_ECX_03;
  uint uVar8;
  ushort uVar9;

  uVar7 = 0;
  bVar2 = false;
  uVar1 = 0;
  do {
    if (9 < uVar1) {
      return;
    }
    if (*(short *)(&DAT_004e296c + (uint)uVar1 * 2 + (uint)in_AL * 0x14) != -1) {
      FUN_00418a74(uVar7,(uint)in_AL * 0x14);
      uVar5 = FUN_00447107();
      uVar7 = extraout_ECX;
      for (uVar9 = 0; uVar9 < uVar5; uVar9 = uVar9 + 1) {
        cVar3 = FUN_004472d3(uVar7,0);
        uVar7 = extraout_ECX_00;
        if (cVar3 == '\x01') {
          uVar6 = FUN_004472de(extraout_ECX_00,0);
          bVar4 = unidade_obter_tipo(uVar6);
          if ((bVar4 != 9) || (bVar2)) {
            uVar6 = FUN_004473cf(extraout_ECX_01,1);
            uVar8 = extraout_ECX_02;
            if (*(int *)&tabela_unidades[uVar6].field_0x10c != -1) {
              FUN_004832b1(extraout_ECX_02,uVar6);
              uVar8 = extraout_ECX_03;
            }
            uVar7 = uVar8 + 1;
            *(ushort *)(&DAT_004e2958 + (uVar8 & 0xffff) * 2) = uVar6;
            if (7 < (uVar7 & 0xffff)) {
              return;
            }
          }
          else {
            bVar2 = true;
            uVar7 = extraout_ECX_01;
          }
        }
      }
    }
    uVar1 = uVar1 + 1;
  } while( true );
}
