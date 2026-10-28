# AI and runtime research

Owned by the AI and Runtime front. The contract, ownership boundary with Core and Missions, planned APIs and stage sequence are in [docs/AI_RUNTIME.md](../../docs/AI_RUNTIME.md); results and requested contracts are in [HANDOFF.md](HANDOFF.md).

Modules in this folder compose committed Core primitives (`ferramentas/ia.py`, `tarefas_ia.py`, `simbolos_ia.py`, `ordens_unidades.py`, `mensagens_chegada.py`, `cadencia.py`) and the other owners' simulation APIs. They must not duplicate those bodies, and every new module basename must be unique across the flat research namespace (`testes/test_namespace.py`).

Evidence (intact original intervals, original-only captures, reviewed REA excerpts) belongs under `evidencias/`; fresh native reports under `validacao/`; tests under `testes/`.
