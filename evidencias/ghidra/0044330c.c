/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044330c, entrada 0044330c.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall FUN_0044330c(undefined4 param_1,uint param_2)

{
  ulonglong uVar1;
  ulonglong uVar2;
  uint in_EAX;
  uint uVar3;
  uint uVar4;
  ushort uVar5;
  int iVar6;
  uint local_20;
  uint local_18;

  uVar2 = ((ulonglong)in_EAX & 0xffffffff0000ffff) % 0x100;
  local_20 = (uint)uVar2;
  uVar1 = ((ulonglong)in_EAX & 0xffffffff0000ffff) / 0x100;
  local_18 = (uint)uVar1;
  switch(tabela_unidades[param_2 & 0xffff].tipo_id) {
  case 0:
  case 1:
  case 2:
  case 4:
  case 5:
  case 6:
  case 7:
  case 8:
  case 9:
  case 10:
  case 0x11:
  case 0x12:
  case 0x13:
  case 0x14:
  case 0x15:
  case 0x16:
  case 0x17:
  case 0x18:
    break;
  case 3:
  case 0xb:
  case 0xc:
  case 0xd:
  case 0xe:
  case 0xf:
  case 0x10:
  case 0x19:
  }
  if (uVar2 != 0) {
    local_20 = local_20 - 1;
  }
  if (uVar1 != 0) {
    local_18 = local_18 - 1;
  }
  uVar5 = 0;
  do {
    uVar3 = (uint)uVar5;
    if (8 < uVar5) {
      return 0xffff;
    }
    if (uVar3 != 4) {
      uVar4 = (local_18 & 0xffff) + uVar3 / 3;
      uVar3 = (local_20 & 0xffff) + uVar3 % 3;
      iVar6 = uVar4 * 0x100 + uVar3;
      if (((uVar3 < DAT_00497168) && (uVar4 < DAT_0049716a)) &&
         (uVar3 = FUN_00442668(0,(ushort)iVar6), (char)uVar3 != '\0')) {
        return iVar6;
      }
    }
    uVar5 = uVar5 + 1;
  } while( true );
}
