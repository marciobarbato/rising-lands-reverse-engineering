; SetDeplaceEnginSelect; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00473e6e  53                       push ebx
00473e6f  51                       push ecx
00473e70  56                       push esi
00473e71  57                       push edi
00473e72  83ec08                   sub esp, 8
00473e75  88442404                 mov byte ptr [esp + 4], al
00473e79  891424                   mov dword ptr [esp], edx
00473e7c  31ff                     xor edi, edi
00473e7e  31f6                     xor esi, esi
00473e80  eb01                     jmp 0x473e83
00473e82  46                       inc esi
00473e83  31c9                     xor ecx, ecx
00473e85  8a4c2404                 mov cl, byte ptr [esp + 4]
00473e89  c1e109                   shl ecx, 9
00473e8c  663bb128875000           cmp si, word ptr [ecx + 0x508728]
00473e93  0f836aeaffff             jae 0x472903
00473e99  31c0                     xor eax, eax
00473e9b  6689f0                   mov ax, si
00473e9e  668b84412a875000         mov ax, word ptr [ecx + eax*2 + 0x50872a]
00473ea6  31c9                     xor ecx, ecx
00473ea8  6689c1                   mov cx, ax
00473eab  89c8                     mov eax, ecx
00473ead  e8fbfefcff               call 0x443dad
00473eb2  84c0                     test al, al
00473eb4  74cc                     je 0x473e82
00473eb6  69d914010000             imul ebx, ecx, 0x114
00473ebc  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00473ec1  8a0403                   mov al, byte ptr [ebx + eax]
00473ec4  3a442404                 cmp al, byte ptr [esp + 4]
00473ec8  75b8                     jne 0x473e82
00473eca  31d2                     xor edx, edx
00473ecc  89c8                     mov eax, ecx
00473ece  668b1424                 mov dx, word ptr [esp]
00473ed2  e8fc18fdff               call 0x4457d3
00473ed7  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00473edc  8b157c8f5000             mov edx, dword ptr [0x508f7c]
00473ee2  89940310010000           mov dword ptr [ebx + eax + 0x110], edx
00473ee9  89c8                     mov eax, ecx
00473eeb  e835e1fcff               call 0x442025
00473ef0  25ff000000               and eax, 0xff
00473ef5  e89ae4fcff               call 0x442394
00473efa  84c0                     test al, al
00473efc  7584                     jne 0x473e82
00473efe  89c8                     mov eax, ecx
00473f00  e820e1fcff               call 0x442025
00473f05  25ff000000               and eax, 0xff
00473f0a  e8c0e3fcff               call 0x4422cf
00473f0f  84c0                     test al, al
00473f11  0f856bffffff             jne 0x473e82
00473f17  31c0                     xor eax, eax
00473f19  6689f8                   mov ax, di
00473f1c  83f801                   cmp eax, 1
00473f1f  0f8d5dffffff             jge 0x473e82
00473f25  8a442404                 mov al, byte ptr [esp + 4]
00473f29  8a1541805000             mov dl, byte ptr [0x508041]
00473f2f  47                       inc edi
00473f30  38d0                     cmp al, dl
00473f32  0f854affffff             jne 0x473e82
00473f38  ba0b000000               mov edx, 0xb
00473f3d  89c8                     mov eax, ecx
00473f3f  31db                     xor ebx, ebx
00473f41  e818cefcff               call 0x440d5e
00473f46  e937ffffff               jmp 0x473e82
