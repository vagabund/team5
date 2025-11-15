from pathlib import Path
import teams
from constants import PLAYED_VARS
from players import players, Player


class MatchReferee:
    def __init__(self):
        pass

    def parse_fixtures(self):
        fixtures = []
        path = Path("input.txt")

        with path.open("r", encoding="cp1251") as f:
            for line in f:
                line = line.strip()

                if not line:
                    if fixtures:
                        break
                    else:
                        continue

                if "-" not in line:
                    continue

                home, away = map(str.strip, line.split("-", 1))
                for i in teams.teams:
                    for j in teams.teams:
                        if home == i.name and away == j.name:
                            fixtures.append((i.name, j.name))

                if len(fixtures) == 8:
                    break
        return fixtures

    def parse_lineups_positions(self):
        path = Path("input.txt")

        with path.open("r", encoding="cp1251") as f:
            lines = [line.rstrip() for line in f]

        fixtures_seen = 0
        idx = 0
        while idx < len(lines):
            if "-" in lines[idx]:
                fixtures_seen += 1
            if fixtures_seen == 8 and lines[idx].strip() == "":
                idx += 1
                break
            idx += 1

        lineups = {}
        current_team = None

        while idx < len(lines):
            line = lines[idx].strip()
            idx += 1

            if not line:
                current_team = None
                continue

            for t in teams.teams:
                if t.name == line:
                    current_team = t.name
                    lineups[current_team] = []
                    break
            else:
                if current_team is None:
                    continue

                stripped = line.lstrip()
                if not stripped or not stripped[0].isdigit():
                    continue

                dot = line.find(".")
                lpar = line.find("(")
                if dot == -1 or lpar == -1:
                    continue

                name = line[dot + 1:lpar].strip()
                for i in players:
                    if i.name == name:
                        lineups[current_team].append(i)
        return lineups

    def duel(self, p1: Player, p2: Player, played_vars):
        played = set(played_vars)
        s1, s2 = set(p1.predict), set(p2.predict)
        u1 = s1 - s2
        u2 = s2 - s1
        return len(u1 & played), len(u2 & played), u1&played, u2&played, s1, s2

    def ref_match(self, home_team: teams.Team, away_team: teams.Team, lineups: dict, played_vars: tuple):
        home_name = home_team.name if hasattr(home_team, "name") else home_team
        away_name = away_team.name if hasattr(away_team, "name") else away_team

        home_players = lineups.get(home_name, [])
        away_players = lineups.get(away_name, [])


        n = min(len(home_players), len(away_players))

        home_goals = 0
        away_goals = 0
        pairs = []

        for idx in range(n):
            p_home = home_players[idx]
            p_away = away_players[idx]

            s_home, s_away, vars_home, vars_away, initial_home, initial_away = self.duel(p_home, p_away, played_vars)

            if s_home > s_away:
                home_goals += 1

            if s_away > s_home:
                away_goals += 1

            pairs.append({
                "index": idx + 1,
                "home_player": p_home.name,
                "away_player": p_away.name,
                "home_vars": vars_home,
                "away_vars": vars_away,
                "initial_home": initial_home,
                "initial_away": initial_away,
                "score": (s_home, s_away),
            })

        result = {
            "home": home_name,
            "away": away_name,
            "home_goals": home_goals,
            "away_goals": away_goals,
            "pairs": pairs,
        }

        print(f"{home_name} — {away_name}: {home_goals}–{away_goals}")
        for p in pairs:
            h, a = p["home_player"], p["away_player"]
            h_vars, a_vars = p["home_vars"], p["away_vars"]
            initial_home, initial_away = p["initial_home"], p["initial_away"]
            sh, sa = p["score"]
            print(f"  {p['index']}. {h} ({self.unpack_set(initial_home)}) ({self.unpack_set(h_vars)}) {sh}:{sa} {a} ({self.unpack_set(initial_away)}) ({self.unpack_set(a_vars)})")

        return result

    def ref_all(self, fixtures, lineups: dict, played_vars: tuple):
        results = []
        for home, away in fixtures:
            res = self.ref_match(home, away, lineups, played_vars)
            results.append(res)
            print()
        return results

    def unpack_set(self, input_set: set):
        if len(input_set) == 0:
            return ""
        else:
            out_str = "-".join(str(x) for x in sorted(input_set))
            return out_str

for p in players:
    p.update_predict()
ref = MatchReferee()
lineups = ref.parse_lineups_positions()
fixtures = ref.parse_fixtures()
results = ref.ref_all(fixtures, lineups, PLAYED_VARS)

