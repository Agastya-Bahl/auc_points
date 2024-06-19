import csv
import sys
from func import *

calc_dict = {
    "GKP": calc_gkp,
    "DEF": calc_def,
    "MID": calc_mid,
    "ATT": calc_att
}

quick_sim(calc_dict, save=True)

get_participant_points(num_players=11)

print()

print()

# avg_points(calc_dict)

sys.exit()
