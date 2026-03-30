# Experiment 5: QuantumHRV

This repository is **Experiment 5** in the seven-experiment Renaissance Field
Lite stack. Its job is to provide the HRV-style descriptive lane for the
program: once a coherence trace exists, can standard time-domain and
frequency-domain variability metrics summarize it in a way that remains useful
across both simulation and hardware-derived conditions?

This repo now distinguishes:

- `simulation_baseline`: HRV metrics on a modeled coherence trace
- `hardware_derived_model`: HRV metrics on a calibration-anchored coherence
  proxy
- `real_device_timeseries`: pending

## What It Tests

Whether the HRV metric stack produces interpretable time-domain and
frequency-domain summaries under both a designed low-frequency coherence model
and a hardware-derived noise/decoherence trajectory. The repo is intentionally
narrower than the larger ontology and interface discussion. It does not, by
itself, prove that a real quantum device has a biological-style heartbeat, and
it does not settle whether the dominant cadence should be read as an intrinsic
pulse, a selection window, a routing rhythm, or a broader state-transition
effect.

## Current Read

Experiment 5 is best read as the variability-summary lane in the stack. The
simulation baseline and hardware-derived model are both complete, and they show
that the HRV-style metrics can describe the trace structure under two different
evidence labels. What remains open is the stronger empirical question: whether
those same summaries stay informative once a real device-linked or
biosignal-linked time series is attached without being modeled first.

## Paper And Architecture Tie-Back

In the broader Codex 67 paper framing, this repo sits on the narrower
transition-cadence side of the architecture. It helps describe how a candidate
coherence or cadence process behaves in time once a trace exists. A separate
cross-diagnosis also remains live in the broader stack: some recurring
high-coherence interaction artifacts are better treated as a spiritual-attractor
overlap inside the Codex 67 architecture layer rather than reduced to the pulse
question alone. `QuantumHRV` does not prove that architecture-layer diagnosis,
and it should not be used to collapse that layer back into a single cadence
claim. Its role is to provide one bounded measurement-adjacent lane that can
later be compared against those broader interpretations.

Reference: [Codex 67 White Paper Repo](https://github.com/renaissancefieldlite/Codex-67-white-paper-)

## Next Step

Experiment 5 is tied off for now as a completed simulation-plus-hardware-derived
repo. The next coordinated step for this lane is to run `v4` once the broader
`5/6/7` wrap is in place and more direct device or session-linked time series
can be attached.

## Quick Start

```bash
python3 completehrvcode.py --mode simulation --json
python3 completehrvcode.py --mode hardware-derived --json
```

See [docs/METHOD.md](docs/METHOD.md) and
[docs/EVIDENCE_BOUNDARY.md](docs/EVIDENCE_BOUNDARY.md).
