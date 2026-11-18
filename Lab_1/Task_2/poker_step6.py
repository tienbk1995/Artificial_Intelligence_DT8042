"""
Task 2 - Step 6: Agent with memory (bonus)
This file must be in the same folder as poker_step1.py ... poker_step5.py.
"""
import random
import statistics

from poker_step1 import evaluate_hand, MAX_BID, show, deal_hand
from poker_step3 import play_game
from poker_step4 import summarize
from poker_step5 import ReflexAgent


class MemoryAgent:
    """Bonus: starts from the reflex bid and adjusts it using the opponent's bids."""

    def __init__(self):
        self.opp_prev_avg = None     # memory: opponent's average bid in the previous hand
        self.opp_seen = []           # memory: opponent's bids seen in the current hand

    def new_hand(self, hand):
        # Before the new hand starts, remember the average bid of the previous hand
        if self.opp_seen:
            self.opp_prev_avg = sum(self.opp_seen) / len(self.opp_seen)
        self.opp_seen = []
        self.hand = hand

    def reflex_bid(self, score):
        # Same bids as the reflex agent
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
        # Remember the opponent's latest bid. In phase 1 there is no bid yet,
        # so we use the opponent's average bid from the previous hand.
        if opp_last_bid is not None:
            self.opp_seen.append(opp_last_bid)
            opp = opp_last_bid
        else:
            opp = self.opp_prev_avg

        score = evaluate_hand(self.hand)

        if opp is not None:
            if opp >= 35 and score <= 13:       # opponent bids high, my hand is weak
                return 5
            if opp <= 15 and score >= 14:       # opponent bids low, my hand is a pair or better
                return MAX_BID

        return self.reflex_bid(score)           # otherwise bid like the reflex agent


def run_games(cls1, cls2, n_games=100):
    """Play n_games games with new agents for every game (memory is reset between games).
    Returns the bankroll differences and the number of hands won by each agent."""
    diffs = []
    hands1 = hands2 = ties = 0
    for _ in range(n_games):
        b1, b2, hist = play_game(cls1(), cls2())
        diffs.append(b1 - b2)
        # Count the hands won in this game (winner: 1 = agent 1, 2 = agent 2, 0 = tie)
        hands1 += sum(1 for r in hist if r["winner"] == 1)
        hands2 += sum(1 for r in hist if r["winner"] == 2)
        ties += sum(1 for r in hist if r["winner"] == 0)
    return diffs, hands1, hands2, ties


def demo_hand(memory, reflex, mem_hand, ref_hand):
    """Show one hand: cards, the bids of every phase and the total pot."""
    reflex.new_hand(ref_hand)
    memory.new_hand(mem_hand)

    print("Reflex Agent:", show(ref_hand))
    print("Memory Agent:", show(mem_hand))

    pot = 0
    ref_bid = None
    mem_bid = None
    for phase in (1, 2, 3):
        new_ref = reflex.bid(phase, mem_bid)    # both agents bid at the same time
        new_mem = memory.bid(phase, ref_bid)
        ref_bid, mem_bid = new_ref, new_mem
        print(f"Phase {phase}: Reflex bids {ref_bid}, Memory bids {mem_bid}")
        pot += ref_bid + mem_bid
    print("Total pot:", pot)


if __name__ == "__main__":
    random.seed(42)      # same numbers in every run

    # 1) Demo: 3 random hands
    demo_memory = MemoryAgent()
    demo_reflex = ReflexAgent()
    for i in range(3):
        print(f"\n--- Hand {i + 1} ---")
        demo_hand(demo_memory, demo_reflex, deal_hand(), deal_hand())

    # 2) Memory agent vs Reflex agent: summary of 100 games
    print()
    diffs, hands_mem, hands_ref, hands_tie = run_games(MemoryAgent, ReflexAgent, n_games=100)
    summarize("Memory", "Reflex", diffs)

    # Standard error of the mean = std / sqrt(number of games)
    se = statistics.stdev(diffs) / len(diffs) ** 0.5
    print(f"  Standard error (std / sqrt(100)) : {se:.2f}")

    # Hands won over all games (100 games x 50 hands = 5000 hands)
    print(f"  Hands won (out of {hands_mem + hands_ref + hands_tie}): "
          f"Memory = {hands_mem}, Reflex = {hands_ref}, ties = {hands_tie}")