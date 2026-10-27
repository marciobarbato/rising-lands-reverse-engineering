/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004472ea, entrada 004472ea.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_004472ea(undefined4 param_1,char param_2)

{
  char cVar1;
  bool bVar2;
  ushort *in_EAX;
  uint uVar3;
  ushort unaff_BX;
  ushort uVar4;
  uint uVar5;
  ushort local_1c;

  uVar5 = 0xffff;
  bVar2 = false;
  uVar4 = 0;
  do {
    if ((*in_EAX <= uVar4) || ((uVar5 & 0xffff) != 0xffff)) {
      if (bVar2) {
        while (uVar3 = (uint)local_1c, (int)uVar3 < (int)(*in_EAX - 1)) {
          *(undefined1 *)((int)in_EAX + uVar3 + 0x42) = *(undefined1 *)((int)in_EAX + uVar3 + 0x43);
          local_1c = local_1c + 1;
          in_EAX[uVar3 + 3] = in_EAX[uVar3 + 4];
        }
        *(undefined1 *)((int)in_EAX + uVar3 + 0x42) = 0;
        in_EAX[uVar3 + 3] = 0;
        *in_EAX = *in_EAX - 1;
      }
      return uVar5;
    }
    uVar3 = (uint)uVar4;
    cVar1 = *(char *)(uVar3 + 0x42 + (int)in_EAX);
    if (cVar1 == param_2) {
      if (cVar1 == '\x01') {
        if (tabela_unidades[in_EAX[uVar3 + 3]].tipo_id == unaff_BX) {
          uVar5 = CONCAT22((short)(uVar5 >> 0x10),in_EAX[0x33]) - 1;
          in_EAX[0x33] = (ushort)uVar5;
          goto LAB_0044733b;
        }
      }
      else if (in_EAX[uVar3 + 3] == unaff_BX) {
        in_EAX[0x33] = in_EAX[0x33] - 1;
LAB_0044733b:
        bVar2 = true;
        uVar5 = CONCAT22((short)(uVar5 >> 0x10),in_EAX[uVar3 + 3]);
        local_1c = uVar4;
      }
    }
    uVar4 = uVar4 + 1;
  } while( true );
}
