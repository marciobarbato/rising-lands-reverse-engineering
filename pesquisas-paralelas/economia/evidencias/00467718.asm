; CalculMatiere: limite por próximo símbolo SBL, fim exclusivo 0x004678f2.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00467718  53                       push     ebx
00467719  51                       push     ecx
0046771a  52                       push     edx
0046771b  56                       push     esi
0046771c  57                       push     edi
0046771d  55                       push     ebp
0046771e  83ec10                   sub      esp, 0x10
00467721  30e4                     xor      ah, ah
00467723  bda82e4e00               mov      ebp, 0x4e2ea8
00467728  8864240c                 mov      byte ptr [esp + 0xc], ah
0046772c  be01000000               mov      esi, 1
00467731  eb25                     jmp      0x467758
00467733  31c0                     xor      eax, eax
00467735  31d2                     xor      edx, edx
00467737  a041805000               mov      al, byte ptr [0x508041]
0046773c  8a54240c                 mov      dl, byte ptr [esp + 0xc]
00467740  c1e002                   shl      eax, 2
00467743  01d0                     add      eax, edx
00467745  c1e003                   shl      eax, 3
00467748  01e8                     add      eax, ebp
0046774a  89e2                     mov      edx, esp
0046774c  83c004                   add      eax, 4
0046774f  e8e6050000               call     0x467d3a
00467754  fe44240c                 inc      byte ptr [esp + 0xc]
00467758  31db                     xor      ebx, ebx
0046775a  8a5c240c                 mov      bl, byte ptr [esp + 0xc]
0046775e  83fb04                   cmp      ebx, 4
00467761  0f8d81010000             jge      0x4678e8
00467767  31c0                     xor      eax, eax
00467769  a041805000               mov      al, byte ptr [0x508041]
0046776e  c1e002                   shl      eax, 2
00467771  8d1403                   lea      edx, [ebx + eax]
00467774  668b14d5ac2e4e00         mov      dx, word ptr [edx*8 + 0x4e2eac]
0046777c  89e0                     mov      eax, esp
0046777e  81e2ffff0000             and      edx, 0xffff
00467784  e848050000               call     0x467cd1
00467789  31c0                     xor      eax, eax
0046778b  a041805000               mov      al, byte ptr [0x508041]
00467790  c1e002                   shl      eax, 2
00467793  01d8                     add      eax, ebx
00467795  31d2                     xor      edx, edx
00467797  668b14c5aa2e4e00         mov      dx, word ptr [eax*8 + 0x4e2eaa]
0046779f  8d442404                 lea      eax, [esp + 4]
004677a3  e829050000               call     0x467cd1
004677a8  30d2                     xor      dl, dl
004677aa  88542408                 mov      byte ptr [esp + 8], dl
004677ae  31ff                     xor      edi, edi
004677b0  eb64                     jmp      0x467816
004677b2  0f86d2000000             jbe      0x46788a
004677b8  c605a2054e0001           mov      byte ptr [0x4e05a2], 1
004677bf  31c0                     xor      eax, eax
004677c1  31db                     xor      ebx, ebx
004677c3  a041805000               mov      al, byte ptr [0x508041]
004677c8  8a5c240c                 mov      bl, byte ptr [esp + 0xc]
004677cc  c1e002                   shl      eax, 2
004677cf  01d8                     add      eax, ebx
004677d1  8a04c5ae2e4e00           mov      al, byte ptr [eax*8 + 0x4e2eae]
004677d8  25ff000000               and      eax, 0xff
004677dd  89ca                     mov      edx, ecx
004677df  e8b3050000               call     0x467d97
004677e4  25ff000000               and      eax, 0xff
004677e9  0f8597000000             jne      0x467886
004677ef  fe0c0c                   dec      byte ptr [esp + ecx]
004677f2  31c0                     xor      eax, eax
004677f4  a041805000               mov      al, byte ptr [0x508041]
004677f9  c1e002                   shl      eax, 2
004677fc  01d8                     add      eax, ebx
004677fe  c1e003                   shl      eax, 3
00467801  89ca                     mov      edx, ecx
00467803  01e8                     add      eax, ebp
00467805  bb01000000               mov      ebx, 1
0046780a  83c006                   add      eax, 6
0046780d  e85f050000               call     0x467d71
00467812  fe442408                 inc      byte ptr [esp + 8]
00467816  31c9                     xor      ecx, ecx
00467818  8a4c2408                 mov      cl, byte ptr [esp + 8]
0046781c  83f904                   cmp      ecx, 4
0046781f  0f8d0effffff             jge      0x467733
00467825  8a040c                   mov      al, byte ptr [esp + ecx]
00467828  8a5c0c04                 mov      bl, byte ptr [esp + ecx + 4]
0046782c  38d8                     cmp      al, bl
0046782e  7382                     jae      0x4677b2
00467830  31c0                     xor      eax, eax
00467832  31db                     xor      ebx, ebx
00467834  a041805000               mov      al, byte ptr [0x508041]
00467839  8a5c240c                 mov      bl, byte ptr [esp + 0xc]
0046783d  c1e002                   shl      eax, 2
00467840  b201                     mov      dl, 1
00467842  01d8                     add      eax, ebx
00467844  8815a2054e00             mov      byte ptr [0x4e05a2], dl
0046784a  8a04c5ae2e4e00           mov      al, byte ptr [eax*8 + 0x4e2eae]
00467851  25ff000000               and      eax, 0xff
00467856  89ca                     mov      edx, ecx
00467858  e83a050000               call     0x467d97
0046785d  25ff000000               and      eax, 0xff
00467862  83f801                   cmp      eax, 1
00467865  758b                     jne      0x4677f2
00467867  8a340c                   mov      dh, byte ptr [esp + ecx]
0046786a  fec6                     inc      dh
0046786c  31c0                     xor      eax, eax
0046786e  88340c                   mov      byte ptr [esp + ecx], dh
00467871  a041805000               mov      al, byte ptr [0x508041]
00467876  c1e002                   shl      eax, 2
00467879  01d8                     add      eax, ebx
0046787b  c1e003                   shl      eax, 3
0046787e  89ca                     mov      edx, ecx
00467880  01e8                     add      eax, ebp
00467882  89fb                     mov      ebx, edi
00467884  eb84                     jmp      0x46780a
00467886  31c0                     xor      eax, eax
00467888  ebe7                     jmp      0x467871
0046788a  31c0                     xor      eax, eax
0046788c  31db                     xor      ebx, ebx
0046788e  a041805000               mov      al, byte ptr [0x508041]
00467893  8a5c240c                 mov      bl, byte ptr [esp + 0xc]
00467897  c1e002                   shl      eax, 2
0046789a  01d8                     add      eax, ebx
0046789c  8a04c5ae2e4e00           mov      al, byte ptr [eax*8 + 0x4e2eae]
004678a3  25ff000000               and      eax, 0xff
004678a8  89ca                     mov      edx, ecx
004678aa  e8e8040000               call     0x467d97
004678af  25ff000000               and      eax, 0xff
004678b4  83f801                   cmp      eax, 1
004678b7  0f8555ffffff             jne      0x467812
004678bd  31c0                     xor      eax, eax
004678bf  a041805000               mov      al, byte ptr [0x508041]
004678c4  c1e002                   shl      eax, 2
004678c7  01c3                     add      ebx, eax
004678c9  c1e303                   shl      ebx, 3
004678cc  8d042b                   lea      eax, [ebx + ebp]
004678cf  89ca                     mov      edx, ecx
004678d1  83c006                   add      eax, 6
004678d4  89fb                     mov      ebx, edi
004678d6  b101                     mov      cl, 1
004678d8  e894040000               call     0x467d71
004678dd  880da2054e00             mov      byte ptr [0x4e05a2], cl
004678e3  e92affffff               jmp      0x467812
004678e8  83c410                   add      esp, 0x10
004678eb  5d                       pop      ebp
004678ec  5f                       pop      edi
004678ed  5e                       pop      esi
004678ee  5a                       pop      edx
004678ef  59                       pop      ecx
004678f0  5b                       pop      ebx
004678f1  c3                       ret
