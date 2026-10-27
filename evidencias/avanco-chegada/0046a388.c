/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall OriginaisSBL::SetMiniMap(undefined4 param_1,undefined1 param_2)

{
  byte in_AL;
  undefined1 uVar1;
  char cVar2;
  ushort uVar3;
  uint uVar4;
  undefined4 uVar5;
  char *pcVar6;
  uint uVar7;
  uint extraout_ECX;
  undefined4 extraout_ECX_00;
  uint extraout_ECX_01;
  uint extraout_ECX_02;
  uint extraout_ECX_03;
  uint extraout_ECX_04;
  uint extraout_ECX_05;
  uint extraout_ECX_06;
  undefined2 extraout_var;
  int iVar8;
  uint extraout_ECX_07;
  uint extraout_ECX_08;
  uint extraout_ECX_09;
  uint extraout_ECX_10;
  undefined1 *puVar9;
  uint extraout_EDX;
  undefined4 extraout_EDX_00;
  uint extraout_EDX_01;
  undefined4 extraout_EDX_02;
  uint uVar10;
  uint extraout_EDX_03;
  uint extraout_EDX_04;
  undefined4 extraout_EDX_05;
  ushort unaff_BX;
  uint uVar11;
  ushort uVar12;
  undefined8 uVar13;
  uint local_34;
  ushort local_2c;

  local_34 = (uint)DAT_00496fe0 / (uint)DAT_00497168;
  local_2c = DAT_00496fe2 / DAT_0049716a;
  if ((ushort)local_34 == 0) {
    local_34 = 1;
  }
  if (local_2c == 0) {
    local_2c = 1;
  }
  uVar12 = 0;
  uVar11 = (uint)(ushort)((short)(((uint)(unaff_BX >> 8) * (uint)DAT_00496fe2) / (uint)DAT_0049716a)
                         * DAT_00496fe2) +
           (((uint)unaff_BX % 0x100) * (uint)DAT_00496fe0) / (uint)DAT_00497168;
  uVar7 = (uint)DAT_00496fe2;
  uVar4 = local_34;
  do {
    if (local_2c <= uVar12) {
      return;
    }
    for (uVar3 = 0; uVar3 < (ushort)local_34; uVar3 = uVar3 + 1) {
      switch(param_2) {
      case 1:
        if (in_AL == DAT_00508041) {
          uVar13 = TerrainGetColor(uVar7,0);
          uVar7 = DAT_00507d5c;
          puVar9 = (undefined1 *)
                   (CONCAT31((int3)((ulonglong)uVar13 >> 0x28),(char)uVar13) + DAT_004e24b4);
          uVar1 = *puVar9;
          uVar4 = CONCAT31((int3)((uint)puVar9 >> 8),uVar1);
          *(undefined1 *)(DAT_00507d5c + (uVar11 & 0xffff)) = uVar1;
        }
        break;
      case 2:
        if (in_AL == DAT_00508041) {
          uVar7 = uVar11 & 0xffff;
          pcVar6 = (char *)(DAT_00507d60 + uVar7);
          if ((*pcVar6 != '\0') || (pcVar6 = (char *)(DAT_00507d64 + uVar7), *pcVar6 != '\0')) {
LAB_0046a4fa:
            uVar4 = DAT_00507d5c;
            goto LAB_0046a500;
          }
          uVar13 = TerrainGetColor(uVar7,uVar4);
          cVar2 = (char)uVar13;
          uVar7 = extraout_ECX;
          uVar4 = DAT_00507d5c;
LAB_0046a502:
          *(char *)(uVar7 + uVar4) = cVar2;
        }
        break;
      case 3:
        if (in_AL == DAT_00508041) {
          uVar13 = TerrainGetColor(uVar7,0);
          pcVar6 = (char *)(DAT_004e24b4 + CONCAT31((int3)((ulonglong)uVar13 >> 0x28),(char)uVar13))
          ;
          uVar4 = uVar11 & 0xffff;
          uVar7 = DAT_00507d5c;
LAB_0046a500:
          cVar2 = *pcVar6;
          goto LAB_0046a502;
        }
        break;
      case 4:
        uVar1 = PlayerGetColor();
        *(undefined1 *)((uVar11 & 0xffff) + DAT_00507d60) = uVar1;
        uVar5 = TerrainEstIllumine(extraout_ECX_00,(uint)DAT_00508041);
        uVar7 = extraout_ECX_01;
        uVar4 = extraout_EDX;
        if ((char)uVar5 != '\0') {
          uVar1 = PlayerGetColor();
          uVar4 = CONCAT31((int3)((uint)extraout_EDX_00 >> 8),uVar1);
          *(undefined1 *)((uVar11 & 0xffff) + DAT_00507d5c) = uVar1;
          uVar7 = extraout_ECX_02;
        }
        break;
      case 5:
        *(undefined1 *)((uVar11 & 0xffff) + DAT_00507d60) = 0;
        uVar5 = TerrainEstDecouvert((uint)unaff_BX,(uint)DAT_00508041);
        uVar7 = extraout_ECX_03;
        uVar4 = extraout_EDX_01;
        if ((char)uVar5 != '\0') {
          uVar5 = TerrainEstIllumine(extraout_ECX_03,(uint)DAT_00508041);
          if ((char)uVar5 == '\0') {
            uVar13 = TerrainGetColor(extraout_ECX_04,extraout_EDX_02);
            uVar4 = (uint)uVar13 & 0xff;
            uVar7 = extraout_ECX_06;
            uVar10 = DAT_004e24b4;
LAB_0046a60c:
            pcVar6 = (char *)(uVar4 + uVar10);
            goto LAB_0046a60e;
          }
          pcVar6 = (char *)(DAT_00507d64 + (uVar11 & 0xffff));
          uVar7 = extraout_ECX_04;
          uVar5 = extraout_EDX_02;
          if (*pcVar6 != '\0') goto LAB_0046a60e;
LAB_0046a5eb:
          uVar13 = TerrainGetColor(uVar7,uVar5);
          cVar2 = (char)uVar13;
          uVar7 = extraout_ECX_05;
LAB_0046a616:
          uVar4 = DAT_00507d5c;
          *(char *)(DAT_00507d5c + (uVar11 & 0xffff)) = cVar2;
        }
        break;
      case 6:
        cVar2 = PlayerGetColor();
        iVar8 = CONCAT22(extraout_var,(short)uVar11);
        *(char *)(iVar8 + DAT_00507d64) = cVar2 + '\x02';
        uVar5 = TerrainEstIllumine(iVar8,(uint)DAT_00508041);
        uVar7 = extraout_ECX_07;
        uVar4 = extraout_EDX_03;
        if ((char)uVar5 != '\0') {
          pcVar6 = (char *)(DAT_00507d60 + extraout_ECX_07);
          if (*pcVar6 != '\0') goto LAB_0046a4fa;
          cVar2 = *(char *)(extraout_ECX_07 + DAT_00507d64);
          uVar4 = DAT_00507d5c;
          goto LAB_0046a502;
        }
        break;
      case 7:
        *(undefined1 *)((uVar11 & 0xffff) + DAT_00507d64) = 0;
        uVar5 = TerrainEstDecouvert((uint)unaff_BX,(uint)DAT_00508041);
        uVar7 = extraout_ECX_08;
        uVar4 = extraout_EDX_04;
        if ((char)uVar5 != '\0') {
          uVar5 = TerrainEstIllumine(extraout_ECX_08,(uint)DAT_00508041);
          if ((char)uVar5 == '\0') {
            uVar13 = TerrainGetColor(extraout_ECX_09,0);
            uVar4 = DAT_004e24b4;
            uVar7 = extraout_ECX_10;
            uVar10 = CONCAT31((int3)((ulonglong)uVar13 >> 0x28),(char)uVar13);
            goto LAB_0046a60c;
          }
          pcVar6 = (char *)(DAT_00507d60 + (uVar11 & 0xffff));
          uVar7 = extraout_ECX_09;
          uVar5 = extraout_EDX_05;
          if (*pcVar6 == '\0') goto LAB_0046a5eb;
LAB_0046a60e:
          cVar2 = *pcVar6;
          goto LAB_0046a616;
        }
      }
      uVar11 = uVar11 + 1;
    }
    uVar12 = uVar12 + 1;
    uVar11 = uVar11 + (0x80 - local_34);
    uVar7 = 0x80 - local_34;
  } while( true );
}
