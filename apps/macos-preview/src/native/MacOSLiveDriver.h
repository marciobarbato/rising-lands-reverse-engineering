#ifndef MACOS_LIVE_DRIVER_H
#define MACOS_LIVE_DRIVER_H
#include <stdint.h>
#include "MacOSAudioMapper.h"
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
uint32_t macos_live_engine_binding(void);
uint32_t macos_live_status_size(void);
MacOSLiveDriver *macos_live_create(const char *library,const char *inputs,char *error,uint32_t capacity);
/* Select before load_tail. Validation is the default for proof consumers.
 * Play mode performs no projection, hash, comparison or observer callback. */
int32_t macos_live_validation(MacOSLiveDriver *,uint32_t);
void macos_live_audit_window(MacOSLiveDriver *,uint32_t);
int32_t macos_live_advance(MacOSLiveDriver *,MacOSPhaseObserver,void *);
/* ABI1.5 descriptor is copied synchronously; arrays must outlive the call. */
typedef struct {uint32_t message,wparam,lparam;} MacOSInputMessage;
typedef struct {uint32_t vk;int32_t value;} MacOSInputKey;
typedef struct {
 uint32_t size,flags;int32_t cursor_x,cursor_y;
 const MacOSInputMessage *messages;uint32_t message_count;
 const MacOSInputKey *keys;uint32_t key_count;
} MacOSDeclaredInput;
/* Input phases are the same calls used by play; this test entry omits rendering.
 * Only at frame128+, play mode, in exact 2/3 order. Context/world never reloaded. */
int32_t macos_live_human_phase(MacOSLiveDriver *,uint32_t);
int32_t macos_live_input_phase(MacOSLiveDriver *,uint32_t,const MacOSDeclaredInput *);
int32_t macos_live_frame_context(MacOSLiveDriver *,uint8_t *,uint32_t);
/* Mac events are scheduled at a game frame, independent of presentation/clock.
 * kind1 mouse,2 key. Returns 0 or a latched named input/queue error. */
int32_t macos_live_event(MacOSLiveDriver *,uint32_t kind,uint32_t message,int32_t x,int32_t y,uint32_t wparam,uint32_t vk,uint32_t down);
/* Optional test/benchmark diagnostics; never called by normal play. */
uint32_t macos_live_order_tags(MacOSLiveDriver *,uint32_t *,uint32_t);
uint64_t macos_live_human_events(MacOSLiveDriver *);
/* Play-mode sound requests: enable after create; each successful input phase
 * appends its kind-10 PostSound/StopSound copies plus PlaySnd_Manage ticks.
 * Draining is the app's only consumer; game state and audits are untouched. */
int32_t macos_live_sound_capture(MacOSLiveDriver *,uint32_t enabled);
uint32_t macos_live_sound_events(MacOSLiveDriver *,MacOSSoundEvent *,uint32_t capacity);
uint64_t macos_live_sound_dropped(MacOSLiveDriver *);
uint64_t macos_live_declared_frames(MacOSLiveDriver *);
void macos_live_status(MacOSLiveDriver *,MacOSLiveStatus *);
uint64_t macos_live_renderer(MacOSLiveDriver *);
const uint8_t *macos_live_pixels(MacOSLiveDriver *);
const uint8_t *macos_live_palette(MacOSLiveDriver *);
int32_t macos_live_read(MacOSLiveDriver *,uint32_t,uint32_t,uint8_t *);
void macos_live_free(MacOSLiveDriver *);
#endif
