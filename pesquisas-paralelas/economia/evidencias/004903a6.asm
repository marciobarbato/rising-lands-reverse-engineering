; __init_80x87: limite por próximo símbolo SBL, fim exclusivo 0x004903cd.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004903a6  6650                     push     ax
004903a8  9b                       wait
004903a9  dbe3                     fninit
004903ab  d9e8                     fld1
004903ad  d9ee                     fldz
004903af  def9                     fdivp    st(1)
004903b1  d9c0                     fld      st(0)
004903b3  d9e0                     fchs
004903b5  ded9                     fcompp
004903b7  dfe0                     fnstsw   ax
004903b9  b002                     mov      al, 2
004903bb  9e                       sahf
004903bc  7402                     je       0x4903c0
004903be  b003                     mov      al, 3
004903c0  9b                       wait
004903c1  dbe3                     fninit
004903c3  d92c24                   fldcw    word ptr [esp]
004903c6  66870424                 xchg     word ptr [esp], ax
004903ca  6658                     pop      ax
004903cc  c3                       ret
