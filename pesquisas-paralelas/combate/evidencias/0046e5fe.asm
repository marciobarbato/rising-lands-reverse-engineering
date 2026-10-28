; ProjectileInfligeDegat; intervalo [0x0046e5fe, 0x0046eaf8)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046e5fe  53                       push     ebx
0046e5ff  51                       push     ecx
0046e600  52                       push     edx
0046e601  56                       push     esi
0046e602  89c6                     mov      esi, eax
0046e604  31c0                     xor      eax, eax
0046e606  31c9                     xor      ecx, ecx
0046e608  31db                     xor      ebx, ebx
0046e60a  31d2                     xor      edx, edx
0046e60c  8a4623                   mov      al, byte ptr [esi + 0x23]
0046e60f  8a4e22                   mov      cl, byte ptr [esi + 0x22]
0046e612  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046e616  50                       push     eax
0046e617  31c0                     xor      eax, eax
0046e619  8a561f                   mov      dl, byte ptr [esi + 0x1f]
0046e61c  668b4616                 mov      ax, word ptr [esi + 0x16]
0046e620  e84f22feff               call     0x450874
0046e625  8a1e                     mov      bl, byte ptr [esi]
0046e627  80fb15                   cmp      bl, 0x15
0046e62a  0f82ab040000             jb       0x46eadb
0046e630  0f86bd040000             jbe      0x46eaf3
0046e636  80fb1a                   cmp      bl, 0x1a
0046e639  0f828e040000             jb       0x46eacd
0046e63f  0f86ae040000             jbe      0x46eaf3
0046e645  80fb1f                   cmp      bl, 0x1f
0046e648  0f83a5040000             jae      0x46eaf3
0046e64e  80fb1d                   cmp      bl, 0x1d
0046e651  0f859c040000             jne      0x46eaf3
0046e657  31d2                     xor      edx, edx
0046e659  668b5616                 mov      dx, word ptr [esi + 0x16]
0046e65d  b900010000               mov      ecx, 0x100
0046e662  89d0                     mov      eax, edx
0046e664  c1fa1f                   sar      edx, 0x1f
0046e667  f7f9                     idiv     ecx
0046e669  85d2                     test     edx, edx
0046e66b  7420                     je       0x46e68d
0046e66d  6a00                     push     0
0046e66f  31c9                     xor      ecx, ecx
0046e671  668b4616                 mov      ax, word ptr [esi + 0x16]
0046e675  88d9                     mov      cl, bl
0046e677  31db                     xor      ebx, ebx
0046e679  48                       dec      eax
0046e67a  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046e67e  ba04000000               mov      edx, 4
0046e683  25ffff0000               and      eax, 0xffff
0046e688  e8e721feff               call     0x450874
0046e68d  31d2                     xor      edx, edx
0046e68f  668b5616                 mov      dx, word ptr [esi + 0x16]
0046e693  bb00010000               mov      ebx, 0x100
0046e698  89d0                     mov      eax, edx
0046e69a  c1fa1f                   sar      edx, 0x1f
0046e69d  f7fb                     idiv     ebx
0046e69f  81faff000000             cmp      edx, 0xff
0046e6a5  7420                     je       0x46e6c7
0046e6a7  6a00                     push     0
0046e6a9  668b4616                 mov      ax, word ptr [esi + 0x16]
0046e6ad  31c9                     xor      ecx, ecx
0046e6af  31db                     xor      ebx, ebx
0046e6b1  40                       inc      eax
0046e6b2  8a0e                     mov      cl, byte ptr [esi]
0046e6b4  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046e6b8  ba04000000               mov      edx, 4
0046e6bd  25ffff0000               and      eax, 0xffff
0046e6c2  e8ad21feff               call     0x450874
0046e6c7  31db                     xor      ebx, ebx
0046e6c9  668b5e16                 mov      bx, word ptr [esi + 0x16]
0046e6cd  89da                     mov      edx, ebx
0046e6cf  89d8                     mov      eax, ebx
0046e6d1  c1fa1f                   sar      edx, 0x1f
0046e6d4  c1e208                   shl      edx, 8
0046e6d7  1bc2                     sbb      eax, edx
0046e6d9  c1f808                   sar      eax, 8
0046e6dc  85c0                     test     eax, eax
0046e6de  7437                     je       0x46e717
0046e6e0  b900010000               mov      ecx, 0x100
0046e6e5  89da                     mov      edx, ebx
0046e6e7  89d8                     mov      eax, ebx
0046e6e9  c1fa1f                   sar      edx, 0x1f
0046e6ec  f7f9                     idiv     ecx
0046e6ee  85d2                     test     edx, edx
0046e6f0  7425                     je       0x46e717
0046e6f2  6a00                     push     0
0046e6f4  668b4616                 mov      ax, word ptr [esi + 0x16]
0046e6f8  31c9                     xor      ecx, ecx
0046e6fa  31db                     xor      ebx, ebx
0046e6fc  81e801010000             sub      eax, 0x101
0046e702  8a0e                     mov      cl, byte ptr [esi]
0046e704  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046e708  ba04000000               mov      edx, 4
0046e70d  25ffff0000               and      eax, 0xffff
0046e712  e85d21feff               call     0x450874
0046e717  31d2                     xor      edx, edx
0046e719  668b5616                 mov      dx, word ptr [esi + 0x16]
0046e71d  89d0                     mov      eax, edx
0046e71f  c1fa1f                   sar      edx, 0x1f
0046e722  c1e208                   shl      edx, 8
0046e725  1bc2                     sbb      eax, edx
0046e727  c1f808                   sar      eax, 8
0046e72a  85c0                     test     eax, eax
0046e72c  7425                     je       0x46e753
0046e72e  6a00                     push     0
0046e730  668b4616                 mov      ax, word ptr [esi + 0x16]
0046e734  31c9                     xor      ecx, ecx
0046e736  31db                     xor      ebx, ebx
0046e738  81e800010000             sub      eax, 0x100
0046e73e  8a0e                     mov      cl, byte ptr [esi]
0046e740  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046e744  ba04000000               mov      edx, 4
0046e749  25ffff0000               and      eax, 0xffff
0046e74e  e82121feff               call     0x450874
0046e753  31db                     xor      ebx, ebx
0046e755  668b5e16                 mov      bx, word ptr [esi + 0x16]
0046e759  89da                     mov      edx, ebx
0046e75b  89d8                     mov      eax, ebx
0046e75d  c1fa1f                   sar      edx, 0x1f
0046e760  c1e208                   shl      edx, 8
0046e763  1bc2                     sbb      eax, edx
0046e765  c1f808                   sar      eax, 8
0046e768  85c0                     test     eax, eax
0046e76a  743b                     je       0x46e7a7
0046e76c  b900010000               mov      ecx, 0x100
0046e771  89da                     mov      edx, ebx
0046e773  89d8                     mov      eax, ebx
0046e775  c1fa1f                   sar      edx, 0x1f
0046e778  f7f9                     idiv     ecx
0046e77a  81faff000000             cmp      edx, 0xff
0046e780  7425                     je       0x46e7a7
0046e782  6a00                     push     0
0046e784  668b4616                 mov      ax, word ptr [esi + 0x16]
0046e788  31c9                     xor      ecx, ecx
0046e78a  31db                     xor      ebx, ebx
0046e78c  81e8ff000000             sub      eax, 0xff
0046e792  8a0e                     mov      cl, byte ptr [esi]
0046e794  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046e798  ba04000000               mov      edx, 4
0046e79d  25ffff0000               and      eax, 0xffff
0046e7a2  e8cd20feff               call     0x450874
0046e7a7  31db                     xor      ebx, ebx
0046e7a9  668b5e16                 mov      bx, word ptr [esi + 0x16]
0046e7ad  89da                     mov      edx, ebx
0046e7af  89d8                     mov      eax, ebx
0046e7b1  c1fa1f                   sar      edx, 0x1f
0046e7b4  c1e208                   shl      edx, 8
0046e7b7  1bc2                     sbb      eax, edx
0046e7b9  c1f808                   sar      eax, 8
0046e7bc  3dff000000               cmp      eax, 0xff
0046e7c1  7436                     je       0x46e7f9
0046e7c3  b900010000               mov      ecx, 0x100
0046e7c8  89da                     mov      edx, ebx
0046e7ca  89d8                     mov      eax, ebx
0046e7cc  c1fa1f                   sar      edx, 0x1f
0046e7cf  f7f9                     idiv     ecx
0046e7d1  85d2                     test     edx, edx
0046e7d3  7424                     je       0x46e7f9
0046e7d5  6a00                     push     0
0046e7d7  668b4616                 mov      ax, word ptr [esi + 0x16]
0046e7db  31c9                     xor      ecx, ecx
0046e7dd  31db                     xor      ebx, ebx
0046e7df  05ff000000               add      eax, 0xff
0046e7e4  8a0e                     mov      cl, byte ptr [esi]
0046e7e6  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046e7ea  ba04000000               mov      edx, 4
0046e7ef  25ffff0000               and      eax, 0xffff
0046e7f4  e87b20feff               call     0x450874
0046e7f9  31d2                     xor      edx, edx
0046e7fb  668b5616                 mov      dx, word ptr [esi + 0x16]
0046e7ff  89d0                     mov      eax, edx
0046e801  c1fa1f                   sar      edx, 0x1f
0046e804  c1e208                   shl      edx, 8
0046e807  1bc2                     sbb      eax, edx
0046e809  c1f808                   sar      eax, 8
0046e80c  3dff000000               cmp      eax, 0xff
0046e811  7421                     je       0x46e834
0046e813  6a00                     push     0
0046e815  668b4616                 mov      ax, word ptr [esi + 0x16]
0046e819  31c9                     xor      ecx, ecx
0046e81b  31db                     xor      ebx, ebx
0046e81d  fec4                     inc      ah
0046e81f  8a0e                     mov      cl, byte ptr [esi]
0046e821  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046e825  ba04000000               mov      edx, 4
0046e82a  25ffff0000               and      eax, 0xffff
0046e82f  e84020feff               call     0x450874
0046e834  31db                     xor      ebx, ebx
0046e836  668b5e16                 mov      bx, word ptr [esi + 0x16]
0046e83a  89da                     mov      edx, ebx
0046e83c  89d8                     mov      eax, ebx
0046e83e  c1fa1f                   sar      edx, 0x1f
0046e841  c1e208                   shl      edx, 8
0046e844  1bc2                     sbb      eax, edx
0046e846  c1f808                   sar      eax, 8
0046e849  3dff000000               cmp      eax, 0xff
0046e84e  0f849f020000             je       0x46eaf3
0046e854  b900010000               mov      ecx, 0x100
0046e859  89da                     mov      edx, ebx
0046e85b  89d8                     mov      eax, ebx
0046e85d  c1fa1f                   sar      edx, 0x1f
0046e860  f7f9                     idiv     ecx
0046e862  81faff000000             cmp      edx, 0xff
0046e868  0f8485020000             je       0x46eaf3
0046e86e  6a00                     push     0
0046e870  668b4616                 mov      ax, word ptr [esi + 0x16]
0046e874  31c9                     xor      ecx, ecx
0046e876  31db                     xor      ebx, ebx
0046e878  0501010000               add      eax, 0x101
0046e87d  8a0e                     mov      cl, byte ptr [esi]
0046e87f  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046e883  ba04000000               mov      edx, 4
0046e888  25ffff0000               and      eax, 0xffff
0046e88d  e8e21ffeff               call     0x450874
0046e892  5e                       pop      esi
0046e893  5a                       pop      edx
0046e894  59                       pop      ecx
0046e895  5b                       pop      ebx
0046e896  c3                       ret
0046e897  31d2                     xor      edx, edx
0046e899  668b5616                 mov      dx, word ptr [esi + 0x16]
0046e89d  bb00010000               mov      ebx, 0x100
0046e8a2  89d0                     mov      eax, edx
0046e8a4  c1fa1f                   sar      edx, 0x1f
0046e8a7  f7fb                     idiv     ebx
0046e8a9  85d2                     test     edx, edx
0046e8ab  7421                     je       0x46e8ce
0046e8ad  6a00                     push     0
0046e8af  668b4616                 mov      ax, word ptr [esi + 0x16]
0046e8b3  31c9                     xor      ecx, ecx
0046e8b5  31db                     xor      ebx, ebx
0046e8b7  31d2                     xor      edx, edx
0046e8b9  48                       dec      eax
0046e8ba  8a4e22                   mov      cl, byte ptr [esi + 0x22]
0046e8bd  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046e8c1  8a561f                   mov      dl, byte ptr [esi + 0x1f]
0046e8c4  25ffff0000               and      eax, 0xffff
0046e8c9  e8a61ffeff               call     0x450874
0046e8ce  31d2                     xor      edx, edx
0046e8d0  668b5616                 mov      dx, word ptr [esi + 0x16]
0046e8d4  bb00010000               mov      ebx, 0x100
0046e8d9  89d0                     mov      eax, edx
0046e8db  c1fa1f                   sar      edx, 0x1f
0046e8de  f7fb                     idiv     ebx
0046e8e0  81faff000000             cmp      edx, 0xff
0046e8e6  7421                     je       0x46e909
0046e8e8  6a00                     push     0
0046e8ea  668b4616                 mov      ax, word ptr [esi + 0x16]
0046e8ee  31c9                     xor      ecx, ecx
0046e8f0  31db                     xor      ebx, ebx
0046e8f2  31d2                     xor      edx, edx
0046e8f4  40                       inc      eax
0046e8f5  8a4e22                   mov      cl, byte ptr [esi + 0x22]
0046e8f8  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046e8fc  8a561f                   mov      dl, byte ptr [esi + 0x1f]
0046e8ff  25ffff0000               and      eax, 0xffff
0046e904  e86b1ffeff               call     0x450874
0046e909  31db                     xor      ebx, ebx
0046e90b  668b5e16                 mov      bx, word ptr [esi + 0x16]
0046e90f  89da                     mov      edx, ebx
0046e911  89d8                     mov      eax, ebx
0046e913  c1fa1f                   sar      edx, 0x1f
0046e916  c1e208                   shl      edx, 8
0046e919  1bc2                     sbb      eax, edx
0046e91b  c1f808                   sar      eax, 8
0046e91e  85c0                     test     eax, eax
0046e920  7438                     je       0x46e95a
0046e922  b900010000               mov      ecx, 0x100
0046e927  89da                     mov      edx, ebx
0046e929  89d8                     mov      eax, ebx
0046e92b  c1fa1f                   sar      edx, 0x1f
0046e92e  f7f9                     idiv     ecx
0046e930  85d2                     test     edx, edx
0046e932  7426                     je       0x46e95a
0046e934  6a00                     push     0
0046e936  668b4616                 mov      ax, word ptr [esi + 0x16]
0046e93a  31c9                     xor      ecx, ecx
0046e93c  31db                     xor      ebx, ebx
0046e93e  31d2                     xor      edx, edx
0046e940  81e801010000             sub      eax, 0x101
0046e946  8a4e22                   mov      cl, byte ptr [esi + 0x22]
0046e949  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046e94d  8a561f                   mov      dl, byte ptr [esi + 0x1f]
0046e950  25ffff0000               and      eax, 0xffff
0046e955  e81a1ffeff               call     0x450874
0046e95a  31d2                     xor      edx, edx
0046e95c  668b5616                 mov      dx, word ptr [esi + 0x16]
0046e960  89d0                     mov      eax, edx
0046e962  c1fa1f                   sar      edx, 0x1f
0046e965  c1e208                   shl      edx, 8
0046e968  1bc2                     sbb      eax, edx
0046e96a  c1f808                   sar      eax, 8
0046e96d  85c0                     test     eax, eax
0046e96f  7426                     je       0x46e997
0046e971  6a00                     push     0
0046e973  668b4616                 mov      ax, word ptr [esi + 0x16]
0046e977  31c9                     xor      ecx, ecx
0046e979  31db                     xor      ebx, ebx
0046e97b  31d2                     xor      edx, edx
0046e97d  81e800010000             sub      eax, 0x100
0046e983  8a4e22                   mov      cl, byte ptr [esi + 0x22]
0046e986  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046e98a  8a561f                   mov      dl, byte ptr [esi + 0x1f]
0046e98d  25ffff0000               and      eax, 0xffff
0046e992  e8dd1efeff               call     0x450874
0046e997  31db                     xor      ebx, ebx
0046e999  668b5e16                 mov      bx, word ptr [esi + 0x16]
0046e99d  89da                     mov      edx, ebx
0046e99f  89d8                     mov      eax, ebx
0046e9a1  c1fa1f                   sar      edx, 0x1f
0046e9a4  c1e208                   shl      edx, 8
0046e9a7  1bc2                     sbb      eax, edx
0046e9a9  c1f808                   sar      eax, 8
0046e9ac  85c0                     test     eax, eax
0046e9ae  743c                     je       0x46e9ec
0046e9b0  b900010000               mov      ecx, 0x100
0046e9b5  89da                     mov      edx, ebx
0046e9b7  89d8                     mov      eax, ebx
0046e9b9  c1fa1f                   sar      edx, 0x1f
0046e9bc  f7f9                     idiv     ecx
0046e9be  81faff000000             cmp      edx, 0xff
0046e9c4  7426                     je       0x46e9ec
0046e9c6  6a00                     push     0
0046e9c8  668b4616                 mov      ax, word ptr [esi + 0x16]
0046e9cc  31c9                     xor      ecx, ecx
0046e9ce  31db                     xor      ebx, ebx
0046e9d0  31d2                     xor      edx, edx
0046e9d2  81e8ff000000             sub      eax, 0xff
0046e9d8  8a4e22                   mov      cl, byte ptr [esi + 0x22]
0046e9db  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046e9df  8a561f                   mov      dl, byte ptr [esi + 0x1f]
0046e9e2  25ffff0000               and      eax, 0xffff
0046e9e7  e8881efeff               call     0x450874
0046e9ec  31db                     xor      ebx, ebx
0046e9ee  668b5e16                 mov      bx, word ptr [esi + 0x16]
0046e9f2  89da                     mov      edx, ebx
0046e9f4  89d8                     mov      eax, ebx
0046e9f6  c1fa1f                   sar      edx, 0x1f
0046e9f9  c1e208                   shl      edx, 8
0046e9fc  1bc2                     sbb      eax, edx
0046e9fe  c1f808                   sar      eax, 8
0046ea01  3dff000000               cmp      eax, 0xff
0046ea06  7437                     je       0x46ea3f
0046ea08  b900010000               mov      ecx, 0x100
0046ea0d  89da                     mov      edx, ebx
0046ea0f  89d8                     mov      eax, ebx
0046ea11  c1fa1f                   sar      edx, 0x1f
0046ea14  f7f9                     idiv     ecx
0046ea16  85d2                     test     edx, edx
0046ea18  7425                     je       0x46ea3f
0046ea1a  6a00                     push     0
0046ea1c  668b4616                 mov      ax, word ptr [esi + 0x16]
0046ea20  31c9                     xor      ecx, ecx
0046ea22  31db                     xor      ebx, ebx
0046ea24  31d2                     xor      edx, edx
0046ea26  05ff000000               add      eax, 0xff
0046ea2b  8a4e22                   mov      cl, byte ptr [esi + 0x22]
0046ea2e  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046ea32  8a561f                   mov      dl, byte ptr [esi + 0x1f]
0046ea35  25ffff0000               and      eax, 0xffff
0046ea3a  e8351efeff               call     0x450874
0046ea3f  31d2                     xor      edx, edx
0046ea41  668b5616                 mov      dx, word ptr [esi + 0x16]
0046ea45  89d0                     mov      eax, edx
0046ea47  c1fa1f                   sar      edx, 0x1f
0046ea4a  c1e208                   shl      edx, 8
0046ea4d  1bc2                     sbb      eax, edx
0046ea4f  c1f808                   sar      eax, 8
0046ea52  3dff000000               cmp      eax, 0xff
0046ea57  7422                     je       0x46ea7b
0046ea59  6a00                     push     0
0046ea5b  668b4616                 mov      ax, word ptr [esi + 0x16]
0046ea5f  31c9                     xor      ecx, ecx
0046ea61  31db                     xor      ebx, ebx
0046ea63  31d2                     xor      edx, edx
0046ea65  fec4                     inc      ah
0046ea67  8a4e22                   mov      cl, byte ptr [esi + 0x22]
0046ea6a  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046ea6e  8a561f                   mov      dl, byte ptr [esi + 0x1f]
0046ea71  25ffff0000               and      eax, 0xffff
0046ea76  e8f91dfeff               call     0x450874
0046ea7b  31db                     xor      ebx, ebx
0046ea7d  668b5e16                 mov      bx, word ptr [esi + 0x16]
0046ea81  89da                     mov      edx, ebx
0046ea83  89d8                     mov      eax, ebx
0046ea85  c1fa1f                   sar      edx, 0x1f
0046ea88  c1e208                   shl      edx, 8
0046ea8b  1bc2                     sbb      eax, edx
0046ea8d  c1f808                   sar      eax, 8
0046ea90  3dff000000               cmp      eax, 0xff
0046ea95  745c                     je       0x46eaf3
0046ea97  b900010000               mov      ecx, 0x100
0046ea9c  89da                     mov      edx, ebx
0046ea9e  89d8                     mov      eax, ebx
0046eaa0  c1fa1f                   sar      edx, 0x1f
0046eaa3  f7f9                     idiv     ecx
0046eaa5  81faff000000             cmp      edx, 0xff
0046eaab  7446                     je       0x46eaf3
0046eaad  6a00                     push     0
0046eaaf  668b4616                 mov      ax, word ptr [esi + 0x16]
0046eab3  31c9                     xor      ecx, ecx
0046eab5  31db                     xor      ebx, ebx
0046eab7  31d2                     xor      edx, edx
0046eab9  0501010000               add      eax, 0x101
0046eabe  8a4e22                   mov      cl, byte ptr [esi + 0x22]
0046eac1  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046eac5  8a561f                   mov      dl, byte ptr [esi + 0x1f]
0046eac8  e9bbfdffff               jmp      0x46e888
0046eacd  80fb17                   cmp      bl, 0x17
0046ead0  0f82c1fdffff             jb       0x46e897
0046ead6  5e                       pop      esi
0046ead7  5a                       pop      edx
0046ead8  59                       pop      ecx
0046ead9  5b                       pop      ebx
0046eada  c3                       ret
0046eadb  80fb0e                   cmp      bl, 0xe
0046eade  7213                     jb       0x46eaf3
0046eae0  80fb10                   cmp      bl, 0x10
0046eae3  760e                     jbe      0x46eaf3
0046eae5  80fb12                   cmp      bl, 0x12
0046eae8  7209                     jb       0x46eaf3
0046eaea  80fb13                   cmp      bl, 0x13
0046eaed  0f87a4fdffff             ja       0x46e897
0046eaf3  5e                       pop      esi
0046eaf4  5a                       pop      edx
0046eaf5  59                       pop      ecx
0046eaf6  5b                       pop      ebx
0046eaf7  c3                       ret
