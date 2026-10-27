/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_0041b327, entrada 0041b327.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_0041b327(undefined4 param_1)

{
  byte bVar1;
  ushort in_AX;
  ushort uVar2;
  int iVar3;
  int iVar4;
  ushort extraout_CX;
  undefined4 extraout_ECX;
  ushort in_DX;
  undefined2 extraout_var;
  undefined2 auStack_2c [2];
  undefined4 local_28;
  undefined4 local_24;
  int local_20;
  int local_18;
  ushort local_14 [2];

  iVar3 = (uint)in_AX * 0x114;
  local_24 = 0;
  local_28 = 0;
  unidade_obter_tipo(in_DX);
  FUN_004410d2((undefined2 *)&local_28,local_14);
  local_14[0] = local_14[0] >> 1;
  uVar2 = unidade_obter_vida(in_DX);
  FUN_00457122((int)((uint)local_14[0] * (uint)uVar2) / 100,1);
  uVar2 = unidade_obter_vida(in_DX);
  if (extraout_CX < (ushort)((int)(CONCAT22(extraout_var,uVar2) * (uint)local_14[0]) / 100)) {
    unidade_obter_vida(in_DX);
    iVar4 = FUN_004676e5(0,0,(&DAT_0049a0cc)[iVar3]);
    if ((char)iVar4 == '\0') {
      (&DAT_004dfb58)[(byte)(&DAT_0049a0cc)[iVar3]] = 1;
    }
    else {
      bVar1 = (&DAT_0049a0cc)[iVar3];
      FUN_0046792c(extraout_ECX,1);
      iVar3 = (uint)bVar1 * 6;
      if (*(short *)(&DAT_004dfb2c + iVar3) != 0) {
        FUN_0046769d(auStack_2c,(short *)&local_18,bVar1);
        (&DAT_004dfb30)[iVar3] =
             (char)((((local_20 + local_18 & 0xffffU) / (uint)*(ushort *)(&DAT_004dfb2c + iVar3)) *
                    7) / (uint)*(ushort *)(&DAT_004dfb2e + iVar3));
      }
    }
  }
  return;
}
