"""HRV-style analysis for modeled and hardware-derived coherence traces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from hardware_profile import extract_noise_parameters, load_calibration, simulate_noise_trajectory


def entropy_from_circuit(angle: float) -> float:
    circuit = QuantumCircuit(1)
    circuit.ry(angle, 0)
    state = Statevector.from_instruction(circuit)
    probabilities = np.array(state.probabilities(), dtype=float)
    entropy = -np.sum(probabilities * np.log2(np.clip(probabilities, 1e-12, 1.0)))
    return float(entropy)


def build_simulated_series(duration_seconds: float, sample_rate_hz: float, seed: int = 67) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    time_axis = np.arange(int(duration_seconds * sample_rate_hz)) / sample_rate_hz
    base = 0.6 + 0.2 * np.sin(2 * np.pi * 0.67 * time_axis)
    lf = 0.08 * np.sin(2 * np.pi * 0.1 * time_axis)
    hf = 0.05 * np.sin(2 * np.pi * 0.25 * time_axis)
    noise = 0.02 * rng.normal(size=len(time_axis))
    angle_trace = np.clip(base + lf + hf + noise, 0.05, 1.25)
    series = np.array([1.0 - entropy_from_circuit(angle) for angle in angle_trace], dtype=float)
    return time_axis, series


def spectral_metrics(series: np.ndarray, sample_rate_hz: float) -> dict[str, float]:
    centered = series - np.mean(series)
    freqs = np.fft.rfftfreq(len(centered), d=1.0 / sample_rate_hz)
    psd = np.abs(np.fft.rfft(centered)) ** 2
    dominant_idx = int(np.argmax(psd[1:]) + 1) if len(psd) > 1 else 0
    lf_mask = (freqs >= 0.04) & (freqs < 0.15)
    hf_mask = (freqs >= 0.15) & (freqs < 0.4)
    lf_power = float(np.trapezoid(psd[lf_mask], freqs[lf_mask])) if np.any(lf_mask) else 0.0
    hf_power = float(np.trapezoid(psd[hf_mask], freqs[hf_mask])) if np.any(hf_mask) else 0.0
    return {
        "dominant_frequency_hz": float(freqs[dominant_idx]),
        "lf_power": lf_power,
        "hf_power": hf_power,
        "lf_hf_ratio": float(lf_power / hf_power) if hf_power > 0 else 0.0,
    }


def hrv_metrics(series: np.ndarray, sample_rate_hz: float) -> dict[str, float]:
    return {
        "sdnn": float(np.std(series)),
        "rmssd": float(np.sqrt(np.mean(np.diff(series) ** 2))),
        **spectral_metrics(series, sample_rate_hz),
    }


def run_simulation(duration_seconds: float, sample_rate_hz: float) -> dict[str, object]:
    _, series = build_simulated_series(duration_seconds, sample_rate_hz)
    return {
        "mode": "simulation",
        "evidence_status": "simulation_baseline",
        "metrics": hrv_metrics(series, sample_rate_hz),
    }


def run_hardware_derived(calibration_path: str | None, duration_seconds: float, sample_rate_hz: float) -> dict[str, object]:
    calibration = load_calibration(calibration_path)
    params = extract_noise_parameters(calibration)
    report = simulate_noise_trajectory(params, duration_seconds=duration_seconds, sample_rate_hz=sample_rate_hz)
    series = np.array(report["time_series"]["coherence_proxy"], dtype=float)
    return {
        "mode": "hardware-derived",
        "evidence_status": "hardware_derived_model",
        "noise_summary": report["summary"],
        "metrics": hrv_metrics(series, sample_rate_hz),
    }


def main() -> dict[str, object]:
    parser = argparse.ArgumentParser(description="Run bounded quantum HRV analysis.")
    parser.add_argument("--mode", choices=["simulation", "hardware-derived"], default="simulation")
    parser.add_argument("--calibration")
    parser.add_argument("--duration", type=float, default=180.0)
    parser.add_argument("--sample-rate", type=float, default=20.0)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()

    result = run_simulation(args.duration, args.sample_rate) if args.mode == "simulation" else run_hardware_derived(args.calibration, args.duration, args.sample_rate)
    result["schema_version"] = "rfl.quantum_hrv.v2"
    result["next_step"] = "Run the same HRV metric stack on observed device time series."

    if args.output:
        output_path = Path(args.output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"mode={result['mode']}")
        print(f"dominant_frequency_hz={result['metrics']['dominant_frequency_hz']:.4f}")

    return result


if __name__ == "__main__":
    main()
