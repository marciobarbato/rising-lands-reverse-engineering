# Validation and evidence rules

## Reproducible local checks

```sh
python3 -B scripts/check.py
python3 -B scripts/check.py --domain core
python3 -B scripts/check.py --domain combat
python3 -B scripts/check.py --domain economy
python3 -B scripts/check.py --domain graphics
python3 -B scripts/check.py --domain missions
python3 -B scripts/check.py --domain ai-runtime
python3 -B scripts/check.py --domain audio
```

The common runner uses unittest discovery without rewriting versioned validation reports. It checks the maintained documentation's relative links, excludes immutable local archives, and runs the requested research suites. Missing graphics copied inputs produce an explicit missing-input result; full integration requires those inputs. Optional differential tests are skipped unless enabled. Read skipped counts and reasons rather than calling a local-only run an x86 verification.

Core needs Python 3.9+. PE extraction requires `pefile==2024.8.26` and `capstone>=5.0.7,<6` from `requirements.txt`. Optional x86 validation uses `unicorn==2.1.4` from `requirements-emulacao.txt`. Existing shared libraries in `../source/python` and `.local/python` are reused. A fresh installation can use a local virtual environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install -r requirements-emulacao.txt
```

On this workspace, the worktree helper links existing read-only local inputs. It does not download or install anything. Keep package installation separate from changes to originals or another worker's tools.

## Differential runs and reports

```sh
python3 -B ferramentas/validar.py --emular
python3 -B pesquisas-paralelas/combate/validar.py --emular
python3 -B pesquisas-paralelas/economia/validar.py --emular
RISING_EMULAR=1 python3 -B scripts/check.py
python3 -B pesquisas-paralelas/missoes/validar.py --emular
RISING_EMULAR=1 python3 -B -m unittest discover -s pesquisas-paralelas/ia-runtime/testes -p 'test_*.py' -v
```

Integration runs the common check plus the front's declared native suite (missions, ai-runtime) or app build (macos) inside the merge candidate; see [parallel work](PARALLEL_WORK.md).

Graphics has individual original-x86 validators documented in [graphics](GRAPHICS.md). Run changed routines' reference tests in the owning worktree and commit the resulting owned reports. Do not regenerate another owner's report or imply independent suites form a complete gameplay test.

The harness maps sections from the original executable identified by SHA-256 and executes declared x86 intervals with synthetic memory/registers. It offers no Win32 imports or complete Windows runtime. It configures flat x86 segments for Watcom string operations. Typical calls have instruction/time limits and must reach a declared stop. Some large routines use bounded checkpoints while retaining registers and stack. An expected dependency stop, deliberately tested exception, or expected limit must be identified explicitly.

Earlier macOS sandbox runs encountered SIGILL when Unicorn could not create JIT memory. An ordinary authorized execution context worked. If this happens, report the failed execution accurately and use the available permitted environment; never disable OS protections or fabricate a reference pass. The Python-only preview does not need Unicorn or Rosetta.

## Whole-routine oracles

Milestones M1/M2 of [the roadmap](ROADMAP_MONDE01.md) compare complete routines (`MissionLoad`, `CalculGame` frames) rather than intervals. The rules are the same as for bounded runs, with two additions: every Windows import or game I/O wrapper reached is a **declared binding** that records its exact arguments and the fixture value returned (file bytes from the real ETA, a deterministic allocation arena, fixed clock values, recorded sound posts), and the comparison covers the whole mapped state at the original return or at the declared stop. No engine routine is replaced by Python inside an oracle run. A binding the fixture cannot honor stops the run and is reported as a stop, never as a pass.

## Required evidence for new findings

Record original input hash, virtual address/range, bytes, calling convention, memory/register inputs, supported domain, output/mutation order, stops, delegated calls, and unsupported dependencies. Distinguish direct observation, inferred interpretation, synthetic fixture, disk data, post-load state, and whole-game behavior.

Tests should compare original instructions or independent captured buffers, cover meaningful boundaries and mutations, and preserve fixed-width arithmetic, signedness, RNG order, partial failures, and caller ordering. Do not validate a guessed formula only with the same formula written a second way.

The manifest `relatorios/fontes.json` records 52 original corpus files. Hash verification must cover size and SHA-256 after organizational moves. Frozen graphics manifests and predecessor hashes remain unchanged. The organization check record states exactly which checks were rerun and which saved reports remain historical.
