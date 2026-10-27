/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004517a2, entrada 004517a2.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall FUN_004517a2(uint param_1,undefined1 param_2)

{
  uint3 uVar1;
  byte bVar4;
  uint in_EAX;
  int iVar2;
  uint uVar3;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  uint extraout_ECX_01;
  short sVar5;
  uint unaff_EBX;
  longlong lVar6;

  uVar1 = CONCAT21((short)(in_EAX >> 0x10),param_2);
  bVar4 = tabela_unidades[in_EAX & 0xffff].tipo_id;
  if (bVar4 < 8) {
    if (bVar4 != 4) goto LAB_004517e3;
  }
  else if ((8 < bVar4) && ((bVar4 < 0xc || ((0xc < bVar4 && ((bVar4 < 0x16 || (0x17 < bVar4))))))))
  {
LAB_004517e3:
    iVar2 = (uint)uVar1 << 8;
    goto LAB_004517e5;
  }
  iVar2 = CONCAT31(uVar1,1);
LAB_004517e5:
  if ((char)iVar2 == '\0') {
    bVar4 = (byte)((uint)iVar2 >> 8);
    if (bVar4 < 3) {
      if (bVar4 == 1) {
        param_1 = CONCAT22((short)(param_1 >> 0x10),tabela_unidades[unaff_EBX & 0xffff].celula_passo
                          );
      }
    }
    else if (bVar4 < 4) {
      param_1 = FUN_0041aee2();
    }
    else if (bVar4 == 5) {
      param_1 = unaff_EBX;
    }
    do {
      iVar2 = FUN_00477042(param_1,(ushort)param_1);
      uVar3 = FUN_004770ee(extraout_ECX,(byte)iVar2);
      lVar6 = FUN_0047653c(extraout_ECX_00,uVar3);
      iVar2 = (int)lVar6;
      sVar5 = (short)((ulonglong)lVar6 >> 0x20);
      if ((char)lVar6 != '\0') break;
      param_1 = extraout_ECX_01;
    } while (sVar5 != (short)extraout_ECX_01);
    if (sVar5 != (short)extraout_ECX_01) {
      return (uint)(uint3)((ulonglong)lVar6 >> 8) << 8;
    }
  }
  return CONCAT31((int3)((uint)iVar2 >> 8),1);
}
