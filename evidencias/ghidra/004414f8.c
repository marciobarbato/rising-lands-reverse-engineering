/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004414f8, entrada 004414f8.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_004414f8(void)

{
  byte bVar1;
  bool bVar2;
  byte bVar3;
  ushort uVar4;
  UnidadeParcial *pUVar5;
  ushort uVar6;
  byte local_18;

  for (uVar6 = 0; uVar6 < 4; uVar6 = uVar6 + 1) {
    for (uVar4 = 0; uVar4 < 5; uVar4 = uVar4 + 1) {
      *(undefined1 *)(&DAT_004e19ec + (uint)uVar6 * 5 + (uint)uVar4) = 0xff;
      *(undefined1 *)((uint)uVar6 * 10 + 0x4e19ed + (uint)uVar4 * 2) = 0;
    }
  }
  for (uVar6 = 0; uVar6 < 800; uVar6 = uVar6 + 1) {
    if (tabela_unidades[uVar6].estado != 0) {
      if ((tabela_unidades[uVar6].estado == 0) || (tabela_unidades[uVar6].estado == 4)) {
        bVar2 = false;
      }
      else {
        bVar2 = true;
      }
      if (bVar2) {
        pUVar5 = tabela_unidades + uVar6;
        uVar4 = 1;
        local_18 = 0;
        bVar3 = *(byte *)((int)&DAT_004e19ec + (uint)pUVar5->proprietario_id * 10 + 1);
        while( true ) {
          if (4 < uVar4) break;
          bVar1 = *(byte *)((int)&DAT_004e19ec +
                           (uint)uVar4 * 2 + (uint)pUVar5->proprietario_id * 10 + 1);
          if (bVar1 < bVar3) {
            local_18 = (byte)uVar4;
            bVar3 = bVar1;
          }
          uVar4 = uVar4 + 1;
        }
        if (bVar3 < (byte)pUVar5->field_0xaf) {
          *(undefined1 *)((uint)pUVar5->proprietario_id * 10 + 0x4e19ed + (uint)local_18 * 2) =
               pUVar5->field_0xaf;
          *(byte *)(&DAT_004e19ec + (uint)pUVar5->proprietario_id * 5 + (uint)local_18) =
               pUVar5->tipo_id;
        }
      }
    }
  }
  return;
}
