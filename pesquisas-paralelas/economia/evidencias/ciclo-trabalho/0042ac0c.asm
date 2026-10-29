; InputGame building press with troops 0x42ac0c..0x42b26e; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0042ac0c  31c0                     xor eax, eax
0042ac0e  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042ac14  3dffff0000               cmp eax, 0xffff
0042ac19  0f84f2060000             je 0x42b311
0042ac1f  0fb67dfc                 movzx edi, byte ptr [ebp - 4]
0042ac23  89f8                     mov eax, edi
0042ac25  e813790400               call 0x47253d
0042ac2a  84c0                     test al, al
0042ac2c  0f8409060000             je 0x42b23b
0042ac32  31c0                     xor eax, eax
0042ac34  66a1ae054e00             mov ax, word ptr [0x4e05ae]
0042ac3a  83f808                   cmp eax, 8
0042ac3d  0f8568010000             jne 0x42adab
0042ac43  31c0                     xor eax, eax
0042ac45  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042ac4b  e83cf4feff               call 0x41a08c
0042ac50  3a45fc                   cmp al, byte ptr [ebp - 4]
0042ac53  0f85f1000000             jne 0x42ad4a
0042ac59  31c0                     xor eax, eax
0042ac5b  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042ac61  e88ef8feff               call 0x41a4f4
0042ac66  25ff000000               and eax, 0xff
0042ac6b  83f803                   cmp eax, 3
0042ac6e  0f85d6000000             jne 0x42ad4a
0042ac74  ba05000000               mov edx, 5
0042ac79  89f8                     mov eax, edi
0042ac7b  e8ae770400               call 0x47242e
0042ac80  84c0                     test al, al
0042ac82  7524                     jne 0x42aca8
0042ac84  ba07000000               mov edx, 7
0042ac89  89f8                     mov eax, edi
0042ac8b  e89e770400               call 0x47242e
0042ac90  84c0                     test al, al
0042ac92  7514                     jne 0x42aca8
0042ac94  ba06000000               mov edx, 6
0042ac99  89f8                     mov eax, edi
0042ac9b  e88e770400               call 0x47242e
0042aca0  84c0                     test al, al
0042aca2  0f84a2000000             je 0x42ad4a
0042aca8  bb03000000               mov ebx, 3
0042acad  a1848f5000               mov eax, dword ptr [0x508f84]
0042acb2  31d2                     xor edx, edx
0042acb4  f7f3                     div ebx
0042acb6  66c70510a049003d1e       mov word ptr [0x49a010], 0x1e3d
0042acbf  8a1dae995000             mov bl, byte ptr [0x5099ae]
0042acc5  891514a04900             mov dword ptr [0x49a014], edx
0042accb  84db                     test bl, bl
0042accd  0f84810b0000             je 0x42b854
0042acd3  803daf99500000           cmp byte ptr [0x5099af], 0
0042acda  0f84740b0000             je 0x42b854
0042ace0  bf09000000               mov edi, 9
0042ace5  b803000000               mov eax, 3
0042acea  ba07000000               mov edx, 7
0042acef  31db                     xor ebx, ebx
0042acf1  66a3b0054e00             mov word ptr [0x4e05b0], ax
0042acf7  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042acfd  8a5dfc                   mov bl, byte ptr [ebp - 4]
0042ad00  66a3b2054e00             mov word ptr [0x4e05b2], ax
0042ad06  89d8                     mov eax, ebx
0042ad08  66893dae054e00           mov word ptr [0x4e05ae], di
0042ad0f  e81a770400               call 0x47242e
0042ad14  84c0                     test al, al
0042ad16  740c                     je 0x42ad24
0042ad18  c605b4054e0002           mov byte ptr [0x4e05b4], 2
0042ad1f  e9300b0000               jmp 0x42b854
0042ad24  ba05000000               mov edx, 5
0042ad29  89d8                     mov eax, ebx
0042ad2b  e8fe760400               call 0x47242e
0042ad30  84c0                     test al, al
0042ad32  740c                     je 0x42ad40
0042ad34  c605b4054e0001           mov byte ptr [0x4e05b4], 1
0042ad3b  e9140b0000               jmp 0x42b854
0042ad40  a2b4054e00               mov byte ptr [0x4e05b4], al
0042ad45  e90a0b0000               jmp 0x42b854
0042ad4a  31d2                     xor edx, edx
0042ad4c  bb0e1e0000               mov ebx, 0x1e0e
0042ad51  891514a04900             mov dword ptr [0x49a014], edx
0042ad57  8a15ae995000             mov dl, byte ptr [0x5099ae]
0042ad5d  66891d10a04900           mov word ptr [0x49a010], bx
0042ad64  84d2                     test dl, dl
0042ad66  0f84e80a0000             je 0x42b854
0042ad6c  803daf99500000           cmp byte ptr [0x5099af], 0
0042ad73  0f84db0a0000             je 0x42b854
0042ad79  6a00                     push 0
0042ad7b  ba05000000               mov edx, 5
0042ad80  31db                     xor ebx, ebx
0042ad82  31c0                     xor eax, eax
0042ad84  31c9                     xor ecx, ecx
0042ad86  6a00                     push 0
0042ad88  8a45fc                   mov al, byte ptr [ebp - 4]
0042ad8b  6689f3                   mov bx, si
0042ad8e  e8413f0300               call 0x45ecd4
0042ad93  b9031e0000               mov ecx, 0x1e03
0042ad98  66893504624900           mov word ptr [0x496204], si
0042ad9f  66890dac054e00           mov word ptr [0x4e05ac], cx
0042ada6  e9a90a0000               jmp 0x42b854
0042adab  31c0                     xor eax, eax
0042adad  89fa                     mov edx, edi
0042adaf  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042adb5  e862f8feff               call 0x41a61c
0042adba  84c0                     test al, al
0042adbc  0f8417010000             je 0x42aed9
0042adc2  31c0                     xor eax, eax
0042adc4  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042adca  e85c22ffff               call 0x41d02b
0042adcf  84c0                     test al, al
0042add1  0f8502010000             jne 0x42aed9
0042add7  31c0                     xor eax, eax
0042add9  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042addf  e810f7feff               call 0x41a4f4
0042ade4  25ff000000               and eax, 0xff
0042ade9  83f810                   cmp eax, 0x10
0042adec  7417                     je 0x42ae05
0042adee  31c0                     xor eax, eax
0042adf0  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042adf6  e8f9f6feff               call 0x41a4f4
0042adfb  25ff000000               and eax, 0xff
0042ae00  83f802                   cmp eax, 2
0042ae03  7556                     jne 0x42ae5b
0042ae05  0fb67dfc                 movzx edi, byte ptr [ebp - 4]
0042ae09  ba0a000000               mov edx, 0xa
0042ae0e  89f8                     mov eax, edi
0042ae10  e819760400               call 0x47242e
0042ae15  84c0                     test al, al
0042ae17  7442                     je 0x42ae5b
0042ae19  bb6f1e0000               mov ebx, 0x1e6f
0042ae1e  a1808f5000               mov eax, dword ptr [0x508f80]
0042ae23  8a15ae995000             mov dl, byte ptr [0x5099ae]
0042ae29  83e001                   and eax, 1
0042ae2c  66891d10a04900           mov word ptr [0x49a010], bx
0042ae33  a314a04900               mov dword ptr [0x49a014], eax
0042ae38  84d2                     test dl, dl
0042ae3a  0f84140a0000             je 0x42b854
0042ae40  803daf99500000           cmp byte ptr [0x5099af], 0
0042ae47  0f84070a0000             je 0x42b854
0042ae4d  6a00                     push 0
0042ae4f  bb03000000               mov ebx, 3
0042ae54  ba10000000               mov edx, 0x10
0042ae59  eb67                     jmp 0x42aec2
0042ae5b  0fb67dfc                 movzx edi, byte ptr [ebp - 4]
0042ae5f  31db                     xor ebx, ebx
0042ae61  ba03000000               mov edx, 3
0042ae66  668b1dc46a4900           mov bx, word ptr [0x496ac4]
0042ae6d  89f8                     mov eax, edi
0042ae6f  e8e1740400               call 0x472355
0042ae74  84c0                     test al, al
0042ae76  0f84d8090000             je 0x42b854
0042ae7c  bafd1d0000               mov edx, 0x1dfd
0042ae81  bb06000000               mov ebx, 6
0042ae86  a1808f5000               mov eax, dword ptr [0x508f80]
0042ae8b  66891510a04900           mov word ptr [0x49a010], dx
0042ae92  31d2                     xor edx, edx
0042ae94  f7f3                     div ebx
0042ae96  a0ae995000               mov al, byte ptr [0x5099ae]
0042ae9b  891514a04900             mov dword ptr [0x49a014], edx
0042aea1  84c0                     test al, al
0042aea3  0f84ab090000             je 0x42b854
0042aea9  803daf99500000           cmp byte ptr [0x5099af], 0
0042aeb0  0f849e090000             je 0x42b854
0042aeb6  6a00                     push 0
0042aeb8  bb03000000               mov ebx, 3
0042aebd  ba0e000000               mov edx, 0xe
0042aec2  31c9                     xor ecx, ecx
0042aec4  6a00                     push 0
0042aec6  89f8                     mov eax, edi
0042aec8  668b0dc46a4900           mov cx, word ptr [0x496ac4]
0042aecf  e8003e0300               call 0x45ecd4
0042aed4  e97b090000               jmp 0x42b854
0042aed9  bb05000000               mov ebx, 5
0042aede  a1808f5000               mov eax, dword ptr [0x508f80]
0042aee3  31d2                     xor edx, edx
0042aee5  f7f3                     div ebx
0042aee7  89d0                     mov eax, edx
0042aee9  b9f01d0000               mov ecx, 0x1df0
0042aeee  31d0                     xor eax, edx
0042aef0  66890d10a04900           mov word ptr [0x49a010], cx
0042aef7  8a45fc                   mov al, byte ptr [ebp - 4]
0042aefa  891514a04900             mov dword ptr [0x49a014], edx
0042af00  e8a3720400               call 0x4721a8
0042af05  25ffff0000               and eax, 0xffff
0042af0a  e816710100               call 0x442025
0042af0f  25ff000000               and eax, 0xff
0042af14  83f807                   cmp eax, 7
0042af17  0f8596000000             jne 0x42afb3
0042af1d  31c0                     xor eax, eax
0042af1f  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042af25  e82817ffff               call 0x41c652
0042af2a  84c0                     test al, al
0042af2c  7412                     je 0x42af40
0042af2e  31c0                     xor eax, eax
0042af30  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042af36  e83bfafeff               call 0x41a976
0042af3b  6685c0                   test ax, ax
0042af3e  7473                     je 0x42afb3
0042af40  b8101e0000               mov eax, 0x1e10
0042af45  bb06000000               mov ebx, 6
0042af4a  31d2                     xor edx, edx
0042af4c  66a310a04900             mov word ptr [0x49a010], ax
0042af52  a1808f5000               mov eax, dword ptr [0x508f80]
0042af57  f7f3                     div ebx
0042af59  8a0dae995000             mov cl, byte ptr [0x5099ae]
0042af5f  891514a04900             mov dword ptr [0x49a014], edx
0042af65  84c9                     test cl, cl
0042af67  0f84e7080000             je 0x42b854
0042af6d  803daf99500000           cmp byte ptr [0x5099af], 0
0042af74  0f84da080000             je 0x42b854
0042af7a  6a00                     push 0
0042af7c  bb03000000               mov ebx, 3
0042af81  ba14000000               mov edx, 0x14
0042af86  31c9                     xor ecx, ecx
0042af88  31c0                     xor eax, eax
0042af8a  6a00                     push 0
0042af8c  8a45fc                   mov al, byte ptr [ebp - 4]
0042af8f  668b0dc46a4900           mov cx, word ptr [0x496ac4]
0042af96  e8393d0300               call 0x45ecd4
0042af9b  ba031e0000               mov edx, 0x1e03
0042afa0  66893504624900           mov word ptr [0x496204], si
0042afa7  668915ac054e00           mov word ptr [0x4e05ac], dx
0042afae  e9a1080000               jmp 0x42b854
0042afb3  31d2                     xor edx, edx
0042afb5  8a55fc                   mov dl, byte ptr [ebp - 4]
0042afb8  89d0                     mov eax, edx
0042afba  e83a720400               call 0x4721f9
0042afbf  84c0                     test al, al
0042afc1  0f84d3000000             je 0x42b09a
0042afc7  31c0                     xor eax, eax
0042afc9  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042afcf  e8b8f0feff               call 0x41a08c
0042afd4  38d0                     cmp al, dl
0042afd6  0f85be000000             jne 0x42b09a
0042afdc  89d0                     mov eax, edx
0042afde  e8d1790400               call 0x4729b4
0042afe3  84c0                     test al, al
0042afe5  7417                     je 0x42affe
0042afe7  31c0                     xor eax, eax
0042afe9  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042afef  e800f5feff               call 0x41a4f4
0042aff4  25ff000000               and eax, 0xff
0042aff9  83f813                   cmp eax, 0x13
0042affc  7429                     je 0x42b027
0042affe  31c0                     xor eax, eax
0042b000  8a45fc                   mov al, byte ptr [ebp - 4]
0042b003  e8047a0400               call 0x472a0c
0042b008  84c0                     test al, al
0042b00a  0f848a000000             je 0x42b09a
0042b010  31c0                     xor eax, eax
0042b012  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042b018  e8d7f4feff               call 0x41a4f4
0042b01d  25ff000000               and eax, 0xff
0042b022  83f80e                   cmp eax, 0xe
0042b025  7573                     jne 0x42b09a
0042b027  0fb67dfc                 movzx edi, byte ptr [ebp - 4]
0042b02b  89f8                     mov eax, edi
0042b02d  e8327a0400               call 0x472a64
0042b032  84c0                     test al, al
0042b034  7564                     jne 0x42b09a
0042b036  31c0                     xor eax, eax
0042b038  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042b03e  e80f16ffff               call 0x41c652
0042b043  84c0                     test al, al
0042b045  0f8409080000             je 0x42b854
0042b04b  be3b1e0000               mov esi, 0x1e3b
0042b050  a1808f5000               mov eax, dword ptr [0x508f80]
0042b055  8a3dae995000             mov bh, byte ptr [0x5099ae]
0042b05b  83e001                   and eax, 1
0042b05e  66893510a04900           mov word ptr [0x49a010], si
0042b065  a314a04900               mov dword ptr [0x49a014], eax
0042b06a  84ff                     test bh, bh
0042b06c  0f84e2070000             je 0x42b854
0042b072  803daf99500000           cmp byte ptr [0x5099af], 0
0042b079  0f84d5070000             je 0x42b854
0042b07f  6a00                     push 0
0042b081  ba15000000               mov edx, 0x15
0042b086  89f8                     mov eax, edi
0042b088  31db                     xor ebx, ebx
0042b08a  6a00                     push 0
0042b08c  31c9                     xor ecx, ecx
0042b08e  668b1dc46a4900           mov bx, word ptr [0x496ac4]
0042b095  e935feffff               jmp 0x42aecf
0042b09a  0fb67dfc                 movzx edi, byte ptr [ebp - 4]
0042b09e  31db                     xor ebx, ebx
0042b0a0  ba03000000               mov edx, 3
0042b0a5  668b1dc46a4900           mov bx, word ptr [0x496ac4]
0042b0ac  89f8                     mov eax, edi
0042b0ae  e8b97a0400               call 0x472b6c
0042b0b3  84c0                     test al, al
0042b0b5  0f84f0000000             je 0x42b1ab
0042b0bb  89f8                     mov eax, edi
0042b0bd  e8a2790400               call 0x472a64
0042b0c2  84c0                     test al, al
0042b0c4  0f85e1000000             jne 0x42b1ab
0042b0ca  31c0                     xor eax, eax
0042b0cc  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042b0d2  e87b15ffff               call 0x41c652
0042b0d7  84c0                     test al, al
0042b0d9  0f848a000000             je 0x42b169
0042b0df  bb161e0000               mov ebx, 0x1e16
0042b0e4  a1808f5000               mov eax, dword ptr [0x508f80]
0042b0e9  31d2                     xor edx, edx
0042b0eb  66891d10a04900           mov word ptr [0x49a010], bx
0042b0f2  bb06000000               mov ebx, 6
0042b0f7  f7f3                     div ebx
0042b0f9  89d0                     mov eax, edx
0042b0fb  31d0                     xor eax, edx
0042b0fd  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042b103  891514a04900             mov dword ptr [0x49a014], edx
0042b109  e8e6f3feff               call 0x41a4f4
0042b10e  25ff000000               and eax, 0xff
0042b113  83f815                   cmp eax, 0x15
0042b116  751d                     jne 0x42b135
0042b118  bb09000000               mov ebx, 9
0042b11d  a1808f5000               mov eax, dword ptr [0x508f80]
0042b122  31d2                     xor edx, edx
0042b124  f7f3                     div ebx
0042b126  66c70510a04900ac1e       mov word ptr [0x49a010], 0x1eac
0042b12f  891514a04900             mov dword ptr [0x49a014], edx
0042b135  803dae99500000           cmp byte ptr [0x5099ae], 0
0042b13c  0f8412070000             je 0x42b854
0042b142  803daf99500000           cmp byte ptr [0x5099af], 0
0042b149  0f8405070000             je 0x42b854
0042b14f  6a00                     push 0
0042b151  bb03000000               mov ebx, 3
0042b156  ba10000000               mov edx, 0x10
0042b15b  31c9                     xor ecx, ecx
0042b15d  31c0                     xor eax, eax
0042b15f  6a00                     push 0
0042b161  8a45fc                   mov al, byte ptr [ebp - 4]
0042b164  e95ffdffff               jmp 0x42aec8
0042b169  66c70510a049000e1e       mov word ptr [0x49a010], 0x1e0e
0042b172  31c0                     xor eax, eax
0042b174  8a2dae995000             mov ch, byte ptr [0x5099ae]
0042b17a  a314a04900               mov dword ptr [0x49a014], eax
0042b17f  84ed                     test ch, ch
0042b181  0f84cd060000             je 0x42b854
0042b187  803daf99500000           cmp byte ptr [0x5099af], 0
0042b18e  0f84c0060000             je 0x42b854
0042b194  6a00                     push 0
0042b196  ba05000000               mov edx, 5
0042b19b  89f8                     mov eax, edi
0042b19d  31db                     xor ebx, ebx
0042b19f  6a00                     push 0
0042b1a1  31c9                     xor ecx, ecx
0042b1a3  6689f3                   mov bx, si
0042b1a6  e9ebfdffff               jmp 0x42af96
0042b1ab  31c0                     xor eax, eax
0042b1ad  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042b1b3  8a75fc                   mov dh, byte ptr [ebp - 4]
0042b1b6  e8d1eefeff               call 0x41a08c
0042b1bb  38f0                     cmp al, dh
0042b1bd  0f8591060000             jne 0x42b854
0042b1c3  bb05000000               mov ebx, 5
0042b1c8  a1808f5000               mov eax, dword ptr [0x508f80]
0042b1cd  31d2                     xor edx, edx
0042b1cf  f7f3                     div ebx
0042b1d1  66c70510a04900f01d       mov word ptr [0x49a010], 0x1df0
0042b1da  8a1dae995000             mov bl, byte ptr [0x5099ae]
0042b1e0  891514a04900             mov dword ptr [0x49a014], edx
0042b1e6  84db                     test bl, bl
0042b1e8  0f8466060000             je 0x42b854
0042b1ee  66a1a8995000             mov ax, word ptr [0x5099a8]
0042b1f4  66a324a04900             mov word ptr [0x49a024], ax
0042b1fa  66a1aa995000             mov ax, word ptr [0x5099aa]
0042b200  66a326a04900             mov word ptr [0x49a026], ax
0042b206  66a1a8995000             mov ax, word ptr [0x5099a8]
0042b20c  b701                     mov bh, 1
0042b20e  40                       inc eax
0042b20f  668935b2194e00           mov word ptr [0x4e19b2], si
0042b216  66a328a04900             mov word ptr [0x49a028], ax
0042b21c  66a1aa995000             mov ax, word ptr [0x5099aa]
0042b222  668935b4194e00           mov word ptr [0x4e19b4], si
0042b229  40                       inc eax
0042b22a  883db0194e00             mov byte ptr [0x4e19b0], bh
0042b230  66a32aa04900             mov word ptr [0x49a02a], ax
0042b236  e919060000               jmp 0x42b854
0042b23b  89f8                     mov eax, edi
0042b23d  e874f2feff               call 0x41a4b6
0042b242  668b0dc46a4900           mov cx, word ptr [0x496ac4]
0042b249  6639c8                   cmp ax, cx
0042b24c  7520                     jne 0x42b26e
0042b24e  803db099500000           cmp byte ptr [0x5099b0], 0
0042b255  7417                     je 0x42b26e
0042b257  6a00                     push 0
0042b259  ba21000000               mov edx, 0x21
0042b25e  89f8                     mov eax, edi
0042b260  31db                     xor ebx, ebx
0042b262  6a00                     push 0
0042b264  6689cb                   mov bx, cx
0042b267  31c9                     xor ecx, ecx
0042b269  e961fcffff               jmp 0x42aecf
