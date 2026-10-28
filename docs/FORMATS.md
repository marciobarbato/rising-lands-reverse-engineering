# File formats and localization

All multibyte integers below are little-endian. Offsets are file-relative unless marked as executable virtual addresses. Readers reject truncation and unsupported domains; observed corpus layouts do not prove every possible format variant.

## Original CD

The CUE describes a `MODE2/2352` data track followed by two audio tracks. Each physical sector is 2,352 bytes; ISO payloads used by the legacy extractor begin at byte 24 and contain 2,048 bytes. The ISO9660 primary descriptor is sector 16 with `01 CD001 01`. `../legacy-prototype/tools/cdrom.py` reads directory records without mounting or executing the Windows game.

The recorded full BIN has 705,418,896 bytes and SHA-1 `801e7a9bd00954c281f23767568222b23f3c4981`. Original media, extracted files, and existing vendor dependencies are local data, excluded from Git.

## CMP graphics

A CMP starts with u16 frame count. Each frame contains u16 width, u16 height, u32 compressed length, then exactly that many RLE bytes. The header contains no embedded palette.

| Command | Observed interpretation |
|---|---|
| `0x00` | Consume command without advancing pixels |
| `0x01..0x7F` | Skip that many transparent pixels |
| `0x81..0xFF` | Copy `256-command` literal palette indices |
| `0x80` | Absent from the eight-file corpus; reader rejects it |

Transparent skips preserve the draw destination. Literal zero remains opaque when composition needs a separate mask. The original `NEG BL`/`MOVSX` behavior does not justify treating `0x80` as a generic 128-byte run. The earlier audit examined 2,089,436 commands, including 1,062 zero commands and no `0x80`.

| Bank | Frames |
|---|---:|
| BLOCS | 1,345 |
| TROOPS | 2,848 |
| BUILDING | 611 |
| CREATURE | 1,920 |
| INVENTE | 72 |
| MENU | 40 |
| OTHERS | 4,517 |
| VEHICULE | 915 |

Terrain tiles are 32×32; confirmed terrain access is `frames[id-1]`. Six banks form the engine aggregate; menu/inventory are loaded separately. Read [graphics](GRAPHICS.md) before interpreting an ID or composing a sprite.

## PIE palette

`PLATGAME.PIE` starts with ASCII `Pie`, has a 256-color count at offset 7, and 768 RGB-component bytes at offset 9. Prototype-era expansion used the low six bits, yielding zero for zero and otherwise `4*v+3`, matching a loading-screen reference for indices 16–254. That historical partial comparison is not a complete reconstruction of runtime palette tables. Current graphics code and its x86/composition evidence govern rendering; preserve reserved indices, opacity, shadow, and palette-cycle distinctions.

## ETA V0.3

Cell index is always `y*256+x`, even when the playable dimensions are smaller.

| Offset | Size | Data |
|---|---:|---|
| `0x00000` | 4 | ASCII `V0.3` |
| `0x00004` | 65,536 | Attribute layer, u8[256×256] |
| `0x10004` | 131,072 | Terrain engine IDs, u16[256×256] |
| `0x30004` | 65,536 | Object codes, u8[256×256] |
| `0x40004` | 65,536 | Auxiliary/variant bytes |
| `0x50004` | 8 | Four players' internal resource 1 |
| `0x5000C` | 8 | Four players' internal resource 2 |
| `0x50014` | 8 | Four players' internal resource 0 |
| `0x5001C` | 2 | Playable width |
| `0x5001E` | 2 | Playable height |
| `0x50020` | 16 | Four u16 X/Y view origins |
| `0x50030` | variable | Indexed and simple blocks below |

The economy reconstruction confirms mutation resource IDs 1=food, 2=stone, 0=parts. Disk attributes are not a fully reconstructed runtime walkability/visibility grid. Mission 1 is 64×64 playable cells. Its legacy proof's `TEMP` substitution and simple attribute blocking are prototype choices, not complete original collision rules.

An indexed block has u16 N,S followed by N repetitions of u16 index plus S bytes. A simple block has N,S followed by N*S bytes.

| Block in read order | On-disk layout | Original routine |
|---|---|---|
| Structures | Indexed, S=204 in corpus | `0x46C517` |
| Units | Indexed, S=784 | `0x46ACBF` |
| Table 47534a | N then N*4 bytes | `0x47534A` |
| Table 47c24d | Simple, S=8 | `0x47C24D` |
| Table 47bcc7 | N then N pairs u16,u32 | `0x47BCC7` |
| Table 47c04a | Simple, S=10 | `0x47C04A` |
| Table 458b05 | Simple, S=10,N=10 | `0x458B05` |
| Discarded bytes | Four groups of four reads, 16 bytes | `0x47C30F` |
| Player lists | 4*100 records u16,u8, 1,200 bytes | `0x47C404` |
| Table 47ac30 | Simple, S=6,N=100 | `0x47AC30` |
| Unconsumed suffix | 917,504 bytes in corpus | Outside this load path |

Mission 1 has one initial structure record and 16 unit records. The final consumed block ends at `0x539C8`; file size is 1,259,976 bytes, leaving `0xE0000`. The older interpretation of its last terrain-sized region as a fallback layer does not prove complete suffix semantics.

Unit disk records copy 140 bytes, skip 512, then copy 132 into RAM at `+0x8C`. Runtime stride is 276; copied serialized length is 272. Reports distinguish disk owner/health from post-load effects. Original normalization replaces object `0x36`/54 with `0x42`/66 and auxiliary 1 across the entire grid; [graphics](GRAPHICS.md) documents the verified slice.

## PT-BR text and audio

Mission `WORLD/*.TXT`, `INSTALHD/TEXTES.TXT`, and unit names in `RISING.INI` contain Brazilian Portuguese. Decode Windows-1252 into UTF-8 without changing accents or wording. Remove DOS terminator `0x1A` only in presentation derivatives. The `[FRANCAIS]` header does not establish the actual language of this edition.

Audio originals remain under `INSTALHD/SOUND/` as HED/SND pairs. The legacy extraction/audio utilities and their verification artifacts stay with the legacy prototype; they are separate from completed gameplay audio integration. Original PT-BR voices and music are never translated as part of the English documentation policy.
