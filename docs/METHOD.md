# Method

The HRV metrics in this repo are real computations on a time series. What
matters is where the time series came from.

- In simulation mode the trace is a designed low-frequency coherence model.
- In hardware-derived mode the trace is a coherence proxy built from
  calibration-style hardware parameters.

Those metrics can describe variability in the trace. They do not, by
themselves, establish that a real quantum device has a biological-style
heartbeat or that the dominant cadence is intrinsic to hardware rather than to
selection, routing, or state transition dynamics.
