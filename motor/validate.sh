#!/bin/sh
# Run from any directory; writes build outputs only under motor/target.
set -eu
cd "$(dirname "$0")"
cargo fmt --all --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --locked
cargo build --workspace --locked
python3 -B -m unittest discover -s testes -v
python3 -B testes/differential.py
if [ "$(uname -s)" = Darwin ]; then
    xcrun clang -std=c11 -fsyntax-only -I include testes/header_layout.c
    xcrun swiftc -I include -L target/debug -lrising_engine \
        -Xlinker -rpath -Xlinker "$(pwd)/target/debug" \
        -module-cache-path target/swift-module-cache \
        testes/abi_smoke.swift -o target/abi-smoke
    target/abi-smoke
else
    echo 'Swift/macOS interoperability is not run on this host; the pilot delivery requires aarch64-apple-darwin.'
fi
