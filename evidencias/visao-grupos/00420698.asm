; CalculPosition; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00420698  53                       push ebx
00420699  51                       push ecx
0042069a  52                       push edx
0042069b  56                       push esi
0042069c  57                       push edi
0042069d  83ec08                   sub esp, 8
004206a0  25ffff0000               and eax, 0xffff
004206a5  89c2                     mov edx, eax
004206a7  c1e204                   shl edx, 4
004206aa  01c2                     add edx, eax
004206ac  c1e202                   shl edx, 2
004206af  01c2                     add edx, eax
004206b1  c1e202                   shl edx, 2
004206b4  81c2c8a04900             add edx, 0x49a0c8
004206ba  31db                     xor ebx, ebx
004206bc  8a4208                   mov al, byte ptr [edx + 8]
004206bf  88c3                     mov bl, al
004206c1  89d8                     mov eax, ebx
004206c3  c1e002                   shl eax, 2
004206c6  29d8                     sub eax, ebx
004206c8  c1e002                   shl eax, 2
004206cb  01c3                     add ebx, eax
004206cd  c1e302                   shl ebx, 2
004206d0  668b838c5d4900           mov ax, word ptr [ebx + 0x495d8c]
004206d7  890424                   mov dword ptr [esp], eax
004206da  668b838e5d4900           mov ax, word ptr [ebx + 0x495d8e]
004206e1  89442404                 mov dword ptr [esp + 4], eax
004206e5  8a4208                   mov al, byte ptr [edx + 8]
004206e8  3c15                     cmp al, 0x15
004206ea  0f87ae040000             ja 0x420b9e
004206f0  25ff000000               and eax, 0xff
004206f5  2eff248540064200         jmp dword ptr cs:[eax*4 + 0x420640]
004206fd  b801020000               mov eax, 0x201
00420702  eb62                     jmp 0x420766
00420704  b801010000               mov eax, 0x101
00420709  eb5b                     jmp 0x420766
0042070b  b802020000               mov eax, 0x202
00420710  eb54                     jmp 0x420766
00420712  b800030000               mov eax, 0x300
00420717  eb4d                     jmp 0x420766
00420719  b800010000               mov eax, 0x100
0042071e  eb46                     jmp 0x420766
00420720  b800020000               mov eax, 0x200
00420725  eb3f                     jmp 0x420766
00420727  b801000000               mov eax, 1
0042072c  eb38                     jmp 0x420766
0042072e  8b1c24                   mov ebx, dword ptr [esp]
00420731  8b4c2404                 mov ecx, dword ptr [esp + 4]
00420735  4b                       dec ebx
00420736  49                       dec ecx
00420737  891c24                   mov dword ptr [esp], ebx
0042073a  894c2404                 mov dword ptr [esp + 4], ecx
0042073e  8b3424                   mov esi, dword ptr [esp]
00420741  89cb                     mov ebx, ecx
00420743  668b7a02                 mov di, word ptr [edx + 2]
00420747  c1e308                   shl ebx, 8
0042074a  8a4208                   mov al, byte ptr [edx + 8]
0042074d  01f3                     add ebx, esi
0042074f  88c4                     mov ah, al
00420751  01fb                     add ebx, edi
00420753  3c15                     cmp al, 0x15
00420755  770d                     ja 0x420764
00420757  25ff000000               and eax, 0xff
0042075c  2eff2485d0024200         jmp dword ptr cs:[eax*4 + 0x4202d0]
00420764  31c0                     xor eax, eax
00420766  81e8ff000000             sub eax, 0xff
0042076c  e96e000000               jmp 0x4207df
00420771  b801020000               mov eax, 0x201
00420776  eb61                     jmp 0x4207d9
00420778  b801010000               mov eax, 0x101
0042077d  eb5a                     jmp 0x4207d9
0042077f  b802020000               mov eax, 0x202
00420784  eb53                     jmp 0x4207d9
00420786  b800030000               mov eax, 0x300
0042078b  eb4c                     jmp 0x4207d9
0042078d  b800010000               mov eax, 0x100
00420792  eb45                     jmp 0x4207d9
00420794  b800020000               mov eax, 0x200
00420799  eb3e                     jmp 0x4207d9
0042079b  b801000000               mov eax, 1
004207a0  eb37                     jmp 0x4207d9
004207a2  8b0c24                   mov ecx, dword ptr [esp]
004207a5  8b742404                 mov esi, dword ptr [esp + 4]
004207a9  83e904                   sub ecx, 4
004207ac  83ee02                   sub esi, 2
004207af  890c24                   mov dword ptr [esp], ecx
004207b2  89f3                     mov ebx, esi
004207b4  89742404                 mov dword ptr [esp + 4], esi
004207b8  c1e308                   shl ebx, 8
004207bb  668b4202                 mov ax, word ptr [edx + 2]
004207bf  01cb                     add ebx, ecx
004207c1  01c3                     add ebx, eax
004207c3  8a4208                   mov al, byte ptr [edx + 8]
004207c6  3c15                     cmp al, 0x15
004207c8  770d                     ja 0x4207d7
004207ca  25ff000000               and eax, 0xff
004207cf  2eff248528034200         jmp dword ptr cs:[eax*4 + 0x420328]
004207d7  31c0                     xor eax, eax
004207d9  81e802010000             sub eax, 0x102
004207df  29c3                     sub ebx, eax
004207e1  89d8                     mov eax, ebx
004207e3  e9fdd3ffff               jmp 0x41dbe5
004207e8  b801020000               mov eax, 0x201
004207ed  ebea                     jmp 0x4207d9
004207ef  b801010000               mov eax, 0x101
004207f4  ebe3                     jmp 0x4207d9
004207f6  b802020000               mov eax, 0x202
004207fb  ebdc                     jmp 0x4207d9
004207fd  b800030000               mov eax, 0x300
00420802  ebd5                     jmp 0x4207d9
00420804  b800010000               mov eax, 0x100
00420809  ebce                     jmp 0x4207d9
0042080b  b800020000               mov eax, 0x200
00420810  ebc7                     jmp 0x4207d9
00420812  b801000000               mov eax, 1
00420817  ebc0                     jmp 0x4207d9
00420819  8b0c24                   mov ecx, dword ptr [esp]
0042081c  8b442404                 mov eax, dword ptr [esp + 4]
00420820  49                       dec ecx
00420821  c1e008                   shl eax, 8
00420824  890c24                   mov dword ptr [esp], ecx
00420827  01c8                     add eax, ecx
00420829  668b5a02                 mov bx, word ptr [edx + 2]
0042082d  01c3                     add ebx, eax
0042082f  8a4208                   mov al, byte ptr [edx + 8]
00420832  88c4                     mov ah, al
00420834  3c15                     cmp al, 0x15
00420836  779f                     ja 0x4207d7
00420838  25ff000000               and eax, 0xff
0042083d  2eff248580034200         jmp dword ptr cs:[eax*4 + 0x420380]
00420845  b801020000               mov eax, 0x201
0042084a  eb8d                     jmp 0x4207d9
0042084c  b801010000               mov eax, 0x101
00420851  eb86                     jmp 0x4207d9
00420853  b802020000               mov eax, 0x202
00420858  e97cffffff               jmp 0x4207d9
0042085d  b800030000               mov eax, 0x300
00420862  e972ffffff               jmp 0x4207d9
00420867  b800010000               mov eax, 0x100
0042086c  e968ffffff               jmp 0x4207d9
00420871  b800020000               mov eax, 0x200
00420876  e95effffff               jmp 0x4207d9
0042087b  b801000000               mov eax, 1
00420880  e954ffffff               jmp 0x4207d9
00420885  8b0424                   mov eax, dword ptr [esp]
00420888  8b5c2404                 mov ebx, dword ptr [esp + 4]
0042088c  83e803                   sub eax, 3
0042088f  83eb02                   sub ebx, 2
00420892  890424                   mov dword ptr [esp], eax
00420895  895c2404                 mov dword ptr [esp + 4], ebx
00420899  c1e308                   shl ebx, 8
0042089c  668b7202                 mov si, word ptr [edx + 2]
004208a0  01c3                     add ebx, eax
004208a2  8a4208                   mov al, byte ptr [edx + 8]
004208a5  01f3                     add ebx, esi
004208a7  3c15                     cmp al, 0x15
004208a9  0f8728ffffff             ja 0x4207d7
004208af  25ff000000               and eax, 0xff
004208b4  2eff2485d8034200         jmp dword ptr cs:[eax*4 + 0x4203d8]
004208bc  b801020000               mov eax, 0x201
004208c1  e913ffffff               jmp 0x4207d9
004208c6  b801010000               mov eax, 0x101
004208cb  e909ffffff               jmp 0x4207d9
004208d0  b802020000               mov eax, 0x202
004208d5  e9fffeffff               jmp 0x4207d9
004208da  b800030000               mov eax, 0x300
004208df  e9f5feffff               jmp 0x4207d9
004208e4  b800010000               mov eax, 0x100
004208e9  e9ebfeffff               jmp 0x4207d9
004208ee  b800020000               mov eax, 0x200
004208f3  e9e1feffff               jmp 0x4207d9
004208f8  b801000000               mov eax, 1
004208fd  e9d7feffff               jmp 0x4207d9
00420902  8b0c24                   mov ecx, dword ptr [esp]
00420905  8b742404                 mov esi, dword ptr [esp + 4]
00420909  83e906                   sub ecx, 6
0042090c  83ee04                   sub esi, 4
0042090f  890c24                   mov dword ptr [esp], ecx
00420912  89f0                     mov eax, esi
00420914  89742404                 mov dword ptr [esp + 4], esi
00420918  c1e008                   shl eax, 8
0042091b  668b5a02                 mov bx, word ptr [edx + 2]
0042091f  01c8                     add eax, ecx
00420921  01c3                     add ebx, eax
00420923  8a4208                   mov al, byte ptr [edx + 8]
00420926  3c15                     cmp al, 0x15
00420928  0f87a9feffff             ja 0x4207d7
0042092e  25ff000000               and eax, 0xff
00420933  2eff248530044200         jmp dword ptr cs:[eax*4 + 0x420430]
0042093b  b801020000               mov eax, 0x201
00420940  e994feffff               jmp 0x4207d9
00420945  b801010000               mov eax, 0x101
0042094a  e98afeffff               jmp 0x4207d9
0042094f  b802020000               mov eax, 0x202
00420954  e980feffff               jmp 0x4207d9
00420959  b800030000               mov eax, 0x300
0042095e  e976feffff               jmp 0x4207d9
00420963  b800010000               mov eax, 0x100
00420968  e96cfeffff               jmp 0x4207d9
0042096d  b800020000               mov eax, 0x200
00420972  e962feffff               jmp 0x4207d9
00420977  b801000000               mov eax, 1
0042097c  e958feffff               jmp 0x4207d9
00420981  8b3c24                   mov edi, dword ptr [esp]
00420984  8b442404                 mov eax, dword ptr [esp + 4]
00420988  83ef04                   sub edi, 4
0042098b  83e802                   sub eax, 2
0042098e  893c24                   mov dword ptr [esp], edi
00420991  89442404                 mov dword ptr [esp + 4], eax
00420995  c1e008                   shl eax, 8
00420998  668b5a02                 mov bx, word ptr [edx + 2]
0042099c  01f8                     add eax, edi
0042099e  01c3                     add ebx, eax
004209a0  8a4208                   mov al, byte ptr [edx + 8]
004209a3  3c15                     cmp al, 0x15
004209a5  0f872cfeffff             ja 0x4207d7
004209ab  25ff000000               and eax, 0xff
004209b0  2eff248588044200         jmp dword ptr cs:[eax*4 + 0x420488]
004209b8  b801020000               mov eax, 0x201
004209bd  e917feffff               jmp 0x4207d9
004209c2  b801010000               mov eax, 0x101
004209c7  e90dfeffff               jmp 0x4207d9
004209cc  b802020000               mov eax, 0x202
004209d1  e903feffff               jmp 0x4207d9
004209d6  b800030000               mov eax, 0x300
004209db  e9f9fdffff               jmp 0x4207d9
004209e0  b800010000               mov eax, 0x100
004209e5  e9effdffff               jmp 0x4207d9
004209ea  b800020000               mov eax, 0x200
004209ef  e9e5fdffff               jmp 0x4207d9
004209f4  b801000000               mov eax, 1
004209f9  e9dbfdffff               jmp 0x4207d9
004209fe  8b3c24                   mov edi, dword ptr [esp]
00420a01  8b442404                 mov eax, dword ptr [esp + 4]
00420a05  83ef04                   sub edi, 4
00420a08  48                       dec eax
00420a09  893c24                   mov dword ptr [esp], edi
00420a0c  89442404                 mov dword ptr [esp + 4], eax
00420a10  c1e008                   shl eax, 8
00420a13  668b5a02                 mov bx, word ptr [edx + 2]
00420a17  01f8                     add eax, edi
00420a19  01c3                     add ebx, eax
00420a1b  8a4208                   mov al, byte ptr [edx + 8]
00420a1e  3c15                     cmp al, 0x15
00420a20  0f87b1fdffff             ja 0x4207d7
00420a26  25ff000000               and eax, 0xff
00420a2b  2eff2485e0044200         jmp dword ptr cs:[eax*4 + 0x4204e0]
00420a33  b801020000               mov eax, 0x201
00420a38  e99cfdffff               jmp 0x4207d9
00420a3d  b801010000               mov eax, 0x101
00420a42  e992fdffff               jmp 0x4207d9
00420a47  b802020000               mov eax, 0x202
00420a4c  e988fdffff               jmp 0x4207d9
00420a51  b800030000               mov eax, 0x300
00420a56  e97efdffff               jmp 0x4207d9
00420a5b  b800010000               mov eax, 0x100
00420a60  e974fdffff               jmp 0x4207d9
00420a65  b800020000               mov eax, 0x200
00420a6a  e96afdffff               jmp 0x4207d9
00420a6f  b801000000               mov eax, 1
00420a74  e960fdffff               jmp 0x4207d9
00420a79  8b0424                   mov eax, dword ptr [esp]
00420a7c  8b5c2404                 mov ebx, dword ptr [esp + 4]
00420a80  83e806                   sub eax, 6
00420a83  83eb04                   sub ebx, 4
00420a86  890424                   mov dword ptr [esp], eax
00420a89  895c2404                 mov dword ptr [esp + 4], ebx
00420a8d  89d8                     mov eax, ebx
00420a8f  8b0c24                   mov ecx, dword ptr [esp]
00420a92  c1e008                   shl eax, 8
00420a95  668b5a02                 mov bx, word ptr [edx + 2]
00420a99  01c8                     add eax, ecx
00420a9b  01c3                     add ebx, eax
00420a9d  8a4208                   mov al, byte ptr [edx + 8]
00420aa0  88c4                     mov ah, al
00420aa2  3c15                     cmp al, 0x15
00420aa4  0f872dfdffff             ja 0x4207d7
00420aaa  25ff000000               and eax, 0xff
00420aaf  2eff248538054200         jmp dword ptr cs:[eax*4 + 0x420538]
00420ab7  b801020000               mov eax, 0x201
00420abc  e918fdffff               jmp 0x4207d9
00420ac1  b801010000               mov eax, 0x101
00420ac6  e90efdffff               jmp 0x4207d9
00420acb  b802020000               mov eax, 0x202
00420ad0  e904fdffff               jmp 0x4207d9
00420ad5  b800030000               mov eax, 0x300
00420ada  e9fafcffff               jmp 0x4207d9
00420adf  b800010000               mov eax, 0x100
00420ae4  e9f0fcffff               jmp 0x4207d9
00420ae9  b800020000               mov eax, 0x200
00420aee  e9e6fcffff               jmp 0x4207d9
00420af3  b801000000               mov eax, 1
00420af8  e9dcfcffff               jmp 0x4207d9
00420afd  8b3424                   mov esi, dword ptr [esp]
00420b00  8b7c2404                 mov edi, dword ptr [esp + 4]
00420b04  83ee04                   sub esi, 4
00420b07  4f                       dec edi
00420b08  893424                   mov dword ptr [esp], esi
00420b0b  89f8                     mov eax, edi
00420b0d  897c2404                 mov dword ptr [esp + 4], edi
00420b11  c1e008                   shl eax, 8
00420b14  668b5a02                 mov bx, word ptr [edx + 2]
00420b18  01f0                     add eax, esi
00420b1a  01c3                     add ebx, eax
00420b1c  8a4208                   mov al, byte ptr [edx + 8]
00420b1f  3c15                     cmp al, 0x15
00420b21  0f87b0fcffff             ja 0x4207d7
00420b27  25ff000000               and eax, 0xff
00420b2c  2eff248590054200         jmp dword ptr cs:[eax*4 + 0x420590]
00420b34  b801020000               mov eax, 0x201
00420b39  eb5d                     jmp 0x420b98
00420b3b  b801010000               mov eax, 0x101
00420b40  eb56                     jmp 0x420b98
00420b42  b802020000               mov eax, 0x202
00420b47  eb4f                     jmp 0x420b98
00420b49  b800030000               mov eax, 0x300
00420b4e  eb48                     jmp 0x420b98
00420b50  b800010000               mov eax, 0x100
00420b55  eb41                     jmp 0x420b98
00420b57  b800020000               mov eax, 0x200
00420b5c  eb3a                     jmp 0x420b98
00420b5e  b801000000               mov eax, 1
00420b63  eb33                     jmp 0x420b98
00420b65  8b4c2404                 mov ecx, dword ptr [esp + 4]
00420b69  8b1c24                   mov ebx, dword ptr [esp]
00420b6c  49                       dec ecx
00420b6d  4b                       dec ebx
00420b6e  89c8                     mov eax, ecx
00420b70  891c24                   mov dword ptr [esp], ebx
00420b73  c1e008                   shl eax, 8
00420b76  894c2404                 mov dword ptr [esp + 4], ecx
00420b7a  01d8                     add eax, ebx
00420b7c  668b5a02                 mov bx, word ptr [edx + 2]
00420b80  01c3                     add ebx, eax
00420b82  8a4208                   mov al, byte ptr [edx + 8]
00420b85  3c15                     cmp al, 0x15
00420b87  770d                     ja 0x420b96
00420b89  25ff000000               and eax, 0xff
00420b8e  2eff2485e8054200         jmp dword ptr cs:[eax*4 + 0x4205e8]
00420b96  31c0                     xor eax, eax
00420b98  48                       dec eax
00420b99  e941fcffff               jmp 0x4207df
00420b9e  31c0                     xor eax, eax
00420ba0  e940d0ffff               jmp 0x41dbe5
