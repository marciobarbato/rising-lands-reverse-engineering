//! Original-capture register/state fixture transport; no callbacks or synthetic callees.
use rl_core::{chain_stage5, FrameRegisters, MemoriaJogo};
use std::io::{self, Read, Write};
fn word(r: &mut impl Read) -> io::Result<u32> {
    let mut b = [0; 4];
    r.read_exact(&mut b)?;
    Ok(u32::from_le_bytes(b))
}
fn bytes(r: &mut impl Read) -> io::Result<Vec<u8>> {
    let n = word(r)?;
    if n > 64 * 1024 * 1024 {
        return Err(io::Error::other("fixture span limit"));
    }
    let mut b = vec![0; n as usize];
    r.read_exact(&mut b)?;
    Ok(b)
}
fn put(w: &mut impl Write, n: u32) -> io::Result<()> {
    w.write_all(&n.to_le_bytes())
}
fn blob(w: &mut impl Write, b: &[u8]) -> io::Result<()> {
    put(w, b.len() as u32)?;
    w.write_all(b)
}
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut input = io::stdin().lock();
    let mut output = io::BufWriter::new(io::stdout().lock());
    let n = word(&mut input)?;
    if n > 10000 {
        return Err("fixture count limit".into());
    }
    for _ in 0..n {
        let name = String::from_utf8(bytes(&mut input)?)?;
        let r = FrameRegisters {
            eax: word(&mut input)?,
            ebx: word(&mut input)?,
            ecx: word(&mut input)?,
            edx: word(&mut input)?,
            esi: word(&mut input)?,
            edi: word(&mut input)?,
            ebp: word(&mut input)?,
            esp: word(&mut input)?,
        };
        let count = word(&mut input)?;
        if count > 65536 {
            return Err("fixture block limit".into());
        }
        let mut blocks = Vec::new();
        for _ in 0..count {
            blocks.push((word(&mut input)?, bytes(&mut input)?))
        }
        let mut m = MemoriaJogo::from_blocks(blocks)?;
        match chain_stage5::entry(&mut m, &name, r) {
            Ok(r) => {
                put(&mut output, 0)?;
                blob(&mut output, b"")?;
                for v in [r.eax, r.ebx, r.ecx, r.edx, r.esi, r.edi, r.ebp, r.esp] {
                    put(&mut output, v)?
                }
            }
            Err(e) => {
                put(&mut output, 1)?;
                blob(&mut output, e.to_string().as_bytes())?;
                for _ in 0..8 {
                    put(&mut output, 0)?
                }
            }
        }
        let blocks: Vec<_> = m.blocks().collect();
        put(&mut output, blocks.len() as u32)?;
        for (a, b) in blocks {
            put(&mut output, a)?;
            blob(&mut output, b)?
        }
    }
    output.flush()?;
    Ok(())
}
