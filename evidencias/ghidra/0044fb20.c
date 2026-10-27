/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044fb20, entrada 0044fb20.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0044fb20(undefined4 param_1,byte param_2)

{
  byte bVar1;
  bool bVar2;
  UnidadeParcial *pUVar3;
  ushort uVar4;
  uint in_EAX;
  undefined4 extraout_ECX;
  int extraout_ECX_00;
  int extraout_ECX_01;
  byte *extraout_ECX_02;
  byte *pbVar5;
  uint uVar6;
  uint uVar7;

  pUVar3 = tabela_unidades;
  uVar7 = in_EAX & 0xffff;
  if (4 < param_2) {
    return;
  }
  uVar4 = CONCAT11(param_2,tabela_unidades[uVar7].field_0xaf) & 0xff1f;
  tabela_unidades[uVar7].field_0xaf = (byte)uVar4 | (char)(uVar4 >> 8) << 5;
  switch(param_2) {
  case 1:
    bVar1 = tabela_unidades[uVar7].tipo_id;
    if (bVar1 < 0xf) {
      if (((2 < bVar1) && (3 < bVar1)) &&
         ((bVar1 < 8 || ((8 < bVar1 && ((bVar1 < 0xb || (0xc < bVar1)))))))) goto LAB_0044fb99;
LAB_0044fb81:
      bVar2 = true;
    }
    else {
      if (bVar1 < 0x10) goto LAB_0044fb81;
      if (bVar1 < 0x14) {
        if ((bVar1 < 0x11) || (0x11 < bVar1)) goto LAB_0044fb81;
      }
      else if ((bVar1 < 0x17) || ((bVar1 < 0x19 || (bVar1 == 0x19)))) goto LAB_0044fb81;
LAB_0044fb99:
      bVar2 = false;
    }
    if (bVar2) {
      pUVar3[uVar7].field_0xf7 = 1;
      return;
    }
LAB_0044fbab:
    uVar6 = (uint)*(ushort *)(&DAT_004965dc + (uint)pUVar3[uVar7].tipo_id * 0x32);
    goto LAB_0044fbc6;
  case 2:
    pUVar3[uVar7].field_0xf6 = 1;
    break;
  case 3:
    if (pUVar3[uVar7].field_0x72 == '\0') {
      pUVar3[uVar7].field_0xf5 = 1;
    }
    else {
      FUN_00457058();
      pUVar3[uVar7].field_0xf5 = 1;
      pUVar3 = tabela_unidades;
      FUN_00442cb4(extraout_ECX);
      (&pUVar3->field_0x72)[extraout_ECX_00] = 1;
      pbVar5 = &tabela_unidades->proprietario_id + extraout_ECX_00;
      if ((*pbVar5 != 200) && (*pbVar5 != 4)) {
        FUN_00476851(pbVar5,(uint)(ushort)((ushort)pbVar5[0xf5] + pbVar5[0xbb] + 2));
        FUN_00476cb3(extraout_ECX_01,
                     (uint)(ushort)((ushort)*(byte *)(extraout_ECX_01 + 0xf5) +
                                   (ushort)*(byte *)(extraout_ECX_01 + 0xbb)));
        pbVar5 = extraout_ECX_02;
      }
      FUN_0046a388(pbVar5,4);
    }
    break;
  case 4:
    bVar1 = tabela_unidades[uVar7].tipo_id;
    if (bVar1 < 0xf) {
      if (((2 < bVar1) && (3 < bVar1)) &&
         ((bVar1 < 8 || ((8 < bVar1 && ((bVar1 < 0xb || (0xc < bVar1)))))))) goto LAB_0044fcf5;
LAB_0044fcd9:
      bVar2 = true;
    }
    else {
      if (bVar1 < 0x10) goto LAB_0044fcd9;
      if (bVar1 < 0x14) {
        if ((bVar1 < 0x11) || (0x11 < bVar1)) goto LAB_0044fcd9;
      }
      else if ((bVar1 < 0x17) || ((bVar1 < 0x19 || (bVar1 == 0x19)))) goto LAB_0044fcd9;
LAB_0044fcf5:
      bVar2 = false;
    }
    if (bVar2) goto LAB_0044fbab;
    uVar6 = (uint)*(ushort *)(&DAT_004965dc + (uint)pUVar3[uVar7].tipo_id * 0x32) * 2;
LAB_0044fbc6:
    pUVar3[uVar7].field_0xf8 = (char)(uVar6 / 100);
  }
  return;
}
