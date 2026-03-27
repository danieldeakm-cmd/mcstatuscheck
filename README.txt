# check_minecraft_server

Small utility to check whether a Minecraft server is online (uses the Minecraft status protocol).

Requirements
- Python 3.8 or newer
- Virtual environment recommended
- See `requirements.txt` for Python dependencies (`mcstatus`, `dnspython`)

Quick setup
1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
& .venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r "c:\Documents\My Games\games\python\requirements.txt"
```

Usage

```powershell
& "C:/Documents/My Games/games/python/.venv/Scripts/python.exe" "C:/Documents/My Games/games/python/check_minecraft_server.py"
# or check a different host:
& "C:/Documents/My Games/games/python/.venv/Scripts/python.exe" "C:/Documents/My Games/games/python/check_minecraft_server.py" example.com
```

Behavior notes
- The script prefers the Minecraft protocol query (via `mcstatus`) and will report `ON` only when a proper Minecraft protocol response is received.
- If the Minecraft protocol query fails but the server's TCP port `25565` is open the script will report `STARTING` (TCP open but no protocol response). Exit code `2` is returned for this state.
- If `mcstatus` is not available the script falls back to a TCP connect to port `25565`. By default a TCP-open result is treated as `STARTING` (exit code `2`) to avoid false `ON` reports; use the script with `mcstatus` installed for reliable `ON` detection.
-- After a successful Minecraft protocol response the script by default verifies TCP connectivity to the resolved address/port before reporting `ON`. This avoids cases where a monitoring front-end reports the server online while the game port is unreachable.
-- Flags:
	- `--no-tcp`: do not require TCP verification after protocol success (looser checks).
	- `--protocol-retries N`: number of protocol query attempts used for majority vote (default 3).
	- `--tcp-retries N`: number of TCP connect attempts used for majority vote (default 3).
	- `--delay S`: delay in seconds between retries (default 0.5).
	 - `--no-tcp`: do not require TCP verification after protocol success (looser checks).
	 - `--protocol-retries N`: number of protocol query attempts used for majority vote (default 1).
	 - `--tcp-retries N`: number of TCP connect attempts used for majority vote (default 1).
	 - `--consecutive N`: require N consecutive successful protocol+TCP checks before reporting `ON` (default 0 = disabled).
	 - `--delay S`: delay in seconds between retries (default 0.5).
	 - `--protocol-retries N`: number of protocol query attempts used for majority vote (default 1).
	 - `--tcp-retries N`: number of TCP connect attempts used for majority vote (default 1).
	 - `--consecutive N`: require N consecutive successful protocol+TCP checks before reporting `ON` (default 0 = disabled).
	 - `--delay S`: delay in seconds between retries (default 0.5).
	 - `--dump-status`: print the raw mcstatus protocol response and resolved address to help debug false positives.
	 - `--consecutive N`: require N consecutive successful protocol+TCP checks before reporting `ON` (default 0 = disabled).
	 - `--motd-blacklist`: add a substring to treat as OFF if present in the server MOTD (case-insensitive). This defaults to common Aternos text like `"This server is offline"`. Provide this flag multiple times to add entries.
	 - `--delay S`: delay in seconds between retries (default 0.5).
	 - `--dump-status`: print the raw mcstatus protocol response and resolved address to help debug false positives.
-- Exit codes: `0` = ON, `1` = OFF, `2` = STARTING.

If you want a `--force-tcp` option or additional output formats (JSON), tell me and I will add them.