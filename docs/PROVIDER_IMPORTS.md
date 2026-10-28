# Explicit consumer provider imports

Economy and graphics both have a historical flat `construcoes.py`. Loading the
graphic reader under that name first makes economy's `extracao` fail to import
`TerrenoSacolas`. The mission Stage 7 subprocess regression correctly avoided
that collision, but did not demonstrate same-process coexistence.

[The coordinator-owned loaders](../integracao/providers.py) resolve this
specific bootstrap dependency without editing either research implementation:

```python
from integracao.providers import load_graphics_structures, load_economy_resources

graphics = load_graphics_structures()
resources_module = load_economy_resources()
resources = resources_module.RecursosTerreno(minas=inherited_mines80)
records = graphics.ler_estruturas_eta(original_eta_bytes)
```

Both loader orders work. The graphics structures module gets the unique name
`_risinglands_graphics_construcoes`; its `graficos` dependency is the actual
same-checkout module. Economic `economia`, `construcoes` and `extracao` keep
their original names and class identities. Existing bindings from this checkout
are reused. All required bindings are checked before missing providers load;
foreign, missing-origin or legacy-conflicting bindings raise `ImportError`.
No existing module binding, `sys.path`, provider source or original input is
replaced. A failing new import removes only its own new binding.

Call these loaders during consumer bootstrap, before unrelated legacy flat
imports or worker threads start. They do not repair a process that already
bound graphic structures to flat `construcoes`, migrate historical tests,
initialize a world, or claim to namespace every research module. Consumers
must use `graphics.ler_estruturas_eta` instead of the ambiguous flat import.
The committed mission suite still has its original imports until its owner
adopts this API in a separate owned change. The delivered app is pinned to its
recorded main revision and needs no rebuild for this maintenance alone.

[Regression tests](../scripts/tests/test_provider_imports.py) use isolated
ordinary Python processes to test **both actual providers together within each
process**, in both bootstrap orders. They additionally run the actual mission
mine and structure loaders over the same live economic buffers, preserve mine
reserve words and structure tails, and check class/module identity. Negative
cases reproduce the legacy collision and reject foreign checkout bindings
without swaps. These are synthetic consumer checks, not new native algorithm
comparisons or original-mission execution.

Run `python3 -B -m unittest discover -s scripts/tests -p test_provider_imports.py -v`
and the full `python3 -B scripts/check.py`. Integration must use a separate
reviewed coordinator candidate and the common `.git/rising-integration.lock`
through fetch, checks and non-force main push. No four-domain ownership rule is
bypassed and no extra research chat is created.
