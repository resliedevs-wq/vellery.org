#!/usr/bin/env python3
"""Estimate what runs would cost at API list prices, and summarize a batch.

The runs go through Claude and ChatGPT subscriptions, so these figures are
what the same token usage would cost through each provider's API, priced
from prices.yaml.

Token accounting per CLI:
- claude reports usage per model, including small background calls the
  harness makes to another model; all of them are priced. Cache writes are
  split by TTL only for the main model; writes the split doesn't account
  for, and other models' writes, are priced at the 1-hour rate, the higher
  of the two.
- codex reports one total per run. input_tokens includes cached and
  cache-write tokens, and output_tokens includes reasoning. It does not say
  which cache TTL was used, so writes are priced at the 30-minute rate; the
  summary lists cache-write tokens so the effect of that assumption is visible.

An estimate is None when usage is missing or a model has no price; that
means unknown, not free.

Usage: python3 runner/cost.py <batch>
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PRICES = yaml.safe_load((ROOT / "prices.yaml").read_text())["models"]


def usd(tokens, per_million):
    return tokens * per_million / 1_000_000


def estimate_claude(data, main_model):
    """Price a `claude -p --output-format json` result."""
    model_usage = data.get("modelUsage")
    if not model_usage or any(m not in PRICES for m in model_usage):
        return None
    by_model = {}
    split = (data.get("usage") or {}).get("cache_creation") or {}
    for model, u in model_usage.items():
        p = PRICES[model]
        five = split.get("ephemeral_5m_input_tokens", 0) if model == main_model else 0
        writes = (usd(five, p["cache_write_5m"])
                  + usd(u["cacheCreationInputTokens"] - five, p["cache_write_1h"]))
        by_model[model] = {
            "input_tokens": u["inputTokens"],
            "cache_write_tokens": u["cacheCreationInputTokens"],
            "cache_read_tokens": u["cacheReadInputTokens"],
            "output_tokens": u["outputTokens"],
            "usd": round(usd(u["inputTokens"], p["input"]) + writes
                         + usd(u["cacheReadInputTokens"], p["cache_read"])
                         + usd(u["outputTokens"], p["output"]), 6),
        }
    return by_model


def estimate_codex(usage, model):
    """Price the usage from codex's final turn.completed event."""
    if not usage or model not in PRICES:
        return None
    p = PRICES[model]
    cached = usage.get("cached_input_tokens", 0)
    written = usage.get("cache_write_input_tokens", 0)
    uncached = usage["input_tokens"] - cached - written
    return {model: {
        "input_tokens": uncached,
        "cache_write_tokens": written,
        "cache_read_tokens": cached,
        "output_tokens": usage["output_tokens"],
        "usd": round(usd(uncached, p["input"]) + usd(written, p["cache_write_30m"])
                     + usd(cached, p["cache_read"]) + usd(usage["output_tokens"], p["output"]), 6),
    }}


def total(by_model):
    return None if by_model is None else round(sum(m["usd"] for m in by_model.values()), 6)


def summarize(batch):
    batch_dir = ROOT / "outputs" / batch
    if not batch_dir.is_dir():
        sys.exit(f"no batch at {batch_dir}")
    blank = lambda: {"runs": 0, "failed": 0, "attempts": 0, "unknown": 0, "usd": 0.0,
                     "out": 0, "cache_write": 0}
    rows = defaultdict(blank)
    by_model = defaultdict(blank)
    for meta_path in sorted(batch_dir.glob("*/*/*/run-*/meta.json")):
        meta = json.loads(meta_path.read_text())
        for row in (rows[(meta["label"], meta["task"], meta["variant"])], by_model[meta["label"]]):
            row["runs"] += 1
            row["failed"] += not meta["ok"]
            for attempt_path in meta_path.parent.glob("attempt-*/attempt.json"):
                info = json.loads(attempt_path.read_text())
                row["attempts"] += 1
                if info.get("est_cost_usd") is None:
                    row["unknown"] += 1
                    continue
                row["usd"] += info["est_cost_usd"]
                for m in info["est_cost"].values():
                    row["out"] += m["output_tokens"]
                    row["cache_write"] += m["cache_write_tokens"]

    def line(name, r):
        unknown = f"  ({r['unknown']} attempts unpriced)" if r["unknown"] else ""
        return (f"{name} {r['runs']:>4} {r['failed']:>6} {r['attempts']:>8} "
                f"{r['out'] / max(r['attempts'], 1):>11,.0f} {r['usd'] / r['runs']:>10.4f} {r['usd']:>9.4f}{unknown}")

    header = f"{'Runs':>4} {'Failed':>6} {'Attempts':>8} {'Avg out tok':>11} {'Avg $/run':>10} {'Total $':>9}"
    print(f"{'Model':<20} {'Task':<22} {'Prompt':<7} {header}")
    for (label, task, variant), r in sorted(rows.items()):
        print(line(f"{label:<20} {task:<22} {variant:<7}", r))
    print(f"\n{'Model':<20} {header}")
    for label, r in sorted(by_model.items(), key=lambda kv: -kv[1]["usd"]):
        print(line(f"{label:<20}", r))

    prices = yaml.safe_load((ROOT / "prices.yaml").read_text())
    grand = sum(r["usd"] for r in by_model.values())
    writes = sum(r["cache_write"] for r in by_model.values())
    print(f"\nEstimated API cost for batch {batch}, all attempts included: ${grand:.2f}")
    print(f"List prices checked {prices['checked']}. Cache-write tokens priced by assumed TTL: {writes:,}.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    summarize(sys.argv[1])
