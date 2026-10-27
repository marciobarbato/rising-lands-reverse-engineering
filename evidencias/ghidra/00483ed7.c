/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00483ed7, entrada 00483ed7.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00483ed7(undefined4 param_1)

{
  byte bVar1;
  uint uVar2;
  uint uVar3;
  uint in_EAX;
  char *pcVar4;
  uint extraout_ECX;
  uint extraout_ECX_00;
  UnidadeParcial *pUVar5;
  int iVar6;
  uint *puVar7;
  uint uVar8;
  uint uVar9;
  undefined8 uVar10;
  uint local_28;
  char local_20;
  byte local_1c;

  pUVar5 = tabela_unidades + (in_EAX & 0xffff);
  if ((pUVar5->estado != pUVar5->field_0x10a) || (pUVar5->field_0x89 != pUVar5->field_0x10b)) {
    pUVar5->field_0x10a = pUVar5->estado;
    pUVar5->field_0x10b = pUVar5->field_0x89;
    if (pUVar5->proprietario_id < 4) {
      uVar10 = FUN_0046d817(param_1,pUVar5);
      iVar6 = (int)((ulonglong)uVar10 >> 0x20);
      if (((((((uint)uVar10 & 0xff) == 2) && (uVar9 = *(uint *)(iVar6 + 0x10c), uVar9 != 0xffffffff)
            ) && ((uVar9 & 0x7ffffff) != 0x7fd72b1)) &&
          ((uVar2 = (&DAT_0051a9fc)[uVar9 * 8], uVar2 != 0 &&
           ((ushort)(&DAT_0051a9f6)[uVar9 * 0x10] != 0xffff)))) &&
         (pcVar4 = *(char **)(&DAT_00498b38 + (uint)(ushort)(&DAT_0051a9f6)[uVar9 * 0x10] * 4),
         pcVar4 != (char *)0x0)) {
        uVar9 = 1;
        uVar8 = 0;
        for (; *pcVar4 != -1; pcVar4 = pcVar4 + 0xc) {
          if (((*pcVar4 == *(char *)(iVar6 + 1)) && (pcVar4[1] == *(char *)(iVar6 + 2))) &&
             ((pcVar4[2] == -1 || (pcVar4[2] == *(char *)(iVar6 + 0x89))))) {
            uVar8 = uVar8 | 1 << (pcVar4[4] & 0x1fU);
            if ((*(ushort *)(pcVar4 + 6) != 0) && (bVar1 = pcVar4[5], bVar1 != 0)) {
              puVar7 = (uint *)((uint)*(ushort *)(pcVar4 + 6) + iVar6);
              if (bVar1 < 2) {
                if (bVar1 == 1) {
                  uVar9 = (uint)(byte)*puVar7;
                }
                else {
LAB_0048402b:
                  uVar9 = 0;
                }
              }
              else if (bVar1 < 3) {
                uVar9 = (uint)(ushort)*puVar7;
              }
              else {
                if (bVar1 != 4) goto LAB_0048402b;
                uVar9 = *puVar7;
              }
            }
            local_20 = pcVar4[3];
            local_1c = pcVar4[8];
            if ((*(ushort *)(pcVar4 + 10) != 0) && (bVar1 = pcVar4[9], bVar1 != 0)) {
              puVar7 = (uint *)((uint)*(ushort *)(pcVar4 + 10) + iVar6);
              if (bVar1 < 2) {
                if (bVar1 == 1) {
                  local_28 = (uint)(byte)*puVar7;
                }
                else {
LAB_00484078:
                  local_28 = 0;
                }
              }
              else if (bVar1 < 3) {
                local_28 = (uint)(ushort)*puVar7;
              }
              else {
                if (bVar1 != 4) goto LAB_00484078;
                local_28 = *puVar7;
              }
            }
          }
        }
        if ((uVar8 != 0) &&
           (uVar3 = *(uint *)&tabela_unidades[in_EAX & 0xffff].field_0x10c,
           (uVar3 & 0x7ffffff) != 0x7fd72b1)) {
          (&DAT_0051a9fc)[uVar3 * 8] = 0;
          if ((&DAT_0051a9e8)[uVar3 * 8] != -1) {
            if ((uVar2 & uVar8) == 0) {
              uVar9 = 0xffffffff;
            }
            FUN_0047da54(local_28,uVar9);
            local_28 = extraout_ECX;
          }
          if ((local_20 != '\0') && (local_20 != -1)) {
            FUN_004829c8(local_28,local_20);
            local_28 = extraout_ECX_00;
          }
          if ((local_1c != 0) && (local_1c != 0xff)) {
            FUN_00484808(local_28,local_1c);
          }
        }
      }
    }
  }
  return;
}
