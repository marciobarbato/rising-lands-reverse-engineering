; CalculEntreBatiment; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00449716  53                       push ebx
00449717  51                       push ecx
00449718  52                       push edx
00449719  56                       push esi
0044971a  57                       push edi
0044971b  55                       push ebp
0044971c  83ec1c                   sub esp, 0x1c
0044971f  89c7                     mov edi, eax
00449721  0fb7e8                   movzx ebp, ax
00449724  89eb                     mov ebx, ebp
00449726  c1e304                   shl ebx, 4
00449729  01eb                     add ebx, ebp
0044972b  c1e302                   shl ebx, 2
0044972e  01eb                     add ebx, ebp
00449730  8b35a0194e00             mov esi, dword ptr [0x4e19a0]
00449736  c1e302                   shl ebx, 2
00449739  01de                     add esi, ebx
0044973b  8a4601                   mov al, byte ptr [esi + 1]
0044973e  891c24                   mov dword ptr [esp], ebx
00449741  3c06                     cmp al, 6
00449743  0f829d0b0000             jb 0x44a2e6
00449749  761e                     jbe 0x449769
0044974b  3c09                     cmp al, 9
0044974d  721a                     jb 0x449769
0044974f  3c0a                     cmp al, 0xa
00449751  7616                     jbe 0x449769
00449753  3c10                     cmp al, 0x10
00449755  0f82d4090000             jb 0x44a12f
0044975b  0f86f5040000             jbe 0x449c56
00449761  3c19                     cmp al, 0x19
00449763  0f85c6090000             jne 0x44a12f
00449769  31c0                     xor eax, eax
0044976b  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00449772  3dffff0000               cmp eax, 0xffff
00449777  0f8428010000             je 0x4498a5
0044977d  e8720dfdff               call 0x41a4f4
00449782  25ff000000               and eax, 0xff
00449787  83f808                   cmp eax, 8
0044978a  0f851d010000             jne 0x4498ad
00449790  31c9                     xor ecx, ecx
00449792  6689f9                   mov cx, di
00449795  89cd                     mov ebp, ecx
00449797  31c0                     xor eax, eax
00449799  c1e504                   shl ebp, 4
0044979c  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004497a3  01cd                     add ebp, ecx
004497a5  e8e208fdff               call 0x41a08c
004497aa  c1e502                   shl ebp, 2
004497ad  8844240c                 mov byte ptr [esp + 0xc], al
004497b1  01cd                     add ebp, ecx
004497b3  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004497b8  c1e502                   shl ebp, 2
004497bb  8a54240c                 mov dl, byte ptr [esp + 0xc]
004497bf  3a1428                   cmp dl, byte ptr [eax + ebp]
004497c2  0f85e5000000             jne 0x4498ad
004497c8  31c0                     xor eax, eax
004497ca  89ca                     mov edx, ecx
004497cc  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004497d3  e87f38fdff               call 0x41d057
004497d8  668986b2000000           mov word ptr [esi + 0xb2], ax
004497df  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004497e5  01ea                     add edx, ebp
004497e7  6689427e                 mov word ptr [edx + 0x7e], ax
004497eb  663b3d04634900           cmp di, word ptr [0x496304]
004497f2  7522                     jne 0x449816
004497f4  bbffff0000               mov ebx, 0xffff
004497f9  30c9                     xor cl, cl
004497fb  31ed                     xor ebp, ebp
004497fd  880d360f4e00             mov byte ptr [0x4e0f36], cl
00449803  880d370f4e00             mov byte ptr [0x4e0f37], cl
00449809  892d3c0f4e00             mov dword ptr [0x4e0f3c], ebp
0044980f  66891d04634900           mov word ptr [0x496304], bx
00449816  c6828800000000           mov byte ptr [edx + 0x88], 0
0044981d  31d2                     xor edx, edx
0044981f  6689fa                   mov dx, di
00449822  89d3                     mov ebx, edx
00449824  c1e304                   shl ebx, 4
00449827  b015                     mov al, 0x15
00449829  01d3                     add ebx, edx
0044982b  88442418                 mov byte ptr [esp + 0x18], al
0044982f  c1e302                   shl ebx, 2
00449832  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00449837  01d3                     add ebx, edx
00449839  89f9                     mov ecx, edi
0044983b  8a449802                 mov al, byte ptr [eax + ebx*4 + 2]
0044983f  25ff000000               and eax, 0xff
00449844  7409                     je 0x44984f
00449846  83f804                   cmp eax, 4
00449849  7404                     je 0x44984f
0044984b  b001                     mov al, 1
0044984d  eb02                     jmp 0x449851
0044984f  30c0                     xor al, al
00449851  84c0                     test al, al
00449853  0f844c000000             je 0x4498a5
00449859  31d2                     xor edx, edx
0044985b  6689ca                   mov dx, cx
0044985e  89d3                     mov ebx, edx
00449860  c1e304                   shl ebx, 4
00449863  01d3                     add ebx, edx
00449865  c1e302                   shl ebx, 2
00449868  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044986d  01d3                     add ebx, edx
0044986f  8a542418                 mov dl, byte ptr [esp + 0x18]
00449873  88549802                 mov byte ptr [eax + ebx*4 + 2], dl
00449877  663b0d04634900           cmp cx, word ptr [0x496304]
0044987e  0f8521000000             jne 0x4498a5
00449884  30e4                     xor ah, ah
00449886  bfffff0000               mov edi, 0xffff
0044988b  8825360f4e00             mov byte ptr [0x4e0f36], ah
00449891  8825370f4e00             mov byte ptr [0x4e0f37], ah
00449897  31c0                     xor eax, eax
00449899  66893d04634900           mov word ptr [0x496304], di
004498a0  a33c0f4e00               mov dword ptr [0x4e0f3c], eax
004498a5  83c41c                   add esp, 0x1c
004498a8  e9f0590000               jmp 0x44f29d
004498ad  8b8683000000             mov eax, dword ptr [esi + 0x83]
004498b3  c1f818                   sar eax, 0x18
004498b6  85c0                     test eax, eax
004498b8  7527                     jne 0x4498e1
004498ba  8b8684000000             mov eax, dword ptr [esi + 0x84]
004498c0  c1f818                   sar eax, 0x18
004498c3  85c0                     test eax, eax
004498c5  751a                     jne 0x4498e1
004498c7  31d2                     xor edx, edx
004498c9  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004498d0  668b5608                 mov dx, word ptr [esi + 8]
004498d4  e8469ffdff               call 0x42381f
004498d9  84c0                     test al, al
004498db  0f8579000000             jne 0x44995a
004498e1  668b467e                 mov ax, word ptr [esi + 0x7e]
004498e5  663b4608                 cmp ax, word ptr [esi + 8]
004498e9  7560                     jne 0x44994b
004498eb  31d2                     xor edx, edx
004498ed  6689fa                   mov dx, di
004498f0  89d3                     mov ebx, edx
004498f2  c1e304                   shl ebx, 4
004498f5  31c0                     xor eax, eax
004498f7  01d3                     add ebx, edx
004498f9  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00449900  c1e302                   shl ebx, 2
00449903  e8da15fdff               call 0x41aee2
00449908  01d3                     add ebx, edx
0044990a  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00449910  c1e302                   shl ebx, 2
00449913  01da                     add edx, ebx
00449915  6689427e                 mov word ptr [edx + 0x7e], ax
00449919  663b3d04634900           cmp di, word ptr [0x496304]
00449920  7522                     jne 0x449944
00449922  30db                     xor bl, bl
00449924  31f6                     xor esi, esi
00449926  881d360f4e00             mov byte ptr [0x4e0f36], bl
0044992c  89353c0f4e00             mov dword ptr [0x4e0f3c], esi
00449932  beffff0000               mov esi, 0xffff
00449937  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044993d  66893504634900           mov word ptr [0x496304], si
00449944  c6828800000000           mov byte ptr [edx + 0x88], 0
0044994b  31c0                     xor eax, eax
0044994d  6689f8                   mov ax, di
00449950  e8b7f9ffff               call 0x44930c
00449955  e94bffffff               jmp 0x4498a5
0044995a  31c9                     xor ecx, ecx
0044995c  6689f9                   mov cx, di
0044995f  89cd                     mov ebp, ecx
00449961  c1e504                   shl ebp, 4
00449964  31c0                     xor eax, eax
00449966  01cd                     add ebp, ecx
00449968  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044996f  c1e502                   shl ebp, 2
00449972  89ca                     mov edx, ecx
00449974  01cd                     add ebp, ecx
00449976  e8f35dfdff               call 0x41f76e
0044997b  c1e502                   shl ebp, 2
0044997e  84c0                     test al, al
00449980  0f845d020000             je 0x449be3
00449986  31c0                     xor eax, eax
00449988  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044998f  e84e15fdff               call 0x41aee2
00449994  89c2                     mov edx, eax
00449996  89442404                 mov dword ptr [esp + 4], eax
0044999a  89c8                     mov eax, ecx
0044999c  e8b7d60000               call 0x457058
004499a1  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004499a6  8a442801                 mov al, byte ptr [eax + ebp + 1]
004499aa  25ff000000               and eax, 0xff
004499af  83f80a                   cmp eax, 0xa
004499b2  0f85ac000000             jne 0x449a64
004499b8  31c0                     xor eax, eax
004499ba  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004499c1  e82e0bfdff               call 0x41a4f4
004499c6  25ff000000               and eax, 0xff
004499cb  83f810                   cmp eax, 0x10
004499ce  0f8590000000             jne 0x449a64
004499d4  89d0                     mov eax, edx
004499d6  6689567c                 mov word ptr [esi + 0x7c], dx
004499da  31db                     xor ebx, ebx
004499dc  66894608                 mov word ptr [esi + 8], ax
004499e0  89c8                     mov eax, ecx
004499e2  ba44000000               mov edx, 0x44
004499e7  e85c8c0200               call 0x472648
004499ec  89c8                     mov eax, ecx
004499ee  e8d58f0300               call 0x4829c8
004499f3  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004499f8  01c5                     add ebp, eax
004499fa  31c0                     xor eax, eax
004499fc  8a4502                   mov al, byte ptr [ebp + 2]
004499ff  30d2                     xor dl, dl
00449a01  85c0                     test eax, eax
00449a03  7409                     je 0x449a0e
00449a05  83f804                   cmp eax, 4
00449a08  7404                     je 0x449a0e
00449a0a  b001                     mov al, 1
00449a0c  eb02                     jmp 0x449a10
00449a0e  30c0                     xor al, al
00449a10  84c0                     test al, al
00449a12  0f848dfeffff             je 0x4498a5
00449a18  31c0                     xor eax, eax
00449a1a  6689f8                   mov ax, di
00449a1d  89c3                     mov ebx, eax
00449a1f  c1e304                   shl ebx, 4
00449a22  01c3                     add ebx, eax
00449a24  c1e302                   shl ebx, 2
00449a27  01c3                     add ebx, eax
00449a29  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00449a2e  88549802                 mov byte ptr [eax + ebx*4 + 2], dl
00449a32  663b3d04634900           cmp di, word ptr [0x496304]
00449a39  0f8566feffff             jne 0x4498a5
00449a3f  baffff0000               mov edx, 0xffff
00449a44  30c0                     xor al, al
00449a46  31c9                     xor ecx, ecx
00449a48  a2360f4e00               mov byte ptr [0x4e0f36], al
00449a4d  a2370f4e00               mov byte ptr [0x4e0f37], al
00449a52  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
00449a58  66891504634900           mov word ptr [0x496304], dx
00449a5f  e941feffff               jmp 0x4498a5
00449a64  31c9                     xor ecx, ecx
00449a66  6689f9                   mov cx, di
00449a69  89cd                     mov ebp, ecx
00449a6b  c1e504                   shl ebp, 4
00449a6e  01cd                     add ebp, ecx
00449a70  c1e502                   shl ebp, 2
00449a73  01cd                     add ebp, ecx
00449a75  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00449a7a  c1e502                   shl ebp, 2
00449a7d  8a442801                 mov al, byte ptr [eax + ebp + 1]
00449a81  25ff000000               and eax, 0xff
00449a86  83f80a                   cmp eax, 0xa
00449a89  0f85e1000000             jne 0x449b70
00449a8f  31c0                     xor eax, eax
00449a91  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00449a98  e8570afdff               call 0x41a4f4
00449a9d  25ff000000               and eax, 0xff
00449aa2  83f802                   cmp eax, 2
00449aa5  0f85c5000000             jne 0x449b70
00449aab  31c0                     xor eax, eax
00449aad  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00449ab4  e8d305fdff               call 0x41a08c
00449ab9  3a06                     cmp al, byte ptr [esi]
00449abb  0f84af000000             je 0x449b70
00449ac1  31c0                     xor eax, eax
00449ac3  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00449aca  31d2                     xor edx, edx
00449acc  e8bb05fdff               call 0x41a08c
00449ad1  88c2                     mov dl, al
00449ad3  31c0                     xor eax, eax
00449ad5  8a06                     mov al, byte ptr [esi]
00449ad7  e8ff3f0200               call 0x46dadb
00449adc  8b442404                 mov eax, dword ptr [esp + 4]
00449ae0  6689467c                 mov word ptr [esi + 0x7c], ax
00449ae4  31db                     xor ebx, ebx
00449ae6  66894608                 mov word ptr [esi + 8], ax
00449aea  89c8                     mov eax, ecx
00449aec  ba44000000               mov edx, 0x44
00449af1  e8528b0200               call 0x472648
00449af6  89c8                     mov eax, ecx
00449af8  e8cb8e0300               call 0x4829c8
00449afd  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00449b02  30d2                     xor dl, dl
00449b04  8a442802                 mov al, byte ptr [eax + ebp + 2]
00449b08  25ff000000               and eax, 0xff
00449b0d  7409                     je 0x449b18
00449b0f  83f804                   cmp eax, 4
00449b12  7404                     je 0x449b18
00449b14  b001                     mov al, 1
00449b16  eb02                     jmp 0x449b1a
00449b18  30c0                     xor al, al
00449b1a  84c0                     test al, al
00449b1c  0f8483fdffff             je 0x4498a5
00449b22  31c0                     xor eax, eax
00449b24  6689f8                   mov ax, di
00449b27  89c3                     mov ebx, eax
00449b29  c1e304                   shl ebx, 4
00449b2c  01c3                     add ebx, eax
00449b2e  c1e302                   shl ebx, 2
00449b31  01c3                     add ebx, eax
00449b33  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00449b38  88549802                 mov byte ptr [eax + ebx*4 + 2], dl
00449b3c  663b3d04634900           cmp di, word ptr [0x496304]
00449b43  0f855cfdffff             jne 0x4498a5
00449b49  beffff0000               mov esi, 0xffff
00449b4e  30c9                     xor cl, cl
00449b50  31db                     xor ebx, ebx
00449b52  880d360f4e00             mov byte ptr [0x4e0f36], cl
00449b58  880d370f4e00             mov byte ptr [0x4e0f37], cl
00449b5e  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
00449b64  66893504634900           mov word ptr [0x496304], si
00449b6b  e935fdffff               jmp 0x4498a5
00449b70  31c0                     xor eax, eax
00449b72  8a4601                   mov al, byte ptr [esi + 1]
00449b75  83f809                   cmp eax, 9
00449b78  744a                     je 0x449bc4
00449b7a  31c0                     xor eax, eax
00449b7c  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00449b83  e86c09fdff               call 0x41a4f4
00449b88  25ff000000               and eax, 0xff
00449b8d  83f813                   cmp eax, 0x13
00449b90  7432                     je 0x449bc4
00449b92  31c0                     xor eax, eax
00449b94  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00449b9b  e85409fdff               call 0x41a4f4
00449ba0  25ff000000               and eax, 0xff
00449ba5  83f815                   cmp eax, 0x15
00449ba8  741a                     je 0x449bc4
00449baa  31c9                     xor ecx, ecx
00449bac  ba47000000               mov edx, 0x47
00449bb1  6689f9                   mov cx, di
00449bb4  31db                     xor ebx, ebx
00449bb6  89c8                     mov eax, ecx
00449bb8  e80b8e0300               call 0x4829c8
00449bbd  89c8                     mov eax, ecx
00449bbf  e810d60000               call 0x4571d4
00449bc4  8b442404                 mov eax, dword ptr [esp + 4]
00449bc8  6689467c                 mov word ptr [esi + 0x7c], ax
00449bcc  66894608                 mov word ptr [esi + 8], ax
00449bd0  31c0                     xor eax, eax
00449bd2  6689f8                   mov ax, di
00449bd5  e86e8a0200               call 0x472648
00449bda  c646020e                 mov byte ptr [esi + 2], 0xe
00449bde  e9c2fcffff               jmp 0x4498a5
00449be3  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00449be8  01c5                     add ebp, eax
00449bea  31c0                     xor eax, eax
00449bec  8a4502                   mov al, byte ptr [ebp + 2]
00449bef  b107                     mov cl, 7
00449bf1  85c0                     test eax, eax
00449bf3  7409                     je 0x449bfe
00449bf5  83f804                   cmp eax, 4
00449bf8  7404                     je 0x449bfe
00449bfa  b001                     mov al, 1
00449bfc  eb02                     jmp 0x449c00
00449bfe  30c0                     xor al, al
00449c00  84c0                     test al, al
00449c02  0f849dfcffff             je 0x4498a5
00449c08  31d2                     xor edx, edx
00449c0a  6689fa                   mov dx, di
00449c0d  89d3                     mov ebx, edx
00449c0f  c1e304                   shl ebx, 4
00449c12  01d3                     add ebx, edx
00449c14  c1e302                   shl ebx, 2
00449c17  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00449c1c  01d3                     add ebx, edx
00449c1e  884c9802                 mov byte ptr [eax + ebx*4 + 2], cl
00449c22  663b3d04634900           cmp di, word ptr [0x496304]
00449c29  0f8576fcffff             jne 0x4498a5
00449c2f  30f6                     xor dh, dh
00449c31  bbffff0000               mov ebx, 0xffff
00449c36  8835360f4e00             mov byte ptr [0x4e0f36], dh
00449c3c  8835370f4e00             mov byte ptr [0x4e0f37], dh
00449c42  31d2                     xor edx, edx
00449c44  66891d04634900           mov word ptr [0x496304], bx
00449c4b  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
00449c51  e94ffcffff               jmp 0x4498a5
00449c56  31db                     xor ebx, ebx
00449c58  668b9ec0000000           mov bx, word ptr [esi + 0xc0]
00449c5f  81fbffff0000             cmp ebx, 0xffff
00449c65  0f847e030000             je 0x449fe9
00449c6b  89d8                     mov eax, ebx
00449c6d  e87012fdff               call 0x41aee2
00449c72  40                       inc eax
00449c73  668b4e7e                 mov cx, word ptr [esi + 0x7e]
00449c77  89442408                 mov dword ptr [esp + 8], eax
00449c7b  663b4e08                 cmp cx, word ptr [esi + 8]
00449c7f  7407                     je 0x449c88
00449c81  89e8                     mov eax, ebp
00449c83  e9c8fcffff               jmp 0x449950
00449c88  663b4c2408               cmp cx, word ptr [esp + 8]
00449c8d  0f85f1020000             jne 0x449f84
00449c93  8b2c24                   mov ebp, dword ptr [esp]
00449c96  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00449c9b  01e8                     add eax, ebp
00449c9d  8a80da000000             mov al, byte ptr [eax + 0xda]
00449ca3  25ff000000               and eax, 0xff
00449ca8  83f805                   cmp eax, 5
00449cab  0f94c0                   sete al
00449cae  84c0                     test al, al
00449cb0  7446                     je 0x449cf8
00449cb2  31d2                     xor edx, edx
00449cb4  6689fa                   mov dx, di
00449cb7  89d3                     mov ebx, edx
00449cb9  c1e304                   shl ebx, 4
00449cbc  01d3                     add ebx, edx
00449cbe  c1e302                   shl ebx, 2
00449cc1  01d3                     add ebx, edx
00449cc3  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00449cc9  668b849a9a000000         mov ax, word ptr [edx + ebx*4 + 0x9a]
00449cd1  8a549a01                 mov dl, byte ptr [edx + ebx*4 + 1]
00449cd5  81e2ff000000             and edx, 0xff
00449cdb  89d3                     mov ebx, edx
00449cdd  c1e302                   shl ebx, 2
00449ce0  29d3                     sub ebx, edx
00449ce2  c1e303                   shl ebx, 3
00449ce5  01d3                     add ebx, edx
00449ce7  668b145db6654900         mov dx, word ptr [ebx*2 + 0x4965b6]
00449cef  6639d0                   cmp ax, dx
00449cf2  0f8436010000             je 0x449e2e
00449cf8  31c0                     xor eax, eax
00449cfa  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00449d01  e88603fdff               call 0x41a08c
00449d06  3a06                     cmp al, byte ptr [esi]
00449d08  0f8520010000             jne 0x449e2e
00449d0e  31d2                     xor edx, edx
00449d10  6689fa                   mov dx, di
00449d13  89d0                     mov eax, edx
00449d15  c6869000000005           mov byte ptr [esi + 0x90], 5
00449d1c  e878e8ffff               call 0x448599
00449d21  8a8690000000             mov al, byte ptr [esi + 0x90]
00449d27  3a8691000000             cmp al, byte ptr [esi + 0x91]
00449d2d  0f8572fbffff             jne 0x4498a5
00449d33  89d0                     mov eax, edx
00449d35  e80e890200               call 0x472648
00449d3a  f6057c8f500001           test byte ptr [0x508f7c], 1
00449d41  7517                     jne 0x449d5a
00449d43  31c0                     xor eax, eax
00449d45  8a86ab000000             mov al, byte ptr [esi + 0xab]
00449d4b  83f801                   cmp eax, 1
00449d4e  740a                     je 0x449d5a
00449d50  88c1                     mov cl, al
00449d52  fec9                     dec cl
00449d54  888eab000000             mov byte ptr [esi + 0xab], cl
00449d5a  31c9                     xor ecx, ecx
00449d5c  6689f9                   mov cx, di
00449d5f  89cb                     mov ebx, ecx
00449d61  c1e304                   shl ebx, 4
00449d64  01cb                     add ebx, ecx
00449d66  c1e302                   shl ebx, 2
00449d69  01cb                     add ebx, ecx
00449d6b  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00449d70  c1e302                   shl ebx, 2
00449d73  01c3                     add ebx, eax
00449d75  8a4301                   mov al, byte ptr [ebx + 1]
00449d78  3c0b                     cmp al, 0xb
00449d7a  0f82a7000000             jb 0x449e27
00449d80  7612                     jbe 0x449d94
00449d82  3c12                     cmp al, 0x12
00449d84  7256                     jb 0x449ddc
00449d86  760c                     jbe 0x449d94
00449d88  3c17                     cmp al, 0x17
00449d8a  7208                     jb 0x449d94
00449d8c  3c18                     cmp al, 0x18
00449d8e  7604                     jbe 0x449d94
00449d90  3c19                     cmp al, 0x19
00449d92  7554                     jne 0x449de8
00449d94  8aaba9000000             mov ch, byte ptr [ebx + 0xa9]
00449d9a  fec5                     inc ch
00449d9c  8aa3a7000000             mov ah, byte ptr [ebx + 0xa7]
00449da2  88aba9000000             mov byte ptr [ebx + 0xa9], ch
00449da8  38e5                     cmp ch, ah
00449daa  753c                     jne 0x449de8
00449dac  31d2                     xor edx, edx
00449dae  8a93a4000000             mov dl, byte ptr [ebx + 0xa4]
00449db4  31c9                     xor ecx, ecx
00449db6  42                       inc edx
00449db7  8a8ba5000000             mov cl, byte ptr [ebx + 0xa5]
00449dbd  89d0                     mov eax, edx
00449dbf  c1fa1f                   sar edx, 0x1f
00449dc2  f7f9                     idiv ecx
00449dc4  c683a900000000           mov byte ptr [ebx + 0xa9], 0
00449dcb  8893a4000000             mov byte ptr [ebx + 0xa4], dl
00449dd1  eb15                     jmp 0x449de8
00449dd3  89c8                     mov eax, ecx
00449dd5  e855ddffff               call 0x447b2f
00449dda  eb0c                     jmp 0x449de8
00449ddc  3c0e                     cmp al, 0xe
00449dde  72b4                     jb 0x449d94
00449de0  3c0f                     cmp al, 0xf
00449de2  76b0                     jbe 0x449d94
00449de4  3c11                     cmp al, 0x11
00449de6  74eb                     je 0x449dd3
00449de8  31c0                     xor eax, eax
00449dea  8a86ab000000             mov al, byte ptr [esi + 0xab]
00449df0  83f801                   cmp eax, 1
00449df3  0f85acfaffff             jne 0x4498a5
00449df9  31c0                     xor eax, eax
00449dfb  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00449e02  e8b999fdff               call 0x4237c0
00449e07  84c0                     test al, al
00449e09  0f8596faffff             jne 0x4498a5
00449e0f  31d2                     xor edx, edx
00449e11  31c0                     xor eax, eax
00449e13  6689fa                   mov dx, di
00449e16  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00449e1d  e8f4b6fdff               call 0x425516
00449e22  e97efaffff               jmp 0x4498a5
00449e27  3c03                     cmp al, 3
00449e29  e966ffffff               jmp 0x449d94
00449e2e  31d2                     xor edx, edx
00449e30  6689fa                   mov dx, di
00449e33  89d0                     mov eax, edx
00449e35  e80e880200               call 0x472648
00449e3a  31c0                     xor eax, eax
00449e3c  8a86ab000000             mov al, byte ptr [esi + 0xab]
00449e42  83f832                   cmp eax, 0x32
00449e45  741a                     je 0x449e61
00449e47  f6057c8f500001           test byte ptr [0x508f7c], 1
00449e4e  0f858a000000             jne 0x449ede
00449e54  fec0                     inc al
00449e56  8886ab000000             mov byte ptr [esi + 0xab], al
00449e5c  e97d000000               jmp 0x449ede
00449e61  c644241007               mov byte ptr [esp + 0x10], 7
00449e66  89d3                     mov ebx, edx
00449e68  c1e304                   shl ebx, 4
00449e6b  01d3                     add ebx, edx
00449e6d  c1e302                   shl ebx, 2
00449e70  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00449e75  01d3                     add ebx, edx
00449e77  89f9                     mov ecx, edi
00449e79  8a449802                 mov al, byte ptr [eax + ebx*4 + 2]
00449e7d  25ff000000               and eax, 0xff
00449e82  7409                     je 0x449e8d
00449e84  83f804                   cmp eax, 4
00449e87  7404                     je 0x449e8d
00449e89  b001                     mov al, 1
00449e8b  eb02                     jmp 0x449e8f
00449e8d  30c0                     xor al, al
00449e8f  84c0                     test al, al
00449e91  0f8447000000             je 0x449ede
00449e97  31d2                     xor edx, edx
00449e99  6689ca                   mov dx, cx
00449e9c  89d3                     mov ebx, edx
00449e9e  c1e304                   shl ebx, 4
00449ea1  01d3                     add ebx, edx
00449ea3  c1e302                   shl ebx, 2
00449ea6  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00449eab  01d3                     add ebx, edx
00449ead  8a542410                 mov dl, byte ptr [esp + 0x10]
00449eb1  88549802                 mov byte ptr [eax + ebx*4 + 2], dl
00449eb5  663b0d04634900           cmp cx, word ptr [0x496304]
00449ebc  7520                     jne 0x449ede
00449ebe  30ff                     xor bh, bh
00449ec0  31c0                     xor eax, eax
00449ec2  883d360f4e00             mov byte ptr [0x4e0f36], bh
00449ec8  a33c0f4e00               mov dword ptr [0x4e0f3c], eax
00449ecd  b8ffff0000               mov eax, 0xffff
00449ed2  883d370f4e00             mov byte ptr [0x4e0f37], bh
00449ed8  66a304634900             mov word ptr [0x496304], ax
00449ede  31d2                     xor edx, edx
00449ee0  6689fa                   mov dx, di
00449ee3  89d3                     mov ebx, edx
00449ee5  c1e304                   shl ebx, 4
00449ee8  01d3                     add ebx, edx
00449eea  c1e302                   shl ebx, 2
00449eed  01d3                     add ebx, edx
00449eef  8b35a0194e00             mov esi, dword ptr [0x4e19a0]
00449ef5  c1e302                   shl ebx, 2
00449ef8  01de                     add esi, ebx
00449efa  8a4601                   mov al, byte ptr [esi + 1]
00449efd  3c0b                     cmp al, 0xb
00449eff  0f827b000000             jb 0x449f80
00449f05  7616                     jbe 0x449f1d
00449f07  3c12                     cmp al, 0x12
00449f09  7264                     jb 0x449f6f
00449f0b  7610                     jbe 0x449f1d
00449f0d  3c17                     cmp al, 0x17
00449f0f  720c                     jb 0x449f1d
00449f11  3c18                     cmp al, 0x18
00449f13  7608                     jbe 0x449f1d
00449f15  3c19                     cmp al, 0x19
00449f17  0f8588f9ffff             jne 0x4498a5
00449f1d  8aa6a9000000             mov ah, byte ptr [esi + 0xa9]
00449f23  fec4                     inc ah
00449f25  8a96a7000000             mov dl, byte ptr [esi + 0xa7]
00449f2b  88a6a9000000             mov byte ptr [esi + 0xa9], ah
00449f31  38d4                     cmp ah, dl
00449f33  0f856cf9ffff             jne 0x4498a5
00449f39  31d2                     xor edx, edx
00449f3b  8a96a4000000             mov dl, byte ptr [esi + 0xa4]
00449f41  31db                     xor ebx, ebx
00449f43  42                       inc edx
00449f44  8a9ea5000000             mov bl, byte ptr [esi + 0xa5]
00449f4a  89d0                     mov eax, edx
00449f4c  c1fa1f                   sar edx, 0x1f
00449f4f  f7fb                     idiv ebx
00449f51  c686a900000000           mov byte ptr [esi + 0xa9], 0
00449f58  8896a4000000             mov byte ptr [esi + 0xa4], dl
00449f5e  e942f9ffff               jmp 0x4498a5
00449f63  89d0                     mov eax, edx
00449f65  e8c5dbffff               call 0x447b2f
00449f6a  e936f9ffff               jmp 0x4498a5
00449f6f  3c0e                     cmp al, 0xe
00449f71  72aa                     jb 0x449f1d
00449f73  3c0f                     cmp al, 0xf
00449f75  76a6                     jbe 0x449f1d
00449f77  3c11                     cmp al, 0x11
00449f79  74e8                     je 0x449f63
00449f7b  e925f9ffff               jmp 0x4498a5
00449f80  3c03                     cmp al, 3
00449f82  eb99                     jmp 0x449f1d
00449f84  bb02000000               mov ebx, 2
00449f89  89e8                     mov eax, ebp
00449f8b  31d2                     xor edx, edx
00449f8d  31c9                     xor ecx, ecx
00449f8f  668b542408               mov dx, word ptr [esp + 8]
00449f94  e8cf86ffff               call 0x442668
00449f99  84c0                     test al, al
00449f9b  0f8404f9ffff             je 0x4498a5
00449fa1  8b3424                   mov esi, dword ptr [esp]
00449fa4  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00449faa  01f2                     add edx, esi
00449fac  8b442408                 mov eax, dword ptr [esp + 8]
00449fb0  6689427e                 mov word ptr [edx + 0x7e], ax
00449fb4  663b3d04634900           cmp di, word ptr [0x496304]
00449fbb  7520                     jne 0x449fdd
00449fbd  b9ffff0000               mov ecx, 0xffff
00449fc2  30c0                     xor al, al
00449fc4  31ff                     xor edi, edi
00449fc6  a2360f4e00               mov byte ptr [0x4e0f36], al
00449fcb  a2370f4e00               mov byte ptr [0x4e0f37], al
00449fd0  893d3c0f4e00             mov dword ptr [0x4e0f3c], edi
00449fd6  66890d04634900           mov word ptr [0x496304], cx
00449fdd  c6828800000000           mov byte ptr [edx + 0x88], 0
00449fe4  e9bcf8ffff               jmp 0x4498a5
00449fe9  89e8                     mov eax, ebp
00449feb  e858860200               call 0x472648
00449ff0  31c0                     xor eax, eax
00449ff2  8a86ab000000             mov al, byte ptr [esi + 0xab]
00449ff8  83f832                   cmp eax, 0x32
00449ffb  741c                     je 0x44a019
00449ffd  f6057c8f500001           test byte ptr [0x508f7c], 1
0044a004  0f8587000000             jne 0x44a091
0044a00a  88c7                     mov bh, al
0044a00c  fec7                     inc bh
0044a00e  88beab000000             mov byte ptr [esi + 0xab], bh
0044a014  e978000000               jmp 0x44a091
0044a019  b407                     mov ah, 7
0044a01b  8b1c24                   mov ebx, dword ptr [esp]
0044a01e  88642414                 mov byte ptr [esp + 0x14], ah
0044a022  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044a027  01d8                     add eax, ebx
0044a029  89f9                     mov ecx, edi
0044a02b  8a4002                   mov al, byte ptr [eax + 2]
0044a02e  25ff000000               and eax, 0xff
0044a033  7409                     je 0x44a03e
0044a035  83f804                   cmp eax, 4
0044a038  7404                     je 0x44a03e
0044a03a  b001                     mov al, 1
0044a03c  eb02                     jmp 0x44a040
0044a03e  30c0                     xor al, al
0044a040  84c0                     test al, al
0044a042  0f8449000000             je 0x44a091
0044a048  31d2                     xor edx, edx
0044a04a  6689ca                   mov dx, cx
0044a04d  89d3                     mov ebx, edx
0044a04f  c1e304                   shl ebx, 4
0044a052  01d3                     add ebx, edx
0044a054  c1e302                   shl ebx, 2
0044a057  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044a05c  01d3                     add ebx, edx
0044a05e  8a542414                 mov dl, byte ptr [esp + 0x14]
0044a062  88549802                 mov byte ptr [eax + ebx*4 + 2], dl
0044a066  663b0d04634900           cmp cx, word ptr [0x496304]
0044a06d  7522                     jne 0x44a091
0044a06f  bbffff0000               mov ebx, 0xffff
0044a074  30d2                     xor dl, dl
0044a076  31c9                     xor ecx, ecx
0044a078  8815360f4e00             mov byte ptr [0x4e0f36], dl
0044a07e  8815370f4e00             mov byte ptr [0x4e0f37], dl
0044a084  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044a08a  66891d04634900           mov word ptr [0x496304], bx
0044a091  31c9                     xor ecx, ecx
0044a093  6689f9                   mov cx, di
0044a096  89cb                     mov ebx, ecx
0044a098  c1e304                   shl ebx, 4
0044a09b  01cb                     add ebx, ecx
0044a09d  c1e302                   shl ebx, 2
0044a0a0  01cb                     add ebx, ecx
0044a0a2  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044a0a7  c1e302                   shl ebx, 2
0044a0aa  01c3                     add ebx, eax
0044a0ac  8a4301                   mov al, byte ptr [ebx + 1]
0044a0af  3c0b                     cmp al, 0xb
0044a0b1  0f8274000000             jb 0x44a12b
0044a0b7  7616                     jbe 0x44a0cf
0044a0b9  3c12                     cmp al, 0x12
0044a0bb  725d                     jb 0x44a11a
0044a0bd  7610                     jbe 0x44a0cf
0044a0bf  3c17                     cmp al, 0x17
0044a0c1  720c                     jb 0x44a0cf
0044a0c3  3c18                     cmp al, 0x18
0044a0c5  7608                     jbe 0x44a0cf
0044a0c7  3c19                     cmp al, 0x19
0044a0c9  0f85d6f7ffff             jne 0x4498a5
0044a0cf  8a8ba9000000             mov cl, byte ptr [ebx + 0xa9]
0044a0d5  fec1                     inc cl
0044a0d7  888ba9000000             mov byte ptr [ebx + 0xa9], cl
0044a0dd  3a8ba7000000             cmp cl, byte ptr [ebx + 0xa7]
0044a0e3  0f85bcf7ffff             jne 0x4498a5
0044a0e9  31d2                     xor edx, edx
0044a0eb  8a93a4000000             mov dl, byte ptr [ebx + 0xa4]
0044a0f1  31c9                     xor ecx, ecx
0044a0f3  42                       inc edx
0044a0f4  8a8ba5000000             mov cl, byte ptr [ebx + 0xa5]
0044a0fa  89d0                     mov eax, edx
0044a0fc  c1fa1f                   sar edx, 0x1f
0044a0ff  f7f9                     idiv ecx
0044a101  c683a900000000           mov byte ptr [ebx + 0xa9], 0
0044a108  8893a4000000             mov byte ptr [ebx + 0xa4], dl
0044a10e  e992f7ffff               jmp 0x4498a5
0044a113  89c8                     mov eax, ecx
0044a115  e94bfeffff               jmp 0x449f65
0044a11a  3c0e                     cmp al, 0xe
0044a11c  72b1                     jb 0x44a0cf
0044a11e  3c0f                     cmp al, 0xf
0044a120  76ad                     jbe 0x44a0cf
0044a122  3c11                     cmp al, 0x11
0044a124  74ed                     je 0x44a113
0044a126  e97af7ffff               jmp 0x4498a5
0044a12b  3c03                     cmp al, 3
0044a12d  eba0                     jmp 0x44a0cf
0044a12f  31c0                     xor eax, eax
0044a131  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044a138  3dffff0000               cmp eax, 0xffff
0044a13d  0f8462f7ffff             je 0x4498a5
0044a143  668b4608                 mov ax, word ptr [esi + 8]
0044a147  668b567e                 mov dx, word ptr [esi + 0x7e]
0044a14b  6639d0                   cmp ax, dx
0044a14e  0f85f7f7ffff             jne 0x44994b
0044a154  668b9eb2000000           mov bx, word ptr [esi + 0xb2]
0044a15b  6639da                   cmp dx, bx
0044a15e  0f850e010000             jne 0x44a272
0044a164  31db                     xor ebx, ebx
0044a166  6689fb                   mov bx, di
0044a169  89d8                     mov eax, ebx
0044a16b  c6869000000005           mov byte ptr [esi + 0x90], 5
0044a172  e822e4ffff               call 0x448599
0044a177  8a8690000000             mov al, byte ptr [esi + 0x90]
0044a17d  3a8691000000             cmp al, byte ptr [esi + 0x91]
0044a183  0f851cf7ffff             jne 0x4498a5
0044a189  31c0                     xor eax, eax
0044a18b  ba01000000               mov edx, 1
0044a190  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044a197  e8c004fdff               call 0x41a65c
0044a19c  31c0                     xor eax, eax
0044a19e  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044a1a5  e86f6afdff               call 0x420c19
0044a1aa  84c0                     test al, al
0044a1ac  0f84f3f6ffff             je 0x4498a5
0044a1b2  31c0                     xor eax, eax
0044a1b4  89da                     mov edx, ebx
0044a1b6  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044a1bd  e854b3fdff               call 0x425516
0044a1c2  84c0                     test al, al
0044a1c4  742d                     je 0x44a1f3
0044a1c6  89d8                     mov eax, ebx
0044a1c8  e88bce0000               call 0x457058
0044a1cd  31c0                     xor eax, eax
0044a1cf  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044a1d6  e8070dfdff               call 0x41aee2
0044a1db  6689467c                 mov word ptr [esi + 0x7c], ax
0044a1df  66894608                 mov word ptr [esi + 8], ax
0044a1e3  89d8                     mov eax, ebx
0044a1e5  c646020e                 mov byte ptr [esi + 2], 0xe
0044a1e9  e85a840200               call 0x472648
0044a1ee  e9b2f6ffff               jmp 0x4498a5
0044a1f3  89d8                     mov eax, ebx
0044a1f5  c1e304                   shl ebx, 4
0044a1f8  01c3                     add ebx, eax
0044a1fa  c1e302                   shl ebx, 2
0044a1fd  01c3                     add ebx, eax
0044a1ff  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044a204  b107                     mov cl, 7
0044a206  8a449802                 mov al, byte ptr [eax + ebx*4 + 2]
0044a20a  25ff000000               and eax, 0xff
0044a20f  7409                     je 0x44a21a
0044a211  83f804                   cmp eax, 4
0044a214  7404                     je 0x44a21a
0044a216  b001                     mov al, 1
0044a218  eb02                     jmp 0x44a21c
0044a21a  30c0                     xor al, al
0044a21c  84c0                     test al, al
0044a21e  0f8481f6ffff             je 0x4498a5
0044a224  31d2                     xor edx, edx
0044a226  6689fa                   mov dx, di
0044a229  89d3                     mov ebx, edx
0044a22b  c1e304                   shl ebx, 4
0044a22e  01d3                     add ebx, edx
0044a230  c1e302                   shl ebx, 2
0044a233  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044a238  01d3                     add ebx, edx
0044a23a  884c9802                 mov byte ptr [eax + ebx*4 + 2], cl
0044a23e  663b3d04634900           cmp di, word ptr [0x496304]
0044a245  0f855af6ffff             jne 0x4498a5
0044a24b  30ed                     xor ch, ch
0044a24d  baffff0000               mov edx, 0xffff
0044a252  882d360f4e00             mov byte ptr [0x4e0f36], ch
0044a258  882d370f4e00             mov byte ptr [0x4e0f37], ch
0044a25e  31c9                     xor ecx, ecx
0044a260  66891504634900           mov word ptr [0x496304], dx
0044a267  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044a26d  e933f6ffff               jmp 0x4498a5
0044a272  0fb7ef                   movzx ebp, di
0044a275  31d2                     xor edx, edx
0044a277  31c9                     xor ecx, ecx
0044a279  6689da                   mov dx, bx
0044a27c  89e8                     mov eax, ebp
0044a27e  bb01000000               mov ebx, 1
0044a283  e8e083ffff               call 0x442668
0044a288  84c0                     test al, al
0044a28a  0f8415f6ffff             je 0x4498a5
0044a290  89eb                     mov ebx, ebp
0044a292  c1e304                   shl ebx, 4
0044a295  01eb                     add ebx, ebp
0044a297  c1e302                   shl ebx, 2
0044a29a  01eb                     add ebx, ebp
0044a29c  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044a2a2  c1e302                   shl ebx, 2
0044a2a5  01da                     add edx, ebx
0044a2a7  668b86b2000000           mov ax, word ptr [esi + 0xb2]
0044a2ae  6689427e                 mov word ptr [edx + 0x7e], ax
0044a2b2  663b3d04634900           cmp di, word ptr [0x496304]
0044a2b9  0f851efdffff             jne 0x449fdd
0044a2bf  30db                     xor bl, bl
0044a2c1  beffff0000               mov esi, 0xffff
0044a2c6  881d360f4e00             mov byte ptr [0x4e0f36], bl
0044a2cc  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044a2d2  31db                     xor ebx, ebx
0044a2d4  66893504634900           mov word ptr [0x496304], si
0044a2db  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
0044a2e1  e9f7fcffff               jmp 0x449fdd
0044a2e6  3c02                     cmp al, 2
0044a2e8  e97cf4ffff               jmp 0x449769
