; SortieTroupe; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00420e4c  53                       push ebx
00420e4d  51                       push ecx
00420e4e  56                       push esi
00420e4f  57                       push edi
00420e50  55                       push ebp
00420e51  83ec0c                   sub esp, 0xc
00420e54  50                       push eax
00420e55  8854240c                 mov byte ptr [esp + 0xc], dl
00420e59  31c0                     xor eax, eax
00420e5b  668b0424                 mov ax, word ptr [esp]
00420e5f  89c2                     mov edx, eax
00420e61  c1e204                   shl edx, 4
00420e64  01c2                     add edx, eax
00420e66  c1e202                   shl edx, 2
00420e69  01c2                     add edx, eax
00420e6b  bfc8a04900               mov edi, 0x49a0c8
00420e70  c1e202                   shl edx, 2
00420e73  01d7                     add edi, edx
00420e75  31c0                     xor eax, eax
00420e77  8a477b                   mov al, byte ptr [edi + 0x7b]
00420e7a  e838020200               call 0x4410b7
00420e7f  25ffff0000               and eax, 0xffff
00420e84  89c2                     mov edx, eax
00420e86  c1e202                   shl edx, 2
00420e89  29c2                     sub edx, eax
00420e8b  c1e203                   shl edx, 3
00420e8e  01c2                     add edx, eax
00420e90  8b9f8c000000             mov ebx, dword ptr [edi + 0x8c]
00420e96  c1e202                   shl edx, 2
00420e99  39da                     cmp edx, ebx
00420e9b  0f8749030000             ja 0x4211ea
00420ea1  bb09000000               mov ebx, 9
00420ea6  ba01000000               mov edx, 1
00420eab  8d470c                   lea eax, [edi + 0xc]
00420eae  e837640200               call 0x4472ea
00420eb3  89442404                 mov dword ptr [esp + 4], eax
00420eb7  25ffff0000               and eax, 0xffff
00420ebc  e8e5650200               call 0x4474a6
00420ec1  89c6                     mov esi, eax
00420ec3  bb02000000               mov ebx, 2
00420ec8  89f0                     mov eax, esi
00420eca  89da                     mov edx, ebx
00420ecc  e8e7620200               call 0x4471b8
00420ed1  6685c0                   test ax, ax
00420ed4  742b                     je 0x420f01
00420ed6  bb02000000               mov ebx, 2
00420edb  89f0                     mov eax, esi
00420edd  0fb66f04                 movzx ebp, byte ptr [edi + 4]
00420ee1  31c9                     xor ecx, ecx
00420ee3  89da                     mov edx, ebx
00420ee5  668b0c24                 mov cx, word ptr [esp]
00420ee9  e8fc630200               call 0x4472ea
00420eee  31d2                     xor edx, edx
00420ef0  89eb                     mov ebx, ebp
00420ef2  6689c2                   mov dx, ax
00420ef5  b802000000               mov eax, 2
00420efa  e810250000               call 0x42340f
00420eff  ebc2                     jmp 0x420ec3
00420f01  bb01000000               mov ebx, 1
00420f06  ba02000000               mov edx, 2
00420f0b  89f0                     mov eax, esi
00420f0d  e8a6620200               call 0x4471b8
00420f12  6685c0                   test ax, ax
00420f15  742e                     je 0x420f45
00420f17  bb01000000               mov ebx, 1
00420f1c  ba02000000               mov edx, 2
00420f21  89f0                     mov eax, esi
00420f23  0fb66f04                 movzx ebp, byte ptr [edi + 4]
00420f27  31c9                     xor ecx, ecx
00420f29  e8bc630200               call 0x4472ea
00420f2e  668b0c24                 mov cx, word ptr [esp]
00420f32  31d2                     xor edx, edx
00420f34  89eb                     mov ebx, ebp
00420f36  6689c2                   mov dx, ax
00420f39  b801000000               mov eax, 1
00420f3e  e8cc240000               call 0x42340f
00420f43  ebbc                     jmp 0x420f01
00420f45  31c0                     xor eax, eax
00420f47  31c9                     xor ecx, ecx
00420f49  31db                     xor ebx, ebx
00420f4b  31f6                     xor esi, esi
00420f4d  668b0424                 mov ax, word ptr [esp]
00420f51  8a5c240c                 mov bl, byte ptr [esp + 0xc]
00420f55  668b742404               mov si, word ptr [esp + 4]
00420f5a  e839f7ffff               call 0x420698
00420f5f  0fb7e8                   movzx ebp, ax
00420f62  8a4f7b                   mov cl, byte ptr [edi + 0x7b]
00420f65  89ea                     mov edx, ebp
00420f67  89f0                     mov eax, esi
00420f69  e8196c0300               call 0x457b87
00420f6e  bae8030000               mov edx, 0x3e8
00420f73  89f0                     mov eax, esi
00420f75  e8a8610300               call 0x457122
00420f7a  89f0                     mov eax, esi
00420f7c  e87c210300               call 0x4530fd
00420f81  89f0                     mov eax, esi
00420f83  89ea                     mov edx, ebp
00420f85  e8b8ee0200               call 0x44fe42
00420f8a  89f0                     mov eax, esi
00420f8c  e82b500200               call 0x445fbc
00420f91  31d2                     xor edx, edx
00420f93  89f0                     mov eax, esi
00420f95  668b577c                 mov dx, word ptr [edi + 0x7c]
00420f99  e835480200               call 0x4457d3
00420f9e  8a4704                   mov al, byte ptr [edi + 4]
00420fa1  3a0541805000             cmp al, byte ptr [0x508041]
00420fa7  750e                     jne 0x420fb7
00420fa9  ba06000000               mov edx, 6
00420fae  89f0                     mov eax, esi
00420fb0  31db                     xor ebx, ebx
00420fb2  e8a7fd0100               call 0x440d5e
00420fb7  31c0                     xor eax, eax
00420fb9  668b0424                 mov ax, word ptr [esp]
00420fbd  89c2                     mov edx, eax
00420fbf  c1e204                   shl edx, 4
00420fc2  01c2                     add edx, eax
00420fc4  c1e202                   shl edx, 2
00420fc7  01c2                     add edx, eax
00420fc9  c1e202                   shl edx, 2
00420fcc  81c2c8a04900             add edx, 0x49a0c8
00420fd2  31db                     xor ebx, ebx
00420fd4  8a4208                   mov al, byte ptr [edx + 8]
00420fd7  88c3                     mov bl, al
00420fd9  8d420c                   lea eax, [edx + 0xc]
00420fdc  83fb15                   cmp ebx, 0x15
00420fdf  750d                     jne 0x420fee
00420fe1  e864620200               call 0x44724a
00420fe6  84c0                     test al, al
00420fe8  7429                     je 0x421013
00420fea  b001                     mov al, 1
00420fec  eb27                     jmp 0x421015
00420fee  83fb02                   cmp ebx, 2
00420ff1  7509                     jne 0x420ffc
00420ff3  e852620200               call 0x44724a
00420ff8  84c0                     test al, al
00420ffa  75ee                     jne 0x420fea
00420ffc  8d420c                   lea eax, [edx + 0xc]
00420fff  bb09000000               mov ebx, 9
00421004  ba01000000               mov edx, 1
00421009  e8aa610200               call 0x4471b8
0042100e  6685c0                   test ax, ax
00421011  ebd5                     jmp 0x420fe8
00421013  30c0                     xor al, al
00421015  84c0                     test al, al
00421017  0f8536010000             jne 0x421153
0042101d  8b1c24                   mov ebx, dword ptr [esp]
00421020  31c0                     xor eax, eax
00421022  6689d8                   mov ax, bx
00421025  89c2                     mov edx, eax
00421027  c1e204                   shl edx, 4
0042102a  01c2                     add edx, eax
0042102c  c1e202                   shl edx, 2
0042102f  01c2                     add edx, eax
00421031  b8c8a04900               mov eax, 0x49a0c8
00421036  8a449008                 mov al, byte ptr [eax + edx*4 + 8]
0042103a  3c01                     cmp al, 1
0042103c  7208                     jb 0x421046
0042103e  3c02                     cmp al, 2
00421040  763b                     jbe 0x42107d
00421042  3c05                     cmp al, 5
00421044  7437                     je 0x42107d
00421046  31c0                     xor eax, eax
00421048  668b0424                 mov ax, word ptr [esp]
0042104c  89c2                     mov edx, eax
0042104e  c1e204                   shl edx, 4
00421051  01c2                     add edx, eax
00421053  c1e202                   shl edx, 2
00421056  01c2                     add edx, eax
00421058  b8c8a04900               mov eax, 0x49a0c8
0042105d  8a449008                 mov al, byte ptr [eax + edx*4 + 8]
00421061  25ff000000               and eax, 0xff
00421066  83f809                   cmp eax, 9
00421069  0f84ac000000             je 0x42111b
0042106f  83f80c                   cmp eax, 0xc
00421072  0f85bb010000             jne 0x421233
00421078  e99e000000               jmp 0x42111b
0042107d  31c0                     xor eax, eax
0042107f  6689d8                   mov ax, bx
00421082  89c2                     mov edx, eax
00421084  c1e204                   shl edx, 4
00421087  01c2                     add edx, eax
00421089  c1e202                   shl edx, 2
0042108c  01c2                     add edx, eax
0042108e  c1e202                   shl edx, 2
00421091  81c2c8a04900             add edx, 0x49a0c8
00421097  66c74278ffff             mov word ptr [edx + 0x78], 0xffff
0042109d  c6427bff                 mov byte ptr [edx + 0x7b], 0xff
004210a1  66c7427c0000             mov word ptr [edx + 0x7c], 0
004210a7  31c0                     xor eax, eax
004210a9  66c7427e0000             mov word ptr [edx + 0x7e], 0
004210af  8a4208                   mov al, byte ptr [edx + 8]
004210b2  66c78286000000ffff       mov word ptr [edx + 0x86], 0xffff
004210bb  83f814                   cmp eax, 0x14
004210be  7412                     je 0x4210d2
004210c0  66c782800000000000       mov word ptr [edx + 0x80], 0
004210c9  66c782820000000000       mov word ptr [edx + 0x82], 0
004210d2  c6427400                 mov byte ptr [edx + 0x74], 0
004210d6  31c0                     xor eax, eax
004210d8  8a4205                   mov al, byte ptr [edx + 5]
004210db  c7828c00000000000000     mov dword ptr [edx + 0x8c], 0
004210e5  83f803                   cmp eax, 3
004210e8  0f8458ffffff             je 0x421046
004210ee  c6420505                 mov byte ptr [edx + 5], 5
004210f2  e94fffffff               jmp 0x421046
004210f7  c744240814000000         mov dword ptr [esp + 8], 0x14
004210ff  31c0                     xor eax, eax
00421101  31d2                     xor edx, edx
00421103  668b0424                 mov ax, word ptr [esp]
00421107  668b542408               mov dx, word ptr [esp + 8]
0042110c  e8d19dffff               call 0x41aee2
00421111  25ffff0000               and eax, 0xffff
00421116  e8675d0500               call 0x476e82
0042111b  31c0                     xor eax, eax
0042111d  8a4704                   mov al, byte ptr [edi + 4]
00421120  8b1c24                   mov ebx, dword ptr [esp]
00421123  663b1c45e05b4900         cmp bx, word ptr [eax*2 + 0x495be0]
0042112b  7512                     jne 0x42113f
0042112d  8a4704                   mov al, byte ptr [edi + 4]
00421130  25ff000000               and eax, 0xff
00421135  66c70445e05b4900ffff     mov word ptr [eax*2 + 0x495be0], 0xffff
0042113f  31c0                     xor eax, eax
00421141  ba01000000               mov edx, 1
00421146  668b0424                 mov ax, word ptr [esp]
0042114a  c64704c8                 mov byte ptr [edi + 4], 0xc8
0042114e  e8448dffff               call 0x419e97
00421153  31c0                     xor eax, eax
00421155  668b0424                 mov ax, word ptr [esp]
00421159  89c2                     mov edx, eax
0042115b  c1e204                   shl edx, 4
0042115e  01c2                     add edx, eax
00421160  c1e202                   shl edx, 2
00421163  01c2                     add edx, eax
00421165  c1e202                   shl edx, 2
00421168  81c2c8a04900             add edx, 0x49a0c8
0042116e  66c74278ffff             mov word ptr [edx + 0x78], 0xffff
00421174  c6427bff                 mov byte ptr [edx + 0x7b], 0xff
00421178  66c7427c0000             mov word ptr [edx + 0x7c], 0
0042117e  31c0                     xor eax, eax
00421180  66c7427e0000             mov word ptr [edx + 0x7e], 0
00421186  8a4208                   mov al, byte ptr [edx + 8]
00421189  66c78286000000ffff       mov word ptr [edx + 0x86], 0xffff
00421192  83f814                   cmp eax, 0x14
00421195  7412                     je 0x4211a9
00421197  66c782800000000000       mov word ptr [edx + 0x80], 0
004211a0  66c782820000000000       mov word ptr [edx + 0x82], 0
004211a9  c6427400                 mov byte ptr [edx + 0x74], 0
004211ad  31c0                     xor eax, eax
004211af  8a4205                   mov al, byte ptr [edx + 5]
004211b2  c7828c00000000000000     mov dword ptr [edx + 0x8c], 0
004211bc  83f803                   cmp eax, 3
004211bf  7404                     je 0x4211c5
004211c1  c6420505                 mov byte ptr [edx + 5], 5
004211c5  ba46000000               mov edx, 0x46
004211ca  31c0                     xor eax, eax
004211cc  31db                     xor ebx, ebx
004211ce  668b442404               mov ax, word ptr [esp + 4]
004211d3  e8f0170600               call 0x4829c8
004211d8  ba03000000               mov edx, 3
004211dd  31c0                     xor eax, eax
004211df  31db                     xor ebx, ebx
004211e1  668b0424                 mov ax, word ptr [esp]
004211e5  e81e360600               call 0x484808
004211ea  83c410                   add esp, 0x10
004211ed  e9a8270000               jmp 0x42399a
004211f2  c74424080a000000         mov dword ptr [esp + 8], 0xa
004211fa  e900ffffff               jmp 0x4210ff
004211ff  c744240808000000         mov dword ptr [esp + 8], 8
00421207  e9f3feffff               jmp 0x4210ff
0042120c  c744240804000000         mov dword ptr [esp + 8], 4
00421214  e9e6feffff               jmp 0x4210ff
00421219  c744240805000000         mov dword ptr [esp + 8], 5
00421221  e9d9feffff               jmp 0x4210ff
00421226  c744240807000000         mov dword ptr [esp + 8], 7
0042122e  e9ccfeffff               jmp 0x4210ff
00421233  31db                     xor ebx, ebx
00421235  8a4708                   mov al, byte ptr [edi + 8]
00421238  8a5f04                   mov bl, byte ptr [edi + 4]
0042123b  3c15                     cmp al, 0x15
0042123d  0f87bcfeffff             ja 0x4210ff
00421243  25ff000000               and eax, 0xff
00421248  2eff2485f40d4200         jmp dword ptr cs:[eax*4 + 0x420df4]
