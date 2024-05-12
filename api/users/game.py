import time
from pprint import pprint
import random
import math

TIMESTAMPS_COUNT = 50000

PROBABILITY_SCORE_CHANGED = 0.0001

PROBABILITY_HOME_SCORE = 0.45

OFFSET_MAX_STEP = 3

INITIAL_STAMP = {
    "offset": 0,
    "score": {
        "home": 0,
        "away": 0
    }
}


def generate_stamp(previous_value):
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED
    home_score_change = 1 if score_changed and random.random() > 1 - \
        PROBABILITY_HOME_SCORE else 0
    away_score_change = 1 if score_changed and not home_score_change else 0
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change
        }
    }


def generate_game():
    stamps = [INITIAL_STAMP, ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps


game_stamps = generate_game()

# pprint(game_stamps)
# print(len(game_stamps))


def get_score(game_stamps, offset):
    '''
        Takes list of game's stamps and time offset for which returns the scores for the home and away teams.
        Please pay attention to that for some offsets the game_stamps list may not contain scores.
    '''
    home, away = 0, 0
    # for i in game_stamps:
    #     if i['offset'] == offset:
    #         home, away = i['score']['home'], i['score']['away']
    #         print(home, away)
    n = len(game_stamps)
    off = None
    l, r = 0, n - 1
    while l <= r:
        m = math.floor((l + r) / 2)
        if game_stamps[m]['offset'] == offset:
            off = game_stamps[m]['offset']
            home, away = game_stamps[m]['score']['home'], game_stamps[m]['score']['away']
            #print(home, away)
            break
        elif game_stamps[m]['offset'] < offset:
            l = m + 1
        else:
            r = m - 1

        if l > r and l != 0:
            off = game_stamps[r]['offset']
            home, away = game_stamps[r]['score']['home'], game_stamps[r]['score']['away']

    #print('offset', off)
    return home, away


# t0 = time.perf_counter()
# print(get_score(game_stamps, 98837))
# t1 = time.perf_counter()
# print(t1-t0)