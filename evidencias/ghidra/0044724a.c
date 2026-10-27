/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0044724a, entrada 0044724a.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

ulonglong __fastcall FUN_0044724a(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  uint in_EAX;
  uint uVar2;
  ushort uVar3;
  ushort uVar4;

  uVar4 = 0;
  uVar2 = in_EAX;
  do {
    if (*(ushort *)(in_EAX + 2) <= uVar4) {
      return CONCAT44(param_2,uVar2) & 0xffffffffffffff00;
    }
    uVar2 = (uint)*(byte *)(uVar4 + 0x42 + in_EAX);
    if (uVar2 == 1) {
      uVar2 = (uint)*(ushort *)(in_EAX + 6 + (uint)uVar4 * 2);
      bVar1 = tabela_unidades[uVar2].tipo_id;
      uVar3 = (ushort)(uVar2 * 0x114 >> 0x10);
      uVar2 = CONCAT22(uVar3,CONCAT11(1,bVar1));
      if (bVar1 < 0xe) {
        if (bVar1 < 6) {
          if ((bVar1 < 3) || (3 < bVar1)) goto LAB_004472c1;
        }
        else if ((bVar1 < 9) || (bVar1 < 0xb)) {
LAB_004472c1:
          uVar2 = CONCAT22(uVar3,CONCAT11(1,bVar1));
          goto LAB_004472c3;
        }
LAB_004472b7:
        uVar2 = (uint)uVar3 << 0x10;
      }
      else {
        if ((bVar1 < 0xf) || (bVar1 < 0x12)) goto LAB_004472b7;
        if ((bVar1 < 0x13) || ((bVar1 < 0x17 || (bVar1 < 0x19)))) goto LAB_004472c1;
        if (bVar1 == 0x19) goto LAB_004472b7;
      }
LAB_004472c3:
      if ((char)(uVar2 >> 8) != '\0') {
        return CONCAT44(param_2,CONCAT31((int3)(uVar2 >> 8),1));
      }
    }
    uVar4 = uVar4 + 1;
  } while( true );
}
