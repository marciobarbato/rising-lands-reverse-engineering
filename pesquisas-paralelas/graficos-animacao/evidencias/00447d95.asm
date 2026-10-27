; AnimRechargeEngin [0x447d95, 0x447e12)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00447d95  53                     push     ebx
00447d96  51                     push     ecx
00447d97  52                     push     edx
00447d98  25ffff0000             and      eax, 0xffff
00447d9d  89c3                   mov      ebx, eax
00447d9f  c1e304                 shl      ebx, 4
00447da2  01c3                   add      ebx, eax
00447da4  c1e302                 shl      ebx, 2
00447da7  8d1418                 lea      edx, [eax + ebx]
00447daa  8b1da0194e00           mov      ebx, dword ptr [0x4e19a0]
00447db0  c1e202                 shl      edx, 2
00447db3  01d3                   add      ebx, edx
00447db5  8a5301                 mov      dl, byte ptr [ebx + 1]
00447db8  80fa10                 cmp      dl, 0x10
00447dbb  7207                   jb       0x447dc4
00447dbd  7612                   jbe      0x447dd1
00447dbf  80fa11                 cmp      dl, 0x11
00447dc2  7404                   je       0x447dc8
00447dc4  5a                     pop      edx
00447dc5  59                     pop      ecx
00447dc6  5b                     pop      ebx
00447dc7  c3                     ret      
00447dc8  e862fdffff             call     0x447b2f ; AnimBallonStatic
00447dcd  5a                     pop      edx
00447dce  59                     pop      ecx
00447dcf  5b                     pop      ebx
00447dd0  c3                     ret      
00447dd1  8aa3a9000000           mov      ah, byte ptr [ebx + 0xa9]
00447dd7  fec4                   inc      ah
00447dd9  8a93a7000000           mov      dl, byte ptr [ebx + 0xa7]
00447ddf  88a3a9000000           mov      byte ptr [ebx + 0xa9], ah
00447de5  38d4                   cmp      ah, dl
00447de7  75db                   jne      0x447dc4
00447de9  31d2                   xor      edx, edx
00447deb  8a93a4000000           mov      dl, byte ptr [ebx + 0xa4]
00447df1  31c9                   xor      ecx, ecx
00447df3  42                     inc      edx
00447df4  8a8ba5000000           mov      cl, byte ptr [ebx + 0xa5]
00447dfa  89d0                   mov      eax, edx
00447dfc  c1fa1f                 sar      edx, 0x1f
00447dff  f7f9                   idiv     ecx
00447e01  c683a900000000         mov      byte ptr [ebx + 0xa9], 0
00447e08  8893a4000000           mov      byte ptr [ebx + 0xa4], dl
00447e0e  5a                     pop      edx
00447e0f  59                     pop      ecx
00447e10  5b                     pop      ebx
00447e11  c3                     ret      
