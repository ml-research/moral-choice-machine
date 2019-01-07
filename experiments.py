from MoralChoiceMachine import *
from data import *


""" MCM experiments """
data = mcm_overall(gender_data, occupations, False)                       # gender bias experiment
# data = mcm_overall(experimental_quests, posV_100 + negV_100, False)       # moral bias experiment

for elem in data:
    print(elem)
