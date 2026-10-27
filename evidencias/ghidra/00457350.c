/* Pseudocódigo Ghidra, não é fonte original.
 * Função FUN_00457350, entrada 00457350.
 * Tipos/argumentos automáticos podem estar incorretos: convenção Watcom por registradores.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void FUN_00457350(void)

{
  uint in_EAX;
  uint uVar1;
  UnidadeParcial *pUVar2;
  int extraout_ECX;

  pUVar2 = tabela_unidades + (in_EAX & 0xffff);
  pUVar2->grupo_id = 0xff;
  pUVar2->field_0xdb = 8;
  pUVar2->field_0xda = 1;
  pUVar2->field_0xf9 = 0;
  pUVar2->contador_recarga = (ushort)(byte)(&DAT_004965de)[(uint)pUVar2->tipo_id * 0x32];
  switch(tabela_unidades[in_EAX & 0xffff].tipo_id) {
  case 0:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 2;
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 2;
    pUVar2->field_0xa5 = 8;
    pUVar2->field_0xa6 = 10;
    pUVar2->field_0xdb = 8;
    pUVar2->field_0x9d = 0xff;
    pUVar2->field_0xac = 3;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 0;
    break;
  case 1:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 2;
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 4;
    pUVar2->field_0xa5 = 8;
    pUVar2->field_0xa6 = 4;
    pUVar2->field_0xdb = 8;
    pUVar2->field_0x9d = 0xff;
    pUVar2->field_0xac = 3;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 0;
    pUVar2->field_0x78 = 1;
    pUVar2->field_0x79 = 0x19;
    goto LAB_0045746e;
  case 2:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 3;
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 3;
    pUVar2->field_0xa5 = 8;
    pUVar2->field_0xa6 = 10;
    pUVar2->field_0xdb = 10;
    pUVar2->field_0x9d = 0xff;
    pUVar2->field_0xac = 3;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 0;
    pUVar2->field_0x78 = 1;
    pUVar2->field_0x79 = 1;
    pUVar2->field_0x7a = 7;
    return;
  case 3:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 4;
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 4;
    pUVar2->field_0xa5 = 8;
    pUVar2->field_0xa6 = 8;
    pUVar2->field_0xdb = 8;
    pUVar2->field_0x9d = 0xff;
    pUVar2->field_0xac = 3;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 0;
    pUVar2->field_0x78 = 1;
    pUVar2->field_0x79 = 0x1a;
    pUVar2->field_0x7a = 4;
    return;
  case 4:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 1;
    pUVar2->field_0xa7 = 3;
    pUVar2->field_0xa8 = 2;
    pUVar2->field_0xa5 = 8;
    pUVar2->field_0xa6 = 10;
    pUVar2->field_0xdb = 10;
    pUVar2->field_0x9d = 0xff;
    pUVar2->field_0xac = 3;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 0;
    uVar1 = FUN_00428cc0((uint)pUVar2,0xc);
    *(undefined1 *)(extraout_ECX + 0x7a) = 5;
    *(char *)(extraout_ECX + 0xda) = (char)uVar1 + '\n';
    return;
  case 5:
  case 7:
  case 9:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 2;
    goto LAB_00457868;
  case 6:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 3;
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 4;
    pUVar2->field_0xa5 = 8;
    pUVar2->field_0xa6 = 8;
    pUVar2->field_0xdb = 8;
    pUVar2->field_0x9d = 0xff;
    pUVar2->field_0xac = 3;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 0;
    pUVar2->raio_visao = 5;
    return;
  case 8:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 2;
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 2;
    pUVar2->field_0xa5 = 10;
    pUVar2->field_0xa6 = 10;
    pUVar2->field_0xdb = 8;
    pUVar2->field_0x9d = 0xff;
    pUVar2->field_0xac = 3;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 0;
    pUVar2->field_0x78 = 1;
    pUVar2->field_0x79 = 9;
    break;
  case 10:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 3;
LAB_00457868:
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 4;
    pUVar2->field_0xa5 = 8;
    pUVar2->field_0xa6 = 8;
    pUVar2->field_0xdb = 8;
    pUVar2->field_0x9d = 0xff;
    pUVar2->field_0xac = 3;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 0;
    return;
  case 0xb:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 8;
    pUVar2->field_0xa7 = 1;
    pUVar2->field_0xa8 = 1;
    pUVar2->field_0xa5 = 3;
    pUVar2->field_0xa6 = 3;
    pUVar2->field_0x9d = 100;
    pUVar2->field_0xac = 2;
    pUVar2->field_0xad = 10;
    pUVar2->field_0x99 = 3;
    pUVar2->field_0x78 = 1;
    pUVar2->field_0x79 = 0x1b;
    goto LAB_0045746e;
  case 0xc:
    pUVar2->field_0x93 = 2;
    pUVar2->field_0x98 = 3;
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 4;
    pUVar2->field_0xa5 = 3;
    pUVar2->field_0xa6 = 8;
    pUVar2->field_0x9d = 100;
    pUVar2->field_0xac = 0xf;
    pUVar2->field_0xad = 0x14;
    pUVar2->field_0x99 = 2;
    pUVar2->field_0x78 = 1;
    pUVar2->field_0x79 = 0x16;
    goto LAB_00457418;
  case 0xd:
    pUVar2->field_0x93 = 3;
    pUVar2->field_0x98 = 3;
    pUVar2->field_0xa7 = 3;
    pUVar2->field_0xa8 = 0;
    pUVar2->field_0xa5 = 3;
    pUVar2->field_0xa6 = 8;
    pUVar2->field_0x9d = 100;
    pUVar2->field_0xac = 6;
    pUVar2->field_0xad = 10;
    pUVar2->field_0x99 = 3;
    return;
  case 0xe:
    pUVar2->field_0x93 = 4;
    pUVar2->field_0x98 = 3;
    pUVar2->field_0xa7 = 3;
    pUVar2->field_0xa8 = 4;
    pUVar2->field_0xa5 = 3;
    pUVar2->field_0xa6 = 2;
    pUVar2->field_0x9d = 100;
    pUVar2->field_0xac = 0;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 2;
    return;
  case 0xf:
    pUVar2->field_0x93 = 3;
    pUVar2->field_0x98 = 4;
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 2;
    pUVar2->field_0xa5 = 3;
    pUVar2->field_0xa6 = 1;
    pUVar2->field_0x9d = 100;
    pUVar2->field_0xac = 0;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 2;
    pUVar2->field_0x78 = 1;
    pUVar2->field_0x79 = 1;
LAB_00457418:
    pUVar2->field_0x7a = 0;
    return;
  case 0x10:
    pUVar2->field_0x93 = 2;
    pUVar2->field_0x98 = 8;
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 2;
    pUVar2->field_0xa5 = 8;
    pUVar2->field_0xa6 = 8;
    pUVar2->field_0x9d = 0x30;
    pUVar2->field_0xac = 10;
    pUVar2->field_0xad = 8;
    pUVar2->field_0x99 = 0;
    pUVar2->field_0xab = 0x32;
    return;
  case 0x11:
    pUVar2->field_0x93 = 2;
    pUVar2->field_0x98 = 1;
    pUVar2->field_0xa7 = 4;
    pUVar2->field_0xa8 = 4;
    pUVar2->field_0xa5 = 3;
    pUVar2->field_0xa6 = 4;
    pUVar2->field_0x9d = 100;
    pUVar2->field_0xac = 6;
    pUVar2->field_0xad = 10;
    pUVar2->field_0x99 = 0;
    pUVar2->field_0xab = 0x32;
    pUVar2->field_0x94 = 0;
    pUVar2->field_0x95 = 1;
    pUVar2->field_0x96 = 0;
    pUVar2->field_0xa4 = 0;
    return;
  case 0x12:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 2;
    pUVar2->field_0xa7 = 1;
    pUVar2->field_0xa8 = 2;
    pUVar2->field_0xa5 = 10;
    pUVar2->field_0xa6 = 4;
    pUVar2->field_0xdb = 8;
    pUVar2->field_0x9d = 0xff;
    pUVar2->field_0xac = 3;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 0;
    pUVar2->field_0x78 = 1;
    pUVar2->field_0x79 = 0x11;
    pUVar2->field_0x7a = 2;
    return;
  case 0x13:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 2;
    pUVar2->field_0xa7 = 1;
    pUVar2->field_0xa8 = 2;
    pUVar2->field_0xa5 = 0xf;
    pUVar2->field_0xa6 = 0xf;
    pUVar2->field_0xdb = 0xf;
    goto LAB_00457a8b;
  case 0x14:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 4;
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 2;
    goto LAB_00457a76;
  case 0x15:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 8;
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 2;
    pUVar2->field_0xa5 = 8;
    pUVar2->field_0xa6 = 8;
    pUVar2->field_0xdb = 8;
    pUVar2->field_0x9d = 0xff;
    pUVar2->field_0xac = 3;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 0;
    pUVar2->field_0x78 = 1;
    pUVar2->field_0x79 = 0x18;
    break;
  case 0x16:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 4;
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 2;
    pUVar2->field_0xa5 = 8;
    pUVar2->field_0xa6 = 8;
    pUVar2->field_0xdb = 8;
    pUVar2->field_0x9d = 0xff;
    pUVar2->field_0xac = 3;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 0;
    pUVar2->field_0x78 = 1;
    pUVar2->field_0x79 = 0x17;
    break;
  case 0x17:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 2;
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 2;
    pUVar2->field_0xa5 = 8;
    pUVar2->field_0xa6 = 8;
    pUVar2->field_0xdb = 8;
    pUVar2->field_0x9d = 0xff;
    pUVar2->field_0xac = 3;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 0;
    pUVar2->field_0x78 = 1;
    pUVar2->field_0x79 = 0x17;
    pUVar2->field_0x7a = 5;
    return;
  case 0x18:
    pUVar2->field_0x93 = 3;
    pUVar2->field_0x98 = 1;
    pUVar2->field_0xa7 = 3;
    pUVar2->field_0xa8 = 3;
LAB_00457a76:
    pUVar2->field_0xa5 = 8;
    pUVar2->field_0xa6 = 8;
    pUVar2->field_0xdb = 8;
LAB_00457a8b:
    pUVar2->field_0x9d = 0xff;
    pUVar2->field_0xac = 3;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 0;
    pUVar2->field_0x78 = 0;
    return;
  case 0x19:
    pUVar2->field_0x93 = 1;
    pUVar2->field_0x98 = 4;
    pUVar2->field_0xa7 = 2;
    pUVar2->field_0xa8 = 4;
    pUVar2->field_0xa5 = 8;
    pUVar2->field_0xa6 = 8;
    pUVar2->field_0xdb = 8;
    pUVar2->field_0x9d = 0xff;
    pUVar2->field_0xac = 3;
    pUVar2->field_0xad = 3;
    pUVar2->field_0x99 = 0;
    pUVar2->field_0x78 = 1;
    pUVar2->field_0x79 = 0x1a;
LAB_0045746e:
    pUVar2->field_0x7a = 1;
    return;
  default:
    return;
  }
  pUVar2->field_0x7a = 6;
  return;
}
