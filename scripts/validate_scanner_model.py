#!/usr/bin/env python3
"""
Validate data/scanner-model.json for structural and reference integrity.

Checks:
  - JSON parses without error
  - All required top-level keys present
  - Every signal has required fields and numeric defaultValue in 0-100
  - No duplicate signal keys
  - Scoring weight arrays reference existing signal keys only
  - Weights for each classification type sum to 1.0
  - Derived metrics reference valid signals or classification scores
  - Confidence thresholds are present and numeric
  - Narratives cover all classification types
  - No duplicate preset IDs or names
  - Every preset contains a value for every signal, each 0-100
  - Dispatch example IDs resolve to existing dispatch HTML files
  - Wave dispatch map IDs resolve to existing dispatch HTML files

Exit codes:
  0 = model is valid
  1 = one or more validation errors found
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_TOP_KEYS = {
    "_meta", "signals", "scoring", "derivedMetrics",
    "confidence", "layers", "narratives", "presets",
    "dispatchExamples", "waveDispatchMap",
}

REQUIRED_SCORING_TYPES = {"miner", "shovel", "gatekeeper"}

REQUIRED_CONFIDENCE_KEYS = {
    "lowScoreThreshold", "hybridSpreadThreshold",
    "highSpreadThreshold", "highMinScore",
}

REQUIRED_NARRATIVE_TYPES = {"classification", "matters", "limits"}

REQUIRED_SIGNAL_FIELDS = {
    "key", "label", "description", "leftLabel", "rightLabel", "defaultValue",
}

REQUIRED_PRESET_FIELDS = {"id", "name", "actorType", "marketWave", "values"}

VALID_DERIVED_FORMULAS = {"avg", "score", "signal"}

VALID_SCORE_SOURCES = {"miner", "shovel", "gatekeeper"}


def _repository_root(root_arg: str | None) -> Path:
    if root_arg:
        return Path(root_arg).resolve()
    return Path(__file__).resolve().parents[1]


def validate(model_path: Path, root: Path) -> list[str]:
    errors: list[str] = []

    def fail(msg: str) -> None:
        errors.append(msg)

    # ── 1. Parse JSON ──────────────────────────────────────────────────────
    try:
        data = json.loads(model_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"JSON parse error: {exc}")
        return errors
    except OSError as exc:
        fail(f"Cannot read model file: {exc}")
        return errors

    if not isinstance(data, dict):
        fail("Model root must be a JSON object")
        return errors

    # ── 2. Required top-level keys ─────────────────────────────────────────
    for key in sorted(REQUIRED_TOP_KEYS):
        if key not in data:
            fail(f"Missing top-level key: {key!r}")

    if errors:
        return errors  # structure too broken to continue

    # ── 3. Validate signals ────────────────────────────────────────────────
    signals_raw = data["signals"]
    signal_keys: set[str] = set()

    if not isinstance(signals_raw, list) or not signals_raw:
        fail("'signals' must be a non-empty array")
    else:
        for idx, sig in enumerate(signals_raw):
            if not isinstance(sig, dict):
                fail(f"signals[{idx}] must be an object")
                continue
            for field in sorted(REQUIRED_SIGNAL_FIELDS):
                if field not in sig:
                    fail(f"signals[{idx}] missing field {field!r}")
            skey = sig.get("key")
            if skey:
                if skey in signal_keys:
                    fail(f"Duplicate signal key: {skey!r}")
                signal_keys.add(skey)
            dv = sig.get("defaultValue")
            if dv is not None and not (isinstance(dv, (int, float)) and 0 <= dv <= 100):
                fail(f"signals[{idx}] ({skey!r}) defaultValue must be numeric 0-100, got {dv!r}")

    # ── 4. Validate scoring weights ────────────────────────────────────────
    scoring = data["scoring"]
    if not isinstance(scoring, dict):
        fail("'scoring' must be an object")
    else:
        for stype in sorted(REQUIRED_SCORING_TYPES):
            if stype not in scoring:
                fail(f"scoring missing type: {stype!r}")
                continue
            entries = scoring[stype]
            if not isinstance(entries, list):
                fail(f"scoring.{stype} must be an array")
                continue
            total = 0.0
            for entry in entries:
                if not isinstance(entry, dict):
                    fail(f"scoring.{stype}: each entry must be an object")
                    continue
                sig_ref = entry.get("signal")
                weight = entry.get("weight")
                if sig_ref is None or weight is None:
                    fail(f"scoring.{stype}: entry must have 'signal' and 'weight'")
                    continue
                if sig_ref not in signal_keys:
                    fail(f"scoring.{stype}: unknown signal {sig_ref!r}")
                if not isinstance(weight, (int, float)):
                    fail(f"scoring.{stype}: weight for {sig_ref!r} must be numeric")
                else:
                    total += weight
            if signal_keys and abs(total - 1.0) > 0.001:
                fail(f"scoring.{stype}: weights sum to {total:.4f}, expected 1.0")

    # ── 5. Validate derived metrics ────────────────────────────────────────
    derived = data["derivedMetrics"]
    if not isinstance(derived, dict):
        fail("'derivedMetrics' must be an object")
    else:
        for metric_name, metric_def in derived.items():
            if not isinstance(metric_def, dict):
                fail(f"derivedMetrics.{metric_name} must be an object")
                continue
            formula = metric_def.get("formula")
            if formula not in VALID_DERIVED_FORMULAS:
                fail(f"derivedMetrics.{metric_name}: unknown formula {formula!r}")
                continue
            if formula == "avg":
                comps = metric_def.get("components")
                if not isinstance(comps, list) or not comps:
                    fail(f"derivedMetrics.{metric_name}: 'avg' requires non-empty 'components'")
                else:
                    for comp in comps:
                        sig_ref = comp.get("signal")
                        if sig_ref not in signal_keys:
                            fail(f"derivedMetrics.{metric_name}: unknown signal {sig_ref!r}")
            elif formula == "score":
                source = metric_def.get("source")
                if source not in VALID_SCORE_SOURCES:
                    fail(f"derivedMetrics.{metric_name}: invalid score source {source!r}")
            elif formula == "signal":
                source = metric_def.get("source")
                if source not in signal_keys:
                    fail(f"derivedMetrics.{metric_name}: unknown signal source {source!r}")

    # ── 6. Validate confidence thresholds ──────────────────────────────────
    conf = data["confidence"]
    if not isinstance(conf, dict):
        fail("'confidence' must be an object")
    else:
        for key in sorted(REQUIRED_CONFIDENCE_KEYS):
            if key not in conf:
                fail(f"confidence missing key: {key!r}")
            elif not isinstance(conf[key], (int, float)):
                fail(f"confidence.{key} must be numeric, got {type(conf[key]).__name__}")

    # ── 7. Validate narratives ─────────────────────────────────────────────
    narr = data["narratives"]
    if not isinstance(narr, dict):
        fail("'narratives' must be an object")
    else:
        for ntype in sorted(REQUIRED_NARRATIVE_TYPES):
            if ntype not in narr:
                fail(f"narratives missing type: {ntype!r}")
            elif not isinstance(narr[ntype], dict):
                fail(f"narratives.{ntype} must be an object")

    # ── 8. Validate presets ────────────────────────────────────────────────
    presets_raw = data["presets"]
    if not isinstance(presets_raw, list) or not presets_raw:
        fail("'presets' must be a non-empty array")
    else:
        preset_names: set[str] = set()
        preset_ids: set[str] = set()
        for preset in presets_raw:
            if not isinstance(preset, dict):
                fail("Each preset must be an object")
                continue
            for field in sorted(REQUIRED_PRESET_FIELDS):
                if field not in preset:
                    fail(f"Preset {preset.get('name', '?')!r} missing field {field!r}")
            pid = preset.get("id")
            pname = preset.get("name")
            if pid:
                if pid in preset_ids:
                    fail(f"Duplicate preset id: {pid!r}")
                preset_ids.add(pid)
            if pname:
                if pname in preset_names:
                    fail(f"Duplicate preset name: {pname!r}")
                preset_names.add(pname)
            vals = preset.get("values")
            if isinstance(vals, dict) and signal_keys:
                for skey in signal_keys:
                    if skey not in vals:
                        fail(f"Preset {pname!r} missing signal value: {skey!r}")
                for k, v in vals.items():
                    if k not in signal_keys:
                        fail(f"Preset {pname!r} has unknown signal: {k!r}")
                    elif not (isinstance(v, (int, float)) and 0 <= v <= 100):
                        fail(f"Preset {pname!r} signal {k!r} must be 0-100, got {v!r}")

    # ── 9. Validate dispatch file references ──────────────────────────────
    dispatch_dir = root / "dispatch"
    all_referenced_ids: set[str] = set()

    ex_map = data["dispatchExamples"]
    if isinstance(ex_map, dict):
        for cls_type, examples in ex_map.items():
            if not isinstance(examples, list):
                fail(f"dispatchExamples.{cls_type!r} must be an array")
                continue
            for ex in examples:
                eid = ex.get("id") if isinstance(ex, dict) else None
                if not eid:
                    fail(f"dispatchExamples.{cls_type!r}: entry missing 'id'")
                else:
                    all_referenced_ids.add(eid)
    else:
        fail("'dispatchExamples' must be an object")

    wave_map = data["waveDispatchMap"]
    if isinstance(wave_map, dict):
        for wave, ids in wave_map.items():
            if not isinstance(ids, list):
                fail(f"waveDispatchMap.{wave!r} must be an array")
                continue
            for did in ids:
                all_referenced_ids.add(did)
    else:
        fail("'waveDispatchMap' must be an object")

    for did in sorted(all_referenced_ids):
        dispatch_file = dispatch_dir / f"{did}.html"
        if not dispatch_file.exists():
            fail(f"Dispatch file not found: dispatch/{did}.html")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate data/scanner-model.json for structural and reference integrity."
    )
    parser.add_argument(
        "--root",
        default=None,
        help="Repository root. Defaults to the parent directory of this script's directory.",
    )
    parser.add_argument(
        "--json",
        default=None,
        dest="json_report",
        help="Optional path for a JSON report file.",
    )
    args = parser.parse_args(argv)

    root = _repository_root(args.root)
    model_path = root / "data" / "scanner-model.json"

    print("=" * 60)
    print("Scanner Model Validator")
    print(f"Model : {model_path}")
    print(f"Root  : {root}")
    print("=" * 60)

    if not model_path.exists():
        print(f"\nFAIL: Model file not found: {model_path}\n")
        return 1

    errors = validate(model_path, root)

    if args.json_report:
        import json as _json
        report = {"passed": not errors, "errors": errors}
        Path(args.json_report).write_text(
            _json.dumps(report, indent=2), encoding="utf-8"
        )

    if errors:
        print(f"\nFAIL: {len(errors)} error(s) found:\n")
        for e in errors:
            print(f"  - {e}")
        print()
        return 1

    print("\nPASS: Scanner model is valid.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
