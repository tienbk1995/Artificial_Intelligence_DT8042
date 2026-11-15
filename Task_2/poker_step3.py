from poker_step1 import deal_hand, evaluate_hand, show, hand_name, RandomAgent
from poker_step2 import FixedAgent

HANDS_PER_GAME = 50


def play_hand(agent1, agent2):
    # 1) Card dealing
    hand1, hand2 = deal_hand(), deal_hand()
    agent1.new_hand(hand1)
    agent2.new_hand(hand2)

    # 2) Bidding phases 1-3
    bids1, bids2 = [], []
    last1, last2 = None, None
    for phase in (1, 2, 3):
        b1 = agent1.bid(phase, last2)
        b2 = agent2.bid(phase, last1)
        bids1.append(b1)
        bids2.append(b2)
        last1, last2 = b1, b2

    pot = sum(bids1) + sum(bids2)

    # 3) Showdown
    s1, s2 = evaluate_hand(hand1), evaluate_hand(hand2)
    if hasattr(agent1, "see_showdown"):
        agent1.see_showdown(hand2)
    if hasattr(agent2, "see_showdown"):
        agent2.see_showdown(hand1)

    if s1 > s2:
        net1, net2, winner = pot - sum(bids1), -sum(bids2), 1
    elif s2 > s1:
        net1, net2, winner = -sum(bids1), pot - sum(bids2), 2
    else:
        net1, net2, winner = pot / 2 - sum(bids1), pot / 2 - sum(bids2), 0

    record = {
        "hand1": show(hand1), "hand2": show(hand2),
        "score1": s1, "score2": s2,
        "bids1": bids1, "bids2": bids2,
        "pot": pot, "winner": winner,
    }
    return net1, net2, record


def play_game(agent1, agent2, n_hands=HANDS_PER_GAME):
    bankroll1 = bankroll2 = 0
    history = []
    for _ in range(n_hands):
        n1, n2, rec = play_hand(agent1, agent2)
        bankroll1 += n1
        bankroll2 += n2
        rec["bankroll1"], rec["bankroll2"] = bankroll1, bankroll2
        history.append(rec)
    return bankroll1, bankroll2, history


if __name__ == "__main__":
    a1, a2 = RandomAgent(), FixedAgent()
    b1, b2, hist = play_game(a1, a2)

    print("Pehli 3 hands:")
    for i, r in enumerate(hist[:3], 1):
        print(f"Hand {i}: A1 [{r['hand1']}] bids {r['bids1']} | "
              f"A2 [{r['hand2']}] bids {r['bids2']} | pot {r['pot']} | winner {r['winner']}")

    print("\nGame ke baad:")
    print("Random agent bankroll:", b1)
    print("Fixed agent bankroll :", b2)
    print("Difference (Random - Fixed):", b1 - b2)