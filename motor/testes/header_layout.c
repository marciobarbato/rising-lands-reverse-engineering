/* Small ABI layout check; no engine implementation in C. */
#include <stddef.h>
#include "rising_engine.h"
_Static_assert(sizeof(RlMundo)==8, "handle width");
_Static_assert(sizeof(RlRegisters)==28, "seven u32 data registers");
_Static_assert(offsetof(RlRegisters,edx)==12, "EDX offset");
_Static_assert(sizeof(RlBloco)==16, "64-bit host block descriptor");
_Static_assert(offsetof(RlBloco,data)==8, "host pointer alignment");

_Static_assert(sizeof(RlFrameRegisters)==32, "eight u32 phase registers");
_Static_assert(sizeof(RlFrameInput)==72, "phase input layout");
_Static_assert(offsetof(RlFrameInput,registers)==12, "phase register offset");
_Static_assert(offsetof(RlFrameInput,saved)==44, "saved words offset");
_Static_assert(sizeof(RlFrameEvent)==72, "phase event layout");
_Static_assert(offsetof(RlFrameEvent,stack_mask)==68, "known stack mask offset");
_Static_assert(sizeof(RlRenderBytes)==16, "render byte descriptor");
_Static_assert(sizeof(RlRenderCache)==40, "render cache input");
_Static_assert(sizeof(RlRenderResult)==304, "render result");
_Static_assert(offsetof(RlRenderResult,generation)==8, "render generation alignment");
_Static_assert(offsetof(RlRenderResult,stop_address)==56, "render stop address");
_Static_assert(sizeof(RlRenderObservation)==108, "render observation");
