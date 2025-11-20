import pandas as pd

from players import Player


def duel(p1: Player, p2: Player, played_vars: tuple):
    played = set(played_vars)
    s1, s2 = set(p1.predict), set(p2.predict)
    u1 = s1 - s2
    u2 = s2 - s1
    p1_for = len(u1 & played)
    p2_for = len(u2 & played)
    return p1_for, p2_for

def round_robin(players: list, played_vars: tuple):
    stats = {
        p.name: {
            "team": p.team.name,
            "games": 0, "wins": 0, "draws": 0, "losses": 0,
            "for": 0, "against": 0, "diff": 0,
            "avg_for": 0.0, "avg_against": 0.0, "avg_diff": 0.0,
            "win_rate": 0.0, "points": 0
        }
        for p in players
    }

    n = len(players)
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = players[i], players[j]
            if p1.predict == () or p2.predict == ():
                continue
            if p1.team == p2.team:
                continue
            s1, s2 = duel(p1, p2, played_vars)
            st1 = stats[p1.name]
            st2 = stats[p2.name]

            st1["games"] += 1
            st1["for"] += s1
            st1["against"] += s2
            if s1 > s2:
                st1["wins"] += 1
                st1["points"] += 3
            elif s1 == s2:
                st1["draws"] += 1
                st1["points"] += 1
            else:
                st1["losses"] += 1

            st2["games"] += 1
            st2["for"] += s2
            st2["against"] += s1
            if s2 > s1:
                st2["wins"] += 1
                st2["points"] += 3
            elif s2 == s1:
                st2["draws"] += 1
                st2["points"] += 1
            else:
                st2["losses"] += 1

    for st in stats.values():
        g = st["games"]
        if g > 0:
            st["diff"] = st["for"] - st["against"]
            st["avg_for"] = round((st["for"] / g), 2)
            st["avg_against"] = round((st["against"] / g), 2)
            st["avg_diff"] = round((st["diff"] / g), 2)
            st["win_rate"] = round((st["wins"] / g), 2)

    return stats

def rank_players(stats: dict):
    return sorted(
        stats.items(),
        key=lambda kv: (
            kv[1]["points"],
            kv[1]["win_rate"],
            kv[1]["avg_diff"],
            kv[1]["avg_for"],
            -ord(kv[0][0])
        ),
        reverse=True
    )


def pd_output(stats: dict):
    df = pd.DataFrame.from_dict(stats, orient="index")
    df_sorted = df.sort_values(by=["points", "win_rate", "avg_for", "avg_diff"], ascending=False)
    df_sorted = df_sorted.reset_index(names="player")
    df_sorted.columns = ["Игрок", "Команда", "Игры", "Победы", "Ничьи", "Поражения", "Забито", "Пропущено", "Разница", "Забито в среднем", "Пропущено в среднем", "Средняя разница", "Винрейт", "Очки"]
    print(df_sorted.head(15).to_string(index=True))
    return df_sorted