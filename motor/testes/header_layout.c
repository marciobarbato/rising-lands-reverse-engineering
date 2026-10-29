/* Small ABI layout check; no engine implementation in C. */
#include <stddef.h>
#include "rising_engine.h"
_Static_assert(sizeof(RlMundo)==8, "handle width");
_Static_assert(sizeof(RlRegisters)==28, "seven u32 data registers");
_Static_assert(offsetof(RlRegisters,edx)==12, "EDX offset");
_Static_assert(sizeof(RlBloco)==16, "64-bit host block descriptor");
_Static_assert(offsetof(RlBloco,data)==8, "host pointer alignment");
