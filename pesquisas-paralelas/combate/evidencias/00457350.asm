; EnginSetTypeCaract; intervalo [0x00457350, 0x00457b87)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00457350  53                       push     ebx
00457351  51                       push     ecx
00457352  52                       push     edx
00457353  25ffff0000               and      eax, 0xffff
00457358  89c3                     mov      ebx, eax
0045735a  c1e304                   shl      ebx, 4
0045735d  01c3                     add      ebx, eax
0045735f  c1e302                   shl      ebx, 2
00457362  01c3                     add      ebx, eax
00457364  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
0045736a  c1e302                   shl      ebx, 2
0045736d  01d9                     add      ecx, ebx
0045736f  31d2                     xor      edx, edx
00457371  8a5101                   mov      dl, byte ptr [ecx + 1]
00457374  89d0                     mov      eax, edx
00457376  c1e002                   shl      eax, 2
00457379  c681bc000000ff           mov      byte ptr [ecx + 0xbc], 0xff
00457380  29d0                     sub      eax, edx
00457382  c681db00000008           mov      byte ptr [ecx + 0xdb], 8
00457389  c1e003                   shl      eax, 3
0045738c  c681da00000001           mov      byte ptr [ecx + 0xda], 1
00457393  01d0                     add      eax, edx
00457395  c681f900000000           mov      byte ptr [ecx + 0xf9], 0
0045739c  8a0445de654900           mov      al, byte ptr [eax*2 + 0x4965de]
004573a3  30e4                     xor      ah, ah
004573a5  66898102010000           mov      word ptr [ecx + 0x102], ax
004573ac  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
004573b1  8a440301                 mov      al, byte ptr [ebx + eax + 1]
004573b5  3c19                     cmp      al, 0x19
004573b7  0f8733fdffff             ja       0x4570f0
004573bd  25ff000000               and      eax, 0xff
004573c2  2eff2485e8724500         jmp      dword ptr cs:[eax*4 + 0x4572e8]
004573ca  c6819300000002           mov      byte ptr [ecx + 0x93], 2
004573d1  c6819800000003           mov      byte ptr [ecx + 0x98], 3
004573d8  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
004573df  c681a800000004           mov      byte ptr [ecx + 0xa8], 4
004573e6  c681a500000003           mov      byte ptr [ecx + 0xa5], 3
004573ed  c681a600000008           mov      byte ptr [ecx + 0xa6], 8
004573f4  c6819d00000064           mov      byte ptr [ecx + 0x9d], 0x64
004573fb  c681ac0000000f           mov      byte ptr [ecx + 0xac], 0xf
00457402  c681ad00000014           mov      byte ptr [ecx + 0xad], 0x14
00457409  c6819900000002           mov      byte ptr [ecx + 0x99], 2
00457410  c6417801                 mov      byte ptr [ecx + 0x78], 1
00457414  c6417916                 mov      byte ptr [ecx + 0x79], 0x16
00457418  c6417a00                 mov      byte ptr [ecx + 0x7a], 0
0045741c  5a                       pop      edx
0045741d  59                       pop      ecx
0045741e  5b                       pop      ebx
0045741f  c3                       ret
00457420  c6819300000001           mov      byte ptr [ecx + 0x93], 1
00457427  c6819800000008           mov      byte ptr [ecx + 0x98], 8
0045742e  c681a700000001           mov      byte ptr [ecx + 0xa7], 1
00457435  c681a800000001           mov      byte ptr [ecx + 0xa8], 1
0045743c  c681a500000003           mov      byte ptr [ecx + 0xa5], 3
00457443  c681a600000003           mov      byte ptr [ecx + 0xa6], 3
0045744a  c6819d00000064           mov      byte ptr [ecx + 0x9d], 0x64
00457451  c681ac00000002           mov      byte ptr [ecx + 0xac], 2
00457458  c681ad0000000a           mov      byte ptr [ecx + 0xad], 0xa
0045745f  c6819900000003           mov      byte ptr [ecx + 0x99], 3
00457466  c6417801                 mov      byte ptr [ecx + 0x78], 1
0045746a  c641791b                 mov      byte ptr [ecx + 0x79], 0x1b
0045746e  c6417a01                 mov      byte ptr [ecx + 0x7a], 1
00457472  5a                       pop      edx
00457473  59                       pop      ecx
00457474  5b                       pop      ebx
00457475  c3                       ret
00457476  c6819300000003           mov      byte ptr [ecx + 0x93], 3
0045747d  c6819800000003           mov      byte ptr [ecx + 0x98], 3
00457484  c681a700000003           mov      byte ptr [ecx + 0xa7], 3
0045748b  c681a800000000           mov      byte ptr [ecx + 0xa8], 0
00457492  c681a500000003           mov      byte ptr [ecx + 0xa5], 3
00457499  c681a600000008           mov      byte ptr [ecx + 0xa6], 8
004574a0  c6819d00000064           mov      byte ptr [ecx + 0x9d], 0x64
004574a7  c681ac00000006           mov      byte ptr [ecx + 0xac], 6
004574ae  c681ad0000000a           mov      byte ptr [ecx + 0xad], 0xa
004574b5  c6819900000003           mov      byte ptr [ecx + 0x99], 3
004574bc  5a                       pop      edx
004574bd  59                       pop      ecx
004574be  5b                       pop      ebx
004574bf  c3                       ret
004574c0  c6819300000002           mov      byte ptr [ecx + 0x93], 2
004574c7  c6819800000008           mov      byte ptr [ecx + 0x98], 8
004574ce  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
004574d5  c681a800000002           mov      byte ptr [ecx + 0xa8], 2
004574dc  c681a500000008           mov      byte ptr [ecx + 0xa5], 8
004574e3  c681a600000008           mov      byte ptr [ecx + 0xa6], 8
004574ea  c6819d00000030           mov      byte ptr [ecx + 0x9d], 0x30
004574f1  c681ac0000000a           mov      byte ptr [ecx + 0xac], 0xa
004574f8  c681ad00000008           mov      byte ptr [ecx + 0xad], 8
004574ff  c6819900000000           mov      byte ptr [ecx + 0x99], 0
00457506  c681ab00000032           mov      byte ptr [ecx + 0xab], 0x32
0045750d  5a                       pop      edx
0045750e  59                       pop      ecx
0045750f  5b                       pop      ebx
00457510  c3                       ret
00457511  c6819300000004           mov      byte ptr [ecx + 0x93], 4
00457518  c6819800000003           mov      byte ptr [ecx + 0x98], 3
0045751f  c681a700000003           mov      byte ptr [ecx + 0xa7], 3
00457526  c681a800000004           mov      byte ptr [ecx + 0xa8], 4
0045752d  c681a500000003           mov      byte ptr [ecx + 0xa5], 3
00457534  c681a600000002           mov      byte ptr [ecx + 0xa6], 2
0045753b  c6819d00000064           mov      byte ptr [ecx + 0x9d], 0x64
00457542  c681ac00000000           mov      byte ptr [ecx + 0xac], 0
00457549  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
00457550  c6819900000002           mov      byte ptr [ecx + 0x99], 2
00457557  5a                       pop      edx
00457558  59                       pop      ecx
00457559  5b                       pop      ebx
0045755a  c3                       ret
0045755b  c6819300000003           mov      byte ptr [ecx + 0x93], 3
00457562  c6819800000004           mov      byte ptr [ecx + 0x98], 4
00457569  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
00457570  c681a800000002           mov      byte ptr [ecx + 0xa8], 2
00457577  c681a500000003           mov      byte ptr [ecx + 0xa5], 3
0045757e  c681a600000001           mov      byte ptr [ecx + 0xa6], 1
00457585  c6819d00000064           mov      byte ptr [ecx + 0x9d], 0x64
0045758c  c681ac00000000           mov      byte ptr [ecx + 0xac], 0
00457593  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
0045759a  c6819900000002           mov      byte ptr [ecx + 0x99], 2
004575a1  c6417801                 mov      byte ptr [ecx + 0x78], 1
004575a5  c6417901                 mov      byte ptr [ecx + 0x79], 1
004575a9  e96afeffff               jmp      0x457418
004575ae  c6819300000002           mov      byte ptr [ecx + 0x93], 2
004575b5  c6819800000001           mov      byte ptr [ecx + 0x98], 1
004575bc  c681a700000004           mov      byte ptr [ecx + 0xa7], 4
004575c3  c681a800000004           mov      byte ptr [ecx + 0xa8], 4
004575ca  c681a500000003           mov      byte ptr [ecx + 0xa5], 3
004575d1  c681a600000004           mov      byte ptr [ecx + 0xa6], 4
004575d8  c6819d00000064           mov      byte ptr [ecx + 0x9d], 0x64
004575df  c681ac00000006           mov      byte ptr [ecx + 0xac], 6
004575e6  c681ad0000000a           mov      byte ptr [ecx + 0xad], 0xa
004575ed  c6819900000000           mov      byte ptr [ecx + 0x99], 0
004575f4  c681ab00000032           mov      byte ptr [ecx + 0xab], 0x32
004575fb  c6819400000000           mov      byte ptr [ecx + 0x94], 0
00457602  c6819500000001           mov      byte ptr [ecx + 0x95], 1
00457609  c6819600000000           mov      byte ptr [ecx + 0x96], 0
00457610  c681a400000000           mov      byte ptr [ecx + 0xa4], 0
00457617  5a                       pop      edx
00457618  59                       pop      ecx
00457619  5b                       pop      ebx
0045761a  c3                       ret
0045761b  c6819300000001           mov      byte ptr [ecx + 0x93], 1
00457622  c6819800000002           mov      byte ptr [ecx + 0x98], 2
00457629  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
00457630  c681a800000002           mov      byte ptr [ecx + 0xa8], 2
00457637  c681a500000008           mov      byte ptr [ecx + 0xa5], 8
0045763e  c681a60000000a           mov      byte ptr [ecx + 0xa6], 0xa
00457645  c681db00000008           mov      byte ptr [ecx + 0xdb], 8
0045764c  c6819d000000ff           mov      byte ptr [ecx + 0x9d], 0xff
00457653  c681ac00000003           mov      byte ptr [ecx + 0xac], 3
0045765a  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
00457661  c6819900000000           mov      byte ptr [ecx + 0x99], 0
00457668  c6417a06                 mov      byte ptr [ecx + 0x7a], 6
0045766c  5a                       pop      edx
0045766d  59                       pop      ecx
0045766e  5b                       pop      ebx
0045766f  c3                       ret
00457670  c6819300000001           mov      byte ptr [ecx + 0x93], 1
00457677  c6819800000002           mov      byte ptr [ecx + 0x98], 2
0045767e  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
00457685  c681a800000004           mov      byte ptr [ecx + 0xa8], 4
0045768c  c681a500000008           mov      byte ptr [ecx + 0xa5], 8
00457693  c681a600000004           mov      byte ptr [ecx + 0xa6], 4
0045769a  c681db00000008           mov      byte ptr [ecx + 0xdb], 8
004576a1  c6819d000000ff           mov      byte ptr [ecx + 0x9d], 0xff
004576a8  c681ac00000003           mov      byte ptr [ecx + 0xac], 3
004576af  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
004576b6  c6819900000000           mov      byte ptr [ecx + 0x99], 0
004576bd  c6417801                 mov      byte ptr [ecx + 0x78], 1
004576c1  c6417919                 mov      byte ptr [ecx + 0x79], 0x19
004576c5  e9a4fdffff               jmp      0x45746e
004576ca  c6819300000001           mov      byte ptr [ecx + 0x93], 1
004576d1  c6819800000003           mov      byte ptr [ecx + 0x98], 3
004576d8  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
004576df  c681a800000003           mov      byte ptr [ecx + 0xa8], 3
004576e6  c681a500000008           mov      byte ptr [ecx + 0xa5], 8
004576ed  c681a60000000a           mov      byte ptr [ecx + 0xa6], 0xa
004576f4  c681db0000000a           mov      byte ptr [ecx + 0xdb], 0xa
004576fb  c6819d000000ff           mov      byte ptr [ecx + 0x9d], 0xff
00457702  c681ac00000003           mov      byte ptr [ecx + 0xac], 3
00457709  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
00457710  c6819900000000           mov      byte ptr [ecx + 0x99], 0
00457717  c6417801                 mov      byte ptr [ecx + 0x78], 1
0045771b  c6417901                 mov      byte ptr [ecx + 0x79], 1
0045771f  c6417a07                 mov      byte ptr [ecx + 0x7a], 7
00457723  5a                       pop      edx
00457724  59                       pop      ecx
00457725  5b                       pop      ebx
00457726  c3                       ret
00457727  c6819300000001           mov      byte ptr [ecx + 0x93], 1
0045772e  c6819800000004           mov      byte ptr [ecx + 0x98], 4
00457735  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
0045773c  c681a800000004           mov      byte ptr [ecx + 0xa8], 4
00457743  c681a500000008           mov      byte ptr [ecx + 0xa5], 8
0045774a  c681a600000008           mov      byte ptr [ecx + 0xa6], 8
00457751  c681db00000008           mov      byte ptr [ecx + 0xdb], 8
00457758  c6819d000000ff           mov      byte ptr [ecx + 0x9d], 0xff
0045775f  c681ac00000003           mov      byte ptr [ecx + 0xac], 3
00457766  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
0045776d  c6819900000000           mov      byte ptr [ecx + 0x99], 0
00457774  c6417801                 mov      byte ptr [ecx + 0x78], 1
00457778  c641791a                 mov      byte ptr [ecx + 0x79], 0x1a
0045777c  e9edfcffff               jmp      0x45746e
00457781  c6819300000001           mov      byte ptr [ecx + 0x93], 1
00457788  c6819800000004           mov      byte ptr [ecx + 0x98], 4
0045778f  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
00457796  c681a800000004           mov      byte ptr [ecx + 0xa8], 4
0045779d  c681a500000008           mov      byte ptr [ecx + 0xa5], 8
004577a4  c681a600000008           mov      byte ptr [ecx + 0xa6], 8
004577ab  c681db00000008           mov      byte ptr [ecx + 0xdb], 8
004577b2  c6819d000000ff           mov      byte ptr [ecx + 0x9d], 0xff
004577b9  c681ac00000003           mov      byte ptr [ecx + 0xac], 3
004577c0  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
004577c7  c6819900000000           mov      byte ptr [ecx + 0x99], 0
004577ce  c6417801                 mov      byte ptr [ecx + 0x78], 1
004577d2  c641791a                 mov      byte ptr [ecx + 0x79], 0x1a
004577d6  c6417a04                 mov      byte ptr [ecx + 0x7a], 4
004577da  5a                       pop      edx
004577db  59                       pop      ecx
004577dc  5b                       pop      ebx
004577dd  c3                       ret
004577de  c6819300000001           mov      byte ptr [ecx + 0x93], 1
004577e5  c6819800000001           mov      byte ptr [ecx + 0x98], 1
004577ec  c681a700000003           mov      byte ptr [ecx + 0xa7], 3
004577f3  c681a800000002           mov      byte ptr [ecx + 0xa8], 2
004577fa  c681a500000008           mov      byte ptr [ecx + 0xa5], 8
00457801  c681a60000000a           mov      byte ptr [ecx + 0xa6], 0xa
00457808  c681db0000000a           mov      byte ptr [ecx + 0xdb], 0xa
0045780f  c6819d000000ff           mov      byte ptr [ecx + 0x9d], 0xff
00457816  c681ac00000003           mov      byte ptr [ecx + 0xac], 3
0045781d  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
00457824  c6819900000000           mov      byte ptr [ecx + 0x99], 0
0045782b  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00457830  01d8                     add      eax, ebx
00457832  8a5001                   mov      dl, byte ptr [eax + 1]
00457835  31db                     xor      ebx, ebx
00457837  88d3                     mov      bl, dl
00457839  8a00                     mov      al, byte ptr [eax]
0045783b  ba0c000000               mov      edx, 0xc
00457840  25ff000000               and      eax, 0xff
00457845  e87614fdff               call     0x428cc0
0045784a  040a                     add      al, 0xa
0045784c  c6417a05                 mov      byte ptr [ecx + 0x7a], 5
00457850  8881da000000             mov      byte ptr [ecx + 0xda], al
00457856  5a                       pop      edx
00457857  59                       pop      ecx
00457858  5b                       pop      ebx
00457859  c3                       ret
0045785a  c6819300000001           mov      byte ptr [ecx + 0x93], 1
00457861  c6819800000002           mov      byte ptr [ecx + 0x98], 2
00457868  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
0045786f  c681a800000004           mov      byte ptr [ecx + 0xa8], 4
00457876  c681a500000008           mov      byte ptr [ecx + 0xa5], 8
0045787d  c681a600000008           mov      byte ptr [ecx + 0xa6], 8
00457884  c681db00000008           mov      byte ptr [ecx + 0xdb], 8
0045788b  c6819d000000ff           mov      byte ptr [ecx + 0x9d], 0xff
00457892  c681ac00000003           mov      byte ptr [ecx + 0xac], 3
00457899  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
004578a0  c6819900000000           mov      byte ptr [ecx + 0x99], 0
004578a7  5a                       pop      edx
004578a8  59                       pop      ecx
004578a9  5b                       pop      ebx
004578aa  c3                       ret
004578ab  c6819300000001           mov      byte ptr [ecx + 0x93], 1
004578b2  c6819800000003           mov      byte ptr [ecx + 0x98], 3
004578b9  ebad                     jmp      0x457868
004578bb  c6819300000001           mov      byte ptr [ecx + 0x93], 1
004578c2  c6819800000003           mov      byte ptr [ecx + 0x98], 3
004578c9  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
004578d0  c681a800000004           mov      byte ptr [ecx + 0xa8], 4
004578d7  c681a500000008           mov      byte ptr [ecx + 0xa5], 8
004578de  c681a600000008           mov      byte ptr [ecx + 0xa6], 8
004578e5  c681db00000008           mov      byte ptr [ecx + 0xdb], 8
004578ec  c6819d000000ff           mov      byte ptr [ecx + 0x9d], 0xff
004578f3  c681ac00000003           mov      byte ptr [ecx + 0xac], 3
004578fa  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
00457901  c6819900000000           mov      byte ptr [ecx + 0x99], 0
00457908  c681bb00000005           mov      byte ptr [ecx + 0xbb], 5
0045790f  5a                       pop      edx
00457910  59                       pop      ecx
00457911  5b                       pop      ebx
00457912  c3                       ret
00457913  c6819300000001           mov      byte ptr [ecx + 0x93], 1
0045791a  c6819800000002           mov      byte ptr [ecx + 0x98], 2
00457921  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
00457928  c681a800000002           mov      byte ptr [ecx + 0xa8], 2
0045792f  c681a50000000a           mov      byte ptr [ecx + 0xa5], 0xa
00457936  c681a60000000a           mov      byte ptr [ecx + 0xa6], 0xa
0045793d  c681db00000008           mov      byte ptr [ecx + 0xdb], 8
00457944  c6819d000000ff           mov      byte ptr [ecx + 0x9d], 0xff
0045794b  c681ac00000003           mov      byte ptr [ecx + 0xac], 3
00457952  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
00457959  c6819900000000           mov      byte ptr [ecx + 0x99], 0
00457960  c6417801                 mov      byte ptr [ecx + 0x78], 1
00457964  c6417909                 mov      byte ptr [ecx + 0x79], 9
00457968  e9fbfcffff               jmp      0x457668
0045796d  c6819300000001           mov      byte ptr [ecx + 0x93], 1
00457974  c6819800000002           mov      byte ptr [ecx + 0x98], 2
0045797b  c681a700000001           mov      byte ptr [ecx + 0xa7], 1
00457982  c681a800000002           mov      byte ptr [ecx + 0xa8], 2
00457989  c681a50000000a           mov      byte ptr [ecx + 0xa5], 0xa
00457990  c681a600000004           mov      byte ptr [ecx + 0xa6], 4
00457997  c681db00000008           mov      byte ptr [ecx + 0xdb], 8
0045799e  c6819d000000ff           mov      byte ptr [ecx + 0x9d], 0xff
004579a5  c681ac00000003           mov      byte ptr [ecx + 0xac], 3
004579ac  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
004579b3  c6819900000000           mov      byte ptr [ecx + 0x99], 0
004579ba  c6417801                 mov      byte ptr [ecx + 0x78], 1
004579be  c6417911                 mov      byte ptr [ecx + 0x79], 0x11
004579c2  c6417a02                 mov      byte ptr [ecx + 0x7a], 2
004579c6  5a                       pop      edx
004579c7  59                       pop      ecx
004579c8  5b                       pop      ebx
004579c9  c3                       ret
004579ca  c6819300000001           mov      byte ptr [ecx + 0x93], 1
004579d1  c6819800000002           mov      byte ptr [ecx + 0x98], 2
004579d8  c681a700000001           mov      byte ptr [ecx + 0xa7], 1
004579df  c681a800000002           mov      byte ptr [ecx + 0xa8], 2
004579e6  c681a50000000f           mov      byte ptr [ecx + 0xa5], 0xf
004579ed  c681a60000000f           mov      byte ptr [ecx + 0xa6], 0xf
004579f4  c681db0000000f           mov      byte ptr [ecx + 0xdb], 0xf
004579fb  e98b000000               jmp      0x457a8b
00457a00  c6819300000001           mov      byte ptr [ecx + 0x93], 1
00457a07  c6819800000008           mov      byte ptr [ecx + 0x98], 8
00457a0e  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
00457a15  c681a800000002           mov      byte ptr [ecx + 0xa8], 2
00457a1c  c681a500000008           mov      byte ptr [ecx + 0xa5], 8
00457a23  c681a600000008           mov      byte ptr [ecx + 0xa6], 8
00457a2a  c681db00000008           mov      byte ptr [ecx + 0xdb], 8
00457a31  c6819d000000ff           mov      byte ptr [ecx + 0x9d], 0xff
00457a38  c681ac00000003           mov      byte ptr [ecx + 0xac], 3
00457a3f  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
00457a46  c6819900000000           mov      byte ptr [ecx + 0x99], 0
00457a4d  c6417801                 mov      byte ptr [ecx + 0x78], 1
00457a51  c6417918                 mov      byte ptr [ecx + 0x79], 0x18
00457a55  e90efcffff               jmp      0x457668
00457a5a  c6819300000001           mov      byte ptr [ecx + 0x93], 1
00457a61  c6819800000004           mov      byte ptr [ecx + 0x98], 4
00457a68  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
00457a6f  c681a800000002           mov      byte ptr [ecx + 0xa8], 2
00457a76  c681a500000008           mov      byte ptr [ecx + 0xa5], 8
00457a7d  c681a600000008           mov      byte ptr [ecx + 0xa6], 8
00457a84  c681db00000008           mov      byte ptr [ecx + 0xdb], 8
00457a8b  c6819d000000ff           mov      byte ptr [ecx + 0x9d], 0xff
00457a92  c681ac00000003           mov      byte ptr [ecx + 0xac], 3
00457a99  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
00457aa0  c6819900000000           mov      byte ptr [ecx + 0x99], 0
00457aa7  c6417800                 mov      byte ptr [ecx + 0x78], 0
00457aab  5a                       pop      edx
00457aac  59                       pop      ecx
00457aad  5b                       pop      ebx
00457aae  c3                       ret
00457aaf  c6819300000001           mov      byte ptr [ecx + 0x93], 1
00457ab6  c6819800000004           mov      byte ptr [ecx + 0x98], 4
00457abd  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
00457ac4  c681a800000002           mov      byte ptr [ecx + 0xa8], 2
00457acb  c681a500000008           mov      byte ptr [ecx + 0xa5], 8
00457ad2  c681a600000008           mov      byte ptr [ecx + 0xa6], 8
00457ad9  c681db00000008           mov      byte ptr [ecx + 0xdb], 8
00457ae0  c6819d000000ff           mov      byte ptr [ecx + 0x9d], 0xff
00457ae7  c681ac00000003           mov      byte ptr [ecx + 0xac], 3
00457aee  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
00457af5  c6819900000000           mov      byte ptr [ecx + 0x99], 0
00457afc  c6417801                 mov      byte ptr [ecx + 0x78], 1
00457b00  c6417917                 mov      byte ptr [ecx + 0x79], 0x17
00457b04  e95ffbffff               jmp      0x457668
00457b09  c6819300000001           mov      byte ptr [ecx + 0x93], 1
00457b10  c6819800000002           mov      byte ptr [ecx + 0x98], 2
00457b17  c681a700000002           mov      byte ptr [ecx + 0xa7], 2
00457b1e  c681a800000002           mov      byte ptr [ecx + 0xa8], 2
00457b25  c681a500000008           mov      byte ptr [ecx + 0xa5], 8
00457b2c  c681a600000008           mov      byte ptr [ecx + 0xa6], 8
00457b33  c681db00000008           mov      byte ptr [ecx + 0xdb], 8
00457b3a  c6819d000000ff           mov      byte ptr [ecx + 0x9d], 0xff
00457b41  c681ac00000003           mov      byte ptr [ecx + 0xac], 3
00457b48  c681ad00000003           mov      byte ptr [ecx + 0xad], 3
00457b4f  c6819900000000           mov      byte ptr [ecx + 0x99], 0
00457b56  c6417801                 mov      byte ptr [ecx + 0x78], 1
00457b5a  c6417917                 mov      byte ptr [ecx + 0x79], 0x17
00457b5e  c6417a05                 mov      byte ptr [ecx + 0x7a], 5
00457b62  5a                       pop      edx
00457b63  59                       pop      ecx
00457b64  5b                       pop      ebx
00457b65  c3                       ret
00457b66  c6819300000003           mov      byte ptr [ecx + 0x93], 3
00457b6d  c6819800000001           mov      byte ptr [ecx + 0x98], 1
00457b74  c681a700000003           mov      byte ptr [ecx + 0xa7], 3
00457b7b  c681a800000003           mov      byte ptr [ecx + 0xa8], 3
00457b82  e9effeffff               jmp      0x457a76
