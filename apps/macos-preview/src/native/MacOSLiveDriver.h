#ifndef MACOS_LIVE_DRIVER_H
#define MACOS_LIVE_DRIVER_H
#include <stdint.h>
typedef struct MacOSLiveDriver MacOSLiveDriver;
typedef struct {
 uint64_t world, generation, frames, surfaces_equal, phases_equal, checkpoints_equal;
 uint64_t logic_ns, render_ns, proof_ns;
 uint32_t phase_index, disposition, stopped, stop_phase, counter;
 uint8_t state_sha[32], surface_sha[32];
 char message[512];
} MacOSLiveStatus;
/* Opaque app handle owns host buffers and Rust world/renderer; serialize all calls.
 * phase observer runs only in proof tooling, after each successful actual phase.
 * No callback is used by the normal native UI. */
typedef int32_t (*MacOSPhaseObserver)(void *,uint64_t,uint32_t,uint32_t);
uint32_t macos_live_abi_version(void);
uint32_t macos_live_status_size(void);
MacOSLiveDriver *macos_live_create(const char *library,const char *inputs,char *error,uint32_t capacity);
void macos_live_audit_window(MacOSLiveDriver *,uint32_t);
int32_t macos_live_advance(MacOSLiveDriver *,MacOSPhaseObserver,void *);
void macos_live_status(MacOSLiveDriver *,MacOSLiveStatus *);
uint64_t macos_live_renderer(MacOSLiveDriver *);
const uint8_t *macos_live_pixels(MacOSLiveDriver *);
const uint8_t *macos_live_palette(MacOSLiveDriver *);
int32_t macos_live_read(MacOSLiveDriver *,uint32_t,uint32_t,uint8_t *);
void macos_live_free(MacOSLiveDriver *);
#endif
