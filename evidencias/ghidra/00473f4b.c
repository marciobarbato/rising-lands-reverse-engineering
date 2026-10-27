/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00473f4b, entrada 00473f4b.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00473f4b(undefined4 param_1,undefined4 param_2)

{
  bool bVar1;
  byte in_AL;
  byte bVar2;
  byte bVar3;
  ushort indice_unidade;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  uint extraout_EDX;
  undefined2 extraout_var;
  uint extraout_EDX_00;
  uint uVar4;
  uint uVar5;
  ushort uVar6;
  longlong lVar7;
  undefined2 local_20;

  bVar1 = false;
  uVar6 = 0;
  lVar7 = FUN_0041a4f4(param_1,param_2);
  bVar2 = (byte)lVar7;
  do {
    if (*(ushort *)(&DAT_00508728 + (uint)in_AL * 0x200) <= uVar6) {
      return;
    }
    lVar7 = FUN_00443dad((uint)*(ushort *)(&DAT_0050872a + (uint)uVar6 * 2 + (uint)in_AL * 0x200),
                         (uint)((ulonglong)lVar7 >> 0x20));
    if ((char)lVar7 != '\0') {
      bVar3 = unidade_obter_tipo(indice_unidade);
      local_20 = (undefined2)param_2;
      uVar4 = (uint)bVar3;
      FUN_00445b10(extraout_ECX,CONCAT22(extraout_var,local_20));
      lVar7 = (ulonglong)extraout_EDX_00 << 0x20;
      if (!bVar1) {
        lVar7 = (ulonglong)extraout_EDX_00 << 0x20;
        bVar1 = true;
        if (in_AL == DAT_00508041) {
          uVar5 = CONCAT31((int3)(extraout_EDX_00 >> 8),bVar2);
          if (bVar2 < 10) {
            lVar7 = (ulonglong)uVar5 << 0x20;
            if (bVar2 != 0) {
              if (bVar2 < 2) goto LAB_00474013;
              lVar7 = (ulonglong)uVar5 << 0x20;
              if ((bVar2 == 2) && (lVar7 = CONCAT44(uVar5,uVar4), uVar4 != 10)) {
                uVar4 = 10;
                goto LAB_00473f7f;
              }
            }
          }
          else {
            if (bVar2 < 0xb) {
LAB_00474013:
              uVar4 = 0xe;
            }
            else {
              lVar7 = (ulonglong)uVar5 << 0x20;
              if (bVar2 < 0xd) goto LAB_00473f84;
              if (bVar2 < 0xe) goto LAB_00474013;
              lVar7 = (ulonglong)uVar5 << 0x20;
              if (bVar2 != 0x10) goto LAB_00473f84;
              if (uVar4 == 9) {
                uVar4 = 0x19;
              }
              else {
                lVar7 = (ulonglong)bVar3 << 0x20;
                if (uVar4 != 10) goto LAB_00473f84;
                uVar4 = 0x24;
              }
            }
LAB_00473f7f:
            FUN_00440d5e(extraout_ECX_00,uVar4);
            lVar7 = (ulonglong)extraout_EDX << 0x20;
          }
        }
      }
    }
LAB_00473f84:
    uVar6 = uVar6 + 1;
  } while( true );
}
