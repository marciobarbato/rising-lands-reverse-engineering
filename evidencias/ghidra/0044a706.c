/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044a706, entrada 0044a706.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0044a706(undefined4 param_1)

{
  bool bVar1;
  UnidadeParcial *pUVar2;
  UnidadeParcial *pUVar3;
  short sVar4;
  uint in_EAX;
  undefined4 uVar5;
  undefined4 extraout_ECX;
  uint uVar6;
  undefined4 extraout_ECX_00;
  char cVar8;
  uint uVar7;
  undefined4 extraout_EDX;
  ushort uVar9;
  undefined8 uVar10;

  pUVar2 = tabela_unidades;
  sVar4 = (short)in_EAX;
  uVar7 = in_EAX & 0xffff;
  if (tabela_unidades[uVar7].tipo_id == 0xe) {
    if (tabela_unidades[uVar7].field_0x89 == '\0') {
      if (((tabela_unidades[uVar7].celula_atual == tabela_unidades[uVar7].celula_destino) &&
          (*(int *)&tabela_unidades[uVar7].field_0x83 >> 0x18 == 0)) &&
         (*(int *)&tabela_unidades[uVar7].field_0x84 >> 0x18 == 0)) {
        if (tabela_unidades[uVar7].celula_atual == *(ushort *)&tabela_unidades[uVar7].field_0xb2) {
          tabela_unidades[uVar7].field_0x89 = 1;
          pUVar2[uVar7].field_0x8b = 0x14;
          pUVar2[uVar7].field_0xa9 = 0;
          pUVar2[uVar7].field_0xa4 = 0;
        }
        else if ((*(short *)&tabela_unidades[uVar7].field_0xd8 == 0) ||
                (tabela_unidades[uVar7].field_0xda == '\0')) {
          if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
             (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
            bVar1 = false;
          }
          else {
            bVar1 = true;
          }
          if ((bVar1) && (tabela_unidades[in_EAX & 0xffff].estado = 7, sVar4 == DAT_00496304)) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
          }
          pUVar2[uVar7].estado_caminho = 0;
        }
        else {
          uVar9 = *(ushort *)&tabela_unidades[uVar7].field_0xc4;
          tabela_unidades[uVar7].celula_destino = uVar9;
          if (sVar4 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_00496304 = -1;
            DAT_004e0f3c = 0;
          }
          pUVar2[uVar7].estado_caminho = 0;
          pUVar2[uVar7].estado_caminho = 0;
          pUVar2[uVar7].field_0x89 = 0;
          pUVar2[uVar7].estado = 0x16;
          *(ushort *)&pUVar2[uVar7].field_0xb2 = uVar9;
          for (uVar9 = 0; uVar9 < *(ushort *)&pUVar2[uVar7].field_0xd8; uVar9 = uVar9 + 1) {
            *(undefined2 *)(&pUVar2[uVar7].field_0xc4 + (uint)uVar9 * 2) =
                 *(undefined2 *)(&pUVar2[uVar7].field_0xc6 + (uint)uVar9 * 2);
          }
          *(ushort *)&pUVar2[uVar7].field_0xd8 = *(ushort *)&pUVar2[uVar7].field_0xd8 - 1;
        }
      }
      else {
        FUN_0044930c();
      }
    }
    else if (tabela_unidades[uVar7].field_0x89 == '\x01') {
      FUN_00447e12(param_1,uVar7);
      if (pUVar2[uVar7].field_0x8b == '\x14') {
        FUN_00475431(extraout_ECX,pUVar2[uVar7].celula_atual);
        if (tabela_unidades[uVar7].field_0xda != '\0') {
          tabela_unidades[uVar7].field_0xda = tabela_unidades[uVar7].field_0xda + -1;
        }
        pUVar3 = tabela_unidades;
        uVar6 = in_EAX & 0xffff;
        uVar5 = FUN_004766f0(uVar6,(uint)DAT_00508041);
        if ((char)uVar5 != '\0') {
          uVar10 = FUN_00440c5d(extraout_ECX_00,extraout_EDX);
          pUVar3[uVar6].field_0xf9 = 0;
          if (*(int *)&pUVar3[uVar6].field_0x104 == -1) {
            FUN_0048aa79(0,(uint)pUVar3[uVar6].tipo_id << 0x10 | 0x2300,(uint)uVar10);
          }
        }
      }
      cVar8 = pUVar2[uVar7].field_0x8b + -1;
      pUVar2[uVar7].field_0x8b = cVar8;
      pUVar3 = tabela_unidades;
      if (cVar8 == '\0') {
        if (*(short *)&pUVar2[uVar7].field_0xd8 == 0) {
          if ((tabela_unidades[in_EAX & 0xffff].estado == 0) ||
             (tabela_unidades[in_EAX & 0xffff].estado == 4)) {
            bVar1 = false;
          }
          else {
            bVar1 = true;
          }
          if ((bVar1) && (tabela_unidades[in_EAX & 0xffff].estado = 7, sVar4 == DAT_00496304)) {
            DAT_004e0f36 = (byte)in_EAX ^ (byte)DAT_00496304;
            DAT_004e0f37 = (byte)(in_EAX >> 8) ^ (byte)((ushort)DAT_00496304 >> 8);
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
          }
          pUVar2 = tabela_unidades;
          uVar7 = in_EAX & 0xffff;
          tabela_unidades[uVar7].celula_destino = tabela_unidades[uVar7].celula_passo;
          if (sVar4 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_00496304 = -1;
            DAT_004e0f3c = 0;
          }
          pUVar2[uVar7].estado_caminho = 0;
        }
        else {
          uVar7 = in_EAX & 0xffff;
          uVar9 = *(ushort *)&tabela_unidades[uVar7].field_0xc4;
          tabela_unidades[uVar7].celula_destino = uVar9;
          if (sVar4 == DAT_00496304) {
            DAT_004e0f36 = 0;
            DAT_004e0f37 = 0;
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
          }
          pUVar3[uVar7].estado_caminho = 0;
          pUVar3[uVar7].estado_caminho = 0;
          pUVar3[uVar7].field_0x89 = 0;
          pUVar3[uVar7].estado = 0x16;
          *(ushort *)&pUVar3[uVar7].field_0xb2 = uVar9;
          for (uVar9 = 0; uVar9 < *(ushort *)&pUVar3[uVar7].field_0xd8; uVar9 = uVar9 + 1) {
            *(undefined2 *)(&pUVar3[uVar7].field_0xc4 + (uint)uVar9 * 2) =
                 *(undefined2 *)(&pUVar3[uVar7].field_0xc6 + (uint)uVar9 * 2);
          }
          *(ushort *)&pUVar3[uVar7].field_0xd8 = *(ushort *)&pUVar3[uVar7].field_0xd8 - 1;
        }
      }
    }
  }
  return;
}
