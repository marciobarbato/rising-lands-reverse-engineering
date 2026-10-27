/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0047248f, entrada 0047248f.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

/* WARNING: Removing unreachable block (ram,0x00472534) */

uint __fastcall FUN_0047248f(undefined4 param_1,undefined4 param_2)

{
  uint in_EAX;
  uint uVar1;
  int iVar2;
  int extraout_ECX;
  byte bVar3;
  uint uVar4;
  ushort uVar5;
  bool bVar6;
  longlong lVar7;

  uVar4 = CONCAT22((short)((uint)param_2 >> 0x10),(ushort)(byte)param_2);
  uVar5 = 0;
  uVar1 = in_EAX;
  do {
    iVar2 = (in_EAX & 0xff) * 0x200;
    if (*(ushort *)(&DAT_00508728 + iVar2) <= uVar5) {
      return CONCAT31((int3)(uVar1 >> 8),(char)(uVar4 >> 8));
    }
    lVar7 = FUN_00443dad((uint)*(ushort *)(&DAT_0050872a + (uint)uVar5 * 2 + iVar2),uVar4);
    if ((char)lVar7 != '\0') {
      bVar3 = (byte)((ulonglong)lVar7 >> 0x20);
      if (bVar3 == 0) {
        bVar6 = tabela_unidades[extraout_ECX].tipo_id == 6;
LAB_004724cf:
        if (!bVar6) {
LAB_004724b6:
          return (uint)tabela_unidades & 0xffffff00;
        }
      }
      else {
        if (1 < bVar3) {
          if (bVar3 != 2) goto LAB_004724d3;
          bVar6 = tabela_unidades[extraout_ECX].tipo_id == 7;
          goto LAB_004724cf;
        }
        if ((tabela_unidades[extraout_ECX].tipo_id != 0xd) &&
           (tabela_unidades[extraout_ECX].tipo_id != 5)) goto LAB_004724b6;
      }
      lVar7 = CONCAT44(CONCAT22((short)((ulonglong)lVar7 >> 0x30),CONCAT11(1,bVar3)),tabela_unidades
                      );
    }
LAB_004724d3:
    uVar4 = (uint)((ulonglong)lVar7 >> 0x20);
    uVar1 = (uint)lVar7;
    uVar5 = uVar5 + 1;
  } while( true );
}
