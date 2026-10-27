/* Pseudocódigo automático: argumentos Watcom podem estar incorretos.
 * SHA-256: 26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0
 */

void OriginaisSBL::MurRetire(void)

{
  uint in_EAX;
  int iVar1;
  byte *pbVar2;
  byte bVar3;
  int iVar4;
  uint uVar5;
  byte bVar7;
  uint uVar6;
  byte local_1c [4];

  if (*(char *)(DAT_004e156c + (in_EAX & 0xffff)) != '\0') {
    for (uVar6 = 0x100; (uVar6 & 0xff) < 4; uVar6 = (uint)CONCAT11(bVar7 + 4,(char)uVar6 + '\x01'))
    {
      bVar7 = (byte)(uVar6 >> 8);
      iVar4 = (in_EAX & 0xff) + *(int *)(&DAT_00496308 + (uint)bVar7 * 8);
      iVar1 = ((int)(in_EAX & 0xffff) >> 8) + *(int *)(&DAT_0049630c + (uint)bVar7 * 8);
      if (((iVar4 < 0) || ((int)(DAT_00497168 - 1) < iVar4)) ||
         ((iVar1 < 0 || ((int)(DAT_0049716a - 1) < iVar1)))) {
        uVar5 = 0xffff;
      }
      else {
        uVar5 = iVar4 + iVar1 * 0x100;
      }
      if ((uVar5 & 0xffff) == 0xffff) {
        bVar3 = 0;
      }
      else {
        bVar3 = *(byte *)(DAT_004e156c + (uVar5 & 0xffff));
      }
      local_1c[uVar6 & 0xff] = bVar3;
    }
    *(undefined1 *)(DAT_004e156c + (in_EAX & 0xffff)) = 0;
    for (uVar6 = 0x100; (uVar6 & 0xff) < 4; uVar6 = (uint)CONCAT11(bVar7 + 4,(char)uVar6 + '\x01'))
    {
      bVar7 = (byte)(uVar6 >> 8);
      iVar1 = (in_EAX & 0xff) + *(int *)(&DAT_00496308 + (uint)bVar7 * 8);
      iVar4 = ((int)(in_EAX & 0xffff) >> 8) + *(int *)(&DAT_0049630c + (uint)bVar7 * 8);
      if ((((iVar1 < 0) || ((int)(DAT_00497168 - 1) < iVar1)) || (iVar4 < 0)) ||
         ((int)(DAT_0049716a - 1) < iVar4)) {
        uVar5 = 0xffff;
      }
      else {
        uVar5 = iVar1 + iVar4 * 0x100;
      }
      if ((((uVar5 & 0xffff) != 0xffff) &&
          (pbVar2 = (byte *)((uVar5 & 0xffff) + DAT_004e156c), *pbVar2 != 0)) &&
         (*pbVar2 == local_1c[uVar6 & 0xff])) {
        if (DAT_004e1570 == 0) {
          bVar3 = 0;
        }
        else {
          bVar3 = (&DAT_004e1570)[DAT_004e1570];
          (&DAT_004e1670)[bVar3] = 0;
          DAT_004e1570 = DAT_004e1570 - 1;
        }
        Remplit(uVar5,bVar3);
      }
    }
    if (DAT_004e1570 != 0xff) {
      if (((&DAT_004e1670)[local_1c[0]] == '\0') && (local_1c[0] != 0)) {
        DAT_004e1570 = DAT_004e1570 + 1;
        (&DAT_004e1570)[DAT_004e1570] = local_1c[0];
        (&DAT_004e1670)[local_1c[0]] = 1;
      }
    }
    if (DAT_004e1570 != 0xff) {
      if (((&DAT_004e1670)[local_1c[1]] == '\0') && (local_1c[1] != 0)) {
        DAT_004e1570 = DAT_004e1570 + 1;
        (&DAT_004e1570)[DAT_004e1570] = local_1c[1];
        (&DAT_004e1670)[local_1c[1]] = 1;
      }
    }
    if (DAT_004e1570 != 0xff) {
      if (((&DAT_004e1670)[local_1c[2]] == '\0') && (local_1c[2] != 0)) {
        DAT_004e1570 = DAT_004e1570 + 1;
        (&DAT_004e1570)[DAT_004e1570] = local_1c[2];
        (&DAT_004e1670)[local_1c[2]] = 1;
      }
    }
    if (DAT_004e1570 != 0xff) {
      if (((&DAT_004e1670)[local_1c[3]] == '\0') && (local_1c[3] != 0)) {
        DAT_004e1570 = DAT_004e1570 + 1;
        (&DAT_004e1570)[DAT_004e1570] = local_1c[3];
        (&DAT_004e1670)[local_1c[3]] = 1;
      }
    }
  }
  return;
}
