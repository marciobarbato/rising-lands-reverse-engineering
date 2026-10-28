; iagVilleSetMode (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x004846a7..0x00484808 (end exclusive); labels are original SBL names
004846a7  53                       push ebx
004846a8  51                       push ecx
004846a9  89c1                     mov ecx, eax
004846ab  c1e005                   shl eax, 5
004846ae  0fbed2                   movsx edx, dl
004846b1  29c8                     sub eax, ecx
004846b3  8b1c95108c4900           mov ebx, dword ptr [edx*4 + 0x498c10]
004846ba  891c85a4b85100           mov dword ptr [eax*4 + 0x51b8a4], ebx
004846c1  891485b0b85100           mov dword ptr [eax*4 + 0x51b8b0], edx
004846c8  59                       pop ecx
004846c9  5b                       pop ebx
004846ca  c3                       ret
; 0x004846cb..0x00484808 not reached by any static path (padding or data):
004846cb  .byte 53515256575589e550bfc8a0490031f6
004846db  .byte eb0f4681c71401000081fee80300007d
004846eb  .byte b231c06689f0e83f60f9ff84c074e331
004846fb  .byte c08b55fc8a470439d075d731d0668b47
0048470b  .byte 0685c07ecd6a006a006a006a00bb0100
0048471b  .byte 0000ba020000006a008b45fc89f1e85d
0048472b  .byte 92ffff83f8ff75aa6a006a006a00ba02
0048473b  .byte 0000008b45fc6a0089f331c9e8d491ff
0048474b  .byte ffeb8f53515256575589e583ec045089
0048475b  .byte c2c1e00529d0ba4cb85100c1e00201c2
0048476b  .byte be010000008955fceb014683fe0a0f8f
0048477b  .byte 1fffffff8b5dfc8b5b6431c98b1c9d24
0048478b  .byte 8c4900eb0483c3024183f9167ddc31c0
0048479b  .byte 8a430139f07cee31d28a138b7dfc8d04
004847ab  .byte 1201f831ff668b782c668b0025ffff00
004847bb  .byte 0001f839f07dce31c08a45f8e8c742f9
004847cb  .byte ff25ff00000083f80175ba6a006a006a
004847db  .byte 008a1b6a0081e3ff00000089c231c98b
004847eb  .byte 45f8e82e91ffffe9a7feffff90794848
004847fb  .byte 00a548480094484800d6484800
