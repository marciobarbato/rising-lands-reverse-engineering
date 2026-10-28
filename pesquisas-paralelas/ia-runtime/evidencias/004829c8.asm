; iagUnitSendMessage (messages); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x004829c8..0x00482ebc (end exclusive); labels are original SBL names
004829c8  51                       push ecx
004829c9  56                       push esi
004829ca  57                       push edi
004829cb  55                       push ebp
004829cc  89e5                     mov ebp, esp
004829ce  83ec1c                   sub esp, 0x1c
004829d1  89c6                     mov esi, eax
004829d3  8855fc                   mov byte ptr [ebp - 4], dl
004829d6  89da                     mov edx, ebx
004829d8  31db                     xor ebx, ebx
004829da  6689c3                   mov bx, ax
004829dd  89df                     mov edi, ebx
004829df  c1e704                   shl edi, 4
004829e2  01df                     add edi, ebx
004829e4  c1e702                   shl edi, 2
004829e7  01df                     add edi, ebx
004829e9  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004829ee  c1e702                   shl edi, 2
004829f1  8a0407                   mov al, byte ptr [edi + eax]
004829f4  25ff000000               and eax, 0xff
004829f9  8945e4                   mov dword ptr [ebp - 0x1c], eax
004829fc  31c0                     xor eax, eax
004829fe  8a45e4                   mov al, byte ptr [ebp - 0x1c]
00482a01  e811aefeff               call 0x46d817 ; -> PlayerGetType
00482a06  25ff000000               and eax, 0xff
00482a0b  83f802                   cmp eax, 2
00482a0e  0f85a1040000             jne 0x482eb5
00482a14  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00482a19  8bbc070c010000           mov edi, dword ptr [edi + eax + 0x10c]
00482a20  83ffff                   cmp edi, -1
00482a23  7410                     je 0x482a35
00482a25  89f9                     mov ecx, edi
00482a27  c1e105                   shl ecx, 5
00482a2a  81c1e0a95100             add ecx, 0x51a9e0
00482a30  e902000000               jmp 0x482a37
00482a35  31c9                     xor ecx, ecx
00482a37  8a45fc                   mov al, byte ptr [ebp - 4]
00482a3a  2c41                     sub al, 0x41
00482a3c  3c0b                     cmp al, 0xb
00482a3e  0f8771040000             ja 0x482eb5
00482a44  25ff000000               and eax, 0xff
00482a49  2eff248598294800         jmp dword ptr cs:[eax*4 + 0x482998]
00482a51  85c9                     test ecx, ecx
00482a53  0f845c040000             je 0x482eb5
00482a59  31d2                     xor edx, edx
00482a5b  89f8                     mov eax, edi
00482a5d  6689f2                   mov dx, si
00482a60  e84c080000               call 0x4832b1 ; -> iagUnitRemoveFromGroup
00482a65  31d2                     xor edx, edx
00482a67  6689f2                   mov dx, si
00482a6a  89d0                     mov eax, edx
00482a6c  c1e004                   shl eax, 4
00482a6f  01d0                     add eax, edx
00482a71  c1e002                   shl eax, 2
00482a74  01c2                     add edx, eax
00482a76  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00482a7b  c1e202                   shl edx, 2
00482a7e  01d0                     add eax, edx
00482a80  31d2                     xor edx, edx
00482a82  8a10                     mov dl, byte ptr [eax]
00482a84  89d0                     mov eax, edx
00482a86  c1e002                   shl eax, 2
00482a89  29d0                     sub eax, edx
00482a8b  31d2                     xor edx, edx
00482a8d  c1e005                   shl eax, 5
00482a90  6689f2                   mov dx, si
00482a93  8b988cb65100             mov ebx, dword ptr [eax + 0x51b68c]
00482a99  89d0                     mov eax, edx
00482a9b  c1e004                   shl eax, 4
00482a9e  01d0                     add eax, edx
00482aa0  c1e002                   shl eax, 2
00482aa3  89d9                     mov ecx, ebx
00482aa5  01d0                     add eax, edx
00482aa7  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00482aad  c1e002                   shl eax, 2
00482ab0  c1e105                   shl ecx, 5
00482ab3  01c2                     add edx, eax
00482ab5  b8e0a95100               mov eax, 0x51a9e0
00482aba  01c8                     add eax, ecx
00482abc  0f84f3030000             je 0x482eb5
00482ac2  668b4810                 mov cx, word ptr [eax + 0x10]
00482ac6  66898a08010000           mov word ptr [edx + 0x108], cx
00482acd  899a0c010000             mov dword ptr [edx + 0x10c], ebx
00482ad3  668b5812                 mov bx, word ptr [eax + 0x12]
00482ad7  66897010                 mov word ptr [eax + 0x10], si
00482adb  43                       inc ebx
00482adc  66895812                 mov word ptr [eax + 0x12], bx
00482ae0  e9d0030000               jmp 0x482eb5
00482ae5  31d2                     xor edx, edx
00482ae7  6689f2                   mov dx, si
00482aea  89d0                     mov eax, edx
00482aec  c1e004                   shl eax, 4
00482aef  01d0                     add eax, edx
00482af1  c1e002                   shl eax, 2
00482af4  01d0                     add eax, edx
00482af6  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00482afc  c1e002                   shl eax, 2
00482aff  01d0                     add eax, edx
00482b01  31d2                     xor edx, edx
00482b03  8a10                     mov dl, byte ptr [eax]
00482b05  89d0                     mov eax, edx
00482b07  c1e002                   shl eax, 2
00482b0a  31db                     xor ebx, ebx
00482b0c  29d0                     sub eax, edx
00482b0e  6689f3                   mov bx, si
00482b11  c1e005                   shl eax, 5
00482b14  89da                     mov edx, ebx
00482b16  8b808cb65100             mov eax, dword ptr [eax + 0x51b68c]
00482b1c  e890070000               call 0x4832b1 ; -> iagUnitRemoveFromGroup
00482b21  31d2                     xor edx, edx
00482b23  6689f2                   mov dx, si
00482b26  89d0                     mov eax, edx
00482b28  c1e004                   shl eax, 4
00482b2b  01d0                     add eax, edx
00482b2d  c1e002                   shl eax, 2
00482b30  01d0                     add eax, edx
00482b32  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00482b38  c1e002                   shl eax, 2
00482b3b  01d0                     add eax, edx
00482b3d  31d2                     xor edx, edx
00482b3f  8a10                     mov dl, byte ptr [eax]
00482b41  89d0                     mov eax, edx
00482b43  c1e002                   shl eax, 2
00482b46  29d0                     sub eax, edx
00482b48  c1e005                   shl eax, 5
00482b4b  8b9090b65100             mov edx, dword ptr [eax + 0x51b690]
00482b51  31c0                     xor eax, eax
00482b53  6689f0                   mov ax, si
00482b56  e8760d0000               call 0x4838d1 ; -> iagUnitDispatch
00482b5b  e955030000               jmp 0x482eb5
00482b60  31d2                     xor edx, edx
00482b62  6689f2                   mov dx, si
00482b65  89d0                     mov eax, edx
00482b67  c1e004                   shl eax, 4
00482b6a  01d0                     add eax, edx
00482b6c  c1e002                   shl eax, 2
00482b6f  01d0                     add eax, edx
00482b71  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00482b77  c1e002                   shl eax, 2
00482b7a  01c2                     add edx, eax
00482b7c  31db                     xor ebx, ebx
00482b7e  8a1a                     mov bl, byte ptr [edx]
00482b80  89d8                     mov eax, ebx
00482b82  c1e002                   shl eax, 2
00482b85  29d8                     sub eax, ebx
00482b87  c1e005                   shl eax, 5
00482b8a  8b988cb65100             mov ebx, dword ptr [eax + 0x51b68c]
00482b90  89d8                     mov eax, ebx
00482b92  c1e005                   shl eax, 5
00482b95  89f7                     mov edi, esi
00482b97  05e0a95100               add eax, 0x51a9e0
00482b9c  741e                     je 0x482bbc
00482b9e  668b4810                 mov cx, word ptr [eax + 0x10]
00482ba2  66898a08010000           mov word ptr [edx + 0x108], cx
00482ba9  899a0c010000             mov dword ptr [edx + 0x10c], ebx
00482baf  668b5012                 mov dx, word ptr [eax + 0x12]
00482bb3  66897010                 mov word ptr [eax + 0x10], si
00482bb7  42                       inc edx
00482bb8  66895012                 mov word ptr [eax + 0x12], dx
00482bbc  31d2                     xor edx, edx
00482bbe  6689f2                   mov dx, si
00482bc1  89d0                     mov eax, edx
00482bc3  c1e004                   shl eax, 4
00482bc6  01d0                     add eax, edx
00482bc8  c1e002                   shl eax, 2
00482bcb  01d0                     add eax, edx
00482bcd  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00482bd3  c1e002                   shl eax, 2
00482bd6  01d0                     add eax, edx
00482bd8  31d2                     xor edx, edx
00482bda  31db                     xor ebx, ebx
00482bdc  8a10                     mov dl, byte ptr [eax]
00482bde  8a5801                   mov bl, byte ptr [eax + 1]
00482be1  89d0                     mov eax, edx
00482be3  c1e002                   shl eax, 2
00482be6  29d0                     sub eax, edx
00482be8  c1e005                   shl eax, 5
00482beb  8b90b4b65100             mov edx, dword ptr [eax + 0x51b6b4]
00482bf1  83faff                   cmp edx, -1
00482bf4  7419                     je 0x482c0f
00482bf6  89d0                     mov eax, edx
00482bf8  c1e005                   shl eax, 5
00482bfb  31c9                     xor ecx, ecx
00482bfd  8a88faa95100             mov cl, byte ptr [eax + 0x51a9fa]
00482c03  39d9                     cmp ecx, ebx
00482c05  7408                     je 0x482c0f
00482c07  8b90e4a95100             mov edx, dword ptr [eax + 0x51a9e4]
00482c0d  ebe2                     jmp 0x482bf1
00482c0f  83faff                   cmp edx, -1
00482c12  741e                     je 0x482c32
00482c14  6a00                     push 0
00482c16  6a00                     push 0
00482c18  31db                     xor ebx, ebx
00482c1a  6a00                     push 0
00482c1c  6689f3                   mov bx, si
00482c1f  6a00                     push 0
00482c21  89d8                     mov eax, ebx
00482c23  e81df4fbff               call 0x442045 ; -> EnginGetPlayer
00482c28  ba17000000               mov edx, 0x17
00482c2d  e9ee000000               jmp 0x482d20
00482c32  6a00                     push 0
00482c34  6a00                     push 0
00482c36  31db                     xor ebx, ebx
00482c38  6a00                     push 0
00482c3a  6689f3                   mov bx, si
00482c3d  6a00                     push 0
00482c3f  89d8                     mov eax, ebx
00482c41  e8fff3fbff               call 0x442045 ; -> EnginGetPlayer
00482c46  ba09000000               mov edx, 9
00482c4b  e9d0000000               jmp 0x482d20
00482c50  85c9                     test ecx, ecx
00482c52  0f845d020000             je 0x482eb5
00482c58  8b410c                   mov eax, dword ptr [ecx + 0xc]
00482c5b  83f8ff                   cmp eax, -1
00482c5e  741c                     je 0x482c7c
00482c60  89c2                     mov edx, eax
00482c62  31c0                     xor eax, eax
00482c64  6689f0                   mov ax, si
00482c67  bbffffffff               mov ebx, 0xffffffff
00482c6c  e8ce5a0000               call 0x48873f ; -> iagWarUnlockTargetAfterDeath
00482c71  8b45e4                   mov eax, dword ptr [ebp - 0x1c]
00482c74  8b510c                   mov edx, dword ptr [ecx + 0xc]
00482c77  e86e600000               call 0x488cea ; -> iagWarProbReturnTo
00482c7c  31d2                     xor edx, edx
00482c7e  89f8                     mov eax, edi
00482c80  6689f2                   mov dx, si
00482c83  e829060000               call 0x4832b1 ; -> iagUnitRemoveFromGroup
00482c88  83791c00                 cmp dword ptr [ecx + 0x1c], 0
00482c8c  0f8423020000             je 0x482eb5
00482c92  837908ff                 cmp dword ptr [ecx + 8], -1
00482c96  0f8419020000             je 0x482eb5
00482c9c  f6411c01                 test byte ptr [ecx + 0x1c], 1
00482ca0  7412                     je 0x482cb4
00482ca2  ba01000000               mov edx, 1
00482ca7  8b4108                   mov eax, dword ptr [ecx + 8]
00482caa  e8a5adffff               call 0x47da54 ; -> iaProbReturnTo
00482caf  e901020000               jmp 0x482eb5
00482cb4  baffffffff               mov edx, 0xffffffff
00482cb9  ebec                     jmp 0x482ca7
00482cbb  31db                     xor ebx, ebx
00482cbd  6689f3                   mov bx, si
00482cc0  89d8                     mov eax, ebx
00482cc2  c1e004                   shl eax, 4
00482cc5  01d8                     add eax, ebx
00482cc7  c1e002                   shl eax, 2
00482cca  01d8                     add eax, ebx
00482ccc  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00482cd2  c1e002                   shl eax, 2
00482cd5  01d0                     add eax, edx
00482cd7  31d2                     xor edx, edx
00482cd9  8a10                     mov dl, byte ptr [eax]
00482cdb  89d0                     mov eax, edx
00482cdd  c1e002                   shl eax, 2
00482ce0  29d0                     sub eax, edx
00482ce2  c1e005                   shl eax, 5
00482ce5  8b9064b65100             mov edx, dword ptr [eax + 0x51b664]
00482ceb  89d8                     mov eax, ebx
00482ced  e8df0b0000               call 0x4838d1 ; -> iagUnitDispatch
00482cf2  89d8                     mov eax, ebx
00482cf4  e82cf3fbff               call 0x442025 ; -> EnginGetType
00482cf9  25ff000000               and eax, 0xff
00482cfe  f60485f989490002         test byte ptr [eax*4 + 0x4989f9], 2
00482d06  0f84a9010000             je 0x482eb5
00482d0c  6a00                     push 0
00482d0e  6a00                     push 0
00482d10  6a00                     push 0
00482d12  6a00                     push 0
00482d14  89d8                     mov eax, ebx
00482d16  e82af3fbff               call 0x442045 ; -> EnginGetPlayer
00482d1b  ba10000000               mov edx, 0x10
00482d20  25ff000000               and eax, 0xff
00482d25  31c9                     xor ecx, ecx
00482d27  e8f4abffff               call 0x47d920 ; -> iaProbPost
00482d2c  e984010000               jmp 0x482eb5
00482d31  31db                     xor ebx, ebx
00482d33  6689f3                   mov bx, si
00482d36  89d9                     mov ecx, ebx
00482d38  c1e104                   shl ecx, 4
00482d3b  01d9                     add ecx, ebx
00482d3d  c1e102                   shl ecx, 2
00482d40  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00482d45  01d9                     add ecx, ebx
00482d47  89da                     mov edx, ebx
00482d49  c1e102                   shl ecx, 2
00482d4c  31da                     xor edx, ebx
00482d4e  8a1401                   mov dl, byte ptr [ecx + eax]
00482d51  89d0                     mov eax, edx
00482d53  c1e002                   shl eax, 2
00482d56  29d0                     sub eax, edx
00482d58  c1e005                   shl eax, 5
00482d5b  89da                     mov edx, ebx
00482d5d  8b808cb65100             mov eax, dword ptr [eax + 0x51b68c]
00482d63  e849050000               call 0x4832b1 ; -> iagUnitRemoveFromGroup
00482d68  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00482d6d  31d2                     xor edx, edx
00482d6f  8a1401                   mov dl, byte ptr [ecx + eax]
00482d72  e964ffffff               jmp 0x482cdb
00482d77  85c9                     test ecx, ecx
00482d79  0f8436010000             je 0x482eb5
00482d7f  31c0                     xor eax, eax
00482d81  8a411b                   mov al, byte ptr [ecx + 0x1b]
00482d84  3dff000000               cmp eax, 0xff
00482d89  0f8426010000             je 0x482eb5
00482d8f  8b0485948e4900           mov eax, dword ptr [eax*4 + 0x498e94]
00482d96  8b00                     mov eax, dword ptr [eax]
00482d98  8945ec                   mov dword ptr [ebp - 0x14], eax
00482d9b  85c0                     test eax, eax
00482d9d  0f8412010000             je 0x482eb5
00482da3  31c0                     xor eax, eax
00482da5  81e2ffff0000             and edx, 0xffff
00482dab  6689f0                   mov ax, si
00482dae  ff55ec                   call dword ptr [ebp - 0x14]
00482db1  e9ff000000               jmp 0x482eb5
00482db6  85c9                     test ecx, ecx
00482db8  0f84f7000000             je 0x482eb5
00482dbe  31c0                     xor eax, eax
00482dc0  8a411b                   mov al, byte ptr [ecx + 0x1b]
00482dc3  3dff000000               cmp eax, 0xff
00482dc8  0f84e7000000             je 0x482eb5
00482dce  8b0485948e4900           mov eax, dword ptr [eax*4 + 0x498e94]
00482dd5  8b400c                   mov eax, dword ptr [eax + 0xc]
00482dd8  8945f4                   mov dword ptr [ebp - 0xc], eax
00482ddb  85c0                     test eax, eax
00482ddd  0f84d2000000             je 0x482eb5
00482de3  31c0                     xor eax, eax
00482de5  81e2ffff0000             and edx, 0xffff
00482deb  6689f0                   mov ax, si
00482dee  ff55f4                   call dword ptr [ebp - 0xc]
00482df1  e9bf000000               jmp 0x482eb5
00482df6  85c9                     test ecx, ecx
00482df8  0f84b7000000             je 0x482eb5
00482dfe  31c0                     xor eax, eax
00482e00  8a411b                   mov al, byte ptr [ecx + 0x1b]
00482e03  3dff000000               cmp eax, 0xff
00482e08  0f84a7000000             je 0x482eb5
00482e0e  8b0485948e4900           mov eax, dword ptr [eax*4 + 0x498e94]
00482e15  8b4008                   mov eax, dword ptr [eax + 8]
00482e18  8945e8                   mov dword ptr [ebp - 0x18], eax
00482e1b  85c0                     test eax, eax
00482e1d  0f8492000000             je 0x482eb5
00482e23  31c0                     xor eax, eax
00482e25  81e2ffff0000             and edx, 0xffff
00482e2b  6689f0                   mov ax, si
00482e2e  ff55e8                   call dword ptr [ebp - 0x18]
00482e31  e97f000000               jmp 0x482eb5
00482e36  85c9                     test ecx, ecx
00482e38  0f8477000000             je 0x482eb5
00482e3e  31c0                     xor eax, eax
00482e40  8a411b                   mov al, byte ptr [ecx + 0x1b]
00482e43  3dff000000               cmp eax, 0xff
00482e48  741b                     je 0x482e65
00482e4a  8b0485948e4900           mov eax, dword ptr [eax*4 + 0x498e94]
00482e51  8b4004                   mov eax, dword ptr [eax + 4]
00482e54  8945f8                   mov dword ptr [ebp - 8], eax
00482e57  85c0                     test eax, eax
00482e59  740a                     je 0x482e65
00482e5b  31c0                     xor eax, eax
00482e5d  31d2                     xor edx, edx
00482e5f  6689f0                   mov ax, si
00482e62  ff55f8                   call dword ptr [ebp - 8]
00482e65  8b410c                   mov eax, dword ptr [ecx + 0xc]
00482e68  83f8ff                   cmp eax, -1
00482e6b  7448                     je 0x482eb5
00482e6d  bb01000000               mov ebx, 1
00482e72  89c2                     mov edx, eax
00482e74  8b45e4                   mov eax, dword ptr [ebp - 0x1c]
00482e77  e86e5e0000               call 0x488cea ; -> iagWarProbReturnTo
00482e7c  eb37                     jmp 0x482eb5
00482e7e  85c9                     test ecx, ecx
00482e80  7433                     je 0x482eb5
00482e82  31c0                     xor eax, eax
00482e84  8a411b                   mov al, byte ptr [ecx + 0x1b]
00482e87  3dff000000               cmp eax, 0xff
00482e8c  741d                     je 0x482eab
00482e8e  8b0485948e4900           mov eax, dword ptr [eax*4 + 0x498e94]
00482e95  8b4010                   mov eax, dword ptr [eax + 0x10]
00482e98  8945f0                   mov dword ptr [ebp - 0x10], eax
00482e9b  85c0                     test eax, eax
00482e9d  7416                     je 0x482eb5
00482e9f  31c0                     xor eax, eax
00482ea1  31d2                     xor edx, edx
00482ea3  6689f0                   mov ax, si
00482ea6  ff55f0                   call dword ptr [ebp - 0x10]
00482ea9  eb0a                     jmp 0x482eb5
00482eab  31c0                     xor eax, eax
00482ead  6689f0                   mov ax, si
00482eb0  e8cf0cfdff               call 0x453b84 ; -> EnginSetFatigue
00482eb5  89ec                     mov esp, ebp
00482eb7  5d                       pop ebp
00482eb8  5f                       pop edi
00482eb9  5e                       pop esi
00482eba  59                       pop ecx
00482ebb  c3                       ret
