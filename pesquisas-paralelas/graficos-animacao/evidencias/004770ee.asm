; CalculDirCase [0x4770ee, 0x4772ec)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
004770ee  53                     push     ebx
004770ef  51                     push     ecx
004770f0  56                     push     esi
004770f1  89c3                   mov      ebx, eax
004770f3  80fa07                 cmp      dl, 7
004770f6  0f82d3010000           jb       0x4772cf
004770fc  762c                   jbe      0x47712a
004770fe  80fa0b                 cmp      dl, 0xb
00477101  0f82bd010000           jb       0x4772c4
00477107  0f868a000000           jbe      0x477197
0047710d  80fa0d                 cmp      dl, 0xd
00477110  0f82a8010000           jb       0x4772be
00477116  0f867c010000           jbe      0x477298
0047711c  80fa0f                 cmp      dl, 0xf
0047711f  0f840c010000           je       0x477231
00477125  e994010000             jmp      0x4772be ;
0047712a  31c9                   xor      ecx, ecx
0047712c  6689c1                 mov      cx, ax
0047712f  89ca                   mov      edx, ecx
00477131  89c8                   mov      eax, ecx
00477133  c1fa1f                 sar      edx, 0x1f
00477136  c1e208                 shl      edx, 8
00477139  1bc2                   sbb      eax, edx
0047713b  c1f808                 sar      eax, 8
0047713e  85c0                   test     eax, eax
00477140  741b                   je       0x47715d
00477142  be00010000             mov      esi, 0x100
00477147  89ca                   mov      edx, ecx
00477149  89c8                   mov      eax, ecx
0047714b  c1fa1f                 sar      edx, 0x1f
0047714e  f7fe                   idiv     esi
00477150  31c0                   xor      eax, eax
00477152  66a168714900           mov      ax, word ptr [0x497168]
00477158  48                     dec      eax
00477159  39c2                   cmp      edx, eax
0047715b  7509                   jne      0x477166
0047715d  b8ffff0000             mov      eax, 0xffff
00477162  5e                     pop      esi
00477163  59                     pop      ecx
00477164  5b                     pop      ebx
00477165  c3                     ret
00477166  89d8                   mov      eax, ebx
00477168  81e8ff000000           sub      eax, 0xff
0047716e  5e                     pop      esi
0047716f  59                     pop      ecx
00477170  5b                     pop      ebx
00477171  c3                     ret
00477172  31d2                   xor      edx, edx
00477174  6689c2                 mov      dx, ax
00477177  b900010000             mov      ecx, 0x100
0047717c  89d0                   mov      eax, edx
0047717e  c1fa1f                 sar      edx, 0x1f
00477181  f7f9                   idiv     ecx
00477183  31c0                   xor      eax, eax
00477185  66a168714900           mov      ax, word ptr [0x497168]
0047718b  48                     dec      eax
0047718c  39c2                   cmp      edx, eax
0047718e  74cd                   je       0x47715d
00477190  89d8                   mov      eax, ebx
00477192  40                     inc      eax
00477193  5e                     pop      esi
00477194  59                     pop      ecx
00477195  5b                     pop      ebx
00477196  c3                     ret
00477197  31c9                   xor      ecx, ecx
00477199  6689c1                 mov      cx, ax
0047719c  be00010000             mov      esi, 0x100
004771a1  89ca                   mov      edx, ecx
004771a3  89c8                   mov      eax, ecx
004771a5  c1fa1f                 sar      edx, 0x1f
004771a8  f7fe                   idiv     esi
004771aa  31c0                   xor      eax, eax
004771ac  66a168714900           mov      ax, word ptr [0x497168]
004771b2  48                     dec      eax
004771b3  39c2                   cmp      edx, eax
004771b5  74a6                   je       0x47715d
004771b7  89ca                   mov      edx, ecx
004771b9  89c8                   mov      eax, ecx
004771bb  c1fa1f                 sar      edx, 0x1f
004771be  f7fe                   idiv     esi
004771c0  31d2                   xor      edx, edx
004771c2  668b156a714900         mov      dx, word ptr [0x49716a]
004771c9  4a                     dec      edx
004771ca  39d0                   cmp      eax, edx
004771cc  748f                   je       0x47715d
004771ce  89d8                   mov      eax, ebx
004771d0  0501010000             add      eax, 0x101
004771d5  5e                     pop      esi
004771d6  59                     pop      ecx
004771d7  5b                     pop      ebx
004771d8  c3                     ret
004771d9  31c9                   xor      ecx, ecx
004771db  6689c1                 mov      cx, ax
004771de  be00010000             mov      esi, 0x100
004771e3  89ca                   mov      edx, ecx
004771e5  89c8                   mov      eax, ecx
004771e7  c1fa1f                 sar      edx, 0x1f
004771ea  f7fe                   idiv     esi
004771ec  85d2                   test     edx, edx
004771ee  0f8469ffffff           je       0x47715d
004771f4  89ca                   mov      edx, ecx
004771f6  89c8                   mov      eax, ecx
004771f8  c1fa1f                 sar      edx, 0x1f
004771fb  f7fe                   idiv     esi
004771fd  85c0                   test     eax, eax
004771ff  0f8458ffffff           je       0x47715d
00477205  89d8                   mov      eax, ebx
00477207  81e801010000           sub      eax, 0x101
0047720d  5e                     pop      esi
0047720e  59                     pop      ecx
0047720f  5b                     pop      ebx
00477210  c3                     ret
00477211  31d2                   xor      edx, edx
00477213  6689c2                 mov      dx, ax
00477216  b900010000             mov      ecx, 0x100
0047721b  89d0                   mov      eax, edx
0047721d  c1fa1f                 sar      edx, 0x1f
00477220  f7f9                   idiv     ecx
00477222  85d2                   test     edx, edx
00477224  0f8433ffffff           je       0x47715d
0047722a  89d8                   mov      eax, ebx
0047722c  48                     dec      eax
0047722d  5e                     pop      esi
0047722e  59                     pop      ecx
0047722f  5b                     pop      ebx
00477230  c3                     ret
00477231  31c9                   xor      ecx, ecx
00477233  6689c1                 mov      cx, ax
00477236  be00010000             mov      esi, 0x100
0047723b  89ca                   mov      edx, ecx
0047723d  89c8                   mov      eax, ecx
0047723f  c1fa1f                 sar      edx, 0x1f
00477242  f7fe                   idiv     esi
00477244  85d2                   test     edx, edx
00477246  0f8411ffffff           je       0x47715d
0047724c  89ca                   mov      edx, ecx
0047724e  89c8                   mov      eax, ecx
00477250  c1fa1f                 sar      edx, 0x1f
00477253  f7fe                   idiv     esi
00477255  31d2                   xor      edx, edx
00477257  668b156a714900         mov      dx, word ptr [0x49716a]
0047725e  4a                     dec      edx
0047725f  39d0                   cmp      eax, edx
00477261  0f84f6feffff           je       0x47715d
00477267  89d8                   mov      eax, ebx
00477269  05ff000000             add      eax, 0xff
0047726e  5e                     pop      esi
0047726f  59                     pop      ecx
00477270  5b                     pop      ebx
00477271  c3                     ret
00477272  31d2                   xor      edx, edx
00477274  6689c2                 mov      dx, ax
00477277  89d0                   mov      eax, edx
00477279  c1fa1f                 sar      edx, 0x1f
0047727c  c1e208                 shl      edx, 8
0047727f  1bc2                   sbb      eax, edx
00477281  c1f808                 sar      eax, 8
00477284  85c0                   test     eax, eax
00477286  0f84d1feffff           je       0x47715d
0047728c  89d8                   mov      eax, ebx
0047728e  81e800010000           sub      eax, 0x100
00477294  5e                     pop      esi
00477295  59                     pop      ecx
00477296  5b                     pop      ebx
00477297  c3                     ret
00477298  31d2                   xor      edx, edx
0047729a  6689c2                 mov      dx, ax
0047729d  89d0                   mov      eax, edx
0047729f  c1fa1f                 sar      edx, 0x1f
004772a2  c1e208                 shl      edx, 8
004772a5  1bc2                   sbb      eax, edx
004772a7  c1f808                 sar      eax, 8
004772aa  31d2                   xor      edx, edx
004772ac  668b156a714900         mov      dx, word ptr [0x49716a]
004772b3  4a                     dec      edx
004772b4  39d0                   cmp      eax, edx
004772b6  0f84a1feffff           je       0x47715d
004772bc  fec7                   inc      bh
004772be  89d8                   mov      eax, ebx
004772c0  5e                     pop      esi
004772c1  59                     pop      ecx
004772c2  5b                     pop      ebx
004772c3  c3                     ret
004772c4  80fa09                 cmp      dl, 9
004772c7  0f84a5feffff           je       0x477172
004772cd  ebef                   jmp      0x4772be ;
004772cf  80fa03                 cmp      dl, 3
004772d2  720d                   jb       0x4772e1
004772d4  0f86fffeffff           jbe      0x4771d9
004772da  80fa05                 cmp      dl, 5
004772dd  7493                   je       0x477272
004772df  ebdd                   jmp      0x4772be ;
004772e1  80fa01                 cmp      dl, 1
004772e4  0f8427ffffff           je       0x477211
004772ea  ebd2                   jmp      0x4772be ;
