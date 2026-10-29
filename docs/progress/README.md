# Progress report snapshots

The live consolidated report is [docs/PROGRESS.md](../PROGRESS.md). It separates implementation, original validation, main integration and complete-flow testing for every L/R stage, and includes a Portuguese executive summary.

- [Recovery baseline CXR-20261028-01](2026-10-28-CXR-01-baseline.md): first visibility snapshot, round still in progress, research main `8810b37`.

- [Closed recovery CXR-20261028-01](2026-10-28-CXR-01-closed.md): research main advanced from8810b37 to5d24c91 with verified Core15 and AI initialization providers; full MissionLoad still unaccepted.

- [Closed Core16 round CXR-20261028-02](2026-10-28-CXR-02-closed.md): verified research mainb4c5a10, bindings/classification/getters integrated; final remap and M1 still pending.

- [Closed Missions11 round CXR-20261028-03](2026-10-28-CXR-03-closed.md): complete placement integrated/reproduced at7f617fa; Economy inventory reconciled at2456848; M1 still unaccepted.

- [Closed full-remap round CXR-20261028-04](2026-10-28-CXR-04-closed.md): whole Chemin_Remap integrated/reproduced at09d3953; actual MissionLoad still unaccepted.

- [Closed Economy query round CXR-20261028-05](2026-10-28-CXR-05-closed.md):3actual initialization queries validated/integrated/reproduced at85dc813; actual AI adapter and wholeMissionLoad still pending.

- [AI adapter proof checkpoint CXR-20261028-06](2026-10-28-CXR-06-checkpoint.md): unchanged main85dc813;11fresh original comparisons passed, adapter main integration/fullgate pending at development cutoff.

- [Closed Claude resumption round CXR-20261028-07](2026-10-28-CXR-07-closed.md): AI adapter `977c890`, Core XP `3d782ca` and the whole original MissionLoad oracle `14c0122` integrated/reproduced; Python composition pending, M1 not accepted.

- [Closed M1 acceptance round CXR-20261028-08](2026-10-28-CXR-08-closed.md): strict Python MissionLoad composition equals the original at `927c7e5`; **M1 accepted**; M2 next.

- [Closed M2 round 1 CXR-20261029-M2R1](2026-10-29-M2R1-closed.md): six M2 fronts integrated, including the first-frame original capture at `ec931d2`; frame composition pending, M2 not accepted.

- [Closed M2 round 2 CXR-20261029-M2R2](2026-10-29-M2R2-closed.md): frame-0/1 callees validated at exact inputs and integrated at `67fb81f`; display path to be executed in the oracle; M2 not accepted.

- [Closed M2 round 3 CXR-20261029-M2R3](2026-10-29-M2R3-closed.md): chained frame-0/1 composition equal on v1; display-scenario reference adopted at `81e0a26`; M2 not accepted.

At each actual execution-round closure, append a new `YYYY-MM-DD-CXR-NN-closed.md` snapshot copied from the verified live report and add it here. Keep a failed/pending round too, with its unchanged main SHA and reason. Never edit a prior snapshot to reflect later success. A repeated heartbeat without a changed round disposition does not require a duplicate snapshot.
