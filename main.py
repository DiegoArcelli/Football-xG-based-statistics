import numpy as np
from tqdm import tqdm
from plot_utils import *
import argparse
from scraping import get_game_info

parser = argparse.ArgumentParser(description='.')
parser.add_argument('--url', default="https://fbref.com/it/partite/a315e1cc/Milan-Lazio-30-Settembre-2023-Serie-A", type=str)
parser.add_argument('--reference_stat', default="xg", type=str)
parser.add_argument('--iterations', default=10000, type=int)
parser.add_argument('--plots', action="store_true")

args = parser.parse_args()

assert args.reference_stat in ["xg", "xgot"], "--reference_stat arguments must be 'xg' or 'xgot'"

ref_stat = "xG" if args.reference_stat == "xg" else "xGoT"
n_iters = args.iterations

game_info = get_game_info(args.url)


HOME_TEAM = game_info["home_team"]["name"]
AWAY_TEAM = game_info["away_team"]["name"]

home_team_shot_info = game_info["home_team"][args.reference_stat]
away_team_shot_info = game_info["away_team"][args.reference_stat]

home_sum = 0.0
home_team_cum_xgs = [(0, 0.0)]
for shot in home_team_shot_info:
    minute = shot["minute"]
    xg = shot[args.reference_stat]
    home_team_cum_xgs.append((minute, home_sum))
    home_sum += xg
    home_team_cum_xgs.append((minute, home_sum))
    
away_sum = 0.0
away_team_cum_xgs = [(0, 0.0)]
for shot in away_team_shot_info:
    minute = shot["minute"]
    xg = shot[args.reference_stat]
    away_team_cum_xgs.append((minute, away_sum))
    away_sum += xg
    away_team_cum_xgs.append((minute, away_sum))

last_minute = max(away_team_shot_info[-1]["minute"], home_team_shot_info[-1]["minute"])
home_team_cum_xgs.append((last_minute, home_sum))
away_team_cum_xgs.append((last_minute, away_sum))

if args.plots:
    get_time_line(home_team_cum_xgs, away_team_cum_xgs, HOME_TEAM, AWAY_TEAM, ref_stat)

home_team_xgs = list(map(lambda x: x[args.reference_stat], home_team_shot_info))
away_team_xgs = list(map(lambda x: x[args.reference_stat], away_team_shot_info))


home_team_total_xgs = sum(home_team_xgs)
away_team_total_xgs = sum(away_team_xgs)

results = []

outcomes_count = {
    HOME_TEAM: 0,
    AWAY_TEAM: 0,
    "draw": 0
}

results_count = {}
goal_diff_count = {}
goal_diff_dist = {}

with tqdm(total=n_iters) as pbar:
    for iter in range(n_iters):
        home_team_goals = sum([np.random.binomial(1, xg, 1)[0] for xg in home_team_xgs])
        away_team_goals = sum([np.random.binomial(1, xg, 1)[0] for xg in away_team_xgs])
        
        result = {
            HOME_TEAM: home_team_goals,
            AWAY_TEAM: away_team_goals
        }

        key = f"{home_team_goals}-{away_team_goals}"
        goal_diff = home_team_goals - away_team_goals

        results_count[key] = 1 if key not in results_count.keys() else results_count[key]+1
        goal_diff_count[goal_diff] = 1 if goal_diff not in goal_diff_count.keys() else goal_diff_count[goal_diff]+1

        if result[HOME_TEAM] > result[AWAY_TEAM]:
            outcomes_count[HOME_TEAM] += 1
        elif result[HOME_TEAM] < result[AWAY_TEAM]:
            outcomes_count[AWAY_TEAM] += 1
        else:
            outcomes_count["draw"] += 1


        results.append(result)

        pbar.update(1)

print(f"\n{HOME_TEAM}-{AWAY_TEAM} {ref_stat}: {round(home_team_total_xgs, 3)}-{round(away_team_total_xgs, 3)}\n")


home_team_xp = (3*outcomes_count[HOME_TEAM] + outcomes_count["draw"])/n_iters
away_team_xp = (3*outcomes_count[AWAY_TEAM] + outcomes_count["draw"])/n_iters
print(f"{HOME_TEAM} xPoints: {round(home_team_xp, 3)}")   
print(f"{AWAY_TEAM} xPoints: {round(away_team_xp, 3)}\n")  


outcomes_dist =  {outcome: count/n_iters for outcome, count in outcomes_count.items()}
print(f"{HOME_TEAM} wins: {outcomes_count[HOME_TEAM]} ({round(outcomes_dist[HOME_TEAM], 5)*100}%)")
print(f"{AWAY_TEAM} wins: {outcomes_count[AWAY_TEAM]} ({round(outcomes_dist[AWAY_TEAM], 5)*100}%)")
print(f"Draws: {outcomes_count['draw']} ({round(outcomes_dist['draw'], 5)*100}%)\n")


results_count = dict(sorted(results_count.items(), key=lambda x:x[1], reverse=True))
results_dist = {result: count/n_iters for result, count in results_count.items()}
for result in results_count.keys():
    count = results_count[result]
    perc = results_dist[result]*100
    print(f"{HOME_TEAM}-{AWAY_TEAM}: {result}, {count} times ({round(perc, 5)}%)")
print()


goal_diff_count = dict(sorted(goal_diff_count.items(), key=lambda x:x[0], reverse=True))
goal_diff_dist = {diff: count/n_iters for diff, count in goal_diff_count.items()}
for diff in goal_diff_count.keys():
    count = goal_diff_count[diff]
    perc = goal_diff_dist[diff]*100
    diff_str = str(diff) if diff <= 0 else f"+{diff}"
    print(f"{diff_str}, {count} times ({round(perc, 5)}%)")

if args.plots:
    get_single_bar_plot(
        outcomes_dist.keys(),
        outcomes_dist.values(),
        "Outcomes distribution",
    )

    get_bar_plot(
        results_dist.keys(),
        results_dist.values(),
        "Results distribution",
        "Result",
        "Probability"
    )

    get_bar_plot(
        goal_diff_dist.keys(),
        goal_diff_dist.values(),
        "Goals difference distribution",
        "Goals differnece",
        "Probability"
    )
