from best_players import round_robin, pd_output
from output import create_xlsx
from parse_players import parse_input
from constants import PLAYED_VARS
from ref import MatchReferee

forty_teams, players = parse_input()
games = round_robin(players, PLAYED_VARS)
df = pd_output(games)

ref = MatchReferee(forty_teams, players)
lineups = ref.parse_lineups_positions()
fixtures = ref.parse_fixtures()
results = ref.ref_all(fixtures, lineups, PLAYED_VARS)
create_xlsx(results, df)