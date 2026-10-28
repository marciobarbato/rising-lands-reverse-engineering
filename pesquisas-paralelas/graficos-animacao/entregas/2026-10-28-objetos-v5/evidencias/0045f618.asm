; Cyclage [0x45f618, 0x45f6e1)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0045f618  53                     push     ebx
0045f619  51                     push     ecx
0045f61a  52                     push     edx
0045f61b  56                     push     esi
0045f61c  83ec04                 sub      esp, 4
0045f61f  31f6                   xor      esi, esi
0045f621  eb68                   jmp      0x45f68b ;
0045f623  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
0045f628  8a4c0203               mov      cl, byte ptr [edx + eax + 3]
0045f62c  880c02                 mov      byte ptr [edx + eax], cl
0045f62f  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
0045f634  8a4c0204               mov      cl, byte ptr [edx + eax + 4]
0045f638  884c0201               mov      byte ptr [edx + eax + 1], cl
0045f63c  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
0045f641  01d0                   add      eax, edx
0045f643  8a5005                 mov      dl, byte ptr [eax + 5]
0045f646  43                     inc      ebx
0045f647  885002                 mov      byte ptr [eax + 2], dl
0045f64a  0fbfc6                 movsx    eax, si
0045f64d  8d0440                 lea      eax, [eax + eax*2]
0045f650  31c9                   xor      ecx, ecx
0045f652  8a88e5244e00           mov      cl, byte ptr [eax + 0x4e24e5]
0045f658  31c0                   xor      eax, eax
0045f65a  6689d8                 mov      ax, bx
0045f65d  8d1440                 lea      edx, [eax + eax*2]
0045f660  39c8                   cmp      eax, ecx
0045f662  7cbf                   jl       0x45f623
0045f664  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
0045f669  8a1c24                 mov      bl, byte ptr [esp]
0045f66c  881c02                 mov      byte ptr [edx + eax], bl
0045f66f  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
0045f674  8a5c2401               mov      bl, byte ptr [esp + 1]
0045f678  885c0201               mov      byte ptr [edx + eax + 1], bl
0045f67c  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
0045f681  01c2                   add      edx, eax
0045f683  8a442402               mov      al, byte ptr [esp + 2]
0045f687  46                     inc      esi
0045f688  884202                 mov      byte ptr [edx + 2], al
0045f68b  31c0                   xor      eax, eax
0045f68d  0fbfd6                 movsx    edx, si
0045f690  a0e1244e00             mov      al, byte ptr [0x4e24e1]
0045f695  39c2                   cmp      edx, eax
0045f697  7d36                   jge      0x45f6cf
0045f699  8d1452                 lea      edx, [edx + edx*2]
0045f69c  31c0                   xor      eax, eax
0045f69e  8a82e4244e00           mov      al, byte ptr [edx + 0x4e24e4]
0045f6a4  8d0c40                 lea      ecx, [eax + eax*2]
0045f6a7  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
0045f6ac  8a1c01                 mov      bl, byte ptr [ecx + eax]
0045f6af  881c24                 mov      byte ptr [esp], bl
0045f6b2  8a5c0101               mov      bl, byte ptr [ecx + eax + 1]
0045f6b6  885c2401               mov      byte ptr [esp + 1], bl
0045f6ba  8a440102               mov      al, byte ptr [ecx + eax + 2]
0045f6be  30ff                   xor      bh, bh
0045f6c0  88442402               mov      byte ptr [esp + 2], al
0045f6c4  8a9ae4244e00           mov      bl, byte ptr [edx + 0x4e24e4]
0045f6ca  e97bffffff             jmp      0x45f64a ;
0045f6cf  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
0045f6d4  e858f7fdff             call     0x43ee31 ; DDSetPalette
0045f6d9  83c404                 add      esp, 4
0045f6dc  5e                     pop      esi
0045f6dd  5a                     pop      edx
0045f6de  59                     pop      ecx
0045f6df  5b                     pop      ebx
0045f6e0  c3                     ret
