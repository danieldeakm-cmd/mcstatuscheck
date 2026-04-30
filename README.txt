# check_minecraft_server

Small utility to check whether a Minecraft server is online (uses the Minecraft status protocol).

Requirements
- Python 3.8 or newer
- Virtual environment recommended

Quick setup
1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
& .venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r "location"
```

Usage

```powershell
& "C:/Documents/My Games/games/python/.venv/Scripts/python.exe" "location"
# or check a different host:
& "C:/Documents/My Games/games/python/.venv/Scripts/python.exe" "location" example.com
```




what we plan to add:

-connect the frontend and the backend and be able to check multiple servers at once
-a database for the servers
-print a list of the mods(the file names of the mods we get from the motd object) or when we can automaticlly connect to a server get the mods that way
-install all mods needed to connect to the server
-be able to automaticly open a curseforge moded minecraft and connect to the server

what we had problem with:

-trying to "connect" to a server to see what mods we need by catching erres
-spagety code

the servers this program does not work with(as far as we know)

-below1.7
-bedrockservers