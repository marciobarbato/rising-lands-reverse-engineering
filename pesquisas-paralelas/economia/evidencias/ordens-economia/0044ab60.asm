; CalculConstruireBatiment; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044ab60  53                       push ebx
0044ab61  51                       push ecx
0044ab62  52                       push edx
0044ab63  56                       push esi
0044ab64  57                       push edi
0044ab65  55                       push ebp
0044ab66  83ec04                   sub esp, 4
0044ab69  89c7                     mov edi, eax
0044ab6b  31d2                     xor edx, edx
0044ab6d  6689c2                   mov dx, ax
0044ab70  89d0                     mov eax, edx
0044ab72  c1e004                   shl eax, 4
0044ab75  01d0                     add eax, edx
0044ab77  c1e002                   shl eax, 2
0044ab7a  8d1c02                   lea ebx, [edx + eax]
0044ab7d  8b35a0194e00             mov esi, dword ptr [0x4e19a0]
0044ab83  c1e302                   shl ebx, 2
0044ab86  01de                     add esi, ebx
0044ab88  31c0                     xor eax, eax
0044ab8a  8a4601                   mov al, byte ptr [esi + 1]
0044ab8d  83f807                   cmp eax, 7
0044ab90  0f84e4090000             je 0x44b57a
0044ab96  e9a7070000               jmp 0x44b342
0044ab9b  31c0                     xor eax, eax
0044ab9d  8a4602                   mov al, byte ptr [esi + 2]
0044aba0  83f80b                   cmp eax, 0xb
0044aba3  0f85ab050000             jne 0x44b154
0044aba9  31c0                     xor eax, eax
0044abab  8a86be000000             mov al, byte ptr [esi + 0xbe]
0044abb1  83f809                   cmp eax, 9
0044abb4  7409                     je 0x44abbf
0044abb6  83f80c                   cmp eax, 0xc
0044abb9  0f859c000000             jne 0x44ac5b
0044abbf  668b4608                 mov ax, word ptr [esi + 8]
0044abc3  663b86b2000000           cmp ax, word ptr [esi + 0xb2]
0044abca  0f858b000000             jne 0x44ac5b
0044abd0  8b8683000000             mov eax, dword ptr [esi + 0x83]
0044abd6  c1f818                   sar eax, 0x18
0044abd9  85c0                     test eax, eax
0044abdb  0f857a000000             jne 0x44ac5b
0044abe1  8b8684000000             mov eax, dword ptr [esi + 0x84]
0044abe7  c1f818                   sar eax, 0x18
0044abea  85c0                     test eax, eax
0044abec  756d                     jne 0x44ac5b
0044abee  31c9                     xor ecx, ecx
0044abf0  31d2                     xor edx, edx
0044abf2  6689f9                   mov cx, di
0044abf5  668b5608                 mov dx, word ptr [esi + 8]
0044abf9  89c8                     mov eax, ecx
0044abfb  e82ea5ffff               call 0x44512e
0044ac00  89c3                     mov ebx, eax
0044ac02  31c0                     xor eax, eax
0044ac04  6689d8                   mov ax, bx
0044ac07  3dffff0000               cmp eax, 0xffff
0044ac0c  744d                     je 0x44ac5b
0044ac0e  89c8                     mov eax, ecx
0044ac10  c1e004                   shl eax, 4
0044ac13  01c8                     add eax, ecx
0044ac15  c1e002                   shl eax, 2
0044ac18  01c8                     add eax, ecx
0044ac1a  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044ac20  c1e002                   shl eax, 2
0044ac23  01d0                     add eax, edx
0044ac25  6689587e                 mov word ptr [eax + 0x7e], bx
0044ac29  663b3d04634900           cmp di, word ptr [0x496304]
0044ac30  7522                     jne 0x44ac54
0044ac32  b9ffff0000               mov ecx, 0xffff
0044ac37  30d2                     xor dl, dl
0044ac39  31ed                     xor ebp, ebp
0044ac3b  8815360f4e00             mov byte ptr [0x4e0f36], dl
0044ac41  8815370f4e00             mov byte ptr [0x4e0f37], dl
0044ac47  892d3c0f4e00             mov dword ptr [0x4e0f3c], ebp
0044ac4d  66890d04634900           mov word ptr [0x496304], cx
0044ac54  c6808800000000           mov byte ptr [eax + 0x88], 0
0044ac5b  668b467e                 mov ax, word ptr [esi + 0x7e]
0044ac5f  663b4608                 cmp ax, word ptr [esi + 8]
0044ac63  7412                     je 0x44ac77
0044ac65  31c0                     xor eax, eax
0044ac67  8a86be000000             mov al, byte ptr [esi + 0xbe]
0044ac6d  83f809                   cmp eax, 9
0044ac70  7405                     je 0x44ac77
0044ac72  83f80c                   cmp eax, 0xc
0044ac75  754f                     jne 0x44acc6
0044ac77  31c0                     xor eax, eax
0044ac79  8a86be000000             mov al, byte ptr [esi + 0xbe]
0044ac7f  83f809                   cmp eax, 9
0044ac82  7405                     je 0x44ac89
0044ac84  83f80c                   cmp eax, 0xc
0044ac87  7523                     jne 0x44acac
0044ac89  668b4608                 mov ax, word ptr [esi + 8]
0044ac8d  668b9eb2000000           mov bx, word ptr [esi + 0xb2]
0044ac94  6639d8                   cmp ax, bx
0044ac97  742d                     je 0x44acc6
0044ac99  31d2                     xor edx, edx
0044ac9b  31c0                     xor eax, eax
0044ac9d  6689da                   mov dx, bx
0044aca0  6689f8                   mov ax, di
0044aca3  e8f9baffff               call 0x4467a1
0044aca8  84c0                     test al, al
0044acaa  741a                     je 0x44acc6
0044acac  8b8683000000             mov eax, dword ptr [esi + 0x83]
0044acb2  c1f818                   sar eax, 0x18
0044acb5  85c0                     test eax, eax
0044acb7  750d                     jne 0x44acc6
0044acb9  8b8684000000             mov eax, dword ptr [esi + 0x84]
0044acbf  c1f818                   sar eax, 0x18
0044acc2  85c0                     test eax, eax
0044acc4  740f                     je 0x44acd5
0044acc6  31c0                     xor eax, eax
0044acc8  6689f8                   mov ax, di
0044accb  e83ce6ffff               call 0x44930c
0044acd0  e96d060000               jmp 0x44b342
0044acd5  668b4608                 mov ax, word ptr [esi + 8]
0044acd9  663b86b2000000           cmp ax, word ptr [esi + 0xb2]
0044ace0  7431                     je 0x44ad13
0044ace2  31c0                     xor eax, eax
0044ace4  8a86be000000             mov al, byte ptr [esi + 0xbe]
0044acea  83f809                   cmp eax, 9
0044aced  7409                     je 0x44acf8
0044acef  83f80c                   cmp eax, 0xc
0044acf2  0f85db020000             jne 0x44afd3
0044acf8  31c0                     xor eax, eax
0044acfa  31d2                     xor edx, edx
0044acfc  6689f8                   mov ax, di
0044acff  668b96b2000000           mov dx, word ptr [esi + 0xb2]
0044ad06  e896baffff               call 0x4467a1
0044ad0b  84c0                     test al, al
0044ad0d  0f84c0020000             je 0x44afd3
0044ad13  31c0                     xor eax, eax
0044ad15  8a86be000000             mov al, byte ptr [esi + 0xbe]
0044ad1b  3dff000000               cmp eax, 0xff
0044ad20  0f841c060000             je 0x44b342
0044ad26  83f809                   cmp eax, 9
0044ad29  7415                     je 0x44ad40
0044ad2b  83f80c                   cmp eax, 0xc
0044ad2e  7410                     je 0x44ad40
0044ad30  e86f01fdff               call 0x41aea4
0044ad35  668b5608                 mov dx, word ptr [esi + 8]
0044ad39  01c2                     add edx, eax
0044ad3b  891424                   mov dword ptr [esp], edx
0044ad3e  eb0a                     jmp 0x44ad4a
0044ad40  668b86b2000000           mov ax, word ptr [esi + 0xb2]
0044ad47  890424                   mov dword ptr [esp], eax
0044ad4a  0fb7ef                   movzx ebp, di
0044ad4d  31c9                     xor ecx, ecx
0044ad4f  31c0                     xor eax, eax
0044ad51  668b0c24                 mov cx, word ptr [esp]
0044ad55  89eb                     mov ebx, ebp
0044ad57  8a86be000000             mov al, byte ptr [esi + 0xbe]
0044ad5d  89ca                     mov edx, ecx
0044ad5f  e8ae4dfdff               call 0x41fb12
0044ad64  89ea                     mov edx, ebp
0044ad66  c1e504                   shl ebp, 4
0044ad69  01d5                     add ebp, edx
0044ad6b  c1e502                   shl ebp, 2
0044ad6e  01d5                     add ebp, edx
0044ad70  c1e502                   shl ebp, 2
0044ad73  84c0                     test al, al
0044ad75  0f8402010000             je 0x44ae7d
0044ad7b  89c8                     mov eax, ecx
0044ad7d  31db                     xor ebx, ebx
0044ad7f  31d2                     xor edx, edx
0044ad81  8a1e                     mov bl, byte ptr [esi]
0044ad83  8a96be000000             mov dl, byte ptr [esi + 0xbe]
0044ad89  e81451fdff               call 0x41fea2
0044ad8e  668986c0000000           mov word ptr [esi + 0xc0], ax
0044ad95  31c0                     xor eax, eax
0044ad97  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044ad9e  3dffff0000               cmp eax, 0xffff
0044ada3  7467                     je 0x44ae0c
0044ada5  c6868900000001           mov byte ptr [esi + 0x89], 1
0044adac  c6868b00000014           mov byte ptr [esi + 0x8b], 0x14
0044adb3  c686a900000000           mov byte ptr [esi + 0xa9], 0
0044adba  31c0                     xor eax, eax
0044adbc  8a86be000000             mov al, byte ptr [esi + 0xbe]
0044adc2  c686a400000000           mov byte ptr [esi + 0xa4], 0
0044adc9  83f811                   cmp eax, 0x11
0044adcc  750c                     jne 0x44adda
0044adce  c6869000000007           mov byte ptr [esi + 0x90], 7
0044add5  e968050000               jmp 0x44b342
0044adda  83f809                   cmp eax, 9
0044addd  7405                     je 0x44ade4
0044addf  83f80c                   cmp eax, 0xc
0044ade2  751c                     jne 0x44ae00
0044ade4  31d2                     xor edx, edx
0044ade6  31c0                     xor eax, eax
0044ade8  668b1424                 mov dx, word ptr [esp]
0044adec  668b4608                 mov ax, word ptr [esi + 8]
0044adf0  e84dc20200               call 0x477042
0044adf5  888690000000             mov byte ptr [esi + 0x90], al
0044adfb  e942050000               jmp 0x44b342
0044ae00  c6869000000003           mov byte ptr [esi + 0x90], 3
0044ae07  e936050000               jmp 0x44b342
0044ae0c  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044ae11  01c5                     add ebp, eax
0044ae13  31c0                     xor eax, eax
0044ae15  8a4502                   mov al, byte ptr [ebp + 2]
0044ae18  b307                     mov bl, 7
0044ae1a  85c0                     test eax, eax
0044ae1c  7409                     je 0x44ae27
0044ae1e  83f804                   cmp eax, 4
0044ae21  7404                     je 0x44ae27
0044ae23  b001                     mov al, 1
0044ae25  eb02                     jmp 0x44ae29
0044ae27  30c0                     xor al, al
0044ae29  84c0                     test al, al
0044ae2b  0f8411050000             je 0x44b342
0044ae31  31d2                     xor edx, edx
0044ae33  6689fa                   mov dx, di
0044ae36  89d0                     mov eax, edx
0044ae38  c1e004                   shl eax, 4
0044ae3b  01d0                     add eax, edx
0044ae3d  c1e002                   shl eax, 2
0044ae40  01d0                     add eax, edx
0044ae42  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044ae48  885c8202                 mov byte ptr [edx + eax*4 + 2], bl
0044ae4c  663b3d04634900           cmp di, word ptr [0x496304]
0044ae53  0f85e9040000             jne 0x44b342
0044ae59  30c0                     xor al, al
0044ae5b  baffff0000               mov edx, 0xffff
0044ae60  a2360f4e00               mov byte ptr [0x4e0f36], al
0044ae65  a2370f4e00               mov byte ptr [0x4e0f37], al
0044ae6a  31c0                     xor eax, eax
0044ae6c  66891504634900           mov word ptr [0x496304], dx
0044ae73  a33c0f4e00               mov dword ptr [0x4e0f3c], eax
0044ae78  e9c5040000               jmp 0x44b342
0044ae7d  31c0                     xor eax, eax
0044ae7f  8a86be000000             mov al, byte ptr [esi + 0xbe]
0044ae85  83f809                   cmp eax, 9
0044ae88  0f85b4040000             jne 0x44b342
0044ae8e  31c0                     xor eax, eax
0044ae90  668b86d8000000           mov ax, word ptr [esi + 0xd8]
0044ae97  85c0                     test eax, eax
0044ae99  0f84a3000000             je 0x44af42
0044ae9f  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044aea4  01e8                     add eax, ebp
0044aea6  668b98c4000000           mov bx, word ptr [eax + 0xc4]
0044aead  6689587e                 mov word ptr [eax + 0x7e], bx
0044aeb1  668b0d04634900           mov cx, word ptr [0x496304]
0044aeb8  89c2                     mov edx, eax
0044aeba  6639cf                   cmp di, cx
0044aebd  7522                     jne 0x44aee1
0044aebf  beffff0000               mov esi, 0xffff
0044aec4  30c9                     xor cl, cl
0044aec6  31ed                     xor ebp, ebp
0044aec8  880d360f4e00             mov byte ptr [0x4e0f36], cl
0044aece  880d370f4e00             mov byte ptr [0x4e0f37], cl
0044aed4  892d3c0f4e00             mov dword ptr [0x4e0f3c], ebp
0044aeda  66893504634900           mov word ptr [0x496304], si
0044aee1  c6828800000000           mov byte ptr [edx + 0x88], 0
0044aee8  c6808800000000           mov byte ptr [eax + 0x88], 0
0044aeef  c6808900000000           mov byte ptr [eax + 0x89], 0
0044aef6  66c780c0000000ffff       mov word ptr [eax + 0xc0], 0xffff
0044aeff  c640020b                 mov byte ptr [eax + 2], 0xb
0044af03  668998b2000000           mov word ptr [eax + 0xb2], bx
0044af0a  bb01000000               mov ebx, 1
0044af0f  eb16                     jmp 0x44af27
0044af11  31d2                     xor edx, edx
0044af13  6689da                   mov dx, bx
0044af16  668bb450c4000000         mov si, word ptr [eax + edx*2 + 0xc4]
0044af1e  43                       inc ebx
0044af1f  6689b450c2000000         mov word ptr [eax + edx*2 + 0xc2], si
0044af27  668b88d8000000           mov cx, word ptr [eax + 0xd8]
0044af2e  6639cb                   cmp bx, cx
0044af31  72de                     jb 0x44af11
0044af33  89ce                     mov esi, ecx
0044af35  4e                       dec esi
0044af36  6689b0d8000000           mov word ptr [eax + 0xd8], si
0044af3d  e900040000               jmp 0x44b342
0044af42  c686be000000ff           mov byte ptr [esi + 0xbe], 0xff
0044af49  66c786b2000000ffff       mov word ptr [esi + 0xb2], 0xffff
0044af52  66c786c0000000ffff       mov word ptr [esi + 0xc0], 0xffff
0044af5b  c6868900000000           mov byte ptr [esi + 0x89], 0
0044af62  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044af67  01c5                     add ebp, eax
0044af69  31c0                     xor eax, eax
0044af6b  8a4502                   mov al, byte ptr [ebp + 2]
0044af6e  b307                     mov bl, 7
0044af70  85c0                     test eax, eax
0044af72  7409                     je 0x44af7d
0044af74  83f804                   cmp eax, 4
0044af77  7404                     je 0x44af7d
0044af79  b001                     mov al, 1
0044af7b  eb02                     jmp 0x44af7f
0044af7d  30c0                     xor al, al
0044af7f  84c0                     test al, al
0044af81  7444                     je 0x44afc7
0044af83  31d2                     xor edx, edx
0044af85  6689fa                   mov dx, di
0044af88  89d0                     mov eax, edx
0044af8a  c1e004                   shl eax, 4
0044af8d  01d0                     add eax, edx
0044af8f  c1e002                   shl eax, 2
0044af92  01d0                     add eax, edx
0044af94  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044af9a  885c8202                 mov byte ptr [edx + eax*4 + 2], bl
0044af9e  663b3d04634900           cmp di, word ptr [0x496304]
0044afa5  7520                     jne 0x44afc7
0044afa7  baffff0000               mov edx, 0xffff
0044afac  30c0                     xor al, al
0044afae  31ff                     xor edi, edi
0044afb0  a2360f4e00               mov byte ptr [0x4e0f36], al
0044afb5  a2370f4e00               mov byte ptr [0x4e0f37], al
0044afba  893d3c0f4e00             mov dword ptr [0x4e0f3c], edi
0044afc0  66891504634900           mov word ptr [0x496304], dx
0044afc7  c6868800000000           mov byte ptr [esi + 0x88], 0
0044afce  e96f030000               jmp 0x44b342
0044afd3  31c0                     xor eax, eax
0044afd5  8a86be000000             mov al, byte ptr [esi + 0xbe]
0044afdb  83f809                   cmp eax, 9
0044afde  0f85c8000000             jne 0x44b0ac
0044afe4  31c0                     xor eax, eax
0044afe6  668b86d8000000           mov ax, word ptr [esi + 0xd8]
0044afed  85c0                     test eax, eax
0044afef  0f84b7000000             je 0x44b0ac
0044aff5  31d2                     xor edx, edx
0044aff7  6689fa                   mov dx, di
0044affa  89d0                     mov eax, edx
0044affc  c1e004                   shl eax, 4
0044afff  01d0                     add eax, edx
0044b001  c1e002                   shl eax, 2
0044b004  01c2                     add edx, eax
0044b006  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044b00b  c1e202                   shl edx, 2
0044b00e  01d0                     add eax, edx
0044b010  668b98c4000000           mov bx, word ptr [eax + 0xc4]
0044b017  6689587e                 mov word ptr [eax + 0x7e], bx
0044b01b  668b0d04634900           mov cx, word ptr [0x496304]
0044b022  89c2                     mov edx, eax
0044b024  6639cf                   cmp di, cx
0044b027  7522                     jne 0x44b04b
0044b029  30c9                     xor cl, cl
0044b02b  beffff0000               mov esi, 0xffff
0044b030  880d360f4e00             mov byte ptr [0x4e0f36], cl
0044b036  880d370f4e00             mov byte ptr [0x4e0f37], cl
0044b03c  31c9                     xor ecx, ecx
0044b03e  66893504634900           mov word ptr [0x496304], si
0044b045  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044b04b  c6828800000000           mov byte ptr [edx + 0x88], 0
0044b052  c6808800000000           mov byte ptr [eax + 0x88], 0
0044b059  c6808900000000           mov byte ptr [eax + 0x89], 0
0044b060  66c780c0000000ffff       mov word ptr [eax + 0xc0], 0xffff
0044b069  c640020b                 mov byte ptr [eax + 2], 0xb
0044b06d  ba01000000               mov edx, 1
0044b072  668998b2000000           mov word ptr [eax + 0xb2], bx
0044b079  eb16                     jmp 0x44b091
0044b07b  31f6                     xor esi, esi
0044b07d  6689d6                   mov si, dx
0044b080  668b9c70c4000000         mov bx, word ptr [eax + esi*2 + 0xc4]
0044b088  42                       inc edx
0044b089  66899c70c2000000         mov word ptr [eax + esi*2 + 0xc2], bx
0044b091  668bb8d8000000           mov di, word ptr [eax + 0xd8]
0044b098  6639fa                   cmp dx, di
0044b09b  72de                     jb 0x44b07b
0044b09d  89fa                     mov edx, edi
0044b09f  4a                       dec edx
0044b0a0  668990d8000000           mov word ptr [eax + 0xd8], dx
0044b0a7  e996020000               jmp 0x44b342
0044b0ac  31d2                     xor edx, edx
0044b0ae  6689fa                   mov dx, di
0044b0b1  b107                     mov cl, 7
0044b0b3  89d0                     mov eax, edx
0044b0b5  c686be000000ff           mov byte ptr [esi + 0xbe], 0xff
0044b0bc  c1e004                   shl eax, 4
0044b0bf  66c786b2000000ffff       mov word ptr [esi + 0xb2], 0xffff
0044b0c8  01d0                     add eax, edx
0044b0ca  66c786c0000000ffff       mov word ptr [esi + 0xc0], 0xffff
0044b0d3  c1e002                   shl eax, 2
0044b0d6  c6868900000000           mov byte ptr [esi + 0x89], 0
0044b0dd  01c2                     add edx, eax
0044b0df  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044b0e4  c1e202                   shl edx, 2
0044b0e7  89fb                     mov ebx, edi
0044b0e9  8a440202                 mov al, byte ptr [edx + eax + 2]
0044b0ed  25ff000000               and eax, 0xff
0044b0f2  7409                     je 0x44b0fd
0044b0f4  83f804                   cmp eax, 4
0044b0f7  7404                     je 0x44b0fd
0044b0f9  b001                     mov al, 1
0044b0fb  eb02                     jmp 0x44b0ff
0044b0fd  30c0                     xor al, al
0044b0ff  84c0                     test al, al
0044b101  0f84c0feffff             je 0x44afc7
0044b107  31d2                     xor edx, edx
0044b109  6689da                   mov dx, bx
0044b10c  89d0                     mov eax, edx
0044b10e  c1e004                   shl eax, 4
0044b111  01d0                     add eax, edx
0044b113  c1e002                   shl eax, 2
0044b116  01d0                     add eax, edx
0044b118  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044b11e  884c8202                 mov byte ptr [edx + eax*4 + 2], cl
0044b122  663b1d04634900           cmp bx, word ptr [0x496304]
0044b129  0f8598feffff             jne 0x44afc7
0044b12f  30db                     xor bl, bl
0044b131  31c0                     xor eax, eax
0044b133  881d360f4e00             mov byte ptr [0x4e0f36], bl
0044b139  a33c0f4e00               mov dword ptr [0x4e0f3c], eax
0044b13e  b8ffff0000               mov eax, 0xffff
0044b143  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044b149  66a304634900             mov word ptr [0x496304], ax
0044b14f  e973feffff               jmp 0x44afc7
0044b154  83f80f                   cmp eax, 0xf
0044b157  0f85e5010000             jne 0x44b342
0044b15d  8b8683000000             mov eax, dword ptr [esi + 0x83]
0044b163  c1f818                   sar eax, 0x18
0044b166  85c0                     test eax, eax
0044b168  0f8558fbffff             jne 0x44acc6
0044b16e  8b8684000000             mov eax, dword ptr [esi + 0x84]
0044b174  c1f818                   sar eax, 0x18
0044b177  85c0                     test eax, eax
0044b179  0f8547fbffff             jne 0x44acc6
0044b17f  31d2                     xor edx, edx
0044b181  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044b188  668b5608                 mov dx, word ptr [esi + 8]
0044b18c  e88e86fdff               call 0x42381f
0044b191  84c0                     test al, al
0044b193  0f842dfbffff             je 0x44acc6
0044b199  c6868900000001           mov byte ptr [esi + 0x89], 1
0044b1a0  c6868b00000032           mov byte ptr [esi + 0x8b], 0x32
0044b1a7  31c0                     xor eax, eax
0044b1a9  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044b1b0  31d2                     xor edx, edx
0044b1b2  e82bfdfcff               call 0x41aee2
0044b1b7  6689c2                   mov dx, ax
0044b1ba  31c0                     xor eax, eax
0044b1bc  e92bfcffff               jmp 0x44adec
0044b1c1  8a8690000000             mov al, byte ptr [esi + 0x90]
0044b1c7  3a8691000000             cmp al, byte ptr [esi + 0x91]
0044b1cd  740c                     je 0x44b1db
0044b1cf  89d0                     mov eax, edx
0044b1d1  e8c3d3ffff               call 0x448599
0044b1d6  e967010000               jmp 0x44b342
0044b1db  89d0                     mov eax, edx
0044b1dd  e830ccffff               call 0x447e12
0044b1e2  31c0                     xor eax, eax
0044b1e4  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044b1eb  e86214fdff               call 0x41c652
0044b1f0  84c0                     test al, al
0044b1f2  7417                     je 0x44b20b
0044b1f4  31c0                     xor eax, eax
0044b1f6  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044b1fd  e874f7fcff               call 0x41a976
0044b202  6685c0                   test ax, ax
0044b205  0f843f010000             je 0x44b34a
0044b20b  31c0                     xor eax, eax
0044b20d  8a868b000000             mov al, byte ptr [esi + 0x8b]
0044b213  85c0                     test eax, eax
0044b215  740a                     je 0x44b221
0044b217  88c5                     mov ch, al
0044b219  fecd                     dec ch
0044b21b  88ae8b000000             mov byte ptr [esi + 0x8b], ch
0044b221  31c0                     xor eax, eax
0044b223  8a868b000000             mov al, byte ptr [esi + 0x8b]
0044b229  85c0                     test eax, eax
0044b22b  0f8511010000             jne 0x44b342
0044b231  8a86a4000000             mov al, byte ptr [esi + 0xa4]
0044b237  83f802                   cmp eax, 2
0044b23a  0f8502010000             jne 0x44b342
0044b240  31d2                     xor edx, edx
0044b242  31c0                     xor eax, eax
0044b244  8a9691000000             mov dl, byte ptr [esi + 0x91]
0044b24a  668b4608                 mov ax, word ptr [esi + 8]
0044b24e  e89bbe0200               call 0x4770ee
0044b253  89c2                     mov edx, eax
0044b255  b817000000               mov eax, 0x17
0044b25a  e87d520200               call 0x4704dc
0044b25f  a801                     test al, 1
0044b261  7511                     jne 0x44b274
0044b263  6a00                     push 0
0044b265  6a00                     push 0
0044b267  6a00                     push 0
0044b269  6a00                     push 0
0044b26b  6a00                     push 0
0044b26d  b80f000000               mov eax, 0xf
0044b272  eb0f                     jmp 0x44b283
0044b274  6a00                     push 0
0044b276  6a00                     push 0
0044b278  6a00                     push 0
0044b27a  6a00                     push 0
0044b27c  6a00                     push 0
0044b27e  b810000000               mov eax, 0x10
0044b283  81e2ffff0000             and edx, 0xffff
0044b289  31c9                     xor ecx, ecx
0044b28b  89d3                     mov ebx, edx
0044b28d  e8ba310200               call 0x46e44c
0044b292  31c0                     xor eax, eax
0044b294  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044b29b  e8d6f6fcff               call 0x41a976
0044b2a0  6685c0                   test ax, ax
0044b2a3  7410                     je 0x44b2b5
0044b2a5  31c0                     xor eax, eax
0044b2a7  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044b2ae  e8111cfdff               call 0x41cec4
0044b2b3  eb0e                     jmp 0x44b2c3
0044b2b5  31c0                     xor eax, eax
0044b2b7  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044b2be  e8961cfdff               call 0x41cf59
0044b2c3  c6868b00000014           mov byte ptr [esi + 0x8b], 0x14
0044b2ca  8a06                     mov al, byte ptr [esi]
0044b2cc  3a0541805000             cmp al, byte ptr [0x508041]
0044b2d2  756e                     jne 0x44b342
0044b2d4  31db                     xor ebx, ebx
0044b2d6  6689fb                   mov bx, di
0044b2d9  89d8                     mov eax, ebx
0044b2db  c1e004                   shl eax, 4
0044b2de  01d8                     add eax, ebx
0044b2e0  c1e002                   shl eax, 2
0044b2e3  8b35a0194e00             mov esi, dword ptr [0x4e19a0]
0044b2e9  01d8                     add eax, ebx
0044b2eb  89da                     mov edx, ebx
0044b2ed  c1e002                   shl eax, 2
0044b2f0  31da                     xor edx, ebx
0044b2f2  01c6                     add esi, eax
0044b2f4  31c0                     xor eax, eax
0044b2f6  8a1541805000             mov dl, byte ptr [0x508041]
0044b2fc  668b4608                 mov ax, word ptr [esi + 8]
0044b300  e8ebb30200               call 0x4766f0
0044b305  84c0                     test al, al
0044b307  7439                     je 0x44b342
0044b309  89d8                     mov eax, ebx
0044b30b  e84d59ffff               call 0x440c5d
0044b310  8bbe04010000             mov edi, dword ptr [esi + 0x104]
0044b316  c686f900000000           mov byte ptr [esi + 0xf9], 0
0044b31d  83ffff                   cmp edi, -1
0044b320  7520                     jne 0x44b342
0044b322  50                       push eax
0044b323  31c0                     xor eax, eax
0044b325  8a4601                   mov al, byte ptr [esi + 1]
0044b328  c1e010                   shl eax, 0x10
0044b32b  8d9e04010000             lea ebx, [esi + 0x104]
0044b331  80cc25                   or ah, 0x25
0044b334  31c9                     xor ecx, ecx
0044b336  89c2                     mov edx, eax
0044b338  b850000000               mov eax, 0x50
0044b33d  e837f70300               call 0x48aa79
0044b342  83c404                   add esp, 4
0044b345  e9533f0000               jmp 0x44f29d
0044b34a  31c0                     xor eax, eax
0044b34c  8a86be000000             mov al, byte ptr [esi + 0xbe]
0044b352  83f809                   cmp eax, 9
0044b355  0f85b5000000             jne 0x44b410
0044b35b  31c0                     xor eax, eax
0044b35d  668b86d8000000           mov ax, word ptr [esi + 0xd8]
0044b364  85c0                     test eax, eax
0044b366  0f84a4000000             je 0x44b410
0044b36c  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044b372  01da                     add edx, ebx
0044b374  668b9ac4000000           mov bx, word ptr [edx + 0xc4]
0044b37b  66895a7e                 mov word ptr [edx + 0x7e], bx
0044b37f  668b0d04634900           mov cx, word ptr [0x496304]
0044b386  89d0                     mov eax, edx
0044b388  6639cf                   cmp di, cx
0044b38b  7522                     jne 0x44b3af
0044b38d  30ed                     xor ch, ch
0044b38f  31f6                     xor esi, esi
0044b391  882d360f4e00             mov byte ptr [0x4e0f36], ch
0044b397  89353c0f4e00             mov dword ptr [0x4e0f3c], esi
0044b39d  beffff0000               mov esi, 0xffff
0044b3a2  882d370f4e00             mov byte ptr [0x4e0f37], ch
0044b3a8  66893504634900           mov word ptr [0x496304], si
0044b3af  c6808800000000           mov byte ptr [eax + 0x88], 0
0044b3b6  c6828800000000           mov byte ptr [edx + 0x88], 0
0044b3bd  c6828900000000           mov byte ptr [edx + 0x89], 0
0044b3c4  66c782c0000000ffff       mov word ptr [edx + 0xc0], 0xffff
0044b3cd  c642020b                 mov byte ptr [edx + 2], 0xb
0044b3d1  66899ab2000000           mov word ptr [edx + 0xb2], bx
0044b3d8  bb01000000               mov ebx, 1
0044b3dd  eb16                     jmp 0x44b3f5
0044b3df  31c0                     xor eax, eax
0044b3e1  6689d8                   mov ax, bx
0044b3e4  668bb442c4000000         mov si, word ptr [edx + eax*2 + 0xc4]
0044b3ec  43                       inc ebx
0044b3ed  6689b442c2000000         mov word ptr [edx + eax*2 + 0xc2], si
0044b3f5  668b8ad8000000           mov cx, word ptr [edx + 0xd8]
0044b3fc  6639cb                   cmp bx, cx
0044b3ff  72de                     jb 0x44b3df
0044b401  89ce                     mov esi, ecx
0044b403  4e                       dec esi
0044b404  6689b2d8000000           mov word ptr [edx + 0xd8], si
0044b40b  e932ffffff               jmp 0x44b342
0044b410  8a1541805000             mov dl, byte ptr [0x508041]
0044b416  3a16                     cmp dl, byte ptr [esi]
0044b418  756e                     jne 0x44b488
0044b41a  31c9                     xor ecx, ecx
0044b41c  6689f9                   mov cx, di
0044b41f  89c8                     mov eax, ecx
0044b421  c1e004                   shl eax, 4
0044b424  01c8                     add eax, ecx
0044b426  c1e002                   shl eax, 2
0044b429  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044b42f  01c8                     add eax, ecx
0044b431  89ca                     mov edx, ecx
0044b433  c1e002                   shl eax, 2
0044b436  31ca                     xor edx, ecx
0044b438  01c3                     add ebx, eax
0044b43a  31c0                     xor eax, eax
0044b43c  8a1541805000             mov dl, byte ptr [0x508041]
0044b442  668b4308                 mov ax, word ptr [ebx + 8]
0044b446  e8a5b20200               call 0x4766f0
0044b44b  84c0                     test al, al
0044b44d  7439                     je 0x44b488
0044b44f  89c8                     mov eax, ecx
0044b451  e80758ffff               call 0x440c5d
0044b456  8b9304010000             mov edx, dword ptr [ebx + 0x104]
0044b45c  c683f900000000           mov byte ptr [ebx + 0xf9], 0
0044b463  83faff                   cmp edx, -1
0044b466  7520                     jne 0x44b488
0044b468  50                       push eax
0044b469  31d2                     xor edx, edx
0044b46b  31c9                     xor ecx, ecx
0044b46d  8a5301                   mov dl, byte ptr [ebx + 1]
0044b470  8d8304010000             lea eax, [ebx + 0x104]
0044b476  c1e210                   shl edx, 0x10
0044b479  89c3                     mov ebx, eax
0044b47b  b850000000               mov eax, 0x50
0044b480  80ce12                   or dh, 0x12
0044b483  e8f1f50300               call 0x48aa79
0044b488  31d2                     xor edx, edx
0044b48a  6689fa                   mov dx, di
0044b48d  89d0                     mov eax, edx
0044b48f  c1e004                   shl eax, 4
0044b492  b107                     mov cl, 7
0044b494  01d0                     add eax, edx
0044b496  c686be000000ff           mov byte ptr [esi + 0xbe], 0xff
0044b49d  c1e002                   shl eax, 2
0044b4a0  66c786b2000000ffff       mov word ptr [esi + 0xb2], 0xffff
0044b4a9  01c2                     add edx, eax
0044b4ab  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044b4b0  c1e202                   shl edx, 2
0044b4b3  89fb                     mov ebx, edi
0044b4b5  8a440202                 mov al, byte ptr [edx + eax + 2]
0044b4b9  25ff000000               and eax, 0xff
0044b4be  7409                     je 0x44b4c9
0044b4c0  83f804                   cmp eax, 4
0044b4c3  7404                     je 0x44b4c9
0044b4c5  b001                     mov al, 1
0044b4c7  eb02                     jmp 0x44b4cb
0044b4c9  30c0                     xor al, al
0044b4cb  84c0                     test al, al
0044b4cd  744b                     je 0x44b51a
0044b4cf  31d2                     xor edx, edx
0044b4d1  6689da                   mov dx, bx
0044b4d4  89d0                     mov eax, edx
0044b4d6  c1e004                   shl eax, 4
0044b4d9  01d0                     add eax, edx
0044b4db  c1e002                   shl eax, 2
0044b4de  01d0                     add eax, edx
0044b4e0  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044b4e6  884c8202                 mov byte ptr [edx + eax*4 + 2], cl
0044b4ea  668b1504634900           mov dx, word ptr [0x496304]
0044b4f1  6639d3                   cmp bx, dx
0044b4f4  7524                     jne 0x44b51a
0044b4f6  30f6                     xor dh, dh
0044b4f8  30d3                     xor bl, dl
0044b4fa  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044b500  31db                     xor ebx, ebx
0044b502  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
0044b508  bbffff0000               mov ebx, 0xffff
0044b50d  8835360f4e00             mov byte ptr [0x4e0f36], dh
0044b513  66891d04634900           mov word ptr [0x496304], bx
0044b51a  31d2                     xor edx, edx
0044b51c  6689fa                   mov dx, di
0044b51f  89d0                     mov eax, edx
0044b521  c1e004                   shl eax, 4
0044b524  01d0                     add eax, edx
0044b526  c1e002                   shl eax, 2
0044b529  01d0                     add eax, edx
0044b52b  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044b531  c1e002                   shl eax, 2
0044b534  01d0                     add eax, edx
0044b536  668b587c                 mov bx, word ptr [eax + 0x7c]
0044b53a  6689587e                 mov word ptr [eax + 0x7e], bx
0044b53e  668b0d04634900           mov cx, word ptr [0x496304]
0044b545  89c2                     mov edx, eax
0044b547  6639cf                   cmp di, cx
0044b54a  7522                     jne 0x44b56e
0044b54c  beffff0000               mov esi, 0xffff
0044b551  30ff                     xor bh, bh
0044b553  31c9                     xor ecx, ecx
0044b555  883d360f4e00             mov byte ptr [0x4e0f36], bh
0044b55b  883d370f4e00             mov byte ptr [0x4e0f37], bh
0044b561  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044b567  66893504634900           mov word ptr [0x496304], si
0044b56e  c6828800000000           mov byte ptr [edx + 0x88], 0
0044b575  e9c8fdffff               jmp 0x44b342
0044b57a  8a8689000000             mov al, byte ptr [esi + 0x89]
0044b580  84c0                     test al, al
0044b582  0f8613f6ffff             jbe 0x44ab9b
0044b588  3c01                     cmp al, 1
0044b58a  0f8431fcffff             je 0x44b1c1
0044b590  e9adfdffff               jmp 0x44b342
