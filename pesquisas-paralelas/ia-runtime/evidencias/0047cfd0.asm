; listInit (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047cfd0..0x0047d012 (end exclusive); labels are original SBL names
0047cfd0  56                       push esi
0047cfd1  57                       push edi
0047cfd2  89c6                     mov esi, eax
0047cfd4  89df                     mov edi, ebx
0047cfd6  895804                   mov dword ptr [eax + 4], ebx
0047cfd9  894808                   mov dword ptr [eax + 8], ecx
0047cfdc  8b5c240c                 mov ebx, dword ptr [esp + 0xc]
0047cfe0  89500c                   mov dword ptr [eax + 0xc], edx
0047cfe3  85db                     test ebx, ebx
0047cfe5  741e                     je 0x47d005
0047cfe7  4f                       dec edi
0047cfe8  c70000000000             mov dword ptr [eax], 0
0047cfee  31db                     xor ebx, ebx
0047cff0  eb07                     jmp 0x47cff9
0047cff2  89d0                     mov eax, edx
0047cff4  43                       inc ebx
0047cff5  01ca                     add edx, ecx
0047cff7  8918                     mov dword ptr [eax], ebx
0047cff9  39fb                     cmp ebx, edi
0047cffb  7cf5                     jl 0x47cff2
0047cffd  c702ffffffff             mov dword ptr [edx], 0xffffffff
0047d003  eb06                     jmp 0x47d00b
0047d005  c700ffffffff             mov dword ptr [eax], 0xffffffff
0047d00b  89f0                     mov eax, esi
0047d00d  5f                       pop edi
0047d00e  5e                       pop esi
0047d00f  c20400                   ret 4
