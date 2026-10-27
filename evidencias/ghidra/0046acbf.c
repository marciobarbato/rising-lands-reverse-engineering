/* Pseudocódigo Ghidra, não é fonte original.
 * Função carregar_unidades_eta, entrada 0046acbf.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void carregar_unidades_eta(void)

{
  bool bVar1;
  char cVar2;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 uVar3;
  undefined4 extraout_ECX_02;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  ushort uVar4;
  ushort local_18;
  ushort local_14;
  ushort local_10;

  FUN_00472555();
  for (uVar4 = 0; uVar4 < 4; uVar4 = uVar4 + 1) {
    (&DAT_004e19bc)[uVar4] = 0x32;
  }
  FUN_00458461(extraout_ECX,2);
  FUN_00458461(extraout_ECX_00,2);
  uVar3 = extraout_ECX_01;
  for (uVar4 = 0; uVar4 < local_14; uVar4 = uVar4 + 1) {
    FUN_00458461(uVar3,2);
    FUN_00458461(extraout_ECX_02,0x8c);
    FUN_0045848b();
    FUN_00458461(tabela_unidades,local_18 - 0x28c);
    tabela_unidades[uVar4].selecionada = 0;
    bVar1 = unidade_esta_ativa(local_10);
    uVar3 = extraout_ECX_03;
    if (bVar1) {
      FUN_00457350();
      tabela_unidades[local_10].vida = 100;
      tabela_unidades[local_10].raio_visao =
           (&DAT_004965d8)[(uint)tabela_unidades[local_10].tipo_id * 0x32];
      tabela_unidades[local_10].alcance_quadrado_u8 =
           (&DAT_004965da)[(uint)tabela_unidades[local_10].tipo_id * 0x32];
      tabela_unidades[local_10].grupo_id = 0xff;
      tabela_unidades[local_10].field_0xf5 = 0;
      tabela_unidades[local_10].field_0xf7 = 0;
      tabela_unidades[local_10].field_0xf8 = 0;
      tabela_unidades[local_10].field_0xf6 = 0;
      tabela_unidades[local_10].field_0xdc = 0;
      *(undefined4 *)&tabela_unidades[local_10].field_0x104 = 0xffffffff;
      *(undefined4 *)&tabela_unidades[local_10].field_0x10c = 0xffffffff;
      *(undefined4 *)&tabela_unidades[local_10].field_0x110 = 0;
      if (tabela_unidades[local_10].estado == 0xe) {
        tabela_unidades[local_10].field_0x72 = 0;
      }
      tabela_unidades[local_10].contador_recarga =
           *(ushort *)(&DAT_004965de + (uint)tabela_unidades[local_10].tipo_id * 0x32);
      if (tabela_unidades[local_10].tipo_id == 4) {
        tabela_unidades[local_10].field_0xda = 10;
      }
      if ((tabela_unidades[local_10].tipo_id == 0x10) || (tabela_unidades[local_10].tipo_id == 0xe))
      {
        tabela_unidades[local_10].field_0xda = 0;
      }
      if (tabela_unidades[local_10].tipo_id == 0x10) {
        tabela_unidades[local_10].proprietario_id = 0;
      }
      unidade_obter_tipo(local_10);
      cVar2 = FUN_004422dd();
      uVar3 = extraout_ECX_04;
      if (cVar2 != '\0') {
        tabela_unidades[local_10].proprietario_id = 4;
      }
    }
  }
  return;
}
