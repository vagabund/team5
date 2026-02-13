import teams
from parse_players import input_path
from players import Player


class MatchReferee:
    def __init__(self, teams, players):
        self.teams = teams
        self.players = players

    def parse_fixtures(self):
        fixtures = []
        with input_path.open("r", encoding="cp1251") as f:
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
                for i in self.teams:
                    for j in self.teams:
                        if home == i.name and away == j.name:
                            fixtures.append((i, j))

                if len(fixtures) == 8:
                    break
        return fixtures

    def parse_lineups_positions(self):
        with input_path.open("r", encoding="cp1251") as f:
            lines = [line.rstrip() for line in f]

        idx = 0
        lineups = {}
        current_team = None

        while idx < len(lines):
            line = lines[idx].strip()
            idx += 1

            if not line:
                current_team = None
                continue

            for t in self.teams:
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
                for i in self.players:
                    if i.name == name:
                        lineups[current_team].append(i)
        return lineups

    def duel(self, p1: Player, p2: Player, played_vars):
        played = set(played_vars)
        s1, s2 = set(p1.predict), set(p2.predict)
        u1 = s1 - s2
        u2 = s2 - s1
        return len(u1 & played), len(u2 & played), u1&played, u2&played, s1, s2, s1&played, s2&played

    def duel_cup(self, p1: Player, p2: Player, played_vars, tier: int):
        played = set(played_vars)
        s1 = set(p1.predict_cup[tier])
        s2 = set(p2.predict_cup[tier])
        u1 = s1 - s2
        u2 = s2 - s1
        return len(u1 & played), len(u2 & played), (u1 & played), (u2 & played), s1, s2, (s1 & played), (s2 & played)

    def ref_match(self, home_team: teams.Team, away_team: teams.Team, lineups: dict, played_vars: tuple):
        home_name = home_team.name if hasattr(home_team, "name") else home_team
        away_name = away_team.name if hasattr(away_team, "name") else away_team
        home_captain = home_team.captain
        away_captain = away_team.captain

        home_players = lineups.get(home_name, [])
        away_players = lineups.get(away_name, [])


        n = min(len(home_players), len(away_players))

        home_goals = 0
        away_goals = 0
        pairs = []

        for idx in range(n):
            p_home = home_players[idx]
            p_away = away_players[idx]

            s_home, s_away, vars_home, vars_away, initial_home, initial_away, overall_home, overall_away = self.duel(p_home, p_away, played_vars)

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
                "home_overall": overall_home,
                "away_overall": overall_away,
                "initial_home": initial_home,
                "initial_away": initial_away,
                "score": (s_home, s_away),
            })

        result = {
            "home": home_name,
            "away": away_name,
            "home_captain": home_captain,
            "away_captain": away_captain,
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

    def ref_cup_match(self, home_team: teams.Team, away_team: teams.Team, lineups: dict, played_vars: tuple):
        home_name = home_team.name if hasattr(home_team, "name") else home_team
        away_name = away_team.name if hasattr(away_team, "name") else away_team
        home_captain = home_team.captain
        away_captain = away_team.captain

        home_players = lineups.get(home_name, [])
        away_players = lineups.get(away_name, [])

        n = min(len(home_players), len(away_players))

        def play_tier(tier: int):
            home_goals = 0
            away_goals = 0
            pairs = []

            for idx in range(n):
                p_home = home_players[idx]
                p_away = away_players[idx]

                s_home, s_away, vars_home, vars_away, initial_home, initial_away, overall_home, overall_away = \
                    self.duel_cup(p_home, p_away, played_vars, tier)

                if s_home > s_away:
                    home_goals += 1
                elif s_away > s_home:
                    away_goals += 1

                pairs.append({
                    "index": idx + 1,
                    "home_player": p_home.name,
                    "away_player": p_away.name,
                    "home_vars": vars_home,
                    "away_vars": vars_away,
                    "home_overall": overall_home,
                    "away_overall": overall_away,
                    "initial_home": initial_home,
                    "initial_away": initial_away,
                    "score": (s_home, s_away),
                    "tier": tier,
                })

            return home_goals, away_goals, pairs

        tier_results = []
        decided = None

        for tier in (0, 1, 2):
            hg, ag, pairs = play_tier(tier)
            tier_results.append((hg, ag, pairs))

            if hg != ag:
                decided = (tier, hg, ag, pairs)
                break

        if decided is None:
            home_sum = sum(x for x, _ in tier_results)
            away_sum = sum(y for _, y in tier_results)
            if home_sum != away_sum:
                winner = home_name if home_sum > away_sum else away_name
            else:
                winner = min(home_name, away_name)

            result = {
                "home": home_name,
                "away": away_name,
                "home_captain": home_captain,
                "away_captain": away_captain,
                "home_goals": home_sum,
                "away_goals": away_sum,
                "pairs": [],
                "mode": "cup",
                "tier": tier,
                "tier_results": tier_results,
                "winner": winner,
                "note": "forced tiebreak"
            }
            print(f"[CUP] {home_name} — {away_name}: {home_sum}–{away_sum} (forced)")
            return result

        tier, hg, ag, pairs = decided
        winner = home_name if hg > ag else away_name

        result = {
            "home": home_name,
            "away": away_name,
            "home_captain": home_captain,
            "away_captain": away_captain,
            "home_goals": hg,
            "away_goals": ag,
            "pairs": pairs,
            "mode": "cup",
            "tier_results": tier_results,
            "winner": winner,
            "decided_on_tier": tier
        }

        print(f"[CUP tier={tier}] {home_name} — {away_name}: {hg}–{ag} | winner: {winner}")
        return result

    def ref_all(self, fixtures, lineups: dict, played_vars: tuple):
        results = []
        team_name = next(iter(lineups.keys()))
        cup_check = lineups.get(team_name)[0].predict_cup[1]
        if cup_check == ():
            for home, away in fixtures:
                res = self.ref_match(home, away, lineups, played_vars)
                results.append(res)
                print()
            return results
        else:
            for home, away in fixtures:
                res = self.ref_cup_match(home, away, lineups, played_vars)
                results.append(res)
                print()
            return results

    def unpack_set(self, input_set: set):
        if len(input_set) == 0:
            return ""
        else:
            out_str = "-".join(str(x) for x in sorted(input_set))
            return out_str


