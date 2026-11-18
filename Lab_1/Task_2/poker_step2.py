"""
Task 2 - Step 2: Fixed agent (2b)

"""
from poker_step1 import deal_hand, show, hand_name, evaluate_hand, RandomAgent, MAX_BID


class FixedAgent:
    """
    2b: follows a pre-defined sequence of bids.
    It ignores its own hand and the opponent's bids.
    Each hand has 3 bidding phases, so the sequence contains 3 bids,
    and the same 3 bids are repeated in every hand.
    """

    def __init__(self, bids=(25, 25, 25)):
        self.bids = bids

    def new_hand(self, hand):
        self.hand = hand                       # the hand is received but never used for bidding

    def bid(self, phase, opp_last_bid=None):
        return min(self.bids[phase - 1], MAX_BID)   # phase 1, 2, 3 -> index 0, 1, 2


# ---------------- Quick test ----------------
if __name__ == "__main__":
    # Deal 3 hands and print the (always identical) bids of the fixed agent
    agent = FixedAgent()
    for _ in range(3):
        h = deal_hand()
        agent.new_hand(h)
        print(show(h), "->", hand_name(h), "| bids:", [agent.bid(p) for p in (1, 2, 3)])