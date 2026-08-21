"""のび太の手が均等なランダムかを確認する"""

import random
from collections import Counter
from main import Hand, Nobita, winning_hand

SEED = 42
TRIALS = 10000
TOLERANCE = 0.01  # 許容誤差


def judge(hands: list[Hand]) -> list[bool]:
    winner = winning_hand(set(hands))
    return [hand is winner for hand in hands]


# 手ごとの勝利条件
assert all(
    h.beats(Hand((h.value + 1) % 3)) and not h.beats(h) and not h.beats(Hand((h.value - 1) % 3))
    for h in Hand
)

# 3人以上の勝敗判定
assert judge([Hand.ROCK, Hand.ROCK, Hand.SCISSORS]) == [True, True, False]
assert judge([Hand.ROCK, Hand.SCISSORS, Hand.PAPER]) == [False, False, False]
assert judge([Hand.ROCK, Hand.ROCK]) == [False, False]


random.seed(SEED)
nobita = Nobita()
counts = Counter(nobita.hand() for _ in range(TRIALS))
rates = [counts[hand] / TRIALS for hand in Hand]

expected = 1 / len(Hand)
worst = max(rates, key=lambda rate: abs(rate - expected))
print(f"{worst * 100:.2f}% {all(abs(rate - expected) <= TOLERANCE for rate in rates)}")
