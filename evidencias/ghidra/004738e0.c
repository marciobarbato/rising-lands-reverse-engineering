/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004738e0, entrada 004738e0.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

undefined8 __fastcall FUN_004738e0(undefined4 param_1,undefined4 param_2)

{
  uint in_EAX;
  uint uVar1;
  uint uVar2;
  int extraout_ECX;
  undefined4 extraout_ECX_00;
  int extraout_ECX_01;
  int iVar3;
  char *pcVar4;
  longlong lVar5;
  undefined8 uVar6;

  uVar2 = 0;
  uVar1 = in_EAX;
  do {
    iVar3 = (in_EAX & 0xff) * 0x200;
    if (*(ushort *)(&DAT_00508728 + iVar3) <= (ushort)uVar2) {
      uVar1 = uVar1 & 0xffffff00;
LAB_00473991:
      return CONCAT44(param_2,uVar1);
    }
    lVar5 = FUN_00443dad(uVar2,(uint)(tabela_unidades +
                                     *(ushort *)(&DAT_0050872a + (uVar2 & 0xffff) * 2 + iVar3)));
    pcVar4 = (char *)((ulonglong)lVar5 >> 0x20);
    uVar1 = (uint)lVar5;
    iVar3 = extraout_ECX;
    if ((((char)lVar5 != '\0') &&
        (uVar1 = CONCAT31((int3)((ulonglong)lVar5 >> 8),*pcVar4), *pcVar4 == (char)in_EAX)) &&
       (uVar1 = (uint)(byte)pcVar4[1], uVar1 == 0xe)) {
      uVar1 = (uint)*(ushort *)(pcVar4 + 0xd8);
      if (uVar1 != 10) {
        uVar6 = FUN_00440e11(extraout_ECX,pcVar4);
        uVar6 = FUN_0044828b(extraout_ECX_00,
                             (uint)*(ushort *)((int)((ulonglong)uVar6 >> 0x20) + 0xd8) +
                             (uint)(((uint)uVar6 & 0xff) == 0x16));
        uVar1 = (uint)uVar6 & 0xff;
        iVar3 = extraout_ECX_01;
        if ((int)((ulonglong)uVar6 >> 0x20) < (int)uVar1) goto LAB_004738ee;
      }
      uVar1 = CONCAT31((int3)(uVar1 >> 8),1);
      goto LAB_00473991;
    }
LAB_004738ee:
    uVar2 = iVar3 + 1;
  } while( true );
}
