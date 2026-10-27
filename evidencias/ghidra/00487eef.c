/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00487eef, entrada 00487eef.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00487eef(undefined4 param_1,int param_2)

{
  ushort uVar1;
  ushort uVar2;
  uint uVar3;
  UnidadeParcial *pUVar4;
  char cVar5;
  uint *in_EAX;
  uint uVar6;
  uint uVar7;
  uint extraout_ECX;
  undefined4 extraout_ECX_00;
  byte bVar8;
  uint uVar9;
  uint uVar10;
  int local_20;

  uVar3 = *in_EAX;
  if ((((uVar3 & 0x7ffffff) != 0x7fd72b1) && ((&DAT_0051a9f2)[uVar3 * 0x10] != 0)) &&
     ((&DAT_0051a9f0)[uVar3 * 0x10] != -1)) {
    uVar10 = (uint)*(ushort *)((int)in_EAX + param_2 * 8 + 0x12);
    uVar1 = (ushort)in_EAX[param_2 * 2 + 4];
    if ((uVar1 & 0x8000) == 0) {
      uVar9 = (uint)tabela_unidades[uVar1].vida;
    }
    else {
      uVar9 = (uint)*(ushort *)(&DAT_0049a0d2 + (uint)(uVar1 & 0x7fff) * 0x114) -
              (uint)(ushort)(&DAT_0049a0ce)[(uint)(uVar1 & 0x7fff) * 0x8a];
    }
    local_20 = 1;
    while ((-1 < local_20 && ((int)uVar10 < (int)uVar9))) {
      uVar2 = (&DAT_0051a9f0)[uVar3 * 0x10];
      while ((pUVar4 = tabela_unidades, uVar7 = (uint)uVar2, uVar7 != 0xffff &&
             ((int)uVar10 < (int)uVar9))) {
        if (*(short *)&tabela_unidades[uVar7].field_0xb8 == -1) {
          uVar6 = uVar7;
          if (local_20 != 0) {
            if ((uVar1 & 0x8000) == 0) {
              cVar5 = '\x01';
            }
            else {
              cVar5 = '\x03';
            }
            cVar5 = FUN_00446cb5(uVar7,cVar5);
            uVar6 = extraout_ECX;
            if (cVar5 == '\0') goto LAB_004880e2;
          }
          if ((uVar1 & 0x8000) == 0) {
            bVar8 = tabela_unidades[uVar1].tipo_id;
          }
          else {
            bVar8 = 0x1a;
          }
          uVar6 = FUN_0044f98a(uVar6,bVar8);
          if ((uVar6 & 0xff) != 0) {
            uVar10 = uVar10 + (uVar6 & 0xff);
            if ((uVar1 & 0x8000) == 0) {
              cVar5 = '\x01';
            }
            else {
              cVar5 = '\x03';
            }
            FUN_00445a36(extraout_ECX_00,cVar5);
          }
        }
LAB_004880e2:
        uVar2 = *(ushort *)&pUVar4[uVar7].field_0x108;
      }
      local_20 = local_20 + -1;
    }
    *(short *)((int)in_EAX + param_2 * 8 + 0x12) = (short)uVar10;
  }
  return;
}
