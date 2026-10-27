/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0041b1c6, entrada 0041b1c6.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0041b1c6(undefined4 param_1)

{
  byte bVar1;
  uint in_EAX;
  int iVar2;
  ushort uVar3;
  int extraout_ECX;
  int iVar4;
  undefined2 local_30 [4];
  undefined4 local_28;
  uint local_24 [3];
  int local_18;

  iVar4 = (in_EAX & 0xffff) * 0x114;
  local_24[1] = 0;
  local_28 = 0;
  unidade_obter_tipo(*(ushort *)(&DAT_0049a150 + iVar4));
  FUN_004410d2((undefined2 *)&local_28,(undefined2 *)local_24);
  uVar3 = (ushort)local_24[0] >> 1;
  local_24[0] = CONCAT22((short)(local_24[0] >> 0x10),uVar3);
  if (*(ushort *)(&DAT_004dfb5c + (uint)(byte)(&DAT_0049a0cc)[iVar4] * 2) <
      (ushort)(((uint)uVar3 * *(int *)(&DAT_0049a154 + iVar4)) / 10000)) {
    iVar2 = FUN_004676e5(0,0,(&DAT_0049a0cc)[iVar4]);
    if ((char)iVar2 == '\0') {
      (&DAT_004dfb54)[(byte)(&DAT_0049a0cc)[iVar4]] = 1;
    }
    else if ((short)local_24[0] != 0) {
      bVar1 = (&DAT_0049a0cc)[iVar4];
      FUN_0046792c((uint)bVar1,1);
      iVar2 = ((uint)bVar1 * 4 - extraout_ECX) * 2;
      if (*(short *)(&DAT_004dfb2c + iVar2) != 0) {
        FUN_0046769d(local_30,(short *)&local_18,(byte)extraout_ECX);
        (&DAT_004dfb30)[iVar2] =
             (char)((((local_24[2] + local_18 & 0xffff) / (uint)*(ushort *)(&DAT_004dfb2c + iVar2))
                    * 7) / (uint)*(ushort *)(&DAT_004dfb2e + iVar2));
      }
      *(short *)(&DAT_004dfb5c + (uint)(byte)(&DAT_0049a0cc)[iVar4] * 2) =
           (short)(((local_24[0] & 0xffff) * *(int *)(&DAT_0049a154 + iVar4)) / 10000);
      FUN_0041b31f();
      return;
    }
  }
  FUN_0041db1e();
  return;
}
