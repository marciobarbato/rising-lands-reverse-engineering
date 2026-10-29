00442cb4  53                   push ebx
00442cb5  51                   push ecx
00442cb6  56                   push esi
00442cb7  57                   push edi
00442cb8  55                   push ebp
00442cb9  83ec04               sub esp, 4
00442cbc  89c3                 mov ebx, eax
00442cbe  89d6                 mov esi, edx
00442cc0  31ff                 xor edi, edi
00442cc2  6689c7               mov di, ax
00442cc5  89f8                 mov eax, edi
00442cc7  c1e004               shl eax, 4
00442cca  01f8                 add eax, edi
00442ccc  c1e002               shl eax, 2
00442ccf  01f8                 add eax, edi
00442cd1  8b2da0194e00         mov ebp, dword ptr [0x4e19a0]
00442cd7  c1e002               shl eax, 2
00442cda  01c5                 add ebp, eax
00442cdc  8a4501               mov al, byte ptr [ebp + 1]
00442cdf  3c19                 cmp al, 0x19
00442ce1  0f8738000000         ja 0x442d1f
00442ce7  25ff000000           and eax, 0xff
00442cec  2eff24854c2c4400     jmp dword ptr cs:[eax*4 + 0x442c4c]
00442cf4  81e6ffff0000         and esi, 0xffff
00442cfa  ba01000000           mov edx, 1
00442cff  89f0                 mov eax, esi
00442d01  8d8dfa000000         lea ecx, [ebp + 0xfa]
00442d07  e822350300           call 0x47622e
00442d0c  6a00                 push 0
00442d0e  31d2                 xor edx, edx
00442d10  89f0                 mov eax, esi
00442d12  6689da               mov dx, bx
00442d15  bb02000000           mov ebx, 2
00442d1a  e819b4ffff           call 0x43e138
00442d1f  83c404               add esp, 4
00442d22  e900320000           jmp 0x445f27
00442d27  31c0                 xor eax, eax
00442d29  6689d0               mov ax, dx
00442d2c  ba02000000           mov edx, 2
00442d31  e8f8340300           call 0x47622e
00442d36  ebe7                 jmp 0x442d1f
00442d38  ba01000000           mov edx, 1
00442d3d  8d8dfa000000         lea ecx, [ebp + 0xfa]
00442d43  31c0                 xor eax, eax
00442d45  31ff                 xor edi, edi
00442d47  6689f0               mov ax, si
00442d4a  6689df               mov di, bx
00442d4d  bb02000000           mov ebx, 2
00442d52  890424               mov dword ptr [esp], eax
00442d55  e8d4340300           call 0x47622e
00442d5a  6a00                 push 0
00442d5c  8b442404             mov eax, dword ptr [esp + 4]
00442d60  89fa                 mov edx, edi
00442d62  e8d1b3ffff           call 0x43e138
00442d67  89f0                 mov eax, esi
00442d69  48                   dec eax
00442d6a  ba01000000           mov edx, 1
00442d6f  bb02000000           mov ebx, 2
00442d74  25ffff0000           and eax, 0xffff
00442d79  8d8dfc000000         lea ecx, [ebp + 0xfc]
00442d7f  890424               mov dword ptr [esp], eax
00442d82  e8a7340300           call 0x47622e
00442d87  6a01                 push 1
00442d89  8b442404             mov eax, dword ptr [esp + 4]
00442d8d  89fa                 mov edx, edi
00442d8f  e8a4b3ffff           call 0x43e138
00442d94  89f0                 mov eax, esi
00442d96  81e801010000         sub eax, 0x101
00442d9c  ba01000000           mov edx, 1
00442da1  bb02000000           mov ebx, 2
00442da6  25ffff0000           and eax, 0xffff
00442dab  8d8dfe000000         lea ecx, [ebp + 0xfe]
00442db1  890424               mov dword ptr [esp], eax
00442db4  e875340300           call 0x47622e
00442db9  6a02                 push 2
00442dbb  8b442404             mov eax, dword ptr [esp + 4]
00442dbf  89fa                 mov edx, edi
00442dc1  81ee00010000         sub esi, 0x100
00442dc7  e86cb3ffff           call 0x43e138
00442dcc  ba01000000           mov edx, 1
00442dd1  81e6ffff0000         and esi, 0xffff
00442dd7  bb02000000           mov ebx, 2
00442ddc  89f0                 mov eax, esi
00442dde  8d8d00010000         lea ecx, [ebp + 0x100]
00442de4  e845340300           call 0x47622e
00442de9  6a03                 push 3
00442deb  89fa                 mov edx, edi
00442ded  89f0                 mov eax, esi
00442def  e926ffffff           jmp 0x442d1a
00442df4  31c0                 xor eax, eax
00442df6  6689d0               mov ax, dx
00442df9  ba02000000           mov edx, 2
00442dfe  e82b340300           call 0x47622e
00442e03  89f0                 mov eax, esi
00442e05  48                   dec eax
00442e06  ba02000000           mov edx, 2
00442e0b  25ffff0000           and eax, 0xffff
00442e10  e819340300           call 0x47622e
00442e15  89f0                 mov eax, esi
00442e17  81e801010000         sub eax, 0x101
00442e1d  ba02000000           mov edx, 2
00442e22  25ffff0000           and eax, 0xffff
00442e27  e802340300           call 0x47622e
00442e2c  81ee00010000         sub esi, 0x100
00442e32  31c0                 xor eax, eax
00442e34  ba02000000           mov edx, 2
00442e39  6689f0               mov ax, si
00442e3c  e9f0feffff           jmp 0x442d31
