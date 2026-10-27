/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00444533, entrada 00444533.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00444533(uint param_1,byte param_2)

{
  byte bVar1;
  bool bVar2;
  UnidadeParcial *pUVar3;
  ushort in_AX;
  ushort uVar4;
  UnidadeParcial *pUVar5;
  uint uVar6;
  undefined4 extraout_ECX;
  UnidadeParcial *extraout_ECX_00;
  short unaff_BX;
  char local_14;

  pUVar5 = tabela_unidades;
  if (param_2 != 0) {
    if (param_2 < 2) {
      pUVar3 = tabela_unidades + in_AX;
      do {
        for (uVar4 = 0; uVar4 < pUVar5[in_AX].campo_0c; uVar4 = uVar4 + 1) {
          param_1 = (uint)uVar4;
          if ((&pUVar3->field_0x4c)[(int)&((UnidadeParcial *)param_1)->proprietario_id] == '\x01') {
            bVar1 = tabela_unidades[*(ushort *)(&pUVar5[in_AX].field_0x10 + param_1 * 2)].tipo_id;
            bVar2 = true;
            if (bVar1 < 0xe) {
              if (bVar1 < 6) {
                if ((bVar1 < 3) || (3 < bVar1)) goto LAB_0044474e;
              }
              else if ((bVar1 < 9) || (bVar1 < 0xb)) {
LAB_0044474e:
                bVar2 = true;
                goto LAB_00444750;
              }
LAB_00444744:
              bVar2 = false;
            }
            else {
              if ((bVar1 < 0xf) || (bVar1 < 0x12)) goto LAB_00444744;
              if ((bVar1 < 0x13) || ((bVar1 < 0x17 || (bVar1 < 0x19)))) goto LAB_0044474e;
              if (bVar1 == 0x19) goto LAB_00444744;
            }
LAB_00444750:
            param_1 = (uint)tabela_unidades;
            if (bVar2) {
              bVar2 = true;
              goto LAB_0044475a;
            }
          }
        }
        bVar2 = false;
LAB_0044475a:
        if (!bVar2) {
          return;
        }
        FUN_004438d8(param_1,1);
        param_1 = (uint)extraout_ECX_00;
      } while( true );
    }
    if (param_2 == 2) {
      FUN_0044357c();
      if (unaff_BX == 0) {
        uVar4 = FUN_0047790d(0,10);
        if (uVar4 == 0xffff) {
          return;
        }
        pUVar5[in_AX].estado = 0x11;
        pUVar5[in_AX].field_0x82 = 2;
        *(undefined2 *)&pUVar5[in_AX].field_0x84 = 0;
        pUVar5 = tabela_unidades + in_AX;
        pUVar5->celula_destino = uVar4;
        if (in_AX == DAT_00496304) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_004e0f3c = 0;
          DAT_00496304 = 0xffff;
        }
      }
      else {
        local_14 = (char)unaff_BX;
        FUN_0047790d(local_14 + 0x42,10);
        uVar6 = FUN_004757af(extraout_ECX,local_14 + 'B');
        if ((uVar6 & 0xffff) == 0xffff) {
          FUN_004457d3();
          return;
        }
        pUVar5[in_AX].field_0x82 = 2;
        *(short *)&pUVar5[in_AX].field_0x84 = unaff_BX;
        pUVar5[in_AX].estado = 0x11;
        pUVar5 = tabela_unidades + in_AX;
        pUVar5->celula_destino = (ushort)uVar6;
        if (in_AX == DAT_00496304) {
          DAT_004e0f36 = 0;
          DAT_004e0f37 = 0;
          DAT_004e0f3c = 0;
          DAT_00496304 = 0xffff;
        }
      }
      pUVar5->estado_caminho = 0;
    }
  }
  return;
}
