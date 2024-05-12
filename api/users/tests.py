import random
import time
from pprint import pprint

from django.test import TestCase
from .game import get_score


class GetScoreTestCase(TestCase):
    def setUp(self) -> None:
        self.game_stamps, self.offset_lst = [], []
        game_stamps_len, self.offset_step, self.n_iter = 10**2, 3, 20
        for i in range(game_stamps_len):
            self.game_stamps.append({
                "offset": i * self.offset_step,
                "score": {
                    "home": i,
                    "away": i
                }
            })
            self.offset_lst.append(i * self.offset_step)
        self.max_offset = self.game_stamps[-1]["offset"]

    def test_existing_offset(self):
        for i in range(self.n_iter):
            offset = random.choice(self.offset_lst)
            print(offset)
            home, away = get_score(self.game_stamps, offset)
            self.assertEqual(home, offset / self.offset_step)
            self.assertEqual(away, offset / self.offset_step)

    def test_min_offset(self):
        offset = 0
        print(f'offset: {offset}, min_offset: 0')
        home, away = get_score(self.game_stamps, offset)
        self.assertEqual(home, 0)
        self.assertEqual(away, 0)
        print(f'home: {home}, away: {away}')

    def test_greater_than_max_offset(self):
        for i in range(self.n_iter):
            offset = random.randint(self.max_offset, self.max_offset + 100)
            print(f'offset: {offset}, max_offset: {self.max_offset}')
            home, away = get_score(self.game_stamps, offset)
            self.assertEqual(home, self.max_offset / self.offset_step)
            self.assertEqual(away, self.max_offset / self.offset_step)
            print(f'home: {home}, away: {away}')

    def test_not_existing_offset(self):
        for i in range(self.n_iter):
            step = random.randint(1, self.offset_step - 1)
            offset = random.choice(self.offset_lst) + step
            print(f'offset: {offset}, max_offset: {self.max_offset}')
            home, away = get_score(self.game_stamps, offset)
            self.assertEqual(home, (offset - step) / self.offset_step)
            self.assertEqual(away, (offset - step) / self.offset_step)
            print(f'home: {home}, away: {away}')
        pprint(self.game_stamps)

    def tearDown(self) -> None:
        ...


class GetScoreSpeedTestCase(TestCase):
    def setUp(self) -> None:
        self.game_stamps, self.offset_lst = [], []
        game_stamps_len, self.offset_step, self.n_iter = 10**5, 3, 50
        for i in range(game_stamps_len):
            self.game_stamps.append({
                "offset": i * self.offset_step,
                "score": {
                    "home": i,
                    "away": i
                }
            })
            self.offset_lst.append(i * self.offset_step)
        self.max_offset = self.game_stamps[-1]["offset"]

    def test_speed(self):
        worst_time = float('-inf')
        for i in range(self.n_iter):
            step = random.randint(0, self.offset_step)
            offset = random.choice(self.offset_lst) + step
            t0 = time.perf_counter()
            get_score(self.game_stamps, offset)
            t1 = time.perf_counter()
            worst_time = max(worst_time, t1 - t0)
        print(f'worst time is {worst_time}')
