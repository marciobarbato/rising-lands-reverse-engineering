# Later-chain native contracts

This continuation uses profile `chain8`, with logic, graphics and transitive
imports pinned to `92fab50ccfa14271f6657fc0f6032b6b4b68dd4b` through Git objects.
Older profiles are unchanged. The intact execution oracle is RISING.EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
The normalized analysis PE is never executed as that oracle. The C ABI remains
1.6 and renderer contract 1.9; no existing layout or signature changes.

## Inputs and typed interfaces

All providers consume the current owned `MemoriaJogo` projection. Unit identifiers
are 16-bit indices into the original 276-byte records at `[0x4e19a0]`;
structures use `0x49a0c8 + 276*index`. Resources, Bag entries, occupancy, terrain,
vision, minimap, paths, RNGs and all relevant static tables are explicit input
bytes. Absent bytes fail with their address and width; no fabricated page,
empty callback, hidden oracle reload or captured later-state repair is used.
Fixture transport may coalesce adjacent declared spans without adding bytes.

`chain_stage5` names ending `:effects`, `:AL` or `:AX` describe internal typed
interfaces. Their masks explicitly exclude only discarded x86 scratch results.
Those results are never guessed and passed to a dependent provider. Full-register
query APIs compare all eight GPRs; EIP/EFLAGS and original callee stack scratch
writes are outside the native ABI. Search routines requiring stack residue receive
the original stack bytes in full-register fixtures; semantic production searches
return the cell identifier only.

## Mutation and callback order

- Structure entry/state13 is documented in CHAIN7_AUDIT.md. Cave habitation sets
  technology, discovery/light and timers before lodging completes.
- Work state5 (0x456600) validates its depot before CalculWorkEngin (0x44bc74).
  Food phases0–3 and stone phases0–5 preserve each timer, animation, movement,
  RNG draw, resource debit/credit and Bag mutation in the pinned owner order.
  Mine state/index, terrain harvesting, animation and work voices are concrete
  providers. Depot mode1, depleted mines and other types keep addressed stops.
- Fatigue (EnginSetFatigue 0x453b84) saves state/target before the food search,
  then searches a free sack or an own cave, changes state and releases the path.
  Its sound request uses the actual call site0x44b33d. TerrainEstGc, vegetation,
  free-cell, passability and blocking queries inspect live tables and occupancy.
- Hunger body0x4554db–0x454ccd checks the saved state and relevant structures,
  moves until arrival, consumes terrain food or debits own cave food, refills
  provisions, tests TerrainEstDecouvert with its full0x1f mask, issues the meal sound
  request at0x455660 (search-found request at0x45582d), then restores
  the saved order. EnginRestaureEtat0x45315f retains per-state reset/target/order
  sequencing. BatimentEnleveMatiere0x4235bd debits total and RMI, saturating each,
  before cave stock recalculation. Tag19 preserves selection iteration and the
  first live unit's speech order.
- Tag17 recruitment debits before resetting the request/rally state.
  SortieTroupe0x420e4c converts using the actual direction, restores health and
  fatigue, records experience at0x4e19c4, then inserts occupancy, vision and
  minimap. The abandonment branch precedes the common request-reset/message tail.
  Tag33 releases the lodged colonist through the same concrete physical providers.
  Recruitment icons read the current request/status and actual resource costs.
- Combat tag14 uses BatimentInitAttaqueSelect0x4242cc and the complete
  BatimentPeutAttaquer mode/type/owner/range/bonus predicate. Targets and queue
  fields are actual inputs; the predicate does not imply a physical turret test.
- Core vision/groups/output-provider code from the prior piece remains active.
  SetMiniMap modes1–7 are native. S1 terrain, list/task, structure-adjacency and
  refuge queries are concrete providers. VoixOffAsk emits the actual sound
  request; fixtures lacking its observed-request inputs are explicitly skipped.
- iagVilleSendMessage executes only the assembly-proved non-AI prefix from
  0x484808: invalid owners and PlayerGetType !=2 return as the original does.
  An actual AI city handler stops at0x48484c; this is not a no-op AI callback.

Display guards add only the finite original-origin lists from the pinned
`origens_efeitos_monde01.json`, with the original player/map64x64/camera0/mode18
context. There is no interpolated origin-domain relaxation.

## Proof boundaries

Advancing proofs load the original frame128 checkpoint once, then carry Rust's
own world and renderer/cache/background state. P6 whole-state uses the published
cumulative mask without widening it; block identities and byte lengths also match.
P3/P7 indicator proof does not imply their whole-state equality. Surfaces compare
pixels, cache, raster-call order, carried backgrounds and explicitly declared
text requests; original nonexecution of AffText remains qualified.

S1 snapshot helpers replay-check the opening snapshot, execute fresh intact-x86
leaves, compare the entire game image and restore/check the opening afterwards.
Register tuples from historical captures are new snapshot variants, not historical
in-situ replays. Blocking variants explicitly declare the live search owner.
Fatigue and hunger input variants list every changed byte and make no mission-flow
claim. Hunger sack variants declare discovery bytes0/1/16/31 and an existing sound
handle. The original itself omits a new sound post; partially discovered cells
retain the original0x1f test. No callback is installed.

Sparse legacy movement fixtures can require additional bytes that the x86 leaf
never read. Those attempts remain failures/dependency evidence, never equality.
Unsupported saved-state validity/abort branches, vehicle/AI handlers, nonzero
terrain-deposit modes and undeclared sound inputs retain named stops. This work
claims the bounded probe windows in its report, not S1/D1 mission completion.
