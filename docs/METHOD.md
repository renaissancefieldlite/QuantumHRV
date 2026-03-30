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

In stack terms, this repo belongs to the narrower transition-cadence program.
It is compatible with the broader Codex 67 paper and architecture layer, but it
does not collapse that wider architecture into a single pulse claim. The
broader spiritual-attractor-overlap read remains an interpretation layer that
can later be compared against this repo's outputs rather than forced into them.

The next stronger step for this lane is `v4`: rerun the method against a more
directly observed device-linked or session-linked time series so the HRV layer
is no longer limited to simulation and hardware-derived traces.
