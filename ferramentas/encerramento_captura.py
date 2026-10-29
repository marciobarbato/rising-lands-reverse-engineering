"""Durable fast exit for native captures, so no Unicorn ``uc_close`` runs at shutdown.

In Unicorn 2.1.4, ``uc_close`` frees the mapped regions one at a time. Each free
commits a QEMU memory transaction that rebuilds the flat view of every region
still mapped, so teardown time grows superlinearly with the region count. The
same holds for ``mem_unmap`` in any order (docs/core/UNICORN_TEARDOWN.md). A
Python process that still owns a ``Uc`` runs ``uc_close`` from the binding's
``weakref.finalize`` during interpreter finalization, after its last line.

A capture script that has written and closed its evidence ends with
``encerrar_captura(codigo, *caminhos)``. It fsyncs each output file and its
directory, flushes stdout/stderr (fsyncing them when they are regular files)
and leaves with ``os._exit``. No finalizer runs and the operating system
reclaims the emulator's memory. Every fsync error propagates, and a missing
output raises before the process exits.

Do not call it from a test runner or a library: it ends the whole process,
skipping ``atexit`` handlers and pending ``finally`` blocks.
"""
import os
import stat
import sys
from pathlib import Path


def _fsync_caminho(caminho):
    fd = os.open(caminho, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def sincronizar(*caminhos):
    """fsync each (already closed) file and then its parent directory."""
    for caminho in map(Path, caminhos):
        if not caminho.is_file():
            raise FileNotFoundError(f'Capture output {caminho} is not a written file')
        _fsync_caminho(caminho)
        _fsync_caminho(caminho.resolve().parent)


def descarregar_saidas_padrao():
    """Flush stdout/stderr; fsync them when redirected to a regular file."""
    for fluxo in (sys.stdout, sys.stderr):
        if fluxo is None:
            continue
        fluxo.flush()
        fd = fluxo.fileno()
        if stat.S_ISREG(os.fstat(fd).st_mode):
            os.fsync(fd)


def encerrar_captura(codigo, *caminhos):
    """Make ``caminhos`` and stdio durable, then end the process with ``codigo``, with no finalization."""
    if not isinstance(codigo, int) or not 0 <= codigo <= 255:
        raise ValueError(f'Exit status {codigo!r} is not 0..255')
    sincronizar(*caminhos)
    descarregar_saidas_padrao()
    os._exit(codigo)
