/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00446cb5, entrada 00446cb5.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00446cb5(undefined4 param_1,char param_2)

{
  byte bVar1;
  ushort uVar2;
  char cVar3;
  uint in_EAX;
  undefined4 uVar4;
  int iVar5;
  uint uVar6;
  UnidadeParcial *pUVar7;
  int extraout_ECX;
  int extraout_ECX_00;
  uint extraout_ECX_01;
  ushort unaff_BX;
  bool bVar8;
  undefined8 uVar9;
  uint local_1c;
  uint local_18;

  pUVar7 = tabela_unidades + (in_EAX & 0xffff);
  bVar1 = pUVar7->alcance_quadrado_u8;
  uVar2 = pUVar7->celula_atual;
  local_18 = FUN_00428cc0((uint)pUVar7,4);
  local_18 = bVar1 + local_18;
  iVar5 = extraout_ECX;
  if (param_2 == '\x01') {
    local_1c = (uint)tabela_unidades[unaff_BX].celula_passo;
    if (*(char *)(extraout_ECX + 2) == '\x18') {
LAB_00446e4a:
      uVar9 = FUN_004746c9(iVar5,4);
      local_18 = FUN_00428cc0(extraout_ECX_01,(char)((ulonglong)uVar9 >> 0x20));
      local_18 = (int)uVar9 + local_18;
    }
    else {
      cVar3 = *(char *)(extraout_ECX + 1);
      if (cVar3 == '\x10') {
        bVar8 = uVar2 == tabela_unidades[unaff_BX].celula_passo;
LAB_00446dc0:
        if (bVar8) goto LAB_00446d89;
        goto LAB_00446ee6;
      }
      if (((*(char *)(extraout_ECX + 0x78) == '\0') || (cVar3 == '\x15')) ||
         ((cVar3 == '\x01' || (cVar3 == '\x04')))) {
        uVar4 = FUN_004468e4(extraout_ECX);
        cVar3 = (char)uVar4;
LAB_00446d81:
        if (cVar3 != '\0') goto LAB_00446d89;
      }
    }
  }
  else if (param_2 == '\x03') {
    local_1c = FUN_0041aee2();
    iVar5 = extraout_ECX_00;
    if (*(char *)(extraout_ECX_00 + 2) == '\x18') goto LAB_00446e4a;
    cVar3 = *(char *)(extraout_ECX_00 + 1);
    if (cVar3 == '\x10') {
      bVar8 = uVar2 == (ushort)local_1c;
      goto LAB_00446dc0;
    }
    if (((*(char *)(extraout_ECX_00 + 0x78) == '\0') || (cVar3 == '\x15')) ||
       ((cVar3 == '\x01' || (cVar3 == '\x04')))) {
      iVar5 = FUN_0042381f(extraout_ECX_00,(uint)uVar2);
      cVar3 = (char)iVar5;
      goto LAB_00446d81;
    }
  }
  else if (param_2 == '\x05') {
    local_1c = (uint)*(ushort *)(extraout_ECX + 0xb8);
    if (*(char *)(extraout_ECX + 2) == '\x18') goto LAB_00446e4a;
    cVar3 = *(char *)(extraout_ECX + 1);
    if (cVar3 == '\x10') {
      bVar8 = uVar2 == *(ushort *)(extraout_ECX + 0xb8);
      goto LAB_00446dc0;
    }
    if ((((*(char *)(extraout_ECX + 0x78) == '\0') || (cVar3 == '\x15')) || (cVar3 == '\x01')) ||
       (cVar3 == '\x04')) {
      uVar6 = FUN_00446b0c(extraout_ECX,unaff_BX);
      cVar3 = (char)uVar6;
      goto LAB_00446d81;
    }
  }
  uVar6 = FUN_00479555((ushort)(local_1c >> 8) & 0xff,uVar2 >> 8);
  if (uVar6 <= (local_18 & 0xffff)) {
LAB_00446d89:
    FUN_00440f94();
    return;
  }
LAB_00446ee6:
  FUN_00440f94();
  return;
}
