/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0042ece0, entrada 0042ece0.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_0042ece0(undefined4 param_1,int param_2)

{
  byte bVar1;
  bool bVar2;
  char cVar3;
  char cVar4;
  char cVar5;
  int in_EAX;
  int iVar6;
  undefined4 uVar7;
  ushort extraout_var;
  ushort extraout_var_00;
  ushort uVar9;
  uint3 uVar8;
  undefined2 extraout_var_01;
  undefined2 extraout_var_02;
  undefined2 uVar11;
  uint uVar10;
  UnidadeParcial *pUVar12;
  bool bVar13;
  bool bVar14;

  pUVar12 = tabela_unidades + in_EAX;
  iVar6 = (int)((uint)pUVar12->direcao_desejada - param_2) / 2;
  if (iVar6 < -4) {
    iVar6 = iVar6 + 8;
  }
  if (4 < iVar6) {
    iVar6 = iVar6 + -8;
  }
  if ((iVar6 < -1) || (1 < iVar6)) {
    cVar4 = '\0';
  }
  else {
    cVar4 = '\x01';
  }
  uVar7 = FUN_0046d838(tabela_unidades + DAT_00496304,pUVar12->proprietario_id);
  cVar5 = FUN_00442409();
  uVar11 = extraout_var_01;
  uVar9 = extraout_var;
  if ((cVar5 == '\0') ||
     (cVar5 = FUN_004423d5(), uVar11 = extraout_var_02, uVar9 = extraout_var_00, cVar5 == '\0')) {
    bVar2 = false;
  }
  else {
    bVar2 = true;
  }
  uVar10 = CONCAT22(uVar11,pUVar12->celula_atual);
  bVar1 = pUVar12->tipo_id;
  iVar6 = CONCAT31(CONCAT21(uVar9,pUVar12->celula_destino != pUVar12->celula_atual),bVar1);
  if (bVar1 < 6) {
    bVar13 = bVar1 == 0;
    bVar14 = bVar1 == 1;
LAB_0042eddd:
    if ((bVar13 || bVar14) && (uVar10 = (uint)pUVar12->estado, uVar10 == 1)) {
      bVar1 = pUVar12->field_0x8a;
LAB_0042edbe:
      uVar10 = (uint)bVar1;
      if (uVar10 == 1) {
        iVar6 = (uint)uVar9 << 0x10;
      }
    }
  }
  else if (bVar1 < 8) {
    uVar10 = (uint)pUVar12->estado;
    if (uVar10 == 0xf) {
      bVar1 = pUVar12->field_0x89;
      goto LAB_0042edbe;
    }
  }
  else if (0x13 < bVar1) {
    bVar13 = bVar1 < 0x15;
    bVar14 = bVar1 == 0x15;
    goto LAB_0042eddd;
  }
  uVar8 = (uint3)((uint)iVar6 >> 8);
  cVar5 = (char)((uint)iVar6 >> 8);
  if ((char)uVar7 == '\0') {
    if (bVar2) goto LAB_0042edf4;
    cVar3 = cVar4;
    if (cVar5 != '\0') goto joined_r0x0042ee02;
  }
  else {
    cVar3 = DAT_004e1771;
    if (cVar5 != '\0') {
      cVar3 = cVar4;
    }
joined_r0x0042ee02:
    if (cVar3 != '\0') {
LAB_0042edf4:
      iVar6 = CONCAT31(uVar8,1);
      goto LAB_0042ecd8;
    }
  }
  iVar6 = (uint)uVar8 << 8;
LAB_0042ecd8:
  return CONCAT44(uVar10,iVar6);
}
