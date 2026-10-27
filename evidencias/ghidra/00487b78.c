/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00487b78, entrada 00487b78.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

byte __fastcall FUN_00487b78(undefined4 param_1,int param_2)

{
  ushort uVar1;
  byte bVar2;
  undefined4 in_EAX;
  ushort *puVar3;
  undefined4 *puVar4;
  uint extraout_ECX;
  uint extraout_ECX_00;
  undefined4 *puVar5;
  uint uVar6;
  int iVar7;
  uint unaff_EBX;
  uint uVar8;
  uint uVar9;
  uint uVar10;
  undefined8 uVar11;
  uint local_24;
  ushort indice_unidade;

  indice_unidade = (ushort)unaff_EBX;
  if ((unaff_EBX & 0x8000) == 0) {
    bVar2 = unidade_obter_proprietario(indice_unidade);
    uVar9 = (uint)bVar2;
    uVar8 = extraout_ECX_00;
  }
  else {
    uVar11 = FUN_0041a08c(in_EAX,param_2);
    uVar9 = (uint)uVar11;
    uVar8 = extraout_ECX;
  }
  if ((uVar9 & 0xff) == uVar8) {
    bVar2 = (byte)uVar9 ^ (byte)uVar8;
  }
  else {
    puVar5 = &DAT_0051bd24 + uVar8 * 0x451 + param_2 * 0x44;
    if (*(ushort *)((int)puVar5 + 0xe) < 0x20) {
      puVar3 = (ushort *)(puVar5 + 4);
      if ((unaff_EBX & 0x8000) == 0) {
        bVar2 = (byte)*(undefined4 *)
                       (&DAT_00498cf4 + (uint)tabela_unidades[unaff_EBX & 0xffff].tipo_id * 4);
      }
      else {
        bVar2 = (byte)*(undefined4 *)
                       (&DAT_00498d5c +
                       (uint)(byte)(&DAT_0049a0d0)[(uint)(indice_unidade & 0x7fff) * 0x114] * 4);
      }
      uVar8 = 0xffffffff;
      uVar9 = 0xffffffff;
      uVar6 = 0;
      while (((int)uVar6 < (int)(uint)*(ushort *)((int)puVar5 + 0xe) && (uVar8 == 0xffffffff))) {
        if (*puVar3 == unaff_EBX) {
          if (puVar3[1] == 0) {
            FUN_00487eef(puVar5,uVar6);
          }
          goto LAB_00487bef;
        }
        if (puVar3[2] == (ushort)bVar2) {
          if ((unaff_EBX & 0x8000) == 0) {
            uVar10 = (uint)tabela_unidades[unaff_EBX & 0xffff].vida;
          }
          else {
            uVar10 = (uint)*(ushort *)(&DAT_0049a0d2 + (unaff_EBX & 0x7fff) * 0x114) -
                     (uint)(ushort)(&DAT_0049a0ce)[(unaff_EBX & 0x7fff) * 0x8a];
          }
          uVar1 = *puVar3;
          if ((uVar1 & 0x8000) == 0) {
            local_24 = (uint)tabela_unidades[uVar1].vida;
          }
          else {
            local_24 = (uint)*(ushort *)(&DAT_0049a0d2 + (uint)(uVar1 & 0x7fff) * 0x114) -
                       (uint)(ushort)(&DAT_0049a0ce)[(uint)(uVar1 & 0x7fff) * 0x8a];
          }
          if ((int)uVar10 < (int)local_24) {
            uVar9 = uVar6;
          }
        }
        else if (puVar3[2] < (ushort)bVar2) {
          if (uVar9 == 0xffffffff) {
            uVar8 = uVar6;
          }
          else {
            uVar8 = uVar9;
          }
        }
        puVar3 = puVar3 + 4;
        uVar6 = uVar6 + 1;
      }
      if (uVar8 == 0xffffffff) {
        *(ushort *)(puVar5 + (uint)*(ushort *)((int)puVar5 + 0xe) * 2 + 5) = (ushort)bVar2;
        *(ushort *)(puVar5 + (uint)*(ushort *)((int)puVar5 + 0xe) * 2 + 4) = indice_unidade;
        *(undefined2 *)((int)puVar5 + (uint)*(ushort *)((int)puVar5 + 0xe) * 8 + 0x12) = 0;
        uVar8 = (uint)*(ushort *)((int)puVar5 + 0xe);
      }
      else {
        iVar7 = *(ushort *)((int)puVar5 + 0xe) - 1;
        puVar4 = puVar5 + iVar7 * 2;
        for (; (int)uVar8 <= iVar7; iVar7 = iVar7 + -1) {
          puVar4[6] = puVar4[4];
          puVar4[7] = puVar4[5];
          puVar4 = puVar4 + -2;
        }
        *(undefined2 *)((int)puVar5 + uVar8 * 8 + 0x12) = 0;
        *(ushort *)(puVar5 + uVar8 * 2 + 5) = (ushort)bVar2;
        *(ushort *)(puVar5 + uVar8 * 2 + 4) = indice_unidade;
      }
      *(short *)((int)puVar5 + 0xe) = *(short *)((int)puVar5 + 0xe) + 1;
      FUN_00487eef(puVar5,uVar8);
      bVar2 = 1;
    }
    else {
LAB_00487bef:
      bVar2 = 0;
    }
  }
  return bVar2;
}
