//! Offline original-input fixture runner. The production C ABI never installs
//! recorded text boundaries. Bounded streaming avoids duplicating whole probes.
use rl_core::{
    render::{Cache, RecordedTextBoundary, Renderer},
    render_assets::Assets,
    MemoriaJogo,
};
use std::{
    collections::VecDeque,
    io::{self, BufReader, BufWriter, Read, Write},
    sync::Arc,
};
fn read_u32(r: &mut impl Read) -> u32 {
    let mut v = [0; 4];
    r.read_exact(&mut v).unwrap();
    u32::from_le_bytes(v)
}
fn blob(r: &mut impl Read) -> Vec<u8> {
    let n = read_u32(r) as usize;
    assert!(n <= 64 * 1024 * 1024);
    let mut b = vec![0; n];
    r.read_exact(&mut b).unwrap();
    b
}
fn u32_out(w: &mut impl Write, v: u32) {
    w.write_all(&v.to_le_bytes()).unwrap();
}
fn blob_out(w: &mut impl Write, b: &[u8]) {
    u32_out(w, b.len() as u32);
    w.write_all(b).unwrap();
}
fn main() {
    let mut input = BufReader::new(io::stdin().lock());
    let mut output = BufWriter::new(io::stdout().lock());
    let mut magic = [0; 8];
    input.read_exact(&mut magic).unwrap();
    assert_eq!(&magic, b"RLRP1700");
    let blobs: Vec<_> = (0..9).map(|_| blob(&mut input)).collect();
    let refs: Vec<_> = blobs.iter().map(|b| b.as_slice()).collect();
    let assets = Arc::new(Assets::load(&refs).unwrap());
    let mut renderer: Option<Renderer> = None;
    loop {
        let mut flag = [0; 4];
        match input.read_exact(&mut flag) {
            Ok(()) => {}
            Err(e) if e.kind() == io::ErrorKind::UnexpectedEof => break,
            Err(e) => panic!("{e}"),
        };
        let flags = u32::from_le_bytes(flag);
        assert!(flags <= 7);
        let tick = read_u32(&mut input);
        let mut memory = MemoriaJogo::default();
        for _ in 0..read_u32(&mut input) {
            let base = read_u32(&mut input);
            let data = blob(&mut input);
            memory.declare(base, data).unwrap();
        }
        if flags & 1 != 0 {
            let surface = blob(&mut input);
            let keys = blob(&mut input);
            let raw = blob(&mut input);
            let cursor = read_u32(&mut input) as u16;
            renderer = Some(
                Renderer::new(Arc::clone(&assets), &surface, Cache { keys, raw, cursor }).unwrap(),
            );
        }
        let renderer = renderer.as_mut().unwrap();
        renderer.tick = if tick == u32::MAX { None } else { Some(tick) };
        if flags & 2 != 0 {
            let mut boundaries = VecDeque::new();
            for _ in 0..read_u32(&mut input) {
                let text = blob(&mut input);
                let mut rectangle = [0; 4];
                for v in &mut rectangle {
                    *v = read_u32(&mut input) as i32;
                }
                let font = read_u32(&mut input);
                let flags = [read_u32(&mut input), read_u32(&mut input)];
                let mut surface_sha256 = [0; 32];
                input.read_exact(&mut surface_sha256).unwrap();
                boundaries.push_back(RecordedTextBoundary {
                    text,
                    rectangle,
                    font,
                    flags,
                    surface_sha256,
                });
            }
            renderer.recorded_text_boundaries = Some(boundaries);
        } else {
            renderer.recorded_text_boundaries = None;
        }
        let result = if flags & 4 != 0 {
            let x = read_u32(&mut input) as i32;
            let y = read_u32(&mut input) as i32;
            let cell = read_u32(&mut input);
            renderer.render_building_fixture(&memory, x, y, cell)
        } else {
            renderer.render(&memory, true)
        };
        let result = match result {
            Ok(r) => r,
            Err(e) => {
                eprintln!("Fixture render error: {e:?}");
                std::process::exit(2)
            }
        };
        u32_out(&mut output, result.disposition);
        u32_out(&mut output, result.stop.as_ref().map_or(0, |v| v.0));
        blob_out(
            &mut output,
            result.stop.as_ref().map_or("", |v| v.1.as_str()).as_bytes(),
        );
        u32_out(&mut output, result.text_boundaries_checked);
        blob_out(&mut output, &renderer.surface);
        blob_out(&mut output, &renderer.cache.keys);
        blob_out(&mut output, &renderer.cache.raw);
        u32_out(&mut output, renderer.cache.cursor as u32);
        if let Some(bg) = &renderer.saved_background {
            u32_out(&mut output, bg.address);
            blob_out(&mut output, &bg.pixels);
        } else {
            u32_out(&mut output, 0);
            blob_out(&mut output, &[]);
        }
        u32_out(&mut output, result.observations.len() as u32);
        for event in result.observations {
            u32_out(&mut output, event.kind);
            u32_out(&mut output, event.address);
            output.write_all(&event.name).unwrap();
            u32_out(&mut output, event.count);
            for v in event.args {
                u32_out(&mut output, v as u32);
            }
            output.write_all(&event.before).unwrap();
            output.write_all(&event.after).unwrap();
        }
        output.flush().unwrap();
    }
}
