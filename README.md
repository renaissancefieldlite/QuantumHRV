# QuantumHRV

This is the heartbeat-variability layer for the 0.67 Hz program.

It asks whether coherence traces behave with enough time-domain and frequency-domain structure to justify an HRV-style reading.

This repo now distinguishes:

- `simulation_baseline`: HRV metrics on a modeled coherence trace
- `hardware_derived_model`: HRV metrics on a calibration-anchored coherence
  proxy
- `real_device_timeseries`: pending

## What It Tests

Whether the HRV metric stack produces interpretable time-domain and
frequency-domain summaries under both a designed low-frequency coherence model
and a hardware-derived noise/decoherence trajectory.

## Quick Start

```bash
python3 completehrvcode.py --mode simulation --json
python3 completehrvcode.py --mode hardware-derived --json
```

See [docs/METHOD.md](docs/METHOD.md) and
[docs/EVIDENCE_BOUNDARY.md](docs/EVIDENCE_BOUNDARY.md).
