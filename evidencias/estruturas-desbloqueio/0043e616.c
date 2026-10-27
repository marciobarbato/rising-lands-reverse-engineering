/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void OriginaisSBL::MurAjoute(void)

{
  byte bVar1;
  uint in_EAX;
  int iVar2;
  uint uVar3;
  uint uVar4;
  int iVar5;
  byte bVar6;
  byte local_24 [4];
  uint local_20;
  byte local_1c;

  for (uVar4 = 0x100; (uVar4 & 0xff) < 4; uVar4 = (uint)CONCAT11(bVar6 + 4,(char)uVar4 + '\x01')) {
    bVar6 = (byte)(uVar4 >> 8);
    iVar2 = (in_EAX & 0xff) + *(int *)(&DAT_00496308 + (uint)bVar6 * 8);
    iVar5 = ((int)(in_EAX & 0xffff) >> 8) + *(int *)(&DAT_0049630c + (uint)bVar6 * 8);
    if (((iVar2 < 0) || ((int)(DAT_00497168 - 1) < iVar2)) ||
       ((iVar5 < 0 || ((int)(DAT_0049716a - 1) < iVar5)))) {
      uVar3 = 0xffff;
    }
    else {
      uVar3 = iVar2 + iVar5 * 0x100;
    }
    if ((uVar3 & 0xffff) == 0xffff) {
      local_24[uVar4 & 0xff] = 0;
    }
    else {
      local_24[uVar4 & 0xff] = *(byte *)(DAT_004e156c + (uVar3 & 0xffff));
    }
  }
  if (DAT_004e1570 == 0) {
    local_1c = 0;
  }
  else {
    local_1c = (&DAT_004e1570)[DAT_004e1570];
    DAT_004e1570 = DAT_004e1570 - 1;
    (&DAT_004e1670)[local_1c] = 0;
  }
  local_20 = CONCAT22((short)(in_EAX >> 0x10),(ushort)(byte)in_EAX);
  for (uVar4 = 0x100; (uVar4 & 0xff) < 4; uVar4 = (uint)CONCAT11(bVar6 + 4,(char)uVar4 + '\x01')) {
    bVar6 = (byte)(uVar4 >> 8);
    iVar2 = (local_20 & 0xffff) + *(int *)(&DAT_00496308 + (uint)bVar6 * 8);
    iVar5 = ((int)(in_EAX & 0xffff) >> 8) + *(int *)(&DAT_0049630c + (uint)bVar6 * 8);
    if ((((iVar2 < 0) || ((int)(DAT_00497168 - 1) < iVar2)) || (iVar5 < 0)) ||
       ((int)(DAT_0049716a - 1) < iVar5)) {
      uVar3 = 0xffff;
    }
    else {
      uVar3 = iVar2 + iVar5 * 0x100;
    }
    if ((uVar3 & 0xffff) != 0xffff) {
      bVar1 = *(byte *)(DAT_004e156c + (uVar3 & 0xffff));
      if ((bVar1 != 0) && (bVar1 == local_24[uVar4 & 0xff])) {
        Remplit((uint)bVar1,local_1c);
      }
    }
  }
  *(byte *)(DAT_004e156c + (in_EAX & 0xffff)) = local_1c;
  if (DAT_004e1570 != 0xff) {
    if (((&DAT_004e1670)[local_24[0]] == '\0') && (local_24[0] != 0)) {
      DAT_004e1570 = DAT_004e1570 + 1;
      uVar4 = (uint)DAT_004e1570;
      (&DAT_004e1670)[local_24[0]] = 1;
      (&DAT_004e1570)[uVar4] = local_24[0];
    }
  }
  if (DAT_004e1570 != 0xff) {
    if (((&DAT_004e1670)[local_24[1]] == '\0') && (local_24[1] != 0)) {
      DAT_004e1570 = DAT_004e1570 + 1;
      uVar4 = (uint)DAT_004e1570;
      (&DAT_004e1670)[local_24[1]] = 1;
      (&DAT_004e1570)[uVar4] = local_24[1];
    }
  }
  if (DAT_004e1570 != 0xff) {
    if (((&DAT_004e1670)[local_24[2]] == '\0') && (local_24[2] != 0)) {
      DAT_004e1570 = DAT_004e1570 + 1;
      (&DAT_004e1570)[DAT_004e1570] = local_24[2];
      (&DAT_004e1670)[local_24[2]] = 1;
    }
  }
  if (DAT_004e1570 != 0xff) {
    if (((&DAT_004e1670)[local_24[3]] == '\0') && (local_24[3] != 0)) {
      DAT_004e1570 = DAT_004e1570 + 1;
      uVar4 = (uint)DAT_004e1570;
      (&DAT_004e1670)[local_24[3]] = 1;
      (&DAT_004e1570)[uVar4] = local_24[3];
    }
  }
  return;
}
