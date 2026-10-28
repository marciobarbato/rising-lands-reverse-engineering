; iagWarInit (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0048614c..0x004862f5 (end exclusive); labels are original SBL names
0048614c  53                       push ebx
0048614d  51                       push ecx
0048614e  52                       push edx
0048614f  56                       push esi
00486150  83ec20                   sub esp, 0x20
00486153  bb04290000               mov ebx, 0x2904
00486158  baf8514900               mov edx, 0x4951f8
0048615d  b803524900               mov eax, 0x495203
00486162  e8ed9affff               call 0x47fc54 ; -> iaConfigGetValue
00486167  bbac0d0000               mov ebx, 0xdac
0048616c  ba07524900               mov edx, 0x495207
00486171  a3b08c4900               mov dword ptr [0x498cb0], eax
00486176  b814524900               mov eax, 0x495214
0048617b  e8d49affff               call 0x47fc54 ; -> iaConfigGetValue
00486180  bbdc050000               mov ebx, 0x5dc
00486185  ba18524900               mov edx, 0x495218
0048618a  a3b48c4900               mov dword ptr [0x498cb4], eax
0048618f  b824524900               mov eax, 0x495224
00486194  e8bb9affff               call 0x47fc54 ; -> iaConfigGetValue
00486199  bbe8030000               mov ebx, 0x3e8
0048619e  ba28524900               mov edx, 0x495228
004861a3  a3b88c4900               mov dword ptr [0x498cb8], eax
004861a8  b834524900               mov eax, 0x495234
004861ad  e8a29affff               call 0x47fc54 ; -> iaConfigGetValue
004861b2  bb05000000               mov ebx, 5
004861b7  ba38524900               mov edx, 0x495238
004861bc  a3bc8c4900               mov dword ptr [0x498cbc], eax
004861c1  b84a524900               mov eax, 0x49524a
004861c6  e8899affff               call 0x47fc54 ; -> iaConfigGetValue
004861cb  bb03000000               mov ebx, 3
004861d0  ba4e524900               mov edx, 0x49524e
004861d5  a3c48c4900               mov dword ptr [0x498cc4], eax
004861da  b862524900               mov eax, 0x495262
004861df  e8709affff               call 0x47fc54 ; -> iaConfigGetValue
004861e4  bb0f000000               mov ebx, 0xf
004861e9  ba66524900               mov edx, 0x495266
004861ee  a3c88c4900               mov dword ptr [0x498cc8], eax
004861f3  b879524900               mov eax, 0x495279
004861f8  31f6                     xor esi, esi
004861fa  e8559affff               call 0x47fc54 ; -> iaConfigGetValue
004861ff  bb0a000000               mov ebx, 0xa
00486204  ba7d524900               mov edx, 0x49527d
00486209  a3cc8c4900               mov dword ptr [0x498ccc], eax
0048620e  b890524900               mov eax, 0x495290
00486213  31c9                     xor ecx, ecx
00486215  e83a9affff               call 0x47fc54 ; -> iaConfigGetValue
0048621a  a3d08c4900               mov dword ptr [0x498cd0], eax
0048621f  56                       push esi
00486220  6894524900               push 0x495294
00486225  8d442408                 lea eax, [esp + 8]
00486229  50                       push eax
0048622a  8d54240c                 lea edx, [esp + 0xc]
0048622e  83c104                   add ecx, 4
00486231  e8856d0000               call 0x48cfbb ; -> sprintf
00486236  b8a8524900               mov eax, 0x4952a8
0048623b  83c40c                   add esp, 0xc
0048623e  8b99f08c4900             mov ebx, dword ptr [ecx + 0x498cf0]
00486244  46                       inc esi
00486245  e80a9affff               call 0x47fc54 ; -> iaConfigGetValue
0048624a  8981f08c4900             mov dword ptr [ecx + 0x498cf0], eax
00486250  83fe1a                   cmp esi, 0x1a
00486253  7cca                     jl 0x48621f
00486255  bb0a000000               mov ebx, 0xa
0048625a  baac524900               mov edx, 0x4952ac
0048625f  b8ba524900               mov eax, 0x4952ba
00486264  e8eb99ffff               call 0x47fc54 ; -> iaConfigGetValue
00486269  bb0a000000               mov ebx, 0xa
0048626e  babe524900               mov edx, 0x4952be
00486273  a350135200               mov dword ptr [0x521350], eax
00486278  b8cf524900               mov eax, 0x4952cf
0048627d  e8d299ffff               call 0x47fc54 ; -> iaConfigGetValue
00486282  bb28000000               mov ebx, 0x28
00486287  bad3524900               mov edx, 0x4952d3
0048628c  a354135200               mov dword ptr [0x521354], eax
00486291  b8ee524900               mov eax, 0x4952ee
00486296  e8b999ffff               call 0x47fc54 ; -> iaConfigGetValue
0048629b  bb0a000000               mov ebx, 0xa
004862a0  baf2524900               mov edx, 0x4952f2
004862a5  a358135200               mov dword ptr [0x521358], eax
004862aa  b80c534900               mov eax, 0x49530c
004862af  e8a099ffff               call 0x47fc54 ; -> iaConfigGetValue
004862b4  bb0a000000               mov ebx, 0xa
004862b9  ba10534900               mov edx, 0x495310
004862be  a35c135200               mov dword ptr [0x52135c], eax
004862c3  b826534900               mov eax, 0x495326
004862c8  e88799ffff               call 0x47fc54 ; -> iaConfigGetValue
004862cd  bb70170000               mov ebx, 0x1770
004862d2  ba2a534900               mov edx, 0x49532a
004862d7  a360135200               mov dword ptr [0x521360], eax
004862dc  b837534900               mov eax, 0x495337
004862e1  e86e99ffff               call 0x47fc54 ; -> iaConfigGetValue
004862e6  a364135200               mov dword ptr [0x521364], eax
004862eb  31c0                     xor eax, eax
004862ed  83c420                   add esp, 0x20
004862f0  5e                       pop esi
004862f1  5a                       pop edx
004862f2  59                       pop ecx
004862f3  5b                       pop ebx
004862f4  c3                       ret
