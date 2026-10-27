/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00410a2c, entrada 00410a2c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00410a2c(undefined4 param_1,int param_2)

{
  char cVar1;
  byte bVar2;
  ushort uVar3;
  int iVar4;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  undefined4 uVar5;
  undefined4 extraout_ECX_03;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  ushort unaff_BX;
  ushort uVar6;
  int iVar7;
  undefined8 uVar8;
  ushort local_14;

  uVar8 = FUN_004474a6(param_1,param_2);
  if (*(short *)((int)uVar8 + 2) != 1) {
    uVar5 = extraout_ECX;
    for (uVar3 = 0; uVar3 < *(ushort *)((int)uVar8 + 2); uVar3 = uVar3 + 1) {
      cVar1 = FUN_004472d3(uVar5,(uint)uVar3);
      iVar7 = param_2 + 8;
      if (cVar1 == '\x01') {
        bVar2 = unidade_obter_proprietario(unaff_BX);
        FUN_0045c455('\x01',(short)param_2,bVar2);
        uVar5 = extraout_ECX_05;
      }
      else if (cVar1 == '\x02') {
        iVar7 = FUN_004471b8(extraout_ECX_04,'\x02');
        iVar4 = FUN_004471b8(extraout_ECX_00,'\x02');
        local_14 = (short)iVar7 + (short)iVar4;
        uVar5 = extraout_ECX_01;
        for (uVar6 = 0; uVar6 < local_14; uVar6 = uVar6 + 1) {
          FUN_0045b247('\x01',(short)param_2);
          param_2 = param_2 + 8;
          uVar5 = extraout_ECX_02;
        }
        uVar3 = uVar3 + (uVar6 - 1);
        iVar7 = param_2;
      }
      else {
        FUN_0045b247('\x01',(short)param_2);
        uVar5 = extraout_ECX_03;
      }
      param_2 = iVar7;
    }
  }
  return;
}
