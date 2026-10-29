#!/usr/bin/env python3
"""Prepare blind grading material for the kitchen drawings.

Collects one image per run (skipping runs a replacement batch supersedes),
copies it to grading/kitchen/<variant>/<id>.<ext> under a random id, and
writes:
  key.json         id -> run. Do not open until grading is done.
  grades.csv       one row per id with the checks to fill in.
  <variant>.html   a gallery of the images, ids only.

PNGs are shrunk to 900px wide for viewing. The original files stay in outputs/.

Usage: python3 runner/blind.py <batch> [<batch> ...]
"""

import csv
import json
import random
import shutil
import sys
from pathlib import Path

import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = ROOT / "outputs"
OUT = ROOT / "grading" / "kitchen"
SEED = 20261029


def collect(batches):
    replaced = set()
    for batch in batches:
        f = OUTPUTS / batch / "replaces.json"
        if f.exists():
            spec = json.loads(f.read_text())
            replaced |= {(spec["batch"], r) for r in spec["runs"]}
    runs = []
    for batch in batches:
        for meta_path in sorted((OUTPUTS / batch).glob("kitchen-illustration/*/*/run-*/meta.json")):
            meta = json.loads(meta_path.read_text())
            if (batch, f"kitchen-illustration/{meta['variant']}/{meta['model']}") in replaced:
                continue
            run_dir = meta_path.parent
            images = sorted(p for p in (run_dir / f"attempt-{meta['attempts']}" / "files").rglob("*")
                            if p.suffix in (".svg", ".png"))
            runs.append({"batch": batch, "variant": meta["variant"], "model": meta["model"],
                         "run": meta["run"], "images": images})
    return runs


def main(batches):
    checks = yaml.safe_load((TASK / "task.yaml").read_text())["checks"]
    rng = random.Random(SEED)
    runs = collect(batches)
    ids = [f"K{n:03d}" for n in rng.sample(range(1, 1000), len(runs))]
    rng.shuffle(runs)
    shutil.rmtree(OUT, ignore_errors=True)
    key, pages = {}, {"strong": [], "weak": []}
    for run_id, run in zip(ids, runs):
        folder = OUT / run["variant"]
        folder.mkdir(parents=True, exist_ok=True)
        shown = []
        for i, src in enumerate(run["images"]):
            name = f"{run_id}{'' if i == 0 else chr(97 + i)}{src.suffix}"
            if src.suffix == ".png":
                img = Image.open(src)
                img.thumbnail((900, 900))
                img.save(folder / name)
            else:
                shutil.copy(src, folder / name)
            shown.append(name)
        key[run_id] = {k: run[k] for k in ("batch", "variant", "model", "run")}
        key[run_id]["files"] = [str(p.relative_to(ROOT)) for p in run["images"]]
        pages[run["variant"]].append((run_id, shown))

    (OUT / "key.json").write_text(json.dumps(key, indent=2) + "\n")
    for variant, items in pages.items():
        items.sort()
        cols = (["id", "viewable"] + [f"major: {c}" for c in checks["major"]]
                + [f"minor: {c}" for c in checks["minor"]]) if variant == "strong" else ["id", "viewable", "clearly a kitchen", "clearly morning"]
        with (OUT / f"{variant}-grades.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols + ["notes"])
            for run_id, _ in items:
                w.writerow([run_id] + [""] * (len(cols) - 1) + [""])
        cells = "".join(
            f'<figure><div>{"".join(f"<img src={name!r}>".replace(chr(39), chr(34)) for name in shown)}</div>'
            f"<figcaption>{run_id}</figcaption></figure>"
            for run_id, shown in items)
        (OUT / f"{variant}.html").write_text(
            "<!doctype html><meta charset=utf-8><title>Kitchen drawings, blind</title>"
            "<style>body{font-family:sans-serif;margin:16px}"
            ".g{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}"
            "figure{margin:0}div{background:#fff;border:1px solid #ccc;border-radius:8px;overflow:hidden}"
            "img{width:100%;display:block}figcaption{font:600 13px monospace;margin-top:4px}</style>"
            f'<div class="g">{cells}</div>')
    print(f"{len(runs)} drawings -> {OUT.relative_to(ROOT)}")


TASK = ROOT / "tasks" / "kitchen-illustration"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:])
