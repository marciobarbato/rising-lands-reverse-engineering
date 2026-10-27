/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044930c, entrada 0044930c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_0044930c(void)

{
  UnidadeParcial *pUVar1;
  UnidadeParcial *pUVar2;
  uint in_EAX;
  uint uVar3;
  int extraout_ECX;
  undefined8 uVar4;

  pUVar1 = tabela_unidades;
  uVar3 = in_EAX & 0xffff;
  switch(tabela_unidades[uVar3].estado_caminho) {
  case 1:
    tabela_unidades[uVar3].estado_caminho = 0;
    break;
  case 3:
    if ((*(int *)&tabela_unidades[uVar3].field_0x83 >> 0x18 == 0) &&
       (*(int *)&tabela_unidades[uVar3].field_0x84 >> 0x18 == 0)) {
      if (DAT_004e0f36 == '\0') {
        FUN_0043b30b((tabela_unidades[uVar3].field_0xab != '\0') + 1,
                     tabela_unidades[uVar3].celula_destino,
                     *(undefined2 **)(DAT_004e1924 + uVar3 * 4),0,0);
        FUN_0042f214();
        pUVar1[uVar3].estado_caminho = 4;
        return;
      }
      return;
    }
  case 0:
  case 5:
    FUN_00448f50(uVar3 * 0x114);
    break;
  case 4:
    if (DAT_00496302 == '\0') {
      FUN_0042f214();
    }
    else {
      if (DAT_004e0f37 == '\0') {
        if (DAT_004e0f4c == '\b') {
          tabela_unidades[uVar3].estado_caminho = 6;
          pUVar1[uVar3].field_0x8b = 0;
        }
        else {
          uVar4 = FUN_00449176(uVar3 * 0x114,in_EAX);
          pUVar2 = tabela_unidades;
          in_EAX = (uint)((ulonglong)uVar4 >> 0x20);
          if ((char)uVar4 == '\0') {
            *(undefined2 *)((int)&tabela_unidades->celula_destino + extraout_ECX) =
                 *(undefined2 *)((int)&tabela_unidades->celula_passo + extraout_ECX);
            if ((short)((ulonglong)uVar4 >> 0x20) == DAT_00496304) {
              DAT_004e0f36 = '\0';
              DAT_004e0f37 = '\0';
              DAT_00496304 = -1;
              DAT_004e0f3c = 0;
            }
            (&pUVar2->estado_caminho)[extraout_ECX] = 0;
          }
          else {
            pUVar1[uVar3].estado_caminho = 0;
          }
        }
      }
      else {
        if ((tabela_unidades[uVar3].estado == 2) && (DAT_004e0f4c == '\x02')) {
          tabela_unidades[uVar3].celula_destino = DAT_004e0f4a;
          if ((short)in_EAX == DAT_00496304) {
            DAT_004e0f36 = '\0';
            DAT_004e0f37 = '\0';
            DAT_004e0f3c = 0;
            DAT_00496304 = -1;
          }
          pUVar1[uVar3].estado_caminho = 0;
        }
        pUVar1[uVar3].estado_caminho = 5;
      }
      if ((short)in_EAX == DAT_00496304) {
        DAT_004e0f36 = '\0';
        DAT_004e0f37 = '\0';
        DAT_004e0f3c = 0;
        DAT_00496304 = -1;
      }
    }
    break;
  case 6:
    tabela_unidades[uVar3].field_0x8b = tabela_unidades[uVar3].field_0x8b + '\x01';
    if (pUVar1[uVar3].field_0x8b == '\x14') {
      pUVar1[uVar3].field_0x8b = 0;
      pUVar1[uVar3].estado_caminho = 3;
    }
  }
  return;
}
