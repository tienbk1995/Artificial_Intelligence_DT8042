"""
Task 2 - Step 5: Reflex agent (2e)

"""
from poker_step1 import evaluate_hand, RandomAgent, MAX_BID
from poker_step2 import FixedAgent
from poker_step4 import run_experiment, summarize


class ReflexAgent:
    """2e: it uses the strength of its own hand to decide its bid (no memory)."""

    def new_hand(self, hand):
        self.hand = hand

    def bid(self, phase, opp_last_bid=None):
        score = evaluate_hand(self.hand)    # hand score 1..39
        if score <= 7:                      # weak high card
            return 5
        elif score <= 13:                   # strong high card
            return 15
        elif score <= 20:                   # low pair
            return 30
        elif score <= 26:                   # high pair
            return 40
        else:                               # three of a kind
            return MAX_BID


if __name__ == "__main__":
    reflex = ReflexAgent()

    diffs = run_experiment(reflex, RandomAgent(), n_games=100)
    summarize("Reflex", "Random", diffs)

    print()

    diffs = run_experiment(reflex, FixedAgent(), n_games=100)
    summarize("Reflex", "Fixed", diffs)