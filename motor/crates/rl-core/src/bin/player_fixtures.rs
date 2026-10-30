//! Bounded offline adapter: original input bytes in, real Rust effects out.
use rl_core::{
    player::{fixture, DeclaredInput},
    MemoriaJogo,
};
use std::io::{self, Read, Write};
fn word(r: &mut impl Read) -> io::Result<u32> {
    let mut b = [0; 4];
    r.read_exact(&mut b)?;
    Ok(u32::from_le_bytes(b))
}
fn bytes(r: &mut impl Read) -> io::Result<Vec<u8>> {
    let n = word(r)?;
    if n > 64 * 1024 * 1024 {
        return Err(io::Error::other("fixture size limit"));
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
    let mut out = io::BufWriter::new(io::stdout().lock());
    let count = word(&mut input)?;
    if count > 10000 {
        return Err("fixture count limit".into());
    }
    for _ in 0..count {
        let name = String::from_utf8(bytes(&mut input)?)?;
        let mut args = [0; 6];
        for a in &mut args {
            *a = word(&mut input)?
        }
        let flags = word(&mut input)?;
        let mut answers = DeclaredInput {
            display_sound_boundary: true,
            display_text_boundary: flags & 2 != 0,
            cursor: Some((word(&mut input)? as i32, word(&mut input)? as i32)),
            ..Default::default()
        };
        let n = word(&mut input)?;
        if n > 256 {
            return Err("fixture key limit".into());
        }
        for _ in 0..n {
            let k = word(&mut input)?;
            let v = word(&mut input)?;
            answers.keys.insert(k, v);
        }
        let n = word(&mut input)?;
        if n > 65536 {
            return Err("fixture block limit".into());
        }
        let mut blocks = Vec::new();
        for _ in 0..n {
            let a = word(&mut input)?;
            blocks.push((a, bytes(&mut input)?));
        }
        let mut memory = MemoriaJogo::from_blocks(blocks)?;
        let result = fixture(&mut memory, &name, args, answers);
        match result {
            Ok(v) => {
                put(&mut out, 0)?;
                put(&mut out, u32::from(v.is_some()))?;
                put(&mut out, v.unwrap_or(0))?;
                blob(&mut out, b"")?
            }
            Err(e) => {
                put(&mut out, 1)?;
                put(&mut out, 0)?;
                put(&mut out, 0)?;
                blob(&mut out, e.to_string().as_bytes())?
            }
        }
        let blocks: Vec<_> = memory.blocks().collect();
        put(&mut out, blocks.len() as u32)?;
        for (a, b) in blocks {
            put(&mut out, a)?;
            blob(&mut out, b)?
        }
        let texts = rl_core::player::fixture_text_requests(&memory);
        put(&mut out, texts.len() as u32)?;
        for request in texts {
            for value in request {
                put(&mut out, value)?;
            }
        }
    }
    out.flush()?;
    Ok(())
}
