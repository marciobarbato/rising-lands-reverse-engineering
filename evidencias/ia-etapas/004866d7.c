/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined4 FUN_004866d7(void)

{
  byte bVar1;
  undefined2 uVar2;
  short sVar3;
  uint in_EAX;
  short extraout_var_02;
  undefined3 extraout_var;
  undefined3 extraout_var_00;
  undefined3 extraout_var_01;
  uint uVar4;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  int extraout_ECX_03;
  int iVar5;
  undefined4 extraout_ECX_04;
  undefined4 extraout_ECX_05;
  uint extraout_ECX_06;
  uint extraout_ECX_07;
  undefined4 extraout_ECX_08;
  undefined4 extraout_ECX_09;
  ushort indice_unidade;
  int iVar6;
  undefined4 uVar7;
  ushort uVar8;
  longlong lVar9;
  undefined8 uVar10;
  int local_38;
  uint local_28;
  ushort local_20 [2];
  ushort local_1c [2];
  undefined2 local_18 [2];

  if (((int)in_EAX < 4) &&
     (iVar6 = (int)(DAT_00521364 * in_EAX) >> 0x1f,
     DAT_00508f7c % DAT_00521364 ==
     (int)((DAT_00521364 * in_EAX + iVar6 * -4) - (uint)(iVar6 << 1 < 0)) >> 2)) {
    lVar9 = FUN_00489728(DAT_00521364,DAT_00508f7c % DAT_00521364);
    if ((int)lVar9 == 0) {
      uVar2 = FUN_00484b76(extraout_ECX,0x10);
      if ((CONCAT22(extraout_var_02,uVar2) == 0 || extraout_var_02 < 0) ||
         (iVar6 = FUN_0047d98b(0,0x2a,0,0,0,0,0), iVar6 != -1)) goto LAB_004867b7;
      uVar7 = 0x2a;
    }
    else {
      iVar6 = FUN_0047d98b(0,0x27,0,0,0,0,0);
      if (iVar6 != -1) goto LAB_004867b7;
      uVar7 = 0x27;
    }
    FUN_0047d920(0,uVar7,0,0,0,0);
  }
LAB_004867b7:
  if ((DAT_00508f7c % *(uint *)(&DAT_0051bcfc + in_EAX * 0x1144) == 0) &&
     (*(char *)((int)&DAT_0051a98e + in_EAX * 0x10 + 1) != '\0')) {
    FUN_00467670(local_18,local_20,(byte)in_EAX);
    bVar1 = FUN_00486e39(local_20,&DAT_00498cd8,local_1c,(&DAT_0051bd08)[in_EAX * 0x451]);
    if (CONCAT31(extraout_var,bVar1) != 0xff) {
      (&DAT_0051bd08)[in_EAX * 0x451] = CONCAT31(extraout_var,bVar1);
    }
    bVar1 = FUN_00486e39(local_20,&DAT_00498cec,local_1c,(&DAT_0051bd0c)[in_EAX * 0x451]);
    if (CONCAT31(extraout_var_00,bVar1) != 0xff) {
      (&DAT_0051bd0c)[in_EAX * 0x451] = CONCAT31(extraout_var_00,bVar1);
    }
    bVar1 = FUN_00486e39(local_20,&DAT_00498ce0,local_1c,(&DAT_0051bd10)[in_EAX * 0x451]);
    if (CONCAT31(extraout_var_01,bVar1) != 0xff) {
      (&DAT_0051bd10)[in_EAX * 0x451] = CONCAT31(extraout_var_01,bVar1);
    }
    uVar4 = FUN_00483867(extraout_ECX_00,0);
    iVar6 = 0;
    uVar7 = extraout_ECX_01;
    if ((uVar4 & 0x7ffffff) != 0x7fd72b1) {
      iVar6 = 0;
      if ((ushort)(&DAT_0051a9f2)[uVar4 * 0x10] != 0) {
        uVar10 = FUN_004837f0(extraout_ECX_01,(uint)(ushort)(&DAT_0051a9f2)[uVar4 * 0x10]);
        iVar6 = 0;
        uVar7 = extraout_ECX_02;
        while ((ushort)uVar10 != 0xffff) {
          lVar9 = FUN_00443dad(uVar7,(uint)(ushort)uVar10);
          uVar4 = (uint)((ulonglong)lVar9 >> 0x20);
          iVar5 = extraout_ECX_03;
          if ((char)lVar9 != '\0') {
            iVar5 = uVar4 * 0x114;
            uVar4 = (uint)tabela_unidades[uVar4].tipo_id;
            iVar6 = iVar6 + *(int *)(&DAT_00498cf4 + uVar4 * 4);
          }
          uVar10 = FUN_00483825(iVar5,uVar4);
          uVar7 = extraout_ECX_04;
        }
      }
    }
    uVar10 = FUN_00485fa3(uVar7,iVar6);
    uVar4 = 0;
    local_38 = 500;
    local_28 = 0;
    do {
      if (uVar4 != in_EAX) {
        sVar3 = FUN_0046dc6c(uVar4,uVar4 & 0xff);
        iVar5 = (int)sVar3;
        uVar7 = FUN_0046d838(extraout_ECX_05,(byte)uVar4);
        if ((char)uVar7 != '\0') {
          iVar5 = iVar5 + 0x19;
        }
        uVar4 = extraout_ECX_06;
        if (iVar5 < local_38) {
          local_38 = iVar5;
          local_28 = extraout_ECX_06;
        }
      }
      uVar4 = uVar4 + 1;
    } while ((int)uVar4 < 4);
    if (((int)uVar10 == 3) && (DAT_00521350 < iVar6)) {
      FUN_0047d920(local_28,0x24,5,0,0,0);
      uVar7 = 1;
    }
    else if (DAT_00521354 < iVar6) {
      FUN_0047d920(local_28,0x24,6,0,0,0);
      uVar7 = 6;
    }
    else {
      iVar6 = 0;
      for (uVar8 = 0; uVar8 < 800; uVar8 = uVar8 + 1) {
        lVar9 = FUN_00443dad(uVar4,(uint)uVar8);
        uVar4 = extraout_ECX_07;
        if ((char)lVar9 != '\0') {
          bVar1 = unidade_obter_proprietario((ushort)((ulonglong)lVar9 >> 0x20));
          uVar4 = CONCAT31((int3)((uint)extraout_ECX_08 >> 8),bVar1);
          if (uVar4 == local_28) {
            bVar1 = unidade_obter_tipo(indice_unidade);
            uVar4 = CONCAT31((int3)((uint)extraout_ECX_09 >> 8),bVar1);
            if ((1 << (bVar1 & 0x1f) & 0x3f1991fU) != 0) {
              iVar6 = iVar6 + *(int *)(&DAT_00498cf4 + (uint)bVar1 * 4);
            }
          }
        }
      }
      if (iVar6 < DAT_00521360) {
        FUN_0047d920(local_28,0x25,3,0,0,0);
        uVar7 = 8;
      }
      else {
        uVar10 = FUN_00485fb9(uVar4,(uint)uVar8);
        if ((int)uVar10 < DAT_00521358) {
          uVar7 = 0;
        }
        else {
          FUN_0047d920(local_28,0x24,2,0,0,0);
          uVar7 = 9;
        }
      }
    }
    *(undefined4 *)(&DAT_0051bd14 + in_EAX * 0x1144) = uVar7;
  }
  return 0;
}
