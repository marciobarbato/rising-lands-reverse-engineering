/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_004770ee, entrada 004770ee.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

uint __fastcall FUN_004770ee(undefined4 param_1,byte param_2)

{
  uint in_EAX;

  if (param_2 < 7) {
    if (param_2 < 3) {
      if (param_2 != 1) {
        return in_EAX;
      }
      if ((int)(((ulonglong)in_EAX & 0xffffffff0000ffff) % 0x100) != 0) {
        return in_EAX - 1;
      }
    }
    else if (param_2 < 4) {
      if (((int)(((ulonglong)in_EAX & 0xffffffff0000ffff) % 0x100) != 0) &&
         ((int)(((ulonglong)in_EAX & 0xffffffff0000ffff) / 0x100) != 0)) {
        return in_EAX - 0x101;
      }
    }
    else {
      if (param_2 != 5) {
        return in_EAX;
      }
      if ((int)(in_EAX & 0xffff) >> 8 != 0) {
        return in_EAX - 0x100;
      }
    }
  }
  else if (param_2 < 8) {
    if (((int)(in_EAX & 0xffff) >> 8 != 0) &&
       ((int)(((ulonglong)in_EAX & 0xffffffff0000ffff) % 0x100) != DAT_00497168 - 1)) {
      return in_EAX - 0xff;
    }
  }
  else if (param_2 < 0xb) {
    if (param_2 != 9) {
      return in_EAX;
    }
    if ((int)(((ulonglong)in_EAX & 0xffffffff0000ffff) % 0x100) != DAT_00497168 - 1) {
      return in_EAX + 1;
    }
  }
  else if (param_2 < 0xc) {
    if (((int)(((ulonglong)in_EAX & 0xffffffff0000ffff) % 0x100) != DAT_00497168 - 1) &&
       ((int)(((ulonglong)in_EAX & 0xffffffff0000ffff) / 0x100) != DAT_0049716a - 1)) {
      return in_EAX + 0x101;
    }
  }
  else {
    if (param_2 < 0xd) {
      return in_EAX;
    }
    if (param_2 < 0xe) {
      if ((int)(in_EAX & 0xffff) >> 8 != DAT_0049716a - 1) {
        return CONCAT22((short)(in_EAX >> 0x10),CONCAT11((char)(in_EAX >> 8) + '\x01',(char)in_EAX))
        ;
      }
    }
    else {
      if (param_2 != 0xf) {
        return in_EAX;
      }
      if (((int)(((ulonglong)in_EAX & 0xffffffff0000ffff) % 0x100) != 0) &&
         ((int)(((ulonglong)in_EAX & 0xffffffff0000ffff) / 0x100) != DAT_0049716a - 1)) {
        return in_EAX + 0xff;
      }
    }
  }
  return 0xffff;
}
