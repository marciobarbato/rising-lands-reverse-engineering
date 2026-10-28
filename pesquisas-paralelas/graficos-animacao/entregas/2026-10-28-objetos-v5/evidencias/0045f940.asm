; CalculOmbrage [0x45f940, 0x45fafc)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0045f940  53                     push     ebx
0045f941  51                     push     ecx
0045f942  56                     push     esi
0045f943  57                     push     edi
0045f944  55                     push     ebp
0045f945  81ec0c040000           sub      esp, 0x40c
0045f94b  89c5                   mov      ebp, eax
0045f94d  88942408040000         mov      byte ptr [esp + 0x408], dl
0045f954  31ff                   xor      edi, edi
0045f956  e9ec000000             jmp      0x45fa47 ;
0045f95b  8b15b4244e00           mov      edx, dword ptr [0x4e24b4]
0045f961  c60402df               mov      byte ptr [edx + eax], 0xdf
0045f965  e9dc000000             jmp      0x45fa46 ;
0045f96a  8b15b4244e00           mov      edx, dword ptr [0x4e24b4]
0045f970  c60402de               mov      byte ptr [edx + eax], 0xde
0045f974  e9cd000000             jmp      0x45fa46 ;
0045f979  8b15b4244e00           mov      edx, dword ptr [0x4e24b4]
0045f97f  c60402dd               mov      byte ptr [edx + eax], 0xdd
0045f983  e9be000000             jmp      0x45fa46 ;
0045f988  8b15b4244e00           mov      edx, dword ptr [0x4e24b4]
0045f98e  c60402a7               mov      byte ptr [edx + eax], 0xa7
0045f992  e9af000000             jmp      0x45fa46 ;
0045f997  8d0449                 lea      eax, [ecx + ecx*2]
0045f99a  89da                   mov      edx, ebx
0045f99c  01f0                   add      eax, esi
0045f99e  e80c9c0100             call     0x4795af ; Distance3d
0045f9a3  89048c                 mov      dword ptr [esp + ecx*4], eax
0045f9a6  89c8                   mov      eax, ecx
0045f9a8  40                     inc      eax
0045f9a9  6689842404040000       mov      word ptr [esp + 0x404], ax
0045f9b1  31c9                   xor      ecx, ecx
0045f9b3  668b8c2404040000       mov      cx, word ptr [esp + 0x404]
0045f9bb  81f900010000           cmp      ecx, 0x100
0045f9c1  7cd4                   jl       0x45f997
0045f9c3  b901000000             mov      ecx, 1
0045f9c8  30ff                   xor      bh, bh
0045f9ca  66898c2404040000       mov      word ptr [esp + 0x404], cx
0045f9d2  eb3e                   jmp      0x45fa12 ;
0045f9d4  42                     inc      edx
0045f9d5  31c9                   xor      ecx, ecx
0045f9d7  31c0                   xor      eax, eax
0045f9d9  8a0de1244e00           mov      cl, byte ptr [0x4e24e1]
0045f9df  6689d0                 mov      ax, dx
0045f9e2  39c8                   cmp      eax, ecx
0045f9e4  7d17                   jge      0x45f9fd
0045f9e6  8d0440                 lea      eax, [eax + eax*2]
0045f9e9  3a98e4244e00           cmp      bl, byte ptr [eax + 0x4e24e4]
0045f9ef  72e3                   jb       0x45f9d4
0045f9f1  3a98e5244e00           cmp      bl, byte ptr [eax + 0x4e24e5]
0045f9f7  77db                   ja       0x45f9d4
0045f9f9  b001                   mov      al, 1
0045f9fb  eb02                   jmp      0x45f9ff ;
0045f9fd  30d0                   xor      al, dl
0045f9ff  84c0                   test     al, al
0045fa01  7507                   jne      0x45fa0a
0045fa03  8abc2404040000         mov      bh, byte ptr [esp + 0x404]
0045fa0a  66ff842404040000       inc      word ptr [esp + 0x404]
0045fa12  31c0                   xor      eax, eax
0045fa14  668b842404040000       mov      ax, word ptr [esp + 0x404]
0045fa1c  3d00010000             cmp      eax, 0x100
0045fa21  7d17                   jge      0x45fa3a
0045fa23  31c9                   xor      ecx, ecx
0045fa25  88f9                   mov      cl, bh
0045fa27  8b0484                 mov      eax, dword ptr [esp + eax*4]
0045fa2a  3b048c                 cmp      eax, dword ptr [esp + ecx*4]
0045fa2d  73db                   jae      0x45fa0a
0045fa2f  8a9c2404040000         mov      bl, byte ptr [esp + 0x404]
0045fa36  31d2                   xor      edx, edx
0045fa38  eb9b                   jmp      0x45f9d5 ;
0045fa3a  8b15b4244e00           mov      edx, dword ptr [0x4e24b4]
0045fa40  0fbfc7                 movsx    eax, di
0045fa43  883c02                 mov      byte ptr [edx + eax], bh
0045fa46  47                     inc      edi
0045fa47  0fbfc7                 movsx    eax, di
0045fa4a  3d00010000             cmp      eax, 0x100
0045fa4f  0f8d9b000000           jge      0x45faf0
0045fa55  6683ff06               cmp      di, 6
0045fa59  721c                   jb       0x45fa77
0045fa5b  0f8609ffffff           jbe      0x45f96a
0045fa61  6683ff07               cmp      di, 7
0045fa65  0f860effffff           jbe      0x45f979
0045fa6b  6683ff0f               cmp      di, 0xf
0045fa6f  0f8613ffffff           jbe      0x45f988
0045fa75  eb0a                   jmp      0x45fa81 ;
0045fa77  6683ff05               cmp      di, 5
0045fa7b  0f84dafeffff           je       0x45f95b
0045fa81  0fbfcf                 movsx    ecx, di
0045fa84  31d2                   xor      edx, edx
0045fa86  8d0c49                 lea      ecx, [ecx + ecx*2]
0045fa89  0fb6b42408040000       movzx    esi, byte ptr [esp + 0x408]
0045fa91  8a1429                 mov      dl, byte ptr [ecx + ebp]
0045fa94  0fafd6                 imul     edx, esi
0045fa97  bb64000000             mov      ebx, 0x64
0045fa9c  89d0                   mov      eax, edx
0045fa9e  c1fa1f                 sar      edx, 0x1f
0045faa1  f7fb                   idiv     ebx
0045faa3  88842400040000         mov      byte ptr [esp + 0x400], al
0045faaa  31d2                   xor      edx, edx
0045faac  8a542901               mov      dl, byte ptr [ecx + ebp + 1]
0045fab0  0fafd6                 imul     edx, esi
0045fab3  89d0                   mov      eax, edx
0045fab5  c1fa1f                 sar      edx, 0x1f
0045fab8  f7fb                   idiv     ebx
0045faba  88842401040000         mov      byte ptr [esp + 0x401], al
0045fac1  31d2                   xor      edx, edx
0045fac3  8a542902               mov      dl, byte ptr [ecx + ebp + 2]
0045fac7  0fafd6                 imul     edx, esi
0045faca  89d0                   mov      eax, edx
0045facc  c1fa1f                 sar      edx, 0x1f
0045facf  f7fb                   idiv     ebx
0045fad1  89ee                   mov      esi, ebp
0045fad3  8d9c2400040000         lea      ebx, [esp + 0x400]
0045fada  31d2                   xor      edx, edx
0045fadc  88842402040000         mov      byte ptr [esp + 0x402], al
0045fae3  6689942404040000       mov      word ptr [esp + 0x404], dx
0045faeb  e9c1feffff             jmp      0x45f9b1 ;
0045faf0  81c40c040000           add      esp, 0x40c
0045faf6  5d                     pop      ebp
0045faf7  5f                     pop      edi
0045faf8  5e                     pop      esi
0045faf9  59                     pop      ecx
0045fafa  5b                     pop      ebx
0045fafb  c3                     ret
