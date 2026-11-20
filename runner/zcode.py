"""Run Z.ai's official Agent CLI with an isolated provider and workspace."""
import json
import os


def run_zcode(model, prompt, workdir, execute):
    home = workdir.parent / "home"
    config_dir = home / ".zcode" / "cli"
    config_dir.mkdir(parents=True)
    provider_file = home / "provider.json"
    model_id = model["id"]
    provider = {
        "providerId": "zai-api", "providerName": "Z.ai Coding Plan",
        "config": {
            "group": "standard-personal",
            "access": {"type": "api-key", "apiKey": os.environ["ZAI_API_KEY"]},
            "api": {"type": "openai-chat-completions", "baseUrl": "https://api.z.ai/api/coding/paas/v4"},
            "personalModelIds": [model_id],
        },
    }
    selection = {"providerId": "zai-api", "modelId": model_id,
                 "options": {"reasoningLevel": model["effort"]}}
    provider_file.touch(mode=0o600)
    provider_file.write_text(json.dumps({"schemaVersion": 1, "config": {
        "providerConfigRules": {"providerRules": [provider]},
        "modelConfigRules": {"providerModelRules": [], "manualProviderModelRules": []},
        "defaultModelSelection": selection,
    }}))
    (config_dir / "config.json").write_text(json.dumps({
        "features": dict.fromkeys(("mcp", "subagent", "memory", "skill"), False),
        "plugins": {"enabled": False}, "skills": {"enabled": False}, "hooks": {"enabled": False},
    }))
    # Headless edit mode refuses Bash ("No permission client configured").
    # yolo, the CLI's default for --prompt, is safe because the run is jailed.
    cmd = ["zcode", "--prompt", prompt, "--cwd", str(workdir), "--mode", "yolo",
           "--disallowed-tools", "WebSearch WebFetch Browser AskUserQuestion EnterPlanMode ExitPlanMode",
           "--output-format", "json", "--no-color"]
    env = {"HOME": str(home), "PATH": os.environ["PATH"], "ZCODE_DATA_BASE_DIR": str(home),
           "ZCODE_PERSONAL_PROVIDER_CONFIG_FILE": str(provider_file)}
    code, out, err, error = execute(cmd, cwd=workdir, env=env)
    try:
        data = json.loads(out)
    except ValueError:
        data = {}
    response = data.get("response", "")
    if code != 0 or not response:
        error = error or "ZCode did not return a final response"
    return {"command": cmd[:2] + ["<prompt>"] + cmd[3:], "raw": out, "stderr": err,
            "error": error, "response": response, "usage": data.get("usage")}
