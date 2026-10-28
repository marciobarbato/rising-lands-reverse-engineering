; SortilegeEstInvente: Type-6 branch; exclusive end 0x004749ad.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00474991  53                       push     ebx
00474992  89d3                     mov      ebx, edx
00474994  31d2                     xor      edx, edx
00474996  88c2                     mov      dl, al
00474998  89d0                     mov      eax, edx
0047499a  c1e002                   shl      eax, 2
0047499d  01c2                     add      edx, eax
0047499f  31c0                     xor      eax, eax
004749a1  6689d8                   mov      ax, bx
004749a4  8a8402448f5000           mov      al, byte ptr [edx + eax + 0x508f44]
004749ab  5b                       pop      ebx
004749ac  c3                       ret
