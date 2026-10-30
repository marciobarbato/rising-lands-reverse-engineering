# Continuation audit: structure entry, habitation and later work

Execution identity: intact RISING.EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
The normalized analysis executable is not an execution oracle.

The recovered `acaa7c2` implementation was unvalidated. It is reviewed against
Core `entrada_estruturas.py`, Economy `caverna_recrutamento.py` and
`ciclo_trabalho.py` at immutable `89575fad00ad3ee506879b275bdceb8f63423baf`.
Graphics remains separately pinned at `24f0ec85714dbbfa4645212ca81f8f4145a76143`.
All transitive imports and original evidence are read from verified Git objects.
Earlier logic/input/chain5/chain6 profiles and evidence remain unchanged.

The Bag API retains original flat addresses and tags; capacity scans differ
from count scans. BagRetire shifts tags then words and finally clears the last
slot. Register wrappers compare all eight registers; typed effects/AL APIs
explicitly exclude scratch registers that their production callers discard.
They never supply guessed scratch values to game logic.

State13 (0x4558e4) checks destruction and ownership before lodging or movement.
RetireEngin (0x457058) deselects, removes occupancy at current then next cell,
clears physical presence, removes its minimap mark, then extinguishes sight.
Lodging credits carried stone before food and takes ownership before habitation,
minimap, owner counters and sound. It appends the unit only after those effects.
BatimentHabitable (0x41cc70) sets technology before radius discovery/light and
writes the final +0x84 timer. Typed providers discard x86 scratch registers.

Unknown vehicle, diplomacy, nonzero terrain-deposit and unsupported technology
paths retain addressed errors. Sparse leaf fixtures can expose additional
reads by the existing whole-world movement providers; such errors are failures
or documented dependency stops, never leaf equality. No captured later state
may repair an advancing Rust world.

Subsequent stages use a new immutable profile for the owner providers at
`92fab50` (full SHA in that profile). Work state5 enters at 0x456600, validates
its depot before CalculWorkEngin 0x44bc74; hunger state19 enters at 0x4554db.
EnginRestaureEtat 0x45315f restores saved orders; BatimentEnleveMatiere 0x4235bd
must debit total AND RMI before recalculating cave stock. Recruitment must run
SortieTroupe 0x420e4c through its request reset and messages, with abandonment
before that common tail. Turret tag14 calls BatimentInitAttaqueSelect 0x4242cc.
No ABI addition is needed for internal providers or the separate fixture binary.
