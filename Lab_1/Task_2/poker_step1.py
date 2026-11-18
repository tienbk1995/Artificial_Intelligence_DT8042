import random

SUITS = ['s', 'h', 'c', 'd']          # spade, heart, club, diamond
RANKS = list(range(2, 15))            # 2..10, J=11, Q=12, K=13, A=14
MAX_BID = 50                          # maximum bid per bidding phase


def make_deck():
    """Return a deck of 52 cards. Each card is a (rank, suit) tuple."""
    return [(r, s) for r in RANKS for s in SUITS]


def deal_hand():
    """Deal 3 random cards from the deck (without replacement)."""
    return random.sample(make_deck(), 3)


def evaluate_hand(hand):
    """
    Return a hand score from 1 to 39:
      high card       : 1  - 13
      pair            : 14 - 26
      three of a kind : 27 - 39
    """
    ranks = sorted([c[0] for c in hand], reverse=True)

    if ranks[0] == ranks[1] == ranks[2]:
        return 26 + (ranks[0] - 1)            # three of a kind (27..39)

    if ranks[0] == ranks[1] or ranks[1] == ranks[2]:
        pair_rank = ranks[1]                  # the middle card always belongs to the pair
        return 13 + (pair_rank - 1)           # pair (14..26)

    return ranks[0] - 1                       # high card (1..13)


def hand_name(hand):
    """Return the hand type as text, based on its score."""
    score = evaluate_hand(hand)
    if score >= 27:
        return "three of a kind"
    if score >= 14:
        return "pair"
    return "high card"


def show(hand):
    """Return the hand as readable text, e.g. 'Ks 10h 4c'."""
    names = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
    return ' '.join(f"{names.get(r, r)}{s}" for r, s in hand)


# ---------------- Agents ----------------
class RandomAgent:
    """2a: bids a random amount and ignores all input."""

    def new_hand(self, hand):
        self.hand = hand                       # sensor: own hand (dealing phase), not used for bidding

    def bid(self, phase, opp_last_bid=None):
        return random.randint(0, MAX_BID)      # any amount from $0 to $50


# ---------------- Quick test ----------------
if __name__ == "__main__":
    # Deal 5 random hands and print their type and score
    for _ in range(5):
        h = deal_hand()
        print(show(h), "->", hand_name(h), evaluate_hand(h))

    # Check that the random agent gives 3 valid bids (one per bidding phase)
    agent = RandomAgent()
    agent.new_hand(deal_hand())
    print("Random agent has 3 bids:", [agent.bid(p) for p in (1, 2, 3)])