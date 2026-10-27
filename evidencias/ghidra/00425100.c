/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00425100, entrada 00425100.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void __fastcall FUN_00425100(undefined4 param_1,char param_2,undefined4 param_3,undefined2 param_4)

{
  undefined1 in_AL;
  char cVar1;
  int iVar2;
  int iVar3;
  short unaff_SI;
  short unaff_DI;
  undefined4 uVar4;

  if (param_2 == '\v') {
    switch(in_AL) {
    case 1:
      unaff_DI = -0xb;
      unaff_SI = 3;
      break;
    case 2:
      unaff_DI = -10;
      goto LAB_0042515d;
    case 3:
      unaff_DI = -9;
      goto LAB_00425169;
    case 4:
      unaff_DI = -7;
      unaff_SI = -0xb;
      break;
    case 5:
      unaff_DI = -2;
      unaff_SI = -0x11;
      break;
    case 6:
      unaff_DI = 2;
      unaff_SI = -0x14;
      break;
    case 7:
      unaff_DI = 9;
      goto LAB_00425199;
    case 8:
      unaff_DI = 0x11;
      goto LAB_004251a5;
    case 9:
      unaff_DI = 0x18;
LAB_004251a5:
      unaff_SI = -0x1a;
      break;
    case 10:
      unaff_DI = 0x20;
      unaff_SI = -0x19;
      break;
    case 0xb:
      unaff_DI = 0x26;
LAB_00425199:
      unaff_SI = -0x17;
      break;
    case 0xc:
      unaff_DI = 0x2d;
      unaff_SI = -0x15;
      break;
    case 0xd:
      unaff_DI = 0x32;
      unaff_SI = -0x10;
      break;
    case 0xe:
      unaff_DI = 0x35;
      unaff_SI = -0xd;
      break;
    case 0xf:
      unaff_DI = 0x3a;
LAB_00425169:
      unaff_SI = -7;
      break;
    case 0x10:
      unaff_DI = 0x3a;
LAB_0042515d:
      unaff_SI = -2;
      break;
    case 0x11:
      unaff_DI = 0x3b;
      unaff_SI = 4;
      break;
    case 0x12:
      unaff_DI = 0x3b;
      unaff_SI = 7;
      break;
    case 0x13:
      unaff_DI = 0x3a;
      unaff_SI = 0xc;
      break;
    case 0x14:
      unaff_DI = 0x36;
      goto LAB_0042523f;
    case 0x15:
      unaff_DI = 0x31;
      unaff_SI = 0x16;
      break;
    case 0x16:
      unaff_DI = 0x2c;
      unaff_SI = 0x1a;
      break;
    case 0x17:
      unaff_DI = 0x26;
      goto LAB_0042526c;
    case 0x18:
      unaff_DI = 0x1f;
LAB_0042526c:
      unaff_SI = 0x1b;
      break;
    case 0x19:
      unaff_DI = 0x19;
      goto LAB_00425282;
    case 0x1a:
      unaff_DI = 0x12;
LAB_00425282:
      unaff_SI = 0x1c;
      break;
    case 0x1b:
      unaff_DI = 10;
      unaff_SI = 0x19;
      break;
    case 0x1c:
      unaff_DI = 5;
      unaff_SI = 0x17;
      break;
    case 0x1d:
      unaff_SI = 0x13;
      unaff_DI = 0;
      break;
    case 0x1e:
      unaff_DI = -5;
LAB_0042523f:
      unaff_SI = 0x10;
      break;
    case 0x1f:
      unaff_DI = -8;
      unaff_SI = 0xb;
      break;
    case 0x20:
      unaff_DI = -10;
      unaff_SI = 8;
    }
    uVar4 = 0;
    iVar2 = (int)unaff_SI;
    iVar3 = (int)unaff_DI;
    goto LAB_0042550c;
  }
  if (param_2 != '\n') {
    return;
  }
  switch(in_AL) {
  case 1:
    unaff_DI = -9;
    unaff_SI = -0xf;
    break;
  case 2:
    unaff_DI = -9;
    goto LAB_00425358;
  case 3:
    unaff_DI = -7;
    goto LAB_00425364;
  case 4:
    unaff_DI = -3;
    unaff_SI = -0x23;
    break;
  case 5:
    unaff_DI = 1;
    goto LAB_0042537c;
  case 6:
    unaff_DI = 7;
    unaff_SI = -0x29;
    break;
  case 7:
    unaff_DI = 0xd;
    goto LAB_00425397;
  case 8:
    unaff_DI = 0x11;
    goto LAB_00425397;
  case 9:
    unaff_DI = 0x17;
    goto LAB_00425397;
  case 10:
    unaff_DI = 0x1e;
LAB_00425397:
    unaff_SI = -0x2b;
    break;
  case 0xb:
    unaff_DI = 0x24;
    unaff_SI = -0x2a;
    break;
  case 0xc:
    unaff_DI = 0x2b;
    unaff_SI = -0x28;
    break;
  case 0xd:
    unaff_DI = 0x2e;
LAB_0042537c:
    unaff_SI = -0x25;
    break;
  case 0xe:
    unaff_DI = 0x34;
    unaff_SI = -0x21;
    break;
  case 0xf:
    unaff_DI = 0x36;
LAB_00425364:
    unaff_SI = -0x1d;
    break;
  case 0x10:
    unaff_DI = 0x38;
LAB_00425358:
    unaff_SI = -0x18;
    break;
  case 0x11:
    unaff_DI = 0x38;
    unaff_SI = -0x13;
    break;
  case 0x12:
    unaff_DI = 0x38;
    unaff_SI = -0xc;
    break;
  case 0x13:
    unaff_DI = 0x37;
    unaff_SI = -8;
    break;
  case 0x14:
    unaff_DI = 0x33;
    unaff_SI = -4;
    break;
  case 0x15:
    unaff_DI = 0x2f;
    goto LAB_0042543f;
  case 0x16:
    unaff_DI = 0x29;
    unaff_SI = 3;
    break;
  case 0x17:
    unaff_DI = 0x23;
    goto LAB_0042545a;
  case 0x18:
    unaff_DI = 0x1e;
    goto LAB_00425469;
  case 0x19:
    unaff_DI = 0x19;
    goto LAB_00425469;
  case 0x1a:
    unaff_DI = 0x12;
LAB_00425469:
    unaff_SI = 6;
    break;
  case 0x1b:
    unaff_DI = 0xd;
LAB_0042545a:
    unaff_SI = 5;
    break;
  case 0x1c:
    unaff_DI = 7;
    unaff_SI = 2;
    break;
  case 0x1d:
    unaff_DI = 2;
LAB_0042543f:
    unaff_SI = 0;
    break;
  case 0x1e:
    unaff_DI = -2;
    unaff_SI = -3;
    break;
  case 0x1f:
    unaff_DI = -5;
    unaff_SI = -7;
    break;
  case 0x20:
    unaff_DI = -9;
    unaff_SI = -0xd;
  }
  unidade_obter_tipo((ushort)param_3);
  cVar1 = FUN_004422cf();
  if (cVar1 == '\0') {
    uVar4 = 0;
    iVar2 = (int)unaff_SI;
    iVar3 = (int)unaff_DI;
  }
  else {
    uVar4 = 1;
    iVar2 = (int)unaff_SI;
    iVar3 = (int)unaff_DI;
  }
LAB_0042550c:
  FUN_0046e44c(param_4,0,iVar3,iVar2,uVar4);
  return;
}
