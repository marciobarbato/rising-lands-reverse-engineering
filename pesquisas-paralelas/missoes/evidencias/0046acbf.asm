; LoadEngin; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046acbf  53                       push ebx
0046acc0  51                       push ecx
0046acc1  52                       push edx
0046acc2  83ec0c                   sub esp, 0xc
0046acc5  e88b780000               call 0x472555
0046acca  b332                     mov bl, 0x32
0046accc  31d2                     xor edx, edx
0046acce  eb07                     jmp 0x46acd7
0046acd0  42                       inc edx
0046acd1  8898bc194e00             mov byte ptr [eax + 0x4e19bc], bl
0046acd7  31c0                     xor eax, eax
0046acd9  6689d0                   mov ax, dx
0046acdc  83f804                   cmp eax, 4
0046acdf  7cef                     jl 0x46acd0
0046ace1  ba02000000               mov edx, 2
0046ace6  8d442404                 lea eax, [esp + 4]
0046acea  e872d7feff               call 0x458461
0046acef  ba02000000               mov edx, 2
0046acf4  89e0                     mov eax, esp
0046acf6  31db                     xor ebx, ebx
0046acf8  e864d7feff               call 0x458461
0046acfd  eb01                     jmp 0x46ad00
0046acff  43                       inc ebx
0046ad00  663b5c2404               cmp bx, word ptr [esp + 4]
0046ad05  0f8307040000             jae 0x46b112
0046ad0b  ba02000000               mov edx, 2
0046ad10  8d442408                 lea eax, [esp + 8]
0046ad14  e848d7feff               call 0x458461
0046ad19  31c0                     xor eax, eax
0046ad1b  668b442408               mov ax, word ptr [esp + 8]
0046ad20  69c014010000             imul eax, eax, 0x114
0046ad26  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0046ad2c  01d0                     add eax, edx
0046ad2e  ba8c000000               mov edx, 0x8c
0046ad33  e829d7feff               call 0x458461
0046ad38  ba01000000               mov edx, 1
0046ad3d  b800020000               mov eax, 0x200
0046ad42  e844d7feff               call 0x45848b
0046ad47  31c0                     xor eax, eax
0046ad49  668b442408               mov ax, word ptr [esp + 8]
0046ad4e  69c014010000             imul eax, eax, 0x114
0046ad54  31d2                     xor edx, edx
0046ad56  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
0046ad5c  668b1424                 mov dx, word ptr [esp]
0046ad60  01c8                     add eax, ecx
0046ad62  81ea8c020000             sub edx, 0x28c
0046ad68  058c000000               add eax, 0x8c
0046ad6d  e8efd6feff               call 0x458461
0046ad72  31c0                     xor eax, eax
0046ad74  6689d8                   mov ax, bx
0046ad77  69c014010000             imul eax, eax, 0x114
0046ad7d  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0046ad83  c68402bd00000000         mov byte ptr [edx + eax + 0xbd], 0
0046ad8b  31c0                     xor eax, eax
0046ad8d  668b442408               mov ax, word ptr [esp + 8]
0046ad92  e86872fdff               call 0x441fff
0046ad97  84c0                     test al, al
0046ad99  0f8460ffffff             je 0x46acff
0046ad9f  31c0                     xor eax, eax
0046ada1  668b442408               mov ax, word ptr [esp + 8]
0046ada6  e8a5c5feff               call 0x457350
0046adab  31c0                     xor eax, eax
0046adad  668b442408               mov ax, word ptr [esp + 8]
0046adb2  69c014010000             imul eax, eax, 0x114
0046adb8  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0046adbe  66c784029a0000006400     mov word ptr [edx + eax + 0x9a], 0x64
0046adc8  31c0                     xor eax, eax
0046adca  668b442408               mov ax, word ptr [esp + 8]
0046adcf  69c014010000             imul eax, eax, 0x114
0046add5  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0046addb  01d0                     add eax, edx
0046addd  31d2                     xor edx, edx
0046addf  8a5001                   mov dl, byte ptr [eax + 1]
0046ade2  6bd232                   imul edx, edx, 0x32
0046ade5  8a92d8654900             mov dl, byte ptr [edx + 0x4965d8]
0046adeb  8890bb000000             mov byte ptr [eax + 0xbb], dl
0046adf1  31c0                     xor eax, eax
0046adf3  668b442408               mov ax, word ptr [esp + 8]
0046adf8  69c014010000             imul eax, eax, 0x114
0046adfe  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0046ae04  01d0                     add eax, edx
0046ae06  31d2                     xor edx, edx
0046ae08  8a5001                   mov dl, byte ptr [eax + 1]
0046ae0b  6bd232                   imul edx, edx, 0x32
0046ae0e  8a92da654900             mov dl, byte ptr [edx + 0x4965da]
0046ae14  8890b0000000             mov byte ptr [eax + 0xb0], dl
0046ae1a  31d2                     xor edx, edx
0046ae1c  668b542408               mov dx, word ptr [esp + 8]
0046ae21  69d214010000             imul edx, edx, 0x114
0046ae27  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0046ae2c  c68402bc000000ff         mov byte ptr [edx + eax + 0xbc], 0xff
0046ae34  31d2                     xor edx, edx
0046ae36  668b542408               mov dx, word ptr [esp + 8]
0046ae3b  69d214010000             imul edx, edx, 0x114
0046ae41  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0046ae46  c68402f500000000         mov byte ptr [edx + eax + 0xf5], 0
0046ae4e  31c0                     xor eax, eax
0046ae50  668b442408               mov ax, word ptr [esp + 8]
0046ae55  69d014010000             imul edx, eax, 0x114
0046ae5b  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0046ae60  c68402f700000000         mov byte ptr [edx + eax + 0xf7], 0
0046ae68  31c0                     xor eax, eax
0046ae6a  668b442408               mov ax, word ptr [esp + 8]
0046ae6f  69c014010000             imul eax, eax, 0x114
0046ae75  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0046ae7b  c68402f800000000         mov byte ptr [edx + eax + 0xf8], 0
0046ae83  31c0                     xor eax, eax
0046ae85  668b442408               mov ax, word ptr [esp + 8]
0046ae8a  69d014010000             imul edx, eax, 0x114
0046ae90  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0046ae95  c68402f600000000         mov byte ptr [edx + eax + 0xf6], 0
0046ae9d  31c0                     xor eax, eax
0046ae9f  668b442408               mov ax, word ptr [esp + 8]
0046aea4  69c014010000             imul eax, eax, 0x114
0046aeaa  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0046aeb0  c68402dc00000000         mov byte ptr [edx + eax + 0xdc], 0
0046aeb8  31d2                     xor edx, edx
0046aeba  668b542408               mov dx, word ptr [esp + 8]
0046aebf  69d214010000             imul edx, edx, 0x114
0046aec5  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0046aeca  c7840204010000ffffffff   mov dword ptr [edx + eax + 0x104], 0xffffffff
0046aed5  31c0                     xor eax, eax
0046aed7  668b442408               mov ax, word ptr [esp + 8]
0046aedc  69c014010000             imul eax, eax, 0x114
0046aee2  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0046aee8  c784020c010000ffffffff   mov dword ptr [edx + eax + 0x10c], 0xffffffff
0046aef3  31c0                     xor eax, eax
0046aef5  668b442408               mov ax, word ptr [esp + 8]
0046aefa  69c014010000             imul eax, eax, 0x114
0046af00  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0046af06  c784021001000000000000   mov dword ptr [edx + eax + 0x110], 0
0046af11  31c0                     xor eax, eax
0046af13  668b442408               mov ax, word ptr [esp + 8]
0046af18  69c014010000             imul eax, eax, 0x114
0046af1e  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0046af24  01d0                     add eax, edx
0046af26  31d2                     xor edx, edx
0046af28  8a5002                   mov dl, byte ptr [eax + 2]
0046af2b  83fa0e                   cmp edx, 0xe
0046af2e  7504                     jne 0x46af34
0046af30  c6407200                 mov byte ptr [eax + 0x72], 0
0046af34  31c0                     xor eax, eax
0046af36  668b442408               mov ax, word ptr [esp + 8]
0046af3b  69d014010000             imul edx, eax, 0x114
0046af41  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0046af46  01d0                     add eax, edx
0046af48  31d2                     xor edx, edx
0046af4a  8a5001                   mov dl, byte ptr [eax + 1]
0046af4d  6bd232                   imul edx, edx, 0x32
0046af50  668b92de654900           mov dx, word ptr [edx + 0x4965de]
0046af57  66899002010000           mov word ptr [eax + 0x102], dx
0046af5e  31c0                     xor eax, eax
0046af60  668b442408               mov ax, word ptr [esp + 8]
0046af65  69d014010000             imul edx, eax, 0x114
0046af6b  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0046af70  01d0                     add eax, edx
0046af72  31d2                     xor edx, edx
0046af74  8a5001                   mov dl, byte ptr [eax + 1]
0046af77  83fa04                   cmp edx, 4
0046af7a  7507                     jne 0x46af83
0046af7c  c680da0000000a           mov byte ptr [eax + 0xda], 0xa
0046af83  31c0                     xor eax, eax
0046af85  668b442408               mov ax, word ptr [esp + 8]
0046af8a  69d014010000             imul edx, eax, 0x114
0046af90  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0046af95  8a440201                 mov al, byte ptr [edx + eax + 1]
0046af99  25ff000000               and eax, 0xff
0046af9e  83f810                   cmp eax, 0x10
0046afa1  7405                     je 0x46afa8
0046afa3  83f80e                   cmp eax, 0xe
0046afa6  751a                     jne 0x46afc2
0046afa8  31c0                     xor eax, eax
0046afaa  668b442408               mov ax, word ptr [esp + 8]
0046afaf  69d014010000             imul edx, eax, 0x114
0046afb5  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0046afba  c68402da00000000         mov byte ptr [edx + eax + 0xda], 0
0046afc2  31c0                     xor eax, eax
0046afc4  668b442408               mov ax, word ptr [esp + 8]
0046afc9  69c014010000             imul eax, eax, 0x114
0046afcf  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0046afd5  01d0                     add eax, edx
0046afd7  31d2                     xor edx, edx
0046afd9  8a5001                   mov dl, byte ptr [eax + 1]
0046afdc  83fa10                   cmp edx, 0x10
0046afdf  7503                     jne 0x46afe4
0046afe1  c60000                   mov byte ptr [eax], 0
0046afe4  31c0                     xor eax, eax
0046afe6  668b442408               mov ax, word ptr [esp + 8]
0046afeb  e83570fdff               call 0x442025
0046aff0  25ff000000               and eax, 0xff
0046aff5  e8e372fdff               call 0x4422dd
0046affa  84c0                     test al, al
0046affc  0f84fdfcffff             je 0x46acff
0046b002  31c0                     xor eax, eax
0046b004  668b442408               mov ax, word ptr [esp + 8]
0046b009  69c014010000             imul eax, eax, 0x114
0046b00f  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0046b015  c6040204                 mov byte ptr [edx + eax], 4
0046b019  e9e1fcffff               jmp 0x46acff
