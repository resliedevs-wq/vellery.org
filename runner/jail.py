"""Run an agent CLI inside a bubblewrap jail.

Some harnesses have no working sandbox of their own: their shell commands
can reach the internet and write anywhere. In the jail the whole CLI runs
with:

- no network except relays to the model endpoints it needs;
- a read-only filesystem, writable only inside the run's own temp root;
- an empty /tmp and an empty /root, apart from the installed CLIs, so no
  credentials or personal config are readable.

Each endpoint is relayed through a Unix socket: socat outside connects to
the real host, socat inside listens on a loopback address that the jail's
/etc/hosts maps the host name to. TLS passes through untouched.
"""

import shutil
import subprocess
import tempfile
import time
from pathlib import Path

HOME = Path.home()
# Installed CLIs and their runtimes; nothing here holds credentials.
VISIBLE = [HOME / ".local/bin", HOME / ".local/node", HOME / ".local/share/zcode",
           HOME / ".local/share/magpie-agy-cli"]


def jail(cmd, root, endpoints):
    """Return (jailed command, relay processes). Stop the relays when the run ends."""
    if not (shutil.which("bwrap") and shutil.which("socat")):
        raise RuntimeError("the jail needs bubblewrap (bwrap) and socat")
    box = Path(tempfile.mkdtemp(prefix=".jail-", dir=root))
    hosts = ["127.0.0.1 localhost"]
    relays, listeners = [], []
    for i, (host, port) in enumerate(endpoints):
        sock = box / f"{i}.sock"
        local = host in ("127.0.0.1", "localhost")
        ip = "127.0.0.1" if local else f"127.0.0.{i + 2}"
        if not local:
            hosts.append(f"{ip} {host}")
        relays.append(subprocess.Popen(
            ["socat", f"UNIX-LISTEN:{sock},fork", f"TCP:{host}:{port}"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        listeners.append(f"socat TCP-LISTEN:{port},bind={ip},fork,reuseaddr UNIX-CONNECT:{sock} &")
    (box / "hosts").write_text("\n".join(hosts) + "\n")
    for i in range(len(endpoints)):
        for _ in range(50):
            if (box / f"{i}.sock").exists():
                break
            time.sleep(0.05)
    binds = ["--tmpfs", "/tmp", "--tmpfs", str(HOME)]
    for path in VISIBLE:
        if path.exists():
            binds += ["--ro-bind", str(path), str(path)]
    wrapped = [
        "bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", *binds,
        "--bind", str(root), str(root), "--ro-bind", str(box / "hosts"), "/etc/hosts",
        "--unshare-net", "--unshare-pid", "--die-with-parent", "--",
        "sh", "-c", " ".join(listeners) + ' sleep 0.3; exec "$@"', "jail", *cmd,
    ]
    return wrapped, relays


def stop(relays):
    for proc in relays:
        proc.terminate()
    for proc in relays:
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
