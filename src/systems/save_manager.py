# save_manager.py — lê e grava save.json na raiz do projeto
import json
import os

SAVE_PATH = "save.json"
_DEFAULT  = {"attempts": 0}


def load() -> dict:
    if not os.path.isfile(SAVE_PATH):
        return dict(_DEFAULT)
    try:
        with open(SAVE_PATH, encoding="utf-8") as f:
            data = json.load(f)
        # Garante que todos os campos existem.
        for k, v in _DEFAULT.items():
            data.setdefault(k, v)
        return data
    except (json.JSONDecodeError, OSError):
        return dict(_DEFAULT)


def save(data: dict):
    try:
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError:
        pass


def increment_attempts() -> int:
    data = load()
    data["attempts"] += 1
    save(data)
    return data["attempts"]


def get_attempts() -> int:
    return load()["attempts"]
