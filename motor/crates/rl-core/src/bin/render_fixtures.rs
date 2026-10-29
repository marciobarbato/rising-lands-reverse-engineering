//! Test-only offline batch driver: explicit original inputs, never emulates x86.
use rl_core::{
    render::{Cache, Renderer},
    render_assets::Assets,
    MemoriaJogo,
};
use std::{fs, io::Write, path::PathBuf, sync::Arc};
struct Reader {
    data: Vec<u8>,
    p: usize,
}
impl Reader {
    fn u32(&mut self) -> u32 {
        let v = u32::from_le_bytes(self.data[self.p..self.p + 4].try_into().unwrap());
        self.p += 4;
        v
    }
    fn bytes(&mut self, n: usize) -> Vec<u8> {
        let v = self.data[self.p..self.p + n].to_vec();
        self.p += n;
        v
    }
    fn blob(&mut self) -> Vec<u8> {
        let n = self.u32() as usize;
        self.bytes(n)
    }
}
fn main() {
    let args: Vec<_> = std::env::args().collect();
    let mut input = Reader {
        data: fs::read(&args[1]).unwrap(),
        p: 0,
    };
    let out = PathBuf::from(&args[2]);
    fs::create_dir_all(&out).unwrap();
    assert_eq!(input.bytes(8), b"RLRF1500");
    let blobs: Vec<_> = (0..9).map(|_| input.blob()).collect();
    let refs: Vec<_> = blobs.iter().map(|b| b.as_slice()).collect();
    let assets = Arc::new(Assets::load(&refs).unwrap());
    let count = input.u32();
    for case in 0..count {
        let tick = input.u32();
        let mut m = MemoriaJogo::default();
        for _ in 0..input.u32() {
            let base = input.u32();
            let bytes = input.blob();
            m.declare(base, bytes).unwrap();
        }
        let surface = input.blob();
        let keys = input.blob();
        let raw = input.blob();
        let cursor = input.u32() as u16;
        let mut renderer =
            Renderer::new(Arc::clone(&assets), &surface, Cache { keys, raw, cursor }).unwrap();
        if tick != u32::MAX {
            renderer.tick = Some(tick);
        }
        let result = renderer.render(&m, true).unwrap();
        fs::write(out.join(format!("{case}.pixels")), &renderer.surface).unwrap();
        let mut cache = renderer.cache.keys;
        cache.extend(renderer.cache.raw);
        cache.extend((renderer.cache.cursor as u32).to_le_bytes());
        fs::write(out.join(format!("{case}.cache")), cache).unwrap();
        let mut obs = fs::File::create(out.join(format!("{case}.observations"))).unwrap();
        for o in result.observations {
            let name = String::from_utf8_lossy(&o.name);
            let name = name.trim_end_matches('\0');
            if o.kind == 2 {
                writeln!(obs, "{} {:?}", name, &o.args[..o.count as usize]).unwrap();
            } else if o.kind == 1 {
                writeln!(
                    obs,
                    "effect {} {} {:?} {:?}",
                    name,
                    o.address,
                    &o.before[..o.count as usize],
                    &o.after[..o.count as usize]
                )
                .unwrap();
            }
        }
        println!("{} {} {:?}", case, result.disposition, result.stop);
    }
    assert_eq!(input.p, input.data.len());
}
