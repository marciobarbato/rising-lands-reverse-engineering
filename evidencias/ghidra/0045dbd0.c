/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0045dbd0, entrada 0045dbd0.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0045dbd0(undefined4 param_1,byte param_2)

{
  byte bVar1;
  undefined2 uVar2;
  ushort *in_EAX;
  ushort uVar4;
  uint3 uVar3;
  uint uVar5;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 extraout_ECX_01;
  undefined4 extraout_ECX_02;
  short sVar6;
  short sVar7;
  undefined4 extraout_EDX;
  undefined4 extraout_EDX_00;
  undefined4 extraout_EDX_01;
  ushort unaff_BX;
  uint uVar8;
  int iVar9;
  uint uVar10;
  undefined8 uVar11;
  longlong lVar12;
  ulonglong uVar13;
  undefined2 local_ac [2];
  undefined4 local_a8;
  int local_a4;
  uint local_a0;
  undefined4 local_9c;
  int local_98;
  undefined4 local_94;
  undefined4 local_90;
  int local_8c;
  int local_88;
  uint uStack_84;
  uint local_80;
  uint local_7c;
  ushort local_78;
  undefined4 local_74;
  undefined4 local_70;
  undefined4 local_6c;
  undefined4 local_64;
  undefined4 local_60;
  undefined4 local_5c;
  undefined4 local_58;
  undefined2 local_54 [2];
  uint local_50;
  int local_4c;
  undefined4 local_48;
  int iStack_44;
  uint local_40;
  int local_3c;
  undefined4 local_38;
  undefined4 uStack_34;
  int local_30;
  int local_2c;
  undefined4 local_28;
  int local_24;
  undefined4 local_20;
  byte local_1c;
  byte local_18;
  byte local_14;

  uVar10 = 0;
  if (in_EAX[2] == 0) {
    if (((DAT_004e2440 != 0x29b1) || (DAT_004e2442 != 1)) || (DAT_004e2444 != 0)) {
      DAT_004e05a2 = 1;
    }
    DAT_004e2440 = 0x29b1;
  }
  else {
    if (((DAT_004e2440 != 0x29cf) || (DAT_004e2442 != 1)) || (DAT_004e2444 != 0)) {
      DAT_004e05a2 = 1;
    }
    DAT_004e2440 = 0x29cf;
  }
  DAT_004e2444 = 0;
  DAT_004e2442 = 1;
  if (in_EAX[2] + 4 < (uint)*in_EAX) {
    uVar5 = 0;
    if (((DAT_004e2446 != 0x29cf) || (DAT_004e2448 != 1)) || (DAT_004e244a != 0)) {
      DAT_004e05a2 = 1;
    }
    DAT_004e2446 = 0x29cf;
  }
  else {
    uVar5 = 1;
    if (((DAT_004e2446 != 0x29b1) || (DAT_004e2448 != 1)) || (DAT_004e244a != 0)) {
      DAT_004e05a2 = 1;
    }
    DAT_004e2446 = 0x29b1;
  }
  DAT_004e244a = 0;
  DAT_004e2448 = 1;
  local_7c = (uint)in_EAX[2];
  local_18 = param_2;
  do {
    if (in_EAX[1] <= (ushort)local_7c) {
      for (; uVar5 = uVar10 & 0xffff, uVar5 < 4; uVar10 = uVar10 + 1) {
        if ((((&DAT_004e2410)[uVar5 * 3] != 0x29b1) || ((&DAT_004e2412)[uVar5 * 3] != 1)) ||
           ((&DAT_004e2414)[uVar5 * 3] != 0)) {
          DAT_004e05a2 = 1;
        }
        uVar5 = uVar10 & 0xffff;
        (&DAT_004e2410)[uVar5 * 3] = 0x29b1;
        (&DAT_004e2412)[uVar5 * 3] = 1;
        (&DAT_004e2414)[uVar5 * 3] = 0;
      }
      return;
    }
    bVar1 = (byte)in_EAX[(local_7c & 0xffff) + 3];
    local_1c = bVar1;
    switch(*(undefined1 *)((local_7c & 0xffff) + 0x42 + (int)in_EAX)) {
    case 0:
      local_60 = 0x29b1;
      if ((((&DAT_004e2410)[(uVar10 & 0xffff) * 3] != 0x29b1) ||
          ((&DAT_004e2412)[(uVar10 & 0xffff) * 3] != 1)) ||
         ((&DAT_004e2414)[(uVar10 & 0xffff) * 3] != 0)) {
        DAT_004e05a2 = 1;
      }
      (&DAT_004e2410)[(uVar10 & 0xffff) * 3] = 0x29b1;
      (&DAT_004e2412)[(uVar10 & 0xffff) * 3] = 1;
LAB_0045ddf0:
      uVar5 = 0;
      (&DAT_004e2414)[(uVar10 & 0xffff) * 3] = 0;
      break;
    case 2:
      local_48 = 1;
      uVar5 = 0;
      local_4c = in_EAX[(local_7c & 0xffff) + 3] + 0x29f0;
      if ((((short)local_4c != (&DAT_004e2410)[(uVar10 & 0xffff) * 3]) ||
          ((&DAT_004e2412)[(uVar10 & 0xffff) * 3] != 1)) ||
         ((&DAT_004e2414)[(uVar10 & 0xffff) * 3] != 0)) {
        DAT_004e05a2 = 1;
      }
      uVar8 = uVar10 & 0xffff;
      iVar9 = uVar8 * 6;
      (&DAT_004e2410)[uVar8 * 3] = (short)local_4c;
      (&DAT_004e2414)[uVar8 * 3] = 0;
      uVar2 = 1;
LAB_0045dea8:
      *(undefined2 *)((int)&DAT_004e2412 + iVar9) = uVar2;
      break;
    case 3:
      if ((local_18 == 3) && (uVar5 = FUN_00422fa5(uVar5,(uint)DAT_00508041), (char)uVar5 != '\0'))
      {
        local_74 = 0;
        uVar5 = (CONCAT31((int3)((uint)extraout_EDX >> 8),local_1c) & 0xffff00ff) + 0x29b9;
        if (((short)uVar5 != (&DAT_004e2410)[(uVar10 & 0xffff) * 3]) ||
           (((&DAT_004e2412)[(uVar10 & 0xffff) * 3] != 0 ||
            ((&DAT_004e2414)[(uVar10 & 0xffff) * 3] != 0)))) {
          DAT_004e05a2 = 1;
        }
        uVar8 = uVar10 & 0xffff;
        iVar9 = uVar8 * 6;
        (&DAT_004e2410)[uVar8 * 3] = (short)uVar5;
        sVar6 = 0;
        (&DAT_004e2412)[uVar8 * 3] = 0;
        local_80 = uVar10;
      }
      else {
        FUN_0041aace(local_54,local_ac);
        iVar9 = FUN_004676e5(0,local_78,DAT_00508041);
        uVar4 = (ushort)((uint)iVar9 >> 0x10);
        if ((char)iVar9 != '\0') {
          uVar8 = uVar10 & 0xffff;
          uVar5 = 1;
          iVar9 = CONCAT31((int3)(((uint)uVar4 << 0x10) >> 8),local_1c) + 0x29b9;
          if ((((short)iVar9 != (&DAT_004e2410)[uVar8 * 3]) || ((&DAT_004e2412)[uVar8 * 3] != 1)) ||
             ((&DAT_004e2414)[uVar8 * 3] != 0)) {
            DAT_004e05a2 = 1;
          }
          local_a0 = uVar10;
          local_98 = iVar9;
LAB_0045dff9:
          sVar6 = 0;
          (&DAT_004e2410)[(uVar10 & 0xffff) * 3] = (short)iVar9;
          (&DAT_004e2412)[(uVar10 & 0xffff) * 3] = (short)uVar5;
LAB_0045e007:
          (&DAT_004e2414)[(uVar10 & 0xffff) * 3] = sVar6;
          break;
        }
        local_94 = 0;
        local_90 = 0;
        uVar8 = uVar10 & 0xffff;
        uVar5 = CONCAT31((int3)(((uint)uVar4 << 0x10) >> 8),local_1c) + 0x29b9;
        if ((((short)uVar5 != (&DAT_004e2410)[uVar8 * 3]) || ((&DAT_004e2412)[uVar8 * 3] != 0)) ||
           ((&DAT_004e2414)[uVar8 * 3] != 0)) {
          DAT_004e05a2 = 1;
        }
        uVar8 = uVar10 & 0xffff;
        iVar9 = uVar8 * 6;
        (&DAT_004e2410)[uVar8 * 3] = (short)uVar5;
        (&DAT_004e2412)[uVar8 * 3] = 0;
        sVar6 = 0;
      }
      goto LAB_0045e279;
    case 4:
      if (local_18 != 0) {
        if (local_18 < 2) {
          uVar11 = FUN_0044828b(uVar5,(uint)CONCAT11((char)(local_7c >> 8),bVar1));
          uVar11 = FUN_004746e4(extraout_ECX_00,
                                CONCAT31((int3)((ulonglong)uVar11 >> 0x28),(char)uVar11));
          uVar4 = (ushort)((ulonglong)uVar11 >> 0x10);
          if ((byte)uVar11 <= (byte)((ulonglong)uVar11 >> 0x20)) {
            local_a4 = CONCAT31((int3)(((uint)uVar4 << 0x10) >> 8),local_1c) + 0x29ea;
            if ((((&DAT_004e2410)[(uVar10 & 0xffff) * 3] != (short)local_a4) ||
                ((&DAT_004e2412)[(uVar10 & 0xffff) * 3] != 1)) ||
               ((&DAT_004e2414)[(uVar10 & 0xffff) * 3] != 0)) {
              DAT_004e05a2 = 1;
            }
            (&DAT_004e2410)[(uVar10 & 0xffff) * 3] = (short)local_a4;
            (&DAT_004e2412)[(uVar10 & 0xffff) * 3] = 1;
            goto LAB_0045ddf0;
          }
          uVar3 = (uint3)(((uint)uVar4 << 0x10) >> 8);
          sVar6 = (short)CONCAT31(uVar3,local_1c) + 0x29ea;
          local_88 = (uint)uVar3 << 8;
          uVar5 = 0;
          if (((sVar6 != (&DAT_004e2410)[(uVar10 & 0xffff) * 3]) ||
              ((&DAT_004e2412)[(uVar10 & 0xffff) * 3] != 0)) ||
             ((&DAT_004e2414)[(uVar10 & 0xffff) * 3] != 0)) {
            DAT_004e05a2 = 1;
          }
          (&DAT_004e2410)[(uVar10 & 0xffff) * 3] = sVar6;
        }
        else {
          if (local_18 != 3) break;
          uVar5 = FUN_00420ba5(uVar5,(uint)DAT_00508041);
          if ((char)uVar5 != '\0') {
            lVar12 = FUN_00423f83(extraout_ECX,(uint)DAT_00508041);
            uVar3 = (uint3)(((uint)(ushort)((ulonglong)lVar12 >> 0x30) << 0x10) >> 8);
            uVar5 = CONCAT31(uVar3,local_1c) + 0x29ea;
            iStack_44 = (uint)uVar3 << 8;
            sVar6 = (short)lVar12;
            if ((((short)uVar5 != (&DAT_004e2410)[(uVar10 & 0xffff) * 3]) ||
                ((&DAT_004e2412)[(uVar10 & 0xffff) * 3] != 0)) ||
               (sVar6 != (&DAT_004e2414)[(uVar10 & 0xffff) * 3])) {
              DAT_004e05a2 = 1;
            }
            (&DAT_004e2410)[(uVar10 & 0xffff) * 3] = (short)uVar5;
            (&DAT_004e2412)[(uVar10 & 0xffff) * 3] = 0;
            goto LAB_0045e007;
          }
          uVar5 = FUN_00422fa5(extraout_ECX,(uint)DAT_00508041);
          if ((char)uVar5 != '\0') {
            uVar5 = 0;
            local_28 = 0;
            local_2c = (CONCAT31((int3)((uint)extraout_EDX_00 >> 8),local_1c) & 0xffff00ff) + 0x29ea
            ;
            if ((((short)local_2c != (&DAT_004e2410)[(uVar10 & 0xffff) * 3]) ||
                ((&DAT_004e2412)[(uVar10 & 0xffff) * 3] != 0)) ||
               ((&DAT_004e2414)[(uVar10 & 0xffff) * 3] != 0)) {
              DAT_004e05a2 = 1;
            }
            uVar8 = uVar10 & 0xffff;
            iVar9 = uVar8 * 6;
            (&DAT_004e2410)[uVar8 * 3] = (short)local_2c;
            (&DAT_004e2412)[uVar8 * 3] = 0;
            sVar6 = 0;
            goto LAB_0045e279;
          }
          FUN_004746fe(local_54,local_ac);
          iVar9 = FUN_004676e5(0,local_78,DAT_00508041);
          if ((char)iVar9 == '\0') {
            local_58 = 0;
            uVar8 = uVar10 & 0xffff;
            uVar5 = 0;
            local_30 = (CONCAT31((int3)((uint)iVar9 >> 8),local_1c) & 0xffff00ff) + 0x29ea;
            if ((((short)local_30 != (&DAT_004e2410)[uVar8 * 3]) ||
                ((&DAT_004e2412)[uVar8 * 3] != 0)) || ((&DAT_004e2414)[uVar8 * 3] != 0)) {
              DAT_004e05a2 = 1;
            }
            uVar8 = uVar10 & 0xffff;
            iVar9 = uVar8 * 6;
            (&DAT_004e2410)[uVar8 * 3] = (short)local_30;
            (&DAT_004e2414)[uVar8 * 3] = 0;
            uVar2 = 0;
            goto LAB_0045dea8;
          }
          local_64 = 0;
          uVar8 = uVar10 & 0xffff;
          uVar5 = 1;
          if ((((ushort)(local_1c + 0x29ea) != (&DAT_004e2410)[uVar8 * 3]) ||
              ((&DAT_004e2412)[uVar8 * 3] != 1)) || ((&DAT_004e2414)[uVar8 * 3] != 0)) {
            DAT_004e05a2 = 1;
          }
          (&DAT_004e2410)[(uVar10 & 0xffff) * 3] = local_1c + 0x29ea;
          local_50 = uVar10;
        }
        iVar9 = (uVar10 & 0xffff) * 6;
        sVar6 = 0;
        (&DAT_004e2412)[(uVar10 & 0xffff) * 3] = (short)uVar5;
        goto LAB_0045e279;
      }
      break;
    case 6:
      local_14 = bVar1;
      uVar5 = FUN_00420bdf(uVar5,(uint)DAT_00508041);
      if ((char)uVar5 == '\0') {
        uVar5 = FUN_00422fa5(extraout_ECX_01,(uint)DAT_00508041);
        if ((char)uVar5 == '\0') {
          if (bVar1 == 0x19) {
            local_14 = 0x12;
          }
          FUN_004410d2(local_54,local_ac);
          iVar9 = FUN_004676e5(0,local_78,DAT_00508041);
          uVar4 = (ushort)((uint)iVar9 >> 0x10);
          if ((char)iVar9 == '\0') {
            uVar8 = uVar10 & 0xffff;
            uVar5 = 0;
            iVar9 = CONCAT31((int3)(((uint)uVar4 << 0x10) >> 8),local_14) + 0x29cf;
            if ((((short)iVar9 != (&DAT_004e2410)[uVar8 * 3]) || ((&DAT_004e2412)[uVar8 * 3] != 0))
               || ((&DAT_004e2414)[uVar8 * 3] != 0)) {
              DAT_004e05a2 = 1;
            }
            local_40 = uVar10;
            local_3c = iVar9;
            goto LAB_0045dff9;
          }
          local_a8 = 0;
          uVar5 = uVar10 & 0xffff;
          local_8c = CONCAT31((int3)(((uint)uVar4 << 0x10) >> 8),local_14) + 0x29cf;
          if ((((short)local_8c != (&DAT_004e2410)[uVar5 * 3]) || ((&DAT_004e2412)[uVar5 * 3] != 1))
             || ((&DAT_004e2414)[uVar5 * 3] != 0)) {
            DAT_004e05a2 = 1;
          }
          uVar5 = uVar10 & 0xffff;
          iVar9 = uVar5 * 6;
          (&DAT_004e2410)[uVar5 * 3] = (short)local_8c;
          (&DAT_004e2412)[uVar5 * 3] = 1;
          sVar6 = 0;
          uVar5 = uVar10;
        }
        else {
          if (bVar1 == 0x19) {
            local_14 = 0x12;
          }
          local_9c = 0;
          local_5c = 0;
          uVar5 = uVar10 & 0xffff;
          if ((((ushort)(local_14 + 0x29cf) != (&DAT_004e2410)[uVar5 * 3]) ||
              ((&DAT_004e2412)[uVar5 * 3] != 0)) || ((&DAT_004e2414)[uVar5 * 3] != 0)) {
            DAT_004e05a2 = 1;
          }
          uVar5 = uVar10 & 0xffff;
          iVar9 = uVar5 * 6;
          (&DAT_004e2410)[uVar5 * 3] = local_14 + 0x29cf;
          (&DAT_004e2412)[uVar5 * 3] = 0;
          sVar6 = 0;
          uVar5 = uVar10;
        }
      }
      else {
        if (bVar1 == 0x19) {
          local_14 = 0x12;
        }
        local_6c = 0;
        uVar8 = uVar10 & 0xffff;
        lVar12 = FUN_00423f83(extraout_ECX_01,(uint)DAT_00508041);
        uStack_34 = (undefined4)lVar12;
        uVar5 = CONCAT31((int3)(((uint)(ushort)((ulonglong)lVar12 >> 0x30) << 0x10) >> 8),local_14)
                + 0x29cf;
        sVar7 = (short)uVar5;
        sVar6 = (short)lVar12;
        if (((sVar7 != (&DAT_004e2410)[uVar8 * 3]) || ((&DAT_004e2412)[uVar8 * 3] != 0)) ||
           (sVar6 != (&DAT_004e2414)[uVar8 * 3])) {
          DAT_004e05a2 = 1;
        }
        uVar8 = uVar10 & 0xffff;
        iVar9 = uVar8 * 6;
        (&DAT_004e2410)[uVar8 * 3] = sVar7;
        (&DAT_004e2412)[uVar8 * 3] = (short)local_6c;
        uStack_84 = uVar10;
      }
      goto LAB_0045e279;
    case 7:
      if ((local_18 == 1) && (bVar1 = unidade_obter_tipo(unaff_BX), bVar1 == 0xe)) {
        uVar13 = FUN_0044828b(extraout_ECX_02,extraout_EDX_01);
        if ((uVar13 & 0xff) == 0) {
          uVar5 = uVar10 & 0xffff;
          local_24 = ((uint)(uVar13 >> 0x20) & 0xff) + 0x29e2;
          local_20 = 0;
          if ((((short)local_24 != (&DAT_004e2410)[uVar5 * 3]) || ((&DAT_004e2412)[uVar5 * 3] != 0))
             || ((&DAT_004e2414)[uVar5 * 3] != 0)) {
            DAT_004e05a2 = 1;
          }
          uVar5 = uVar10 & 0xffff;
          iVar9 = uVar5 * 6;
          (&DAT_004e2410)[uVar5 * 3] = (short)local_24;
          (&DAT_004e2414)[uVar5 * 3] = 0;
          uVar2 = 0;
          uVar5 = uVar10;
          goto LAB_0045dea8;
        }
      }
      local_70 = 0;
      uVar5 = uVar10 & 0xffff;
      local_38 = 1;
      sVar6 = (short)(local_1c + 0x29e2);
      if (((sVar6 != (&DAT_004e2410)[uVar5 * 3]) || ((&DAT_004e2412)[uVar5 * 3] != 1)) ||
         ((&DAT_004e2414)[uVar5 * 3] != 0)) {
        DAT_004e05a2 = 1;
      }
      uVar5 = uVar10 & 0xffff;
      iVar9 = uVar5 * 6;
      (&DAT_004e2410)[uVar5 * 3] = sVar6;
      (&DAT_004e2412)[uVar5 * 3] = 1;
      sVar6 = 0;
      uVar5 = local_1c + 0x29e2;
LAB_0045e279:
      *(short *)((int)&DAT_004e2414 + iVar9) = sVar6;
    }
    uVar10 = uVar10 + 1;
    if ((uVar10 & 0xffff) == 4) {
      return;
    }
    local_7c = local_7c + 1;
  } while( true );
}
