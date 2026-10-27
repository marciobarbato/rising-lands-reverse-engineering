/* Pseudocódigo Ghidra, não é fonte original.
 * Função carregar_atributos_tipos, entrada 0044188b.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void carregar_atributos_tipos(void)

{
  LPCSTR lpAppName;
  short extraout_AX;
  UINT UVar1;
  ushort extraout_DX;
  int iVar2;
  ushort local_1c;

  UVar1 = GetPrivateProfileIntA(s_DIVERS_00494819,s_BONUSCAPITAINE_0049480a,2,&DAT_00508f94);
  _DAT_004965ac = (short)UVar1;
  FUN_00441792();
  local_1c = extraout_DX;
  while( true ) {
    if (0x19 < local_1c) break;
    lpAppName = s_SOLDAT_004965ba + (uint)(byte)local_1c * 0x32;
    iVar2 = (uint)local_1c * 0x32;
    FUN_00441792();
    UVar1 = GetPrivateProfileIntA(lpAppName,s_BLINDAGE_00494820,5,&DAT_00508f94);
    (&DAT_004965b9)[iVar2] = (char)UVar1;
    UVar1 = GetPrivateProfileIntA(lpAppName,s_RAYON_00494829,5,&DAT_00508f94);
    *(short *)(&DAT_004965d8 + iVar2) = (short)UVar1;
    UVar1 = GetPrivateProfileIntA(lpAppName,s_PORTEE_0049482f,1,&DAT_00508f94);
    extraout_AX = (short)UVar1;
    *(short *)(&DAT_004965da + iVar2) = extraout_AX;
    *(short *)(&DAT_004965da + iVar2) = extraout_AX * extraout_AX;
    UVar1 = GetPrivateProfileIntA(lpAppName,s_FATIGUE_00494836,3000,&DAT_00508f94);
    *(short *)(&DAT_004965dc + iVar2) = (short)UVar1;
    UVar1 = GetPrivateProfileIntA(lpAppName,s_RECHARGE_0049483e,100,&DAT_00508f94);
    *(short *)(&DAT_004965de + iVar2) = (short)UVar1;
    UVar1 = GetPrivateProfileIntA(lpAppName,s_TMPSRECRUTE_00494847,0x78,&DAT_00508f94);
    *(short *)(&DAT_004965ae + iVar2) = (short)UVar1;
    UVar1 = GetPrivateProfileIntA(lpAppName,s_COUTPATATE_00494853,1,&DAT_00508f94);
    *(short *)(&DAT_004965b0 + iVar2) = (short)UVar1;
    UVar1 = GetPrivateProfileIntA(lpAppName,s_COUTROCHE_0049485e,1,&DAT_00508f94);
    *(short *)(&DAT_004965b4 + iVar2) = (short)UVar1;
    UVar1 = GetPrivateProfileIntA(lpAppName,s_COUTPIECE_00494868,1,&DAT_00508f94);
    *(short *)(&DAT_004965b2 + iVar2) = (short)UVar1;
    local_1c = local_1c + 1;
    GetPrivateProfileStringA
              (lpAppName,&DAT_00494872,lpAppName,s_SOLDAT_004965ba + iVar2,0x1e,&DAT_00508f94);
  }
  return;
}
