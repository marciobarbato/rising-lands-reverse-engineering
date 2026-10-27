/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00441baa, entrada 00441baa.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00441baa(undefined4 param_1,undefined4 param_2)

{
  byte in_AL;
  ushort uVar1;
  uint uVar2;
  int iVar3;
  int extraout_ECX;
  undefined4 extraout_ECX_00;
  int extraout_ECX_01;
  int extraout_ECX_02;
  UnidadeParcial *extraout_ECX_03;
  UnidadeParcial *pUVar4;
  int extraout_ECX_04;
  undefined4 extraout_ECX_05;
  ulonglong uVar5;

  iVar3 = (uint)in_AL * 8;
  if (*(short *)(&DAT_004e1a14 + iVar3) == 0) {
    uVar1 = *(ushort *)(&DAT_004e1a18 + iVar3);
    if (uVar1 == 0xffff) {
      uVar5 = FUN_004704dc(iVar3,param_2);
      *(short *)(&DAT_004e1a1a + extraout_ECX) =
           (short)((uVar5 & 0xffffffff) % (ulonglong)DAT_00497168);
      uVar1 = FUN_00457e6c(in_AL);
      FUN_004829c8(extraout_ECX_00,0x45);
      FUN_00442cb4(tabela_unidades);
      *(undefined1 *)(extraout_ECX_01 + 0x72 + (uint)uVar1 * 0x114) = 1;
      pUVar4 = tabela_unidades + uVar1;
      if ((pUVar4->proprietario_id != 200) && (pUVar4->proprietario_id != 4)) {
        FUN_00476851(pUVar4,(uint)(ushort)((ushort)(byte)pUVar4->field_0xf5 + pUVar4->raio_visao + 2
                                          ));
        FUN_00476cb3(extraout_ECX_02,
                     (uint)(ushort)((ushort)*(byte *)(extraout_ECX_02 + 0xf5) +
                                   (ushort)*(byte *)(extraout_ECX_02 + 0xbb)));
        pUVar4 = extraout_ECX_03;
      }
      FUN_0046a388(pUVar4,4);
      iVar3 = extraout_ECX_04;
    }
    uVar2 = FUN_0045d864(iVar3,in_AL);
    if ((uVar2 & 0xffff) == 0xffff) {
      FUN_0045d864(extraout_ECX_05,in_AL);
      FUN_0041aee2();
    }
    else {
      FUN_0041aee2();
    }
    FUN_004457d3();
    *(ushort *)(&DAT_004e1a18 + (uint)in_AL * 8) = uVar1;
  }
  *(short *)(&DAT_004e1a14 + (uint)in_AL * 8) = *(short *)(&DAT_004e1a14 + (uint)in_AL * 8) + 1;
  return;
}
