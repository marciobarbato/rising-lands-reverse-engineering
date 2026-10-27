/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00453b84, entrada 00453b84.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00453b84(void)

{
  UnidadeParcial *pUVar1;
  ushort in_AX;
  ushort uVar2;
  int iVar3;
  uint uVar4;
  undefined4 uVar5;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined2 extraout_DX;
  undefined4 extraout_EDX;
  UnidadeParcial *pUVar6;

  pUVar6 = tabela_unidades + in_AX;
  if (*(short *)&pUVar6->field_0x4 == 4) {
    return;
  }
  if (pUVar6->estado == 0x13) {
    return;
  }
  *(ushort *)&pUVar6->field_0xa0 = (ushort)pUVar6->estado;
  *(ushort *)&pUVar6->field_0xa2 = pUVar6->celula_destino;
  uVar2 = FUN_00477b74(0x43,0x14);
  if (uVar2 == 0xffff) {
    iVar3 = FUN_004676e5(0,0,pUVar6->proprietario_id);
    if ((char)iVar3 == '\0') {
      return;
    }
    uVar4 = FUN_004538fa((uint)pUVar6->proprietario_id,0x28);
    pUVar1 = tabela_unidades;
    if ((uVar4 & 0xffff) == 0xffff) {
      if (pUVar6->proprietario_id != DAT_00508041) {
        return;
      }
      if (*(short *)&pUVar6->field_0x74 != 1) {
        return;
      }
      uVar5 = FUN_004766f0(extraout_ECX,(uint)DAT_00508041);
      if ((char)uVar5 == '\0') {
        return;
      }
      FUN_00440c5d(extraout_ECX_00,extraout_EDX);
      iVar3 = *(int *)&pUVar1[in_AX].field_0x104;
      pUVar1[in_AX].field_0xf9 = 0;
      if (iVar3 == -1) {
        FUN_0044b334();
        return;
      }
      return;
    }
    uVar2 = FUN_0041aee2();
    pUVar6->estado = 0x13;
    *(undefined2 *)&pUVar6->field_0xc2 = extraout_DX;
    pUVar6 = tabela_unidades + in_AX;
    pUVar6->celula_destino = uVar2;
    if (in_AX == DAT_00496304) {
      DAT_004e0f36 = 0;
      DAT_004e0f3c = 0;
      DAT_004e0f37 = 0;
      DAT_00496304 = 0xffff;
    }
  }
  else {
    *(undefined2 *)&pUVar6->field_0xc2 = 0xffff;
    pUVar6->estado = 0x13;
    pUVar6 = tabela_unidades + in_AX;
    pUVar6->celula_destino = uVar2;
    if (in_AX == DAT_00496304) {
      DAT_004e0f36 = 0;
      DAT_004e0f37 = 0;
      DAT_004e0f3c = 0;
      DAT_00496304 = 0xffff;
    }
  }
  pUVar6->estado_caminho = 0;
  return;
}
