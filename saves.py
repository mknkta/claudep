import json, os

PATH = "save.json"

def _load():
    if not os.path.isfile(PATH): return {"attempts": 0}
    try:
        with open(PATH) as f: return json.load(f)
    except: return {"attempts": 0}

def _save(data):
    try:
        with open(PATH, "w") as f: json.dump(data, f, indent=2)
    except: pass

def get_attempts() -> int:
    return _load()["attempts"]

def increment() -> int:
    d = _load()
    d["attempts"] += 1
    _save(d)
    return d["attempts"]
