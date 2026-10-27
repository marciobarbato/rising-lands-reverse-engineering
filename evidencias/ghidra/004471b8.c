/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004471b8, entrada 004471b8.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall FUN_004471b8(undefined4 param_1,char param_2)

{
  int in_EAX;
  ushort uVar1;
  ushort unaff_BX;
  int iVar2;
  ushort uVar3;
  uint uVar4;

  iVar2 = 0;
  uVar1 = 0;
  do {
    if (*(ushort *)(in_EAX + 2) <= uVar1) {
      return iVar2;
    }
    uVar4 = (uint)uVar1;
    if (*(char *)(uVar4 + 0x42 + in_EAX) != param_2) goto switchD_00447238_caseD_4;
    switch(param_2) {
    case '\x01':
      uVar3 = (ushort)tabela_unidades[*(ushort *)(in_EAX + 6 + uVar4 * 2)].tipo_id;
      goto LAB_004471f8;
    case '\x02':
      uVar3 = *(ushort *)(in_EAX + 6 + uVar4 * 2);
LAB_004471f8:
      if (unaff_BX == uVar3) {
        iVar2 = iVar2 + 1;
      }
      break;
    case '\x03':
    case '\x06':
    case '\a':
      if (unaff_BX == *(ushort *)(in_EAX + 6 + (uint)uVar1 * 2)) {
        return 1;
      }
    }
switchD_00447238_caseD_4:
    uVar1 = uVar1 + 1;
  } while( true );
}
