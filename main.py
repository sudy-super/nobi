"""じゃんけん勝敗シミュレーション"""

import random
import sys
from collections import Counter
from enum import Enum


class Hand(Enum):
    ROCK = 0
    SCISSORS = 1
    PAPER = 2

    def beats(self, other: "Hand") -> bool:
        # グー -> チョキ -> パー -> グーの順で勝つ
        return (other.value - self.value) % len(Hand) == 1


class Player:
    """hand()を別で実装すれば新しいプレイヤーを追加できる"""

    def __init__(self) -> None:
        self.wins = Counter()  # 手ごとの勝利回数
        self.plays = Counter() # 手ごとに出した回数

    @property
    def total_wins(self) -> int:
        return sum(self.wins.values())

    def hand(self) -> Hand:
        raise NotImplementedError

    def record(self, hand: Hand, won: bool) -> None:
        self.wins[hand] += won
        self.plays[hand] += 1


class Nobita(Player):
    def hand(self) -> Hand:
        return random.choice(list(Hand))


class Suneo(Player):
    def win_rate(self, hand: Hand) -> float:
        if not self.plays[hand]:
            # まだ出していない手は期待値とみなす
            return 1 / len(Hand)
        return self.wins[hand] / self.plays[hand]

    def hand(self) -> Hand:
        best = max(self.win_rate(hand) for hand in Hand)
        return random.choice([hand for hand in Hand if self.win_rate(hand) == best])


def winning_hand(kinds: set[Hand]) -> Hand | None:
    """
    出た手のうち、他の全てに勝つ手を返す
    無ければあいこ
    """
    if len(kinds) < 2:
        return None
    for hand in kinds:
        others = kinds - {hand}
        if all(hand.beats(other) for other in others):
            return hand
    return None


def play(players: list[Player], rounds: int) -> None:
    """
    あいこも1回として数え、再戦しない
    勝ち手を出した人は何人いても全員勝ち
    """
    for _ in range(rounds):
        hands = [player.hand() for player in players]
        winner = winning_hand(set(hands))
        for player, hand in zip(players, hands):
            player.record(hand, hand is winner)


if __name__ == "__main__":
    rounds = int(sys.argv[1])
    if len(sys.argv) > 2:
        random.seed(int(sys.argv[2])) # 再現したいときだけ指定する
    nobita, suneo = Nobita(), Suneo()
    play([nobita, suneo], rounds)
    print(f"N: {nobita.total_wins / rounds * 100:.2f}%")
    print(f"S: {suneo.total_wins / rounds * 100:.2f}%")
