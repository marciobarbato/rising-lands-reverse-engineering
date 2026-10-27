/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00472576, entrada 00472576.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00472576(undefined4 param_1,uint param_2)

{
  ushort uVar1;
  bool bVar2;
  ushort in_AX;
  ushort uVar3;
  ushort *puVar4;

  puVar4 = (ushort *)(&DAT_00508728 + (param_2 & 0xff) * 0x200);
  uVar1 = *puVar4;
  bVar2 = false;
  for (uVar3 = 1; uVar3 <= uVar1; uVar3 = uVar3 + 1) {
    if (bVar2) {
      (&DAT_00508726)[(param_2 & 0xff) * 0x100 + (uint)uVar3] = puVar4[uVar3];
    }
    else {
      if (in_AX == puVar4[uVar3]) {
        bVar2 = true;
      }
      tabela_unidades[in_AX].selecionada = 0;
    }
  }
  if (bVar2) {
    *puVar4 = *puVar4 - 1;
  }
  return;
}
