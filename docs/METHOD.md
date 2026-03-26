# Method

The HRV metrics in this repo are real computations on a time series. What
matters is where the time series came from.

- In simulation mode the trace is a designed low-frequency coherence model.
- In hardware-derived mode the trace is a coherence proxy built from
  calibration-style hardware parameters.

Those metrics describe variability in the trace and let this repo compare a designed cadence model against a hardware-derived coherence proxy. The next stronger step is a real device time series so the same HRV stack can be run on observed data.
