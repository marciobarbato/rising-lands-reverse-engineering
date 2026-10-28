; native_fill_leaf; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0048d890  09c9                     or ecx, ecx
0048d892  742c                     je 0x48d8c0
0048d894  3810                     cmp byte ptr [eax], dl
0048d896  a803                     test al, 3
0048d898  7409                     je 0x48d8a3
0048d89a  8810                     mov byte ptr [eax], dl
0048d89c  40                       inc eax
0048d89d  c1ca08                   ror edx, 8
0048d8a0  49                       dec ecx
0048d8a1  75f3                     jne 0x48d896
0048d8a3  51                       push ecx
0048d8a4  c1e902                   shr ecx, 2
0048d8a7  e81b000000               call 0x48d8c7
0048d8ac  59                       pop ecx
0048d8ad  83e103                   and ecx, 3
0048d8b0  740e                     je 0x48d8c0
0048d8b2  8810                     mov byte ptr [eax], dl
0048d8b4  49                       dec ecx
0048d8b5  7409                     je 0x48d8c0
0048d8b7  887001                   mov byte ptr [eax + 1], dh
0048d8ba  49                       dec ecx
0048d8bb  7403                     je 0x48d8c0
0048d8bd  885002                   mov byte ptr [eax + 2], dl
0048d8c0  c3                       ret
0048d8c1  90                       nop
0048d8c2  90                       nop
0048d8c3  90                       nop
0048d8c4  90                       nop
0048d8c5  90                       nop
0048d8c6  90                       nop
0048d8c7  09c9                     or ecx, ecx
0048d8c9  7467                     je 0x48d932
0048d8cb  a81f                     test al, 0x1f
0048d8cd  7408                     je 0x48d8d7
0048d8cf  8910                     mov dword ptr [eax], edx
0048d8d1  8d4004                   lea eax, [eax + 4]
0048d8d4  49                       dec ecx
0048d8d5  75f4                     jne 0x48d8cb
0048d8d7  51                       push ecx
0048d8d8  c1e902                   shr ecx, 2
0048d8db  743a                     je 0x48d917
0048d8dd  49                       dec ecx
0048d8de  7429                     je 0x48d909
0048d8e0  8910                     mov dword ptr [eax], edx
0048d8e2  895004                   mov dword ptr [eax + 4], edx
0048d8e5  49                       dec ecx
0048d8e6  895008                   mov dword ptr [eax + 8], edx
0048d8e9  89500c                   mov dword ptr [eax + 0xc], edx
0048d8ec  7418                     je 0x48d906
0048d8ee  385020                   cmp byte ptr [eax + 0x20], dl
0048d8f1  895010                   mov dword ptr [eax + 0x10], edx
0048d8f4  895014                   mov dword ptr [eax + 0x14], edx
0048d8f7  49                       dec ecx
0048d8f8  895018                   mov dword ptr [eax + 0x18], edx
0048d8fb  89501c                   mov dword ptr [eax + 0x1c], edx
0048d8fe  8d4020                   lea eax, [eax + 0x20]
0048d901  75dd                     jne 0x48d8e0
0048d903  8d40f0                   lea eax, [eax - 0x10]
0048d906  8d4010                   lea eax, [eax + 0x10]
0048d909  8910                     mov dword ptr [eax], edx
0048d90b  895004                   mov dword ptr [eax + 4], edx
0048d90e  895008                   mov dword ptr [eax + 8], edx
0048d911  89500c                   mov dword ptr [eax + 0xc], edx
0048d914  8d4010                   lea eax, [eax + 0x10]
0048d917  59                       pop ecx
0048d918  83e103                   and ecx, 3
0048d91b  7415                     je 0x48d932
0048d91d  8910                     mov dword ptr [eax], edx
0048d91f  8d4004                   lea eax, [eax + 4]
0048d922  49                       dec ecx
0048d923  740d                     je 0x48d932
0048d925  8910                     mov dword ptr [eax], edx
0048d927  8d4004                   lea eax, [eax + 4]
0048d92a  49                       dec ecx
0048d92b  7405                     je 0x48d932
0048d92d  8910                     mov dword ptr [eax], edx
0048d92f  8d4004                   lea eax, [eax + 4]
0048d932  c3                       ret
