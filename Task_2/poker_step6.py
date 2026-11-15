from Task_2.poker_step1 import evaluate_hand, MAX_BID
from Task_2.poker_step5 import ReflexAgent
from Task_2.poker_step4 import run_experiment, summarize


class MemoryAgent:
    """Bonus: apne hand ki strength + opponent ki bids (memory) dono use karta hai."""

    def __init__(self):
        self.opp_prev_avg = None     # opponent ki pichli hand ki average bid (memory)
        self.opp_seen = []           # is hand mein opponent ki dekhi hui bids

    def new_hand(self, hand):
        # nayi hand shuru hone se pehle, pichli hand ki average yaad rakho
        if self.opp_seen:
            self.opp_prev_avg = sum(self.opp_seen) / len(self.opp_seen)
        self.opp_seen = []
        self.hand = hand

    def base_bid(self, score):
        # wahi reflex wali bids
        if score <= 7:
            return 5
        elif score <= 13:
            return 15
        elif score <= 20:
            return 30
        elif score <= 26:
            return 40
        return MAX_BID

    def bid(self, phase, opp_last_bid=None):
        if opp_last_bid is not None:
            self.opp_seen.append(opp_last_bid)

        score = evaluate_hand(self.hand)
        bid = self.base_bid(score)

        # opponent ki taqat ka andaza: abhi ki bid, warna pichli hand ki average
        if opp_last_bid is not None:
            opp = opp_last_bid
        else:
            opp = self.opp_prev_avg

        if opp is not None:
            if opp >= 35 and score <= 13:      # opponent strong lag raha, mera hand weak
                bid = 5
            elif opp <= 15 and score >= 14:    # opponent weak lag raha, mera hand achha
                bid = MAX_BID
        return bid


if __name__ == "__main__":
    memory = MemoryAgent()
    reflex = ReflexAgent()

    diffs = run_experiment(memory, reflex, n_games=100)
    summarize("Memory", "Reflex", diffs)