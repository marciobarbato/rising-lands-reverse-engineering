/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00449530, entrada 00449530.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00449530(undefined4 param_1,undefined4 param_2)

{
  bool bVar1;
  UnidadeParcial *pUVar2;
  UnidadeParcial *pUVar3;
  char cVar4;
  ushort in_AX;
  ushort uVar5;
  uint uVar6;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 extraout_EDX;
  undefined8 uVar7;
  longlong lVar8;

  pUVar2 = tabela_unidades;
  if (*(short *)&tabela_unidades[in_AX].field_0xc0 != -1) {
    uVar5 = tabela_unidades[in_AX].celula_destino;
    if (tabela_unidades[in_AX].celula_atual == uVar5) {
      if (uVar5 == *(ushort *)&tabela_unidades[in_AX].field_0xb2) {
        tabela_unidades[in_AX].field_0x90 = 5;
        uVar7 = FUN_00448599(param_1,CONCAT22((short)((uint)param_2 >> 0x10),uVar5));
        if (pUVar2[in_AX].field_0x90 == pUVar2[in_AX].field_0x91) {
          uVar7 = FUN_004237c0(extraout_ECX,(int)((ulonglong)uVar7 >> 0x20));
          if ((char)uVar7 == '\0') {
            FUN_0041a65c(extraout_ECX_00,1);
            lVar8 = FUN_00420c19(extraout_ECX_01,extraout_EDX);
            if ((char)lVar8 != '\0') {
              cVar4 = FUN_00424f5c();
              if (cVar4 == '\0') {
                if ((tabela_unidades[in_AX].estado == 0) || (tabela_unidades[in_AX].estado == 4)) {
                  bVar1 = false;
                }
                else {
                  bVar1 = true;
                }
                if ((bVar1) && (tabela_unidades[in_AX].estado = 7, in_AX == DAT_00496304)) {
                  DAT_004e0f36 = 0;
                  DAT_004e0f37 = 0;
                  DAT_00496304 = 0xffff;
                  DAT_004e0f3c = 0;
                }
              }
              else {
                FUN_00457058();
                uVar5 = FUN_0041aee2();
                pUVar2[in_AX].celula_passo = uVar5;
                pUVar2[in_AX].celula_atual = uVar5;
                pUVar2[in_AX].estado = 0xe;
                FUN_00472648(extraout_ECX_02);
              }
            }
          }
        }
      }
      else {
        uVar6 = FUN_00442668(0,*(ushort *)&tabela_unidades[in_AX].field_0xb2);
        pUVar3 = tabela_unidades;
        if ((char)uVar6 != '\0') {
          tabela_unidades[in_AX].celula_destino = *(ushort *)&pUVar2[in_AX].field_0xb2;
          if (in_AX == DAT_00496304) {
            DAT_004e0f36 = (byte)(in_AX >> 8) ^ (byte)(DAT_00496304 >> 8);
            DAT_004e0f37 = 0;
            DAT_00496304 = 0xffff;
            DAT_004e0f3c = 0;
          }
          pUVar3[in_AX].estado_caminho = 0;
        }
      }
    }
    else {
      FUN_0044930c();
    }
  }
  return;
}
