//! Original-capture register/state fixture transport; no callbacks or synthetic callees.
use rl_core::{chain_technology::Technology, FrameRegisters, MemoriaJogo};
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
        m.start_validation_trace();
        let mut technology = Technology::default();
        let mut fp = None;
        match technology.entry(&mut m, &name, r) {
            Ok(result) => {
                let r = result.registers;
                fp = result.x87_push;
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
        for v in fp.map_or([0; 4], |v| {
            [
                1,
                v.significand as u32,
                (v.significand >> 32) as u32,
                u32::from(v.sign_exponent),
            ]
        }) {
            put(&mut output, v)?;
        }
        let stores = m.take_validation_trace();
        put(&mut output, stores.len() as u32)?;
        for (a, b) in stores {
            put(&mut output, a)?;
            blob(&mut output, &b)?;
        }
        put(&mut output, technology.calls.len() as u32)?;
        for call in technology.calls {
            blob(&mut output, call.name.as_bytes())?;
            put(&mut output, call.site)?;
            for r in [call.input, call.output] {
                for v in [r.eax, r.ebx, r.ecx, r.edx, r.esi, r.edi, r.ebp, r.esp] {
                    put(&mut output, v)?;
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
