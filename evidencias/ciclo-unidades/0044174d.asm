; unit_bag_headers; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044174d  66c740660000             mov word ptr [eax + 0x66], 0
00441753  66c740040000             mov word ptr [eax + 4], 0
00441759  31d2                     xor edx, edx
0044175b  66c740020000             mov word ptr [eax + 2], 0
00441761  89c1                     mov ecx, eax
00441763  66c7000000               mov word ptr [eax], 0
00441768  e974ffffff               jmp 0x4416e1
