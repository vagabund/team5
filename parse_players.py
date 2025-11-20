import re

from players import Player
from teams import Team


def parse_block(block: str):
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    team_name = lines[0]
    captain = lines[1]
    team = Team(team_name, captain)
    players = []
    pattern = re.compile(r'^(\d+)\.\s+(.+?)\s*\(([^)]*)\)')
    for line in lines[2:]:
        m = pattern.match(line)
        if not m:
            continue
        name = m.group(2).strip()
        inside = m.group(3)
        nums = [int(x) for x in re.findall(r'\d+', inside)]
        predict = tuple(nums)
        players.append(Player(name, team, predict))
    return team, players



def parse_input():
    with open("input.txt", "r", encoding="cp1251") as f:
        content = f.read()
    raw_blocks = [b for b in content.split("\n\n") if b.strip()]
    team_blocks = raw_blocks[1:]
    teams = []
    all_players = []
    for block in team_blocks:
        team, players = parse_block(block)
        teams.append(team)
        all_players.extend(players)
    return teams, all_players