"""Stable native/harness provenance for input proofs; no live reference-source gate."""
import hashlib,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def sources():
 paths=sorted(set((ROOT/'motor/crates').rglob('*.rs'))|set((ROOT/'motor/crates').rglob('Cargo.toml'))|set((ROOT/'motor/include').glob('*'))|set((ROOT/'motor/testes').glob('*.py'))|set((ROOT/'motor/testes').glob('*pins*.json'))|{ROOT/'motor/Cargo.toml',ROOT/'motor/Cargo.lock'})
 return {str(p.relative_to(ROOT)):sha(p) for p in paths if p.is_file()}
def begin(binary):
 return dict(source_revision=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),source_dirty=bool(subprocess.check_output(['git','-C',str(ROOT),'status','--porcelain'],text=True)),source_sha256=sources(),binary_sha256=sha(binary))
def finish(before,binary):
 if before['source_sha256']!=sources() or before['binary_sha256']!=sha(binary):raise ValueError('Native input proof sources/binary changed while running')
 return dict(before,source_stable=True,binary_stable=True)
