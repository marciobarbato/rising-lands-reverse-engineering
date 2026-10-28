; iagRessInit (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x00484bc4..0x00484dd0 (end exclusive); labels are original SBL names
00484bc4  53                       push ebx
00484bc5  52                       push edx
00484bc6  bb64000000               mov ebx, 0x64
00484bcb  ba10504900               mov edx, 0x495010
00484bd0  b81b504900               mov eax, 0x49501b
00484bd5  e87ab0ffff               call 0x47fc54 ; -> iaConfigGetValue
00484bda  bb20030000               mov ebx, 0x320
00484bdf  ba20504900               mov edx, 0x495020
00484be4  a3388c4900               mov dword ptr [0x498c38], eax
00484be9  b82d504900               mov eax, 0x49502d
00484bee  e861b0ffff               call 0x47fc54 ; -> iaConfigGetValue
00484bf3  bb64000000               mov ebx, 0x64
00484bf8  ba32504900               mov edx, 0x495032
00484bfd  a33c8c4900               mov dword ptr [0x498c3c], eax
00484c02  b83e504900               mov eax, 0x49503e
00484c07  e848b0ffff               call 0x47fc54 ; -> iaConfigGetValue
00484c0c  bbe8030000               mov ebx, 0x3e8
00484c11  ba43504900               mov edx, 0x495043
00484c16  a3408c4900               mov dword ptr [0x498c40], eax
00484c1b  b84f504900               mov eax, 0x49504f
00484c20  e82fb0ffff               call 0x47fc54 ; -> iaConfigGetValue
00484c25  bb14000000               mov ebx, 0x14
00484c2a  ba54504900               mov edx, 0x495054
00484c2f  a3448c4900               mov dword ptr [0x498c44], eax
00484c34  b86c504900               mov eax, 0x49506c
00484c39  e816b0ffff               call 0x47fc54 ; -> iaConfigGetValue
00484c3e  bb05000000               mov ebx, 5
00484c43  ba71504900               mov edx, 0x495071
00484c48  a34c8c4900               mov dword ptr [0x498c4c], eax
00484c4d  b88b504900               mov eax, 0x49508b
00484c52  e8fdafffff               call 0x47fc54 ; -> iaConfigGetValue
00484c57  bb01000000               mov ebx, 1
00484c5c  ba90504900               mov edx, 0x495090
00484c61  a3508c4900               mov dword ptr [0x498c50], eax
00484c66  b8a9504900               mov eax, 0x4950a9
00484c6b  e8e4afffff               call 0x47fc54 ; -> iaConfigGetValue
00484c70  a3548c4900               mov dword ptr [0x498c54], eax
00484c75  bb01000000               mov ebx, 1
00484c7a  baae504900               mov edx, 0x4950ae
00484c7f  b8c7504900               mov eax, 0x4950c7
00484c84  e8cbafffff               call 0x47fc54 ; -> iaConfigGetValue
00484c89  bacc504900               mov edx, 0x4950cc
00484c8e  a3588c4900               mov dword ptr [0x498c58], eax
00484c93  31db                     xor ebx, ebx
00484c95  b8e2504900               mov eax, 0x4950e2
00484c9a  e8b5afffff               call 0x47fc54 ; -> iaConfigGetValue
00484c9f  bb1e000000               mov ebx, 0x1e
00484ca4  bae7504900               mov edx, 0x4950e7
00484ca9  a3608c4900               mov dword ptr [0x498c60], eax
00484cae  b8ff504900               mov eax, 0x4950ff
00484cb3  e89cafffff               call 0x47fc54 ; -> iaConfigGetValue
00484cb8  bb1e000000               mov ebx, 0x1e
00484cbd  ba04514900               mov edx, 0x495104
00484cc2  a3708c4900               mov dword ptr [0x498c70], eax
00484cc7  b81b514900               mov eax, 0x49511b
00484ccc  e883afffff               call 0x47fc54 ; -> iaConfigGetValue
00484cd1  bb14000000               mov ebx, 0x14
00484cd6  ba20514900               mov edx, 0x495120
00484cdb  a3808c4900               mov dword ptr [0x498c80], eax
00484ce0  b837514900               mov eax, 0x495137
00484ce5  e86aafffff               call 0x47fc54 ; -> iaConfigGetValue
00484cea  bb64000000               mov ebx, 0x64
00484cef  ba3c514900               mov edx, 0x49513c
00484cf4  a3908c4900               mov dword ptr [0x498c90], eax
00484cf9  b850514900               mov eax, 0x495150
00484cfe  e851afffff               call 0x47fc54 ; -> iaConfigGetValue
00484d03  bb64000000               mov ebx, 0x64
00484d08  ba55514900               mov edx, 0x495155
00484d0d  a3dcbc5100               mov dword ptr [0x51bcdc], eax
00484d12  b868514900               mov eax, 0x495168
00484d17  e838afffff               call 0x47fc54 ; -> iaConfigGetValue
00484d1c  bb64000000               mov ebx, 0x64
00484d21  ba6d514900               mov edx, 0x49516d
00484d26  a3e0bc5100               mov dword ptr [0x51bce0], eax
00484d2b  b882514900               mov eax, 0x495182
00484d30  e81fafffff               call 0x47fc54 ; -> iaConfigGetValue
00484d35  bb05000000               mov ebx, 5
00484d3a  ba87514900               mov edx, 0x495187
00484d3f  a3e4bc5100               mov dword ptr [0x51bce4], eax
00484d44  b892514900               mov eax, 0x495192
00484d49  e806afffff               call 0x47fc54 ; -> iaConfigGetValue
00484d4e  bb50000000               mov ebx, 0x50
00484d53  ba97514900               mov edx, 0x495197
00484d58  a3e8bc5100               mov dword ptr [0x51bce8], eax
00484d5d  b8ab514900               mov eax, 0x4951ab
00484d62  e8edaeffff               call 0x47fc54 ; -> iaConfigGetValue
00484d67  bb05000000               mov ebx, 5
00484d6c  bab0514900               mov edx, 0x4951b0
00484d71  a3ecbc5100               mov dword ptr [0x51bcec], eax
00484d76  b8ba514900               mov eax, 0x4951ba
00484d7b  e8d4aeffff               call 0x47fc54 ; -> iaConfigGetValue
00484d80  a3f0bc5100               mov dword ptr [0x51bcf0], eax
00484d85  83f805                   cmp eax, 5
00484d88  7f05                     jg 0x484d8f
00484d8a  83f802                   cmp eax, 2
00484d8d  7d0a                     jge 0x484d99
00484d8f  c705f0bc510005000000     mov dword ptr [0x51bcf0], 5
00484d99  bb03000000               mov ebx, 3
00484d9e  babf514900               mov edx, 0x4951bf
00484da3  b8d6514900               mov eax, 0x4951d6
00484da8  e8a7aeffff               call 0x47fc54 ; -> iaConfigGetValue
00484dad  bb02000000               mov ebx, 2
00484db2  badb514900               mov edx, 0x4951db
00484db7  a3f4bc5100               mov dword ptr [0x51bcf4], eax
00484dbc  b8f0514900               mov eax, 0x4951f0
00484dc1  e88eaeffff               call 0x47fc54 ; -> iaConfigGetValue
00484dc6  a3f8bc5100               mov dword ptr [0x51bcf8], eax
00484dcb  31c0                     xor eax, eax
00484dcd  5a                       pop edx
00484dce  5b                       pop ebx
00484dcf  c3                       ret
