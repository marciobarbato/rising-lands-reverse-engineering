004772ec  53                   push ebx
004772ed  51                   push ecx
004772ee  56                   push esi
004772ef  57                   push edi
004772f0  55                   push ebp
004772f1  83ec08               sub esp, 8
004772f4  c1e208               shl edx, 8
004772f7  89c3                 mov ebx, eax
004772f9  31ff                 xor edi, edi
004772fb  01d3                 add ebx, edx
004772fd  bd01000000           mov ebp, 1
00477302  eb0a                 jmp 0x47730e
00477304  b800010000           mov eax, 0x100
00477309  29c8                 sub eax, ecx
0047730b  47                   inc edi
0047730c  01c3                 add ebx, eax
0047730e  663b3d26875000       cmp di, word ptr [0x508726]
00477315  0f83d7010000         jae 0x4774f2
0047731b  31f6                 xor esi, esi
0047731d  e981000000           jmp 0x4773a3
00477322  f6057c8f500003       test byte ptr [0x508f7c], 3
00477329  0f8572000000         jne 0x4773a1
0047732f  a0181d4e00           mov al, byte ptr [0x4e1d18]
00477334  31c9                 xor ecx, ecx
00477336  88c1                 mov cl, al
00477338  fec0                 inc al
0047733a  a2181d4e00           mov byte ptr [0x4e1d18], al
0047733f  f681181c4e0003       test byte ptr [ecx + 0x4e1c18], 3
00477346  0f8555000000         jne 0x4773a1
0047734c  a1ac7d5000           mov eax, dword ptr [0x507dac]
00477351  01c2                 add edx, eax
00477353  8a02                 mov al, byte ptr [edx]
00477355  fec0                 inc al
00477357  2403                 and al, 3
00477359  8802                 mov byte ptr [edx], al
0047735b  eb44                 jmp 0x4773a1
0047735d  f6057c8f500001       test byte ptr [0x508f7c], 1
00477364  750e                 jne 0x477374
00477366  31c0                 xor eax, eax
00477368  8b15ac7d5000         mov edx, dword ptr [0x507dac]
0047736e  6689d8               mov ax, bx
00477371  fe0402               inc byte ptr [edx + eax]
00477374  31c0                 xor eax, eax
00477376  8b15ac7d5000         mov edx, dword ptr [0x507dac]
0047737c  6689d8               mov ax, bx
0047737f  8a1402               mov dl, byte ptr [edx + eax]
00477382  81e2ff000000         and edx, 0xff
00477388  83fa10               cmp edx, 0x10
0047738b  7514                 jne 0x4773a1
0047738d  8b15747d5000         mov edx, dword ptr [0x507d74]
00477393  c6040200             mov byte ptr [edx + eax], 0
00477397  8b15ac7d5000         mov edx, dword ptr [0x507dac]
0047739d  c6040200             mov byte ptr [edx + eax], 0
004773a1  43                   inc ebx
004773a2  46                   inc esi
004773a3  668b0d24875000       mov cx, word ptr [0x508724]
004773aa  6639ce               cmp si, cx
004773ad  0f8351ffffff         jae 0x477304
004773b3  31d2                 xor edx, edx
004773b5  a1747d5000           mov eax, dword ptr [0x507d74]
004773ba  6689da               mov dx, bx
004773bd  01d0                 add eax, edx
004773bf  8a08                 mov cl, byte ptr [eax]
004773c1  84c9                 test cl, cl
004773c3  0f85bc000000         jne 0x477485
004773c9  ebd6                 jmp 0x4773a1
004773cb  f6057c8f500001       test byte ptr [0x508f7c], 1
004773d2  7508                 jne 0x4773dc
004773d4  a1ac7d5000           mov eax, dword ptr [0x507dac]
004773d9  fe0402               inc byte ptr [edx + eax]
004773dc  31c0                 xor eax, eax
004773de  8b15ac7d5000         mov edx, dword ptr [0x507dac]
004773e4  6689d8               mov ax, bx
004773e7  8a1402               mov dl, byte ptr [edx + eax]
004773ea  81e2ff000000         and edx, 0xff
004773f0  83fa40               cmp edx, 0x40
004773f3  75ac                 jne 0x4773a1
004773f5  8b15747d5000         mov edx, dword ptr [0x507d74]
004773fb  01c2                 add edx, eax
004773fd  31c9                 xor ecx, ecx
004773ff  8a0a                 mov cl, byte ptr [edx]
00477401  83f93b               cmp ecx, 0x3b
00477404  7405                 je 0x47740b
00477406  83f938               cmp ecx, 0x38
00477409  7510                 jne 0x47741b
0047740b  31c0                 xor eax, eax
0047740d  8b15747d5000         mov edx, dword ptr [0x507d74]
00477413  6689d8               mov ax, bx
00477416  e978ffffff           jmp 0x477393
0047741b  30ed                 xor ch, ch
0047741d  882a                 mov byte ptr [edx], ch
0047741f  8b15ac7d5000         mov edx, dword ptr [0x507dac]
00477425  66890c24             mov word ptr [esp], cx
00477429  882c02               mov byte ptr [edx + eax], ch
0047742c  8a1424               mov dl, byte ptr [esp]
0047742f  feca                 dec dl
00477431  88542404             mov byte ptr [esp + 4], dl
00477435  8b15747d5000         mov edx, dword ptr [0x507d74]
0047743b  01c2                 add edx, eax
0047743d  31c9                 xor ecx, ecx
0047743f  8a0a                 mov cl, byte ptr [edx]
00477441  85c9                 test ecx, ecx
00477443  0f8558ffffff         jne 0x4773a1
00477449  8a4c2404             mov cl, byte ptr [esp + 4]
0047744d  880a                 mov byte ptr [edx], cl
0047744f  e943ffffff           jmp 0x477397
00477454  a1ac7d5000           mov eax, dword ptr [0x507dac]
00477459  fe0402               inc byte ptr [edx + eax]
0047745c  a1ac7d5000           mov eax, dword ptr [0x507dac]
00477461  8a0402               mov al, byte ptr [edx + eax]
00477464  25ff000000           and eax, 0xff
00477469  83f820               cmp eax, 0x20
0047746c  0f852fffffff         jne 0x4773a1
00477472  a1747d5000           mov eax, dword ptr [0x507d74]
00477477  c6040200             mov byte ptr [edx + eax], 0
0047747b  a1ac7d5000           mov eax, dword ptr [0x507dac]
00477480  e918ffffff           jmp 0x47739d
00477485  88c8                 mov al, cl
00477487  80f91b               cmp cl, 0x1b
0047748a  722c                 jb 0x4774b8
0047748c  0f86cbfeffff         jbe 0x47735d
00477492  80f938               cmp cl, 0x38
00477495  7213                 jb 0x4774aa
00477497  80f93d               cmp cl, 0x3d
0047749a  0f862bffffff         jbe 0x4773cb
004774a0  80f941               cmp cl, 0x41
004774a3  76af                 jbe 0x477454
004774a5  e9f7feffff           jmp 0x4773a1
004774aa  80f937               cmp cl, 0x37
004774ad  0f84aafeffff         je 0x47735d
004774b3  e9e9feffff           jmp 0x4773a1
004774b8  80f901               cmp cl, 1
004774bb  0f82e0feffff         jb 0x4773a1
004774c1  80f90b               cmp cl, 0xb
004774c4  0f8658feffff         jbe 0x477322
004774ca  80f917               cmp cl, 0x17
004774cd  0f82cefeffff         jb 0x4773a1
004774d3  f6057c8f500001       test byte ptr [0x508f7c], 1
004774da  0f85c1feffff         jne 0x4773a1
004774e0  a1ac7d5000           mov eax, dword ptr [0x507dac]
004774e5  01c2                 add edx, eax
004774e7  8a02                 mov al, byte ptr [edx]
004774e9  fec0                 inc al
004774eb  240f                 and al, 0xf
004774ed  e967feffff           jmp 0x477359
004774f2  83c408               add esp, 8
004774f5  e9fee6ffff           jmp 0x475bf8
