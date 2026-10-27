/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00444938, entrada 00444938.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00444938(void)

{
  bool bVar1;
  UnidadeParcial *pUVar2;
  short sVar3;
  uint in_EAX;
  uint uVar4;
  undefined4 uVar5;
  int iVar6;
  uint uVar7;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  uint extraout_ECX_03;
  uint3 uVar8;
  undefined2 extraout_var;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  int extraout_ECX_06;
  undefined4 extraout_ECX_07;
  undefined4 extraout_ECX_08;
  undefined4 extraout_ECX_09;
  uint extraout_EDX;
  undefined4 extraout_EDX_00;
  uint extraout_EDX_01;
  UnidadeParcial *pUVar9;
  undefined8 uVar10;

  sVar3 = (short)in_EAX;
  pUVar9 = tabela_unidades + (in_EAX & 0xffff);
  if ((pUVar9->estado == 0) || (pUVar9->estado == 4)) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  if (bVar1) {
    uVar7 = in_EAX & 0xffff;
    uVar4 = FUN_00467d97(uVar7,2);
    if ((char)uVar4 == '\0') {
      FUN_004829c8(extraout_ECX,0x44);
      thunk_FUN_0048a438(extraout_ECX_00,extraout_EDX);
      pUVar2 = tabela_unidades;
      uVar5 = FUN_004766f0(extraout_ECX_01,(uint)DAT_00508041);
      if ((char)uVar5 != '\0') {
        uVar10 = FUN_00440c5d(extraout_ECX_02,extraout_EDX_00);
        pUVar2[uVar7].field_0xf9 = 0;
        if (*(int *)&pUVar2[uVar7].field_0x104 == -1) {
          FUN_0048aa79(0,(uint)pUVar2[uVar7].tipo_id << 0x10 | 0x500,(uint)uVar10);
        }
      }
      if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
         (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
        bVar1 = false;
      }
      else {
        bVar1 = true;
      }
      if ((bVar1) && (tabela_unidades[in_EAX & 0xffff].estado = 4, sVar3 == DAT_00496304)) {
        DAT_004e0f36 = 0;
        DAT_004e0f3c = 0;
        DAT_004e0f37 = 0;
        DAT_00496304 = -1;
      }
      pUVar2 = tabela_unidades + (in_EAX & 0xffff);
      uVar4 = in_EAX;
      while (pUVar2->campo_0a != 0) {
        FUN_00443dfc(uVar4,0);
        uVar4 = extraout_ECX_03;
      }
      uVar8 = (uint3)(uVar4 >> 8);
      iVar6 = CONCAT31(uVar8,4);
      if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
         (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
        bVar1 = false;
      }
      else {
        bVar1 = true;
      }
      if ((bVar1) && (tabela_unidades[in_EAX & 0xffff].estado = 4, sVar3 == DAT_00496304)) {
        DAT_004e0f36 = (byte)(in_EAX >> 8) ^ (byte)((ushort)DAT_00496304 >> 8);
        iVar6 = (uint)uVar8 << 8;
        DAT_004e0f37 = 0;
        DAT_004e0f3c = 0;
        DAT_00496304 = -1;
      }
      pUVar9->field_0xa4 = 0;
      *(undefined2 *)&pUVar9->field_0xc2 = 0;
      FUN_00472648(iVar6);
      FUN_00442eac();
      uVar5 = CONCAT22(extraout_var,pUVar9->celula_passo);
      if (pUVar9->celula_atual != pUVar9->celula_passo) {
        FUN_00442eac();
        uVar5 = extraout_ECX_04;
      }
      switch(tabela_unidades[in_EAX & 0xffff].tipo_id) {
      case 0xb:
      case 0xc:
      case 0xd:
      case 0xe:
      case 0xf:
      case 0x10:
      case 0x11:
        bVar1 = true;
        break;
      default:
        bVar1 = false;
      }
      if (!bVar1) {
        return;
      }
      if (pUVar9->tipo_id == 0x10) {
        iVar6 = (int)(short)-(ushort)(byte)pUVar9->field_0xab;
        uVar5 = 0;
      }
      else {
        FUN_004704dc(uVar5,(in_EAX & 0xffff) * 0x114);
        iVar6 = -0x20;
        uVar5 = 0xffffffe0;
      }
      goto LAB_00444da3;
    }
  }
  uVar4 = FUN_00467d97((in_EAX & 0xffff) * 0x114,2);
  if ((char)uVar4 == '\0') {
    return;
  }
  thunk_FUN_0048a438(extraout_ECX_05,extraout_EDX_01);
  FUN_00472648(CONCAT31((int3)((uint)extraout_ECX_06 >> 8),
                        (&tabela_unidades->field_0x72)[extraout_ECX_06]));
  FUN_00442eac();
  uVar5 = extraout_ECX_07;
  if (pUVar9->celula_atual != pUVar9->celula_passo) {
    FUN_00442eac();
    uVar5 = extraout_ECX_08;
  }
  if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
     (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  if ((bVar1) && (tabela_unidades[in_EAX & 0xffff].estado = 0, sVar3 == DAT_00496304)) {
    DAT_004e0f36 = 0;
    DAT_004e0f37 = 0;
    DAT_004e0f3c = 0;
    DAT_00496304 = -1;
  }
  if ((byte)uVar5 == 0) {
    return;
  }
  FUN_0046a388(CONCAT22((short)((uint)uVar5 >> 0x10),(ushort)(byte)uVar5),5);
  if ((pUVar9->proprietario_id != 200) && (pUVar9->proprietario_id != 4)) {
    FUN_00476e82(extraout_ECX_09,
                 (uint)(ushort)((ushort)(byte)pUVar9->field_0xf5 + (ushort)pUVar9->raio_visao));
  }
  iVar6 = 0;
  uVar5 = 0;
LAB_00444da3:
  FUN_0046e44c(0,0,uVar5,iVar6,0);
  return;
}
