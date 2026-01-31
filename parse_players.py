import re
import sys
from pathlib import Path

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
        predict, predict_cups = parse_predict(inside)
        players.append(Player(name, team, predict, predict_cups))
    return team, players

def parse_predict(block: str):
    block = block.strip()
    if "/" in block:
        parts = block.split("/")
        while len(parts) < 3:
            parts.append("")
        t1 = tuple(int(x) for x in re.findall(r"\d+", parts[0]))
        t2 = tuple(int(x) for x in re.findall(r"\d+", parts[1]))
        t3 = tuple(int(x) for x in re.findall(r"\d+", parts[2]))
        return t1, (t1, t2, t3)
    vars = tuple(int(x) for x in re.findall(r"\d+", block))
    return vars, (vars, (), ())

def get_input_path():
    filename = "input.txt"
    if getattr(sys, "frozen", False):
        exe_path = Path(sys.argv[0]).resolve()
        app_bundle = exe_path.parents[2] if exe_path.name != filename else exe_path.parent
        app_folder = app_bundle.parent
        external = app_folder / filename
        if external.exists():
            return external
        else:
            return None
    else:
       script_dir = Path(__file__).resolve().parent
       return script_dir / filename

input_path = get_input_path()

def parse_input():
    with input_path.open("r", encoding="cp1251") as f:
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