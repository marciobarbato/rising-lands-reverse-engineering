/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00477042, entrada 00477042.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

int __fastcall FUN_00477042(undefined4 param_1,ushort param_2)

{
  char cVar1;
  uint in_EAX;
  undefined3 uVar2;
  short sVar3;
  int iVar4;
  short sVar5;

  sVar5 = (short)((ulonglong)(longlong)(int)(uint)param_2 % 0x100) -
          (short)(((ulonglong)in_EAX & 0xffffffff0000ffff) % 0x100);
  iVar4 = (int)((ulonglong)(longlong)(int)(uint)param_2 / 0x100) -
          (int)(((ulonglong)in_EAX & 0xffffffff0000ffff) / 0x100);
  sVar3 = (short)iVar4;
  cVar1 = (char)((uint)iVar4 >> 8);
  if (0 < sVar5) {
    if (sVar3 < 0) {
      return CONCAT31((int3)cVar1,7);
    }
    if (sVar3 == 0) {
      return CONCAT31((int3)cVar1,9);
    }
    return CONCAT31((int3)cVar1,0xb);
  }
  if (-1 < sVar5) {
    if (sVar3 < 0) {
      return CONCAT31((int3)cVar1,5);
    }
    if (sVar3 < 1) {
      return (uint)(uint3)(int3)cVar1 << 8;
    }
    return CONCAT31((int3)cVar1,0xd);
  }
  uVar2 = (undefined3)((uint)iVar4 >> 8);
  if (sVar3 < 0) {
    return CONCAT31(uVar2,3);
  }
  if (sVar3 == 0) {
    return CONCAT31(uVar2,1);
  }
  return CONCAT31(uVar2,0xf);
}
