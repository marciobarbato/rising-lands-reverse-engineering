/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0048873f, entrada 0048873f.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0048873f(undefined4 param_1,int param_2)

{
  ushort uVar1;
  ushort uVar2;
  int in_EAX;
  int iVar3;
  uint uVar4;
  byte bVar5;
  ushort *puVar6;

  if (in_EAX != 0xffff) {
    uVar4 = (uint)tabela_unidades[in_EAX].proprietario_id;
    uVar1 = *(ushort *)&tabela_unidades[in_EAX].field_0xb8;
    if (uVar1 != 0xffff) {
      puVar6 = (ushort *)(&DAT_0051bd24 + uVar4 * 0x451 + param_2 * 0x44 + 4);
      for (iVar3 = 0;
          iVar3 < (int)(uint)*(ushort *)
                              ((int)&DAT_0051bd24 + param_2 * 0x110 + uVar4 * 0x1144 + 0xe);
          iVar3 = iVar3 + 1) {
        uVar2 = *puVar6;
        if (uVar1 == uVar2) {
          if ((uVar2 & 0x8000) == 0) {
            bVar5 = tabela_unidades[uVar2].tipo_id;
          }
          else {
            bVar5 = 0x1a;
          }
          uVar4 = FUN_0044f98a(in_EAX * 0x114,bVar5);
          if ((uint)puVar6[1] < (uVar4 & 0xff)) {
            puVar6[1] = 0;
            return;
          }
          puVar6[1] = puVar6[1] - (short)(uVar4 & 0xff);
          return;
        }
        puVar6 = puVar6 + 4;
      }
    }
  }
  return;
}
