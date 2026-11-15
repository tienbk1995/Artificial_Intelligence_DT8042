"""
Task 2 - Step 2: Fixed agent (2b)
Ye file poker_step1.py ke saath same folder mein honi chahiye.
"""
from Task_2.poker_step1 import deal_hand, show, hand_name, evaluate_hand, RandomAgent, MAX_BID


class FixedAgent:
    """
    2b: pehle se tay ki hui bids ki sequence chalata hai.
    Apna hand, opponent ki bid, kuch nahi dekhta.
    Har hand mein 3 bidding phases hain, to sequence mein 3 bids hain
    jo har hand mein same repeat hoti hain.
    """

    def __init__(self, bids=(25, 25, 25)):
        self.bids = bids

    def new_hand(self, hand):
        self.hand = hand                       # hand milta hai lekin use nahi hota

    def bid(self, phase, opp_last_bid=None):
        return min(self.bids[phase - 1], MAX_BID)   # phase 1, 2, 3 -> index 0, 1, 2


# ---------------- Quick test ----------------
if __name__ == "__main__":
    agent = FixedAgent()
    for _ in range(3):
        h = deal_hand()
        agent.new_hand(h)
        print(show(h), "->", hand_name(h), "| bids:", [agent.bid(p) for p in (1, 2, 3)])