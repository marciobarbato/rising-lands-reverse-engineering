/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined8 __fastcall OriginaisSBL::EnginDebloqueNextCase(undefined4 param_1,undefined4 param_2)

{
  ulonglong uVar1;
  UnidadeParcial *pUVar2;
  byte bVar3;
  uint in_EAX;
  uint uVar4;
  uint uVar5;
  UnidadeParcial *pUVar6;
  int extraout_ECX;
  int extraout_ECX_00;
  int extraout_ECX_01;
  int iVar7;
  int extraout_ECX_02;
  undefined2 extraout_var;
  char cVar8;
  uint uVar9;
  undefined4 extraout_EDX;
  undefined2 uVar10;
  byte bVar11;
  undefined8 uVar12;
  byte local_20;

  pUVar2 = tabela_unidades;
  uVar9 = in_EAX & 0xffff;
  local_20 = 0;
  uVar4 = CalculDirection(param_1,tabela_unidades[uVar9].celula_destino);
  uVar4 = uVar4 & 0xff;
  iVar7 = extraout_ECX;
  do {
    uVar10 = (undefined2)uVar4;
    bVar11 = (byte)(uVar4 >> 8);
    if (2 < bVar11) {
      pUVar2[uVar9].field_0x8b = 0;
      pUVar2[uVar9].estado_caminho = 1;
      return CONCAT44(param_2,(uint)local_20);
    }
    uVar5 = CalculDirCase(iVar7,(byte)uVar4);
    iVar7 = extraout_ECX_02;
    if ((uVar5 & 0xffff) != 0xffff) {
      uVar12 = ChercheIndiceEngin(0,extraout_EDX);
      _DAT_004e1a34 = (undefined2)uVar12;
      iVar7 = CONCAT22(extraout_var,_DAT_004e1a34);
      if (((iVar7 == 0xffff) ||
          (pUVar6 = tabela_unidades + iVar7,
          tabela_unidades[in_EAX & 0xffff].proprietario_id != pUVar6->proprietario_id)) ||
         (pUVar6->celula_atual != pUVar6->celula_destino)) {
        bVar3 = 0;
      }
      else {
        uVar5 = EnginChercheCaseLibre(iVar7,iVar7);
        _DAT_004e1a36 = (undefined2)uVar5;
        iVar7 = extraout_ECX_00;
        if ((uVar5 & 0xffff) != 0xffff) {
          SetDeplaceEngin();
          iVar7 = extraout_ECX_01;
        }
        bVar3 = 1;
      }
      local_20 = local_20 | bVar3;
    }
    if (bVar11 == 0) {
      if ((uVar4 & 0xff) == 1) {
        uVar5 = 0x10;
      }
      else {
        uVar5 = (uVar4 & 0xff) - 1;
      }
      if ((uVar5 & 0xff) == 1) {
        cVar8 = '\x10';
      }
      else {
        cVar8 = (char)uVar5 + -1;
      }
LAB_00449214:
      uVar10 = (undefined2)CONCAT31((int3)(uVar4 >> 8),cVar8);
    }
    else if (bVar11 == 1) {
      iVar7 = 0x10;
      uVar1 = (ulonglong)uVar4;
      uVar4 = uVar4 & 0xffffff00;
      cVar8 = (char)((ulonglong)((int)((uVar1 & 0xffffffff000000ff) % 0x10) + 1) % 0x10) + '\x01';
      goto LAB_00449214;
    }
    uVar4 = (uint)CONCAT11((char)((ushort)uVar10 >> 8) + '\x01',(char)uVar10);
  } while( true );
}
