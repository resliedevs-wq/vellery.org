#!/usr/bin/env python3
"""Run a command with this machine's provider credentials in its environment.

    python3 runner/provider_env.py python3 runner/run.py BATCH --model MODEL

Reads the keys from the local Magpie gateway's config, never prints them,
and passes them only to the command it starts:

  DEEPSEEK_API_KEY   ~/.config/magpie/providers.json, provider "deepseek"
  ZAI_API_KEY        ~/.config/magpie/providers.json, provider "zai"
  MAGPIE_BASE_URL    the Magpie route in ~/.dsh/profiles/superagent/magpie.patch.yml
  MAGPIE_API_KEY     (the same route's caller key)
  PATH               gains ~/.local/share/magpie-agy-cli, the pinned official agy

Claude and Codex use their own logins and need nothing from here.
"""

import json
import os
import sys
from pathlib import Path

import yaml

HOME = Path.home()


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    env = dict(os.environ)
    providers = {p["id"]: p for p in json.loads((HOME / ".config/magpie/providers.json").read_text())["providers"]}
    for var, pid in (("DEEPSEEK_API_KEY", "deepseek"), ("ZAI_API_KEY", "zai")):
        if providers.get(pid, {}).get("key"):
            env.setdefault(var, providers[pid]["key"])
    patch = HOME / ".dsh/profiles/superagent/magpie.patch.yml"
    if patch.exists():
        route = yaml.safe_load(patch.read_text())[0]["config"]["providers"]["magpie"]
        env.setdefault("MAGPIE_BASE_URL", route["baseURL"].removesuffix("/v1"))
        env.setdefault("MAGPIE_API_KEY", route["headers"]["authorization"].split()[-1])
    env["PATH"] = f"{HOME / '.local/share/magpie-agy-cli'}:{env['PATH']}"
    os.execvpe(sys.argv[1], sys.argv[1:], env)


if __name__ == "__main__":
    main()
