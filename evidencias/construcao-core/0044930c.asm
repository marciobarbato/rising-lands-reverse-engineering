; DeplaceEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044930c  53                       push ebx
0044930d  51                       push ecx
0044930e  52                       push edx
0044930f  56                       push esi
00449310  57                       push edi
00449311  89c2                     mov edx, eax
00449313  31c0                     xor eax, eax
00449315  6689d0                   mov ax, dx
00449318  89c1                     mov ecx, eax
0044931a  c1e104                   shl ecx, 4
0044931d  01c1                     add ecx, eax
0044931f  c1e102                   shl ecx, 2
00449322  01c1                     add ecx, eax
00449324  8b35a0194e00             mov esi, dword ptr [0x4e19a0]
0044932a  c1e102                   shl ecx, 2
0044932d  01ce                     add esi, ecx
0044932f  8a9e88000000             mov bl, byte ptr [esi + 0x88]
00449335  80fb06                   cmp bl, 6
00449338  0f871a7affff             ja 0x440d58
0044933e  81e3ff000000             and ebx, 0xff
00449344  2eff249df0924400         jmp dword ptr cs:[ebx*4 + 0x4492f0]
0044934c  c6868800000000           mov byte ptr [esi + 0x88], 0
00449353  e9007affff               jmp 0x440d58
00449358  8b9e83000000             mov ebx, dword ptr [esi + 0x83]
0044935e  c1fb18                   sar ebx, 0x18
00449361  85db                     test ebx, ebx
00449363  7564                     jne 0x4493c9
00449365  8b9e84000000             mov ebx, dword ptr [esi + 0x84]
0044936b  c1fb18                   sar ebx, 0x18
0044936e  85db                     test ebx, ebx
00449370  7557                     jne 0x4493c9
00449372  803d360f4e0000           cmp byte ptr [0x4e0f36], 0
00449379  0f85d979ffff             jne 0x440d58
0044937f  6a00                     push 0
00449381  8b1d24194e00             mov ebx, dword ptr [0x4e1924]
00449387  6a00                     push 0
00449389  8b0c83                   mov ecx, dword ptr [ebx + eax*4]
0044938c  8abeab000000             mov bh, byte ptr [esi + 0xab]
00449392  51                       push ecx
00449393  84ff                     test bh, bh
00449395  0f95c0                   setne al
00449398  25ff000000               and eax, 0xff
0044939d  31c9                     xor ecx, ecx
0044939f  31db                     xor ebx, ebx
004493a1  40                       inc eax
004493a2  6689d3                   mov bx, dx
004493a5  88c1                     mov cl, al
004493a7  31d2                     xor edx, edx
004493a9  31c0                     xor eax, eax
004493ab  668b567e                 mov dx, word ptr [esi + 0x7e]
004493af  668b4608                 mov ax, word ptr [esi + 8]
004493b3  e8531fffff               call 0x43b30b
004493b8  e8575efeff               call 0x42f214
004493bd  c6868800000004           mov byte ptr [esi + 0x88], 4
004493c4  e98f79ffff               jmp 0x440d58
004493c9  31c0                     xor eax, eax
004493cb  6689d0                   mov ax, dx
004493ce  e87dfbffff               call 0x448f50
004493d3  e98079ffff               jmp 0x440d58
004493d8  803d0263490000           cmp byte ptr [0x496302], 0
004493df  0f840d010000             je 0x4494f2
004493e5  8a3d370f4e00             mov bh, byte ptr [0x4e0f37]
004493eb  84ff                     test bh, bh
004493ed  7461                     je 0x449450
004493ef  31c0                     xor eax, eax
004493f1  8a4602                   mov al, byte ptr [esi + 2]
004493f4  83f802                   cmp eax, 2
004493f7  754b                     jne 0x449444
004493f9  803d4c0f4e0002           cmp byte ptr [0x4e0f4c], 2
00449400  7542                     jne 0x449444
00449402  668b1d4a0f4e00           mov bx, word ptr [0x4e0f4a]
00449409  66895e7e                 mov word ptr [esi + 0x7e], bx
0044940d  668b3d04634900           mov di, word ptr [0x496304]
00449414  89f0                     mov eax, esi
00449416  6639fa                   cmp dx, di
00449419  7522                     jne 0x44943d
0044941b  30db                     xor bl, bl
0044941d  31ff                     xor edi, edi
0044941f  881d360f4e00             mov byte ptr [0x4e0f36], bl
00449425  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044942b  bbffff0000               mov ebx, 0xffff
00449430  893d3c0f4e00             mov dword ptr [0x4e0f3c], edi
00449436  66891d04634900           mov word ptr [0x496304], bx
0044943d  c6808800000000           mov byte ptr [eax + 0x88], 0
00449444  c6868800000005           mov byte ptr [esi + 0x88], 5
0044944b  e96f000000               jmp 0x4494bf
00449450  803d4c0f4e0008           cmp byte ptr [0x4e0f4c], 8
00449457  750f                     jne 0x449468
00449459  c6868800000006           mov byte ptr [esi + 0x88], 6
00449460  88be8b000000             mov byte ptr [esi + 0x8b], bh
00449466  eb57                     jmp 0x4494bf
00449468  e809fdffff               call 0x449176
0044946d  84c0                     test al, al
0044946f  7408                     je 0x449479
00449471  88be88000000             mov byte ptr [esi + 0x88], bh
00449477  eb46                     jmp 0x4494bf
00449479  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044947e  01c8                     add eax, ecx
00449480  668b487c                 mov cx, word ptr [eax + 0x7c]
00449484  6689487e                 mov word ptr [eax + 0x7e], cx
00449488  668b0d04634900           mov cx, word ptr [0x496304]
0044948f  89c3                     mov ebx, eax
00449491  6639ca                   cmp dx, cx
00449494  7522                     jne 0x4494b8
00449496  30c9                     xor cl, cl
00449498  beffff0000               mov esi, 0xffff
0044949d  880d360f4e00             mov byte ptr [0x4e0f36], cl
004494a3  880d370f4e00             mov byte ptr [0x4e0f37], cl
004494a9  31c9                     xor ecx, ecx
004494ab  66893504634900           mov word ptr [0x496304], si
004494b2  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
004494b8  c6838800000000           mov byte ptr [ebx + 0x88], 0
004494bf  663b1504634900           cmp dx, word ptr [0x496304]
004494c6  0f858c78ffff             jne 0x440d58
004494cc  beffff0000               mov esi, 0xffff
004494d1  30c9                     xor cl, cl
004494d3  31c0                     xor eax, eax
004494d5  880d360f4e00             mov byte ptr [0x4e0f36], cl
004494db  880d370f4e00             mov byte ptr [0x4e0f37], cl
004494e1  a33c0f4e00               mov dword ptr [0x4e0f3c], eax
004494e6  66893504634900           mov word ptr [0x496304], si
004494ed  e96678ffff               jmp 0x440d58
004494f2  e81d5dfeff               call 0x42f214
004494f7  e95c78ffff               jmp 0x440d58
004494fc  fe868b000000             inc byte ptr [esi + 0x8b]
00449502  31c0                     xor eax, eax
00449504  8a868b000000             mov al, byte ptr [esi + 0x8b]
0044950a  83f814                   cmp eax, 0x14
0044950d  0f854578ffff             jne 0x440d58
00449513  c6868b00000000           mov byte ptr [esi + 0x8b], 0
0044951a  c6868800000003           mov byte ptr [esi + 0x88], 3
00449521  e93278ffff               jmp 0x440d58
