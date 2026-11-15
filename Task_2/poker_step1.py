import random

SUITS = ['s', 'h', 'c', 'd']          # spade, heart, club, diamond
RANKS = list(range(2, 15))            # 2..10, J=11, Q=12, K=13, A=14
MAX_BID = 50


def make_deck():
    """52 cards ka deck. Card = (rank, suit)"""
    return [(r, s) for r in RANKS for s in SUITS]


def deal_hand():
    """Deck se 3 random cards (bina repeat ke)"""
    return random.sample(make_deck(), 3)


def evaluate_hand(hand):
    """
    Hand ka score 1..39 return karta hai:
      high card      : 1  - 13
      pair           : 14 - 26
      three of a kind: 27 - 39
    """
    ranks = sorted([c[0] for c in hand], reverse=True)

    if ranks[0] == ranks[1] == ranks[2]:
        return 26 + (ranks[0] - 1)            # three of a kind (27..39)

    if ranks[0] == ranks[1] or ranks[1] == ranks[2]:
        pair_rank = ranks[1]                  # beech wala card hamesha pair ka hota hai
        return 13 + (pair_rank - 1)           # pair (14..26)

    return ranks[0] - 1                       # high card (1..13)


def hand_name(hand):
    score = evaluate_hand(hand)
    if score >= 27:
        return "three of a kind"
    if score >= 14:
        return "pair"
    return "high card"


def show(hand):
    names = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    return ' '.join(f"{names.get(r, r)}{s}" for r, s in hand)


# ---------------- Agents ----------------
class RandomAgent:
    """2a: random bid karta hai, kisi input ko nahi dekhta"""

    def new_hand(self, hand):
        self.hand = hand                       # sensor: apna hand (dealing phase)

    def bid(self, phase, opp_last_bid=None):
        return random.randint(0, MAX_BID)


# ---------------- Quick test ----------------
if __name__ == "__main__":
    for _ in range(5):
        h = deal_hand()
        print(show(h), "->", hand_name(h), evaluate_hand(h))

    agent = RandomAgent()
    agent.new_hand(deal_hand())
    print("Random agent has 3 bids:", [agent.bid(p) for p in (1, 2, 3)])