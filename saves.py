"""
saves.py — Persistência de dados do jogo em arquivo JSON.

Armazena tentativas acumuladas e o ranking dos 10 melhores jogadores
(organizado por maior porcentagem completada).
O arquivo é salvo em save.json na raiz do projeto.
"""

import json, os

PATH = "save.json"


def _load() -> dict:
    """Carrega e retorna os dados salvos; retorna estrutura padrão se não existir."""
    if not os.path.isfile(PATH):
        return {"attempts": 0}
    try:
        with open(PATH) as f:
            return json.load(f)
    except Exception:
        return {"attempts": 0}


def _save(data: dict):
    """Persiste os dados em disco; falha silenciosamente em caso de erro."""
    try:
        with open(PATH, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def get_attempts() -> int:
    """Retorna o número total de tentativas da sessão atual."""
    return _load()["attempts"]


def increment() -> int:
    """Incrementa e salva o contador de tentativas; retorna o novo valor."""
    d = _load()
    d["attempts"] += 1
    _save(d)
    return d["attempts"]


def reset_attempts():
    """Zera o contador de tentativas (chamado ao voltar ao menu)."""
    d = _load()
    d["attempts"] = 0
    _save(d)


def get_ranking() -> list:
    """Retorna a lista de ranking salva (até 10 entradas, ordem decrescente por best_pct)."""
    return _load().get("ranking", [])


def update_player_ranking(name: str, pct: float, attempts: int):
    """
    Atualiza o ranking do jogador. Só salva se a porcentagem for maior que o recorde atual.
    Cada jogador tem apenas uma entrada; o top 10 é mantido.

    Args:
        name: Nome do jogador.
        pct: Porcentagem completada nesta partida (0–100).
        attempts: Número de tentativas usadas.
    """
    d = _load()
    ranking = d.get("ranking", [])
    existing = next((e for e in ranking if e["name"] == name), None)
    if existing is None:
        ranking.append({"name": name, "best_pct": pct, "attempts": attempts})
    elif pct > existing["best_pct"]:
        existing["best_pct"] = pct
        existing["attempts"] = attempts
    ranking.sort(key=lambda x: x["best_pct"], reverse=True)
    d["ranking"] = ranking[:10]
    _save(d)
